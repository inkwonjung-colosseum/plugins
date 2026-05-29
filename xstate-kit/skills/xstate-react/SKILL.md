---
name: xstate-react
description: "Wire an XState v5 machine into React via @xstate/react (useMachine, useSelector, createActorContext). Use when using a machine in a component or across a tree."
---
# XState React

Wire an XState v5 machine into React with `@xstate/react`. Use when using a machine in a component, sharing machine state across a tree, or migrating `useMachine` from v4.

## Local — `useMachine`

```tsx
const [state, send] = useMachine(machine);
state.matches('loading');
send({ type: 'FETCH' });
```

## Shared across a tree — `createActorContext`

Preferred over prop-drilling. One actor for the whole subtree.

```tsx
export const Ctx = createActorContext(machine);
// wrap subtree in <Ctx.Provider>…</Ctx.Provider>
const isLoading = Ctx.useSelector((s) => s.matches('loading'));
const ref = Ctx.useActorRef();
ref.send({ type: 'FETCH' });
```

Full provider + multi-component example: `references/examples.md`.

## Hook map

| Hook | Use |
|------|-----|
| `useMachine(machine)` | local actor; returns `[state, send, ref]` |
| `useActor(ref)` | bind to an existing actor ref |
| `useSelector(ref, sel)` | subscribe to a derived slice — minimizes re-renders |
| `createActorContext(machine)` | provider + `.useSelector` / `.useActorRef` for a subtree |

## Rules

- Prefer `useSelector` over reading the whole `state` when a slice suffices — the main perf lever (referential-equality bailout).
- Pass input via `useMachine(machine, { input })` or `<Ctx.Provider options={{ input }}>`.
- Define the machine at module scope — never recreate it in render.
- `send` takes an event object (`send({ type: 'X' })`), not a string, in v5.
