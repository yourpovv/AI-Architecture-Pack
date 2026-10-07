# 01. Single Responsibility Principle

> **Rule:** Every class has one job. Every method serves that job. A second job means a second class.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

A **job** is the one thing a class is in charge of. Method lists reveal violations fast: when methods fall into distinct groups, each group is a different job fighting for the same class.

An `Invoice` that calculates totals, builds emails, and sends them changes for tax rules *and* for delivery reminders — two very different reasons, one class. Split so each new requirement lands in exactly one class, where a change to one job cannot break the other.

When you write a class, ask what would make you change it. More than one answer means more than one class.

---

## Rules

- One class owns one job; every method must serve it.
- If methods cluster into distinct groups, split each group into its own class.
- A change to tax/pricing must never force an edit to email/delivery code, and vice versa.
- Name each split class with a single noun phrase that covers *all* of its methods.

---

## Bad vs good

### Bad
```text
class Invoice:
  calculateTotal()   // pricing job
  buildEmail()       // messaging job
  sendEmail()        // delivery job
```

### Good
```text
class Invoice:
  calculateTotal()

class InvoiceMailer:
  buildEmail(invoice)
  sendEmail(invoice)
```

---

## Review checklist

- [ ] Can I state the class's job in one phrase without "and"?
- [ ] Do all methods serve that job?
- [ ] Does one requirement touch only one class?

---

## Related standards

- SOLID 02 A Reason to Change
- CLASSES 01 Naming Pressure
- 15 One thing / story

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
