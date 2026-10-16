# Universal Engineering Principles

> A stack-neutral handbook covering SOLID, Clean Architecture, YAGNI and KISS, testing,
> concurrency, security, performance, and team habits. It sits under the
> [`Clean-Code/`](./Clean-Code/README.md) lessons and agrees with every one of them.

## Relationship to the Clean-Code lessons

The 60 lessons in [`Clean-Code/`](./Clean-Code/README.md) are the mandatory coding standard.
This handbook adds the topics the lessons do not cover (architecture, concurrency, security,
operations, team practice) and summarizes the ones they do.

- Where a section here touches naming, functions, comments, errors, null, objects, classes,
  boundaries, or tests, it links the lesson that defines the rule. The lesson is the
  authority. This file only summarizes it.
- If a summary here ever drifts from its lesson, fix this file to match the lesson.
- The skills under `../skills/` (`errors`, `necessary-comments`, `craft`, `uncle-bob`) are
  subordinate in the same way.

## Agent load policy

This is a reference handbook, not default context.

- Do not load the whole file. Open the one section the task needs.
- For day-to-day work, the project `AGENTS.md`, one `Clean-Code/` lesson,
  `../skills/review/audit/SKILL.md`, and `../skills/engineering/errors/SKILL.md` come first.
- Examples use Java-like or web-flavored pseudocode. Translate them into the language of the
  repo you are in. The rule holds when the syntax changes.
- Project facts (owned code, secrets, verify commands) never live here. They belong in the
  project's own `AGENTS.md` and README.

### Section map

| Topic | Section |
|---|---|
| Philosophy, YAGNI, KISS, Boy Scout rule | 0 |
| Names | 1 |
| Functions | 2 |
| Comments | 3 |
| Formatting and file structure | 4 |
| Error handling | 5 (also `../skills/engineering/errors/SKILL.md`) |
| Objects, data, boundaries | 6 |
| Classes, modules, SOLID, DRY | 7 |
| Architecture | 8 |
| Testing | 9 |
| Concurrency | 10 |
| Git, code review, refactoring | 11 to 13 |
| Observability | 14 |
| Security | 15 |
| Performance | 16 |
| Documentation | 17 |
| Simple design, smells, culture, quick reference | 18 to 21 |

---

## 0. Philosophy

- **Write for the human reading the code.** The compiler ignores names, whitespace, and
  function length. The person debugging a production incident at 2 a.m. does not.
- **Leave the code cleaner than you found it, within the change's budget.** Improve what you
  touch. Do not rewrite unrelated modules in the middle of a feature; name that debt instead
  (Clean-Code 22).
- **YAGNI.** Build for the requirement in front of you, not an imagined one. When a real
  requirement arrives that the code cannot absorb, reshape first, then add the feature
  (Clean-Code `classes/05`).
- **KISS.** The hard part of the job is finding the simplest thing that works.
- **Make it work, make it right, make it fast, in that order.** A messy first draft is fine.
  Shipping it is not (Clean-Code 22). Optimize only what measurement points at (section 16).
- **Prefer boring code.** Clever abstractions become liabilities. Predictable code is easier
  to teach and debug.
- **Disagree and commit.** Once the team sets a convention, follow it even if you would have
  chosen differently.

---

## 1. Names

Names are the cheapest documentation in the codebase. Lessons: 04, 06, 20, 30, 36, 39,
`classes/01`, `function-design/02`, `function-design/03`.

### 1.1 Reveal intent (06, 20)

`daysElapsed`, not `d`. `customerAccount`, not `acc`. If a name needs a comment, rename it.
If you have to read the body to understand the name, the name failed.

### 1.2 No disinformation (36)

Call it `accountList` only if it is a list. Avoid names that differ by a few characters
(`XYZControllerForEfficientHandlingOfStrings` vs `XYZControllerForEfficientStorageOfStrings`)
and visually confusable characters. When the structure changes, rename in the same change.

### 1.3 Meaningful distinctions

`a1, a2, a3` say nothing. If two things play the same role, unify them. If they differ, name
the difference.

### 1.4 No mental mapping, pronounceable, searchable (04, 30, 39)

`genymdhms` fails. `generationTimestamp` passes. No private abbreviations (`tx`, `mgr`).
Acronyms the team already says as words (URL, ID, HTTP) are fine. Magic numbers become named
constants.

### 1.5 Conventions

- Types: nouns (`Customer`, `EmailQueue`).
- Functions: verbs or verb phrases (`postPayment`, `deletePage`).
- Booleans: read as questions (`isActive`, `hasPermission`).
- Casing follows the language and project convention. Do not import another ecosystem's style.
- No puns, no cute names, no type encodings (`sName`, `bIsActive`). Do not prefix interfaces
  with `I` unless the project already does.

### 1.6 Name length follows scope (30, `function-design/03`)

The rule differs for variables and functions:

- **Variables and constants:** the wider the scope, the longer and more specific the name. A
  loop counter `i` is fine in a three-line loop. A module-level `x` is not.
- **Functions:** a narrow, crowded private scope needs longer, distinguishing names
  (`importCsvRows`). A widely used public operation earns the shortest unambiguous verb
  (`parse`, `charge`). Judge a function name against its neighbours, not an absolute length.

### 1.7 Name the why, one level above the how (`function-design/02`)

Name a function after why a caller would call it, not after the comparison or loop inside it.
`isEligibleForRefund`, not `checkDaysLessThan30`.

### 1.8 An argued name means an unfinished design (`classes/01`)

If a class name needs "and", or falls back to `Manager`, `Processor`, or `Handler` to cover
two jobs, split the class until one noun phrase fits.

### 1.9 Rename when you learn

When you understand a thing better than its name says, rename it. Editors make the rename
safe.

---

## 2. Functions

Lessons: 01, 02, 15, 18, 23, 24, 26, 27, 28, 40, `classes/03`.

### 2.1 Size follows responsibility (15, 26, `classes/03`)

There is no line limit. A function is the right size when it does one thing at one level of
abstraction and reads as a short story. Length is a prompt to look for a second job or a
data seam, not a rule by itself.

When you split, split where the data stops being shared. Cutting through shared state to hit
a line count spreads one responsibility across two owners. Do not extract without a way to
verify behavior.

### 2.2 Do one thing (15)

A function does one thing when you cannot extract another function from it whose name is more
than a restatement of the code. If you could label sections inside it with comments, extract
those sections. If describing it needs "and", it does two things.

### 2.3 One level of abstraction (27)

Policy and bit-twiddling do not belong in the same function. Every line should sit at
roughly the same altitude. Push parsing, encoding, and I/O into lower helpers.

### 2.4 Few arguments (23, 28)

- 0 to 2 arguments: preferred.
- 3: needs a natural, obvious order.
- 4 or more: introduce a parameter object or options type with named fields.
- Two arguments that form one concept (a point, a range) become one value.

### 2.5 Argument roles, no flag arguments (02)

Each argument is data for a question, data for a transformation, or an event to handle. A
boolean that switches which algorithm runs (`render(user, true)`) is two functions in one:
split it. A boolean that is itself the data (`setVisible(true)`) is fine. Prefer return
values over output arguments.

### 2.6 No hidden side effects (01)

`checkPassword` must not start a session. `getUser` must not change state. When a function
needs both an answer and an effect, split it and compose at the call site. Renaming it to
`checkPasswordAndStartSession` is more honest but still two jobs. Split.

### 2.7 Command-query separation (40)

A function either does something or answers something, never both. Queries (`is`, `has`,
`can`, `get`, `list`, `find`) have no observable side effects. Commands may return the
artifact they created. They must not smuggle a second answer such as "did it already exist".

### 2.8 Stepdown order (18)

Put the highest-level function at the top of the file and each helper below its first caller,
so the file reads top-down.

### 2.9 Bury the switch (24)

Keep large `switch` or `if/else` chains on type out of high-level policy. Put them in one
place at the bottom (a lookup table, a factory, polymorphism) and never copy the same switch
into several files.

### 2.10 Errors and null

See section 5 and Clean-Code 03, 13, 34, 37.

---

## 3. Comments

Lessons: 05, 07, 08, 09, 10, 17, 19, 33, 38, 41. Skill: `../skills/engineering/necessary-comments/SKILL.md`.

The default is no comment. Before writing one, try a rename, an extracted variable, an
extracted function, or a named constant (33).

### 3.1 Comments worth keeping

- **Legal:** required license or copyright headers, using standard text (07, 41).
- **Why:** the reason behind a choice the code cannot express (17).
- **Warnings and amplification:** a load-bearing detail someone might "clean up" by mistake,
  or a consequence such as "slow" or "not thread-safe" (08).
- **Public API docs:** purpose, inputs, outputs, failures, and an example for exported
  symbols (41). These are not noise (19).
- **TODOs with a constraint:** name the external blocker or ticket, for example
  `TODO(vendor#123): remove when upstream fixes X` (08, 10).

### 3.2 Comments to remove

- Redundant comments that restate the next line (19).
- Misleading or stale comments that no longer match the code (05, 09).
- Comments that need their own comments, or describe another module's behavior from afar (09).
- Mumbled or essay-length comments, and HTML in source comments (10).
- Journal entries, author bylines, and commented-out code. Git keeps history (07).
- Closing-brace labels and section banners. Fix the structure instead (38).
- Mandated boilerplate on every getter (19).

### 3.3 When in doubt

If removing a comment would not confuse the next reader, remove it. If it would, try a better
name or an extraction first. When the code changes, update or delete the comment next to it
in the same change (05).

---

## 4. Formatting and File Structure

Lessons: 11, 18, 25, 35, 38.

### 4.1 Vertical density (35)

Lines that belong together have no blank lines between them. One blank line separates
distinct ideas.

### 4.2 Newspaper order (18)

The file's purpose and public entry points come first. Helpers follow, each below its first
caller, with related helpers grouped.

### 4.3 Declarations close to use (11)

Declare local variables in the smallest scope, at or just before first use. Group a type's or
module's fields in one place (usually the top). Helper *functions* follow the stepdown rule in
4.2, below their callers.

### 4.4 Horizontal formatting

- Keep lines within the project's configured width (commonly 100 to 120 columns). Break long
  expressions with a named intermediate value.
- One statement per line.
- Consistent spacing around operators and after commas.
- Indent to show hierarchy. Do not hand-align columns; the next edit breaks them.

### 4.5 Tools settle style (25, 35)

Use the project's formatter and linter and run them automatically. Style is not a review
topic. Turn on the strictest type checking the language supports.

### 4.6 File organization (38)

- One public idea per file, named after that idea.
- Small private helpers that serve only that idea stay in the same file.
- If a file needs banner comments to be navigable, split it.

---

## 5. Error Handling

Lessons: 03, 12, 13, 31, 34, 37. Skill: `../skills/engineering/errors/SKILL.md`.

### 5.1 Define the failure contract first (12)

Decide what a function can fail with, and translate lower-level failures into that contract
at the function that owns it, before writing the steps inside. Test the failure mode first
when practical.

### 5.2 Exceptions over error codes (03)

Return codes make every caller remember a check. Exceptions keep the happy path a flat list
of steps (37). Languages without exceptions use their one idiomatic error channel (Go's
`error`, Rust's `Result`) with context, and still avoid nested status pyramids. Languages with
exceptions do not use hand-rolled `{ ok, error }` result objects in domain code.

### 5.3 Context in every failure (03)

`throw new IOException("couldn't read")` is useless. Include the operation, the identifiers
or inputs involved (minus secrets), and the cause. A stack trace alone is not enough.

### 5.4 Wrap third-party failures (31)

Domain code never catches vendor exceptions. The wrapper for each external system catches
them and rethrows your own types.

### 5.5 Fail fast at the trust boundary (13)

Reject bad input and null where it enters the system, with a clear error. Do not let a bad
value travel three layers before it breaks something.

### 5.6 Catch is not if; never swallow (34)

- An empty catch is always wrong.
- A catch that turns failure into fake success (`return []`, default data, "ok") is always
  wrong.
- Best-effort work logs the failure with context and a one-line why-comment, or rethrows.
- Expected alternate paths (not found, empty, already done) are modeled in normal flow with
  defaults, Special Case objects, or explicit branches, not with throw and catch.

### 5.7 One failure mechanism, mapped once at the edge (03)

Use one failure mechanism end to end inside the application. Map it to HTTP status codes, exit
codes, or UI messages once, at the outermost boundary.

### 5.8 User errors and internal errors

- **User errors** (bad input, not found, permission denied): a clear message the user can act
  on, a 4xx-class response for APIs.
- **Internal errors** (broken invariant, dependency outage): a short, safe message for the
  user, a 5xx-class response, and full detail in the logs.
- User-facing copy follows the what / why / action rules in
  `../skills/engineering/errors/SKILL.md` Part B.

### 5.9 No null; Special Case for normal absence (13)

- Collections: return empty, never null.
- Numeric absence: the identity value (0) or a no-op.
- Missing optional collaborator: a Special Case or Null Object with the same interface.
- Lookups that may legitimately miss: a typed optional (`Optional`, `Option`, `T | undefined`)
  only when the type system forces every caller to handle it.
- Missing required data: throw with context.
- Never pass null into your own functions.

---

## 6. Objects, Data, and Boundaries

Lessons: 16, 21, 29, 31, 32, `boundaries/01`, `boundaries/02`, `function-design/01`.

### 6.1 Not everything is an object (16)

Use a plain function or module for stateless transforms. Use a class when it hides state and
offers behavior over time. Do not build hierarchies for one use site.

### 6.2 Tell, don't ask (21)

Ask the object for the outcome instead of pulling its fields out and computing outside:
`bill.total()` rather than summing `bill.lineItems` in the caller. Do not add getters just so
other modules can re-implement the object's rules.

### 6.3 Law of Demeter (32)

A method `f` of class `C` calls methods only on `C` itself, objects `C` creates, objects
passed to `f`, and objects held in `C`'s fields. Not `a.getB().getC().doSomething()`. Ask a
direct collaborator for the outcome you need. Do not "fix" a chain by wrapping it in a
`getBCPath()` method that still encodes it.

### 6.4 Objects or data structures, not hybrids (29)

- **Data structures and DTOs** expose fields and contain no business logic. They are correct
  at boundaries (API payloads, database rows).
- **Objects** hide data and expose meaningful operations. Domain rules live here.
- **Hybrids** (public fields or getters for everything plus business methods) lose the
  benefits of both. Split them.
- **Active records** handle persistence navigation only. Pricing and rules live in domain
  objects or services.

### 6.5 Translate at the border (32, `boundaries/02`)

Inside the system, pass domain types. At the edge (HTTP, database, files, engine events),
convert to and from plain data. Raw JSON and ORM entities do not travel into the domain.

### 6.6 Wrap third-party code (31, `boundaries/01`, `boundaries/02`)

Call each external system through one adapter you own, with an interface designed from your
callers' needs rather than the vendor's docs. You get one place to swap the vendor, one place
for its quirks, retries, timeouts, and error mapping, and a small surface to fake in tests.
Build against a fake until the real system exists.

### 6.7 Learning tests

Before depending on external code, write tests that prove what you believe about it. When the
library updates, those tests tell you whether your assumptions still hold.

### 6.8 Public is a promise (`function-design/01`)

Public members are the stable "what" that callers may depend on. Private members are the
volatile "how". Do not make a helper public for one caller's convenience; add a dedicated
public operation instead.

---

## 7. Classes, Modules, and SOLID

Lessons: `solid/01`, `solid/02`, `classes/01` to `classes/06`, 14.

### 7.1 Single Responsibility Principle (`solid/01`, `solid/02`)

A class has one job, and every method serves that job. A "reason to change" is an **actor**:
a group of people who can demand a change. If tax rules (finance) and email templates
(marketing) live in one class, a change for one actor risks breaking the other. Split them.
Code owned by the same actor stays together even when it covers several operations.

### 7.2 Size by responsibility, not lines (`classes/01`, `classes/03`)

A long class with one job is acceptable. A short class with three jobs is not. Signs of an
unfinished split: a name you have to argue about, methods that cluster around separate groups
of fields, or a name that needs "and".

### 7.3 Cohesion and hidden classes (`classes/03`)

A class is cohesive when its methods use most of its fields. When fields fall into groups used
by different methods, there are hidden classes inside. Extract by shared data, and leave the
original as a thin coordinator.

### 7.4 Feature envy (`classes/02`)

A method that mostly reads another object's data belongs on that object. Move it, then have
callers use the behavior (`invoice.totalDue()`).

### 7.5 Policy and detail (`classes/04`)

A module either declares the workflow and delegates every step, or implements one step's
detail. When a file changes for both policy and detail reasons, move the detail out.

### 7.6 Open/Closed Principle (`classes/06`)

Add new behavior with new code (a new strategy, handler, or subclass) rather than by editing
working code. When a real requirement does not fit, apply 7.9 first.

### 7.7 Liskov Substitution Principle

A subtype must work anywhere its supertype works. If `Square extends Rectangle` and `setWidth`
on a square silently changes its height, the hierarchy is wrong.

### 7.8 Interface Segregation Principle

Clients should not depend on methods they do not use. Split wide interfaces into small,
role-specific ones.

### 7.9 Prefactoring: refactor for real requirements (`classes/05`)

Leave working code alone until a real requirement arrives. If the requirement fits, extend
directly with a minimal diff. If it does not, make a behavior-preserving refactor first,
verify that nothing changed, then add the feature. No speculative generalization.

### 7.10 Do not over-engineer (`classes/06`)

Split a class only when the split pays for itself through an isolated test, removed
duplication, a findable name, or an extension point for new behavior. If none applies, keep
the code together. Every class is a cost.

### 7.11 Dependency Inversion Principle

High-level policy and low-level detail both depend on abstractions. The domain owns a
`PaymentGateway` interface. The infrastructure layer implements `StripeGateway`. Nothing in
the domain imports the vendor.

### 7.12 Composition over inheritance

Inheritance couples tightly and is hard to undo. Composition gives the same reuse with looser
coupling. Use inheritance only for a true "is-a" relationship with substitutable behavior.

### 7.13 DRY: one home for each piece of knowledge (14)

Each piece of knowledge (a rule, a limit, a URL, a timeout, a validation) has one
authoritative home. As soon as you would have to change the same knowledge in two places,
extract it. DRY is about knowledge, not text: two pieces of code that look alike but change
for different reasons (different actors, see 7.1) are not duplicates, and merging them
creates a wrong abstraction.

---

## 8. Architecture

### 8.1 Separate construction from use

Wiring code (`main`, the composition root, dependency injection setup) stays apart from code
that does the work. Business rules do not construct their own infrastructure.

### 8.2 Clean Architecture, Hexagonal, Ports and Adapters

Layers from innermost to outermost:

1. **Entities:** enterprise-wide business rules. No framework imports.
2. **Use cases:** application-specific rules that orchestrate entities.
3. **Interface adapters:** controllers, gateways, presenters that translate between use cases
   and frameworks.
4. **Frameworks and drivers:** web framework, database, UI, devices, game engine.

**The Dependency Rule:** source code dependencies point inward only. Entities know nothing of
use cases. Use cases know nothing of the web or the engine. To audit a codebase, find the
innermost policy and check whether its imports are policy or infrastructure. Look at
dependency direction, not folder names.

### 8.3 Package cohesion

- **REP (Reuse/Release Equivalence):** the unit of reuse is the unit of release.
- **CCP (Common Closure):** group things that change for the same reason.
- **CRP (Common Reuse):** group things that are used together. Do not force users to depend on
  things they do not need.

### 8.4 Package coupling

- **ADP (Acyclic Dependencies):** no cycles in the package graph.
- **SDP (Stable Dependencies):** depend in the direction of stability.
- **SAP (Stable Abstractions):** stable packages are abstract; volatile packages can be
  concrete.

### 8.5 Sketch before building

Before writing a non-trivial system, sketch where requests enter, where data lives, which
external systems are called, and where the domain sits. If you cannot sketch it, the design is
not ready.

### 8.6 Defer decisions

Good boundaries let you postpone the choice of framework, database, or UI. The less they leak
into the core, the cheaper it is to change them later.

---

## 9. Testing

Lessons: `unit-tests/01` to `unit-tests/06`.

### 9.1 The three laws of TDD (`unit-tests/01`)

1. Write no production code except to make a failing test pass.
2. Write no more of a test than is enough to fail (a compile failure counts).
3. Write no more production code than is enough to pass the current failing test.

Do not add branches, options, or generality that no failing test asked for. If the project has
no test runner, say so and state how the change was verified.

### 9.2 F.I.R.S.T. (`unit-tests/06`)

- **Fast:** milliseconds per unit test. Put network, disk, and sleeps behind fakes.
- **Independent:** each test builds its own world. No test depends on another's run.
- **Repeatable:** same result on any machine, offline, at any time, in any locale.
- **Self-validating:** pass or fail by assertion, never by reading logs.
- **Timely:** written just before the code that makes it pass.

### 9.3 One concept per test (`unit-tests/05`)

Name each test for the behavior it guards, not for the function under test. Several assertions
are fine when they prove one concept. A second concept gets a second test.

### 9.4 Build, act, assert (`unit-tests/04`)

State facts about the world in the setup, perform exactly one action, and assert one claim.
Move shared setup into builders or factories (`given.user.admin.withPlan("premium")`) so each
test reads as a short story.

### 9.5 Tests are production code (`unit-tests/02`)

Apply the same naming, extraction, and DRY standards to tests. A skipped or ignored test is not
a permanent resident: fix it or delete it deliberately. A test that cannot explain its own
failure is broken.

### 9.6 Tests make change safe (`unit-tests/03`)

Before refactoring or optimizing code you are afraid of, pin its current behavior with
characterization tests, then change it. Untested code gets tests, then cleanup, in that order.

### 9.7 Test behavior, not implementation (`unit-tests/03`)

Assert what callers can observe: inputs, outputs, and side effects. A test that breaks when a
private helper is renamed is testing the wrong thing.

### 9.8 Test at the right level

- **Unit:** one function or class, no real I/O. Many of these, each fast.
- **Integration:** several parts with real dependencies (database, file system, local
  process). Enough to prove the joints hold.
- **End-to-end:** a full user path. A few, because they are slow and brittle.

### 9.9 Property-based tests where they fit

For code with wide input spaces (parsers, encoders, math), state properties that always hold
(round-trip, invariants) instead of only hand-picked cases.

---

## 10. Concurrency

### 10.1 Default to sequential

Concurrency costs reasoning effort. Use it only when you need throughput, responsiveness, or
real parallelism.

### 10.2 Keep concurrent code behind a small API

Concentrate the hard parts in one small module so the rest of the code can stay sequential.

### 10.3 Do not share mutable state

In order of preference:

1. **Immutable data:** nothing to race on.
2. **Message passing:** each thread or task owns its data and communicates through queues or
   channels.
3. **Explicit synchronization:** locks, mutexes, atomics. Requires care and stress testing.

### 10.4 Know the runtime's model

- **JavaScript:** single-threaded event loop plus workers and async I/O. Never block the loop.
- **Java:** OS threads, virtual threads, `java.util.concurrent`.
- **Go:** goroutines and channels. Run tests with `-race`.
- **Rust:** ownership prevents data races at compile time.
- **Python:** the GIL limits CPU parallelism. Use processes or async.
- **C and C++:** use proven libraries rather than hand-rolled primitives.
- **Luau (Roblox):** cooperative scheduling with `task.spawn` and `task.defer`. Any yield can
  interleave other code, so re-check state after yielding.

### 10.5 Test for concurrency bugs

Use race detectors, stress tests, and fuzzing. Code review alone rarely finds races.

### 10.6 Hold locks briefly

Acquire late, release early. Never hold a lock across network calls, disk I/O, or calls into
code you do not own.

---

## 11. Version Control

### 11.1 Small, focused commits

One logical change per commit. Keep fixes, features, and refactors in separate commits.

### 11.2 Commit messages

- Subject line of 72 characters or fewer: `<type>: <imperative summary>`, for example
  `fix: stop login redirect loop`. Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`,
  `style` (see `../skills/agent/commits/SKILL.md`).
- Body: why the change was made, not what the diff already shows. Link the ticket.

### 11.3 Short-lived branches

Merge or rebase often. A branch left open for weeks turns into a painful merge.

### 11.4 Never rewrite published history

Amend and squash before pushing. Once a branch is shared, do not rewrite it. Never force-push
to `main`.

### 11.5 Review before merging

Every change to `main` goes through review, including your own.

### 11.6 Tag releases

Tag releases (`v1.2.3`) with release notes, following Semantic Versioning: MAJOR for breaking
changes, MINOR for backward-compatible additions, PATCH for fixes.

---

## 12. Code Review

The harness for every review is `../skills/review/audit/SKILL.md`.

### 12.1 Order: intent, correctness, then style

First ask whether the change solves the right problem in the right way. Style comes last, and
the formatter should already have settled it.

### 12.2 Critique the code, not the author

"This function has three jobs" is useful. "You always write bloated code" is not.

### 12.3 Explain why

Link the reason: a lesson number, an ADR, a measurement. "This reads oddly" teaches nothing.

### 12.4 Decide

End with a clear approve or block. Forty suggestions with no verdict do not help anyone ship.

### 12.5 Authors make review easy

- The PR description covers what, why, how, and how it was tested.
- Keep PRs small (under about 400 changed lines). Large PRs get skimmed.
- Respond to every comment, even with "done" or "not now, because ...".

---

## 13. Refactoring

### 13.1 Refactor in its own commit (`classes/05`)

Never mix cleanup with new behavior. Commit the behavior-preserving refactor, verify nothing
changed, then add the feature.

### 13.2 The Mikado Method

For a change too large to see through: try the goal, note what blocks it, revert, fix the
blockers first, and repeat.

### 13.3 Seams

Legacy code becomes testable at seams where you can substitute a fake: interfaces, injected
parameters, small parameter objects. Add seams at the edges and work inward.

### 13.4 Named refactorings

Use Fowler's names so the team shares a vocabulary: Extract Method, Inline Method, Extract
Class, Inline Class, Rename, Introduce Parameter Object, Replace Conditional with
Polymorphism, Replace Temp with Query, Move Method, Move Field.

### 13.5 Do not refactor broken code

Get to green first. Otherwise you cannot tell whether a refactoring step broke something.

---

## 14. Observability

### 14.1 Logs, metrics, traces

- **Logs:** what happened. Structured (for example JSON), with correlation IDs.
- **Metrics:** how much and how often. Histograms for latency, counters for events.
- **Traces:** how a request flows across services. OpenTelemetry where available.

### 14.2 Log at boundaries

Log entry, exit, and failure of external calls (database, HTTP, queues). Do not log inside hot
loops.

### 14.3 Useful log lines

Include timestamp, level, correlation or request ID, user ID (hashed if sensitive), the
operation attempted, and the result. Never log secrets, unnecessary PII, or full request
bodies.

### 14.4 Every page is a promise

An alert that wakes someone must require action. If the honest response is "nothing", fix or
remove the alert.

### 14.5 Degrade visibly, never silently (13, 34)

When a dependency fails, keep the rest of the system working, but make the failure visible:
log it with context, show the user an honest state ("showing results from 5 minutes ago",
"saving is unavailable, retrying"), and stop writes that could corrupt data. Never substitute
default or empty data that looks like a real result, and never persist a fallback over real
data.

### 14.6 SLIs and SLOs

Define Service Level Indicators (what you measure) and Objectives (the targets) so reliability
is a number, not a feeling.

---

## 15. Security

### 15.1 Validate at trust boundaries

Treat everything that enters the system (HTTP, CLI arguments, files, queues, client-to-server
remotes) as hostile until validated. Parse, don't just check: convert raw input into a typed,
constrained domain value as early as possible, then trust it inside. Client-side checks are
never the only validation.

### 15.2 Least privilege

Every process, service account, and user gets the minimum rights needed. Default to deny.

### 15.3 Never log secrets

API keys, tokens, passwords, session IDs, and card numbers never go into logs, including
development logs.

### 15.4 Defense in depth

Assume each layer can fail: edge filtering, authentication, authorization, input validation,
parameterized queries, row-level security.

### 15.5 Cryptography

- Never implement your own. Use libsodium, OpenSSL, or the platform KMS.
- Hash passwords with Argon2id, bcrypt, or scrypt. Never MD5, SHA-1, or plain SHA-256.
- Rotate secrets and have a plan for "this secret leaked today".

### 15.6 Supply chain

Commit lockfiles. Scan dependencies (Dependabot, `npm audit`, Snyk). Prefer small,
well-maintained packages over popular ones with a single maintainer.

### 15.7 OWASP Top 10

Check every web application against the current OWASP Top 10. The 2021 list:

1. Broken Access Control
2. Cryptographic Failures
3. Injection (including XSS)
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

The list changes every few years. Check [owasp.org/Top10](https://owasp.org/Top10/) at the
start of each project.

---

## 16. Performance

### 16.1 Measure before optimizing

Profile and benchmark first. Without numbers, optimization usually targets the wrong place.

### 16.2 Algorithms first, micro-optimizations last

An O(n²) loop costs more than any language difference. Fix the algorithm before shaving
constant factors.

### 16.3 Latency and throughput are different goals

User-facing code optimizes tail latency (p99). Batch code optimizes throughput.

### 16.4 A cache is a promise

Every cache brings a staleness contract. Decide how stale is acceptable, how invalidation
works, and what happens when the cache is down.

### 16.5 Avoid premature distribution

Scale up before scaling out. Distributed systems bring new failure modes; adopt them only when
load requires it.

---

## 17. Documentation

Lesson: 41. Prose rules: `../skills/writing/prose/SKILL.md`.

### 17.1 Keep docs next to the code

- **README.md:** how to run and test the project; the page a new teammate needs.
- **CONTRIBUTING.md:** conventions, review process, release steps.
- **ADRs (Architecture Decision Records):** one short record per significant decision
  (context, decision, consequences).

### 17.2 Document public APIs (41)

Every exported function or module states what it does, its inputs and outputs, how it fails,
and an example when usage is not obvious. Internal helpers rely on clear code instead.

### 17.3 Examples over prose

A ten-line runnable example beats three paragraphs of description.

### 17.4 Do not document what the code already says (19)

"Increments the counter" above `counter++` is noise. "Capped at 100/min to protect the billing
API" is information.

### 17.5 Diagrams for architecture

Draw request flows and service boundaries, not getters. Keep diagrams in the repo as text
(Mermaid, PlantUML) so they are versioned with the code.

---

## 18. The Four Rules of Simple Design (Kent Beck)

In priority order:

1. **Passes all the tests.**
2. **Reveals intent:** names and structure say what the code is for.
3. **No duplication:** each piece of knowledge has one home (Clean-Code 14).
4. **Fewest elements:** the smallest number of classes, functions, and modules that still
   satisfies the first three (Clean-Code `classes/06`).

Never trade away intent to reduce element count.

---

## 19. Code Smells Checklist

### Names

- **Vague:** `data`, `info`, `handler`, `manager`, `util` (20).
- **Lying:** a `list` that is a map, a `validate` that mutates (01, 36).
- **Inconsistent:** `fetchUser`, `getAccount`, `retrieveOrder` in one codebase. Pick one verb.

### Functions

- **Doing more than one thing**, or mixing abstraction levels (15, 27).
- **Four or more arguments** (23).
- **Flag arguments** that select behavior (02).
- **Hidden side effects** or mixed command and query (01, 40).
- **Deep nesting:** three or more levels of `if` or `for`. Extract or return early.
- **Unused parameters.** Remove them.

### Classes

- **God class:** knows and does too much (`solid/01`).
- **Feature envy:** uses another class's data more than its own (`classes/02`).
- **Hybrid object / anemic domain type:** public data plus business logic, or a domain type
  with only fields that should own its rules. DTOs at boundaries are fine (29).
- **Shotgun surgery:** one change touches ten files. Group what changes together.

### Comments

- **Redundant** or stale (05, 19).
- **Commented-out code** (07).
- **TODO without a named blocker or ticket** (08).

### Control flow

- **Duplicated logic** in branches or files (14).
- **Switch on type** repeated across files (24).
- **Magic numbers and strings** (30).
- **Null returned from APIs you own** (13).
- **Catch used as an if, or empty catch** (34).

### Coupling

- **Train wrecks:** `a.b().c().d()` (32).
- **Global mutable state.**
- **Cyclic dependencies** between modules or packages.
- **Vendor SDK imported outside its wrapper** (31).

### Testing

- **No tests** for code that is changing.
- **Tests that cannot fail.**
- **Flaky or skipped tests.** Fix or delete them (`unit-tests/02`).
- **Tests coupled to implementation details** (`unit-tests/03`).

---

## 20. Team Practices

### 20.1 Disagreement is a conversation

Resolve design disagreements with evidence, small experiments, and ADRs. When discussion
stalls, a named decision-maker decides and everyone commits.

### 20.2 Blameless retrospectives

Ask "how did our process let this through", not "who broke this". Fix the process.

### 20.3 Teach in review

A review comment that links the underlying rule teaches the whole team.

### 20.4 Estimates are ranges

Treat estimates as ranges, not promises. The bigger the work, the wider the range. Split work
until the range is acceptable.

### 20.5 Respect on-call

Do not deploy risky or untested changes late on a Friday or at the end of the day.

### 20.6 Rest

Tired engineers write bugs. Sustainable pace is part of the craft.

---

## 21. Quick Reference

| When you... | Ask |
|---|---|
| Name a thing | Would a new teammate understand it with no context? (06) |
| Write a function | Can you describe it in one line without "and"? (15) |
| Add a comment | Could a rename or extraction make it unnecessary? (33) |
| Copy and paste | Is this the same knowledge in a second place? Extract it now. (14) |
| Reach for inheritance | Would composition do? |
| Catch an exception | Are you translating, recovering, or reporting? Never just hiding it. (34) |
| Return null | Would an empty value, a Special Case, or a throw be clearer? (13) |
| Share mutable state | Could you pass a message or an immutable copy? |
| Add a parameter | Is the function now doing two things? (02, 23) |
| Split a class | Which payoff does it buy: test, dedup, name, or extension? (`classes/06`) |
| Open a large PR | Can it be split into a refactor and a behavior change? |
| Log something | Does it have a correlation ID? Is any of it secret? |
| Deploy | Is it late on a Friday? |

---

## 22. Further Reading

- **Clean Code**, Robert C. Martin. The source for most of the Clean-Code lessons.
- **Clean Architecture**, Robert C. Martin. The Dependency Rule and SOLID at system scale.
- **The Pragmatic Programmer**, Hunt and Thomas. DRY, orthogonality, tracer bullets.
- **Refactoring**, Martin Fowler. The catalog of named refactorings.
- **Working Effectively with Legacy Code**, Michael Feathers. Seams and testing untested code.
- **Domain-Driven Design**, Eric Evans. Bounded contexts and ubiquitous language.
- **A Philosophy of Software Design**, John Ousterhout. Deep modules and managing complexity.
- **Designing Data-Intensive Applications**, Martin Kleppmann. How distributed data systems
  behave in practice.
- **Accelerate**, Forsgren, Humble, and Kim. Metrics that predict high-performing teams.
- **The Mythical Man-Month**, Fred Brooks. Why adding people to a late project makes it later.

---

The Clean-Code lessons are mandatory. This handbook is guidance around them: when one of its
non-craft rules does not fit a situation, say which rule you are setting aside and why.
