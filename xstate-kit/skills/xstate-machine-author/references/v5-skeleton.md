# XState v5 — full typed skeleton

Canonical `setup().createMachine()` with typed context/events, an actor (`fromPromise`), guards, delays, `invoke`, and `after`.

```ts
import { setup, assign, createActor, fromPromise } from 'xstate';

const machine = setup({
  types: {
    context: {} as { retries: number; data: unknown },
    events: {} as
      | { type: 'FETCH' }
      | { type: 'RETRY' }
      | { type: 'CANCEL' },
  },
  actors: {
    fetchUser: fromPromise(async ({ input }: { input: { id: string } }) => {
      const res = await fetch(`/api/users/${input.id}`);
      return res.json();
    }),
  },
  actions: {
    bumpRetries: assign({ retries: ({ context }) => context.retries + 1 }),
  },
  guards: {
    canRetry: ({ context }) => context.retries < 3,
  },
  delays: { BACKOFF: 1000 },
}).createMachine({
  id: 'fetcher',
  context: { retries: 0, data: null },
  initial: 'idle',
  states: {
    idle: { on: { FETCH: 'loading' } },
    loading: {
      invoke: {
        src: 'fetchUser',
        input: { id: 'abc' },
        onDone: { target: 'success', actions: assign({ data: ({ event }) => event.output }) },
        onError: 'failure',
      },
      on: { CANCEL: 'idle' },
    },
    success: { type: 'final' },
    failure: {
      on: { RETRY: { target: 'loading', guard: 'canRetry', actions: 'bumpRetries' } },
      after: { BACKOFF: { target: 'loading', guard: 'canRetry' } },
    },
  },
});

// run it
const actor = createActor(machine);
actor.subscribe((s) => console.log(s.value, s.context));
actor.start();
actor.send({ type: 'FETCH' });
```

## Spawning child actors

Store refs in context via `assign` / `enqueueActions`:

```ts
import { setup, assign, spawnChild } from 'xstate';
// inside actions:
actions: {
  spawnWorker: assign({
    worker: ({ spawn }) => spawn('workerMachine', { id: 'worker' }),
  }),
}
```

## Machine output

Final output at the root replaces v4 `data`:

```ts
.createMachine({
  /* ... */
  output: ({ context }) => ({ result: context.data }),
});
```
