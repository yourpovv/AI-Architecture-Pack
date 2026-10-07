# 01. Function Contexts

> **Rule:** Read `private` as a promise about change: public is the stable what, private is the volatile how. Do not leave helpers public for convenience.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Every context groups functions with the data they share. The public surface should describe *what* at a higher level; private internals handle *how* below. That boundary is a decision about what you expect to hold still versus keep moving.

Leave a general `send` helper public and distant modules reach straight for it whenever the interface lacks something. When the delivery format changes, every external caller that depended on *how* emails are sent must change too. Make it private and force those use cases inside as dedicated operations — the next delivery change stays contained in one context. The boundary you draw is your intent.

---

## Rules

- Public = stable concepts callers may depend on; private = details free to move.
- Never expose a general helper publicly just to unblock one caller — add a dedicated public operation instead.
- When an external change ripples through callers, the boundary was too wide — narrow it.
- Review boundaries on every change: what held still, what moved, and did the line match?

---

## Bad vs good

### Bad
```text
class OrderMailer:
  send(to, subject, body)  // public "how" — 12 modules call it directly
```

### Good
```text
class OrderMailer:
  sendConfirmation(order)  // public "what"
  sendRefund(order)         // public "what"
  private send(to, subject, body)  // volatile "how", free to change
```

---

## Review checklist

- [ ] Is every public member a stable concept, not a convenience helper?
- [ ] Could I change the delivery/format mechanism without touching callers?
- [ ] Are external modules reaching past the "what" into the "how"?

---

## Related standards

- 21 Expose behavior, not data
- 32 Law of Demeter
- 29 Objects vs data structures

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
