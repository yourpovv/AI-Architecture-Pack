---
name: necessary-comments
description: >
  Robert C. Martin's "Necessary Comments" rule: comments are a last resort, not
  a default. Use when writing, reviewing, or stripping comments; when deciding
  whether an explanation belongs in prose or in a rename/extraction; or when a
  reviewer flags a comment as narration, noise, or non-local information.
  Pairs with skills/engineering/craft/SKILL.md (comment quality) and skills/engineering/uncle-bob/SKILL.md (Clean
  Code methodology). Language-agnostic.
---

# Necessary Comments (Universal)

Listen. You read Robert C. Martin, ["Necessary
Comments"](https://blog.cleancoder.com/uncle-bob/2017/02/23/NecessaryComments.html),
in full before you apply this skill to a real review, plus the comment
chapter of *Clean Code* (`standards/Principles.md` §3).

**Authority:** comment craft is defined by `standards/Clean-Code/` lessons
**05–10, 17, 19, 33, 38, 41** (and protective cases in **08**). If this skill and
those lessons disagree, **Clean-Code wins**.

**Your default is zero.** Every comment you write is a confession that your code failed to
explain itself. Before you write one, you try a rename, an extraction, or a smaller
function first. Most of the time one of those wins and your comment becomes
unnecessary.

---

## 1. The test for "necessary"

Your comment earns its place only when **your code cannot express it, no matter
how you restructure it.** Concretely, that is a short list for you:

1. **Your algorithm's shape isn't visible in your code.** A choking / debounce /
   backoff algorithm's behavior across several timed scenarios is easier for you to
   read from a small timing diagram in a comment than to infer from the
   conditionals implementing it. The diagram is the necessary part, not prose
   restating the `if` statements.
2. **A decision that looks wrong without its rationale.** When your code looks like
   an obvious "bug" to your future reader (an inverted condition, a skipped
   validation, a magic offset), you owe one line saying why, or someone will
   "fix" it back into an actual bug.
3. **A warning of consequences from you.** `// don't call on the hot path, allocates`,
   `// deliberately not thread-safe, see #142`. The cost isn't visible at your
   call site.
4. **Best-effort failure handling (rare).** Empty `catch` is **forbidden**
   for you (Clean-Code **34**). If your work is truly best-effort, you **log with context** and add a
   short why-comment — or you rethrow. You prefer design that needs no catch.
5. **Public API docs from you.** Javadoc / TSDoc / rustdoc on exported symbols (Clean-Code
   **41**): what, inputs, outputs, failures, example. Not noise (**19**). Still
   you must not narrate the private implementation.
6. **Legal notices**, required license/copyright headers you must keep (Clean-Code **07**, **41**).

If your comment doesn't fit one of those, it almost certainly doesn't survive
this skill. Ask yourself: can you say it in code instead?

---

## 2. The test for "not necessary" (rename or extract instead)

- **It restates your next line.** `// increment i` above `i++`. You delete it.
- **It explains what your poorly-named thing does.** You rename the thing. A comment
  that says "system" means the guard/lock is protecting a subsystem you
  could have named; you name it, and your comment stops earning its keep.
- **It narrates a well-known idiom you already know.** Recovering a poisoned mutex, guarding a
  null, wrapping a third-party error, anything a competent reader of your
  language already recognizes on sight, doesn't need a caption from you. If the
  *idiom* needs teaching, that belongs in your team wiki page, not a comment on every
  occurrence of it.
- **It cites something your reader can't open.** A comparison to another
  project's file, an old ticket number with no link, an author's name. If
  the reference isn't reachable from your repo, it's not evidence for your team, it's
  trivia. (`standards/Principles.md` §3.2, "non-local information".)
- **It is a banner or section label from you.** `// ==== Helpers ====` above a group of
  functions that already read as a group. Your blank line already did that
  job.
- **It duplicates a doc comment one function away.** You state a rule once, at the
  layer that owns it; you don't re-explain it at every call site.

---

## 3. Applying this to a review

1. You read every comment in scope. For each: which numbered case in §1 does it
   satisfy? If none, it is a candidate for your deletion.
2. Before you delete, you check whether removing it would leave your future reader
   confused about *why*, not *what*. "Why" gaps are real findings for you; "what"
   gaps mean your code needs a better name, not the comment back.
3. You don't swing to zero-tolerance past the point of usefulness. A necessary
   comment that's merely a little long is a trim for you, not a deletion, if the
   only content past the second sentence is restating code, you cut from there.
4. Rustdoc/TSDoc/Javadoc on your exported symbols is exempt from "restates the
   code" scrutiny at the *signature* level (params, return, throws) but not
   from narrating the *body*.

---

## 4. Quick reference

| Keep | Cut |
|---|---|
| Timing/algorithm diagram your code can't show | Restates your next line |
| Why your "looks like a bug" line is correct | Explains your poorly-named symbol (rename instead) |
| Consequence warning for your team (perf, thread-safety, hot path) | Narrates a well-known language idiom |
| Justified empty/swallowed branch you logged | Cites another repo/project your reader can't open |
| Exported-symbol API doc you own (signature-level) | Section-banner / position marker |
| Legal notice you must keep | Duplicate of a doc comment elsewhere |
