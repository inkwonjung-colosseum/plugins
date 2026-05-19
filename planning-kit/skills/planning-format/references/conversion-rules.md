# Conversion Rules

Use during image handling, body merge, and policy/feature document generation.

## Source merge

- Text/file/directory input is source 0.
- URL and discovered child URLs follow BFS source order.
- Images can come from input files, directories, markdown/HTML references, image content-type responses, or inline `data:image`.
- For images, transcribe visible text and describe screen/flow/diagram meaning. Prefix uncertain inference with `추정:`.

## Feature name

Prefer explicit user topic, then URL title/H1, file stem, directory name, repeated heading, then first core noun phrase. Keep one feature name; track other candidates as excluded input.

## Template generation

Read both templates in the same turn:

- `templates/정책서.md`: 10-section policy document.
- `templates/기능설계서.md`: 8-section feature design document.

Templates use field lists and `### item` cards by default. Add Markdown tables only for short 2-4 column comparisons. Do not leave empty placeholder rows. Use `[TBD]` for missing evidence and mirror it in unresolved items.

## Mapping

- UI, fields, buttons, messages, visible behavior -> feature design.
- User flow, trigger, action sequence -> feature design.
- Permission/data visibility -> both documents, split by policy intent vs screen/action access.
- Rules, limits, allowed/forbidden criteria -> policy.
- State transitions and processing criteria -> policy.
- Exceptions, approval, operational decision authority -> policy.
- External integration policy and failure handling -> policy.
- Terms, scope, principles -> policy.
- Anything unmapped -> exclusion tracking.

## Cross-document anchors

Policy rules, states, permissions, exceptions, and integrations should name related feature behavior. Feature actions, screens, permissions, and messages should name related policy sections.

## Terms

Policy prefers domain/system terms. Feature UI fields prefer Korean label first with system term in parentheses, such as `존 코드 (Zone Code)`.

## Auxiliary tables

Use `### N.M [purpose] 보조 표` only when a list is too heterogeneous for one field. Number sequentially. No legacy backlink suffix. Max nested depth is 3; deeper detail stays summarized with an exclusion note.
