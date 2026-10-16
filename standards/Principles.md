# Universal Engineering Principles

> This is your handbook for any stack. It covers my Clean Code, the SOLID principles,
> Clean Architecture, DRY/KISS/YAGNI, testing, concurrency, security, and the habits
> that separate code you sign with pride from code you regret. You can carry it into any project you own. You will need it there.

You keep your rule short when the point is plain. You write longer when your reader needs the nuance.
When two principles fight, **clarity wins**. You pick the reading your teammate will grasp on first pass. What good is a rule your reader cannot use.

### Mandatory lesson standards (authoritative for craft)

**Your day-to-day coding standards live in** [`Clean-Code/`](./Clean-Code/README.md). That is **60 detailed
Uncle Bob / clean-code lessons** (side effects, naming, errors, comments, DRY, Demeter, CQS, …). You answer to them every day you write code. They are not advice. They are your standard.

- For naming, functions, comments, null, exceptions, structure: open the matching
  `Clean-Code/` lesson file for your task (flat `NN-*.md` or one from the grouped folders). **That file wins** over anything below in this handbook. You obey it. No debate.
- This `Principles.md` handbook covers **SOLID, architecture, testing, security,
  concurrency**, and philosophy. Where a section here restates your craft rules, it is a
  **summary only**. If the wording drifts, you fix this file toward `Clean-Code/`, not the reverse. You never bend `Clean-Code/` to fit this handbook. The rule outranks the summary. Always.
- Your skills (`Errors.md`, `NecessaryComments.md`, `Craft.md`) are subordinate the same way. You hold them below your craft rules. They do not overrule your lessons.

---

## Agent load policy (read this first)

This file is a **reference handbook**, not your default agent context. You leave it on your shelf until you need it. Why carry the whole book when you need one page.

- **Do not** load the whole document into your session by default. It runs long on purpose. You would burn attention you need for your code.
- **Do** open the **one section** that matches your task (names, functions, errors, SOLID, testing, security, etc.). You move faster when you read only what your task demands.
- Trust your project `AGENTS.md`, `standards/Clean-Code/` (one lesson), `skills/review/audit/SKILL.md`, and `skills/engineering/errors/SKILL.md` first for your day-to-day work. You trust them first because they speak to your repo.
- The examples below use Java-like or web-flavored snippets as illustrations only. They are not your required stack. You map the rule onto the language in your current repo. The rule holds even when your syntax changes.
- Your project facts (owned code, secrets, verify commands) never live here. They live in your project's tracked agent contract and README. You keep this handbook free of your private details. That separation keeps you honest.

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
| Testing | search this file for the testing part your task needs |
| Security / concurrency | search this file for your task. Pair it with `prompts/reviews/` or `prompts/domains/*` |

---

## 0. Philosophy (set the tone)

- **Write your code for the human reading it, not the machine executing it.** Your compiler
  does not care about your names. It does not care about your whitespace. It does not care about your function length. You will care
  at 2 AM on a production incident. Your reader pays for every shortcut you take. Who do you write for. The man who comes after you.
- **Leave the campground cleaner than you found it.** (The Boy Scout Rule.) Every commit you make
  is your chance to leave the code a little better than you found it. That is how a craftsman works.
- **You Aren't Gonna Need It (YAGNI).** Do not build for imagined requirements. Build
  for the requirement in front of you. Make it easy to change when the next one shows up. Can you predict the future. No. So keep your code ready to move.
- **Keep It Simple, Stupid (KISS).** Complexity is not an achievement. The hard part
  of your job is finding the simplest thing that works. Simple takes discipline.
- **Make it work, make it right, make it fast, in that order.** Early speed tricks
  tax your clarity. You measure first. Then you optimize what the numbers point to.
- **Prefer boring.** Fancy tricks and clever abstractions turn into
  liabilities in your code. Boring code is predictable. It is teachable. It is debuggable. You want boring when you are tired.
- **Disagree and commit.** Teams ship. When your convention is set, you follow it even if you
  would have picked differently. Your pride does not outrank the team.

---

## 1. Names

Your names are the first documentation you write. They are the cheapest. They are the most effective. Treat them that way. Would you make your reader guess. No.

### 1.1 Intention-revealing

`daysElapsed`, not `d`. `customerAccount`, not `acc`. If you need a comment to explain
your name, your name has failed you. Fix the name.

### 1.2 Avoid disinformation

Never call it `accountList` unless it is a `List` in your code. You lie to your reader when you do. Do not use names that
look alike to your reader (`XYZControllerForEfficientHandlingOfStrings` and
`XYZControllerForEfficientStorageOfStrings`). How long before you mix them up.

### 1.3 Meaningful distinctions

`a1, a2, a3` tells your reader nothing. If two things play the same role in your code, unify them.
If they differ, you name the difference. That is your job.

### 1.4 Pronounceable and searchable

`genymdhms` fails both tests for you. `generationTimestamp` passes. A single letter is
fine as your loop counter. Anywhere else it hides. Why make your reader decode.

### 1.5 Conventions

- **Classes and types**: nouns. `Customer`, `ParserResult`, `EmailQueue`. A class is a thing. Name the thing.
- **Functions and methods**: verbs. `postPayment()`, `deletePage()`, `save()`. A function does work. Name the work.
- **Booleans**: read like questions. `isActive`, `hasPermission`, `shouldRetry`. Your reader should hear the question.
- **Constants**: `SCREAMING_SNAKE_CASE`. Magic numbers become `MAX_RETRY_COUNT`. Give the number a name your reader can trust.

### 1.6 Scope ↔ name length

Short scope, short name. Long scope, long name. A counter `i` in your 5-line loop is fine.
A global named `x` is malpractice. Ask yourself this. How far must your reader carry this name.

### 1.7 No puns, no cuteness, no encodings

`HolyHandGrenade` does not tell your reader what it does. Hungarian notation (`sName`, `bIsActive`)
stayed in the 90s. Let it rest there. Do not prefix your interfaces with `I` unless your team standard
requires it. `Account` vs `AccountImpl` is usually enough.

### 1.8 Rename when you learn

The moment you understand a thing better than its name says, you rename it. Your modern
editors make rename refactors safe and global. Why keep a lie in your code.

---

## 2. Functions and Methods

### 2.1 Small

Your function should fit on your screen without scrolling. Under 20 lines is a good target for you. Under 10 is better. Blocks inside your `if`/`for`/`while` should usually be **one line**.
That line is a call to a well named function you trust. Small is professional.

### 2.2 Do one thing

Your function does one thing if you cannot pull another function out of it with a name
that is more than a restatement of its code. If you catch yourself saying this function does
X, *and* then Y, it does two things. Listen. That *and* is your warning.

### 2.3 One level of abstraction per function

Mixing high level policy and low level string work in your same function is the
most common way you will write unreadable code. Read your function top to bottom. Every
line should sit at the same height.

### 2.4 Few arguments

- **0 (niladic)**, best. You ask nothing. You carry nothing.
- **1 (monadic)**, easy. One idea in. One job done.
- **2 (dyadic)**, ok. Two is honest work.
- **3 (triadic)**, suspicious. You justify it.
- **4+**, extract an object or split the function. Four means you hid a structure.

### 2.5 No flag arguments

`render(true)` tells your reader nothing. You split it into `renderForSuite()` and
`renderForSingleTest()`. If your function acts one way on true and another way on false, it
does two things (rule 2.2). Would you accept that in your own code.

### 2.6 No side effects the name doesn't announce

`checkPassword(user, pw)` should not *also* log your user in. `getUser()` should not
*also* change your state. If your function does X and Y, you name it X and Y, or you split it.
Would you trust a name that hides half the work.

### 2.7 Command-query separation

Authoritative detail: [`Clean-Code/40-command-query-separation.md`](./Clean-Code/40-command-query-separation.md).

Your function either *does* something (command) or *answers* something (query), never both.
Your queries have no observable side effects. Your commands may return the artifact they created.
They must not smuggle a second “did it already exist?” question. Never name your writer `get*` / `check*`. A writer that reads like a query lies to you.

### 2.8 Don't return null, don't pass null

Authoritative detail: [`Clean-Code/13-stop-returning-null.md`](./Clean-Code/13-stop-returning-null.md).

**Never return null** from APIs you control. You return an empty collection, a Special Case /
Null Object, or you throw. You do not pass null. You reject it at the boundary. You do not hide your failures
as empty success (`catch { return [] }`). That lie will cost you.

### 2.9 Prefer exceptions to return codes

Authoritative detail: [`Clean-Code/03-exceptions-over-error-codes.md`](./Clean-Code/03-exceptions-over-error-codes.md),
[`34`](./Clean-Code/34-catch-is-not-if.md), [`37`](./Clean-Code/37-algorithm-breathes.md).

Your happy path is a flat list of steps. You throw on operational failure with context. You catch at
the boundary that can translate or report. You do not use catch as an ordinary branch.
You do not return status code bags in languages that have exceptions. Keep the path clean.

### 2.10 Extract 'til you drop

Each helper you pull out is your chance to give something a true name. Your named behaviors
are the words your codebase speaks. Will your team thank you for that name. They will if you choose well.

---

## 3. Comments

Authoritative detail: [`Clean-Code/`](./Clean-Code/README.md) lessons **05 to 10, 17, 19, 33, 38, 41**. Those lessons win. This part is only a reminder.

> Your comments are a last resort. You try rename and extract first. When you need one, you write why, warnings,
> public API docs, licenses. You do not write narration. You do not build history museums. A comment must earn its place.

### 3.1 Good comments (rare)

- **Legal.** Your copyright and license headers your policy demands (Clean-Code 07, 41). You keep them. The law is the law.
- **Intent.** *Why* you picked this path when it is not plain to your reader (17). Tell the reason you cannot put in code.
- **Warnings / amplification.** Your load bearing limits that a teammate might clean away by mistake (08). Warn him plainly.
- **Public API docs.** Your exported symbols. What they take. What they return. How they fail. One example (41). No noise (19).
- **TODO with context.** Your blocker or ticket, not `// TODO fix this` (08). Name what holds you up.

### 3.2 Bad comments (common)

- **Redundant**, `// increment i` before your `i++`. Your code already says it. Do not repeat it.
- **Misleading**, your code and comment disagree because you changed one and forgot the other. A lie is worse than silence.
- **Mandated**, a comment you demand on every getter fills your code with noise. Noise hides signal.
- **Journal**, "Changed Sep 3, then again Sep 4". That is what your version control is for. Let git keep the date.
- **Attributions/bylines**, `// added by Steve`. Your git blame knows who wrote it. You do not need the tag.
- **Closing-brace labels**, `} // end if`. If you need this, your block runs too long. Shorten it.
- **Commented-out code**, you delete it. Your version control remembers it for you. Dead code rots.
- **Non-local info**, you note on function A a rule that lives on function B. Put the note where it belongs.
- **Noise**, `// Default constructor.` above your default constructor. It adds nothing. Cut it.

### 3.3 When in doubt

If taking your comment out would not confuse your future reader, you take it out. If it would confuse him,
you try a better name or a small extracted function first. Code that explains itself beats a note about unclear code.

---

## 4. Formatting and Structure

### 4.1 Vertical density and openness

Lines that belong together sit together in your file with no blank line between them.
You part distinct ideas with exactly one blank line. No double blanks. Your reader sees the grouping at a glance.

### 4.2 Vertical ordering (newspaper metaphor)

You write your source file like a newspaper. The headline with the module intent sits at
the top. The ideas that matter most come next. Helpers and detail flow down.
Your reader should be able to stop anywhere and still hold the context. Would you read a paper from the bottom up. No.

### 4.3 Declarations close to use

Your loop counter belongs at the top of your loop. Your helper belongs just above
its first use. You do not haul things to the top of your function for looks. Near use is honest.

### 4.4 Horizontal formatting

- Lines under ~100-120 columns in your code. You wrap long lines. You use a named middle step so your reader can follow.
- One statement per line in your code. One idea per line.
- Steady whitespace around your operators and after your commas. Steadiness builds trust.
- You indent to show rank. You never use spacing to fake lined up columns. Faked columns rot on the next edit.

### 4.5 Team rules trump personal preference

You pick a formatter (Prettier, gofmt, rustfmt, Black, …) and a linter (ESLint, Clippy,
Ruff, …). You run them on commit. Your style fight is over. You get your time back for real work.

### 4.6 File organization

- One public idea per file. One class. One component. One module. Your reader knows what he opened.
- Small helpers that serve only that public idea stay in the same file. Do not scatter them.
- Your file name matches the idea name. No guessing.

---

## 5. Error Handling

### 5.1 Make errors a normal part of the design

Your errors are not the rare case. Your bugs are. You plan your error path before your happy path.
What will you do when this fails. Answer that first.

### 5.2 Prefer exceptions, not return codes

Authoritative: [`Clean-Code/03`](./Clean-Code/03-exceptions-over-error-codes.md).

Return codes force every caller you write to remember the check. Exceptions keep your steps
readable. In languages without exceptions (e.g. Go), you use that language’s **single**
idiomatic error channel with context. You still build no nested status pyramids. You still use no
TypeScript/Java-style `{ ok, error }` bags when exceptions exist.

### 5.3 Provide context

`throw new IOException("couldn't read")` tells your reader nothing. You include *what* you tried to do.
You name *which* resource you touched. You list *what* inputs you used, minus secrets. Your stack trace alone is not enough.
(Also required by Clean-Code 03.) Context is respect for the man on call.

### 5.4 Wrap third-party exceptions at boundaries

Authoritative: [`Clean-Code/31`](./Clean-Code/31-wrap-third-party-apis.md).

Your domain code must not leak vendor exceptions. You catch at the wrapper. You turn the error
into your domain’s own words. You throw again. Your core never learns the vendor name.

### 5.5 Fail fast

You catch bad state where it starts, not three layers down. You check your inputs at the door.
You never let a bad value drift through your system. Would you let rot spread. No.

### 5.6 Don't swallow exceptions

Authoritative: [`Clean-Code/34`](./Clean-Code/34-catch-is-not-if.md).

Your empty `catch` is always wrong. Your catch that turns failure into fake success (`[]`,
default “ok”) is always wrong. Your best effort work still logs with context and a short
why. Usually you throw again after you translate. Your normal business paths use Special Case or
defaults. They do not use try and catch for decisions.

### 5.7 One failure mechanism in exception languages

You use exceptions end to end inside your app. You map them to HTTP or status once at the edge.
You do not mix thrown exceptions with handmade error codes in your same layer. One way. Not two.

### 5.8 Treat internal errors and user errors differently

- **User errors** (bad input, not-found, permission denied) → you return a clear message, 4xx-class. Your user can act on it.
- **Internal errors** (broken invariant, network flake) → you return a short safe message to the user, 5xx-class,
  full detail in your logs. User-facing copy: `skills/engineering/errors/SKILL.md` Part B (subordinate to craft rules above). Craft rules still win.

### 5.9 Special-Case / Null-Object pattern

Authoritative: [`Clean-Code/13`](./Clean-Code/13-stop-returning-null.md), [`34`](./Clean-Code/34-catch-is-not-if.md).

Instead of null and guards all through your code, you return a Special Case object with the same
interface, or an empty collection or zero. You throw when missing data means true failure. Your caller stays clean.

---

## 6. Objects, Data, and Boundaries

### 6.1 Tell, don't ask

Do not pull a field out and do the math outside in your code. You tell the object to do the work.
`bill.calculateTotal()` > `calculateTotal(bill.lineItems)`. Would you rather read the aim or the math. The aim wins.

### 6.2 Law of Demeter

A method `f` of class `C` should call only methods of:
- `C` itself,
- objects `C` creates,
- objects passed as arguments,
- objects held in `C`'s fields.

Not: `a.getB().getC().doSomething()` (a "train wreck" in your code). If you feel the pull, you give the whole
chain to one method on the object that owns the facts. That owner does the work.

### 6.3 Data objects vs behavior objects

Authoritative: [`Clean-Code/29`](./Clean-Code/29-objects-vs-data-structures.md), [`21`](./Clean-Code/21-expose-behavior-not-data.md).

- **Data objects (structs, DTOs)**. You expose fields. **No business behavior**. This is right
  and planned at your boundaries (API responses, DB rows). Do **not** “fix” your DTO by
  stuffing domain rules into it. A DTO carries. It does not decide.
- **Behavior objects**. You hide data. You show operations. Your domain rules live here. This is where your craft shows.
- **Hybrids** (public getters/setters for everything *and* business methods) lose both
  strengths for you. You split them. Pick a side.
- **Anemic domain types** (should own rules but only carry fields) are a smell in your code. You move
  behavior into your domain objects and services, not into DTOs. Behavior belongs with its data.

### 6.4 Encapsulate at boundaries, not inside

Inside your system you pass rich objects freely. At your edge (HTTP,
DB, file), you turn them into plain data objects. You never let JSON or ORM entities wander into your
domain. Your domain stays clean.

### 6.5 Boundaries around third-party code

You wrap each outside library in a thin adapter you own. You earn three things:
- A single place to swap the library. One edit. Not fifty.
- A single place to hold its quirks. You learn them once.
- A smaller face for you to learn and test. Small is kind to your reader.

### 6.6 Learning tests

Before you lean on outside code, you write tests that *prove what you believe*
about it. When the library ships a new version, those tests tell you if your belief still holds.
Cheap cover for you. Would you trust a stranger without a test. No.

---

## 7. Classes and Modules

### 7.1 Single Responsibility Principle (SRP)

> A class should have one reason to change.

If your `Report` formats *and* saves *and* schedules, three owners
will pull it three ways. You split it. How many reasons would force you to touch this class. Count them.

### 7.2 Classes should be small

You measure by jobs, not by lines. A 500-line class with one job is
fine. A 50-line class with three jobs is not. Size lies. Duty tells the truth.

### 7.3 Cohesion

A class holds together when its fields and methods serve one idea. When fields
break into groups used by different methods, you watch two classes fight for one name. Split them.

### 7.4 Organize for change

You wall off the parts that will likely change. The parts that will *not* change
live in steady walls that all else leans on. Change has a place. Steadiness has a place.

### 7.5 Open/Closed Principle (OCP)

> Modules should be open for extension, closed for modification.

You add new behavior by *writing new code*, not by editing code that works.
Plugin walls, strategy objects, and polymorphism live for this. Would you risk old paths to add a new one. No.

### 7.6 Liskov Substitution Principle (LSP)

> A subtype must be usable anywhere its supertype is used.

If `Square extends Rectangle` but `setWidth` on a Square quietly changes height too,
you broke LSP. Inheritance is a promise. Your child must stand in for its parent.

### 7.7 Interface Segregation Principle (ISP)

> Clients shouldn't depend on methods they don't use.

A fat face forces callers and builders to learn things they never use.
Cut it into small faces, each for one role. Your caller thanks you.

### 7.8 Dependency Inversion Principle (DIP)

> Depend on abstractions, not concretions. High-level policy should not depend on
> low-level detail. Both should depend on abstractions.

Your domain layer holds `PaymentGateway` (an interface). Your infrastructure layer
holds `StripeGateway`. Nothing in the domain imports Stripe. Your policy never learns vendor names.

### 7.9 Composition over inheritance

Inheritance ties files tight and is hard to undo.
Holding a helper inside (composition) gives you the same reuse with looser ties. Use inheritance only for true "is-a" ties with
real swap in behavior. When in doubt, you hold. You do not extend.

### 7.10 Don't Repeat Yourself (DRY)

Two copies of one rule is debt. Three is a bug on its way. But two
things that *look* the same today yet mean different things are not
copies. They may grow apart later. Rule of three. You pull it out after the
third sighting if you are unsure. Patience here is discipline.

---

## 8. Architecture, the big picture

### 8.1 Separate construction from use

Code that *joins* things (dependency injection root, main, composition
root) stays apart from code that *does* the work. Your business rules never call `new` on their helpers. Would you mix the wiring with the work. No.

### 8.2 Clean Architecture / Hexagonal / Ports & Adapters

Layers from innermost to outermost:

1. **Entities**, enterprise-wide business rules. No framework imports. Your core truths live here.
2. **Use cases**, application-specific business rules. They lead entities. They hold your app story.
3. **Interface adapters**, controllers, gateways, presenters. They carry words between
  use cases and frameworks. Nothing more.
4. **Frameworks and drivers**, web framework, DB, UI, devices. Tools at the edge.

**The Dependency Rule**: source code dependencies point *inward only*. Entities know
nothing of use cases. Use cases know nothing of the web. Nothing imports
the framework upward. Inward. Always inward.

### 8.3 Package cohesion (Robert Martin)

- **REP**, Reuse/Release Equivalence: the unit of reuse is the unit of release. You ship what you reuse.
- **CCP**, Common Closure: you pack things that change for the same reason. One reason. One pack.
- **CRP**, Common Reuse: you pack things that get used together. You never force users
  to drag in things they do not need. Needless weight is a tax.

### 8.4 Package coupling

- **ADP**, Acyclic Dependencies: no loops in your pack graph. A needs
  B needs A means you cannot touch one without the other. Loops lock you.
- **SDP**, Stable Dependencies: you lean toward steadiness. You depend where things move least.
- **SAP**, Stable Abstractions: steady packs stay abstract. Shaky ones
  may stay concrete. Steadiness earns abstraction.

### 8.5 Draw the architecture before you write it

Draw your walls on a board first. Show where calls enter, where data rests, where
outside help gets called, where your domain lives. If you cannot draw it, you
have not planned it. Would you build a house without a sketch. No.

### 8.6 Defer decisions

Good walls let you hold off tool picks like framework, DB, UI. The longer you
keep them out of your core, the more paths you keep. A sound wall
lets you trade MySQL for Postgres, React for Vue, REST for gRPC, with *minimal*
domain code change. That freedom is the payoff.

---

## 9. Testing

### 9.1 TDD's three laws

1. Don't write production code except to make a failing test pass.
2. Don't write more of a test than is sufficient to fail.
3. Don't write more production code than is sufficient to pass the current failing test.

Hold these three and you will write code that can be tested. That habit is the side gain. Discipline first. Testability follows.

### 9.2 F.I.R.S.T tests

- **Fast**, tests you skip help no one. Slow tests die. Keep them quick.
- **Independent**, tests stand alone. No test leans on the run before it.
- **Repeatable**, same answer on any box, offline, any day. No weather in your tests.
- **Self-Validating**, green or red, no log reading by hand. The test speaks plain.
- **Timely**, written with the code, not weeks after. Late tests rot.

### 9.3 One logical assertion per test

You may keep several `assert` calls when they prove the *same* idea. The moment
you check a *second* idea, you cut a second test. One idea. One test.

### 9.4 Build a testing DSL

Your tests should read like promises. If you repeat setup, you pull out
helpers like `given.user.admin.withPlan("premium")`. Tests are code. They earn
the same care you give production.

### 9.5 Test at the right level

- **Unit**, one function or class, no outside talk. Hundreds of these, each a few milliseconds. Your backbone.
- **Integration**, several parts together, real helpers (DB, file, local process).
  Dozens of these. Enough to prove the joints hold.
- **E2E / Acceptance**, full road, true user walk. A handful of these. Few, because they cost.

The **testing pyramid**: many unit, fewer integration, very few E2E. Wide at the base. Narrow at the top.

### 9.6 Clean tests

Tests you cannot read stay broken. You treat them like shipping code. Small.
Clear names. One care at a time. One shaky test kills faith in *all* tests. Would you trust a scale that lies sometimes. No.

### 9.7 Test behavior, not implementation

A test that snaps when you rename a private helper tests the wrong thing.
You test what the caller sees. Inputs. Outputs. Side moves. Not how you got there. Behavior holds. Shape may move.

### 9.8 Property-based testing where it fits

For code with wide open inputs (parsers, encoders, math), you state *rules that always hold*
(round-trip, commutativity, invariants) rather than a few picked cases. Rules prove more than cases.

---

## 10. Concurrency

### 10.1 Default to not concurrent

Running side by side costs you in head pain. You pay it only when you need speed,
quick answers, or true parallel work you cannot get alone. Simple first. Threads later.

### 10.2 Keep concurrent code behind a small API

The hard parts live in one small room. All above that door you think in straight lines. Small door. Safe house.

### 10.3 Don't share mutable state across threads

Pick one path for your code:
- **Immutable data**, it cannot rot under you. No writes. No races.
- **Message passing**, each thread owns its land. Threads talk by queue. No shared yard.
- **Explicit synchronization**, locks, mutexes, atomics. This path demands care and
  hard testing. You earn every line.

In that order of taste. Top first. Bottom last.

### 10.4 Know your runtime's concurrency model

- JavaScript: single threaded event loop plus workers plus async. Never block the loop. The loop is your heart.
- Java: OS threads plus Virtual Threads (Loom), `synchronized`, `java.util.concurrent`. Learn the toolbox.
- Go: goroutines plus channels. `go vet -race` is mandatory. You run it. No skip.
- Rust: ownership stops data races at build time. The compiler guards you.
- Python: GIL caps true parallel work. You use processes or async. You work with the limit.
- C/C++: you stand alone here. You use proven kits (TBB, Boost). Do not hand roll your own.

### 10.5 Test for concurrency bugs

Race tools, hard stress runs, fuzz runs, and chaos runs catch what eyes miss.
You plan steady runs under load. Your review cannot see a race. Your rig can.

### 10.6 Lock scope ≪ function scope

You take the lock late. You free it early. You never hold a lock across a network call, disk work,
or a call you do not own. Short hold. Clean release. That is discipline.

---

## 11. Version Control (Git) Hygiene

### 11.1 Small, focused commits

Each commit holds one clear change. A fix and a feature never share a bed.
A cleanup and a behavior shift never share a commit. One thought. One commit. Your history reads clean.

### 11.2 Meaningful commit messages

- **Subject line** (≤72 chars): plain command mood, "Fix login redirect", not
  "Fixed" or "Fixes". You command. You do not report past deeds.
- **Body**: *why*, not *what* (the diff shows what). Link tickets. Your future reader needs the reason.
- Think of **Conventional Commits** (`feat:`, `fix:`, `refactor:`, …) for notes
  and semantic release. Shared words help machines and men.

### 11.3 Branching

You keep branches short lived. You pull and fold often. A branch left open for two weeks turns into
a merge fight. Would you let two weeks of work drift apart. No.

### 11.4 Never rewrite published history

You may mend and squash *before* you push. Once a branch is shared, rewriting it
wrongs your team. Force push to `main` is a fireable offense. You do not touch shared time.

### 11.5 Review before merging

Even when you wrote it. `main` is holy. PRs and MRs force a pause and a read. No straight push. No hurry past review.

### 11.6 Tag releases

`v1.2.3` tags make turn backs easy. You add release notes. Semantic Versioning holds:
MAJOR breaks, MINOR adds backward-compatibly, PATCH fixes. Numbers with meaning.

---

## 12. Code Review

### 12.1 Review for intent, then for correctness, then for style

A reviewer who starts with nits missed the point. You start here. *Does this fix the
right need in the right way.* Style can wait. Aim comes first.

### 12.2 Critique the code, not the author

"This function holds three jobs", good. "You always bloat", bad. You hit the code. You never hit the man.

### 12.3 Explain why

"This reads odd" with no link teaches nothing. "We pick X because Y, see ADR-7"
teaches. You show your reason. You leave a trail.

### 12.4 Approve or block, don't drown in suggestions

A review with 40 nits and no call will not land. Either it ships
or it holds. You say which. Plain and kind.

### 12.5 Authors: make your reviewer's job easy

- PR words: what, why, how, how tried. Your reviewer should not guess.
- Small PRs (<400 lines) earn true reads. 2000-line PRs earn nods. Size decides care.
- You answer each note (even with "done" or "hold, because …"). No silent skip.

---

## 13. Refactoring

### 13.1 Refactor in its own commit

You never mix cleanup with new behavior. Mixed work blinds review. You ship the cleanup
alone. You prove with tests that nothing moved. Then you add the new path. Clean steps.

### 13.2 The Mikado Method

When the rework is too large to see through, you start at the aim. You note what blocks you.
You step back. You clear the blocks first. You loop. Small bites beat one blind leap.

### 13.3 Seams

Old code opens for tests only at seams you can feed a fake through. You build seams (faces,
feed points, small param packs) at the edges, and the tangle turns
testable bit by bit. Patience wins here.

### 13.4 Catalog of refactorings (Fowler)

Learn these moves and speak them by name. Shared names make your team fast:
- Extract Method / Inline Method
- Extract Class / Inline Class
- Rename Variable / Method / Class
- Introduce Parameter Object
- Replace Conditional with Polymorphism
- Replace Temp with Query
- Move Method / Move Field

Named moves turn into team speech. When you say the name, your teammate sees the change.

### 13.5 Don't refactor broken code

Green tests first. Cleanup second. Else you will never know which move broke the build. Would you rework blind. No.

---

## 14. Observability and Operability

### 14.1 Logs, metrics, traces, the three pillars

- **Logs**: what happened. Structured (JSON, not `printf`), with correlation IDs. You can read them by machine. You owe that to the man on call.
- **Metrics**: how much, how often. Histograms for latency, counters for events. Numbers tell the load. You watch them.
- **Traces**: how a request flows across services. OpenTelemetry if you can. You follow the path end to end.

### 14.2 Log at boundaries

You log entry, exit, and failure of every external call (DB, HTTP, queue). Never inside hot
loops. Hot loops drown you in noise. Log at the doors.

### 14.3 Useful log lines

Include: timestamp, level, correlation/request id, user id (hashed if sensitive),
what was attempted, result. Never: secrets, PII beyond what you need, whole request
bodies. What would you want leaked about you. Nothing. Log like a pro.

### 14.4 Alerts that page are promises

Each bell that wakes a man must call for real work. If the answer to "what do I do" is
"nothing, it cries wolf", you kill the bell or mend the trip. False alarms burn trust.

### 14.5 Graceful degradation

When a helper fails, you *bend* instead of falling flat. Cache. Default.
Hold for later. Full falls are seldom a must. Would you shut the shop because one shelf broke. No.

### 14.6 Know your SLIs / SLOs

Service Level Indicators (what you measure) and Objectives (your targets) turn
steadiness into true engineering work, not a wish. Numbers keep you honest. Watch them.

---

## 15. Security

### 15.1 Validate at trust boundaries

Each scrap that steps into your house (HTTP, CLI, file, queue) stays suspect till proven
clean. Parse, do not just check. You turn raw input into a typed, constrained domain
value as early as possible. Then you trust it internally. Early shape keeps you safe.

### 15.2 Principle of Least Privilege

Each worker, each service name, each user gets the least rights to do the
job, and no more. Closed by default. Would you hand keys to rooms a man never enters. No.

### 15.3 Never log secrets

API keys, tokens, passwords, session IDs, full credit cards. Never in logs.
Even in dev logs, because dev logs turn into prod logs one day. A leak is a leak.

### 15.4 Defense in depth

Each layer thinks the one before it fell. WAF → auth → input validation → DB
parameterization → row-level security. One fall must not sink you. Layers save you.

### 15.5 Cryptography

- **Do not build your own.** You use `libsodium`, `OpenSSL`, your platform KMS. Home locks fail.
- **You treat passwords right:** Argon2id/bcrypt/scrypt, never MD5/SHA1/SHA256. Old hashes betray you.
- **Rotate secrets** and hold a plan for "what if this leaks today". Leaks happen. Plans save you.

### 15.6 Supply chain

You commit your lockfiles (`package-lock.json`, `Cargo.lock`, `poetry.lock`). You scan
your helpers (Snyk, Dependabot, `npm audit`). You pick small, tried kits over shiny
ones with 3 keepers. Would you bet your shop on strangers. No.

### 15.7 OWASP Top 10, memorize the current list

The most hit weak spots on the web, revised every few years. As of the
2021 edition. Learn them cold:

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

You check each web app against these. Re-check [owasp.org](https://owasp.org/Top10/)
each project, the list moves and shifts names as new hits rise. Stay current.

---

## 16. Performance

### 16.1 Measure before optimizing

You profile. You bench. Without numbers you will tune the wrong spot 90% of the time. Guessing is not work. Measuring is work.

### 16.2 Big-O first, micro-optimizations last

An `O(n²)` loop in Python costs more than `O(n log n)` in JavaScript. You fix the
plan before you shave the steps. Big O first. Small trims last.

### 16.3 Latency vs throughput

Two different fights. Code that faces users fights for
the tail (p99). Code that grinds batches fights for the mean. Know which fight you fight.

### 16.4 Caching is a promise, not a shortcut

Each cache you add brings a staleness debt. You state how old may pass,
you clear right, and you know the road when the cache dies. Can you live with old answers. Decide up front.

### 16.5 Avoid premature distribution

One tuned box beats a loose crowd. You grow up before you grow out,
unless true load demands more. Spread systems breed fresh fail ways. Do you need that pain now. Often no.

---

## 17. Documentation

### 17.1 Code-adjacent > code-distant

- **README.md**: how to run, how to test, the one page a new hand needs to join. Write it for him.
- **CONTRIBUTING.md**: your ways, your review path, your release steps. No guessing.
- **ADR (Architecture Decision Records)**: one short note per weighty call
  (context → decision → consequences). They grow old *with* your code. They tell why.

### 17.2 Docstrings on public APIs

Each open face you ship tells what it does, what it takes, what it gives back, what
it throws, with a sample when the use is not plain. Your IDE shows this at the call. Write for that moment.

### 17.3 Examples > prose

One live 10-line run beats three long talks.
Show. Then tell.

### 17.4 Don't document what the code already says

"Increments the counter" over `counter++` is noise. "Capped at 100/min to
spare the billing API downstream" is news. One wastes eyes. One saves calls.

### 17.5 Diagrams for architecture, not for getters

You draw flows for calls. You draw boxes for services.
You keep them in your repo (Mermaid, PlantUML) so they live with versions and all can find them. Drawn truth beats stray talk.

---

## 18. The Four Rules of Simple Design (Kent Beck)

In this order, no skip:

1. **Passes all tests**, your acts are right.
2. **Reveals intent**, each name and each shape tells your reader its aim.
3. **No duplication**, one idea, one home.
4. **Fewest elements**, the smallest count of classes, methods, modules that
  still hold the first three.

When you clean, you honor this order. You never cut shapes at the cost
of clear aim. Clarity outranks brevity.

---

## 19. Code Smells, A Checklist

When you or your tired self at 3 AM mutters "this feels off", you will find it is one of these. Learn the smells. Trust your nose.

### Names

- **Vague** (`data`, `info`, `handler`, `manager`), what data. Whose handler. Vague steals time from your reader.
- **Lies** (`list` that isn't a list, `validate` that mutates), the name lies to you. Lies breed bugs. Tell truth.
- **Inconsistent** (`fetchUser` / `getAccount` / `retrieveOrder`, pick one verb). One job. One verb. No drift.

### Functions

- **Long**, runs past your screen. Long hides jobs.
- **Too many arguments**, 4+. Four means a missing object.
- **Flag arguments**, a true false switch that picks behavior. Split it.
- **Side effects**, does what the name never said. Names must tell truth.
- **Deep nesting**, three+ levels of `if`/`for`. Pull out.
- **Dead parameter**, never used. Cut it.

### Classes

- **God class**, knows too much, does too much. One class plays the whole team.
- **Feature envy**, a method that uses another class's fields more than its own. Homesick code. Move it home.
- **Hybrid / anemic domain**, getters everywhere *plus* rules, or domain type with only fields when it should own behavior (DTOs at boundaries are fine. See 29). Pick a side.
- **Shotgun surgery**, one change needs 10 files. Weak hold. Pull together what moves together.

### Comments

- **Redundant**, says again what the code says. Twice is once too many.
- **Commented-out code**, dead lines. Cut them.
- **TODO with no owner or date**, no name, no time. Dates push work.

### Control flow

- **Duplicated logic in branches**, same lines twice. Pull out. Twice is debt.
- **Switch on type**, your code asks what it is. Give that choice a home with many shapes.
- **Magic numbers / strings**, bare values. Give them names your reader trusts.
- **`null` in public APIs**, you return Optional or Special Case. Never bare null.

### Coupling

- **Train wrecks** (`a.b().c().d()`), you break Demeter. Long chains snap. Shorten them.
- **Global mutable state**, hidden ties all over. No man sees the full pull. Kill it where you can.
- **Cyclic dependencies** between packages and modules, round trips. Cut the loop.

### Testing

- **No tests**, you fly blind. Blind flies crash. Write one.
- **Tests that never fail**, empty claims. They prove nothing. Fix the claim.
- **Flaky tests**, you kill or mend today, you never "skip". Skips lie. Trust dies.
- **Tests coupled to implementation**, they snap on rename. Test acts. Not walls.

---

## 20. Cultural Rules

### 20.1 Disagreement is a conversation, not a war

Two good builders will differ. That is health. You use facts, small trials, ADRs to
meet. When talk stalls, one named decider calls it. Then all commit. Would you stall a team for pride. No.

### 20.2 Blameless retrospectives

"How did our build let this pass" beats "who broke this" each time.
Men ship slips. Builds let them through. Fix the build.

### 20.3 Teach as you go

One note that shows the whole crew a rule with a link beats ten notes that
mend one line. You teach when you review. Teaching scales.

### 20.4 Estimates are wrong

You treat guesses as spans, not vows. The bigger the job, the wider the span. You cut work
till the span fits your sprint. Small is honest.

### 20.5 Respect the on-call

You do not push wild work on Friday. You do not push what you have not tried. You do not
push at 4:50 PM. Your on call mate has a home too.

### 20.6 Rest

Weary hands plant bugs. Sleep is output. The lone hero who works each weekend burns
out, and your crew pays his debt. Rest is craft too.

---

## 21. Quick Reference (the fridge magnet)

| When you… | Ask yourself… |
|---|---|
| Name a thing | Would a new teammate grasp it with no context. |
| Write a function | Can you say what it does in one short line with no and. |
| Add a comment | Could you fix the code so this comment was not needed. |
| Copy-paste | Is the third time here. Extract. |
| Reach for inheritance | Would composition do. |
| Catch an exception | What will you do about it. |
| Return null | What Special Case could you return instead. |
| Share mutable state | Can you use a message or an immutable copy. |
| Add a parameter | Does this function now do two things. |
| Open a giant PR | Can you split this into a refactor + a behavior change. |
| Log something | Does this have a correlation ID. Is any of it a secret. |
| Deploy | Is it Friday 4:50 PM. Think twice. |

---

## 22. Further Reading (one-line each)

- **Clean Code**, Robert C. Martin. The source text for most of this handbook. You read it first. You mark it up.
- **Clean Architecture**, Robert C. Martin. Dependency rule + SOLID at the system level. Walls that hold at scale.
- **The Pragmatic Programmer**, Hunt & Thomas. DRY, orthogonality, tracer bullets. Old advice that still pays.
- **Refactoring**, Martin Fowler. Named refactorings as a vocabulary. You speak them daily.
- **Working Effectively with Legacy Code**, Michael Feathers. Seams. How to test untested code. Your way into old tangles.
- **Domain-Driven Design**, Eric Evans. Bounded contexts, ubiquitous language. One tongue for the team.
- **A Philosophy of Software Design**, John Ousterhout. Deep modules, complexity. How you fight tangle with depth.
- **Designing Data-Intensive Applications**, Martin Kleppmann. How distributed systems really work. No myths. Only tradeoffs.
- **Accelerate**, Forsgren et al. The metrics that predict elite engineering teams. You track what counts.
- **The Mythical Man-Month**, Fred Brooks. Still true 50 years later. Men and months do not trade even.

---

*This paper is a guide, not a law. When clarity fights a rule, clarity
wins. When speed fights a rule, you ask if the rule still earns its place for your work. Rules are tools. Your judgment is the craft. Use them like a craftsman.*
