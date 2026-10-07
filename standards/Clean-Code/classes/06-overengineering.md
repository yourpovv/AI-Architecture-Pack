# 06. Overengineering

> **Rule:** Split when the next class earns its keep — testability, no duplication, a findable name, or room for new behavior. Past that is over-engineering.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Keep classes small, single-job, well-named, policy apart from detail — every one of those rules turns one class into many, and usually that is what we want: a feature lands as a new class without touching working code. But nothing in those rules says *stop*, and past a point the pieces add nothing.

Take a split only as far as the next class still does something for us. There are four payoffs: test one piece alone without its surroundings; remove duplication so a fix happens once; give a name to something nameless so the next person can find it; hold new behavior so existing code stays closed. Anything past that is an element you did not need — the last rule of simple design is as few elements as you can.

---

## Rules

- Before splitting, name the payoff: isolated test, dedup, discoverability, or extension seam.
- If none of the four applies, leave the code together.
- Prefer a new class for new behavior over editing working classes (open/closed).
- Count elements as cost: fewer classes that still pay rent beats more that do not.

---

## Bad vs good

### Bad
```text
// split for its own sake — three one-line wrappers, no test/dedup/name/extension win
OrderValidatorPart1 / OrderValidatorPart2 / OrderValidatorPart3
```

### Good
```text
// split that pays: pricing testable alone, email reusable, new coupon = new class
OrderPricer      // isolated tests, holds new pricing behavior
InvoiceMailer    // dedup + findable name
```

---

## Review checklist

- [ ] Which of the four payoffs does this split buy?
- [ ] Can I test, reuse, find, or extend something I could not before?
- [ ] Am I adding elements out of habit rather than need?

---

## Related standards

- SOLID 01 Single Responsibility Principle
- 14 DRY
- CLASSES 03 Hidden Classes

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
