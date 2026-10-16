# Default Stack

> **Agent load: optional, personal defaults only.** Do not treat this file as required
> architecture for every project. The project's `AGENTS.md`, README, and lockfiles win. Use it
> when starting something new and the human has not named a stack.

Default services and tools. Not every project needs all of them: start with the essentials and
add the rest when a real need appears.

---

## Essentials (almost every project)

| Concern | Pick | Why |
|---|---|---|
| **Coding (AI)** | Claude Opus | Long-context reasoning that holds up in large refactors |
| **Version control** | GitHub | Ubiquitous, with good PRs and Actions |
| **Backend / DB / Auth** | Supabase | Postgres, realtime, row-level security, and auth in one service |
| **Deploy (web)** | Vercel | Zero-config for Next.js and SvelteKit, preview URLs per PR |
| **Domain** | Namecheap | Cheap renewals, usable UI |
| **DNS / edge** | Cloudflare | Generous free tier, proxy, WAF, and R2 when needed |

---

## When the product ships to real users

| Concern | Pick | Why |
|---|---|---|
| **Auth (non-Supabase)** | Clerk | Social login, organizations, and passwordless without writing them |
| **Payments** | Stripe | Checkout, subscriptions, invoicing, and an easy sandbox |
| **Transactional email** | Resend | Simple API, good developer experience, reliable delivery |
| **Uptime monitoring** | UptimeRobot | Free tier covers most side projects |
| **Error tracking** | Sentry | Source maps, releases, and performance tracing |
| **Product analytics** | PostHog | Self-host or cloud; funnels, session replay, feature flags |

---

## When the product gets AI features

| Concern | Pick | Why |
|---|---|---|
| **Vector DB** | Pinecone | Managed; the serverless tier is enough to start |
| **LLM API** | Anthropic (Claude) | Primary provider; fall back to OpenAI for niche cases |

---

## AI design and dev tooling

Install and configure these in the Claude Code environment. Most live in `.mcp.json`. Setup
syntax for all of them is at [code.claude.com/docs](https://code.claude.com/docs).

| Tool | What it does | Link |
|---|---|---|
| **Google Stitch MCP** | UI mockup generation via MCP | https://stitch.withgoogle.com/docs/mcp/setup |
| **Gemini Nano Banana 2** | Visual asset and mockup generation | https://gemini.google/overview/image-generation/ |
| **21st.dev** | Reactive and 3D component library | https://21st.dev |
| **n8n-MCP** | Knowledge of 1000+ n8n nodes for production automations | https://github.com/czlonkowski/n8n-mcp |
| **Obsidian Skills** | Markdown, canvas, and CLI skills for an Obsidian vault | https://github.com/kepano/obsidian-skills |
| **Claude-Mem** | Persistent memory compression across Claude Code sessions | https://github.com/thedotmack/claude-mem |
| **Get Shit Done (GSD)** | Spec-driven development: interview, plan, execute, verify | https://github.com/gsd-build/get-shit-done |
| **Superpowers** | Enforces TDD, debugging, code review, and planning workflows | https://github.com/obra/superpowers |
| **Awesome Claude Code** | Curated list of 200+ Claude Code tools | https://github.com/hesreallyhim/awesome-claude-code |
| **MengTo/Skills** | Skills collection worth reading before writing your own | https://github.com/MengTo/Skills |
| **Skills CLI** | Installs skills from any GitHub repo across 75+ agents; search with `npx skills find` | https://github.com/vercel-labs/skills |
| **Token Shield** | Measures real token usage from session transcripts: cache hit ratio, first-request cost, sub-agent output share | https://github.com/khalilmaaouni/token-shield |
| **Figma Dev Mode MCP** | Component and style context from the design file; pairs with `design/font-pairing` | https://www.figma.com |
| **Playwright MCP** | Screenshots and interaction for the design-build-verify loop | https://github.com/microsoft/playwright-mcp |
| **needmcp.com** | Directory for finding more MCP servers | https://needmcp.com/ |
| **toolcraft.sh** | Open-source kit for building AI design apps | https://toolcraft.sh/ |
| **Bolt templates** | Free templates to turn into sites with prompts | https://bolt.new/resources/templates |
| **Framer** | AI site builder: agents, AEO scanner, text effects, resource hub | https://www.framer.com/ |

For components, icons, illustrations, gradients, and 3D assets, see
[`design/README.md`](./design/README.md).

---

## Picking a stack for a new project

Work through the list in order and stop when you have enough.

1. **Which language fits the problem?**
   - Systems, performance, Windows native: C++ or Rust
   - Web, desktop (Tauri), CLI tooling: TypeScript
   - Data, ML, scripting: Python
   - Concurrent services: Go
   - Roblox game: Luau
2. **What is the surface?** Web app, desktop app, service, bot, game, or library.
3. **Does it need persistence?** Supabase by default, unless the domain already picked a
   database.
4. **Does it need auth?** Supabase Auth; move to Clerk if requirements get complex.
5. **Does it take money?** Stripe.
6. **Does it need AI features?** Anthropic, plus Pinecone if it does retrieval.
7. **Where does it live?** Vercel for web, GitHub Releases for desktop binaries, and npm,
   crates.io, or PyPI for libraries.
8. **How do you know it stays healthy in production?** Sentry, UptimeRobot, and PostHog, once
   there are users.

---

## Deliberately not defaults

- **Firebase:** painful vendor lock-in and a steep cost curve. Supabase covers the same ground.
- **Heroku:** Vercel plus Supabase is cheaper and better for the usual web stack.
- **AWS from day one:** start on managed Supabase and Vercel; move to AWS at real scale.
- **Custom auth:** never roll your own. Use Clerk or Supabase.
- **MongoDB:** Postgres via Supabase, unless there is a specific reason.
- **Monorepos from day one:** one repo per project until coupling makes that painful.

---

## Notes

- These are defaults, not rules. If a project needs something else, use it.
- Reassess every six months. Tools change.
- Every managed service is a monthly bill. Turn off what you are not using.
- For agents: if `AGENTS.md` or an existing lockfile conflicts with this file, ignore this
  file.
