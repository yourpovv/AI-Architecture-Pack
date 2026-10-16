# skills/ index

One folder per skill, grouped by purpose. Each folder holds a `SKILL.md` with YAML
frontmatter: a `name` and a `description` full of trigger phrases. The agent reads the
descriptions and decides on its own when to load a skill. That is the difference from
[`../prompts/`](../prompts/README.md), which you paste in by hand.

**The folder name is the skill's `name`,** so a skill copies straight into `.claude/skills/`
without renaming:

```bash
cp -r skills/review/audit ~/.claude/skills/
```

---

## `agent/`: how the agent runs

| Skill | `name` | Fires when |
|---|---|---|
| **[sub-agents](./agent/sub-agents/SKILL.md)** | `sub-agents` | Delegating work: model tiers, setting the model explicitly, writing a brief an agent can act on, commit authority, and when inline beats fan-out. Ends with a paste-ready block for the global `CLAUDE.md` |
| **[context-budget](./agent/context-budget/SKILL.md)** | `context-budget` | A session feels expensive or keeps hitting limits: the always-loaded floor, prompt-cache mechanics and what silently breaks them, and why output tokens cost the most |
| **[commits](./agent/commits/SKILL.md)** | `commits` | Committing: one commit per task, staging only that task's files, message types, never pushing unasked |
| **[claude-folder](./agent/claude-folder/SKILL.md)** | `claude-folder` | Setting up `.claude/`: CLAUDE.md vs CLAUDE.local.md, what each directory does, why a hook is not firing |

## `engineering/`: how code gets written

| Skill | `name` | Fires when |
|---|---|---|
| **[errors](./engineering/errors/SKILL.md)** | `errors` | How code should fail and how the failure should read to a human: Uncle Bob's error handling plus user-facing copy |
| **[uncle-bob](./engineering/uncle-bob/SKILL.md)** | `uncle-bob` | Structure, seams, architecture, TDD discipline, and professional scope calls. Methodology, not a report about one repo |
| **[craft](./engineering/craft/SKILL.md)** | `craft` | Naming, comments, structure, and prose judged for the person who debugs the code later |
| **[necessary-comments](./engineering/necessary-comments/SKILL.md)** | `necessary-comments` | Deciding whether a comment earns its place, or whether a rename or extraction should replace it |

## `review/`: how work gets checked

| Skill | `name` | Fires when |
|---|---|---|
| **[audit](./review/audit/SKILL.md)** | `audit` | Any review, security pass, or audit. Sets scope, mode, exclusions, severity, and output shape. **Required before every `prompts/reviews/*` file** |

## `web/`: shipping websites

| Skill | `name` | Fires when |
|---|---|---|
| **[web-seo](./web/web-seo/SKILL.md)** | `web-seo` | Meta and OG tags, canonical URLs, robots, sitemap, JSON-LD, per-route metadata in a SPA |

## `writing/`: documentation

| Skill | `name` | Fires when |
|---|---|---|
| **[create-readme](./writing/create-readme/SKILL.md)** | `create-readme` | Writing a README from the real tree instead of a template, verifying every claim against an opened file |
| **[prose](./writing/prose/SKILL.md)** | `prose` | Any written material: README, docs, PR body, commit message, changelog, release notes. The single source of prose rules in this pack |

---

### On "anti-slop" and humanizer skills

Some skills strip AI tells from prose and score the result against a rubric, sometimes with a
pass threshold. [`prose`](./writing/prose/SKILL.md) covers the same patterns, including the
structural ones that survive a word-level cleanup, but it does not score.

A detector score measures how text was generated. What matters is whether a teammate can
follow the doc. Writing to move a score produces docs that read oddly and still fail their
job, and the usual next step, adding deliberate inconsistency to look human, makes the file
harder to trust. `prose` is also scoped to engineering writing, where the reader is trying to
complete a task rather than waiting to be persuaded.

To run the rules as an audit, use [`../prompts/reviews/Docs-Review.md`](../prompts/reviews/Docs-Review.md).

---

[`../design/apple-design/`](../design/apple-design/SKILL.md) is built the same way but stays
opt-in, because an aesthetic should never apply on its own.

## Installing

Copy the skill folder. The name is already correct:

```bash
cp -r skills/review/audit .claude/skills/
cp -r skills/engineering/errors .claude/skills/
```

Use `~/.claude/skills/` instead of `.claude/skills/` to install for every project on the
machine. Category folders are for browsing this repo. Claude Code reads a flat `skills/`
directory, so copy individual skill folders, not categories.

To use a skill without installing it, copy the file under `docs/skills/` and point
`AGENTS.md` at it.

Exact paths and frontmatter keys are documented at
[code.claude.com/docs](https://code.claude.com/docs) and change between releases. Check the
docs when something stops working. [`claude-folder`](./agent/claude-folder/SKILL.md) covers the
surrounding `.claude/` layout.

## Adding a skill

1. Pick the category the skill belongs to, or add one when nothing fits.
2. Create `skills/<category>/<name>/SKILL.md`, where `<name>` is kebab-case and matches the
   `name` in the frontmatter. A mismatch between the two is the most common reason an install
   silently does nothing.
3. Copy the frontmatter shape from [`engineering/errors`](./engineering/errors/SKILL.md).
4. Write the `description` for the matcher, not for a human. Include the phrases someone would
   actually type. A vague description means the skill never fires.
5. Keep the body portable. If it only makes sense on one stack, it belongs in
   [`../prompts/`](../prompts/README.md).
6. Add a row to the matching table above.

## Authority

On naming, functions, comments, null, exceptions, Demeter, DRY, CQS, and structure, the
lessons in [`../standards/Clean-Code/`](../standards/Clean-Code/README.md) outrank every skill
here. See [`../standards/README.md`](../standards/README.md) for the full order.
