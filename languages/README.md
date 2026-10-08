# languages/ index

You pick **one** file per project. Pick the one you are actually writing. These guides sit on top of `../standards/`. They do not replace it. The standards tell you what good code is. These files show you what that looks like in your language. You follow both. That is how you stay consistent.

| File | Use it for |
|---|---|
| **[TypeScript.md](./TypeScript.md)** | Web apps, desktop frontends, CLI tooling. The default for most work here |
| **[Bun-Node.md](./Bun-Node.md)** | Server-side JS/TS: routes, services, database layer, middleware, HTTP clients |
| **[Go.md](./Go.md)** | Concurrent services and daemons. Packages, interfaces, goroutine discipline |
| **[Python.md](./Python.md)** | Data work, ML, scripting. Modules, type hints, packaging |
| **[Cpp.md](./Cpp.md)** | Native and performance work. Memory and resource management, threading, hot reload |
| **[Luau.md](./Luau.md)** | Roblox only |

## What is in every file

Every file gives you Project Structure, Principles, Error Handling, Testing, Configuration, a Summary, and a **Project Prompt** with Setup, Deliverables, Validation, and Pre-Delivery steps you hand straight to your agent. You hand those steps over as they are. That saves you from repeating yourself.

Each file opens with an **Agent load** blockquote. It names the sections you read first. That line is the point of the whole folder. A language guide runs to thousands of tokens. When your agent swallows all of it, you have less room left for your actual code. Why pay for tokens you do not need?

## Pairing

- Building a desktop app or a React frontend? You add one file from [`../frameworks/`](../frameworks/README.md). You keep your UI rules next to your language rules.
- Reviewing rather than writing? You load [`../skills/review/audit/SKILL.md`](../skills/review/audit/SKILL.md) first. You review against a fixed scope. That keeps you honest.
- Unsure what to build with at all? You start with [`../STACK.md`](../STACK.md). It walks you through the decision. You pick your stack before you write your code.

## Adding a language

1. You copy the closest existing file and you keep the section order. You do not invent a new shape. Your team already knows this one.
2. You keep the required sections listed above, including the Project Prompt. If you drop one, you lose part of the handoff.
3. You copy the **Agent load** blockquote from any sibling and you edit it to match. You point your reader to what matters first.
4. Discover verify commands from the project. Never hard-code a toolchain that only exists
   on your machine. Your team must be able to run what you write. What good is a check your team cannot run?
5. You add a row to the table above. You keep the index honest.
