---
name: coding-standards
description: >
  Coding standards from the Architecture Pack, built on Clean Code (Robert C. Martin).
  Apply whenever writing, editing, refactoring, or reviewing code in any language: naming,
  function size and arguments, side effects, command-query separation, error handling
  (exceptions over error codes, no null returns, no swallowed errors), comments, DRY and
  constants, classes and SRP, wrapping third-party APIs, Law of Demeter, tests (TDD,
  F.I.R.S.T.), and review/audit discipline. Use it for any code task even when the user
  never says "standards", "clean code", or "style": new features, bug fixes, scripts,
  Luau/Roblox, TypeScript, Node/Bun, Go, Python, C++. Also use for "review this", "audit",
  "clean this up", "refactor", "is this good code", "make this better", or "why is this bad".
---

# Coding Standards

These standards come from the Architecture Pack's 60 Clean-Code lessons, built on Robert C.
Martin's Clean Code. The goal is code the next person can read, change, and debug at 2 a.m. without
asking the author anything. Apply them by default. Don't announce them or lecture about them.
When a standard shaped a decision the user might question, cite the lesson number in one clause
(for example, "threw instead of returning nil, per 13").

## Authority

When sources disagree, the higher one wins:

1. An explicit exception named in the project's `AGENTS.md` / `CLAUDE.md`, for that repo only.
2. This file and `references/clean-code/` (the 60 lessons).
3. The `coding-errors`, `coding-necessary-comments`, and `coding-audit` skills, and
   `references/principles.md`.
4. Language and framework idiom. Idiom decides *syntax* (how to throw, how to type an
   optional). It never overrides *policy* (whether failures can be swallowed).

Existing code that breaks these rules is not license to copy it. Match its naming and
formatting conventions, and fix rule violations only inside the area you were asked to change
(see "Scope discipline").

## How to use this skill

- **Writing code:** apply the core rules below as you go. When a topic is genuinely in play
  (say, designing an error contract or splitting a class), open the one matching lesson in
  `references/clean-code/`. The map is `references/clean-code/README.md`. Open one file at a
  time, not the folder.
- **Reviewing code:** follow "Review mode" below, and read `../coding-audit/SKILL.md` for the full
  harness.
- **User-facing error text:** `../coding-errors/SKILL.md` Part B (what / why / action).
- **Should this comment exist?** `../coding-necessary-comments/SKILL.md`.
- **SOLID, architecture, concurrency, security, performance, observability:** open only the
  matching section of `references/principles.md` (grep for the `##` heading). It is long, and
  its craft sections summarize and link the lessons.

---

## Core rules

### Names (04, 06, 20, 30, 36, 39, function-design/02–03, classes/01)

- A name answers why the thing exists and how it's used. If you need a comment to explain a
  name, rename it.
- No private abbreviations (`tx`, `mgr`, `plr`, `cfg2`). Acronyms the team says as words
  (URL, ID, HTTP, API, UI) are fine.
- Name functions for the caller's intent, one level above the body: `isEligibleForRefund`,
  not `checkDateDiffLessThan30`.
- Scope sets length. Short single letters only in tiny loops and lambdas. Narrow private
  helpers get longer, more specific names. Widely used public operations get the shortest
  unambiguous verb.
- Names must not lie. Call it `List` only if it is one. Rename in the same change when the
  structure changes. Avoid near-duplicate names.
- `Manager`, `Processor`, `Handler`, `Util`, `data`, `process`, `handle` are signs of an unfinished
  design. If an honest name needs "and", split the thing.
- Replace magic numbers with named constants.

### Functions (15, 18, 23, 26, 27, 02, 28, 24, classes/03)

- No line-count rule. Length is a prompt to look for a second job or a data seam; split where
  the data stops being shared, never mid-shared-state.
- One thing, one abstraction level. If you could put section-header comments inside it,
  extract those sections. Orchestration stays high, mechanics go into helpers.
- Stepdown order: callers above callees, so the file reads top-down like a story.
- Arguments: 0–2 preferred, 3 needs a natural order, 4+ becomes an options/params object.
- No boolean flags that pick between two algorithms. `render(user, true)` becomes
  `renderUser` + `renderAdminTools`. A boolean that *is* the data (`setVisible(true)`) is fine.
- Return values, not output parameters.
- Big `switch`/`if` chains on a type go to the bottom of the stack (a lookup table,
  polymorphism, or one buried dispatcher), never copied across files.

### Side effects and command-query separation (01, 40)

- A function either does something or answers something, never both.
- `is*`, `has*`, `can*`, `get*`, `find*`, `check*`, `validate*` must not mutate anything,
  including fields, globals, sessions, files, or network state.
- Need the answer *and* the effect? Split them and compose at the call site.
- A factory returning what it created is a command, which is fine.

### Errors (03, 12, 31, 34, 37, plus `coding-errors`)

- Fail loudly with context: operation, identifiers, cause. A bare `throw Error()` /
  `error("failed")` is forbidden.
- Use the language's one idiomatic failure channel (see "Per-language mapping"). Don't
  hand-roll `{ ok, error }` / `{ success, data }` bags in languages that have exceptions.
- Decide the function's failure contract first. Translate lower-level failures into it once,
  at the boundary that owns the contract. Inside, the happy path is a flat list of steps with
  no status checks between them.
- Wrap each third-party system in one module you own. Vendor errors become your error types
  there, and domain code never imports the vendor SDK.
- Catch is not if. Expected alternate paths (not found, empty, already done) are normal flow,
  handled with a default, a Special Case object, or an explicit branch.
- **Never** use an empty catch. **Never** let a catch turn failure into fake success
  (`catch → return []`, `pcall` fail → default data). Best-effort work logs with context
  and carries a one-line why-comment, or it rethrows.
- Map failures to HTTP codes, UI messages, or exit codes once, at the outermost edge.

### Absence and null (13)

- Collections come back empty, never null/nil.
- Numeric absence returns its identity value (0) or a no-op.
- A missing collaborator becomes a Special Case object with the same interface.
- Missing *required* data is a failure, so throw with context.
- Lookups like `find*`/`try*` may return a typed optional (`T | undefined`, `T?`,
  `Optional[T]`, `std::optional`). The type checker must force callers to handle it, and the
  name must say it can miss. `get*` either returns the thing or throws.
- Don't pass null/nil into your own functions. Reject it at the trust boundary.
- Don't paper over a bad producer with more null checks downstream. Fix the producer.

### Comments (05, 07, 08, 09, 10, 17, 19, 33, 38, 41, plus `coding-necessary-comments`)

- The default is zero. Before writing a comment, try a rename, an extracted variable, an
  extracted function, or a named constant.
- Keep these comments:
  - why a line that looks wrong is right
  - a warning about a consequence (hot path, not thread-safe, slow)
  - a TODO that names its external blocker or ticket
  - a timing or algorithm diagram the code can't show
  - public API docs (purpose, inputs, outputs, failures, example)
  - required license headers
- Cut these comments: narration of the next line, section banners, closing-brace labels,
  commented-out code, author or date journals, and notes about another module's behavior.
- When code changes, update or delete the comment next to it in the same change. A stale
  comment is worse than none.

### Classes, modules, and objects (16, 21, 29, 32, solid/*, classes/*, function-design/01)

- A function or module beats a class unless there is real state and behavior over time.
- An object hides data and exposes behavior (`order.total()`). A data structure exposes
  fields and has no logic. Never build a hybrid.
- SRP is decided by **actor**: who can demand a change. Different actors mean different
  modules, even if the code looks cohesive. One actor means it stays together, even if it
  covers several operations.
- Split where the data stops being shared, not at a line count.
- Move feature envy: a method that mostly reads another object's data moves to that object.
- A module either declares the workflow (delegates every step) or implements one step. Never
  both.
- Law of Demeter: no `a.b().c().d()` chains through strangers. Ask a friend for the outcome.
- Keep helpers private by default. Public means "stable, callers may depend on this".

### DRY, tools, and formatting (14, 25, 35, 11)

- Every piece of knowledge has one home: timeouts, URLs, limits, item tables, validation
  rules. Two places that must change together get extracted to a third.
- DRY is about knowledge, not similar-looking code. Don't merge two things that only look
  alike and change for different reasons.
- Turn on the strictest type mode the language offers (`strict` TS, `--!strict` Luau,
  mypy/pyright strict). Don't cast to `any` to move faster.
- The project's formatter and linter own whitespace and style. Don't argue style.
- Declare locals at their first use, in the smallest scope. Group fields in one place.
- Use a blank line between ideas and keep related lines dense.

### Tests (unit-tests/01–06)

- When the project has a test runner, write the failing test first, then just enough code to
  pass it. Don't add speculative branches no test asked for.
- One concept per test, named for the behavior it guards (`rejects_negative_amount`, not
  `test_addCoins`). Several asserts are fine if they prove one idea.
- Arrange the world, act once, assert the claim. Shared setup goes into builders and
  factories, not copy-paste.
- F.I.R.S.T.: Fast, Independent, Repeatable (no real network, clock, or locale),
  Self-validating, Timely.
- Before refactoring code you're afraid of, pin its behavior with characterization tests.
- Tests get the same craft standard as production code. No permanently skipped tests.
- **No test runner** (common for Roblox scripts and one-off tools): say so plainly. State how
  the change was or should be verified (playtest steps, a manual script, a REPL check). Don't
  invent a toolchain.

### Scope discipline (22, classes/05, classes/06, and Clean Coder methodology)

- Don't speculatively generalize working code. Make room only for a real requirement: first a
  behavior-preserving reshape, then the feature.
- Split a class only when it pays for a test seam, deduplication, a findable name, or an
  extension point. Otherwise leave it together.
- The Boy Scout rule has a budget. Leave the code you touched cleaner. Don't rewrite
  unrelated modules mid-task. Name the debt you saw instead.
- Don't refactor without a way to verify behavior (tests, a verify command, or explicit manual
  checks). An oversized function you can't safely verify stays as named debt.
- Dependencies point inward: core policy doesn't import UI, frameworks, or I/O. Adapters sit
  at the edge.
- Validate untrusted input (network, client, user, file, remotes) at the boundary. Everything
  else trusts its types.
- "I don't know yet" beats a confident guess. Read the real call chain before calling
  something a bug.

---

## Per-language mapping

| Language | Failure channel | Absence | Notes |
|---|---|---|---|
| **Luau (Roblox)** | `error()` with a context message (operation, ids, cause), raised with `error(msg, 2)` where caller blame helps. `pcall`/`xpcall` only at boundaries: a RemoteEvent handler, a DataStore/HTTP wrapper, a top-level task/thread | `{}` for collections. `T?` only on `find`/`try` lookups under `--!strict`. `get` errors when the value is missing | `--!strict` at the top of every module. `local function` only, no globals and no `_G`/`shared` as state. Disconnect connections and clean up per-player state on leave. **Never** answer a failed DataStore load with default data. That overwrites the real save, which is data loss. Kick or retry instead. The server validates every remote argument (type, range, ownership) and rate-limits. Handle remote message types with a handler table, not `if action == ...` chains |
| **TypeScript / JS** | `throw` an `Error` subclass with `{ cause }` | `T \| undefined` only from `find*` under `strict`. Empty arrays, never `null` collections | `strict: true`. No `any`. One API client module per external service |
| **Node / Bun services** | Throw domain errors, then map them to HTTP status in one middleware | As TS | Repositories: `findById` → `User \| undefined`, `getById` → throws `UserNotFound` |
| **Python** | `raise` a domain exception `from` the cause | `Optional[T]` only for `find_*` under mypy/pyright strict. Never `return None` to signal failure | Type-hint public functions |
| **Go** | `error` as the last return, wrapped with `fmt.Errorf("op %d: %w", id, err)` | Zero value plus a non-nil error on failure. Never a half-built value with `nil` error | Keep the happy path un-nested with early returns |
| **C++** | Exceptions, or `std::expected` if the project already uses it. Pick one per layer | `std::optional` for absence | RAII for every resource. No raw owning pointers |
| **Rust** | `Result<T, E>` with context (`thiserror` / `anyhow`) | `Option<T>` | Same flat-happy-path bar |

---

## Review mode

Use this whenever asked to review, audit, check, or critique code. Full harness:
`../coding-audit/SKILL.md`.

1. **Scope is required.** It might be paths, a diff, or a PR. If the user gave none and it
   can't be inferred from context (for example, "review this file" with a file open), ask.
2. **The mode is `report-only` unless the user asks for fixes.** "Review", "audit", and
   "check" never imply editing.
3. **Order:** security and correctness first, then architecture, then craft. A clean
   abstraction on top of a hole is still a hole.
4. **Each finding includes** its location, the trigger (exact scenario), the effect, a
   severity (`blocker` / `high` / `medium` / `low`), evidence (what you opened and traced),
   and a concrete fix. Cite the lesson number when one applies.
5. **Untraced paths are labeled `unverified`, not safe.** Never claim coverage you didn't
   read.
6. **End with** what was covered, what was skipped and why, findings by severity, the
   verification you ran (or "none"), and a go/no-go.

Don't pad a review with style nits the formatter would catch. Don't flag idiomatic framework
names as violations. Follow the full error path (a logger or sink upstream may already surface
it) before calling a catch "swallowed".

