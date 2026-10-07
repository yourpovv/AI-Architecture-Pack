# 03. Name Length

> **Rule:** Narrow scope forces longer, more specific function names; wide scope earns short, general ones. Count the neighbours before debating length.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Variables follow scope the obvious way: a two-line local can be `i`; a global needs description to avoid collisions. Functions run backwards. Eight private helpers in one importer, all doing subtle variations of file work, need extra words just to tell each other apart — that narrow, crowded context demands specificity.

Push scope to the whole codebase and functions become distinct general operations called from everywhere: a single verb says everything, and short keeps every call site clean. Length is not a virtue or a smell by itself — it is a function of how many neighbours compete for the same idea.

---

## Rules

- Crowded private context → longer, distinguishing names (`importCsvRows`, not `import`).
- Public / widely-called operations → shortest verb that stays unambiguous (`parse`, `charge`).
- Never shorten a narrow helper until it collides with its siblings; never pad a global API with context callers already have.
- Judge a name against its scope, not an absolute length rule.

---

## Bad vs good

### Bad
```text
class Importer:  // 8 file-operation helpers, all vague
  load() / read() / open() / fetch() / get() / parse() / handle() / run()
```

### Good
```text
class Importer:
  importCsvRows() / importJsonRows() / resolveEncoding()

// wide scope, distinct operation — short is clean
parse(document)
charge(order)
```

---

## Review checklist

- [ ] How many neighbours share this context and job family?
- [ ] Would a shorter name collide or a longer name add noise at call sites?
- [ ] Does specificity grow as scope narrows?

---

## Related standards

- 06 Intention-revealing names
- 30 Searchable names
- 36 Honest naming

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
