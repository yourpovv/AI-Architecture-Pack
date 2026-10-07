# Universal Engineering Principles

> This is your tech-stack-agnostic handbook. It covers my Clean Code, the SOLID principles,
> Clean Architecture, DRY/KISS/YAGNI, testing, concurrency, security, and the habits
> that separate code you are proud of from code you regret. Drop it into any project you own.

You keep it short where your rule is obvious, longer where the nuance matters.
When two principles conflict, **clarity wins**.

### Mandatory lesson standards (authoritative for craft)

**Your day-to-day coding standards live in** [`Clean-Code/`](./Clean-Code/README.md) — **60 detailed
Uncle Bob / clean-code lessons** (side effects, naming, errors, comments, DRY, Demeter, CQS, …).

- For naming, functions, comments, null, exceptions, structure: open the matching
  `Clean-Code/` lesson file for your task (flat `NN-*.md` or one from the grouped folders). **That file wins** over anything below in this handbook.
- This `Principles.md` handbook covers **SOLID, architecture, testing, security,
  concurrency**, and philosophy. Where a section here restates your craft rules, it is a
  **summary only** — if the wording drifts, you fix this file toward `Clean-Code/`, not the reverse.
- Your skills (`Errors.md`, `NecessaryComments.md`, `Craft.md`) are subordinate the same way.

---

## Agent load policy (read this first)

This file is a **reference handbook**, not your default agent context.

- **Do not** load the whole document into your session by default. It is long on purpose.
- **Do** open the **one section** that matches your task (names, functions, errors, SOLID, testing, security, etc.).
- Prefer your project `AGENTS.md`, `standards/Clean-Code/` (one lesson), `skills/review/audit/SKILL.md`, and `skills/engineering/errors/SKILL.md` for your day-to-day work.
- The examples below use Java-like or web-flavored snippets as illustrations only. They are not your required stack. You translate the rule to the language in your current repo.
- Your project facts (owned code, secrets, verify commands) never live here. They live in your project's tracked agent contract and README.

### Section map (jump, do not stream all)

| Topic | Section |
|---|---|
| Philosophy, YAGNI, KISS | 0 |
| Naming | 1 |
| Functions | 2 |
| Comments | 3 |
| Formatting / objects | 4-5 |
| Error handling (deep) | 6 (also `skills/engineering/errors/SKILL.md`) |
| SOLID / architecture | 7-8 |
| DRY / boundaries | 9-10 |
| Git / review / refactor | 11-13 |
| Observability | 14 |
| Testing | search within file for testing sections |
| Security / concurrency | search within file; pair with `prompts/reviews/` or `prompts/domains/*` |

---

## 0. Philosophy (set the tone)

- **Write your code for the human reading it, not the machine executing it.** Your compiler
  does not care about your names, your whitespace, or your function length. You will care
  at 2 AM on a production incident.
- **Leave the campground cleaner than you found it.** (The Boy Scout Rule.) Every commit you make
  is your chance to nudge the codebase toward better.
- **You Aren't Gonna Need It (YAGNI).** Do not build for imagined requirements. Build
  for the requirement in front of you, and make it easy to change when the next one shows up.
- **Keep It Simple, Stupid (KISS).** Complexity is not an achievement. The hardest part
  of your job is finding the simplest solution that works.
- **Make it work, make it right, make it fast, in that order.** Premature optimization
  taxes your clarity. You measure, then you optimize.
- **Prefer boring.** Exotic techniques, clever tricks, and novel abstractions are
  liabilities in your code. Boring code is predictable, teachable, and debuggable.
- **Disagree and commit.** Teams ship. When your convention is set, you follow it even if you
  would have chosen differently.

---

## 1. Names

Your names are the first, cheapest, and most effective documentation you write.

### 1.1 Intention-revealing

`daysElapsed`, not `d`. `customerAccount`, not `acc`. If you need a comment to explain
your name, your name is wrong.

### 1.2 Avoid disinformation

Don't name something `accountList` unless it is literally a `List` in your code. Don't use names that
look alike to your reader (`XYZControllerForEfficientHandlingOfStrings` and
`XYZControllerForEfficientStorageOfStrings`).

### 1.3 Meaningful distinctions

`a1, a2, a3` tells your reader nothing. If two things have the same role in your code, unify them;
if they are different, you name the difference.

### 1.4 Pronounceable and searchable

`genymdhms` fails both tests for you. `generationTimestamp` passes. A single-letter variable is
fine as your loop counter; anywhere else it hides.

### 1.5 Conventions

- **Classes and types**: nouns. `Customer`, `ParserResult`, `EmailQueue`.
- **Functions and methods**: verbs. `postPayment()`, `deletePage()`, `save()`.
- **Booleans**: read like questions. `isActive`, `hasPermission`, `shouldRetry`.
- **Constants**: `SCREAMING_SNAKE_CASE`. Magic numbers become `MAX_RETRY_COUNT`.

### 1.6 Scope ↔ name length

Short scope, short name. Long scope, long name. A counter `i` in your 5-line loop is fine.
A global named `x` is malpractice. Ask yourself: how far must your reader carry this name?

### 1.7 No puns, no cuteness, no encodings

`HolyHandGrenade` does not tell your reader what it does. Hungarian notation (`sName`, `bIsActive`)
survived the 90s; let it rest. Don't prefix your interfaces with `I` unless your team standard
requires it, `Account` vs `AccountImpl` is usually enough.

### 1.8 Rename when you learn

The moment you understand something better than its name says, you rename it. Your modern
editors make rename-refactors safe and global. Why keep a lie?

---

## 2. Functions and Methods

### 2.1 Small

Your function should fit on your screen without scrolling. Under 20 lines is a good target for you;
under 10 is better. Blocks inside your `if`/`for`/`while` should usually be **one line**
(a call to a well-named function you trust).

### 2.2 Do one thing

Your function does one thing if you cannot extract another function from it with a name
other than a restatement of its implementation. If you can say "this function does
X, *and* then Y", it is doing two things. Listen. That *and* is your warning.

### 2.3 One level of abstraction per function

Mixing high-level policy and low-level string mashing in your same function is the
single most common source of unreadable code you will write. Read your function top-to-bottom: every
line should sit at the same conceptual altitude.

### 2.4 Few arguments

- **0 (niladic)**, best
- **1 (monadic)**, easy
- **2 (dyadic)**, ok
- **3 (triadic)**, suspicious; justify it
- **4+**, extract an object or split the function

### 2.5 No flag arguments

`render(true)` tells your reader nothing. You split it into `renderForSuite()` and
`renderForSingleTest()`. If your function behaves differently based on a flag, it is
doing two things (rule 2.2).

### 2.6 No side effects the name doesn't announce

`checkPassword(user, pw)` should not *also* log your user in. `getUser()` should not
*also* mutate your state. If your function does X and Y, you name it X-and-Y, or you split it.
Would you trust a name that hides half the work?

### 2.7 Command-query separation

Authoritative detail: [`Clean-Code/40-command-query-separation.md`](./Clean-Code/40-command-query-separation.md).

Your function either *does* something (command) or *answers* something (query), never both.
Your queries have no observable side effects. Your commands may return the artifact they created;
they must not smuggle a second “did it already exist?” question. Never name your writer `get*` / `check*`.

### 2.8 Don't return null, don't pass null

Authoritative detail: [`Clean-Code/13-stop-returning-null.md`](./Clean-Code/13-stop-returning-null.md).

**Never return null** from APIs you control. You return an empty collection, a Special Case /
Null Object, or you throw. You do not pass null — you reject it at the boundary. You do not hide your failures
as empty success (`catch { return [] }`).

### 2.9 Prefer exceptions to return codes

Authoritative detail: [`Clean-Code/03-exceptions-over-error-codes.md`](./Clean-Code/03-exceptions-over-error-codes.md),
[`34`](./Clean-Code/34-catch-is-not-if.md), [`37`](./Clean-Code/37-algorithm-breathes.md).

Your happy path is a flat list of steps. You throw on operational failure with context; you catch at
the boundary that can translate or report. You do not use catch as an ordinary branch.
You do not return status-code bags in languages that have exceptions.

### 2.10 Extract 'til you drop

Each helper you extract is your opportunity to give something a name. Your named behaviors
are the vocabulary of your codebase. Will your team thank you for that name?

---

## 3. Comments

Authoritative detail: [`Clean-Code/`](./Clean-Code/README.md) lessons **05–10, 17, 19, 33, 38, 41**.

> Your comments are a last resort. You prefer rename/extract. When you need one: why, warnings,
> public API docs, licenses — not narration or history museums.

### 3.1 Good comments (rare)

- **Legal.** Your copyright/license headers required by policy (Clean-Code 07, 41).
- **Intent.** *Why* you chose this approach when it is non-obvious to your reader (17).
- **Warnings / amplification.** Your load-bearing constraints others might “optimize” away (08).
- **Public API docs.** Your exported symbols: what, inputs, outputs, failures, example (41) — not noise (19).
- **TODO with context.** Your blocker or ticket, not `// TODO fix this` (08).

### 3.2 Bad comments (common)

- **Redundant**, `// increment i` before your `i++`.
- **Misleading**, your code and comment disagree because you updated one.
- **Mandated**, a comment you require on every getter adds noise to your code.
- **Journal**, "Changed Sep 3, then again Sep 4". That is what your version control is for.
- **Attributions/bylines**, `// added by Steve`. Your git blame knows.
- **Closing-brace labels**, `} // end if`. If you need this, your block is too long.
- **Commented-out code**, you delete it. Your version control remembers.
- **Non-local info**, you comment function A with policy that lives on function B.
- **Noise**, `// Default constructor.` above your default constructor.

### 3.3 When in doubt

If removing your comment would not confuse your future reader, you remove it. If it would,
you try a better name or an extracted function first to remove the need.

---

## 4. Formatting and Structure

### 4.1 Vertical density and openness

Lines that are conceptually related sit together in your file with no blank line between them.
Conceptually distinct blocks you separate by exactly one blank line. No double-blanks.

### 4.2 Vertical ordering (newspaper metaphor)

You write your source file like a newspaper: the headline (module intent) at
the top, the most important concepts near the top, details (helpers) flowing down.
Your reader should be able to stop at any point and still have context.

### 4.3 Declarations close to use

Your loop's counter belongs at the top of your loop. Your helper variable belongs just above
its first use. You do not hoist things to the top of your function for cosmetic symmetry.

### 4.4 Horizontal formatting

- Lines under ~100-120 columns in your code. You wrap long expressions; you use intermediate named variables.
- One statement per line in your code.
- Consistent whitespace around your operators and after your commas.
- You indent to show hierarchy; you never use indentation to fake alignment.

### 4.5 Team rules trump personal preference

You pick a formatter (Prettier, gofmt, rustfmt, Black, …) and a linter (ESLint, Clippy,
Ruff, …). You run them on commit. Your style debate is over; you get your time back.

### 4.6 File organization

- One public concept per your file, a class, a component, a module.
- Small helpers that exist only to support your public concept stay in the same file.
- Your file name matches the concept name.

---

## 5. Error Handling

### 5.1 Make errors a normal part of the design

Your errors are not the exception; your bugs are. You plan your error flow before your happy path.
What will you do when this fails?

### 5.2 Prefer exceptions, not return codes

Authoritative: [`Clean-Code/03`](./Clean-Code/03-exceptions-over-error-codes.md).

Return codes force every caller you write to remember to check. Exceptions keep your algorithm
readable. In languages without exceptions (e.g. Go), you use that language’s **single**
idiomatic error channel with context — still no nested status pyramids and no
TypeScript/Java-style `{ ok, error }` bags when exceptions exist.

### 5.3 Provide context

`throw new IOException("couldn't read")` is useless to your reader. You include *what* you were doing,
*which* resource you touched, *with what* inputs (minus secrets). Your stack traces alone are not enough.
(Also required by Clean-Code 03.)

### 5.4 Wrap third-party exceptions at boundaries

Authoritative: [`Clean-Code/31`](./Clean-Code/31-wrap-third-party-apis.md).

Your domain code should not leak vendor exceptions. You catch at the wrapper, you translate
into your domain’s error vocabulary, you re-throw.

### 5.5 Fail fast

You detect bad state at its source, not three layers deep. You validate your inputs at the entry
point. You never let a bad value quietly propagate through your system.

### 5.6 Don't swallow exceptions

Authoritative: [`Clean-Code/34`](./Clean-Code/34-catch-is-not-if.md).

Your empty `catch` is always wrong. Your catch that turns failure into fake success (`[]`,
default “ok”) is always wrong. Your best-effort work still logs with context and a short
why; usually you rethrow after translation. Your expected business branches use Special Case /
defaults — not try/catch.

### 5.7 One failure mechanism in exception languages

You use exceptions end-to-end inside your app; you map to HTTP/status once at the edge.
You do not mix exception throws with ad-hoc error-code returns in your same layer.

### 5.8 Treat internal errors and user errors differently

- **User errors** (bad input, not-found, permission denied) → you return a clear message, 4xx-class.
- **Internal errors** (broken invariant, network flake) → you return an opaque user message, 5xx-class,
  full detail in your logs. User-facing copy: `skills/engineering/errors/SKILL.md` Part B (subordinate to craft rules above).

### 5.9 Special-Case / Null-Object pattern

Authoritative: [`Clean-Code/13`](./Clean-Code/13-stop-returning-null.md), [`34`](./Clean-Code/34-catch-is-not-if.md).

Instead of null and guards everywhere in your code, you return a Special Case object with the same
interface, or an empty collection / zero. You throw when absence is a true failure.

---

## 6. Objects, Data, and Boundaries

### 6.1 Tell, don't ask

Don't fetch a field and compute on it externally in your code. You ask the object to do the work.
`bill.calculateTotal()` > `calculateTotal(bill.lineItems)`. Would you rather read the intention or the math?

### 6.2 Law of Demeter

A method `f` of class `C` should call only methods of:
- `C` itself,
- objects `C` creates,
- objects passed as arguments,
- objects held in `C`'s fields.

Not: `a.getB().getC().doSomething()` (a "train wreck" in your code). If you must, you make the whole
chain one method on the object that owns the knowledge.

### 6.3 Data objects vs behavior objects

Authoritative: [`Clean-Code/29`](./Clean-Code/29-objects-vs-data-structures.md), [`21`](./Clean-Code/21-expose-behavior-not-data.md).

- **Data objects (structs, DTOs)** — you expose fields, **no business behavior**. Correct
  and intentional at your boundaries (API responses, DB rows). Do **not** “fix” your DTO by
  stuffing domain rules into it.
- **Behavior objects** — you hide data, you expose operations. Your domain rules live here.
- **Hybrids** (public getters/setters for everything *and* business methods) lose both
  advantages for you — you split them.
- **Anemic domain types** (should own rules but only carry fields) are a smell in your code — you move
  behavior into your domain objects/services, not into DTOs.

### 6.4 Encapsulate at boundaries, not inside

Your internal code should pass rich objects freely. At your system boundary (HTTP,
DB, file), you serialize to data objects. You do not leak JSON or ORM entities into your
domain.

### 6.5 Boundaries around third-party code

You wrap external libraries in a thin adapter you control. You get:
- A single place to replace the library.
- A single place to handle its idiosyncrasies.
- A smaller API surface for you to learn and test.

### 6.6 Learning tests

Before you depend on a third-party API, you write tests that *prove your understanding*
of it. When the library upgrades, those tests tell you whether the upgrade broke
your assumptions. Cheap insurance for you.

---

## 7. Classes and Modules

### 7.1 Single Responsibility Principle (SRP)

> A class should have one reason to change.

If your `Report` handles formatting *and* persistence *and* scheduling, three stakeholders
will pull it in three directions. You split it. How many reasons would force you to touch this class?

### 7.2 Classes should be small

Measure by responsibilities, not lines. A 500-line class with one responsibility is
fine. A 50-line class that does three things isn't.

### 7.3 Cohesion

A class is cohesive when its fields and methods work on the same concept. When fields
split into groups used by different methods, that's two classes fighting for one name.

### 7.4 Organize for change

Classes isolate the parts that are likely to change. The parts that *won't* change
live in stable abstractions that everything depends on.

### 7.5 Open/Closed Principle (OCP)

> Modules should be open for extension, closed for modification.

You should be able to add new behavior by *writing new code*, not editing existing
code. Plugin architectures, strategy patterns, and polymorphism exist for this.

### 7.6 Liskov Substitution Principle (LSP)

> A subtype must be usable anywhere its supertype is used.

If `Square extends Rectangle` but `setWidth` on a Square silently also changes height,
you've broken LSP. Inheritance is a promise of interchangeability.

### 7.7 Interface Segregation Principle (ISP)

> Clients shouldn't depend on methods they don't use.

A fat interface forces implementations and callers to know about things they don't
care about. Split into small, role-specific interfaces.

### 7.8 Dependency Inversion Principle (DIP)

> Depend on abstractions, not concretions. High-level policy should not depend on
> low-level detail; both should depend on abstractions.

Your domain layer defines `PaymentGateway` (an interface); your infrastructure layer
implements `StripeGateway`. Nothing in the domain imports Stripe.

### 7.9 Composition over inheritance

Inheritance creates tight coupling across file boundaries and is hard to unwind.
Composition (holding a reference to a collaborator) gives you the same code reuse
with looser coupling. Use inheritance only for genuine "is-a" relationships with
behavioral substitutability.

### 7.10 Don't Repeat Yourself (DRY)

Two copies of the same logic is debt. Three is a bug waiting to happen. But: two
things that *look* identical today but represent different concepts are not
duplication, they're allowed to diverge later. Rule of three: extract after the
third occurrence if you're unsure.

---

## 8. Architecture, the big picture

### 8.1 Separate construction from use

Code that *wires* things together (dependency injection root, main, composition
root) should be separate from code that *uses* them. Your business logic should
never call `new` on its dependencies.

### 8.2 Clean Architecture / Hexagonal / Ports & Adapters

Layers from innermost to outermost:

1. **Entities**, enterprise-wide business rules. No framework imports.
2. **Use cases**, application-specific business rules. Orchestrate entities.
3. **Interface adapters**, controllers, gateways, presenters. Translate between
  use cases and frameworks.
4. **Frameworks and drivers**, web framework, DB, UI, devices.

**The Dependency Rule**: source code dependencies point *inward only*. Entities know
nothing about use cases; use cases know nothing about the web; nothing ever imports
the framework upward.

### 8.3 Package cohesion (Robert Martin)

- **REP**, Reuse/Release Equivalence: the unit of reuse is the unit of release.
- **CCP**, Common Closure: package things that change for the same reason.
- **CRP**, Common Reuse: package things that are used together; don't force users
  to depend on things they don't need.

### 8.4 Package coupling

- **ADP**, Acyclic Dependencies: no cycles in the package dependency graph. A depends
  on B depends on A means you can't change either without the other.
- **SDP**, Stable Dependencies: depend in the direction of stability.
- **SAP**, Stable Abstractions: stable packages should be abstract; volatile ones
  can be concrete.

### 8.5 Draw the architecture before you write it

Whiteboard the boundaries. Mark where requests enter, where data persists, where
external services are called, where the domain lives. If you can't draw it, you
haven't designed it.

### 8.6 Defer decisions

Architecture lets you postpone framework/DB/UI decisions. The longer you can
keep them out of the core, the more options you preserve. A good architecture
lets you swap MySQL for Postgres, React for Vue, REST for gRPC, with *minimal*
domain code change.

---

## 9. Testing

### 9.1 TDD's three laws

1. Don't write production code except to make a failing test pass.
2. Don't write more of a test than is sufficient to fail.
3. Don't write more production code than is sufficient to pass the current failing test.

Follow these strictly and you'll write testable code as a side effect.

### 9.2 F.I.R.S.T tests

- **Fast**, tests you don't run are tests that don't help you.
- **Independent**, tests don't depend on each other's order.
- **Repeatable**, same result on any machine, offline, any day.
- **Self-Validating**, green or red, no manual log inspection.
- **Timely**, written with, not after, the production code.

### 9.3 One logical assertion per test

You can have multiple `assert` calls if they verify the *same* concept. The instant
you're checking a *second* thing, split into a second test.

### 9.4 Build a testing DSL

Your tests should read like specifications. If you find yourself repeating setup,
extract helpers like `given.user.admin.withPlan("premium")`. Tests are code; they
deserve the same refactoring love.

### 9.5 Test at the right level

- **Unit**, one function/class, no I/O. Hundreds of these, milliseconds each.
- **Integration**, multiple components, real dependencies (DB, file, local process).
  Dozens of these.
- **E2E / Acceptance**, full system, real user path. A handful of these.

The **testing pyramid**: many unit, fewer integration, very few E2E.

### 9.6 Clean tests

Tests that are hard to read stay broken. Treat them as production code: small,
well-named, one concern at a time. A flaky test deletes trust in *all* tests.

### 9.7 Test behavior, not implementation

A test that breaks when you rename a private method is testing the wrong thing.
Test what the caller observes (inputs, outputs, side effects), not how you got there.

### 9.8 Property-based testing where it fits

For code with broad input domains (parsers, encoders, math), assert *properties*
(round-trip, commutativity, invariants) rather than hand-picked examples.

---

## 10. Concurrency

### 10.1 Default to not concurrent

Concurrency is a complexity cost. Introduce it only when you need throughput,
responsiveness, or parallelism you can't get otherwise.

### 10.2 Keep concurrent code behind a small API

The scary bits live in one place. Everything above that API is sequential reasoning.

### 10.3 Don't share mutable state across threads

Pick one:
- **Immutable data**, can't be corrupted.
- **Message passing**, each thread owns its state; threads communicate via queues.
- **Explicit synchronization**, locks, mutexes, atomics. Requires discipline and
  extensive testing.

In that order of preference.

### 10.4 Know your runtime's concurrency model

- JavaScript: single-threaded event loop + workers + async. Never block the loop.
- Java: OS threads + Virtual Threads (Loom), `synchronized`, `java.util.concurrent`.
- Go: goroutines + channels; `go vet -race` is mandatory.
- Rust: ownership prevents data races at compile time.
- Python: GIL limits true parallelism; use processes or async.
- C/C++: you're on your own; use proven libraries (TBB, Boost).

### 10.5 Test for concurrency bugs

Race detectors, stress tests, fuzz tests, and chaos tests catch what code review
can't. Schedule regular runs under load.

### 10.6 Lock scope ≪ function scope

Acquire late, release early. Never hold a lock across a network call, disk I/O,
or a callback you don't control.

---

## 11. Version Control (Git) Hygiene

### 11.1 Small, focused commits

Each commit is one coherent change. A bug fix and a feature don't share a commit.
A refactor and a behavior change don't share a commit.

### 11.2 Meaningful commit messages

- **Subject line** (≤72 chars): imperative mood, "Fix login redirect", not
  "Fixed" or "Fixes".
- **Body**: *why*, not *what* (the diff shows what). Link tickets.
- Consider **Conventional Commits** (`feat:`, `fix:`, `refactor:`, …) for changelogs
  and semantic release.

### 11.3 Branching

Short-lived branches. Rebase or merge frequently. A branch open for two weeks is a
merge conflict waiting to happen.

### 11.4 Never rewrite published history

You can amend and squash *before* pushing. After a branch is shared, rewriting its
history is a social bug. Force-push to `main` is a fireable offense.

### 11.5 Review before merging

Even if the author is you. `main` is sacred. PRs/MRs enforce pause-and-read.

### 11.6 Tag releases

`v1.2.3` tags make rollbacks trivial. Attach release notes. Semantic Versioning:
MAJOR breaks, MINOR adds backward-compatibly, PATCH fixes.

---

## 12. Code Review

### 12.1 Review for intent, then for correctness, then for style

A reviewer who leads with nits loses the plot. Start with: *does this solve the
right problem the right way?*

### 12.2 Critique the code, not the author

"This function has three responsibilities", good. "You always over-engineer", bad.

### 12.3 Explain why

"This isn't idiomatic" without a link is useless. "We prefer X because Y, see ADR-7"
is teaching.

### 12.4 Approve or block, don't drown in suggestions

A review with 40 nits and no verdict is a review that won't land. Either it ships
or it doesn't; say so.

### 12.5 Authors: make your reviewer's job easy

- PR description: what, why, how, how tested.
- Small PRs (<400 lines) get reviewed; 2000-line PRs get rubber-stamped.
- Respond to every comment (even with "done" or "disagree, because …").

---

## 13. Refactoring

### 13.1 Refactor in its own commit

Mixing refactor and behavior change makes both invisible to review. Ship the refactor
separately, prove nothing changed with tests, then add behavior.

### 13.2 The Mikado Method

When a refactor is too big to see the end, start at the goal, discover prerequisites,
revert, fix the prerequisites first. Iterate.

### 13.3 Seams

Legacy code is testable only where you can inject a fake. Build seams (interfaces,
DI points, parameter objects) at the boundaries, and the pit of spaghetti becomes
testable piece by piece.

### 13.4 Catalog of refactorings (Fowler)

Learn and name them:
- Extract Method / Inline Method
- Extract Class / Inline Class
- Rename Variable / Method / Class
- Introduce Parameter Object
- Replace Conditional with Polymorphism
- Replace Temp with Query
- Move Method / Move Field

Named refactorings become team vocabulary.

### 13.5 Don't refactor broken code

Green tests first. Refactor second. Otherwise you'll never know which change broke things.

---

## 14. Observability and Operability

### 14.1 Logs, metrics, traces, the three pillars

- **Logs**: what happened. Structured (JSON, not `printf`), with correlation IDs.
- **Metrics**: how much, how often. Histograms for latency, counters for events.
- **Traces**: how a request flows across services. OpenTelemetry if you can.

### 14.2 Log at boundaries

Entry, exit, and failure of every external call (DB, HTTP, queue). Never inside hot
loops.

### 14.3 Useful log lines

Include: timestamp, level, correlation/request id, user id (hashed if sensitive),
what was attempted, result. Never: secrets, PII beyond what you need, whole request
bodies.

### 14.4 Alerts that page are promises

Every page-able alert must be actionable. If the answer to "what do I do?" is
"nothing, it's flappy", delete the alert or fix the flap.

### 14.5 Graceful degradation

When a dependency fails, *degrade* rather than fail outright. Cache, default,
queue-for-later. Full-app outages are rarely necessary.

### 14.6 Know your SLIs / SLOs

Service Level Indicators (what you measure) and Objectives (targets) make
reliability a first-class engineering concern, not a vibe.

---

## 15. Security

### 15.1 Validate at trust boundaries

Any input crossing into your system (HTTP, CLI, file, queue) is hostile until proven
otherwise. Parse-don't-validate: turn raw input into a typed, constrained domain
value as early as possible, then trust it internally.

### 15.2 Principle of Least Privilege

Every process, service account, and user gets the minimum permissions to do their
job, and no more. Default deny.

### 15.3 Never log secrets

API keys, tokens, passwords, session IDs, full credit cards. Even in dev logs,
because dev logs become prod logs someday.

### 15.4 Defense in depth

Every layer assumes the previous one failed. WAF → auth → input validation → DB
parameterization → row-level security. One layer failing shouldn't be catastrophic.

### 15.5 Cryptography

- **Don't roll your own.** Use `libsodium`, `OpenSSL`, your platform's KMS.
- **Use passwords correctly:** Argon2id/bcrypt/scrypt, never MD5/SHA1/SHA256.
- **Rotate secrets** and have a story for "what if this leaks today".

### 15.6 Supply chain

Lockfiles (`package-lock.json`, `Cargo.lock`, `poetry.lock`) committed. Dependencies
scanned (Snyk, Dependabot, `npm audit`). Prefer small, vetted libraries over trendy
ones with 3 maintainers.

### 15.7 OWASP Top 10, memorize the current list

The most-exploited classes of web vulnerability, revised every few years. As of the
2021 edition:

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

Every web app gets audited against these. Re-check [owasp.org](https://owasp.org/Top10/)
each project, the list is renumbered and recategorized as threats shift.

---

## 16. Performance

### 16.1 Measure before optimizing

Profile. Benchmark. Without data you will optimize the wrong thing 90% of the time.

### 16.2 Big-O first, micro-optimizations last

An `O(n²)` loop in Python is worse than `O(n log n)` in JavaScript. Fix the
algorithm before you golf the allocations.

### 16.3 Latency vs throughput

Different optimizations. Latency-sensitive code (user-facing requests) fights for
the tail (p99). Throughput-sensitive code (batch) fights for average.

### 16.4 Caching is a promise, not a shortcut

Every cache introduces a consistency problem. Decide how stale is acceptable,
invalidate correctly, and know what happens if the cache disappears.

### 16.5 Avoid premature distribution

A single well-tuned process beats a sloppy cluster. Scale up before you scale out,
unless throughput demands otherwise. Distributed systems multiply failure modes.

---

## 17. Documentation

### 17.1 Code-adjacent > code-distant

- **README.md**: how to run, how to test, the one page someone needs to contribute.
- **CONTRIBUTING.md**: conventions, review process, release steps.
- **ADR (Architecture Decision Records)**: one short file per significant technical
  decision (context → decision → consequences). They age *with* the code.

### 17.2 Docstrings on public APIs

Every exported function/class: what it does, what it takes, what it returns, what
it throws, examples if non-obvious. IDEs surface these at the call site.

### 17.3 Examples > prose

A working 10-line example beats three paragraphs of description.

### 17.4 Don't document what the code already says

"Increments the counter" above `counter++` is noise. "Rate-limited to 100/min to
protect the downstream billing API" is signal.

### 17.5 Diagrams for architecture, not for getters

Sequence diagrams for request flows. Component diagrams for service boundaries.
Keep them in-repo (Mermaid, PlantUML) so they're versioned and discoverable.

---

## 18. The Four Rules of Simple Design (Kent Beck)

In priority order:

1. **Passes all tests**, behavior is correct.
2. **Reveals intent**, every name, every structure tells the reader what it's for.
3. **No duplication**, one concept, one place.
4. **Fewest elements**, the smallest number of classes, methods, modules that
  satisfy the first three.

When refactoring, optimize for these in order. Don't reduce classes at the cost
of intent.

---

## 19. Code Smells, A Checklist

When a reviewer (or you at 3 AM) goes "this feels wrong", it's usually one of these.

### Names

- **Vague** (`data`, `info`, `handler`, `manager`), what kind of data? manager of what?
- **Lies** (`list` that isn't a list, `validate` that mutates), the name misrepresents.
- **Inconsistent** (`fetchUser` / `getAccount` / `retrieveOrder`, pick one verb).

### Functions

- **Long**, screen-exceeding.
- **Too many arguments**, 4+.
- **Flag arguments**, boolean that switches behavior.
- **Side effects**, does something the name doesn't admit.
- **Deep nesting**, three+ levels of `if`/`for`. Extract.
- **Dead parameter**, never used.

### Classes

- **God class**, knows too much, does too much.
- **Feature envy**, a method that uses another class's fields more than its own.
- **Hybrid / anemic domain**, getters everywhere *plus* rules, or domain type with only fields when it should own behavior (DTOs at boundaries are fine — see 29).
- **Shotgun surgery**, one change requires editing 10 files. Poor cohesion.

### Comments

- **Redundant**, restates the code.
- **Commented-out code**, delete.
- **TODO without owner or date**, deadlines matter.

### Control flow

- **Duplicated logic in branches**, extract.
- **Switch on type**, polymorphism wants a word.
- **Magic numbers / strings**, extract named constants.
- **`null` in public APIs**, return Optional or Special Case.

### Coupling

- **Train wrecks** (`a.b().c().d()`), Demeter violation.
- **Global mutable state**, hidden coupling everywhere.
- **Cyclic dependencies** between packages/modules.

### Testing

- **No tests**, self-explanatory.
- **Tests that never fail**, tautological assertions.
- **Flaky tests**, delete or fix today, don't "skip".
- **Tests coupled to implementation**, break on rename.

---

## 20. Cultural Rules

### 20.1 Disagreement is a conversation, not a war

Two senior engineers will disagree. That's healthy. Use data, prototypes, ADRs to
converge. When consensus fails, a designated decider decides; everyone commits.

### 20.2 Blameless retrospectives

"How did our system let this happen?" beats "who caused this outage?" every time.
People ship incidents; systems allow them.

### 20.3 Teach as you go

A PR comment that teaches the whole team via a link to a principle is worth ten that
just fix one line.

### 20.4 Estimates are wrong

Treat them as ranges, not dates. The longer the task, the wider the range. Break down
until the range fits in a sprint.

### 20.5 Respect the on-call

Don't ship risky changes on Friday. Don't ship anything you haven't tested. Don't
deploy at 4:50 PM.

### 20.6 Rest

Tired engineers ship bugs. Rest is productivity. The hero who works weekends burns
out, and the team behind them deals with the debt.

---

## 21. Quick Reference (the fridge magnet)

| When you… | Ask yourself… |
|---|---|
| Name a thing | Would a new teammate understand it without context? |
| Write a function | Can I state what it does in one short sentence without "and"? |
| Add a comment | Could I fix the code so this comment wasn't needed? |
| Copy-paste | Is the third time coming? Extract. |
| Reach for inheritance | Would composition do? |
| Catch an exception | What am I going to do about it? |
| Return null | What Special Case could I return instead? |
| Share mutable state | Can I use a message or an immutable copy? |
| Add a parameter | Does this function now do two things? |
| Open a giant PR | Can I split this into a refactor + a behavior change? |
| Log something | Does this have a correlation ID? Is any of it a secret? |
| Deploy | Is it Friday 4:50 PM? |

---

## 22. Further Reading (one-line each)

- **Clean Code**, Robert C. Martin. The source text for most of this document.
- **Clean Architecture**, Robert C. Martin. Dependency rule + SOLID at the system level.
- **The Pragmatic Programmer**, Hunt & Thomas. DRY, orthogonality, tracer bullets.
- **Refactoring**, Martin Fowler. Named refactorings as a vocabulary.
- **Working Effectively with Legacy Code**, Michael Feathers. Seams; how to test untested code.
- **Domain-Driven Design**, Eric Evans. Bounded contexts, ubiquitous language.
- **A Philosophy of Software Design**, John Ousterhout. Deep modules, complexity.
- **Designing Data-Intensive Applications**, Martin Kleppmann. How distributed systems really work.
- **Accelerate**, Forsgren et al. The metrics that predict elite engineering teams.
- **The Mythical Man-Month**, Fred Brooks. Still correct 50 years later.

---

*This document is a guide, not a law. When clarity conflicts with a rule, clarity
wins. When productivity conflicts with a rule, ask whether the rule still earns its
keep for your context. Principles are tools; your judgment is the craftsman.*
