# 04. Writing Clean Tests

> **Rule:** Structure every test as facts about the world, one action, one claim. Describe what the setup means, not how it was assembled.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Unreadable tests bury three claim lines under boilerplate: you read everything and still do not know what is checked. The fix is three distinct parts — **build** the world, **run** the action once, **check** the result — each describing *what*, not *how*.

Setup should read as facts ("today is Jan 2026, card expired Dec 2020"), not assembly steps. The action section holds only the core call; extra construction moves to helpers serving the whole suite. The check holds only the final claim, not result-unpacking mechanics. Then the test reads as a sentence: given this world, when this happens, expect this.

---

## Rules

- Build: state facts about the world, not mechanical construction steps.
- Act: exactly one core action stays in the test; move scaffolding to shared helpers.
- Assert: only the final claim — no unpacking, branching, or second actions.
- Extract reused setup into suite-level factories/builders, not copy-paste.

---

## Bad vs good

### Bad
```text
test_expired():
  cal = Calendar.getInstance(); cal.set(2026, 0, 1)  // how, not what
  card = new Card(); card.setExp(12, 2020); card.setNum(...)  // assembly
  result = validator.validate(card); parsed = result.getCode()  // unpacking
  assert parsed == 4
```

### Good
```text
test_rejectsExpiredCard():
  // build: today Jan 2026, card expired Dec 2020
  // act: validate(card)
  // check: rejected as expired
```

---

## Review checklist

- [ ] Can I read build / act / assert as one sentence?
- [ ] Does setup state facts rather than assembly?
- [ ] Is there exactly one action and one claim?

---

## Related standards

- UNIT TESTS 05 One Concept Per Test
- UNIT TESTS 06 F.I.R.S.T.
- 33 Code explains itself

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
