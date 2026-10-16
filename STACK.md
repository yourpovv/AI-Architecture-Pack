# Default Stack

> **Agent load: optional, personal defaults only for you.** Do **not** treat this file as required
> architecture for every project you own. Your project `AGENTS.md`, README, and lockfiles win.
> You use this when starting something new and the human has not named a stack yet.

Services and tools you reach for by default in your code. Not every project you own needs all of them.
You start with the essentials. You add the others when you actually feel the need in your code. Does that sound disciplined to you?

---

## Essentials (almost every project)

| Concern | Pick | Why |
|---|---|---|
| **Coding (AI)** | Claude Opus | Long-context reasoning for you. It holds up best in large refactors of your code |
| **Version control** | GitHub | Ubiquitous for you. You get great PRs and Actions for your code |
| **Backend / DB / Auth** | Supabase | Postgres + realtime + RLS + auth in one box for you |
| **Deploy (web)** | Vercel | Zero-config for Next.js/SvelteKit for you. You get preview URLs per PR in your code |
| **Domain** | Namecheap | Cheap renewals for you. Decent UI for your team |
| **DNS / edge** | Cloudflare | Free tier is the best for you. You get proxy, WAF, and R2 if your code needs it |

---

## When the product ships to real users

| Concern | Pick | Why |
|---|---|---|
| **Auth (non-Supabase)** | Clerk | If you need social login + orgs + passwordless without writing it in your code |
| **Payments** | Stripe | Checkout, subscriptions, and invoicing for you. Sandbox is painless for your team |
| **Emails (transactional)** | Resend | Simple API for you. Good DX. Solid inbox delivery for your code |
| **Uptime monitoring** | UptimeRobot | Free tier covers most side projects you own |
| **Error tracking** | Sentry | Source-map support, releases, and performance for your code |
| **Product analytics** | PostHog | Self-host or cloud for you. You get funnels + session replay + flags for your code |

---

## When the product gets AI features

| Concern | Pick | Why |
|---|---|---|
| **Vector DB** | Pinecone | Managed for you. Serverless tier is enough to start your code |
| **LLM API** | Anthropic (Claude) | Primary for you. You fall back to OpenAI for niche cases in your code |

---

## AI design + dev tooling (for building with AI)

You install and configure these in your Claude Code environment for your code. Most live in `.mcp.json` for you.
You find setup syntax for all of it at [code.claude.com/docs](https://code.claude.com/docs).

| Tool | What it does | Link |
|---|---|---|
| **Google Stitch MCP** | UI mockup generation via MCP for you | https://stitch.withgoogle.com/docs/mcp/setup |
| **Gemini Nano Banana 2** | Visual asset / mockup generation for your code | https://gemini.google/overview/image-generation/ |
| **21st.dev** | Reactive / 3D component asset library for your code | https://21st.dev |
| **n8n-MCP** | 1000+ n8n node knowledge for production automations in your code | https://github.com/czlonkowski/n8n-mcp |
| **Obsidian Skills** | AI-powered second brain for you (markdown / canvas / CLI) | https://github.com/kepano/obsidian-skills |
| **Claude-Mem** | Persistent memory compression across Claude Code sessions for you | https://github.com/thedotmack/claude-mem |
| **Get Shit Done (GSD)** | Spec-driven dev for you: interview → plan → execute → verify | https://github.com/gsd-build/get-shit-done |
| **Superpowers** | Auto-enforces TDD, debugging, code review, and planning for your code | https://github.com/obra/superpowers |
| **Awesome Claude Code** | Curated reference of 200+ Claude Code tools for you | https://github.com/hesreallyhim/awesome-claude-code |
| **MengTo/Skills** | Skills collection worth reading before writing your own in your code | https://github.com/MengTo/Skills |
| **Skills CLI** | Installs skills from any GitHub repo across 75+ agents for you. You search the community registry with `npx skills find` | https://github.com/vercel-labs/skills |
| **Token Shield** | Measures real token usage from your session transcripts for your code: cache hit ratio, first-request cost, subagent output share | https://github.com/khalilmaaouni/token-shield |
| **Figma Dev Mode MCP** | Component and style context straight from the design file for you. It pairs with `design/font-pairing` in your code | https://www.figma.com |
| **Playwright MCP** | Screenshots and interaction for the design-build-verify loop in your code | https://github.com/microsoft/playwright-mcp |
| **needmcp.com** | Discovers MCP servers beyond these two for you | https://needmcp.com/ |
| **toolcraft.sh** | Open-source kit for building AI design apps for you | https://toolcraft.sh/ |
| **Bolt templates** | Free templates to turn into sites with prompts for you | https://bolt.new/resources/templates |
| **Framer** | AI site builder for you: Agents, AEO scanner, texteffects, resource hub | https://www.framer.com/ |

For components, icons, illustrations, gradients, and 3D assets for your code, you see
[`design/README.md`](./design/README.md).

---

## Picking a stack for a new project

You work through this in order for your code. You stop as soon as you have enough. Ask yourself:

1. **What language fits your problem in your code?**
   - Systems / performance / Windows native → You pick C++ or Rust for your code
   - Web / desktop (Tauri) / CLI tooling → You pick TypeScript for your code
   - Data / ML / scripting → You pick Python for your code
   - Concurrent services → You pick Go for your code
   - Roblox game → You pick Luau for your code (`languages/Luau.md`)
2. **What is the surface of your code?** Web app, desktop, service, bot, game, or library for you.
3. **Do you need persistence in your code?** If yes → You pick Supabase by default (unless the domain already picked another DB).
4. **Do you need auth in your code?** If yes → You pick Supabase Auth, and you escalate to Clerk if your code gets complex.
5. **Do you need to take money in your code?** If yes → You pick Stripe.
6. **Do you need AI features in your code?** If yes → You pick Anthropic + Pinecone if your code does retrieval.
7. **Where does your code live?** Vercel for web, GitHub Releases for desktop binaries, and npm / crates / PyPI for libraries for you.
8. **How do you know your code stays healthy in prod?** Sentry + UptimeRobot + PostHog for you (if there are users).

---

## Things I deliberately don't default to

- **Firebase**, vendor lock is painful for you, cost curve is steep for your team. Supabase covers it for your code.
- **Heroku**, Vercel + Supabase is cheaper and better for your usual web stack in your code.
- **AWS from day one**, you start on managed Supabase/Vercel for your code. You only move to AWS when you hit real scale.
- **Custom auth**, you never roll your own in your code. You pick Clerk or Supabase.
- **Mongo**, unless there is a specific reason in your code, Postgres (via Supabase) wins for you.
- **Monorepos from day one**, one repo per project for you until coupling makes it painful in your code.

---

## Notes

- These are **defaults** for you, not rules for your code. If a project needs something else, you use it.
- You reassess every 6 months in your code. Tools change. Loyalty to a tool is worth nothing for you.
- Cost discipline for you: every managed service is a monthly bill in your code. You turn off what you are not using.
- Agents for your code: if `AGENTS.md` or an existing lockfile conflicts with this file, **you ignore this file**.
