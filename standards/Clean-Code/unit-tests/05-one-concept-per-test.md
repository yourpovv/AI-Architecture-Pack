# 05. One Concept Per Test

> **Rule:** Name each test for the exact behavior it guards. One test covers one concept — never three behaviours under a function name.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

A test named after the function it calls (`testRegister`) documents nothing: inside, lines 1–3 verify initial member state, line 4 promises raw passwords are never exposed, line 5 rejects duplicate emails. One failure, three suspects — the reader untangles what each line checked.

Split into focused tests named for the promise: member creation, password safety, duplicate rejection. Now a red names the broken promise while the other two stay green. Tests are specifications; a test covering several concepts specifies none of them.

---

## Rules

- Test name = the behavior/promise, not the function under test.
- If failure needs line-by-line reading to identify the concept, split.
- Each test asserts one concept; shared setup becomes helpers/factories, not merged tests.
- Keep the three-way split: state, safety, rejection — each in its own test.

---

## Bad vs good

### Bad
```text
test_register():
  assert member.name == "Ann"        // concept 1: creation
  assert member.active == true       // concept 1
  assert member.rawPassword == null  // concept 2: safety
  assert rejects("ann@x.com")        // concept 3: duplicates
```

### Good
```text
test_newMemberStartsActive(): ...
test_neverExposesRawPassword(): ...
test_rejectsAlreadyRegisteredEmail(): ...
```

---

## Review checklist

- [ ] Does the test name state the promise without opening the body?
- [ ] Would a failure identify the concept instantly?
- [ ] Is there exactly one "why would this break" per test?

---

## Related standards

- UNIT TESTS 06 F.I.R.S.T.
- UNIT TESTS 04 Writing Clean Tests
- 15 One thing

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
