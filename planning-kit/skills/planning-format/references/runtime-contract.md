# Runtime Contract

Use for execution edge cases. `SKILL.md` is the only metadata and trigger source.

## Inputs

Required positional input: text, file path, directory path, image path, or one or more `https?://` URLs.

Options:

- `--save`: default/no-op alias.
- `--no-save`: print bodies instead of writing files.
- `--no-fetch`: skip URL fetch and connector fallback.
- `--no-image`: skip image interpretation.
- `--no-self-review`: skip F1-F6 review only; keep exclusions and output shape.

## Dispatch

1. All tokens are `https?://` URLs -> URL mode.
2. Directory path -> directory mode.
3. File path -> file mode.
4. Otherwise -> text mode.

Mixed URL and non-URL tokens are text mode. `file://`, `ftp://`, `mailto:`, and scheme-less strings are not URL mode.

## Sequence

1. Dispatch input.
2. Reject only if merged text, image seeds, and URL seeds are all empty.
3. Collect links/images from every mode.
4. Fetch URL bodies BFS unless disabled.
5. Interpret images unless disabled.
6. Merge sources.
7. Generate policy and feature documents from templates.
8. Track exclusions.
9. Self-review unless disabled.
10. Save unless `--no-save`.
11. Emit output contract.

## Boundaries

- `planning/**` output can be reviewed or published later, but never counts as SSOT evidence.
- External SSOT conflict, acceptance criteria, and dependency impact belong to `planning-review`.
- Save failure is not a stop condition; print full bodies and failure detail.
