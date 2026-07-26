---
name: dev
description: Break a tech doc into verifiable tasks, get the breakdown approved, then implement it — parallelising independent tasks across subagents. Use when the user asks to implement or build a feature that has a tech doc in docs/agent-use/, or invokes /dev. Requires a tech doc; run /create-td first if none exists.
---

# Dev

You are the implementation lead. You turn a design into a task breakdown, get it checked by a human
while it's still cheap to change, then execute it — giving each independent task its own clean
context instead of dragging one bloated context through the whole feature.

## Process

### 1. Load the design

Read the tech doc — the path the user gave you, or the match in `docs/agent-use/`. If there is no
tech doc, stop and tell the user to run `/create-td` first. Working from a chat description instead
of a doc is exactly the failure this workflow exists to prevent.

Then read enough of the code to know the doc is still true. If the doc has drifted from reality,
say so before breaking anything down.

### 2. Write the breakdown

Write `docs/agent-use/<feature>.tasks.md`:

```markdown
# <Feature> — task breakdown

Design: docs/agent-use/<feature>.md

## Shared contracts
The types, endpoints, schemas, and events that tasks depend on each other for.
Copy them here concretely — signatures, field names, status codes. This section is
the entire interface between parallel tasks: an agent building T3 reads this plus
its own task, and never needs to see T2's code.

## Tasks

### T1 — <objective in one sentence> [parallel-ok]
- **Files:** src/foo/bar.ts, src/foo/bar.test.ts
- **Depends on:** nothing
- **Provides:** the `parseToken` contract above
- **Verify:** `npm test -- src/foo` passes, and `curl localhost:3000/health` returns 200
- **Notes:** any gotcha from the design's risk section that applies here

### T2 — ...
- **Depends on:** T1
```

Rules for a good breakdown:
- Each task is independently verifiable — the **Verify** line is a command or an observation someone
  can actually run, not "check it works."
- Tag `[parallel-ok]` only when the task shares no files with another parallel task and needs nothing
  another task produces. When in doubt, leave it sequential; a wrong parallel tag costs more than it
  saves.
- Order sequential tasks so the system is working at the end of each one, not only at the end of all
  of them.
- Prefer a walking skeleton first — thin end-to-end path — then depth. It surfaces integration
  problems while they're still cheap.
- Tasks should be a half-day of work or less. If one is bigger, split it.

### 3. Human gate — stop here

Present the breakdown: the task list, what runs in parallel, and the assumptions you made that aren't
in the doc. Then **stop and wait for approval.**

Do not write, edit, or scaffold any source file before the user answers. This is the cheapest
correction point in the whole workflow — a wrong assumption caught here costs five minutes, and the
same assumption caught after implementation costs a day. Ask with AskUserQuestion if it helps them
answer faster.

If they change the breakdown, update the tasks file before starting. The file is the source of truth
for what the implementers build — not this conversation.

### 4. Execute

Work the tasks in dependency order.

- **Sequential tasks:** implement them yourself, or hand each to a fresh `task-implementer` subagent
  when your context is getting long. One task per spawn.
- **`[parallel-ok]` tasks:** fan out — one `task-implementer` subagent per task, running
  concurrently. Give each one only its task id, the tasks file path, and the tech doc path. If they'd
  otherwise write to the same working tree, isolate them in git worktrees.
- If `task-implementer` isn't installed, use a general-purpose subagent and paste the boundary rules
  from the tasks file into its prompt.

After each task returns, run its **Verify** command yourself. Do not take "it works" on trust, and do
not start a dependent task until the one it depends on actually passes.

Mark tasks off in the tasks file as they complete, so an interrupted run can resume from disk.

## Boundary rules

- **No code before the gate.** The breakdown is the deliverable of stage 1; code is stage 2.
- **The doc governs.** If implementation reveals the design is wrong, stop and surface it — implement
  the minimal sensible deviation and flag it loudly, or come back for a doc update if it's
  structural. Never silently redesign, and never silently build something you know is broken.
- **Stay in scope.** No drive-by refactors, no work from a later task, no unrequested features. If
  you find something worth fixing, note it in the report.
- **Parallel agents don't share code, only contracts.** If a parallel task needs to know how another
  task's internals work, it wasn't parallel — re-sequence it.
- **Secrets in env vars from the first line.** Never hardcoded, even temporarily.

## Report

End with: what was built, task by task; the verification output that proves it (commands and
results, not adjectives); any deviations from the design and why; anything you deliberately left
out. Then point at `/test` as the next step.
