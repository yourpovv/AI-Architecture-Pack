# standards/ index

This is your universal layer. It names no framework. It names no vendor. It names none of your projects.
That is deliberate. You can apply every file here to every repo you own. That stability keeps your craft honest.

| Path | What it is | How to load it |
|---|---|---|
| **[Clean-Code/](./Clean-Code/README.md)** | 60 lesson standards (41 flat + 19 grouped), one rule per file. This is your mandatory craft baseline. You hold yourself to it | Open the single lesson file that matches your task. Never open the whole folder. You save your attention for your code |
| **[Principles.md](./Principles.md)** | SOLID, Clean Architecture, testing, concurrency, security, and the philosophy that holds them together. You use it to guide your design | Load one section at a time. It is long on purpose. Loading all of it wastes the budget you need for your code |

## Which one answers your question

| Question | Go to |
|---|---|
| Is this name any good? Should this be a comment? Is this function doing too much? | `Clean-Code/` |
| Should this be an interface? How do I test this? Is this dependency pointing the right way? | `Principles.md` |

Craft belongs to `Clean-Code/`. Architecture and testing belong to `Principles.md`. Where
the two overlap, `Clean-Code/` wins. You correct `Principles.md` toward it. You do not bend the rule to fit the handbook.

## Authority order

1. Project **`AGENTS.md`**. It outranks only for an exception it names explicitly for you
2. **`Clean-Code/`**
3. **`../skills/engineering/uncle-bob/SKILL.md`**
4. Other `../skills/*` and **`Principles.md`**

That order exists for a reason. When you face two pieces of contradictory advice, you follow the higher rule.
You do not invent a preference. That discipline protects your team.
