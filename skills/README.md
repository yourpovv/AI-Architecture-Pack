# skills/ index

You get one folder per skill. You group them by what the skill is for. Each folder holds a `SKILL.md`
carrying YAML frontmatter: a `name`, and a `description` full of trigger phrases. Your
agent reads those descriptions and decides on its own when to load one. That is the
difference between this folder and [`../prompts/`](../prompts/README.md), which you paste
in by hand.

**The folder name is the skill's `name`.** That is not cosmetic. It lets you copy
a skill straight into `.claude/skills/` without renaming anything. Your setup stays clean.

```bash
cp -r skills/review/audit ~/.claude/skills/
```

---

## `agent/` — how the agent runs

| Skill | `name` | Fires when |
|---|---|---|
| **[sub-agents](./agent/sub-agents/SKILL.md)** | `sub-agents` | When you delegate work: model tiers, setting the model explicitly, writing a brief your agent can act on, commit authority, and when inline beats fan-out. Ends with a paste-ready block for your global `CLAUDE.md` |
| **[context-budget](./agent/context-budget/SKILL.md)** | `context-budget` | When your session feels expensive or keeps hitting limits: your always-loaded floor, prompt-cache mechanics and what silently breaks them, and why output is your costliest token |
| **[commits](./agent/commits/SKILL.md)** | `commits` | When you commit: one commit per task, staging only that task's files, message types, and never pushing unasked |
| **[claude-folder](./agent/claude-folder/SKILL.md)** | `claude-folder` | When you set up `.claude/`: CLAUDE.md vs CLAUDE.local.md, what each directory does for you, why your hook is not firing |

## `engineering/` — how code gets written

| Skill | `name` | Fires when |
|---|---|---|
| **[errors](./engineering/errors/SKILL.md)** | `errors` | How your code should fail, and how your failure should read to a human. Uncle Bob's error handling plus user-facing copy |
| **[uncle-bob](./engineering/uncle-bob/SKILL.md)** | `uncle-bob` | Structure, seams, architecture, TDD discipline, professional scope calls for you. Methodology, not a report about your repo |
| **[craft](./engineering/craft/SKILL.md)** | `craft` | Naming, comments, structure, and prose judged for the human who has to debug your code later |
| **[necessary-comments](./engineering/necessary-comments/SKILL.md)** | `necessary-comments` | When you decide whether your comment earns its keep, or whether a rename or extraction should replace it |

## `review/` — how work gets checked

| Skill | `name` | Fires when |
|---|---|---|
| **[audit](./review/audit/SKILL.md)** | `audit` | Any review, security pass, or audit on your code. Sets scope, mode, exclusions, severity, and output shape. **Required before every `prompts/reviews/*` file** |

## `web/` — shipping websites

| Skill | `name` | Fires when |
|---|---|---|
| **[web-seo](./web/web-seo/SKILL.md)** | `web-seo` | Meta and OG tags, canonical URLs, robots, sitemap, JSON-LD, per-route metadata in your SPA |

## `writing/` — documentation

| Skill | `name` | Fires when |
|---|---|---|
| **[create-readme](./writing/create-readme/SKILL.md)** | `create-readme` | Writing your README from the real tree instead of a template. You verify every claim against an opened file |
| **[prose](./writing/prose/SKILL.md)** | `prose` | Any written material from you: README, docs, PR body, commit message, changelog, release notes. Your single source of truth for prose rules in this pack |

---

### On "anti-slop" and humanizer skills

There is a genre of skill that strips AI tells from your prose and scores the result against a
rubric, sometimes with a pass threshold. [`prose`](./writing/prose/SKILL.md) covers the same
patterns those skills catch for you, including the structural ones that survive a word-level
cleanup. It stops short of the scoring. You do not need the score to write clean prose.

A detector score measures how your text was generated, and the thing worth measuring is whether
your teammate can follow your doc. Writing to move a score gives you docs that read oddly and
still fail their job, and your usual next step is adding deliberate inconsistency to look
human, which makes your file harder to trust. `prose` is also scoped to engineering writing,
so you can assume your reader is trying to complete a task rather than waiting to be persuaded.

If you want the rules run as an audit on your docs, use
[`../prompts/reviews/Docs-Review.md`](../prompts/reviews/Docs-Review.md).

---

[`../design/apple-design/`](../design/apple-design/SKILL.md) is built the same way but stays
opt-in for you, because your aesthetic should never fire on its own.

## Installing

Copy the skill folder. The name is already correct, so you rename nothing:

```bash
cp -r skills/review/audit .claude/skills/
cp -r skills/engineering/errors .claude/skills/
```

Use `~/.claude/skills/` instead of `.claude/skills/` to install for every project on your
machine. Category folders are for browsing this repo. Claude Code reads a flat
`skills/` directory, so you copy the individual skill folders rather than the category.

If you would rather not install anything, copy the files under `docs/skills/` and point
your `AGENTS.md` at them.

Exact paths and frontmatter keys are documented at
[code.claude.com/docs](https://code.claude.com/docs), and they do change between releases.
Listen. You check the docs when something stops working. [`claude-folder`](./agent/claude-folder/SKILL.md) covers your surrounding `.claude/` layout.

## Adding a skill

1. Pick the category your skill belongs to, or add one when nothing fits.
2. Create `skills/<category>/<name>/SKILL.md`, where `<name>` is kebab-case and matches
   the `name` in the frontmatter. Those two disagreeing is the most common reason your
   install silently does nothing.
3. Copy the frontmatter shape from [`engineering/errors`](./engineering/errors/SKILL.md).
4. Write the `description` for the matcher, not for a human. It should contain the phrases
   someone would actually type. A vague description means your skill never fires.
5. Keep the body portable. If it only makes sense on one stack, it belongs in
   [`../prompts/`](../prompts/README.md).
6. Add a row to the table above for your team.

## Authority

Skills lose to [`../standards/Clean-Code/`](../standards/Clean-Code/README.md) on naming,
functions, comments, null, exceptions, Demeter, DRY, CQS, and structure. Your Clean-Code lessons
outrank every skill here. See
[`../standards/README.md`](../standards/README.md). Why does that matter to you. Your team gets one authority
when two files disagree.
