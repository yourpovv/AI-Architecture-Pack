# standards/ index

This is your universal layer. It names no framework. It names no vendor. It names none of your projects.
That silence is deliberate. You can use every file here in every repo you own. That sameness keeps your work honest. Why does that matter. Because your standards should not shift when you change folders.

| Path | What it is | How to load it |
|---|---|---|
| **[Clean-Code/](./Clean-Code/README.md)** | 60 lesson standards (41 flat + 19 grouped), one rule per file. This is your mandatory craft baseline. You answer to it every day | Open the one lesson file your task needs. Keep the rest closed. Your attention belongs on your code, not on browsing rules |
| **[Principles.md](./Principles.md)** | SOLID, Clean Architecture, testing, concurrency, security, and the philosophy that holds them together. You read it when you must shape your design | Load one section at a time. It runs long on purpose. Read it all at once and you burn the budget you need for your code |

## Which one answers your question

| Question | Go to |
|---|---|
| Is this name any good? Should this be a comment? Is this function doing too much? | `Clean-Code/` |
| Should this be an interface? How do I test this? Is this dependency pointing the right way? | `Principles.md` |

Craft lives in `Clean-Code/`. Architecture and testing live in `Principles.md`. Where
the two overlap, `Clean-Code/` wins. You fix `Principles.md` to match it. You never bend the rule to fit the handbook.

## Authority order

1. Project **`AGENTS.md`**. It wins only when it names an explicit exception for you
2. **`Clean-Code/`**
3. **`../skills/engineering/uncle-bob/SKILL.md`**
4. Other `../skills/*` and **`Principles.md`**

That order exists for a reason. When two rules disagree, you obey the higher one.
You do not invent your own order. That discipline is what protects your team. Can your team trust you if you pick and choose. No.
