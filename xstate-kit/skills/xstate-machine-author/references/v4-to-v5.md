# XState v4 → v5 cheat-sheet

Apply silently when porting v4 code to v5.

| v4 | v5 |
|----|----|
| `Machine(...)` / `createMachine(cfg, opts)` | `setup(opts).createMachine(cfg)` |
| `cond: 'x'` | `guard: 'x'` |
| `interpret(machine)` | `createActor(machine)` |
| `(context, event) => ...` | `({ context, event }) => ...` (single object arg) |
| `services` | `actors` |
| `invoke.src` = function | `fromPromise` / `fromCallback` / `fromObservable` / `fromEventObservable` / `fromTransition` |
| `event.data` (onDone) | `event.output` |
| `send(...)` action | `raise(...)` / `sendTo(...)` / `enqueueActions` |
| `in: 'state'` guard | `stateIn('state')` |
| machine `data` (final output) | machine `output` |
| `predictableActionArguments` flag | removed — always on |

## Notes

- v5 `send` to an actor takes an **event object**, never a bare string.
- Implementations referenced by string in the config must be registered in `setup({ actions, actors, guards, delays })`.
- `spawn` is available inside `assign`/`enqueueActions` as `({ spawn }) => spawn(src, opts)`; top-level `spawn` import is gone.
