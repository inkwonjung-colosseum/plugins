---
name: xstate-machine-author
description: "Write or refactor typed XState v5 statecharts (setup().createMachine) — compound/parallel/history states, actors, guards, v4-to-v5 porting. Use when creating, fixing, or modeling a state machine."
---
# XState Machine Author (v5)

Author typed, idiomatic XState v5 machines. Use when the user creates/refactors a state machine, models a workflow, or fixes v5 machine code.

## v5 mental model

- One machine per file: `setup({ types, actions, actors, guards, delays }).createMachine({...})`. `setup()` registers implementations once and references them by string — keeps the config serializable (required for visualization + model-based tests).
- An actor is a running machine: `createActor(machine).start()` (v4 `interpret` is gone).

## Minimal shape

```ts
const machine = setup({
  types: { context: {} as Ctx, events: {} as Ev },
  actions: { bump: assign({ n: ({ context }) => context.n + 1 }) },
  guards: { canRetry: ({ context }) => context.n < 3 },
}).createMachine({
  id: 'm', context: { n: 0 }, initial: 'idle',
  states: {
    idle: { on: { GO: 'work' } },
    work: { invoke: { src: 'task', onDone: 'done', onError: 'idle' } },
    done: { type: 'final' },
  },
});
```

- Full typed skeleton (invoke / `fromPromise`, `after`, spawning, `output`): `references/v5-skeleton.md`.
- Porting v4 code? Apply the cheat-sheet in `references/v4-to-v5.md` silently.

## Composition — the statechart features (use these, not a flat FSM)

A flat list of states is just an FSM. Reach for these when modeling real workflows:

- **Compound (nested)**: a state with its own `initial` + `states`. Add `onDone` to transition when a child reaches `type: 'final'`.
- **Parallel** (`type: 'parallel'`): independent regions active at once (e.g. `bold` × `italic` in an editor). No `initial` on a parallel node; each region has its own.
- **History** (`type: 'history'`, `history: 'shallow' | 'deep'`): re-enter a compound state at its last active child instead of its `initial` — resumable wizards, restored tabs.

```ts
states: {
  editing: {
    type: 'parallel',
    states: {
      bold:   { initial: 'off', states: { off: { on: { TOGGLE_BOLD: 'on' } }, on: { on: { TOGGLE_BOLD: 'off' } } } },
      italic: { initial: 'off', states: { off: { on: { TOGGLE_IT: 'on' } },  on: { on: { TOGGLE_IT: 'off' } } } },
    },
  },
}
```

Cross-region/absolute targets (`target: '#id.region.state'`) and the `stateIn('region.state')` guard, plus shallow-vs-deep history semantics: `references/composition.md`.

## Rules

- Model events as a discriminated union in `types.events`. Never `any`.
- `guard` not `cond`; `actors` not `services`; handlers take one object arg `({ context, event })`.
- Eventless transition: `always`. Delayed: `after`. `onDone` payload is `event.output` (not `event.data`).
- Keep config serializable — register closures in `setup`, not inline.
- Verify the machine compiles and every `target` resolves to a real state id before returning.
