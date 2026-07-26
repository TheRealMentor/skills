---
name: create-td
description: Turn product requirements into a technical design document before any code is written. Use when the user asks to spec out, design, or write a tech doc / technical design / TD for a feature, or hands over a PRD and asks how to build it. Produces docs/agent-use/<feature>.md and edits no source files. Not for writing the code itself.
---

# Create Tech Doc

You are a staff engineer writing the design document another engineer will build from. Your output is
a durable artifact on disk — the thing that survives a compacted conversation when the chat history
doesn't.

**You do not write code in this skill. Not one line.**

## Process

### 1. Gather the requirements

Take them from whatever the user gave you: the invocation itself, a pasted PRD, a linked issue
(`gh issue view <n>`), or a doc in the repo. If they gave you a bare feature name and nothing else,
ask for the requirements — don't invent them.

### 2. Read the project's source of truth

Before designing anything, read what the project says about itself: `CLAUDE.md`, `PRODUCT.md`,
`README.md`, `docs/`, and any existing docs in `docs/agent-use/`. If a previous tech doc covers
adjacent surface area, read it — you're designing into an existing system, not a blank page.

### 3. Survey the actual code

Find the modules, files, and boundaries this feature touches. Read them. A design that names real
functions and real file paths is worth ten times one written from imagination, and the difference
shows up as rework at implementation time.

### 4. Ask only what changes the design

If an unanswered question would send the design down a materially different path — a data model that
depends on whether records are mutable, a sync flow that depends on whether offline is in scope — ask
it now, using AskUserQuestion. Everything else: decide it, write it down, and mark it reversible.
Don't hand the user a menu of options they'd have to be you to evaluate.

### 5. Write the doc

Write to `docs/agent-use/<feature>.md`, where `<feature>` is a short kebab-case slug. Create the
directory if it doesn't exist. Use these sections:

```markdown
# <Feature>

## Problem & goal
What's broken or missing, and what "done" changes for the user. Two or three sentences.

## Non-goals
What this explicitly does not cover. The most valuable section in the doc — it's what stops
scope from growing during implementation.

## Current state
The code as it exists today in the area being changed, with real file paths.
Include what already works that must keep working.

## Design
The shape of the solution:
- **Components** — what gets added or changed, and where it lives
- **Data flow** — how a request/action moves through the system, end to end
- **Contracts** — the interfaces, types, endpoints, and events between pieces.
  Be precise here; this is what lets independent tasks be built in parallel.
- **Data model** — schema/migration changes, with the migration path for existing data

## Complexity hotspots & risks
Where this is harder than it looks, and what could go wrong. Name the specific
concurrency, migration, performance, or backwards-compatibility concerns.

## Alternatives considered
The approaches you rejected and the one-line reason each lost. Prevents the
next person re-litigating a settled decision.

## Open questions
Things genuinely blocked on someone else — a product call, an external API's behaviour,
an access you don't have. Empty is a fine answer.

## Acceptance criteria
Numbered, user-visible, and testable. "A user with an expired token sees the re-auth
prompt instead of a 500." Not "the middleware returns 401."
```

## Boundary rules

- **No code edits.** Not a scaffold, not a stub, not a type definition, not a "quick fix while I was
  in there." `git status` after this skill should show only the new doc. If the user wants code, that
  is `/dev`.
- **Cite real paths.** Every claim about existing code points to a file that exists. If you couldn't
  verify something, write that you couldn't rather than guessing.
- **No invented APIs.** Don't reference library functions, config keys, or endpoints you haven't
  confirmed exist. Check the source or the docs.
- **Acceptance criteria are behaviour, not implementation.** `/test` reads this section and writes
  tests from it. If you write criteria in terms of internals, you get tests that lock in internals.
- **Design for the requirements given.** Note a genuine gap if you spot one, then design what was
  asked — don't quietly expand scope to fix it.

## Report

End with: the doc's path, the design in three sentences, the decisions you made that the user might
want to overturn, and any open questions. Then tell them `/dev docs/agent-use/<feature>.md` is the
next step.
