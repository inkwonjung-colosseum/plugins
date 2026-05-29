# Statechart composition — compound, parallel, history

The three features that make a statechart more than a flat FSM. All typed via `setup()`.

## Compound (nested) states

A state that has its own `initial` and `states` is compound. Transition out of it when a child hits `type: 'final'` via `onDone`:

```ts
states: {
  active: {
    initial: 'step1',
    states: {
      step1: { on: { NEXT: 'step2' } },
      step2: { on: { NEXT: 'step3', BACK: 'step1' } },
      step3: { type: 'final' },
    },
    onDone: 'completed',   // fires when a child reaches `final`
  },
  completed: { type: 'final' },
}
```

- Targets resolve relative to the current level. Use an absolute id to jump across the tree: `target: '#wizard.active.step1'` (the `#` references a state `id`).
- An event handler on the parent (`active.on`) catches events not handled by the active child — parent transitions are the fallback.

## Parallel states (AND-states)

`type: 'parallel'` runs every region simultaneously. No `initial` on the parallel node itself; each region declares its own:

```ts
const editor = setup({
  types: { events: {} as { type: 'TOGGLE_BOLD' } | { type: 'TOGGLE_IT' } | { type: 'SELECT' } | { type: 'DESELECT' } },
}).createMachine({
  id: 'editor',
  initial: 'idle',
  states: {
    idle: { on: { SELECT: 'selection' } },
    selection: {
      type: 'parallel',
      on: { DESELECT: 'idle' },
      states: {
        bold:   { initial: 'off', states: { off: { on: { TOGGLE_BOLD: 'on' } }, on: { on: { TOGGLE_BOLD: 'off' } } } },
        italic: { initial: 'off', states: { off: { on: { TOGGLE_IT: 'on' } },  on: { on: { TOGGLE_IT: 'off' } } } },
      },
    },
  },
});
```

- `state.value` is now an object: `{ selection: { bold: 'on', italic: 'off' } }`.
- A parallel state's `onDone` fires only when EVERY region reaches a final state.

## History states

A pseudo-state that, on re-entry of its parent, redirects to the last active child instead of the parent's `initial`:

```ts
states: {
  work: {
    initial: 'a',
    states: {
      a: { on: { TO_B: 'b' } },
      b: { on: { TO_A: 'a' } },
      hist: { type: 'history', history: 'shallow' }, // 'deep' restores nested grandchildren too
    },
    on: { PAUSE: 'paused' },
  },
  paused: { on: { RESUME: 'work.hist' } }, // resumes at a or b, whichever was last active
}
```

- `history: 'shallow'` (default) restores only the direct child; `'deep'` restores the full nested path.
- Optional `target` on the history node sets a default if the parent was never entered before.

## Guarding on another region's state

Use `stateIn` to gate a transition on a parallel sibling (or any state) being active:

```ts
import { setup, stateIn } from 'xstate';

setup({
  guards: { isBold: stateIn('#editor.selection.bold.on') },
}).createMachine(/* ... target: { guard: 'isBold', ... } ... */);
```

## Rules

- Give compound states you target across the tree an explicit `id` so `#id` references stay stable through refactors.
- Don't nest deeper than the domain needs — prefer parallel regions over a combinatorial explosion of nested states.
- Every region in a parallel state must be a compound state with its own `initial` (a leaf can't be a region).
- `final` at the root produces machine `output`; `final` in a compound/parallel child triggers that state's `onDone`.
