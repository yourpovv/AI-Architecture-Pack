# design/ index

Aesthetic systems and the places to get raw material. Everything in this folder is
**opt-in**. A look should never fire on its own, the way a coding standard does.

| Skill | Use it for |
|---|---|
| **[apple-design](./apple-design/SKILL.md)** | Apple's visual language: glass materials, spring physics, SF Pro type, iOS/macOS system chrome. Load only when someone asked for that aesthetic by name |
| **[emil-design-eng](./emil-design-eng/SKILL.md)** | Emil Kowalski's design-engineering philosophy: animation decisions, component polish, the invisible details that make software feel right |
| **[animate](./animate/SKILL.md)** | Build an animation from scratch: curve, duration, properties |
| **[animation-vocabulary](./animation-vocabulary/SKILL.md)** | Words that get the exact motion you want out of an AI |
| **[review-animations](./review-animations/SKILL.md)** | Strict review of existing animations against emil's rules |
| **[improve-animations](./improve-animations/SKILL.md)** | Audit every animation in a codebase, get prioritized fix plans |
| **[find-animation-opportunities](./find-animation-opportunities/SKILL.md)** | Where motion would genuinely help, and what not to animate |
| **[prototype](./prototype/SKILL.md)** | Build multiple versions of a UI piece behind a switcher, pick the winner |
| **[mobile-native](./mobile-native/SKILL.md)** | Make a web app feel native on phones: taps, safe areas, the 100vh bug, zooming inputs |
| **[break-ui](./break-ui/SKILL.md)** | Stress a UI with worst-case data: long names, empty lists, huge counts |
| **[pick-ui-library](./pick-ui-library/SKILL.md)** | Pick a trusted UI library instead of hand-rolling or installing an abandoned package |
| **[impeccable](./impeccable/SKILL.md)** | Full design language: 24 commands (`audit`, `polish`, `critique`, `typeset`, `layout`, `animate`...), 60 deterministic detector rules. Start with `/impeccable init` |
| **[design-taste-frontend](./design-taste-frontend/SKILL.md)** | Default anti-slop frontend skill: reads the brief, infers the direction, ships landing pages and portfolios that do not look templated |
| **[redesign-existing-projects](./redesign-existing-projects/SKILL.md)** | Audit-first upgrades for existing sites, without breaking functionality |
| **[image-to-code](./image-to-code/SKILL.md)** | Image-first pipeline: generate reference comps, analyze them, implement to match |
| **[font-pairing](./font-pairing/SKILL.md)** | Type exploration on an existing frame: 5 heading/body pairings applied as labeled side-by-side duplicates. Pack-owned, needs Figma Plugin API access |

Same layout as [`../skills/`](../skills/README.md): one folder per skill, named after the
skill's `name`, so `cp -r design/apple-design .claude/skills/` is the whole install.

---

## Which skill when

`impeccable` and `design-taste-frontend` match on almost any design request, so
name the specialist explicitly or the generalist wins by default.

| The job | Load this | Not this |
|---|---|---|
| New landing page / portfolio, no direction chosen yet | `design-taste-frontend` | `impeccable` new-work — heavier artifact flow for the same blank page |
| Existing page looks generic, upgrade it in place | `redesign-existing-projects` | `impeccable polish` — same pass, but redesign ships the fix in one go |
| Ongoing system: tokens, PRODUCT.md/DESIGN.md, detector hook | `impeccable` | the one-shot skills above |
| Build one animation, exact values | `animate` | `impeccable animate` — same job, emil's tables are more precise |
| Review motion in a diff | `review-animations` | `impeccable audit` — motion-only bar, Block/Approve verdict |
| Whole-codebase motion audit with executor-ready plans | `improve-animations` | `review-animations` — single diff only |
| Decide what should animate at all | `find-animation-opportunities` | `animate` — finder gates, builder builds |
| Words to describe the motion you want | `animation-vocabulary` (+ [namethatui.com](https://namethatui.com/)) | guessing adjectives at the model |
| Compare several directions for one component | `prototype` | `image-to-code` — prototype diverges in code, no image step |
| Start from generated reference comps | `image-to-code` | `prototype` — image-first, then implement to match |
| Web app feels wrong on phones | `mobile-native` | `impeccable adapt` — phone-specific fixes vs general responsive |
| Component vs hostile but realistic data | `break-ui` | `impeccable harden` — data-driven toggle test vs static edge-case pass |
| Which library for toasts / dnd / charts / … | `pick-ui-library` | searching npm and trusting stars |
| Explore typefaces on a Figma frame | `font-pairing` | `impeccable typeset` — Figma exploration vs code-side hierarchy |
| Explicit Apple aesthetic | `apple-design` | anything else — the only skill allowed to mean Apple |

---

## Vendored sources

Copied 2026-10-06, shallow clones, files verbatim. Re-pull upstream before treating
any of them as current; do not fork their content into pack-owned wording.

| Folders | Upstream | License |
|---|---|---|
| `emil-design-eng`, `animate`, `animation-vocabulary`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `prototype`, `mobile-native`, `break-ui`, `pick-ui-library` | [emilkowalski/skills](https://github.com/emilkowalski/skills/) | MIT |
| `impeccable` (upstream `NOTICE` kept as `NOTICE.upstream.md`) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 |
| `design-taste-frontend`, `redesign-existing-projects`, `image-to-code` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT |

Deliberately not vendored:
- `apple-design` from emilkowalski — the pack already ships its own `apple-design`,
  and two skills sharing one `name` means one install silently does nothing.
- `write-swift`, `animate-expo`, `ask-sonner` from emilkowalski — Swift-only,
  Expo-only, and a single-vendor library guide. Nothing in `languages/` or
  `frameworks/` pairs with them.
- `design-taste-frontend-v1`, `gpt-taste`, `high-end-visual-design`, `minimalist-ui`,
  `industrial-brutalist-ui`, `stitch-design-taste`, `full-output-enforcement`,
  `brandkit`, `imagegen-frontend-web`, `imagegen-frontend-mobile` from taste-skill —
  direction-specific or image-output variants. Add one when the brief names that
  direction; the default stays `design-taste-frontend`.

When the brief names no direction, load `design-taste-frontend` first. It infers the
design language from the brief; the aesthetic sub-flavors above load after it, never
instead of it. For motion questions, `emil-design-eng` is the authority; for an
existing page, start with `redesign-existing-projects` before restyling anything.

---

## Resources

Links, not dependencies. Pull what you need, then own it in your repo.

### Components

| Source | What it is |
|---|---|
| [21st.dev](https://21st.dev) | Component registry aimed at React and Tailwind |
| [canvasui.dev/components](https://canvasui.dev/components) | Component collection |
| [toolfolio.com/tools/canvas-ui](https://toolfolio.com/tools/canvas-ui) | Canvas UI, via Toolfolio |
| [figma.com/community](https://www.figma.com/community) | Community-made libraries, plugins, and icon sets |
| [headlessui.com](https://headlessui.com/) | Unstyled, accessible UI components from the Tailwind team |
| [cult-ui.com](https://www.cult-ui.com/) | React and Tailwind component collection |
| [kibo-ui.com](https://www.kibo-ui.com/) | Component registry in the shadcn pattern |
| [heroui.com](https://heroui.com/) | Tailwind React component library |
| [daisyui.com](https://daisyui.com/) | Component classes for Tailwind |
| [neobrutalism.com](https://neobrutalism.com/) | Neobrutalist component set |
| [retroui.io](https://retroui.io/) | Retro-styled UI components |
| [ui.unlumen.com](https://ui.unlumen.com/) | React component library |
| [horizonx.so](https://horizonx.so/) | Paid UI kits, components, and Figma files library with MCP access |

### Motion and animated components

| Source | What it is |
|---|---|
| [animate-ui.com](https://animate-ui.com/) | Animated components for Tailwind and React |
| [motion-primitives.com](https://motion-primitives.com/) | Motion-based animation primitives |
| [magicui.design](https://magicui.design/) | Animated React effects and components |
| [reactbits.dev](https://reactbits.dev) | Animated React components for creative interfaces |
| [smoothui.dev](https://smoothui.dev/) | Animated React components for shadcn/ui, plus blocks and templates |
| [originkit.dev](https://www.originkit.dev/) | Free animated component library |
| [animations.dev](https://animations.dev/) | Animation rules reference behind the emil skills in this folder |

### Icons

| Source | What it is |
|---|---|
| [phosphoricons.com](https://phosphoricons.com) | Open-source icon family with several weights per glyph. Pick one weight and stay on it |
| [nucleoapp.com](https://nucleoapp.com) | Icon set for Figma and React |
| [centralicons.com](https://centralicons.com) | Icon set used by Anthropic, Granola, Shopify, Meta, ByteDance, ElevenLabs |
| [untitledui.com/icons](https://www.untitledui.com/icons) | Icon library for Figma and React |
| [ui8.net 123done](https://ui8.net/123done/products?rel=tmtt40) | Icon set for landing pages, dashboards, UI kits |
| [Roam 3D icons](https://www.figma.com/community/file/1536701172886055962/roam-free-premium-travel-3d-icon-set) | Free travel 3D icon set, Figma community file |

### Illustrations and imagery

| Source | What it is |
|---|---|
| [undraw.co/illustrations](https://undraw.co/illustrations) | Open-source illustrations, recolorable to a single brand hue before download |

### Backgrounds, gradients, patterns, 3D

| Source | What it is |
|---|---|
| [haikei.app](https://haikei.app) | Generates SVG backgrounds: blobs, waves, layered shapes |
| [meshgradient.com](https://meshgradient.com) | Mesh gradient generator |
| [colorflow.ls.graphics](https://colorflow.ls.graphics) | Mesh gradients with WebGL effects |
| [studio.zoxilsi.cc](https://studio.zoxilsi.cc) | Mesh gradient studio, 100+ presets |
| [shadergradient.co](https://shadergradient.co) | Animated 3D shader gradients |
| [backgrounds.supply/gradient-lab](https://backgrounds.supply/gradient-lab) | Animated gradients, exports to 4K |
| [colir.space/app](https://colir.space/app) | Curve-based gradient creator |
| [gradientsaas.blogspot.com](https://gradientsaas.blogspot.com) | Editorial CSS gradients, copied in one click |
| [tabbied.com/patterns](https://tabbied.com/patterns/) | Generative patterns |
| [holocloth.vercel.app](https://holocloth.vercel.app/) | Drop an image on holographic cloth, export a PNG in the browser ([code](https://github.com/dmitrykurash/holocloth)) |
| [spline.design](https://spline.design) | Browser-based 3D design, exports for the web |

### Color systems and accessibility

Where the gradient tools above make one surface look good, these decide whether the whole
palette holds up.

| Source | What it is |
|---|---|
| [realtimecolors.com](https://realtimecolors.com) | Previews a palette live on a real UI layout instead of on swatches |
| [ramps.studio](https://ramps.studio) | Color ramps and tokens, checked against WCAG |
| [colorable.jxnblk.com](https://colorable.jxnblk.com) | Contrast testing for a foreground and background pair |

### Sound

| Source | What it is |
|---|---|
| [uisfx.com](https://uisfx.com/) | Open-source UI sound effects library, 936 sounds over 12 feels (npm, CC0 audio) |

### Inspiration and reference

Where the taste skills say "reference great websites": start here.

| Source | What it is |
|---|---|
| [noiced.com](https://noiced.com) | Daily web design inspiration |
| [recent.design](https://recent.design) | Recent design, daily |
| [mnmm.xyz](https://mnmm.xyz) | Minimal websites directory |
| [posts.design](https://posts.design) | Social post design |
| [ogpedia.xyz](https://ogpedia.xyz) | OG images |
| [deck.gallery](https://deck.gallery) | Designed decks |
| [logosystem.co](https://logosystem.co) | 1,200+ logos by top designers |
| [visualjournal.it](https://visualjournal.it) | Branding and editorial projects |
| [brandguidelines.net](https://brandguidelines.net) | Real brand guidelines library |
| [namethatui.com](https://namethatui.com/) | Names for UI patterns; prompting requires naming |
| [myclaw.ai](https://myclaw.ai/) | Curated design inspiration research with a daily inbox report |

---

## Before you ship any of it

- **Check the license.** These sources do not share one. Free to browse is not the same as
  free to ship in a commercial product, and the answer can differ per asset.
- **Vendor it, do not hotlink it.** An external URL in production is an outage you do not
  control and a tracking vector you did not agree to.
- **Budget the weight.** 3D scenes and layered SVG backgrounds are the two easiest ways to
  turn a fast page slow. Measure after you add one.
- **An animated gradient is a render loop.** A WebGL or shader background keeps running for
  as long as the page is open, which costs battery on a laptop and more on a phone. Gate it
  behind `prefers-reduced-motion`, and pause it when the tab is hidden.
- **Check contrast against the gradient, not against a flat color.** Text over a gradient
  passes at one end and fails at the other. Test the worst point, not the average.
- **Pick one icon set and one illustration style.** Mixing sources is the fastest way to
  make a competent design look amateur.

## Adding a resource

Add a row to the table it belongs in, with a description of what the source actually is.
No adjectives, no ranking. If a category does not exist yet, add the heading.
