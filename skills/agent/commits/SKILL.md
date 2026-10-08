---
name: commits
description: >
  Commit discipline for agent-assisted work: one commit per completed task, staging
  only that task's files, conventional message types, and never pushing without being
  asked. Use when an agent is about to commit, when a session has produced a pile of
  unstaged changes across several tasks, or when deciding who owns commits between a
  parent session and its sub-agents. Trigger on "commit this", "should I commit",
  "write a commit message", "squash these", "git add", or any task finishing with
  changes on disk. Harness-agnostic.
---

# Commits

Listen. Your agent can produce a week of your changes in an hour. Without a commit policy you end up
with one enormous uncommitted diff that nobody on your team can review, bisect, or roll back. Then
your only way out is to read all of it at once. Do you want that job at midnight. You do not.

Your fix is boring and it works. You commit each task as it finishes. Your history stays honest.

## The rule

**One commit per completed task, made as soon as your task is done.** You do not batch at
the end of your session. You do not hold until your human asks. Small commits protect your team.

You give your agent standing authorization for this in your `CLAUDE.md`. Approval per commit
defeats your point, because the cost of your policy is entirely in the interruptions. You pay it
once up front and then you move.

## Staging

**You stage the files your task touched.** `git add <paths>`, never `git add .`.

Your agent sessions leave debris for you: scratch files, a log your agent wrote to think, a config it
edited while diagnosing something unrelated. `git add .` sweeps all of it into a commit
that claims to be one change. Naming paths is also your last check on scope. A task
that touches files you did not expect is a task that did something you did not expect. Professionals
check before they commit.

## Messages

```
<type>: <what changed>
```

| Type | For |
|---|---|
| `feat` | New behavior your user can observe |
| `fix` | Behavior you corrected that was wrong |
| `refactor` | Same behavior, structure you changed |
| `docs` | Documentation only you touched |
| `test` | Tests only you touched |
| `chore` | Tooling, deps, config, housekeeping you did |
| `style` | Formatting with no logic change from you |

`feat: add user auth endpoint`. `fix: resolve null check in parser`.

You describe what changed, not what you did. Ask yourself this. Would you accept
"Update files" and "address feedback" as commit messages. You should not. They are the absence of one.
Your teammate needs the why in one line.

## Pushing

**You never push automatically.** Your commits stay local until your human asks for them. That is discipline.

Your local commits are cheap to amend, reorder, or drop. A pushed commit is a fact other
people build on, and undoing it is their problem as much as yours. That decision belongs
to the person who knows what else is in flight. You ask. You do not assume.

## Splitting

If your task touched several concerns, you make several commits in sequence rather than one
that needs a paragraph to explain. Your test is simple. Can you describe your change in
one line without using "and". If you cannot, it is more than one commit. Keep each one clean.

## Who commits

Your session that owns the work owns your commits. See
[`sub-agents`](../sub-agents/SKILL.md): by default your sub-agent does not commit, because your
parent is the only one that can see whether your change is really finished. You never grant
commit authority to parallel agents sharing a worktree. That is how you avoid mixed up commits.

You verify before every commit. You read the diff you are about to stage and run your project's
verify gate. A clean commit history full of broken commits is worse than no history for you,
because it looks trustworthy. Do not ship lies in neat boxes.

---

## Drop this in your CLAUDE.md

```markdown
## Commits

Commit after each completed task, immediately. Do not batch tasks into one commit.
This is standing authorization, do not ask per commit.

- Stage only that task's files: `git add <paths>`, never `git add .`
- Message format: `<type>: <what changed>`
- Types: feat, fix, refactor, docs, test, chore, style
- Never push. Commits stay local until I ask
- If a task touched several concerns, split it into sequential commits
- Read the diff and run the verify gate before staging
```
