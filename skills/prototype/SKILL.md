---
name: prototype
description: Answer a feasibility question by building the smallest working version on a throwaway branch, then estimate the gap to production. Use when the user asks whether something can be built, wants to spike or try an approach before committing to it, or invokes /prototype. Explicitly throwaway code — not for building the real feature.
---

# Prototype

Some questions are cheaper to answer with code than with argument. This skill builds the smallest
thing that answers one, on a branch nobody will merge, and ends with an honest estimate of what
production would actually cost.

## Process

### 1. Name the question

Before writing anything, state the question in one sentence and write it down. "Can we stream model
output through our existing SSE layer without buffering?" is a question. "Try out streaming" is not —
you can't tell when you're done, and you'll build a feature instead of an answer.

If the user's request is vague, sharpen it into a specific question and confirm you've got it right.
Also agree what would count as an answer: what you'd have to see to call it a yes.

### 2. Take a throwaway branch

```bash
git switch -c prototype/<slug>
```

Make sure the working tree is clean first — an experiment tangled up with uncommitted real work is
how prototypes accidentally ship. If there are uncommitted changes, stash or commit them and say so.

### 3. Build the smallest thing that answers the question

**Explicitly allowed here, and nowhere else in this workflow:** hardcoded values, no error handling,
no tests, ugly UI, copy-paste, one giant function, mock data, `// TODO` everywhere, skipping auth,
ignoring edge cases entirely.

Aim every shortcut in the same direction: at the question. Cut everything that isn't load-bearing for
the answer. If you're building a login screen to test a rendering approach, don't build login.

Timebox it. If the question isn't answered within roughly the effort you scoped, that's a finding —
report it rather than grinding on. "Harder than expected, here's what I hit" is a genuine answer.

**Not allowed, even here:**
- Touching production config, infrastructure, or deployment
- Running migrations against a real database — use a local or throwaway one
- Real credentials or secrets, hardcoded or otherwise
- Deleting or rewriting anything on the main branch
- Third-party calls that cost money or mutate real state without asking first

### 4. Write the verdict — the golden rule

**Every prototype ends with a written production-gap estimate.** No exceptions. This is the rule that
stops a fast experiment from quietly becoming an unreviewed shortcut in the codebase.

Write it to `docs/agent-use/prototypes/<slug>.md`, and **commit that file to the main branch**, not
the prototype branch — the branch gets deleted, and the finding has to outlive it.

```markdown
# Prototype: <slug>

**Question:** the one-sentence question
**Answer:** yes / no / yes-but — in one sentence
**Date:** <date>  ·  **Branch:** prototype/<slug>

## What I built
The shape of the spike, and where the code is.

## What I learned
The actual finding. Include what surprised you — that's usually the valuable part.

## What's faked
Every shortcut taken, listed. Be exhaustive; this list is the input to the estimate below.

## Production gap
What real implementation needs, itemised with rough effort:
| Work | Effort |
|---|---|
| Proper error handling and retries | ~1 day |
| Auth on the new endpoint | ~0.5 day |
| Migration for the new column, with backfill | ~1 day |
| Tests | ~1 day |
**Total: ~X days**

## Recommendation
Keep and harden / rewrite properly from a tech doc / kill it — and why.
Name the risks that only showed up once code existed.
```

### 5. Hand it back

Tell the user the answer first, then the estimate, then where the branch and the write-up are. If the
recommendation is to build it for real, the next step is `/create-td` — and the tech doc should be
written from the design as it *should* be, not reverse-engineered from the spike.

## Boundary rules

- **The verdict document is mandatory.** A prototype without a production-gap estimate isn't
  finished, however well the code works.
- **Never merge prototype code to main.** Not "just the good parts." If it's worth keeping, it's
  worth `/create-td` and `/dev`. The prototype's value is the knowledge, not the lines.
- **Be honest about the gap.** Rounding "two weeks of hardening" down to "mostly done" is how spikes
  end up in production. Overestimate before you underestimate.
- **A failed prototype is a success.** It cost hours and saved weeks. Report it plainly, with no
  hedging and no attempt to salvage the framing.

## Report

End with: the answer to the question, the production-gap total, the recommendation, the branch name,
and the path to the write-up on main.
