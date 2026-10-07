# 01. Wrap Third-Party Code

> **Rule:** You cannot stop a library from changing, but you decide how much code it touches. Call vendors through one wrapper you own.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Calling the payment SDK directly where the charge happens works — until a major version removes that call and the build breaks in every file that copied the pattern. One search reveals how deep the vendor reaches.

A thin wrapper (`charge(order)`, `refund(payment)`) in your own words hides SDK details in one place. Checkout calls your class, not their docs. When the next breaking change lands, only the wrapper updates. Third-party code sits at a boundary; wrap it and you depend on code you own, not code you do not.

Differs from 31: 31 owns *error types*; this owns the *call surface* so version churn has one edit point.

---

## Rules

- One wrapper per external system; domain code never imports the vendor SDK directly.
- Wrapper API uses your domain words, not the vendor's call/field names.
- Vendor upgrades, renames, and signature changes are fixed in the wrapper only.
- Count direct SDK imports in review — the goal trends toward one file.

---

## Bad vs good

### Bad
```text
// in 14 files:
paymentsdk.charge(amountCents, cardToken)
```

### Good
```text
class Payments:
  charge(order)   // hides cents/token/SDK call inside
  refund(payment)

checkout calls payments.charge(order)
```

---

## Review checklist

- [ ] How many files import the vendor SDK?
- [ ] Could a major-version rename be fixed in one module?
- [ ] Does the wrapper speak domain language, not vendor language?

---

## Related standards

- 31 Wrap third-party APIs
- BOUNDARIES 02 The Adapter Pattern
- 14 DRY

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
