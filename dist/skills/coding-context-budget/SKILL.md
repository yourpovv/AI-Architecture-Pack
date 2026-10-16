---
name: coding-context-budget
description: >
  Where an agent session's tokens actually go, and which levers move the number.
  Covers the startup floor (everything always-loaded is billed on every single
  call), prompt caching as a prefix match and what silently invalidates it, why
  switching models mid-session is the most expensive habit there is, and why
  output is the costliest token you can spend. Use when a session feels
  expensive, when usage limits keep getting hit, when cache hit rate is low, or
  when deciding what belongs in always-loaded context. Trigger on "reduce token
  usage", "why is this so expensive", "hitting my limits", "prompt caching",
  "cache hit rate", "context is full", "should I compact", "trim CLAUDE.md".
  Harness-agnostic.
---

# Context Budget

Most cost advice says to do less work. This file is about paying less for the same work.

Three levers move the number, roughly in order of impact:

1. **The startup floor.** Everything always loaded is billed on every call.
2. **The cache.** A cache read costs about a tenth of a fresh read, and small habits throw the
   cache away without any visible signal.
3. **Output.** The most expensive token, and it becomes input on every later turn.

## 1. The startup floor

Every request re-sends the whole conversation: the system prompt, `CLAUDE.md`, every installed
skill's description, every MCP server's tool schemas, and every hook's output. That block is
the floor. It costs the same on turn one and turn eighty.

Caching softens the floor but cannot remove it, since cache reads still cost something. The
only way to shrink it is to put less on it:

- Keep `CLAUDE.md` short and push depth into linked files the agent opens on demand. See
  [`../coding-claude-folder/SKILL.md`](../coding-claude-folder/SKILL.md).
- Uninstall skills and MCP servers you do not use. Each one ships its description into every
  request whether it fires or not.
- Check what hooks print. A chatty `SessionStart` hook is a permanent tax.

This is why the pack's core rule is to load one file at a time. A doc opened for one task is
paid for once. A doc in always-loaded context is paid for on every call.

## 2. The cache is a prefix match

**Changing any byte in the prefix invalidates everything after it.** That one fact explains
most surprising cache misses.

The prompt renders in a fixed order: tools, then system, then messages. Anything volatile
placed early invalidates everything downstream of it. Put stable content first and changing
content last.

| Operation | Cost, relative to an uncached read |
|---|---|
| Cache write, 5-minute TTL | 1.25x |
| Cache write, 1-hour TTL | 2x |
| Cache read | 0.1x |

A 5-minute cache pays for itself on the second request (1.25 + 0.1 against 2.0 uncached). The
1-hour TTL costs twice as much to write, so it needs a third request before it wins. Use it
for bursty traffic with long gaps, not by default.

### Not everything invalidates everything

There are three cache tiers, and a change invalidates only its own tier and the ones after it.

| What changed | Tools | System | Messages |
|---|---|---|---|
| Tool definitions added, removed, or reordered | lost | lost | lost |
| **Model switch** | lost | lost | lost |
| System prompt content | kept | lost | lost |
| `tool_choice`, images, thinking toggled | kept | kept | lost |
| Message content | kept | kept | lost |

Per-turn changes are cheap and structural changes are not. **Switching models mid-session is
the most expensive habit available,** because caches are model-scoped and a switch is a full
rebuild. If a cheap sub-task wants a cheap model, delegate it to a sub-agent and leave the
main loop on its model. See [`../coding-sub-agents/SKILL.md`](../coding-sub-agents/SKILL.md).

Editing `CLAUDE.md` mid-session is safe: it does not take effect until the session reloads.

### Silent invalidators

Nothing errors; the cache just never hits. Search the prompt-building path for:

- `datetime.now()`, `Date.now()`, or any timestamp in the system prompt
- UUIDs or request IDs generated per call and placed early
- JSON serialized without sorted keys, or anything iterating a set
- A user ID or session ID interpolated into the system prompt, which gives every user a
  private prefix nobody else can share
- Conditional system sections, where every flag combination is a separate prefix
- A tool list built per user, which sits at position zero and caches for nobody

The fix is always the same: make it deterministic, or move it after the last cache
breakpoint. A fact injected at turn five invalidates nothing before turn five.

### Two gotchas

**Minimum cacheable prefix.** Below a model-dependent threshold nothing caches, and nothing
says so. The threshold is not monotonic across model generations, so a prompt that caches on
one model may silently not cache on another. Check the current number for the model in use.

**20-block lookback.** A cache breakpoint searches back at most 20 content blocks for a prior
entry. Agentic loops exceed that easily, since every tool call adds two blocks. After a turn
with 15 tool calls, the previous breakpoint is out of reach and the next request starts cold.
Keep turns tight when the cache matters.

### Verify instead of assuming

The response's usage object is the source of truth:

- `cache_read_input_tokens`: served at 0.1x
- `cache_creation_input_tokens`: written at 1.25x or 2x
- `input_tokens`: **only the uncached remainder**, not the total

The total prompt size is all three added together. A long session reporting small
`input_tokens` has a working cache; it is not a small session.

If `cache_read_input_tokens` stays at zero across requests that should share a prefix, there is
a silent invalidator. Diff the rendered bytes of two consecutive requests to find it.

## 3. Output is the most expensive token

Output costs several times as much as input, and then it is re-read as input on every later
turn.

- **Keep evidence on disk, not in context.** Write the full log, test output, or diff to a file
  and read back the part that matters. A 60,000-token log pasted into the conversation is not a
  one-time cost.
- **Cap sub-agent reports.** An uncapped agent returns everything it saw, and the parent
  re-reads that report on every following turn. Ask for findings, not transcripts.
- **Do not paste whole files** when one function is needed.

## 4. Measure, do not guess

Everything above describes mechanisms, not predictions. What is expensive in a given project
is an empirical question.

**Count tokens per accepted result, not per response.** An optimization that halves token use
and doubles rework is not an optimization.

**Change one thing at a time.** Trimming `CLAUDE.md` and dropping three MCP servers in the same
session teaches you nothing about either.

[token-shield](https://github.com/khalilmaaouni/token-shield) is a Claude Code plugin that reads
real usage counters from local session transcripts and reports cache hit ratios, first-request
cost, and the share of output that came from sub-agents. It prints `NO DATA` instead of
guessing when it cannot measure something. It is the fastest way to find which lever is
costing the most.

---

## Drop this in your CLAUDE.md

```markdown
## Context budget

Do not switch models mid-session. A model switch discards the entire prompt cache
and re-bills the whole prefix. If cheap bulk work needs a cheap model, delegate it
to a sub-agent and leave this session where it is.

Keep evidence on disk and out of context. Write full logs, test output, and large
diffs to a file, then read back only the part that matters. Never paste a whole
file when a function will do.

Cap what sub-agents report. Ask for findings, not transcripts. Their output
becomes my input on every turn after this one.
```

## Caveat

People report large drops in usage after adopting a policy like this. The mechanism is real
but not magic: the saving comes from paying less for work you were doing anyway (a warm cache
instead of a cold one, bulk work on a cheap model, evidence on disk instead of in the
transcript). None of it makes a session that does more work cost less.
