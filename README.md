<div align="center">

# Architecture Pack

**Engineering standards, agent skills, and task prompts for building software with AI agents.**

Portable, stack-agnostic, and project-neutral. Copy the parts a repo needs into that repo.

<a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-2f363d?style=flat-square"></a>
<img alt="Stack agnostic" src="https://img.shields.io/badge/scope-stack--agnostic-2f363d?style=flat-square">
<img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2f363d?style=flat-square">
<img alt="Built for Claude Code" src="https://img.shields.io/badge/built_for-Claude_Code-2f363d?style=flat-square">

</div>

---

## TL;DR

1. Copy [`standards/Clean-Code/`](standards/Clean-Code/README.md) into the repo's `docs/`, plus
   a [`frameworks/*`](frameworks/README.md) file if one applies.
2. Write a short `AGENTS.md` at the repo root that points at them, lists what the agent may
   edit, and names the commands that verify its work.
3. Tell the agent to load one file at a time, never the whole folder.

Then install the audit harness so every review has an explicit scope and stays `report-only`
until you switch it to `fix`:

```bash
cp -r skills/review/audit .claude/skills/
```

[Project templates](#project-templates) lists the files to copy for each kind of project.

---

## Why this exists

Agent-built code fails in two common ways.

**There is no standard to code against.** Each file invents its own conventions, and after a
couple of weeks the project stops reading like one codebase. Nothing is visibly broken, so
nothing gets fixed.

**The agent gets everything at once.** The whole repo, every doc, and a 20-page style guide
crowd the context window, and the instructions that matter get buried.

The pack splits the standards into one rule per file, so the agent opens only the lesson the
task needs. Every review prompt carries its own scope and mode, so an audit cannot quietly
turn into a rewrite. Nothing is tied to one project.

---

## What is inside

<table>
<thead>
<tr><th align="left">Layer</th><th align="left">Contents</th><th align="left">When to load it</th></tr>
</thead>
<tbody>
<tr>
  <td><a href="standards/README.md"><b><code>standards/</code></b></a></td>
  <td>60 language-agnostic clean-code lessons, one rule per file, plus a handbook on SOLID, architecture, testing, concurrency, and security that agrees with them</td>
  <td>Every serious project</td>
</tr>
<tr>
  <td><a href="skills/README.md"><b><code>skills/</code></b></a></td>
  <td>Guidance that triggers on its own: audit harness, error handling, comment discipline, prose rules, sub-agent routing, <code>.claude/</code> setup</td>
  <td>Install once</td>
</tr>
<tr>
  <td><a href="frameworks/README.md"><b><code>frameworks/</code></b></a></td>
  <td>Framework conventions: React + Tailwind, Tauri, Electron, Valkyrie, Dear ImGui</td>
  <td>Only when one applies</td>
</tr>
<tr>
  <td><a href="prompts/README.md"><b><code>prompts/</code></b></a></td>
  <td>Paste-in tasks: reviews and audits, greenfield scaffolds, and workflow rules that stop the agent from guessing</td>
  <td>One per task</td>
</tr>
<tr>
  <td><a href="design/README.md"><b><code>design/</code></b></a></td>
  <td>Opt-in aesthetic systems, plus vetted sources for components, icons, illustrations, and 3D assets</td>
  <td>Only for UI work that wants them</td>
</tr>
<tr>
  <td><a href="STACK.md"><b><code>STACK.md</code></b></a></td>
  <td>A walkthrough for choosing a stack, plus default services and AI tooling</td>
  <td>When starting something new</td>
</tr>
</tbody>
</table>

The lessons are written in language-neutral pseudocode. Each one says to translate the
examples into the repo's language, and
[`skills/engineering/errors/SKILL.md`](skills/engineering/errors/SKILL.md) maps the error rules
onto languages without exceptions.

---

## Quick start

### 1. Copy what the project needs

```
your-project/
├── AGENTS.md                        <- you write this, see step 2
└── docs/
    ├── standards/
    │   ├── Clean-Code/              <- the mandatory 60
    │   └── Principles.md
    └── frameworks/Tauri.md          <- optional
```

Keep the same relative layout so cross-references still resolve.

### 2. Write a short `AGENTS.md` at the repo root

This step decides whether the rest works. `AGENTS.md` is the only file that knows about your
project.

```markdown
## Coding standards
Mandatory: docs/standards/Clean-Code/
Load only the lesson file(s) relevant to the task, never the whole folder.
Prefer rename / extract / split / wrap over comments or error-code returns.
Full map: docs/standards/Clean-Code/README.md

## Owned code
src/**        agent may edit
migrations/** ask first
vendor/**     never edit

## Verify
bun test
bun run typecheck
```

### 3. State the rules once, at the start

> Read `AGENTS.md` first. Coding standards live in `docs/standards/Clean-Code/`; load only the
> lesson file that matches the task. For any review, read `docs/skills/review/audit/SKILL.md`
> and set scope and mode (`report-only` by default). Load at most one framework file and one
> prompt. Do not load the whole `Clean-Code/` folder or all of `Principles.md` unless auditing
> against the full map.

---

## Project templates

Each row is a complete setup. Copy the files, then paste the prompt for the task.

<table>
<thead>
<tr><th align="left">Building</th><th align="left">Copy into <code>docs/</code></th><th align="left">Then paste</th></tr>
</thead>
<tbody>
<tr>
  <td><b>Desktop app</b><br><sub>Tauri</sub></td>
  <td><code>standards/Clean-Code/</code><br><code>frameworks/Tauri.md</code></td>
  <td><code>prompts/reviews/Tauri-QC.md</code> before shipping</td>
</tr>
<tr>
  <td><b>Desktop app</b><br><sub>Electron or Valkyrie</sub></td>
  <td><code>standards/Clean-Code/</code><br><code>frameworks/Electron.md</code> or <code>frameworks/Valkyrie.md</code></td>
  <td><code>prompts/reviews/Code-Review.md</code></td>
</tr>
<tr>
  <td><b>Native tool UI</b><br><sub>Dear ImGui</sub></td>
  <td><code>standards/Clean-Code/</code><br><code>frameworks/Dear-ImGui.md</code></td>
  <td><code>prompts/reviews/Code-Review.md</code></td>
</tr>
<tr>
  <td><b>Website or web app</b></td>
  <td><code>standards/Clean-Code/</code><br><code>frameworks/React-Tailwind.md</code><br><code>skills/web/web-seo/SKILL.md</code></td>
  <td><code>prompts/scaffolds/Website.md</code><br><code>prompts/scaffolds/Website-Design.md</code></td>
</tr>
<tr>
  <td><b>Discord bot</b></td>
  <td><code>standards/Clean-Code/</code></td>
  <td><code>prompts/scaffolds/Discord-Bot.md</code></td>
</tr>
<tr>
  <td><b>Backend service</b></td>
  <td><code>standards/Clean-Code/</code><br><code>standards/Principles.md</code></td>
  <td><code>prompts/reviews/Performance-Scalability-Review.md</code></td>
</tr>
<tr>
  <td><b>Game, CLI, or library</b></td>
  <td><code>standards/Clean-Code/</code></td>
  <td><code>prompts/reviews/PR-Review.md</code></td>
</tr>
</tbody>
</table>

Every template starts with `standards/Clean-Code/` because the definition of good code
outlives any particular language or framework.

---

## Load one file at a time

A model given sixty rules at once follows none of them well, and every lesson it reads but
does not apply is context it cannot spend on the code. So every file here is built to be
opened alone: one rule per standards file, an `Agent load` line at the top of each framework
guide naming the sections to read first, and self-contained prompts.

<details>
<summary><b>Default load, and what to add on demand</b></summary>

<br>

**Default load**

1. The project's `AGENTS.md`.
2. The relevant README or tracker.
3. `skills/review/audit/SKILL.md` when reviewing, auditing, or shipping.
4. At most one framework file.
5. One prompt matching the task.

**On demand**

| Doc | When |
|---|---|
| `standards/Clean-Code/NN-*.md` | The primary craft standard. Load one lesson by topic |
| `standards/Clean-Code/README.md` | The full map, for audits against every rule |
| `standards/Principles.md` | SOLID, architecture, testing, concurrency, security. One section at a time |
| `skills/engineering/errors/SKILL.md` | Failure handling and user-facing error copy |
| `skills/engineering/uncle-bob/SKILL.md` | Structure, seams, and professional scope calls |
| `skills/engineering/craft/SKILL.md` | Naming, comments, and structure judged for readability |
| `skills/engineering/necessary-comments/SKILL.md` | Whether a comment earns its place |
| `skills/writing/create-readme/SKILL.md` | A README written from the real tree |
| `skills/writing/prose/SKILL.md` | Any README, doc, PR body, or commit message |
| `skills/web/web-seo/SKILL.md` | Shipping a public site |
| `skills/agent/sub-agents/SKILL.md` | Delegating work and choosing model tiers |
| `skills/agent/context-budget/SKILL.md` | Sessions that feel expensive or keep hitting limits |
| `skills/agent/commits/SKILL.md` | The agent is about to commit, or changes have piled up |
| `skills/agent/claude-folder/SKILL.md` | Setting up `.claude/`, or a hook that will not fire |
| `prompts/workflow/Before-Implementing.md` | The agent is about to build on a guess |
| `prompts/reviews/PR-Review.md` | A pre-merge go/no-go |
| `prompts/reviews/Docs-Review.md` | Docs have drifted from the code or read badly |
| `design/apple-design/SKILL.md` | An explicit request for the Apple aesthetic |
| `STACK.md` | No stack chosen yet |

**Never default-load**

- The entire `standards/Clean-Code/` folder
- All of `standards/Principles.md`
- The entire `prompts/` tree
- `STACK.md` in a project that already chose its stack
- `design/apple-design/SKILL.md` for non-Apple UI

</details>

<details>
<summary><b>Authority, for when two files disagree</b></summary>

<br>

1. The project's **`AGENTS.md`**, only for an exception it names explicitly
2. **`standards/Clean-Code/`**, the craft source of truth
3. **`skills/engineering/uncle-bob/SKILL.md`**, the methodology
4. Other `skills/*` and **`standards/Principles.md`**
5. **`frameworks/*`**, for framework syntax and project layout only

Without a fixed order, an agent facing contradictory advice invents a preference and gives a
different answer every session.

</details>

---

## Prompts vs skills

The difference is who decides when the guidance applies.

|  | `prompts/` | `skills/` and `design/` |
|---|---|---|
| **How it is used** | Pasted into chat for a specific task | Installed once; the agent loads it when the task matches |
| **Frontmatter** | Optional | `name` plus a `description` full of trigger phrases |
| **Best for** | One-off tasks with a clear start and end | Standing rules that should apply without anyone remembering them |

Every review and audit prompt obeys [`skills/review/audit/SKILL.md`](skills/review/audit/SKILL.md):
explicit scope, `report-only` by default, and verification with commands taken from the
project, never invented.

### Installing the skills

Every skill is a folder holding a `SKILL.md`, named the way Claude Code expects. Copy the
folder:

```bash
cp -r skills/review/audit .claude/skills/
```

Use `~/.claude/skills/` to install for every project on the machine. The category folders
(`agent/`, `engineering/`, `review/`, `web/`, `writing/`) exist for browsing this repo. Claude
Code reads a flat skills directory, so copy the individual skill folders, not the category. The
full list with triggers is in [`skills/README.md`](skills/README.md).

Harness details change between releases. [`code.claude.com/docs`](https://code.claude.com/docs)
is the authority on exact paths, settings keys, and hook events. This pack covers what to put
in them.

---

<details>
<summary><b>Full layout</b></summary>

<br>

```
Architecture/
├── README.md                       this file
├── STACK.md                        stack decisions, services, AI tooling
├── LICENSE
│
├── standards/                      UNIVERSAL, applies to every project
│   ├── README.md
│   ├── Principles.md               SOLID, architecture, testing, security
│   └── Clean-Code/                 60 lesson standards, one rule per file
│       ├── README.md               the full map plus topic clusters
│       ├── 01-*.md ... 41-*.md
│       └── solid|classes|function-design|unit-tests|boundaries/
│
├── skills/                         INSTALLABLE, one folder per skill
│   ├── README.md
│   ├── agent/                      how the agent runs
│   │   ├── sub-agents/SKILL.md     delegation, model tiers, briefing
│   │   ├── context-budget/SKILL.md the startup floor, caching, output cost
│   │   ├── commits/SKILL.md        one commit per task, staging, messages
│   │   └── claude-folder/SKILL.md  .claude/ layout and hook registration
│   ├── engineering/                how code gets written
│   │   ├── errors/SKILL.md         failure handling and user-facing copy
│   │   ├── uncle-bob/SKILL.md      craft methodology
│   │   ├── craft/SKILL.md          naming, comments, structure
│   │   └── necessary-comments/SKILL.md
│   ├── review/
│   │   └── audit/SKILL.md          required harness for every review
│   ├── web/
│   │   └── web-seo/SKILL.md        meta, OG, canonical, sitemap, JSON-LD
│   └── writing/
│       ├── create-readme/SKILL.md  README written from the real tree
│       └── prose/SKILL.md          the prose rules the pack defers to
│
├── design/                         INSTALLABLE, opt-in only
│   ├── README.md                   plus sources for components, icons, assets
│   ├── apple-design/SKILL.md       pack-owned Apple aesthetic
│   ├── emil-design-eng/SKILL.md    vendored, see design/README.md
│   ├── animate/, animation-vocabulary/, review-animations/
│   ├── improve-animations/, find-animation-opportunities/
│   ├── prototype/, mobile-native/, break-ui/, pick-ui-library/
│   ├── impeccable/SKILL.md         vendored, see design/README.md
│   ├── design-taste-frontend/SKILL.md
│   ├── redesign-existing-projects/SKILL.md
│   ├── image-to-code/SKILL.md
│   └── font-pairing/SKILL.md
│
├── frameworks/                     optional, one per project
│   ├── README.md
│   ├── React-Tailwind.md
│   ├── Tauri.md
│   ├── Electron.md
│   ├── Valkyrie.md
│   └── Dear-ImGui.md
│
└── prompts/                        PASTE-IN, never auto-loaded
    ├── README.md
    ├── workflow/                   how the agent behaves, any stack
    │   └── Before-Implementing.md
    ├── reviews/                    always pair with skills/review/audit/SKILL.md
    │   ├── PR-Review.md
    │   ├── Code-Review.md
    │   ├── Security-Audit.md
    │   ├── Error-Handling-And-Observability.md
    │   ├── Performance-Scalability-Review.md
    │   ├── Docs-Review.md
    │   ├── Spacing-Audit.md
    │   └── Tauri-QC.md
    └── scaffolds/                  greenfield builds
        ├── Discord-Bot.md
        ├── Website.md
        ├── Website-Design.md
        └── Readme-Voice.md
```

`prompts/domains/` is a documented extension point, not a shipped folder. Create
`prompts/domains/<your-stack>/` for threat models that apply to one platform only.

</details>

<details>
<summary><b>Example prompts</b></summary>

<br>

**Stop the agent building on a guess**

```
Read prompts/workflow/Before-Implementing.md.
Then: <what you want built>.
```

**Run a production review**

```
Read skills/review/audit/SKILL.md and prompts/reviews/PR-Review.md.
Scope: <paths>. Mode: report-only.
```

**Build a website**

```
Read prompts/scaffolds/Website.md and frameworks/React-Tailwind.md.
Build only the pages we discussed.
```

**Build a Discord bot**

```
Read prompts/scaffolds/Discord-Bot.md.
Build a bot that posts daily standup reminders.
```

**Write a README from the real tree**

```
Read skills/writing/create-readme/SKILL.md, and prompts/scaffolds/Readme-Voice.md for voice.
Write README.md from the actual repo. No guessing.
```

**Run a docs pass**

```
Read skills/review/audit/SKILL.md and prompts/reviews/Docs-Review.md.
Scope: README.md and docs/**. Mode: report-only.
```

**Run a craft pass**

```
Read skills/engineering/craft/SKILL.md and skills/engineering/uncle-bob/SKILL.md.
Review naming, comments, and structure for maintainability.
```

</details>

---

## Extending the pack

Every folder's README has an "Adding" section with the required shape. In short:

| Adding a | Start from | Then |
|---|---|---|
| **Skill** | The frontmatter in `skills/engineering/errors/SKILL.md` | Write the `description` for the matcher, using phrases people actually type |
| **Framework** | The closest `frameworks/*` file | Cover only what the framework changes; keep the `Agent load` blockquote |
| **Review prompt** | The harness block in any `prompts/reviews/*` file | Default to `report-only` and always require a scope |
| **Scaffold prompt** | Any `prompts/scaffolds/*` file | Prefer extending an existing repo, and implement only what was asked |
| **Domain pack** | A new `prompts/domains/<name>/` folder | Open every file with the audit harness block |

List anything you add in that folder's README. An unlisted file never gets loaded.

---

## House rules

- **The pack is not a project.** No product code, runtime configs, secrets, session notes, or
  `AGENTS.md`. Those belong in the repo they describe.
- **One file per concept.** Cross-reference instead of duplicating; two copies of a rule
  become two different rules.
- **Universal files stay universal.** No product paths and no toolchains that exist on one
  machine only.
- **Domain packs describe a genre of work,** never one live server or one client.
- **Scaffolds and reviews stay separate.** "Build a bot" and "audit this tree" are different
  files.
- **Update in place.** No orphaned renames and no `-v2` files.
- **When a file is in doubt, delete it.**

---

<div align="center">
<sub>

MIT licensed. The clean-code standards are derived from Robert C. Martin's work, rewritten as
engineering rules with examples and review checklists.

</sub>
</div>
