# 01. Naming Pressure

> **Rule:** If you have to argue a class name — or join jobs with "and" — the design is unfinished. Split until one noun phrase fits.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

`Manager`, `Processor`, `Handler` are catch-all words you reach for when a class lacks a single responsibility. An `OrderManager` that prices orders *and* talks to the payment gateway cannot be rescued by renaming: `OrderPricing` is a lie while it still charges cards and issues refunds.

The test is grammatical: an honest name needs no "and". If making the name honest forces you to list both jobs, split where the "and" sits. The class name is a measurement of the code behind it — when both halves get obvious, honest names, the design is done.

---

## Rules

- Ban `Manager` / `Processor` / `Handler` as a way to paper over two jobs.
- Try the honest rename first; if it needs "and", split instead of debating the label.
- Split at the "and": each resulting class gets a single-noun-phrase name.
- Never keep a lying name — a pricing name must not charge cards.

---

## Bad vs good

### Bad
```text
class OrderManager:       // prices AND charges
  priceOrder()
  chargeCard()
  issueRefund()

class OrderPricing:       // renamed, still charges — a lie
  priceOrder()
  chargeCard()
```

### Good
```text
class OrderPricer:
  priceOrder()

class PaymentGateway:
  chargeCard()
  issueRefund()
```

---

## Review checklist

- [ ] Can I name this class without "and"?
- [ ] Does the name contain Manager / Processor / Handler to hide two jobs?
- [ ] After the split, is each name obvious and honest?

---

## Related standards

- SOLID 01 Single Responsibility Principle
- SOLID 02 A Reason to Change
- 06 Intention-revealing names

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
