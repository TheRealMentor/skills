# Shipping-code skills for Claude Code

Five skills that split feature work into stages, each with clean context and a durable artifact,
instead of one long chat that slowly forgets what you asked for.

```
/create-td  →  /dev  →  /test  →  /handoff
                                                    /prototype (any time you need an answer first)
```

## The problem this solves

Three hours into a single chat, the agent starts forgetting requirements, re-deciding settled
questions, and tripping over its own stale context. That isn't a model limitation so much as a
context management one — and it's the same mistake as cramming a program into one giant function.

So split it by responsibility. Each stage gets a narrow context and hands the next stage a file, not
a scrollback.

Three ideas do the work:

1. **Artifacts over memory.** Specs belong in files. Any agent can read a file in a fresh context; a
   fact mentioned 40 messages ago is gone.
2. **Narrow context beats large context.** An agent holding one feature's design outperforms one
   holding your entire repo history. Relevance beats volume.
3. **Checkpoints where they're cheap.** Review a task breakdown before code exists, not a diff
   afterwards. Same mistake, two orders of magnitude difference in cost.

## The five skills

| Skill | Job | Writes |
|---|---|---|
| **`/create-td`** | Requirements → technical design. Reads the code, writes no code. | `docs/agent-use/<feature>.md` |
| **`/dev`** | Design → task breakdown → **your approval** → implementation, parallelised | `docs/agent-use/<feature>.tasks.md` + code |
| **`/test`** | Tests written from the spec, read *before* the implementation | test files |
| **`/handoff`** | Logical commits + a PR description worth reading | git history + PR body |
| **`/prototype`** | Throwaway branch answering "can this even be built?" | `docs/agent-use/prototypes/<slug>.md` |

Each has one job and one boundary it will not cross. `/create-td` won't touch source. `/dev` won't
write code before you've approved the breakdown. `/test` won't edit a test to make it match buggy
code. `/handoff` won't push without being asked. `/prototype` won't finish without telling you what
production would really cost.

## Install

```bash
git clone https://github.com/TheRealMentor/skills.git shipping-skills
cd shipping-skills
./install.sh
```

That symlinks the skills into `~/.claude/skills/` and the agent into `~/.claude/agents/`, so
`git pull` later updates your install. Prefer copies you can edit freely? `./install.sh --copy`.
Either way it's idempotent, and it will never overwrite a skill you already had by that name.

Or just do it by hand — copy `skills/*` into `~/.claude/skills/` and `agents/*` into
`~/.claude/agents/`. There's nothing magic in the installer.

Start a new session afterwards, then type `/create-td`.

## A run through, end to end

```
/create-td add SSO login for enterprise accounts
```
Reads your `CLAUDE.md` and the auth code that exists today, asks the one or two questions that would
actually change the design, and writes `docs/agent-use/sso-login.md` — problem, non-goals, contracts,
risks, and acceptance criteria in user-visible terms. Your source tree is untouched; check
`git status` if you don't believe it.

Read it. It's a page. Fixing the design here costs a comment.

```
/dev docs/agent-use/sso-login.md
```
Breaks it into tasks — each with the files it touches, what it depends on, and a command that proves
it works — then **stops and shows you the list**. This is the checkpoint that pays for the whole
workflow. Approve it, and independent tasks fan out to subagents that share contracts but never each
other's internals.

```
/test sso-login
```
Reads the acceptance criteria *before* the implementation, deliberately, so the tests describe what
the feature should do rather than what the code happens to do. When they disagree it tells you which
one it thinks is wrong instead of quietly bending the test.

```
/handoff
```
Splits the branch into commits that mean something, writes the PR body, and stops before pushing.

And when you don't yet know whether something is possible:

```
/prototype can we stream model output through our existing SSE layer?
```
Throwaway branch, ugliest possible code, and a mandatory verdict at the end: the answer, everything
that was faked, and an itemised estimate of the gap to production. A "no" here is the cheapest answer
you'll get all week.

## Things worth knowing

**Artifacts land in `docs/agent-use/`.** That directory is agent-owned by convention — you're very
welcome to read and review what's in it, but it stays out of the way of your real docs. Committing it
is usually right (it's how the next session gets context), but if you'd rather not, one line in
`.gitignore` covers all of it.

**They're stack-agnostic on purpose.** Nothing here assumes a language, test runner, or framework —
the skills detect what your project already uses and follow it. If you want them to assume your
stack, edit the files; they're just Markdown, and that's the point.

**`/test` and `/dev` are common words.** Installed at user level, these shadow same-named plugin
skills — notably `anthropic-skills:test`. Rename the directories if you'd rather keep both.

**Skills nudge, they don't enforce.** These describe how to work, and a model can still misjudge one.
The human gate in `/dev` and the mandatory verdict in `/prototype` are there because the two moments
most worth checking are worth checking by a person.

## Credit

Built from [Agentic Workflow for Shipping Code](https://chaiilabs.com/blog/agentic-workflow-for-shipping-code),
which makes the argument these skills implement.

MIT licensed. Fork it and make it yours.
