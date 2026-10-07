# 02. Keep Your Tests Clean

> **Rule:** Write tests as clean as production. You live in test code first — if it rots, features stop being small and skips hide regressions.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

"Tests don't ship, so they don't have to be clean" compounds daily. Every feature starts in test code — you are there first, before production. Tangled tests turn a small change into test-repair work; an unreadable failure gets skipped instead of fixed; enough skips for the same reason ("stopped being readable") and the suite protects nothing.

Behavior changes, so tests must change with it — and a test you can read is a test you can update. You are the reader here every single day. Production sinks to the standard your tests set, so set it high.

---

## Rules

- Apply naming, extraction, and DRY to tests exactly as to production.
- Never leave skipped/ignored tests as permanent residents — fix readability or delete with intent.
- A test that cannot explain its failure on red is broken — rewrite it, do not skip it.
- Keep helpers/factories for shared setup so each test stays a short story.

---

## Bad vs good

### Bad
```text
test_checkout2_skip  // skipped — "too tangled to tell what it wanted"
test_checkout_old   // 80 lines, duplicated setup, cryptic asserts
```

### Good
```text
test_rejectsExpiredCard():  // small, named, uses shared cardFactory()
test_appliesFixedDiscount(): ...
```

---

## Review checklist

- [ ] Would I accept this naming/structure in production?
- [ ] On red, does the test say what it wanted without debugging?
- [ ] Are skips zero, or each tracked with a reason and owner?

---

## Related standards

- UNIT TESTS 06 F.I.R.S.T.
- UNIT TESTS 05 One Concept Per Test
- 22 Messy first draft, then clean

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
