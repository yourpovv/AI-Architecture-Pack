# Clean Code Standards (all projects)

> **Your mandatory coding standards** for every project that uses this Architecture pack.  
> Derived from the personal clean-code lesson set (s4.codes-aligned), expanded into engineering rules with examples and review checklists.

## How to use

| Audience | Use |
|---|---|
| **You** | Read when forming habits; keep open during reviews |
| **Agents** | Load **one lesson file** that matches the task — never the whole folder |
| **New projects** | Copy `standards/Clean-Code/` (or symlink) into `docs/standards/Clean-Code/` and point `AGENTS.md` at it |
| **PR review** | Pick relevant numbers from the map below |

**Also load (subordinate to this folder):**

- `skills/engineering/uncle-bob/SKILL.md` — how to *apply* Clean Code / Clean Architecture / Clean Coder  
- `skills/engineering/errors/SKILL.md` — user-facing error *copy* (three laws) + extra examples; **must not contradict 03/12/13/34/37**  
- `skills/engineering/necessary-comments/SKILL.md` / `skills/engineering/craft/SKILL.md` — comment craft; subordinate to 05–10, 17, 19, 33, 38, 41  
- `standards/Principles.md` — SOLID, testing, security, concurrency; **craft sections defer to Clean-Code/**

### Authority (no contradictions)

When any Architecture doc disagrees with this folder on naming, functions, comments, null, exceptions, Demeter, DRY, CQS, or structure:

1. **`standards/Clean-Code/`** (these lessons) wins.  
2. Then Uncle Bob methodology (`skills/engineering/uncle-bob/SKILL.md`).  
3. Then other skills / `Principles.md`.  
4. Project `AGENTS.md` may name a **explicit** exception for that repo only.

Other packs were rewritten to follow this order. Prefer structure fixes (rename, extract, split, wrap) over comments or error-code returns.

---

## Agent load policy

1. Do **not** default-load all 60 files.  
2. Load the **single** lesson file that matches naming, errors, comments, structure, etc. — flat `NN-*.md` or one file from `solid|classes|function-design|unit-tests|boundaries/`.  
3. For a full audit, load this README + scan the map, then open only files for findings.  
4. Prefer structure fixes (rename, extract, split, wrap) over adding comments or return codes.  
5. On conflict with `Principles.md` or `skills/*`, follow **this folder**.

---

## Full map (01–41 + grouped lessons, 60 total)

| # | File | One-line rule |
|---|---|---|
| 01 | [01-side-effects-honest-functions.md](./01-side-effects-honest-functions.md) | No side effects beyond the name |
| 02 | [02-single-argument-patterns.md](./02-single-argument-patterns.md) | Argument *roles* — no flag-jobs (not “only one arg ever”) |
| 03 | [03-exceptions-over-error-codes.md](./03-exceptions-over-error-codes.md) | Exceptions over error codes (happy path flat) |
| 04 | [04-clarity-is-king.md](./04-clarity-is-king.md) | No mental mapping |
| 05 | [05-code-evolves-comments-may-not.md](./05-code-evolves-comments-may-not.md) | Stale comments are worse than none |
| 06 | [06-intention-revealing-names.md](./06-intention-revealing-names.md) | Names reveal intent |
| 07 | [07-leave-history-to-git.md](./07-leave-history-to-git.md) | No commented-out code / journals |
| 08 | [08-comments-that-protect.md](./08-comments-that-protect.md) | Warnings, amplification, real TODOs |
| 09 | [09-comments-clarify-not-confuse.md](./09-comments-clarify-not-confuse.md) | Specific, local, complete |
| 10 | [10-comments-must-communicate.md](./10-comments-must-communicate.md) | Instantly readable comments |
| 11 | [11-variables-close-to-use.md](./11-variables-close-to-use.md) | Locals near use; fields grouped |
| 12 | [12-define-contract-before-logic.md](./12-define-contract-before-logic.md) | Failure contract first |
| 13 | [13-stop-returning-null.md](./13-stop-returning-null.md) | Never return null — empty / Special Case / throw |
| 14 | [14-dry-single-source-of-truth.md](./14-dry-single-source-of-truth.md) | One authoritative representation |
| 15 | [15-one-thing-tell-a-story.md](./15-one-thing-tell-a-story.md) | One thing; top-down story |
| 16 | [16-not-everything-is-an-object.md](./16-not-everything-is-an-object.md) | Classes only when needed |
| 17 | [17-comments-tell-why.md](./17-comments-tell-why.md) | Why, not how |
| 18 | [18-stepdown-rule.md](./18-stepdown-rule.md) | Highest level first |
| 19 | [19-noise-comments.md](./19-noise-comments.md) | If code says it, comment is noise |
| 20 | [20-names-that-fail.md](./20-names-that-fail.md) | Call site must be enough |
| 21 | [21-expose-behavior-not-data.md](./21-expose-behavior-not-data.md) | Tell objects; don’t strip-mine fields |
| 22 | [22-messy-first-draft-then-clean.md](./22-messy-first-draft-then-clean.md) | Draft messy; ship clean |
| 23 | [23-low-argument-count.md](./23-low-argument-count.md) | Keep arity low |
| 24 | [24-bury-the-switch.md](./24-bury-the-switch.md) | Bury switches; keep policy clean |
| 25 | [25-let-tools-handle-types.md](./25-let-tools-handle-types.md) | Types/linters/formatters own ceremony |
| 26 | [26-extract-from-large-functions.md](./26-extract-from-large-functions.md) | Extract until the parent is an outline |
| 27 | [27-one-abstraction-level.md](./27-one-abstraction-level.md) | One abstraction level per function |
| 28 | [28-pairs-and-triads.md](./28-pairs-and-triads.md) | Careful pairs/triads; named bundles |
| 29 | [29-objects-vs-data-structures.md](./29-objects-vs-data-structures.md) | Object **or** data structure |
| 30 | [30-searchable-names.md](./30-searchable-names.md) | Searchable names; no magic numbers |
| 31 | [31-wrap-third-party-apis.md](./31-wrap-third-party-apis.md) | Wrap vendors; own errors |
| 32 | [32-law-of-demeter.md](./32-law-of-demeter.md) | No stranger chains |
| 33 | [33-code-explains-itself.md](./33-code-explains-itself.md) | Rename/extract before “what” comments |
| 34 | [34-catch-is-not-if.md](./34-catch-is-not-if.md) | Exceptions ≠ normal branches |
| 35 | [35-formatting.md](./35-formatting.md) | Vertical density + hierarchy |
| 36 | [36-honest-naming-no-disinformation.md](./36-honest-naming-no-disinformation.md) | No misleading names |
| 37 | [37-algorithm-breathes.md](./37-algorithm-breathes.md) | Happy path reads as pure steps |
| 38 | [38-comments-apologizing-for-structure.md](./38-comments-apologizing-for-structure.md) | Fix structure, not brace comments |
| 39 | [39-pronounceable-names.md](./39-pronounceable-names.md) | Speakable names |
| 40 | [40-command-query-separation.md](./40-command-query-separation.md) | Command **or** query |
| 41 | [41-docs-for-the-world.md](./41-docs-for-the-world.md) | Code for team; docs for the world |

---

## Grouped lessons (tile-aligned)

| Group | # | File | One-line rule |
|---|---|---|---|
| SOLID | 01 | [01-single-responsibility-principle.md](./solid/01-single-responsibility-principle.md) | One job per class |
| SOLID | 02 | [02-a-reason-to-change.md](./solid/02-a-reason-to-change.md) | One actor, one class |
| CLASSES | 01 | [01-naming-pressure.md](./classes/01-naming-pressure.md) | Argued name means unfinished split |
| CLASSES | 02 | [02-feature-envy.md](./classes/02-feature-envy.md) | Move method to its data |
| CLASSES | 03 | [03-hidden-classes.md](./classes/03-hidden-classes.md) | Split where data stops being shared |
| CLASSES | 04 | [04-policy-and-detail.md](./classes/04-policy-and-detail.md) | Declare workflow or do work, never both |
| CLASSES | 05 | [05-prefactoring.md](./classes/05-prefactoring.md) | Refactor on real requirements, not guesses |
| CLASSES | 06 | [06-overengineering.md](./classes/06-overengineering.md) | Split only for test/dedup/name/extension |
| FUNCTION DESIGN | 01 | [01-function-contexts.md](./function-design/01-function-contexts.md) | Private is the change boundary |
| FUNCTION DESIGN | 02 | [02-naming-altitude.md](./function-design/02-naming-altitude.md) | Name the why, one level above the how |
| FUNCTION DESIGN | 03 | [03-name-length.md](./function-design/03-name-length.md) | Narrow scope long name, wide scope short |
| UNIT TESTS | 01 | [01-the-three-laws-of-tdd.md](./unit-tests/01-the-three-laws-of-tdd.md) | Only code tests asked for |
| UNIT TESTS | 02 | [02-keep-your-tests-clean.md](./unit-tests/02-keep-your-tests-clean.md) | Tests to production standard |
| UNIT TESTS | 03 | [03-tests-enable-the-ilities.md](./unit-tests/03-tests-enable-the-ilities.md) | Tests make change safe |
| UNIT TESTS | 04 | [04-writing-clean-tests.md](./unit-tests/04-writing-clean-tests.md) | Build world, act once, assert claim |
| UNIT TESTS | 05 | [05-one-concept-per-test.md](./unit-tests/05-one-concept-per-test.md) | One test, one promise |
| UNIT TESTS | 06 | [06-f-i-r-s-t.md](./unit-tests/06-f-i-r-s-t.md) | F.I.R.S.T. tests |
| BOUNDARIES | 01 | [01-wrap-third-party-code.md](./boundaries/01-wrap-third-party-code.md) | Own the call surface, limit blast radius |
| BOUNDARIES | 02 | [02-the-adapter-pattern.md](./boundaries/02-the-adapter-pattern.md) | Wish interface, translate at border |

---

## Topic clusters (load by concern)

| Concern | Lessons |
|---|---|
| **Naming** | 04, 06, 20, 30, 36, 39, CLASSES 01, FUNCTION DESIGN 02–03 |
| **Functions & structure** | 01, 02, 15, 18, 22, 23, 24, 26, 27, 28, 40, SOLID 01–02, CLASSES 02–04, CLASSES 06 |
| **Errors** | 03, 12, 13, 34, 37 |
| **Comments** | 05, 07, 08, 09, 10, 17, 19, 33, 38, 41 |
| **Objects & design** | 16, 21, 29, 31, 32, FUNCTION DESIGN 01, BOUNDARIES 01–02, CLASSES 05 |
| **DRY & tools** | 14, 25, 35 |
| **Variables / formatting** | 11, 35 |
| **Testing** | UNIT TESTS 01–06 |

---

## Suggested `AGENTS.md` snippet (drop into projects)

```markdown
## Coding standards
- Mandatory: docs/standards/Clean-Code/ (this Architecture pack).
- Agents: load only the Clean-Code lesson file(s) relevant to the task.
- Prefer rename/extract/split/wrap over comments or error-code returns.
- Full map: docs/standards/Clean-Code/README.md
```

---

## Editing a lesson

The 60 lesson files are hand-maintained. Edit the lesson file directly
(flat `NN-*.md`, or the grouped `solid|classes|function-design|unit-tests|boundaries/` files),
then update its one-line rule in the map above so the two never drift apart.

Keep the shared trailing **Authority** block identical across files. If that block changes,
change it in all 60.
