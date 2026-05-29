---
name: xstate-inspect
description: "Watch a running XState v5 actor live with @statelyai/inspect (createBrowserInspector + the { inspect } actor option). Use when debugging, observing, or visualizing real-time transitions, events, and context of a running machine."
---
# XState Inspect (live runtime debugging)

Stream a running actor's transitions, events, and context into the live Stately inspector. Use when the user wants to debug why a machine did/didn't transition, watch events fire, verify guards/invoked actors at runtime, or demo a machine live. This is runtime observation — distinct from `xstate-graph`, which exports a static diagram.

## Browser — `createBrowserInspector`

```ts
import { createBrowserInspector } from '@statelyai/inspect';
import { createActor } from 'xstate';

const { inspect } = createBrowserInspector(); // opens the Stately inspector tab

const actor = createActor(machine, { inspect });
actor.start(); // every transition/event now streams to the inspector
```

## React — pass `inspect` to the hook

```tsx
const { inspect } = createBrowserInspector();
const [state, send] = useMachine(machine, { inspect });
// createActorContext: <Ctx.Provider options={{ inspect }}>…</Ctx.Provider>
```

## Node / non-browser — `createInspector` over WebSocket

```ts
import { createInspector } from '@statelyai/inspect';
// pipe events to a custom sink (e.g. a WebSocket server the Stately tab connects to)
const inspector = createInspector(myWebSocketAdapter);
const actor = createActor(machine, { inspect: inspector.inspect });
```

## Rules

- `@statelyai/inspect` is the v5-canonical tool; the old `@xstate/inspect` package is v4-era — do not use it for v5.
- Gate it behind a dev flag (`import.meta.env.DEV`) — never ship `createBrowserInspector()` to production; it opens a tab and streams state.
- One inspector can observe many actors — create it once, pass the same `inspect` to every `createActor`/hook you want to watch (including spawned/invoked children, which appear as sub-actors).
- For a static picture instead of a live stream, use `xstate-graph` (Mermaid/DOT/etc.). For automated path assertions, use `xstate-test`.

Filtering events, custom inspector sinks, and the Stately Studio registry round-trip: `references/setup.md`.
