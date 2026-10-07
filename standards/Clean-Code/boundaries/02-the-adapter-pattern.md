# 02. The Adapter Pattern

> **Rule:** Design the interface your code needs, build against it today with a fake, and translate the real provider behind one adapter. Never let provider shapes leak into finished code.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

When the provider is not ready, do not stall: write the interface you wish you had, shaped by your code's needs (`charge(amount, card) → receipt`). Checkout takes it as an argument; a fake approving every charge lets you ship and test *your* logic, not theirs.

When the real provider arrives with mismatched units (cents vs dollars, token vs card), resolve it in exactly one place — an adapter that implements your interface and calls theirs. The adapter is a translator. Checkout never changes, and swapping providers later means swapping one class.

---

## Rules

- Derive the interface from caller needs, not from the vendor's docs.
- Build and test against a fake/stub until the real system exists.
- All unit/format/protocol mismatches live inside one adapter per provider.
- Finished domain code never imports provider types or conversions.

---

## Bad vs good

### Bad
```text
function checkout(order):
  token = tokenize(order.card)            // provider shape leaked in
  paymentsdk.chargeCents(toCents(order.total), token)
```

### Good
```text
interface Charger:
  charge(amount, card) -> receipt

function checkout(order, charger: Charger):
  charger.charge(order.total, order.card)

class StripeAdapter implements Charger:  // translation lives here only
  charge(amount, card): ...
```

---

## Review checklist

- [ ] Could I swap providers without touching checkout?
- [ ] Does any domain file mention cents, tokens, or SDK types?
- [ ] Are tests running against my interface, not their service?

---

## Related standards

- BOUNDARIES 01 Wrap Third-Party Code
- 31 Wrap third-party APIs
- 12 Define contract before logic

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
