# 01. The Three Laws of TDD

> **Rule:** No production code without a failing test. Write just enough test to fail, then just enough code to pass — and no more.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

Code-first invites speculation: you build for cases nobody requested, untested by construction. Test-first flips the order so every line exists because a test demanded it. The "lots of stop" is the discipline: stop writing the test once it fails (even does-not-compile counts), stop writing production once it passes — `yes to everyone` is correct until the second test (non-author) proves otherwise.

Coverage is then a byproduct, not a phase. Tests stay one step ahead of production, and the design stays minimal because speculative branches never get written.

---

## Rules

- Failing test first — red (including compile failure) before any production edit.
- Smallest test that fails, then smallest production change that passes — stop at green.
- No extra branches, options, or "while I'm here" generality without a failing test.
- Let the next test force the generalization; grow design incrementally.

---

## Bad vs good

### Bad
```text
function canEdit(user, post):
  if user.isAdmin: ...       // no test asked for admin yet
  if user.isModerator: ...   // no test asked for moderator yet
  return user.id == post.authorId
```

### Good
```text
// test 1: author can edit → return true for author
function canEdit(user, post):
  return true

// test 2: non-author cannot → minimal growth
function canEdit(user, post):
  return user.id == post.authorId
```

---

## Review checklist

- [ ] Does every production branch trace to a failing-first test?
- [ ] Did I stop at green instead of adding "likely" cases?
- [ ] Is untested speculative code absent?

---

## Related standards

- UNIT TESTS 05 One Concept Per Test
- UNIT TESTS 04 Writing Clean Tests
- UNIT TESTS 03 Tests Enable the -ilities

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
