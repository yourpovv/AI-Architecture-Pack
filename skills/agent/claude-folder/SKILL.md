---
name: claude-folder
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

Listen. Here is what each part does for you, what you actually create, and the traps that waste your
afternoon. Harness details change between releases, so you treat this file as your map. You treat
the official docs as your authority on exact key names. That is the tradeoff you accept.

**Reference:** [code.claude.com/docs](https://code.claude.com/docs), or `/help` in the tool.

## The two-file core

Most projects you touch need exactly two files. Everything else is optional for you. Keep it that way
until you feel real pain.

| File | Tracked? | Role |
|---|---|---|
| `CLAUDE.md` | Yes | Project instructions every agent you run loads. Your rules live here |
| `CLAUDE.local.md` | No | Personal overrides for your machine. You gitignore it |

**You keep `CLAUDE.md` short.** Somewhere under 200 lines is a good ceiling for you. It loads
into every single session you run, so every line you add is rent you pay forever. You push depth
into linked files and reference them by path. Your agent will open what it needs. Short files respect
your team.

`CLAUDE.md` is only part of that rent you pay. Every installed skill's description, every
MCP server's tool schemas, and every hook's output ride along in your same
always-loaded block, billed on every call whether they fire or not.
[`../context-budget/SKILL.md`](../context-budget/SKILL.md) covers your whole floor
and how you measure it.

A common and good split for you: `AGENTS.md` at the root as the portable contract that any
harness reads, and `CLAUDE.md` for the parts specific to this tool. You cross-reference
rather than duplicating. If your two files drift, your agents get mixed orders.

## Directories under .claude/

| Path | What it is |
|---|---|
| `skills/` | Model-invokable. One folder per skill containing `SKILL.md`. Your Claude chooses them by matching your task against the `description`, so descriptions decide whether they fire |
| `agents/` | Sub-agent definitions, one markdown file each. Each runs in its own context window. You read `Sub-Agents.md` before wiring these up |
| `commands/` | Slash commands, one markdown file each. You invoke them, not your model. **Not legacy**, despite what some guides claim |
| `hooks/` | Where you keep hook scripts. Living here does **not** make them run for you (see below) |
| `rules/` | Additional rule files for you. Can be scoped to a glob so they load only for matching paths. **An unscoped rule file loads in every session you run** |
| `output-styles/` | Alternate response shapes, opt-in for you |
| `settings.json` | Tracked, shared config: permissions, env, model, statusline, and your hook registry |
| `settings.local.json` | Your machine only. You gitignore it |

At your repo root, `.mcp.json` declares MCP servers. Root only for you.

## The hook trap

**Dropping a script into your `.claude/hooks/` does nothing.** Your hooks fire only when
you register them in `settings.json` under the `hooks` key with an event and a matcher.
The directory is a convention for where you keep your scripts, not a trigger.

If your hook is not firing, you check registration before you debug your script. Registration is
the usual culprit. Do you want to waste an hour on code that never ran. Check first.

Hooks are the only mechanism that *enforces* anything for you. A rule you write in
`CLAUDE.md` is advisory. It holds while your agent remembers it. A hook is
mechanical and runs regardless. So you put taste and context in `CLAUDE.md`. You put
the one or two rules you actually cannot afford to have violated into a hook. That is professional
judgment.

Worth a hook for you: blocking edits that reintroduce a banned pattern, formatting on
write, refusing destructive shell commands, notifying you when your long run ends. You pick the
ones that protect your team.

## Gitignore

You ignore `.claude/settings.local.json` **in your repo's own `.gitignore`**, not just
your global one. A global ignore protects the machine it is on and nobody else on your team.
You check with `git check-ignore -v <path>`. It prints which ignore file matched, so
you can see whether your protection travels with your repo. Your teammates depend on that.

## Minimum viable setup

For a new project, you work in order. You start small and you earn each new file:

1. `CLAUDE.md` with your project's rules. Short.
2. `.gitignore` entry for `.claude/settings.local.json`.
3. `.claude/settings.json` only once you have a permission or hook worth sharing.

You stop there. You add `skills/`, `agents/`, `commands/`, or `output-styles/` when a real
need appears, not because the directory exists. Empty scaffolding is a cost with
no return for you, and a folder full of half-written skills makes your agent worse at
picking the right one. Discipline is leaving things out until you need them.
