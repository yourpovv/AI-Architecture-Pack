---
name: context-budget
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

Most advice about your agent cost tells you to do less work. Listen. This is about you paying less
for your same work. You keep your output. You cut your waste.

Three levers move your number, roughly in order of how much they matter to you:

1. **Your startup floor.** Everything you always load is billed on every single call you make.
2. **Your cache.** A cache read costs you about a tenth of a fresh read. Small habits
   throw it away without any visible signal to you.
3. **Your output.** The most expensive token you can spend, and it becomes your input on
   the next turn and every turn after that.

## 1. The startup floor

Every request you make re-sends your whole conversation. Your system prompt, your
`CLAUDE.md`, every installed skill's description, every MCP server's tool
schemas, every hook's output. That block is your floor. You pay it on your turn one
and your turn eighty alike. It never goes away on its own.

Caching softens your floor but cannot remove it, because you still pay for a cache read.
The only way you shrink a floor is to put less on it for your team:

- You keep `CLAUDE.md` short. You push depth into linked files your agent opens on demand.
  See [`../claude-folder/SKILL.md`](../claude-folder/SKILL.md).
- You uninstall skills and MCP servers you do not use. Every one of them ships a
  description into every request you make whether it fires or not.
- You check what your hooks print. A chatty `SessionStart` hook is a permanent tax you pay.

This is also why your pack's core rule exists. You load one file at a time. A doc your
agent opens for one task costs you once. A doc in your always-loaded context costs you forever.
Which one do you want for a file you rarely need. You know the answer.

## 2. The cache is a prefix match

**Any byte you change anywhere in your prefix invalidates everything after it for you.**
That single sentence explains almost every surprising cache miss you will see in your work.

Your prompt renders in a fixed order: **tools, then system, then messages**. So
anything volatile you place early poisons everything downstream of it for you. Put stable
things first. Put changing things last.

| Operation | Cost, relative to an uncached read |
|---|---|
| Cache write, 5-minute TTL | 1.25x |
| Cache write, 1-hour TTL | 2x |
| Cache read | 0.1x |

A 5-minute cache pays for itself on your second request (1.25 + 0.1 against 2.0
uncached). The 1-hour TTL costs you double to write, so it needs a third request
before it wins for you. You use it for gaps in your bursty traffic, not by default. That is the
honest tradeoff. You pay more up front to save later.

### Not everything invalidates everything

This is the part you get wrong. There are three cache tiers for you, and a change only
invalidates its own tier and below for you. Learn the tiers and you stop guessing.

| What changed | Tools | System | Messages |
|---|---|---|---|
| Tool definitions added, removed, or reordered | lost | lost | lost |
| **Model switch** | lost | lost | lost |
| System prompt content | kept | lost | lost |
| `tool_choice`, images, thinking toggled | kept | kept | lost |
| Message content | kept | kept | lost |

So per-turn changes are cheap for you and structural changes are not. **Switching models
mid-session is the single most expensive habit available to you**, because it is
a full rebuild with no escape hatch for you: caches are model-scoped. If a cheap sub-task
wants a cheap model, you delegate it to a sub-agent and leave your main loop where it
is. See [`../sub-agents/SKILL.md`](../sub-agents/SKILL.md). Your main loop stays put.

Editing your `CLAUDE.md` mid-session is safe for you, because it does not take effect until
your session reloads. You can fix it now and feel the gain on your next start.

### Silent invalidators

Nothing errors for you. Your cache just never hits. You grep your prompt-building path for these
silent killers:

- `datetime.now()`, `Date.now()`, or any timestamp in the system prompt
- UUIDs or request IDs generated per call and placed early
- JSON serialized without sorted keys, or anything iterating a set
- A user ID or session ID interpolated into the system prompt, which gives every
  user their own private prefix that nobody else can share
- Conditional system sections, where every flag combination is a separate prefix
- A tool list built per user, which lands at position zero and caches for nobody

The fix is the same in every case for you. You make it deterministic, or you move it after your
last cache breakpoint. A fact you inject at turn five invalidates nothing before
your turn five. Your past stays cached when you append at the end.

### Two gotchas worth knowing

**Your minimum cacheable prefix.** Below it, nothing caches for you and nothing tells you.
The threshold is model-dependent and it is **not monotonic across generations** for you,
so a prompt that caches on one model silently will not on another. You check the
current number for the model you are on rather than assuming. Trust the measurement, not your
memory.

**Your 20-block lookback.** A cache breakpoint searches backward at most 20
content blocks for a prior entry. Your agentic loops blow through that easily, since
every tool call you make adds two blocks. A turn with 15 tool calls has already pushed your
previous breakpoint out of reach, and your next request silently starts cold. You keep your turns
tight when you want your cache to hold.

### Verify instead of assuming

The response usage object tells you the truth about your session. You read it like a professional:

- `cache_read_input_tokens` you served at 0.1x
- `cache_creation_input_tokens` you wrote at 1.25x or 2x
- `input_tokens` **only your uncached remainder**, not your total

That last one trips you up. Your total prompt size is all three added together. A
long session reporting a small `input_tokens` is a session with a working cache for you,
not a small session. Do you see the difference. One is efficiency. The other is size.

If your `cache_read_input_tokens` is zero across repeated requests with what should be
an identical prefix, you have a silent invalidator. You diff the rendered bytes of
two consecutive requests and you will find it. Your eyes beat your guesses.

## 3. Output is the most expensive token

Your output costs several times what your input costs, and then it gets re-read as input on
every subsequent turn you run. You pay for it once at the high rate and then forever at
the low one. That is why you treat output as your most precious budget.

- **You keep evidence on disk, not in context.** You write the full log, the whole test
  output, the complete diff to a file and read back the part that matters. A
  60,000-token log you dump into your conversation is not a one-time cost.
- **You cap sub-agent reports.** An uncapped agent returns everything it saw, and you
  then re-read that report on every turn that follows. You ask for findings,
  not transcripts.
- **You do not paste whole files when you need a function.**

## 4. Measure, do not guess

Every number above is a mechanism, not a prediction. What is actually expensive
in your sessions is an empirical question, and the answer differs per project. You measure your
own work like a craftsman.

Two rules keep the measurement honest for you:

**Count tokens per accepted result, not per response.** An optimization that
halves token spend and doubles rework is not an optimization. Cheap output you
throw away costs more than expensive output you keep. Your team pays for results, not attempts.

**Change one thing at a time.** Trim `CLAUDE.md` and drop three MCP servers in
the same session and you have learned nothing about either. Professionals isolate their variables.

[token-shield](https://github.com/khalilmaaouni/token-shield) is a Claude Code
plugin that reads real usage counters out of your local session transcripts and
reports cache hit ratios, first-request cost, and how much of your output came
from sub-agents. It measures rather than estimates, and prints `NO DATA` instead
of guessing when it cannot measure something. It is the fastest way for you to find out
which of the three levers above is actually costing you. Use real numbers when you can.

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

## One honest caveat

People report large drops in usage after adopting a policy like this, and the
mechanism is real, but it is not magic. The saving comes from paying less for
work you were doing anyway: a warm cache instead of a cold one, bulk work routed
to a cheap model, evidence on disk instead of in the transcript. None of it makes
a session that does more work cost less. You still pay for what you ask your machine to do.
