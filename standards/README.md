# standards/ index

This is your universal layer. It names no framework. It names no vendor. It names none of your projects.
That is why every file here applies to every repo you own.

| Path | What it is | How to load it |
|---|---|---|
| **[Clean-Code/](./Clean-Code/README.md)** | 60 lesson standards (41 flat + 19 grouped), one rule per file. Your mandatory craft baseline | Open the single lesson file that matches your task. Never the whole folder |
| **[Principles.md](./Principles.md)** | SOLID, Clean Architecture, testing, concurrency, security, and the philosophy that holds them together | Load one section at a time. It is long, and loading all of it wastes the budget you need for your code |

## Which one answers your question

| Question | Go to |
|---|---|
| Is this name any good? Should this be a comment? Is this function doing too much? | `Clean-Code/` |
| Should this be an interface? How do I test this? Is this dependency pointing the right way? | `Principles.md` |

Craft belongs to `Clean-Code/`. Architecture and testing belong to `Principles.md`. Where
the two overlap, `Clean-Code/` wins and you correct `Principles.md` toward it.

## Authority order

1. Project **`AGENTS.md`**, and only for an exception it names explicitly
2. **`Clean-Code/`**
3. **`../skills/engineering/uncle-bob/SKILL.md`**
4. Other `../skills/*` and **`Principles.md`**

That order exists for a reason. When you face two pieces of contradictory advice, you follow the rule.
You do not invent a preference.
