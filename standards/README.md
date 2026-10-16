# standards/ index

The universal layer. No file here names a framework, a vendor, a language, or a specific
project, so every file applies to every repo.

| Path | What it is | How to load it |
|---|---|---|
| **[Clean-Code/](./Clean-Code/README.md)** | 60 lesson standards (41 flat + 19 grouped), one rule per file. The mandatory craft baseline | Open the one lesson file the task needs. Never load the whole folder |
| **[Principles.md](./Principles.md)** | SOLID, Clean Architecture, testing, concurrency, security, performance, and team practice. Agrees with every lesson and links the lesson for each craft rule | Open one section at a time. The file is long on purpose |

## Which one answers the question

| Question | Go to |
|---|---|
| Is this name any good? Should this be a comment? Is this function doing too much? How should this fail? | `Clean-Code/` |
| Should this be an interface? Which way should this dependency point? How do I make this concurrent? What should I log? | `Principles.md` |

Craft lives in `Clean-Code/`. Architecture, concurrency, security, and operations live in
`Principles.md`. Where they overlap, `Principles.md` summarizes the lesson and links it. If a
summary drifts, fix `Principles.md` to match the lesson.

## Authority order

1. The project's **`AGENTS.md`**, only for an exception it names explicitly
2. **`Clean-Code/`**
3. **`../skills/engineering/uncle-bob/SKILL.md`**
4. Other `../skills/*` and **`Principles.md`**

When two rules disagree, follow the higher one. Without a fixed order, an agent picks a
different winner every session.
