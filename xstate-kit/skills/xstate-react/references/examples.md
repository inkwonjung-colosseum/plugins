# XState React — full examples

## Local machine — `useMachine`

```tsx
import { useMachine } from '@xstate/react';
import { machine } from './fetcher.machine';

function Fetcher() {
  const [state, send] = useMachine(machine);
  return (
    <div>
      {state.matches('loading') && <Spinner />}
      {state.matches('success') && <pre>{JSON.stringify(state.context.data)}</pre>}
      <button onClick={() => send({ type: 'FETCH' })}>Fetch</button>
    </div>
  );
}
```

## Shared machine across a tree — `createActorContext`

Preferred over prop-drilling an actor. One running actor for the whole subtree.

```tsx
import { createActorContext } from '@xstate/react';
import { machine } from './fetcher.machine';

export const FetcherCtx = createActorContext(machine);

function App() {
  return (
    <FetcherCtx.Provider>
      <Status />
      <Controls />
    </FetcherCtx.Provider>
  );
}

function Status() {
  // re-renders ONLY when the selected slice changes
  const isLoading = FetcherCtx.useSelector((s) => s.matches('loading'));
  return isLoading ? <Spinner /> : null;
}

function Controls() {
  const actorRef = FetcherCtx.useActorRef();
  return <button onClick={() => actorRef.send({ type: 'FETCH' })}>Go</button>;
}
```

## Passing input / implementations

```tsx
const [state, send] = useMachine(machine, { input: { id: 'abc' } });
// or for a provider:
<FetcherCtx.Provider options={{ input: { id: 'abc' } }}>…</FetcherCtx.Provider>
```
