# languages/ index

Pick **one** file per project, the one you are actually writing. These sit on top of
`../standards/`, they do not replace it. The standards tell you what good code is. These show you what good code looks like in your language.

| File | Use it for |
|---|---|
| **[TypeScript.md](./TypeScript.md)** | Web apps, desktop frontends, CLI tooling. The default for most work here |
| **[Bun-Node.md](./Bun-Node.md)** | Server-side JS/TS: routes, services, database layer, middleware, HTTP clients |
| **[Go.md](./Go.md)** | Concurrent services and daemons. Packages, interfaces, goroutine discipline |
| **[Python.md](./Python.md)** | Data work, ML, scripting. Modules, type hints, packaging |
| **[Cpp.md](./Cpp.md)** | Native and performance work. Memory and resource management, threading, hot reload |
| **[Luau.md](./Luau.md)** | Roblox only |

## What is in every file

Project Structure, Principles, Error Handling, Testing, Configuration, a Summary, and a
**Project Prompt** with Setup, Deliverables, Validation, and Pre-Delivery steps you hand
straight to your agent.

Each one opens with an **Agent load** blockquote naming the sections you read first. That
line is the point of the whole folder. A language guide is thousands of tokens. When your
agent swallows all of it, you have less room left for your actual code. Why pay for tokens you do not need?

## Pairing

- Building a desktop app or a React frontend? You add one file from [`../frameworks/`](../frameworks/README.md).
- Reviewing rather than writing? You load [`../skills/review/audit/SKILL.md`](../skills/review/audit/SKILL.md) first.
- Unsure what to build with at all? You start with [`../STACK.md`](../STACK.md). It walks you through the decision.

## Adding a language

1. You copy the closest existing file and you keep the section order.
2. You keep the required sections listed above, including the Project Prompt.
3. You copy the **Agent load** blockquote from any sibling and you edit it to match.
4. Discover verify commands from the project. Never hard-code a toolchain that only exists
   on your machine. Your team must be able to run what you write.
5. You add a row to the table above.
