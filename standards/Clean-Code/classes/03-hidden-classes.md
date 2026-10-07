# 03. Hidden Classes

> **Rule:** Do not split long functions by length. Split where the data stops being shared — group logic that touches the same state.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

An overgrown function looks like a class: locals on top acting as fields, blocks below acting as methods. Naive extraction fails because every block reads and mutates the same locals, forcing state to be passed back and forth.

Promote shared locals to fields so blocks extract cleanly, then track which methods touch which fields. Methods sharing the same data form natural groups — pull each group into its own class. The original function is left coordinating, not computing. Shorter is easier to read; co-locating logic with its data is what makes it easy to change.

---

## Rules

- Find the data seams first: which statements share which variables/fields?
- Promote tangled locals to fields as a stepping stone, then extract by shared-data groups.
- Do not split mid-shared-state just to hit a line count — that spreads one responsibility over two owners.
- Leave the original as a thin coordinator over the extracted collaborators.

---

## Bad vs good

### Bad
```text
function process():  // split by line count — both halves still mutate a, b, c
  part1(a, b, c)
  part2(a, b, c)
```

### Good
```text
class Pricing:   // owns price fields + methods that touch them
  ...

class Shipping:  // owns address/rate fields + methods that touch them
  ...

function process():
  pricing.apply()
  shipping.apply()
```

---

## Review checklist

- [ ] Did I split by shared data, not by screen length?
- [ ] Does each extract own its data without parameter ping-pong?
- [ ] Is the leftover function only coordination?

---

## Related standards

- 26 Extract from large functions
- 29 Objects vs data structures
- 15 One thing

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
