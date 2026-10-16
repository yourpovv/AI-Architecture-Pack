---
name: craft
description: >
  Code and prose craft for maintainability and clarity. Use when reviewing naming,
  comments, structure, or written docs. Optimizes for humans who must debug and
  extend the system. Does not score "AI detection" and does not encourage fake
  inconsistency. Language-agnostic.
---

# Craft: Code and Prose Quality (Universal)

The goal is code and docs a teammate can trust at 2 a.m. Looking "less AI" to a detector is
not a goal; detectors say nothing about quality. Correctness, security, and clarity always
beat stylistic camouflage.

**Authority:** on naming and comment craft, `standards/Clean-Code/` wins (especially 04, 06,
17, 19, 20, 30, 33, 36, 39, 41). If this skill and a lesson disagree, follow the lesson.

---

## 1. Naming

- Prefer domain language over empty technical suffixes when the domain term is clear.
- Pick names that make the next line obvious. If a name needs a comment, rename it.
- Consistency within a module beats clever variety. Never introduce inconsistency on purpose
  to "look human".
- Match the conventions in `AGENTS.md` and neighboring files. Framework idioms (event
  handlers, controllers) are fine when they match the stack.

**Smell:** `handleUserDataValidationResultProcessor`
**Better:** `validateUser`, or the verb the domain already uses

**Smell:** renaming a clear, idiomatic `InventoryHandler` to something vaguer during an audit
for style points
**Better:** leave idiomatic names alone and fix real bugs

---

## 2. Comments

- Keep *why*: constraints, workarounds, invariants, hazard warnings.
- Remove *what*: narration of the next statement, step lists that restate the code.
- If removing a comment makes the code unclear, rename or extract until it is clear. Do not
  put the comment back.
- Give TODOs the blocker or ticket that prevents their removal.
- The full test for whether a comment earns its place:
  `skills/engineering/necessary-comments/SKILL.md`.

---

## 3. Structure

- Stay flat until complexity demands a layer. No repository/service/factory stack for a
  three-line operation (Clean-Code `classes/06`).
- One module, one job. A `utils/` folder of unrelated helpers is a smell.
- Keep one level of abstraction per function (Clean-Code 27).
- Asymmetry between modules is fine when their complexity differs. Symmetry for its own sake
  is not a goal, and neither is breaking symmetry on purpose.

---

## 4. Error handling and defense

- Guard boundaries and real failure modes. See `skills/engineering/errors/SKILL.md`.
- Do not wrap every line in try/catch. Do not null-check values the type system or caller
  already guarantees, except at an untrusted boundary.
- Untrusted input (network, client, user, file) is always a boundary.

---

## 5. Prose (docs, PR text, commit messages)

The full rules live in `skills/writing/prose/SKILL.md`; load it when writing or reviewing any
written material. The short version:

- Short sentences and concrete verbs. No filler adjectives or discourse glue.
- No em dash as sentence punctuation. Hyphens in compound words are fine.
- Watch for the structural tells, not just the word list: binary contrast, negative listing,
  rhetorical setup, fragments written for rhythm.
- Do not restate what a linked file already shows; link it.
- Commit and PR bodies give the why and the risk, not a narrative of every keystroke.

---

## 6. Review checklist (craft only)

- [ ] Names match the domain and local convention
- [ ] Comments explain why, not what
- [ ] No extra layers without a proven need
- [ ] Failure paths carry context; nothing is silently swallowed
- [ ] Docs and PR text would pass a "senior engineer wrote this" bar without detector games

When craft conflicts with security or correctness, craft loses.
