# skills/ index

One folder per skill, grouped by purpose. Each folder holds a `SKILL.md` with YAML
frontmatter: a `name` and a `description` full of trigger phrases. The agent reads the
descriptions and decides on its own when to load a skill. That is the difference from
[`../prompts/`](../prompts/README.md), which you paste in by hand.

This folder is the source. Installable builds live in [`../dist/skills/`](../dist/skills/),
where every skill is prefixed `coding-` so they group together in Claude Code. Install them all
with `./install.sh` or `.\install.ps1` from the pack root (see [Installing](#installing)).

---

## `agent/`: how the agent runs

| Skill | Installed as | Fires when |
|---|---|---|
| **[sub-agents](./agent/sub-agents/SKILL.md)** | `coding-sub-agents` | Delegating work: model tiers, setting the model explicitly, writing a brief an agent can act on, commit authority, and when inline beats fan-out. Ends with a paste-ready block for the global `CLAUDE.md` |
| **[context-budget](./agent/context-budget/SKILL.md)** | `coding-context-budget` | A session feels expensive or keeps hitting limits: the always-loaded floor, prompt-cache mechanics and what silently breaks them, and why output tokens cost the most |
| **[commits](./agent/commits/SKILL.md)** | `coding-commits` | Committing: one commit per task, staging only that task's files, message types, never pushing unasked |
| **[claude-folder](./agent/claude-folder/SKILL.md)** | `coding-claude-folder` | Setting up `.claude/`: CLAUDE.md vs CLAUDE.local.md, what each directory does, why a hook is not firing |

## `engineering/`: how code gets written

| Skill | Installed as | Fires when |
|---|---|---|
| **[standards](./engineering/standards/SKILL.md)** | `coding-standards` | Any code you write, edit, refactor, or review. The core rules from all 60 Clean-Code lessons, a per-language error mapping, and review mode. Bundles `standards/Clean-Code/` and `Principles.md` |
| **[errors](./engineering/errors/SKILL.md)** | `coding-errors` | How code should fail and how the failure should read to a human: Uncle Bob's error handling plus user-facing copy |
| **[uncle-bob](./engineering/uncle-bob/SKILL.md)** | `coding-uncle-bob` | Structure, seams, architecture, TDD discipline, and professional scope calls. Methodology, not a report about one repo |
| **[craft](./engineering/craft/SKILL.md)** | `coding-craft` | Naming, comments, structure, and prose judged for the person who debugs the code later |
| **[necessary-comments](./engineering/necessary-comments/SKILL.md)** | `coding-necessary-comments` | Deciding whether a comment earns its place, or whether a rename or extraction should replace it |

## `review/`: how work gets checked

| Skill | Installed as | Fires when |
|---|---|---|
| **[audit](./review/audit/SKILL.md)** | `coding-audit` | Any review, security pass, or audit. Sets scope, mode, exclusions, severity, and output shape. **Required before every `prompts/reviews/*` file** |

## `web/`: shipping websites

| Skill | Installed as | Fires when |
|---|---|---|
| **[web-seo](./web/web-seo/SKILL.md)** | `coding-web-seo` | Meta and OG tags, canonical URLs, robots, sitemap, JSON-LD, per-route metadata in a SPA |

## `writing/`: documentation

| Skill | Installed as | Fires when |
|---|---|---|
| **[create-readme](./writing/create-readme/SKILL.md)** | `coding-create-readme` | Writing a README from the real tree instead of a template, verifying every claim against an opened file |
| **[prose](./writing/prose/SKILL.md)** | `coding-prose` | Any written material: README, docs, PR body, commit message, changelog, release notes. The single source of prose rules in this pack |

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

From the pack root:

```bash
./install.sh              # every project: ~/.claude/skills/
./install.sh --project    # this directory only: ./.claude/skills/
```

On Windows PowerShell use `.\install.ps1` or `.\install.ps1 -Project`. The installer copies
every `coding-*` skill from `../dist/skills/`, replacing older installs of the same name. Start
a new Claude Code session afterwards. To install one skill, copy its folder from
`../dist/skills/` by hand.

To use a skill without installing it, copy the file under `docs/skills/` and point
`AGENTS.md` at it.

Exact paths and frontmatter keys are documented at
[code.claude.com/docs](https://code.claude.com/docs) and change between releases. Check the
docs when something stops working. [`claude-folder`](./agent/claude-folder/SKILL.md) covers the
surrounding `.claude/` layout.

## Adding a skill

1. Pick the category the skill belongs to, or add one when nothing fits.
2. Create `skills/<category>/<name>/SKILL.md`, where `<name>` is kebab-case and matches the
   `name` in the frontmatter. The build adds the `coding-` prefix to both.
3. Copy the frontmatter shape from [`engineering/errors`](./engineering/errors/SKILL.md).
4. Write the `description` for the matcher, not for a human. Include the phrases someone would
   actually type. A vague description means the skill never fires.
5. Keep the body portable. If it only makes sense on one stack, it belongs in
   [`../prompts/`](../prompts/README.md).
6. Add a row to the matching table above.
7. Run `python scripts/build_skills.py` to regenerate `../dist/skills/`, and commit the result.
   Never edit `dist/` by hand; the next build overwrites it.

## Authority

On naming, functions, comments, null, exceptions, Demeter, DRY, CQS, and structure, the
lessons in [`../standards/Clean-Code/`](../standards/Clean-Code/README.md) outrank every skill
here. See [`../standards/README.md`](../standards/README.md) for the full order.
