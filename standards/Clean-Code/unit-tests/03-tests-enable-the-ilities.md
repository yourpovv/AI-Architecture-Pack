# 03. Tests Enable the -ilities

> **Rule:** Stop guarding code you are afraid of. Write the behavior tests that make you willing to change it — then change it.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

"If it works, don't touch it" is fear talking: the code is a mess, but without tests a cleanup or speedup might silently break behavior. Tests do not prove correctness — they pin behavior so implementation becomes your choice. Slow? Swap the approach; a failing test names exactly what broke, you restore the behavior, and the new approach stands.

Same for readability: pin the behavior, clean the structure, let red guide you. Tested code stays flexible, maintainable, and reusable precisely because you remain willing to change it.

---

## Rules

- Before refactoring or optimizing feared code, pin its behavior with characterization tests.
- Tests assert observable behavior, not implementation — so refactors stay green.
- On red after a change, fix what the test points at; do not revert to fear.
- No "do not touch" zones: untested → add tests → clean, in that order.

---

## Bad vs good

### Bad
```text
// legacy pricing — everyone afraid, no tests, "works, don't touch"
function price(order): ... // 200 lines, unknown edge cases
```

### Good
```text
test_pricesBulkDiscount(): ...   // behavior pinned
test_pricesExpiredCouponAsZero(): ...

function price(order): ...  // now safe to simplify / speed up
```

---

## Review checklist

- [ ] Is feared code covered by behavior tests before I touch it?
- [ ] Do tests allow a different implementation strategy?
- [ ] After green, did I actually do the cleanup/speedup?

---

## Related standards

- UNIT TESTS 01 The Three Laws of TDD
- UNIT TESTS 02 Keep Your Tests Clean
- CLASSES 05 Prefactoring

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
