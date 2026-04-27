#!/usr/bin/env python3
"""Index local Markdown files already exported from Confluence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys


INDEX_VERSION = 1
READING_RULE_START = "<!-- confluence-export-kit:reading-rule:start -->"
READING_RULE_END = "<!-- confluence-export-kit:reading-rule:end -->"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def path_display(path: Path, base: Path | None = None) -> str:
    try:
        if base is not None:
            return path.resolve().relative_to(base.resolve()).as_posix()
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def slugify(value: str) -> str:
    normalized = value.strip().lower()
    slug = re.sub(r"[^\w]+", "-", normalized, flags=re.UNICODE).strip("-")
    return slug or "confluence-export"


def extract_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    frontmatter: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        clean_value = value.strip().strip('"').strip("'")
        if clean_value:
            frontmatter[key.strip()] = clean_value
    return frontmatter


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(2).strip())
    return headings


def title_for_file(path: Path, text: str, frontmatter: dict[str, object]) -> str:
    title = frontmatter.get("title")
    if isinstance(title, str) and title:
        return title
    headings = extract_headings(text)
    if headings:
        return headings[0]
    return path.stem


def classify_status(path: Path, frontmatter: dict[str, object]) -> str:
    value = frontmatter.get("status")
    if isinstance(value, str) and value:
        lower = value.lower()
        if lower in {"current", "draft", "archive", "unknown"}:
            return lower

    haystack = path.as_posix().lower()
    if any(token in haystack for token in ["archive", "아카이브"]):
        return "archive"
    if any(token in haystack for token in ["draft", "작성중", "작성 중", "수리중"]):
        return "draft"
    return "unknown"


def classify_source_type(path: Path, frontmatter: dict[str, object], status: str) -> str:
    value = frontmatter.get("source_type") or frontmatter.get("type")
    if isinstance(value, str) and value:
        normalized = slugify(value)
        if normalized in {
            "prd",
            "policy",
            "feature-spec",
            "meeting-note",
            "archive",
            "unknown",
        }:
            return normalized

    haystack = path.as_posix().lower()
    if status == "archive":
        return "archive"
    if "prd" in haystack:
        return "prd"
    if any(token in haystack for token in ["policy", "정책"]):
        return "policy"
    if any(token in haystack for token in ["feature", "기능 설계", "상세설계", "상세 설계"]):
        return "feature-spec"
    if any(token in haystack for token in ["회의록", "weekly", "daily", "sync"]):
        return "meeting-note"
    return "unknown"


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def collect_markdown_entries(export_path: Path, source_id: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for markdown_file in sorted(export_path.rglob("*.md")):
        if ".confluence-index" in markdown_file.parts:
            continue
        text = markdown_file.read_text(errors="replace")
        frontmatter = extract_frontmatter(text)
        status = classify_status(markdown_file, frontmatter)
        entry = {
            "source_id": source_id,
            "path": path_display(markdown_file),
            "source_relative_path": path_display(markdown_file, export_path),
            "title": title_for_file(markdown_file, text, frontmatter),
            "headings": extract_headings(text),
            "tags": [],
            "status": status,
            "source_type": classify_source_type(markdown_file, frontmatter, status),
            "word_count": word_count(text),
            "updated_at": datetime.fromtimestamp(
                markdown_file.stat().st_mtime, timezone.utc
            )
            .replace(microsecond=0)
            .isoformat(),
        }
        entries.append(entry)
    return sorted(entries, key=lambda item: str(item["title"]).lower())


def load_registry(index_root: Path) -> dict[str, object]:
    registry_path = index_root / "registry.json"
    if not registry_path.exists():
        return {"version": INDEX_VERSION, "updated_at": None, "sources": []}
    return json.loads(registry_path.read_text())


def update_registry(
    registry: dict[str, object],
    *,
    source_id: str,
    export_path: Path,
    source_index_path: Path,
    file_count: int,
    total_words: int,
    timestamp: str,
) -> tuple[dict[str, object], str | None]:
    resolved_export_path = export_path.resolve().as_posix()
    sources = list(registry.get("sources") or [])
    updated_sources: list[dict[str, object]] = []
    conflict: str | None = None
    replaced = False

    for source in sources:
        if source.get("source_id") != source_id:
            updated_sources.append(source)
            continue
        existing_path = source.get("export_path")
        if existing_path and existing_path != resolved_export_path:
            conflict = str(existing_path)
            updated_sources.append(source)
            continue
        replaced = True

    if conflict is not None:
        return registry, conflict

    source_record = {
        "source_id": source_id,
        "export_path": resolved_export_path,
        "display_path": path_display(export_path),
        "index_path": path_display(source_index_path),
        "file_count": file_count,
        "word_count": total_words,
        "updated_at": timestamp,
    }
    updated_sources.append(source_record)
    if not replaced:
        updated_sources = list(updated_sources)

    return (
        {
            "version": INDEX_VERSION,
            "updated_at": timestamp,
            "sources": sorted(updated_sources, key=lambda item: str(item["source_id"])),
        },
        None,
    )


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path: Path, entries: list[dict[str, object]]) -> None:
    lines = [json.dumps(entry, ensure_ascii=False, sort_keys=True) for entry in entries]
    path.write_text("\n".join(lines) + ("\n" if lines else ""))


def render_source_tree(source_id: str, entries: list[dict[str, object]]) -> str:
    lines = [f"# {source_id}", ""]
    for entry in sorted(entries, key=lambda item: str(item["source_relative_path"])):
        lines.append(f"- `{entry['source_relative_path']}` — {entry['title']}")
    return "\n".join(lines) + "\n"


def render_source_stats(source_id: str, entries: list[dict[str, object]]) -> str:
    total_words = sum(int(entry["word_count"]) for entry in entries)
    status_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for entry in entries:
        status_counts[str(entry["status"])] = status_counts.get(str(entry["status"]), 0) + 1
        type_counts[str(entry["source_type"])] = type_counts.get(str(entry["source_type"]), 0) + 1

    lines = [
        f"# {source_id} Stats",
        "",
        f"- Files: {len(entries)}",
        f"- Words: {total_words}",
        "",
        "## Status",
        "",
    ]
    lines.extend(f"- {key}: {status_counts[key]}" for key in sorted(status_counts))
    lines.extend(["", "## Source Type", ""])
    lines.extend(f"- {key}: {type_counts[key]}" for key in sorted(type_counts))
    return "\n".join(lines) + "\n"


def render_root_tree(registry: dict[str, object]) -> str:
    lines = ["# Confluence Export Index", ""]
    for source in registry.get("sources", []):
        lines.append(
            f"- `{source['source_id']}` — `{source['display_path']}` "
            f"({source['file_count']} files)"
        )
    return "\n".join(lines) + "\n"


def render_root_stats(registry: dict[str, object]) -> str:
    sources = list(registry.get("sources", []))
    file_count = sum(int(source.get("file_count", 0)) for source in sources)
    word_count = sum(int(source.get("word_count", 0)) for source in sources)
    lines = [
        "# Confluence Export Index Stats",
        "",
        f"- Sources: {len(sources)}",
        f"- Files: {file_count}",
        f"- Words: {word_count}",
    ]
    return "\n".join(lines) + "\n"


def reading_rule_block() -> str:
    return "\n".join(
        [
            READING_RULE_START,
            "## Reading Rule",
            "",
            "When working with exported Confluence documents:",
            "",
            "1. Start from `.confluence-index/registry.json` to choose the relevant export source.",
            "2. Then read `.confluence-index/sources/<source-id>/source-index.jsonl`.",
            "3. Use `.confluence-index/sources/<source-id>/tree.md` to understand that source hierarchy.",
            "4. Select the smallest relevant source files.",
            "5. Read raw exported Markdown only when evidence is needed.",
            "6. Do not load a whole exported space into context.",
            "7. Treat archive/draft/current documents differently when metadata is available.",
            READING_RULE_END,
            "",
        ]
    )


def install_reading_rule(agent_file: Path) -> None:
    block = reading_rule_block()
    if not agent_file.exists():
        agent_file.write_text(block)
        return

    content = agent_file.read_text()
    pattern = re.compile(
        re.escape(READING_RULE_START) + r".*?" + re.escape(READING_RULE_END) + r"\n?",
        flags=re.DOTALL,
    )
    if pattern.search(content):
        agent_file.write_text(pattern.sub(block, content))
        return

    separator = "\n" if content.endswith("\n") else "\n\n"
    agent_file.write_text(content + separator + block)


def append_log(path: Path, message: str) -> None:
    existing = path.read_text() if path.exists() else ""
    path.write_text(existing + message + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Index local Markdown files already exported from Confluence."
    )
    parser.add_argument("export_path", help="Local Confluence export folder to index.")
    parser.add_argument(
        "--source-id",
        help="Source namespace. Defaults to the export folder basename in kebab-case.",
    )
    parser.add_argument(
        "--index-root",
        default=".confluence-index",
        help="Index root directory. Default: ./.confluence-index",
    )
    parser.add_argument(
        "--no-agent-rules",
        action="store_true",
        help="Do not install Reading Rule blocks into AGENTS.md and CLAUDE.md.",
    )
    parser.add_argument(
        "--agent-files",
        nargs="+",
        default=["AGENTS.md", "CLAUDE.md"],
        help="Agent guidance files to create or update. Default: AGENTS.md CLAUDE.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes without creating or modifying files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    export_path = Path(args.export_path)
    if not export_path.exists() or not export_path.is_dir():
        print(f"Export path does not exist or is not a directory: {export_path}", file=sys.stderr)
        return 2

    source_id = args.source_id or slugify(export_path.name)
    index_root = Path(args.index_root)
    source_root = index_root / "sources" / source_id
    source_index_path = source_root / "source-index.jsonl"
    timestamp = now_utc()
    entries = collect_markdown_entries(export_path, source_id)
    total_words = sum(int(entry["word_count"]) for entry in entries)

    registry = load_registry(index_root)
    new_registry, conflict = update_registry(
        registry,
        source_id=source_id,
        export_path=export_path,
        source_index_path=source_index_path,
        file_count=len(entries),
        total_words=total_words,
        timestamp=timestamp,
    )
    if conflict is not None:
        print(
            f"source-id '{source_id}' is already registered for {conflict}. "
            "Use --source-id to choose a different namespace.",
            file=sys.stderr,
        )
        return 2

    planned_files = [
        index_root / "registry.json",
        index_root / "tree.md",
        index_root / "stats.md",
        index_root / "log.md",
        source_root / "source-index.jsonl",
        source_root / "tree.md",
        source_root / "stats.md",
        source_root / "log.md",
    ]
    if not args.no_agent_rules:
        planned_files.extend(Path(file_name) for file_name in args.agent_files)

    if args.dry_run:
        print(f"Source ID: {source_id}")
        print(f"Markdown files: {len(entries)}")
        print("Planned writes:")
        for path in planned_files:
            print(f"- {path}")
        return 0

    source_root.mkdir(parents=True, exist_ok=True)
    write_jsonl(source_index_path, entries)
    (source_root / "tree.md").write_text(render_source_tree(source_id, entries))
    (source_root / "stats.md").write_text(render_source_stats(source_id, entries))
    append_log(
        source_root / "log.md",
        f"- {timestamp} indexed {len(entries)} Markdown files from {path_display(export_path)}",
    )

    index_root.mkdir(parents=True, exist_ok=True)
    write_json(index_root / "registry.json", new_registry)
    (index_root / "tree.md").write_text(render_root_tree(new_registry))
    (index_root / "stats.md").write_text(render_root_stats(new_registry))
    append_log(
        index_root / "log.md",
        f"- {timestamp} indexed source {source_id} from {path_display(export_path)}",
    )

    if not args.no_agent_rules:
        for agent_file in args.agent_files:
            install_reading_rule(Path(agent_file))

    print(f"Source ID: {source_id}")
    print(f"Markdown files: {len(entries)}")
    print(f"Index root: {index_root}")
    print(f"Source index: {source_index_path}")
    if args.no_agent_rules:
        print("Reading Rule: skipped")
    else:
        print(f"Reading Rule files: {', '.join(args.agent_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
