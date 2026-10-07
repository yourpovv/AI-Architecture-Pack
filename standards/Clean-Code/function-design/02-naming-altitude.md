# 02. Naming Altitude

> **Rule:** Do not name a function after what the code does. Name it after why you would call it — one abstraction level above the body.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

A name can be clear, searchable, and accurate — and still wrong, because it restates the comparison inside instead of the concept it serves. Implementation names lock callers to *how*: every call site reads as mechanics, and any change of approach forces a rename or a lie.

Concept names free both sides. Call sites read as intent, and the body can evolve (different comparison, cache, rule table) without touching callers. Keep the name one level above the code: describe what it achieves and hide how it is done.

---

## Rules

- The name states the caller's intent, never the internal comparison/loop/format.
- If the body changed strategy but the purpose held, the name must still fit.
- Call sites must read as product language, not machine steps.
- When tempted to encode the "how", lift one level until the "why" appears.

---

## Bad vs good

### Bad
```text
if compareExpiryToToday(card.expiry, today):  // restates the comparison
  ...
```

### Good
```text
if isExpired(card, today):  // intent; free to change how expiry is computed
  ...
```

---

## Review checklist

- [ ] Does the name survive a change of implementation strategy?
- [ ] Do call sites read as intent rather than mechanics?
- [ ] Is the name a concept, not a paraphrase of the body?

---

## Related standards

- 06 Intention-revealing names
- 04 Clarity is king
- 17 Why, not how

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
