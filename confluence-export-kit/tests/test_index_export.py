from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "index-export"
    / "scripts"
    / "index_export.py"
)


def load_index_export_module():
    spec = importlib.util.spec_from_file_location("index_export", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IndexExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_index_export_module()
        self.tmp = Path(self._testMethodName)
        if self.tmp.exists():
            self._remove_tree(self.tmp)
        self.tmp.mkdir()

    def tearDown(self) -> None:
        if self.tmp.exists():
            self._remove_tree(self.tmp)

    def _remove_tree(self, path: Path) -> None:
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            else:
                child.rmdir()
        path.rmdir()

    def write_source(self, root_name: str, relative_path: str, content: str) -> Path:
        path = self.tmp / root_name / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def read_jsonl(self, path: Path) -> list[dict[str, object]]:
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

    def test_indexes_export_into_source_namespace_and_agent_rules(self) -> None:
        export_root = self.tmp / "Product Team Space"
        self.write_source(
            "Product Team Space",
            "Product Department/Colonova Product/상위 설계서/PRD.md",
            "# PRD\n\n## Goals\n\nProduct direction text.",
        )
        self.write_source(
            "Product Team Space",
            "Product Department/Colonova Product/아카이브 ONLY/old.md",
            "# Old Policy\n\nArchived text.",
        )

        exit_code = self.module.main(
            [
                str(export_root),
                "--index-root",
                str(self.tmp / ".confluence-index"),
                "--agent-files",
                str(self.tmp / "AGENTS.md"),
                str(self.tmp / "CLAUDE.md"),
            ]
        )

        self.assertEqual(exit_code, 0)
        source_root = self.tmp / ".confluence-index" / "sources" / "product-team-space"
        self.assertTrue((source_root / "source-index.jsonl").exists())
        entries = self.read_jsonl(source_root / "source-index.jsonl")
        self.assertEqual([entry["title"] for entry in entries], ["Old Policy", "PRD"])
        self.assertEqual(entries[0]["status"], "archive")
        self.assertEqual(entries[1]["source_type"], "prd")

        registry = json.loads((self.tmp / ".confluence-index" / "registry.json").read_text())
        self.assertEqual(registry["sources"][0]["source_id"], "product-team-space")
        self.assertEqual(registry["sources"][0]["file_count"], 2)

        agents = (self.tmp / "AGENTS.md").read_text()
        claude = (self.tmp / "CLAUDE.md").read_text()
        self.assertIn(".confluence-index/registry.json", agents)
        self.assertIn("confluence-export-kit:reading-rule:start", claude)

    def test_repeated_indexes_keep_sources_separate(self) -> None:
        product_root = self.tmp / "Product Team Space"
        dev_root = self.tmp / "Dev Team Space"
        self.write_source("Product Team Space", "Feature List.md", "# Feature List\n")
        self.write_source("Dev Team Space", "Architecture.md", "# Architecture\n")

        for root in [product_root, dev_root]:
            exit_code = self.module.main(
                [
                    str(root),
                    "--index-root",
                    str(self.tmp / ".confluence-index"),
                    "--no-agent-rules",
                ]
            )
            self.assertEqual(exit_code, 0)

        index_root = self.tmp / ".confluence-index"
        self.assertTrue((index_root / "sources" / "product-team-space").exists())
        self.assertTrue((index_root / "sources" / "dev-team-space").exists())
        registry = json.loads((index_root / "registry.json").read_text())
        self.assertEqual(
            [source["source_id"] for source in registry["sources"]],
            ["dev-team-space", "product-team-space"],
        )

    def test_conflicting_source_id_stops_without_overwriting(self) -> None:
        first_root = self.tmp / "Product Team Space"
        second_root = self.tmp / "Different Product Export"
        self.write_source("Product Team Space", "one.md", "# One\n")
        self.write_source("Different Product Export", "two.md", "# Two\n")

        self.assertEqual(
            self.module.main(
                [
                    str(first_root),
                    "--source-id",
                    "product",
                    "--index-root",
                    str(self.tmp / ".confluence-index"),
                    "--no-agent-rules",
                ]
            ),
            0,
        )
        self.assertEqual(
            self.module.main(
                [
                    str(second_root),
                    "--source-id",
                    "product",
                    "--index-root",
                    str(self.tmp / ".confluence-index"),
                    "--no-agent-rules",
                ]
            ),
            2,
        )
        entries = self.read_jsonl(
            self.tmp / ".confluence-index" / "sources" / "product" / "source-index.jsonl"
        )
        self.assertEqual(entries[0]["title"], "One")


if __name__ == "__main__":
    unittest.main()
