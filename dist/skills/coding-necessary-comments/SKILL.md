---
name: coding-necessary-comments
description: >
  Robert C. Martin's "Necessary Comments" rule: comments are a last resort, not
  a default. Use when writing, reviewing, or stripping comments; when deciding
  whether an explanation belongs in prose or in a rename/extraction; or when a
  reviewer flags a comment as narration, noise, or non-local information.
  Pairs with ../coding-craft/SKILL.md (comment quality) and ../coding-uncle-bob/SKILL.md (Clean
  Code methodology). Language-agnostic.
---

# Necessary Comments (Universal)

Background reading: Robert C. Martin,
["Necessary Comments"](https://blog.cleancoder.com/uncle-bob/2017/02/23/NecessaryComments.html),
and the comments section of `../coding-standards/references/principles.md` (section 3).

**Authority:** comment craft is defined by `../coding-standards/references/clean-code/` lessons **05 to 10, 17, 19,
33, 38, 41** (protective comments in **08**). If this skill and those lessons disagree, follow
the lesson.

**The default is zero comments.** A comment usually means the code failed to explain itself.
Before writing one, try a rename, an extraction, or a smaller function. Most of the time one of
those works and the comment becomes unnecessary.

---

## 1. When a comment is necessary

A comment earns its place only when the code cannot express the information, however it is
restructured. That leaves a short list:

1. **The algorithm's shape is not visible in the code.** A throttle, debounce, or backoff
   algorithm's behavior across timed scenarios is easier to read from a small timing diagram
   than to infer from the conditionals. The diagram is the necessary part, not prose that
   restates the `if` statements.
2. **A decision that looks wrong without its rationale.** An inverted condition, a skipped
   validation, or a magic offset that a future reader would "fix" back into a bug needs one
   line saying why.
3. **A warning about consequences.** `// allocates; keep off the hot path`,
   `// deliberately not thread-safe, see #142`. The cost is not visible at the call site.
4. **Best-effort failure handling (rare).** An empty catch is forbidden (Clean-Code 34). If the
   work is truly best-effort, log the failure with context and add a short why-comment, or
   rethrow. Prefer a design that needs no catch at all.
5. **Public API docs.** Javadoc, TSDoc, rustdoc, or equivalent on exported symbols
   (Clean-Code 41): what, inputs, outputs, failures, example. Not noise (19), but they must not
   narrate the private implementation.
6. **Legal notices.** Required license or copyright headers (Clean-Code 07, 41).

If a comment does not fit one of those, it almost certainly does not survive. Say it in code
instead.

---

## 2. When a comment is not necessary (rename or extract instead)

- **It restates the next line.** `// increment i` above `i++`. Delete it.
- **It explains what a poorly named thing does.** Rename the thing. A comment saying a lock
  "protects the system" means the protected subsystem deserves a name.
- **It narrates a well-known idiom.** Recovering a poisoned mutex, guarding a null, wrapping a
  third-party error: a competent reader of the language recognizes these on sight. If the
  idiom needs teaching, that belongs in a team wiki page, not on every occurrence.
- **It cites something the reader cannot open.** A comparison to another project's file, an
  old ticket number with no link, an author's name. If the reference is not reachable from the
  repo, it is trivia, not evidence (non-local information, Clean-Code 09).
- **It is a banner or section label.** `// ==== Helpers ====` above functions that already read
  as a group. A blank line does that job (Clean-Code 38).
- **It duplicates a doc comment one function away.** State a rule once, at the layer that owns
  it, not at every call site.

---

## 3. Applying this in a review

1. Read every comment in scope. For each, identify which case in section 1 it satisfies. If
   none, it is a deletion candidate.
2. Before deleting, check whether removing it would leave the reader confused about *why*. A
   missing why is a real finding. A missing *what* means the code needs a better name, not the
   comment back.
3. Do not push zero tolerance past the point of usefulness. A necessary comment that is a
   little long gets trimmed, not deleted: if everything after the second sentence restates
   code, cut from there.
4. API docs on exported symbols are exempt from "restates the code" at the signature level
   (parameters, return, throws), but not when they narrate the body.

---

## 4. Quick reference

| Keep | Cut |
|---|---|
| A timing or algorithm diagram the code cannot show | Restating the next line |
| Why a line that looks like a bug is correct | Explaining a poorly named symbol (rename instead) |
| A consequence warning (performance, thread safety, hot path) | Narrating a well-known language idiom |
| A best-effort catch that logs with context, with its why | Citing a repo or ticket the reader cannot open |
| Signature-level docs on exported symbols | A section banner or position marker |
| A required legal notice | A duplicate of a doc comment elsewhere |
