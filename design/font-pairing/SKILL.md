---
name: font-pairing
description: >
  Use this skill when the user wants font pairing options for a design: picking
  heading and body fonts, trying different typefaces side by side, comparing
  type directions on a frame, or "what font goes with this". Generates 5
  pairings and applies them as labeled side-by-side duplicates. Trigger on
  "suggest fonts", "font pairing", "try typefaces", "heading and body fonts",
  or any request to explore typography directions on an existing design.
---

# Font pairing

Analyze what the selected design is communicating, then try new type pairings on labeled
side-by-side copies so they can be compared directly.

## Requirements

- A runner with the Figma Plugin API (`figma.loadFontAsync()`,
  `figma.listAvailableFontsAsync()`): the Figma Dev Mode MCP server or a plugin runner. Without
  one, propose the 5 pairings as text and stop before Step 3.
- Suggest only fonts available in Figma (the Google Fonts catalog).

## Workflow

### Step 1: Analyze the design

Before suggesting any pairing, study the selected frame through the Plugin API:

**Content and purpose**
- What kind of artifact is it? (landing page, dashboard, app screen, editorial, documentation,
  marketing, etc.)
- How dense is the information? (sparse and airy vs. data-heavy)
- How deep is the text hierarchy? (simple heading/body vs. complex multi-level)

**Visual tone**
- The overall mood (corporate, playful, editorial, technical, luxurious, minimal, brutalist,
  etc.)
- The palette's character: warm or cool, muted or strong, monochrome or colorful
- The layout style: rigid grid, organic, card-based, editorial columns, etc.
- The balance of imagery and text: is the design led by pictures or by words?

**Typographic role**
- How prominent is the typography? (hero element vs. functional and secondary)
- Are there decorative type moments (large display text, pull quotes), or is it purely
  functional?
- What rhythm does the current type create? (tight and dense vs. open)

**Current fonts**
- Scan all text nodes and identify the current heading, body, and tertiary fonts
- Note the character of the current pairing (geometric, humanist, monospace, serif, etc.)
- Note what works and what any new pairing must keep (for example, "the monospace labels are
  essential to the dev-tool identity")

Summarize the findings for the user in 3-4 sentences before moving on.

### Step 2: Generate font pairing options

Propose **5 font pairings** based on the analysis. Each option includes:
- A **heading font** (display and headline use)
- A **body font** (paragraph and readable use)
- A short **rationale** tying the choice to what the analysis found

**Selecting pairings**

If the user gave a direction (for example "fun, serif, monospaced, financial"):
- Use each direction they named as one pairing slot
- Fill the remaining slots (up to 5) from the design analysis
- Make the analysis-driven slots complementary or contrasting directions the user may not have
  considered, while staying true to the design's character

If the user gave no direction:
- Use the analysis to suggest 5 pairings ranging from a safe evolution to an adventurous
  departure
- Favor pairings that respect the design's purpose and tone
- Include at least one "unexpected but justified" option that reframes the design's
  personality

**Pairing principles**
- Mix contrast: a serif heading with a sans body, or a bold geometric with a humanist sans
- Protect readability: body fonts must work well at 14 to 18px
- Match the information density: no decorative display face on a data-heavy dashboard
- Consider the tertiary or mono layer; suggest a monospace accent when the design needs one
- Suggest only fonts available in Figma (Google Fonts catalog)

Show the 5 options briefly, then go straight to Step 3. Do not wait for the user to pick; apply
all 5 at once as side-by-side duplicates.

### Step 3: Create duplicate frames with the pairings applied

Duplicate the selected frame 5 times and place the copies side by side with a 100px gap. For
each duplicate:

1. Rename the frame to "Font Pairing N: [Heading Font] + [Body Font]"
2. Load every required font variant with `figma.loadFontAsync()`
3. Walk all text nodes and reassign fonts by original family:
   - Original heading font → new heading font
   - Original body font → new body font
   - Original mono/tertiary font → new mono/tertiary font
4. Map each weight to the closest available weight in the new family (check with
   `figma.listAvailableFontsAsync()` first)
5. Preserve all sizes, colors, line heights, and alignment

### Step 4: Add a label frame above each duplicate

Create a label frame above each duplicated design frame that shows the pairing in use.

**Label frame specs**
- Auto-layout frame, vertical, fixed width matching the design frame (for example 1280px),
  height hugging its content
- Padding: 40px on all sides
- Item spacing: 16px
- Light background fill (for example #F7F7F7), 8px corner radius

**Heading text**
- Set in the pairing's heading font
- Font size 32px, line height 40px
- Content: a clever sentence that starts with the font name (for example "Fraunces Is Not
  French, Madam")

**Body text**
- Set in the pairing's body font
- Font size 16px, line height 24px
- Content: a witty sentence that starts with the body font name and references its role (for
  example "DM Sans? I'm not going to send any DM's to him. He stole all of the feet off of my
  sentences last week.")

**Copy guidelines**
- The first word or words must be the font name, worked into the sentence
- Tone: playful typographic humor, never NSFW or racy
- Unique copy for every pairing
- Heading copy of 5 to 8 words
- Body copy of 1 to 2 sentences

**Height matching**
After creating all 5 labels, find the tallest and set every label to that fixed height so they
align across the row. Place each label directly above its design frame with a 40px gap.

### Step 5: Ask for feedback

Once all frames and labels exist, share them as clickable node links and ask:
"Want me to try different directions, adjust any of these, or remove the ones you don't like?"

## Important notes

- Always check available styles with `figma.listAvailableFontsAsync()` before loading fonts.
  Many families lack "Medium" and need "SemiBold" or "Bold" instead.
- Style names contain spaces ("Semi Bold", not "SemiBold"; "Extra Light", not "ExtraLight").
- Load fonts before applying them.
- When changing the family, map weights to the closest available weight in the new family.
- Preserve mixed-style text runs (for example, a bold word inside a body paragraph).
- In components or instances, change only overridable text layers.
- Never change font sizes, line heights, or letter spacing unless the user asks.
