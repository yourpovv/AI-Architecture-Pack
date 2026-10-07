# 02. Feature Envy

> **Rule:** When a method depends entirely on another object's data, move the method to that object.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

A pure-looking `total(invoice)` with three arguments all drawn from the same `Invoice` is telling you where it belongs. Passing the whole invoice instead only hides the envy — the cost appears when `Invoice` gains a field and every caller must thread it through.

When a function takes most of its arguments from another object, it wants to be part of that object. Move it there: arguments disappear, internals stay hidden, and the caller simply asks for what is due without knowing the details.

---

## Rules

- If 2+ arguments (or most reads) come from one object, move the method to that object.
- Do not fix envy by passing the whole donor object and keeping the method where it was.
- After the move, callers use behavior (`invoice.totalDue()`), not field access.
- A growing argument list from one source is envy — relocate, don't bundle into a bag.

---

## Bad vs good

### Bad
```text
function totalDue(subtotal, discount, tax):  // all from invoice
  return (subtotal - discount) * (1 + tax)

totalDue(invoice.subtotal, invoice.discount, invoice.tax)
```

### Good
```text
class Invoice:
  totalDue():
    return (subtotal - discount) * (1 + tax)

invoice.totalDue()
```

---

## Review checklist

- [ ] Do most arguments originate from one other object?
- [ ] Would a new field on that object ripple through callers?
- [ ] Does the caller know internals it should not?

---

## Related standards

- 21 Expose behavior, not data
- 28 Pairs and triads
- 23 Low argument count

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
