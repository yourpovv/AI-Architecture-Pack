# 02. A Reason to Change

> **Rule:** A reason to change is an actor — a group of people who can demand a change. One actor, one class.

**Status:** mandatory coding standard for every project that pulls this Architecture pack.  
**Source:** personal clean-code lesson pack (s4.codes-aligned).  
**Stack:** language-agnostic. Translate examples to the repo's language.

---

## Principle

"One reason to change" is unusable if you count reasons in the code — every line, function, or feature grouping qualifies, and you split forever. Splitting by layer (all loading together) and by feature (product apart from reviews) both look right until you ask who decides.

Count **actors**, not code shapes. A `SignUp` class doing "just validation" still serves security (password rules, bot checks) and legal (minimum age, terms). Two actors means two reasons to change, so split. Conversely, a `Privacy` class handling consent banners *and* data requests stays whole when every demand comes from legal — one actor, one reason, one class.

Do not count reasons by looking at what a class does. Ask who can demand a change to it.

---

## Rules

- Define the actor for each responsibility: who (which group) can demand this change?
- Different actors → different classes, even if the code looks cohesive today.
- Same actor → keep together, even if the code covers multiple operations.
- Document the actor per class when the split is not obvious from functionality alone.

---

## Bad vs good

### Bad
```text
class SignUp:
  checkPasswordStrength()  // security actor
  checkBot()               // security actor
  checkMinimumAge()        // legal actor
  checkTermsAccepted()     // legal actor
```

### Good
```text
class SignUpSecurityChecks:  // actor: security
  checkPasswordStrength()
  checkBot()

class SignUpLegalChecks:     // actor: legal
  checkMinimumAge()
  checkTermsAccepted()
```

---

## Review checklist

- [ ] Have I named the actor(s) behind each method group?
- [ ] Would one actor's request force edits that risk the other actor's rules?
- [ ] Am I splitting by who decides, not by layer vs feature aesthetics?

---

## Related standards

- SOLID 01 Single Responsibility Principle
- CLASSES 01 Naming Pressure
- 16 Not everything is an object

---

## Agent notes

- Load **this file only** when the task is about this topic — do not stream the whole `Clean-Code/` folder.
- Prefer fixing structure (rename, extract, split, wrap) over adding comments or return codes.
- **Authority:** `standards/Clean-Code/` and Uncle Bob craft rules outrank `Principles.md`, `skills/engineering/errors/SKILL.md`, and other skills on these topics. Only a named exception in project `AGENTS.md` may override.
