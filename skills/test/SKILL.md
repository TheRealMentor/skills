---
name: test
description: Write a test suite against a feature's documented spec rather than against its implementation, reading the acceptance criteria before reading the code so tests can't inherit the code's bugs. Use when the user asks to write tests, add test coverage, or invokes /test after a feature is built. Not for running an existing suite or fixing a single failing test.
---

# Test

You write tests that describe what the feature is *supposed* to do. That is a different job from
writing tests that describe what the code currently does, and the difference only survives if you
read the spec first.

## Process

### 1. Read the spec before the implementation

This ordering is the whole point of this skill. In order:

1. `docs/agent-use/<feature>.md` — the **Acceptance criteria** section especially
2. The project's source of truth — `CLAUDE.md`, `PRODUCT.md`, `README.md`
3. Only then, the implementation

Write down the criteria you're testing against before you open the source. Tests written straight
after implementation, with the implementation still fresh in context, reliably encode the code's bugs
as expected behaviour — you assert what you just watched happen. Reading the spec first is the
cheapest defence against that.

If no tech doc exists, get the intended behaviour from the project docs, the issue, or the user. If
you cannot establish what the feature is *supposed* to do from any source, say so — don't fall back
to describing the code and call it a test suite.

### 2. Learn the project's testing conventions

Detect, don't assume: find the runner and config the project already uses (`package.json`,
`pyproject.toml`, `Cargo.toml`, `go.mod`, CI workflow files), and read two or three existing test
files. Match their structure, naming, assertion style, and fixture/mock approach. A suite that looks
foreign to the repo won't be maintained.

If the project has no tests at all, pick the standard runner for the stack, keep the setup minimal,
and say what you chose and why.

### 3. Write the tests

Cover, in this order:

- **One test per acceptance criterion**, naming the behaviour in the test name. Someone reading the
  test names should be able to reconstruct what the feature does.
- **The edge cases the doc names** — the boundaries, empty states, and limits called out in the
  design's risks and hotspots.
- **Error states** — what the user or caller sees when things fail: bad input, missing auth, an
  upstream that's down, a partial write.

Test at the level the criteria are written at. If the criterion is about what an API returns, test the
endpoint, not the three functions behind it.

### 4. Run them and read the failures carefully

Run the suite. For each failure, decide which is wrong: the spec or the code.

- **Code is wrong** → report it as a bug found. Leave the failing test failing, and tell the user
  clearly. This is the suite doing its job on its first run.
- **Spec is wrong or out of date** → report the discrepancy and ask. Don't quietly pick a side.
- **Test is wrong** → fix the test.

Never edit a test to match the code just to get green. A green suite that was reshaped to fit the
implementation certifies nothing, and it will keep certifying nothing every time it runs.

## Boundary rules

- **Spec first, implementation second.** Every time.
- **Test behaviour, not internals.** No asserting on private methods, internal call counts, or mock
  invocation order as if they were requirements. If refactoring the implementation without changing
  behaviour breaks the test, the test is wrong.
- **Don't change source to make tests pass.** If the code is broken, report it — fixing it is `/dev`'s
  job, and the separation is what keeps the finding visible.
- **No coverage theatre.** Tests that assert nothing meaningful, or that restate the implementation
  line by line, are worse than no tests: they cost maintenance and buy no confidence.
- **Deterministic.** No dependence on wall-clock time, network, ordering, or leftover state from
  another test. Seed and freeze what you must.

## Report

End with: the runner and command to run the suite, real output from the run, which acceptance
criteria are now covered, what you deliberately did not cover and why, and — most importantly — any
place the code and the spec disagreed, with your read on which one is wrong.
