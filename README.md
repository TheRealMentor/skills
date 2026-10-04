<div align="center">

<h1><img src="assets/header.png" alt="Shipping-code skills" width="620"></h1>

**Five skills that stop your Claude Code sessions from forgetting what you asked for.**

Each stage of a feature gets its own clean context and hands the next one a file — not a scrollback.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skills-d97757)](https://claude.com/claude-code)
[![Stack agnostic](https://img.shields.io/badge/stack-agnostic-brightgreen)](#-good-to-know)

</div>

---

```mermaid
flowchart LR
    P("/personal:prototype<br/>can this be built?") -. "if confirm" .-> TD
    TD("/personal:create-td<br/><b>design</b>") --> DEV("/personal:dev<br/><b>build</b><br/>🛑 approval gate")
    DEV --> TEST("/personal:test<br/><b>verify</b>")
    TEST --> HO("/personal:handoff<br/><b>ship</b>")
```

<div align="center"><sub><b>↑</b> <code>/personal:dev</code> stops for your approval before it writes a single line of code.</sub></div>

## ✅ Before you start

|              | What                                            | Why                                                                                                                                           |
| :----------: | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Required** | [Claude Code](https://claude.com/claude-code)   | These are Claude Code skills. CLI, desktop, web, or IDE extension — any of them.                                                              |
| **Required** | A **git repo**                                  | `/personal:handoff` commits and `/personal:prototype` branches. `/personal:create-td` and `/personal:test` work fine without one.             |
| **Required** | **bash** to run the installer                   | Native on macOS and Linux; on Windows use WSL or Git Bash. Or skip it and copy the folders by hand.                                           |
| Recommended  | A **`CLAUDE.md`** or **`PRODUCT.md`**           | `/personal:create-td` and `/personal:test` read it as your project's source of truth. Without one, `/personal:test` has to ask you what the feature is _supposed_ to do. |
|   Optional   | **[`gh`](https://cli.github.com)** (GitHub CLI) | Lets `/personal:create-td` read a linked issue and `/personal:handoff` open the PR for you. Both work without it.                             |

**No language or runtime requirements.** The skills detect whatever your project already uses — test
runner, package manager, commit conventions — and follow it. Nothing to configure.

> ℹ️ `/personal:dev` parallelises independent tasks across **subagents**, using **git worktrees** when they'd
> otherwise collide. Both ship with Claude Code and git; there's nothing extra to install.

## ⚡ Install

```bash
git clone https://github.com/TheRealMentor/skills.git shipping-skills
cd shipping-skills && ./install.sh
```

Start a new Claude Code session, then type `/personal:create-td`. That's it.

<details>
<summary>Other ways to install</summary>

<br>

**Want an editable copy instead of a symlink?**

```bash
./install.sh --copy
```

By default the installer symlinks, so `git pull` here updates your install. `--copy` gives you a copy
you can freely edit in place.

**Prefer to do it by hand?** There's nothing magic in the script — this repo *is* a Claude Code
plugin (see `.claude-plugin/plugin.json`), so a single symlink at the plugin's name is all it takes:

```bash
ln -s "$(pwd)" ~/.claude/skills/personal
```

Either way it's idempotent, and it will never overwrite something at that path that this script didn't
put there.

</details>

## 🤔 Why

Three hours into one long chat, the agent starts forgetting requirements, re-deciding settled
questions, and tripping over its own stale context.

That's not really a model limitation — it's a context management one. And it's the same mistake as
cramming an entire program into one giant function. So split it by responsibility.

> **Artifacts over memory** — specs belong in files. Any agent can read a file in a fresh context; a
> fact mentioned 40 messages ago is gone.
>
> **Narrow context beats large context** — an agent holding one feature's design outperforms one
> holding your entire repo history. Relevance beats volume.
>
> **Checkpoints where they're cheap** — review a task breakdown _before_ code exists, not a diff
> afterwards. Same mistake, two orders of magnitude difference in cost.

## 🛠 The five skills

|     | Skill                     | What it does                                                               | Writes                        |
| :-: | ------------------------- | --------------------------------------------------------------------------- | ----------------------------- |
| 📐  | **`/personal:create-td`** | Requirements → technical design. Reads your code, writes none of it.       | `docs/agent-use/<feature>.md` |
| 🔨  | **`/personal:dev`**       | Design → task breakdown → **your approval** → implementation, parallelised | `…/<feature>.tasks.md` + code |
| 🧪  | **`/personal:test`**      | Tests written from the spec, read _before_ the implementation              | test files                    |
| 📦  | **`/personal:handoff`**   | Logical commits + a PR description worth reading                           | git history + PR body         |
| 🔬  | **`/personal:prototype`** | Throwaway branch answering "can this even be built?"                       | `…/prototypes/<slug>.md`      |
| ✍️  | **`/personal:simplify-text`** | Rewrites text in Simplified Technical English — short, clear, hard to misread. | rewritten text |

Every skill has **one job and one line it won't cross.** That's what makes them predictable:

| Skill                    | The line it won't cross                                        |
| ------------------------ | ---------------------------------------------------------------- |
| 📐 `/personal:create-td` | Won't touch source. Not one line.                              |
| 🔨 `/personal:dev`       | Won't write code before you approve the breakdown.             |
| 🧪 `/personal:test`      | Won't edit a test to make it match buggy code.                 |
| 📦 `/personal:handoff`   | Won't push or open a PR unasked.                               |
| 🔬 `/personal:prototype` | Won't finish without telling you what production really costs. |

## 🚶 A run through, end to end

<details open>
<summary><b>📐 Design it</b></summary>

```
/personal:create-td add SSO login for enterprise accounts
```

Reads your `CLAUDE.md` and the auth code that exists today, asks the one or two questions that would
genuinely change the design, and writes `docs/agent-use/sso-login.md` — problem, non-goals, contracts,
risks, and acceptance criteria in user-visible terms.

Your source tree is untouched. Check `git status` if you don't believe it.

> 💡 **Read it. It's a page.** Fixing the design here costs you a comment.

</details>

<details open>
<summary><b>🔨 Build it</b></summary>

```
/personal:dev docs/agent-use/sso-login.md
```

Breaks the design into tasks — each with the files it touches, what it depends on, and a command that
proves it works — then **stops and shows you the list.**

> 🛑 **This is the checkpoint that pays for the whole workflow.** A wrong assumption caught here costs
> five minutes. The same one caught after implementation costs a day.

Approve it, and independent tasks fan out to subagents that share contracts but never each other's
internals.

</details>

<details open>
<summary><b>🧪 Verify it</b></summary>

```
/personal:test sso-login
```

Reads the acceptance criteria _before_ the implementation — deliberately, so the tests describe what
the feature **should** do rather than what the code **happens** to do.

When the two disagree, it tells you which one it thinks is wrong instead of quietly bending the test.

</details>

<details open>
<summary><b>📦 Ship it</b></summary>

```
/personal:handoff
```

Splits the branch into commits that actually mean something, writes the PR body, and stops before
pushing.

```diff
- fix features and stuff                          (1,604 lines)

+ feat: add billing schema and migrations           (412 lines)
+ feat: implement stripe webhook handler          (1,004 lines)
+ test: cover webhook signature verification        (188 lines)
```

</details>

<details>
<summary><b>🔬 …and when you don't yet know if it's possible</b></summary>

<br>

```
/personal:prototype can we stream model output through our existing SSE layer?
```

Throwaway branch, ugliest possible code, and a mandatory verdict at the end: the answer, everything
that was faked, and an itemised estimate of the gap to production.

> 💡 **A "no" here is the cheapest answer you'll get all week.**

</details>

## 📋 Good to know

<details>
<summary><b>Where the artifacts go</b></summary>

<br>

Everything lands in **`docs/agent-use/`** — agent-owned by convention. You're very welcome to read
and review what's in there, but it stays out of the way of your real docs.

Committing it is usually right (it's how the next session gets context). If you'd rather not, one
line in `.gitignore` covers all of it:

```gitignore
docs/agent-use/
```

</details>

<details>
<summary><b>They're stack-agnostic on purpose</b></summary>

<br>

Nothing here assumes a language, test runner, or framework — the skills detect what your project
already uses and follow it.

If you'd rather they just assume your stack, **edit them.** They're plain Markdown, and that's rather
the point.

</details>

<details>
<summary><b>Skills nudge, they don't enforce</b></summary>

<br>

These describe how to work, and a model can still misjudge one.

The human gate in `/personal:dev` and the mandatory verdict in `/personal:prototype` exist precisely because the two
moments most worth checking are worth checking **by a person.**

</details>

---

<div align="center">

Built from **[Agentic Workflow for Shipping Code](https://chaiilabs.com/blog/agentic-workflow-for-shipping-code)**,
which makes the argument these skills implement.

MIT licensed — fork it and make it yours.

</div>
