# Inspect — filtering, custom sinks, Studio round-trip

`createBrowserInspector()` + `{ inspect }` cover the common case. The detail below handles event filtering, custom transports, and the Stately Studio editor.

## Filtering what gets streamed

`createBrowserInspector` accepts options to cut noise on large/high-frequency machines:

```ts
const { inspect } = createBrowserInspector({
  autoStart: true,
  filter: (event) => event.type !== '@xstate.snapshot' || event.actorRef.id !== 'noisyChild',
  serialize: (event) => event, // customize/scrub payloads before they leave the app
});
```

Use `serialize` to redact secrets from context/events before they reach the inspector tab.

## Custom inspector via `createActor({ inspect: fn })`

The `inspect` option is just a function receiving inspection events — you can log instead of opening the Stately UI:

```ts
const actor = createActor(machine, {
  inspect: (inspEvent) => {
    if (inspEvent.type === '@xstate.snapshot') {
      console.log(inspEvent.actorRef.id, inspEvent.snapshot.value);
    }
    if (inspEvent.type === '@xstate.event') {
      console.log('→', inspEvent.event.type);
    }
  },
});
```

Inspection event types: `@xstate.actor` (actor created), `@xstate.snapshot` (state changed), `@xstate.event` (event sent). This is the hook for piping into your own observability (OpenTelemetry, a logger, a test recorder).

## Node / server inspection

In a non-browser process, run a WebSocket inspector and connect the Stately tab to it:

```ts
import { createInspector } from '@statelyai/inspect';
// adapter forwards inspection events over a WebSocket the Stately UI subscribes to
const inspector = createInspector(webSocketAdapter);
const actor = createActor(machine, { inspect: inspector.inspect });
```

## Stately Studio round-trip

- The static `xstate-graph` Mermaid/JSON export is for docs; to edit a machine visually, paste it into the Stately editor at `https://stately.ai/registry/editor` or import the file.
- The live inspector (above) and the editor are linked: actors you inspect can be opened in Studio to see the running path highlighted on the chart.

## When NOT to use the inspector

- Automated CI assertions → `xstate-test` (path coverage), not the inspector.
- A diagram for a README/Confluence → `xstate-graph` static export.
- The inspector is for interactive, human-in-the-loop debugging and demos.
