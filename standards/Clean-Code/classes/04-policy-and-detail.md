# 04. Policy and Detail

> **Rule:** A module either declares workflow steps and delegates, or implements one step's detail. Mixing policy with detail violates SRP — move the detail out.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

A checkout module with four clean delegating steps plus a block of pricing math in the middle has two reasons to change: policy (reserve stock first, deduct after payment) and detail (shipping rates rose). Both edits land in the same file, so one concern's churn risks the other.

Keep a single level of decision per module. The workflow module names the steps and delegates every one; a separate class owns the math. Then a policy change touches only the workflow, and a detail change touches only the worker.

---

## Rules

- A workflow module delegates all steps — no inline calculations, formatting, or I/O detail.
- A detail class implements one step — it never reorders the workflow.
- When a file changes for both policy and detail reasons, extract the detail.
- For every file, ask: "declaring or doing?" If both, move the detail out.

---

## Bad vs good

### Bad
```text
function checkout(order):
  validate(order)
  reserveStock(order)
  total = order.lines.sum(...) * rateTable.lookup(...)  // detail inline
  charge(order, total)
```

### Good
```text
function checkout(order):
  validate(order)
  reserveStock(order)
  charge(order, pricing.total(order))

class Pricing:
  total(order): ...
```

---

## Review checklist

- [ ] Does this module both order steps and implement one of them?
- [ ] Would a policy change and a rate change collide in this file?
- [ ] Is every step a delegation to a named collaborator?

---

## Related standards

- SOLID 01 Single Responsibility Principle
- 27 One abstraction level
- 15 One thing

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
