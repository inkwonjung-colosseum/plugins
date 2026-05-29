---
name: xstate-persistence
description: "Persist and rehydrate XState v5 actor state with getPersistedSnapshot and createActor({ snapshot }). Use when saving, resuming, restoring, or migrating a running machine's state across reloads, restarts, or requests."
---
# XState Persistence (save & rehydrate)

Serialize a running actor and resume it later — across a page reload, a server restart, or between requests. Use when the user wants durable state, resumable workflows, crash recovery, or server-side machines.

## Save — `getPersistedSnapshot`

```ts
const actor = createActor(machine).start();
actor.send({ type: 'NEXT' });

const persisted = actor.getPersistedSnapshot(); // plain JSON-serializable object
await db.save(id, JSON.stringify(persisted));
```

## Restore — `createActor(machine, { snapshot })`

```ts
const persisted = JSON.parse(await db.load(id));
const actor = createActor(machine, { snapshot: persisted });
actor.start(); // resumes at the saved state value + context, no replay of past events
```

## Rules

- The snapshot captures state value, context, and the state of invoked/spawned actors — not in-flight promises. A `fromPromise` actor that was mid-flight resumes in its invoking state; the promise does NOT re-run automatically. Re-enter the state (or `reenter: true`) to restart it.
- Persist spawned child actors only when they are spawned with `{ syncSnapshot: true }` (or invoked) so their state rides along in the parent snapshot.
- `start()` AFTER passing `{ snapshot }` — restoring then starting is the correct order; never `send` before `start`.
- The machine MUST be the same `setup()` definition that produced the snapshot. Changing state ids/shape breaks restore — version your snapshots and migrate on load.
- Snapshots are data only; closures (actions/actors/guards) come from `setup()` at restore time — another reason to register implementations in `setup`, never inline.

Full lifecycle (spawned-actor sync, versioning/migration, server request pattern): `references/snapshot.md`.
