<div align="center">

# Architecture Pack

**Engineering standards, agent skills, and task prompts for you. You are the one who builds with AI.**

It is portable. It is stack-agnostic. It is project-neutral. Take only what your code needs. Drop it into any repo you own.

<a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-2f363d?style=flat-square"></a>
<img alt="Stack agnostic" src="https://img.shields.io/badge/scope-stack--agnostic-2f363d?style=flat-square">
<img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2f363d?style=flat-square">
<img alt="Built for Claude Code" src="https://img.shields.io/badge/built_for-Claude_Code-2f363d?style=flat-square">

</div>

---

## TL;DR

1. You copy [`standards/Clean-Code/`](standards/Clean-Code/README.md) and one
   [`languages/*`](languages/README.md) file into your `docs/`.
2. You write a short `AGENTS.md` at the repo root pointing at them. List what the agent may
   edit and how you will verify its work.
3. Tell your agent to **load one file at a time**. Never hand it the whole folder.

Then you install the audit harness. Every review runs with an explicit scope. It stays
`report-only` until you say otherwise:

```bash
cp -r skills/review/audit .claude/skills/
```

[Project templates](#project-templates) gives you the exact file list per stack. What follows
tells you why it matters for your code.

---

## Why this exists

Listen. Two things go wrong when you build software with an agent.

**It has no standard to code against.** Every file invents its own conventions. By week
two your project has stopped being one codebase. Nothing looks broken, so nothing
gets fixed. And your code slowly turns unmaintainable in a way you cannot point at.

**It gets handed everything at once.** The whole repo. Every doc you own. Plus a
20-page style guide. The instructions that matter end up buried. And your context
window has no room left for your code.

This pack fixes both for you. Your standards are split one rule per file. Your agent opens the
single lesson your task needs instead of swallowing the folder. Every review prompt carries
its own scope and mode. So an audit cannot quietly turn into a rewrite. And nothing here is
tied to one project. You use the same pieces in every repo you own.

---

## What is inside

<table>
<thead>
<tr><th align="left">Layer</th><th align="left">What it gives you</th><th align="left">When to load it</th></tr>
</thead>
<tbody>
<tr>
  <td><a href="standards/README.md"><b><code>standards/</code></b></a></td>
  <td>60 clean-code lessons for you, one rule per file, plus a universal handbook on SOLID, architecture, testing, and security</td>
  <td>Every serious project you own</td>
</tr>
<tr>
  <td><a href="skills/README.md"><b><code>skills/</code></b></a></td>
  <td>Guidance that fires on its own for you. You get audit harness, error handling, comment discipline, prose rules, sub-agent routing, <code>.claude/</code> setup</td>
  <td>You install once. Then you leave it alone.</td>
</tr>
<tr>
  <td><a href="languages/README.md"><b><code>languages/</code></b></a></td>
  <td>You get structure, idioms, testing, and a ready-to-paste project prompt for TypeScript, Node/Bun, Go, Python, C++, and Luau</td>
  <td>Pick exactly one for your project</td>
</tr>
<tr>
  <td><a href="frameworks/README.md"><b><code>frameworks/</code></b></a></td>
  <td>You get framework conventions on top of your language: React + Tailwind, Tauri, Electron, Valkyrie</td>
  <td>When one applies to your code</td>
</tr>
<tr>
  <td><a href="prompts/README.md"><b><code>prompts/</code></b></a></td>
  <td>Paste-in tasks for you. You get reviews and audits, greenfield scaffolds, and workflow rules that stop your agent guessing</td>
  <td>One per task you run</td>
</tr>
<tr>
  <td><a href="design/README.md"><b><code>design/</code></b></a></td>
  <td>Aesthetic systems for you, plus vetted sources for components, icons, illustrations, and 3D assets</td>
  <td>Opt in only if your code needs it</td>
</tr>
<tr>
  <td><a href="STACK.md"><b><code>STACK.md</code></b></a></td>
  <td>A worked walkthrough for choosing your stack, plus the services and AI tooling worth reaching for</td>
  <td>When you start something new</td>
</tr>
</tbody>
</table>

---

## Quick start

### 1. Copy what the project actually needs

```
your-project/
├── AGENTS.md                        <- you write this, see step 2
└── docs/
    ├── standards/
    │   ├── Clean-Code/              <- the mandatory 60
    │   └── Principles.md
    ├── languages/TypeScript.md      <- exactly one
    └── frameworks/Tauri.md          <- optional
```

Keep the same relative layout. Your cross-references still resolve then.

### 2. Write a short `AGENTS.md` at the repo root

This is the step people skip. It decides whether any of the rest works for you.
It is the only file allowed to know about *your* project.

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

### 3. Say the rules once, at the start

> Read `AGENTS.md` first. Your coding standards live in `docs/standards/Clean-Code/`. Load only
> the lesson file that matches your task. For any review, read `docs/skills/review/audit/SKILL.md` and set
> scope and mode (`report-only` by default). Load one language or framework file, and one
> prompt. Do not load the whole `Clean-Code/` folder or all of `Principles.md` unless you are
> auditing against the full map.

---

## Project templates

Each row is a complete setup for you. You copy the files. Then you paste the prompt.

<table>
<thead>
<tr><th align="left">Building</th><th align="left">Copy into <code>docs/</code></th><th align="left">Then paste</th></tr>
</thead>
<tbody>
<tr>
  <td><b>Desktop app</b><br><sub>Tauri</sub></td>
  <td><code>standards/Clean-Code/</code><br><code>languages/TypeScript.md</code><br><code>frameworks/Tauri.md</code></td>
  <td><code>prompts/reviews/Tauri-QC.md</code> before you ship</td>
</tr>
<tr>
  <td><b>Desktop app</b><br><sub>Electron or Valkyrie</sub></td>
  <td><code>standards/Clean-Code/</code><br><code>languages/TypeScript.md</code><br><code>frameworks/Electron.md</code></td>
  <td><code>prompts/reviews/Code-Review.md</code></td>
</tr>
<tr>
  <td><b>Website or web app</b></td>
  <td><code>standards/Clean-Code/</code><br><code>languages/TypeScript.md</code><br><code>frameworks/React-Tailwind.md</code><br><code>skills/web/web-seo/SKILL.md</code></td>
  <td><code>prompts/scaffolds/Website.md</code><br><code>prompts/scaffolds/Website-Design.md</code></td>
</tr>
<tr>
  <td><b>Discord bot</b></td>
  <td><code>standards/Clean-Code/</code><br><code>languages/TypeScript.md</code></td>
  <td><code>prompts/scaffolds/Discord-Bot.md</code></td>
</tr>
<tr>
  <td><b>Backend service</b></td>
  <td><code>standards/Clean-Code/</code><br><code>languages/Go.md</code> or <code>Bun-Node.md</code></td>
  <td><code>prompts/reviews/Performance-Scalability-Review.md</code></td>
</tr>
<tr>
  <td><b>Roblox game</b></td>
  <td><code>standards/Clean-Code/</code><br><code>languages/Luau.md</code></td>
  <td><code>prompts/reviews/Code-Review.md</code></td>
</tr>
<tr>
  <td><b>CLI or library</b></td>
  <td><code>standards/Clean-Code/</code><br>one <code>languages/*</code> file</td>
  <td><code>prompts/reviews/PR-Review.md</code></td>
</tr>
</tbody>
</table>

Every one of them starts with `standards/Clean-Code/`. That is deliberate. Your language and
your framework change per project. Your definition of good code does not.

---

## The rule that makes this work

**You load one file at a time.**

A pack like this is worth nothing if your agent reads all of it. Context spent on 60 lessons
you are not applying is context it cannot spend on your code. A model given sixty rules
at once follows none of them well.

So every file here is built for you to open alone. The standards are one rule per file. Your
language guides open with an `Agent load` line naming which sections to read first. Your
prompts are self-contained tasks.

<details>
<summary><b>Default load, and what to add on demand</b></summary>

<br>

**Default load**

1. Your project `AGENTS.md`
2. Your relevant README or tracker
3. Your `skills/review/audit/SKILL.md` when you review, audit, or ship
4. **One** language or framework file for your code
5. **One** prompt matching your task

**On demand**

| Doc | When |
|---|---|
| `standards/Clean-Code/NN-*.md` | Your primary craft standards. One lesson, by topic |
| `standards/Clean-Code/README.md` | The full map, when you audit against every rule |
| `standards/Principles.md` | SOLID, testing, security, concurrency for your code. Craft defers to Clean-Code |
| `skills/engineering/errors/SKILL.md` | Failure handling and user-facing error copy for your code |
| `skills/engineering/uncle-bob/SKILL.md` | Structure, seams, professionalism for your code |
| `skills/engineering/craft/SKILL.md` | Naming, comments, structure for your code |
| `skills/engineering/necessary-comments/SKILL.md` | Deciding whether your comment earns its keep |
| `skills/writing/create-readme/SKILL.md` | Writing a README from your real tree |
| `skills/writing/prose/SKILL.md` | Any README, doc, PR body, or commit message for you. The prose rules the rest of the pack defers to |
| `skills/web/web-seo/SKILL.md` | Shipping your public site |
| `skills/agent/sub-agents/SKILL.md` | Delegating your work and picking model tiers |
| `skills/agent/context-budget/SKILL.md` | Your session feels expensive, or your usage limits keep getting hit |
| `skills/agent/commits/SKILL.md` | Your agent is about to commit, or your session has piled up changes |
| `skills/agent/claude-folder/SKILL.md` | Setting up your `.claude/`, or your hook that will not fire |
| `prompts/workflow/Before-Implementing.md` | Your agent is about to build on a guess |
| `prompts/reviews/PR-Review.md` | Your pre-merge go or no-go |
| `prompts/reviews/Docs-Review.md` | Your docs have drifted from your code, or read like nobody proofread them |
| `design/apple-design/SKILL.md` | Your explicit Apple aesthetic request |
| `STACK.md` | You have chosen no stack yet |

**Never default-load**

- The entire `standards/Clean-Code/` folder
- All of `standards/Principles.md`
- The entire `prompts/` tree
- `STACK.md` on your project that already chose its stack
- `design/apple-design/SKILL.md` for your non-Apple UI

</details>

<details>
<summary><b>Authority, for when two files disagree</b></summary>

<br>

1. Your project **`AGENTS.md`**, and only for an exception it names explicitly
2. **`standards/Clean-Code/`**, your craft source of truth
3. **`skills/engineering/uncle-bob/SKILL.md`**, your methodology
4. Your other `skills/*` and **`standards/Principles.md`**
Your agent hits contradictory advice. It needs a rule to follow. Otherwise it invents a
preference. You get a different answer every session.

</details>

---

## Prompts vs skills

You have two ways to deliver guidance. The difference is who decides when it fires for you.

|  | `prompts/` | `skills/` and `design/` |
|---|---|---|
| **How you use it** | You paste into chat, deliberately | You install once. It triggers itself for you |
| **Frontmatter** | Optional for you | Your `name` plus a `description` full of trigger phrases |
| **Best for** | One-off tasks with a clear start and end for you | Standing rules that should apply without you remembering |

Every review and audit prompt obeys [`skills/review/audit/SKILL.md`](skills/review/audit/SKILL.md) for you. It demands explicit scope. It stays
`report-only` by default. No silent full-repo rewrite. You verify with commands discovered from
your project, never invented.

### Installing the skills

Every skill is already a folder holding a `SKILL.md` for you, named the way Claude Code expects.
You copy the folder and you are done:

```bash
cp -r skills/review/audit .claude/skills/
```

Use `~/.claude/skills/` to install for every project on the machine. The category folders
(`agent/`, `engineering/`, `review/`, `web/`, `writing/`) exist for browsing this repo.
Claude Code reads a flat skills directory, so copy the individual skill folders rather than
the category. The full list and the trigger for each skill are in
[`skills/README.md`](skills/README.md).

Harness details move between releases. [`code.claude.com/docs`](https://code.claude.com/docs)
is the authority on exact paths, settings keys, and hook events. This pack tells you what to
put in them.

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
│   └── image-to-code/SKILL.md
│
├── languages/                      pick ONE per project
│   ├── README.md
│   ├── TypeScript.md
│   ├── Bun-Node.md
│   ├── Go.md
│   ├── Python.md
│   ├── Cpp.md
│   └── Luau.md
│
├── frameworks/                     pair with a language
│   ├── README.md
│   ├── React-Tailwind.md
│   ├── Tauri.md
│   ├── Electron.md
│   └── Valkyrie.md
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
    │   └── Tauri-QC.md
    └── scaffolds/                  greenfield builds
        ├── Discord-Bot.md
        ├── Website.md
        ├── Website-Design.md
        └── Readme-Voice.md
```

`prompts/domains/` is a documented extension point rather than a shipped folder. Create
`prompts/domains/<your-stack>/` when you need threat models that only apply to one platform.

</details>

<details>
<summary><b>Example prompts</b></summary>

<br>

**Stop the agent building on a guess**

```
Read prompts/workflow/Before-Implementing.md.
Then: <what you want built>.
```

**Production review**

```
Read skills/review/audit/SKILL.md and prompts/reviews/PR-Review.md.
Scope: <paths>. Mode: report-only.
```

**Website**

```
Read prompts/scaffolds/Website.md, languages/TypeScript.md,
and frameworks/React-Tailwind.md.
Build only the pages we discussed.
```

**Discord bot**

```
Read prompts/scaffolds/Discord-Bot.md and languages/TypeScript.md.
Build a bot that posts daily standup reminders.
```

**README from the real tree**

```
Read skills/writing/create-readme/SKILL.md, and prompts/scaffolds/Readme-Voice.md for voice.
Write README.md from the actual repo. No guessing.
```

**Docs pass**

```
Read skills/review/audit/SKILL.md and prompts/reviews/Docs-Review.md.
Scope: README.md and docs/**. Mode: report-only.
```

**Craft pass**

```
Read skills/engineering/craft/SKILL.md and skills/engineering/uncle-bob/SKILL.md.
Review naming, comments, and structure for maintainability.
```

</details>

---

## Extending the pack

Every folder has its own README with an "adding" section covering the required shape.
Short version:

| Adding a | Start from | Then |
|---|---|---|
| **Skill** | The frontmatter in `skills/engineering/errors/SKILL.md` | Write the `description` for the matcher, using phrases people actually type |
| **Language** | The closest `languages/*` file | Keep the section order and the `Agent load` blockquote |
| **Framework** | The closest `frameworks/*` file | Say which language file it assumes, and cover only what the framework changes |
| **Review prompt** | The harness block in any `prompts/reviews/*` file | Default to `report-only`, always require a scope |
| **Scaffold prompt** | Any `prompts/scaffolds/*` file | Extend an existing repo, implement only what was asked |
| **Domain pack** | A new `prompts/domains/<name>/` folder | Every file opens with the Audit harness block |

Whatever you add, list it in that folder's README. An unlisted file is a file nobody loads.

---

## House rules

These keep the pack from rotting into a junk drawer.

- **This is not a project.** No product code, no runtime configs, no secrets, no session
  notes, no `AGENTS.md`. Those belong in the repo they describe.
- **One file per concept.** Cross-reference instead of duplicating. Two copies of a rule
  become two different rules.
- **Universal files stay universal.** No product paths, no toolchains that only exist on
  one machine.
- **Domain packs describe a genre of work**, never one live server or one client.
- **Scaffolds and reviews stay separate.** "Build a bot" and "audit this tree" are not the
  same file.
- **Update in place.** No orphaned renames, no `-v2` files.
- **Delete when in doubt.**

---

<div align="center">
<sub>

MIT licensed. The clean-code standards are derived from Robert C. Martin's (Uncle Bob's) work,
rewritten as engineering rules with examples and review checklists.

</sub>
</div>
