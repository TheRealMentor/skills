---
name: handoff
description: Turn a working branch into reviewable history — split the diff into logical commits and write a PR description worth reading. Use when the user says they're ready to open a PR, wants the work committed properly, asks to clean up commits before review, or invokes /handoff. Stops before pushing or opening the PR.
---

# Handoff

The work is done; now make it reviewable. Commit messages and PR descriptions are cheap to write
while the reasoning is still in context, and expensive to reconstruct from `git blame` six weeks
later when something breaks and someone needs to know why this line exists.

## Process

### 1. Survey the change

```
git status
git log --oneline <base>..HEAD
git diff <base>...HEAD --stat
git diff <base>...HEAD
```

Work out the base branch rather than assuming (`git symbolic-ref refs/remotes/origin/HEAD`, or the
branch this one forked from). Read the full diff — you're about to describe it, and a summary from
`--stat` alone produces PR descriptions that say nothing.

Also read the tech doc in `docs/agent-use/` if one exists. The "why" belongs in the PR body and it's
already written there.

### 2. Match the repo's conventions

Read `git log -30 --format='%s'`. Follow whatever the repo already does — Conventional Commits,
ticket prefixes, plain sentences, whatever it is. Read `CONTRIBUTING.md` and any PR template in
`.github/` too. Don't impose a convention on someone else's repo.

### 3. Plan the split

Group the diff along logical boundaries — one coherent change per commit:

```
feat: add billing schema and migrations          (412 lines)
feat: implement stripe webhook handler           (1,004 lines)
test: cover webhook signature verification       (188 lines)
```

not:

```
fix features and stuff                           (1,604 lines)
```

Rules for the split:
- **Never mix a refactor with a behaviour change.** The single most common reason a reviewer can't
  tell what a PR actually does. Move-only and rename-only commits should be exactly that.
- Each commit should build and pass tests on its own where the change allows it. This is what makes a
  clean revert possible when something breaks at 2am.
- Split by reason-for-change, not by file type. "All the tests" is not a logical commit unless the
  tests are the change.
- Body text explains *why*, not what. The diff already shows what.

**Show the user the proposed split before creating anything**, with a line of rationale each. Cheap
to reorder now, annoying later.

### 4. Commit

Stage per commit deliberately (`git add <paths>`, or `git add -p` when a file spans two logical
commits). Verify with `git status` that nothing is left behind and nothing unintended got swept in —
check for stray debug output, `.env` files, and credentials before every commit.

### 5. Write the PR description

```markdown
## What
Two or three sentences a reviewer can read before the diff. What changes for the user.

## Why
The problem this solves. Link the tech doc (docs/agent-use/<feature>.md) and the issue.

## How to review
The reading order — which commit to start with and what to look at in each.
Flag the parts that need real scrutiny versus the parts that are mechanical.

## Testing
What you ran and what it said. Real output. New tests, and what they cover.

## Risk & rollback
What could break, what's behind a flag, how to undo this if it goes wrong.
Migrations get explicit rollback notes.

## Screenshots
For anything user-visible. Note that the user needs to add these if you can't.
```

### 6. Stop

Report the commits and hand over the PR body. **Do not push and do not open the PR** unless the user
explicitly asks — publishing is theirs to trigger, and a local commit is trivially amendable while a
pushed branch is not. If they want it, give them the command:

```bash
git push -u origin HEAD && gh pr create --title "<title>" --body-file <path>
```

## Boundary rules

- **Never mix refactor and behaviour change in one commit.**
- **Don't fix things during handoff.** If you spot a bug while reading the diff, report it — don't
  quietly add a seventh commit that changes what the reviewer thought they were reviewing.
- **Don't rewrite already-pushed history** without asking. Reordering local commits is fine;
  force-pushing over a branch someone may have pulled is not.
- **Push and PR creation need explicit approval,** every time. Approval to commit is not approval to
  publish.
- **Never commit secrets.** Scan the diff for keys, tokens, and `.env` files before staging.

## Report

End with: the commit list as created, the PR body (or its path), anything you found in the diff that
concerns you, and the exact command to push when they're ready.
