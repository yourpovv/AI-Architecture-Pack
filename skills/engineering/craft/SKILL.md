---
name: craft
description: >
  Code and prose craft for maintainability and clarity. Use when reviewing naming,
  comments, structure, or written docs. Optimizes for humans who must debug and
  extend the system. Does not score "AI detection" and does not encourage fake
  inconsistency. Language-agnostic.
---

# Craft, Code and Prose Quality (Universal)

Listen. You write code and docs your teammate can trust at 2 a.m.
That is the goal. What is not the goal? Looking "less AI" on a detector.
Detectors tell you nothing about quality. Your correctness, your security,
and your clarity always beat stylistic camouflage.

**Authority:** on naming and comment craft you defer to `standards/Clean-Code/` (especially
04, 06, 17, 19, 20, 30, 33, 36, 39, 41). If this skill and those lessons disagree,
**Clean-Code wins**.

---

## 1. Naming

- You choose domain language over empty CS suffixes when your domain term is clear.
- You pick names that make your next line obvious. If you need a comment to explain the
  name, you rename.
- You keep consistency within your module. It beats clever variety. You do not introduce intentional
  inconsistency to "look human."
- You match the project conventions you find in `AGENTS.md` and neighboring files.
  Framework idioms (e.g. event handlers, controllers) are fine when they match your stack.

**Smell:** `handleUserDataValidationResultProcessor`
**Better:** `validateUser` or the verb your domain already uses

**Smell:** you renaming a clear `InventoryHandler` to something vague mid-audit for style points
**Better:** you leave idiomatic names; you fix real bugs 

---

## 2. Comments

- You keep *why*: constraints, workarounds, invariants, hazard warnings.
- You remove *what*: narration of the next statement, step lists that restate your code.
- If removing a comment makes your code unclear, you rename symbols; you do not put the comment back.
- You give TODOs a condition or owner context when you can: what blocks removal.
- Full test for when a comment earns its keep: `skills/engineering/necessary-comments/SKILL.md`.

---

## 3. Structure

- You stay flat until your complexity demands a layer. You do not add repository/service/factory
  stacks for a three-line operation.
- One module, one job. Ask yourself: is your dumping-ground `utils/` with unrelated helpers a smell? It is.
- You keep the same abstraction level inside your function (Clean Code).
- Asymmetry across your modules is fine when complexity differs. Symmetry for its own
  sake is not your goal, and breaking symmetry on purpose is not your goal either.

---

## 4. Error handling and defense

- You guard boundaries and real failure modes. See `skills/engineering/errors/SKILL.md`.
- You do not wrap every line in try/catch. You do not null-check values your type system
  or caller already guarantees, unless you stand at an untrusted boundary.
- Untrusted input (network, client, user, file) is always a boundary for you.

---

## 5. Prose (docs, PR text, commit messages)

Full rules live in `skills/writing/prose/SKILL.md`. You load it when you write or review any
written material. The short version for you:

- You write short sentences. Concrete verbs. No filler adjectives or discourse glue.
- You never use an em dash as punctuation. Ordinary hyphens in compound words are fine.
- You watch the structural tells, not just the word list: binary contrast, negative listing,
  rhetorical setup, fragments written for rhythm.
- You do not restate what a linked file already shows; you link it.
- Commit/PR body: you give why and risk, not a narrative of every keystroke.

---

## 6. Review checklist (craft only)

- [ ] Do your names match domain and local convention
- [ ] Are your comments why-only
- [ ] Did you add no extra layers without a proven need
- [ ] Do your failure paths have context; no silent swallow
- [ ] Would your docs/PR text pass a "senior engineer wrote this" bar without detector games

If your craft conflicts with security or correctness, your craft loses.
