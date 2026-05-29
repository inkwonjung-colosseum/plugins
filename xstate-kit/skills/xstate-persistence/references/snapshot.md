# Persistence — full lifecycle

`getPersistedSnapshot()` + `createActor(machine, { snapshot })` cover save/restore. The detail below handles spawned actors, versioning, and the server-request pattern.

## Server-side request/response pattern

Each request rehydrates, applies an event, re-persists, and stops:

```ts
import { createActor } from 'xstate';
import { workflowMachine } from './workflow.machine';

export async function handle(id: string, event: WorkflowEvent) {
  const stored = await db.load(id);                 // null on first touch
  const actor = createActor(workflowMachine, {
    snapshot: stored ? JSON.parse(stored) : undefined,
  });
  actor.start();
  actor.send(event);
  await db.save(id, JSON.stringify(actor.getPersistedSnapshot()));
  const snap = actor.getSnapshot();
  actor.stop();                                     // free the actor; state already persisted
  return { value: snap.value, context: snap.context };
}
```

`snapshot: undefined` starts fresh — so the same code path handles new and resumed workflows.

## Spawned / invoked child actors

- Invoked actors (`invoke`) are persisted with the parent automatically.
- Spawned actors (`spawn(...)` inside `assign`) ride along ONLY if spawned with `{ syncSnapshot: true }`:

```ts
actions: {
  spawnWorker: assign({
    worker: ({ spawn }) => spawn('workerMachine', { id: 'worker', syncSnapshot: true }),
  }),
}
```

- In-flight `fromPromise` work is NOT resumed — the persisted actor sits in its invoking state but the async call does not re-fire. To retry on restore, model an explicit re-entry (e.g. a `RESUME` event that re-targets the invoking state, or `reenter: true`).

## Versioning & migration

A snapshot is only restorable by the machine shape that wrote it. When you rename states or change context:

```ts
const SCHEMA_VERSION = 2;

function migrate(raw: any) {
  let s = raw;
  if (s.__v === 1) s = { ...s, context: { ...s.context, retries: 0 }, __v: 2 };
  return s;
}

const stored = migrate(JSON.parse(await db.load(id)));
const actor = createActor(machine, { snapshot: stored });
```

Stamp `__v` (or store it in a column) when you persist, and add a migration branch per version bump. Without this, a deploy that changes the machine silently fails to restore old snapshots.

## Gotchas

- Don't persist secrets in `context` — the snapshot is plain data that lands in your store.
- `getPersistedSnapshot()` is a point-in-time copy; call it AFTER the event that changed state has settled (synchronous transitions are settled immediately; for async, `await waitFor(actor, predicate)` first).
- Restoring does not replay actions — entry actions of the restored state do NOT re-run. Side effects that must happen on resume belong on the `RESUME` transition, not on `entry`.
