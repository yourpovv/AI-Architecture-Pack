---
name: coding-create-readme
description: >
  Write or rewrite a project README from the actual tree, never from a generic
  template. Stack-agnostic discovery process. Trigger when asked to create,
  rewrite, or fix onboarding docs. Verify every claim against opened files.
---

# Create-Readme (Universal)

Write as the new senior engineer walking into the repo. The README is what teammates read
before they touch the code; a wrong, incomplete, or generic one costs them a day or breaks
something.

**Rules:**

- Do not produce a generic "professional GitHub README" template.
- Do not guess. Read the tree before writing any final README content.
- If a claim cannot be verified in a file you opened, do not state it as fact. Leave a clearly
  marked TODO instead.
- Take audience and tone from the project (`AGENTS.md`, the existing README, whether the repo
  is private). By default, write for a teammate who will run the project, not a marketing page.

---

## Discovery checklist (do this first)

Open and use what exists:

1. Top-level layout, package manifests, workspace files
2. Entry configs (env examples, server config examples, deploy files)
3. Dependency and framework pins (lockfiles, manifests, version fields)
4. Trackers if present (`ISSUES.md`, `IDEAS.md`, `TODO.md`, issue templates)
5. The agent contract if present (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`), and follow it
6. SQL and migrations, schema folders, seed scripts
7. CI config, which gives the real verify commands

Keep a list of every path you opened; it goes in the final response.

---

## Recommended README structure

Adapt the sections to what the repo needs and drop the ones that do not apply. Never invent
features.

1. **What this is:** one plain paragraph stating the product type and who the doc is for. No
   marketing adjectives.
2. **Stack and dependencies:** frameworks and critical libraries, with versions read from
   manifests. Say what you could not pin.
3. **Repo structure:** top-level folders, one line each. If a folder name misleads, say what
   is actually inside.
4. **Setup:** verified steps: tooling versions, config files and key names (never secret
   values), databases and migrations, build and run commands from the project.
5. **Notable systems:** non-obvious flows a new teammate would otherwise reverse-engineer
   (custom events, auth, data ownership). Only what the code shows.
6. **Known issues and open work:** point at the trackers rather than copying long issue text.
7. **Conventions:** only patterns confirmed across several modules. If there are none, say the
   repo does not enforce one yet.
8. **Contributing and workflow:** only if the team has one (branch rules, review prompts). Skip
   open-source boilerplate on private repos unless they already use it.

---

## Leave out (unless the repo already requires them)

- Badge spam, and empty license sections in private repos with no license file
- Install steps for tools the project does not use
- Feature lists inferred from folder names
- Secrets, tokens, connection strings, or real keys
- Self-referential "how this README was written" sections

---

## Style

Prose rules live in `../coding-prose/SKILL.md`; load it before writing final README
content. `prompts/scaffolds/Readme-Voice.md` owns tone and section layout by project type.

Two rules matter most here: no claim survives that was not verified against an opened file,
and no sentence restates what a linked file already shows.

Follow any language rules in `AGENTS.md`.

---

## Final response to the human

After writing `README.md`:

1. List every folder and file you opened
2. List the claims you left as TODO because the code did not settle them
3. Confirm that no secrets were copied into the README
