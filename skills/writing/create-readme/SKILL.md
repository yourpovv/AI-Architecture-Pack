---
name: create-readme
description: >
  Write or rewrite a project README from the actual tree, never from a generic
  template. Stack-agnostic discovery process. Trigger when asked to create,
  rewrite, or fix onboarding docs. Verify every claim against opened files.
---

# Create-Readme (Universal)

Listen. You are the new senior walking into this repo. Your README is what
your teammates read before they touch your code. If you leave it wrong,
incomplete, or generic, they will break something or waste a day.

**Rules:**

- Do not hand your team a generic "professional GitHub README" template.
- Do not guess. You read the tree before you write a line of final README content.
- If you cannot verify a claim in files you opened, you do not state it as fact.
  You leave a clearly marked TODO for your reader instead.
- You take audience and tone from the project (`AGENTS.md`, existing README, whether
  the repo is private). By default you write for a teammate who will run this, not a marketing page.

---

## Discovery checklist (do this first)

You open and use what exists:

1. Top-level layout, package manifests, workspace files you actually read
2. Entry configs you check (env examples, server config examples, deploy files)
3. Dependency and framework pins you confirm (lockfiles, manifests, version fields)
4. Trackers if present (`ISSUES.md`, `IDEAS.md`, `TODO.md`, issue templates) — you read them
5. Agent contract if present (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`) — you follow it
6. SQL/migrations, schema folders, seed scripts you inspect
7. CI config, because it gives you the real verify commands

You list every path you opened when you finish the job.

---

## Recommended README structure

You adapt sections to what your repo actually needs. You drop sections that do not apply.
You never invent features.

1. **What this is**, one plain paragraph from you. You state the product type and who the doc is for. No marketing adjectives.
2. **Stack and dependencies**, frameworks and critical libraries with versions you read from manifests. You say what you could not pin.
3. **Repo structure**, top-level folders, one line each from you. If a name misleads, you say what is actually inside.
4. **Setup**, real steps you verified: tooling versions, config files and **key names** (not secret values), databases/migrations, build/run commands from the project.
5. **Notable systems**, non-obvious flows your new teammate would otherwise reverse-engineer (custom events, auth, data ownership). Only what the code shows you.
6. **Known issues / open work**, you point at trackers; you do not duplicate long issue text if trackers exist.
7. **Conventions**, only patterns you confirmed across multiple modules. If you found none, you say the repo does not enforce one yet.
8. **Contributing / workflow**, only if your team has one (branch rules, review prompts, private vs public). You skip open-source boilerplate on private repos unless they use it.

---

## Do not include (unless the repo already requires them)

- Badge spam, empty license sections for private repos with no license file — you leave them out
- Install steps for tools your project does not use — you leave them out
- Feature lists you inferred from folder names — you leave them out
- Secrets, tokens, connection strings, or real keys — you never write them down
- Self-referential "how this README was written" meta sections — you leave them out 

---

## Style

Prose rules live in `skills/writing/prose/SKILL.md`. You load it before you write final README
content. `prompts/scaffolds/Readme-Voice.md` owns tone and section layout by project type.

Two rules matter most here: you let no claim survive that you did not verify against an opened
file, and you write no sentence that restates what a linked file already shows.

You match project language rules in `AGENTS.md` when present.

---

## Final response to the human

After you write `README.md`:

1. You list every folder/file you opened
2. You list claims you left as TODO because the code did not decide them
3. You confirm you copied no secrets into the README 
