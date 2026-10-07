# 05. Prefactoring

> **Rule:** Leave working code alone until a real requirement arrives. Then make room (behavior-preserving reshape), then add the feature.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Guessing the future bakes the wrong flexibility in. Collapsing percentage coupons into a map plus one formula looks clean — until a fixed-amount coupon arrives and forces a branching condition onto the guess, leaving the code further from simple than before.

Wait for the requirement. If it fits existing logic, add it directly. If it needs different logic, first reshape without changing behavior (extract the varying calculation behind its own class/delegate), *then* add the new behavior in its own class without touching what works. Real change shows where flexibility was actually needed — and usually generalizes to the next variation too.

---

## Rules

- No speculative generalization of working code.
- New requirement that fits → extend directly, minimal diff.
- New requirement that does not fit → preparatory refactor (no behavior change) → add feature → verify behavior unchanged for old cases.
- Each refactor must be justified by the requirement in hand, not the one imagined.

---

## Bad vs good

### Bad
```text
// guessed: all coupons are percentages
rates = {SAVE10: 0.10, SAVE20: 0.20}
total = price * (1 - rates[code])  // breaks when FIXED5 ($5 off) arrives
```

### Good
```text
// real requirement arrived: fixed-amount coupon
interface Discount: amountFor(price)
class PercentDiscount implements Discount: ...
class FixedDiscount implements Discount: ...  // new behavior, old code untouched
```

---

## Review checklist

- [ ] Which concrete requirement drives this refactor?
- [ ] Did I reshape without behavior change before adding the feature?
- [ ] Can the next similar variation land as a new class?

---

## Related standards

- 22 Messy first draft, then clean
- CLASSES 06 Overengineering
- 14 DRY

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
