# Extract the directed graph (Step 1 detail)

One extraction feeds every serializer. Never re-walk the machine per format.

```ts
import { toDirectedGraph } from '@xstate/graph';
import { machine } from './fetcher.machine';

const digraph = toDirectedGraph(machine);

// Portable shape every serializer in references/formats.md consumes:
type Node = { id: string; label: string };
type Edge = { source: string; target: string; label: string };

const nodes: Node[] = [];
const edges: Edge[] = [];

(function walk(n) {
  nodes.push({ id: n.id, label: n.stateNode.key });
  for (const e of n.edges) {
    edges.push({
      source: e.source.id,
      target: e.target.id,
      label: e.label.text || e.transition.eventType,
    });
  }
  n.children.forEach(walk);
})(digraph);
```

## Path-based graphs

For coverage / path views, project steps from path generators into the same `{nodes, edges}` shape:

```ts
import { getShortestPaths, getSimplePaths } from '@xstate/graph';

const paths = getShortestPaths(machine); // or getSimplePaths(machine)
// each path.steps has { state, event } — map to nodes/edges as above
```

## Nested (hierarchical) states

Prefix child ids with the parent id (`parent.child`) so ids stay globally unique across every output format. `toDirectedGraph` node ids already encode this hierarchy.
