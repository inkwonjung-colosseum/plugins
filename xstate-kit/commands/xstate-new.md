---
name: xstate-new
description: Scaffold a new typed XState v5 machine from a description
argument-hint: "<machine-name> [description]"
---
Scaffold a new XState v5 machine file from a short description.

Usage: `/xstate-new <machine-name> [description]`

Steps:
1. Ask for the machine's purpose if no description given.
2. Invoke the `xstate-machine-author` skill to produce a typed `setup().createMachine()` file at `<name>.machine.ts`.
3. Offer follow-ups: a React binding (`xstate-react`), tests (`xstate-test`), a diagram (`xstate-graph`), state persistence (`xstate-persistence`), or live debugging (`xstate-inspect`).

