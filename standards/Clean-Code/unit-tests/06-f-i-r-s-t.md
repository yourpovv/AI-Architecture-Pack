# 06. F.I.R.S.T.

> **Rule:** Tests are Fast, Independent, Repeatable, Self-Validating, Timely. Anything less and you stop running them — and lose the freedom to clean.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Tests are confidence infrastructure. **Fast:** slow suites get skipped, so bugs arrive late and cleanup feels unsafe. **Independent:** shared state turns one failure into cascading noise that hides the real bug. **Repeatable:** CI, laptop, offline — same result, so a red always means a real bug, never the environment. **Self-validating:** boolean green/red, no log archaeology. **Timely:** written just before the production they enable, so the code grows testable instead of resisting tests after the fact.

Together they keep the suite protecting code without ever slowing you down.

---

## Rules

- Fast: milliseconds per unit test; isolate slowness (network, disk, sleep) behind fakes.
- Independent: no test sets up conditions for the next; each builds its own world.
- Repeatable: no network/time/locale dependence; same outcome anywhere, anytime.
- Self-validating: assert to pass/fail — never "read the log and decide".
- Timely: test just before the code that makes it pass (see 55).

---

## Bad vs good

### Bad
```text
test_A_createsUser()       // sets global user
test_B_editsUser()         // depends on test_A's user; fails in isolation
  // passes locally, fails in CI (needs network); ends with print(logs)
```

### Good
```text
test_rejectsDuplicateEmail():
  repo = inMemoryRepo(withUser("a@x.com"))  // own world, fast, repeatable
  assert rejects(repo.register("a@x.com"))  // boolean verdict
```

---

## Review checklist

- [ ] Can I run one test alone, in any order, offline, and trust red?
- [ ] Does each test declare green/red without manual inspection?
- [ ] Was it written just before the production code (timely)?

---

## Related standards

- UNIT TESTS 01 The Three Laws of TDD
- UNIT TESTS 05 One Concept Per Test
- UNIT TESTS 04 Writing Clean Tests

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
