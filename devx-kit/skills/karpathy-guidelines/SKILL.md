---
name: karpathy-guidelines
description: Use when reviewing code for simplicity and verifiable success.
license: MIT
---

# Karpathy Guidelines

Reduce common LLM coding mistakes. Bias toward caution when the task has real ambiguity.

## Workflow

1. State assumptions and tradeoffs before coding.
2. Prefer the minimum code that solves the request.
3. Touch only lines that trace to the request.
4. Define verifiable success criteria and run them.
5. Simplify if the solution grows beyond the problem.

Report unrelated dead code or risk separately; do not fix unrelated issues unless asked.
