---
name: coding-commits
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

An agent can produce a week of changes in an hour. Without a commit policy, the session ends
with one enormous uncommitted diff that nobody can review, bisect, or roll back except by
reading all of it at once. The fix is to commit each task as it finishes.

## The rule

**One commit per completed task, made as soon as the task is done.** Do not batch at the end
of the session, and do not wait for the human to ask.

Give the agent standing authorization for this in `CLAUDE.md`. Asking for approval on every
commit defeats the purpose, because the whole cost of the policy is the interruptions.

## Staging

**Stage the files the task touched:** `git add <paths>`, never `git add .`.

Agent sessions leave debris: scratch files, a log written while thinking, a config edited
while diagnosing something unrelated. `git add .` sweeps all of it into a commit that claims
to be one change. Naming paths is also the last scope check: a task that touched files you did
not expect did something you did not expect.

## Messages

```
<type>: <imperative summary of what changed>
```

| Type | For |
|---|---|
| `feat` | New behavior a user can observe |
| `fix` | Corrected behavior that was wrong |
| `refactor` | Same behavior, different structure |
| `docs` | Documentation only |
| `test` | Tests only |
| `chore` | Tooling, dependencies, config, housekeeping |
| `style` | Formatting with no logic change |

Examples: `feat: add user auth endpoint`, `fix: handle empty input in parser`.

Describe what changed, not what you did. "Update files" and "address feedback" are not commit
messages. Keep the subject under 72 characters, and put the why in the body when it is not
obvious from the subject.

## Pushing

**Never push automatically.** Commits stay local until the human asks.

Local commits are cheap to amend, reorder, or drop. A pushed commit is something other people
build on, and undoing it becomes their problem too. That decision belongs to the person who
knows what else is in flight.

## Splitting

If a task touched several concerns, make several commits in sequence. The test: if you cannot
describe the change in one line without "and", it is more than one commit.

## Who commits

The session that owns the work owns the commits. By default a sub-agent does not commit,
because only the parent can see whether the change is really finished (see
[`sub-agents`](../coding-sub-agents/SKILL.md)). Never grant commit authority to parallel agents sharing
a worktree.

Verify before every commit: read the diff you are about to stage and run the project's verify
gate. A tidy history of broken commits is worse than no history, because it looks trustworthy.

---

## Drop this in your CLAUDE.md

```markdown
## Commits

Commit after each completed task, immediately. Do not batch tasks into one commit.
This is standing authorization; do not ask per commit.

- Stage only that task's files: `git add <paths>`, never `git add .`
- Message format: `<type>: <imperative summary>`
- Types: feat, fix, refactor, docs, test, chore, style
- Never push. Commits stay local until I ask
- If a task touched several concerns, split it into sequential commits
- Read the diff and run the verify gate before staging
```
