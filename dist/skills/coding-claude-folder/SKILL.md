---
name: coding-claude-folder
description: >
  Use when setting up or changing a project's Claude Code configuration: what
  belongs in CLAUDE.md versus CLAUDE.local.md, what each directory under .claude/
  actually does, how hooks get registered, and what a minimal new project needs.
  Trigger on "set up .claude", "add a hook", "what goes in settings.json", "make a
  slash command", "add a project skill", "why isn't my hook firing", "CLAUDE.md vs
  CLAUDE.local.md", or scaffolding agent config for a new repo. Tooling reference,
  not a code standard.
---

# The .claude/ Folder

What each part does, what to actually create, and the traps that waste an afternoon. Harness
details change between releases, so treat this file as a map and the official docs as the
authority on exact key names.

**Reference:** [code.claude.com/docs](https://code.claude.com/docs), or `/help` in the tool.

## The two-file core

Most projects need exactly two files. Everything else is optional until a real need appears.

| File | Tracked? | Role |
|---|---|---|
| `CLAUDE.md` | Yes | Project instructions every session loads |
| `CLAUDE.local.md` | No | Personal overrides for one machine. Gitignore it |

**Keep `CLAUDE.md` short.** Under about 200 lines is a good ceiling. It loads into every
session, so every line is paid for on every call. Push depth into linked files and reference
them by path; the agent opens them when needed.

`CLAUDE.md` is only part of that always-loaded cost. Every installed skill's description, every
MCP server's tool schemas, and every hook's output ride in the same block, billed on every call
whether they fire or not. [`../coding-context-budget/SKILL.md`](../coding-context-budget/SKILL.md) covers the
whole floor and how to measure it.

A common split: `AGENTS.md` at the root as the portable contract any harness reads, and
`CLAUDE.md` for the parts specific to Claude Code. Cross-reference rather than duplicate; if
the two drift, agents get conflicting orders.

## Directories under .claude/

| Path | What it is |
|---|---|
| `skills/` | Model-invoked. One folder per skill containing `SKILL.md`. Claude matches the task against each `description`, so descriptions decide whether a skill fires |
| `agents/` | Sub-agent definitions, one markdown file each. Each runs in its own context window. Read [`../coding-sub-agents/SKILL.md`](../coding-sub-agents/SKILL.md) before wiring these up |
| `commands/` | Slash commands, one markdown file each. The user invokes them, not the model. Not legacy, despite what some guides claim |
| `hooks/` | A conventional place for hook scripts. Living here does **not** make them run (see below) |
| `rules/` | Additional rule files. Can be scoped to a glob so they load only for matching paths. **An unscoped rule file loads in every session** |
| `output-styles/` | Alternate response shapes, opt-in |
| `settings.json` | Tracked, shared config: permissions, env, model, statusline, and the hook registry |
| `settings.local.json` | One machine only. Gitignore it |

`.mcp.json` at the repo root declares MCP servers. It belongs at the root only.

## The hook trap

**A script in `.claude/hooks/` does nothing by itself.** Hooks fire only when registered in
`settings.json` under the `hooks` key with an event and a matcher. The directory is a
convention for storage, not a trigger. When a hook is not firing, check registration before
debugging the script.

Hooks are the only mechanism that *enforces* anything. A rule in `CLAUDE.md` is advisory and
holds only while the agent remembers it. A hook runs regardless. Put taste and context in
`CLAUDE.md`, and put the one or two rules you cannot afford to have broken into a hook.

Good hook candidates: blocking edits that reintroduce a banned pattern, formatting on write,
refusing destructive shell commands, and a notification when a long run ends.

## Gitignore

Ignore `.claude/settings.local.json` in the repo's own `.gitignore`, not only a global one. A
global ignore protects one machine and nobody else on the team. Check with
`git check-ignore -v <path>`, which prints the ignore file that matched, so you can see whether
the protection travels with the repo.

## Minimum viable setup

For a new project, in order:

1. `CLAUDE.md` with the project's rules. Short.
2. A `.gitignore` entry for `.claude/settings.local.json`.
3. `.claude/settings.json`, only once there is a permission or hook worth sharing.

Stop there. Add `skills/`, `agents/`, `commands/`, or `output-styles/` when a real need
appears. Empty scaffolding costs something and returns nothing, and a folder of half-written
skills makes the agent worse at picking the right one.
