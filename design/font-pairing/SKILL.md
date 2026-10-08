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

You study what your design is saying. Then you try new type pairs on copies placed side by side, each one labeled so you can judge with clear eyes.

## Requirements

- A runner with the Figma Plugin API (`figma.loadFontAsync()`,
  `figma.listAvailableFontsAsync()`): the Figma Dev Mode MCP server or a
  plugin runner. If you have none, you propose the 5 pairings as text and you stop before
  Step 3.
- You only suggest fonts you can find in Figma (Google Fonts catalog).

## Workflow

### Step 1 — Analyze the design

Before you suggest a single pairing, you study the selected frame. You want to know what it is and how it speaks. You use the Plugin API and you look with your own eyes:

**Content & Purpose:**
- Ask what type of artifact you hold in your hands. (landing page, dashboard, app screen, editorial, documentation, marketing, etc.)
- Ask how dense your information runs. (sparse/airy vs. data-heavy)
- Ask how deep your text hierarchy runs. (simple heading/body vs. complex multi-level)

**Visual Tone & Aesthetic:**
- Name the overall mood you feel in your work. (corporate, playful, editorial, technical, luxurious, minimal, brutalist, etc.)
- Note the color palette character: warm/cool, muted/strong, monochrome/colorful
- Name your layout style: grid-rigid, organic, card-based, editorial columns, etc.
- Judge your use of imagery against text. Is your design led by pictures or by words.

**Typographic Role:**
- Ask how prominent your typography stands in your design. (hero element vs. functional/secondary)
- Look for decorative type moments in your work (large display text, pull quotes) or admit it is purely functional.
- Ask what rhythm your current type creates. (tight/dense vs. open/breathing)

**Current Font Assessment:**
- You scan all text nodes and you name your current heading, body, and tertiary fonts
- You note the character of your current pairing (geometric, humanist, monospace, serif, etc.)
- You name what works and what your new pairing must keep (e.g. "the monospace labels are essential to the dev-tool identity")

You sum up what you found in 3-4 sentences for your user before you move on.

### Step 2 — Generate font pairing options

You propose **5 font pairing options** shaped by what you learned from your design. Each option includes:
- A **heading font** (display/headline use)
- A **body font** (paragraph/readable use)
- A short **rationale** that ties your choice to what you saw in your design

**How to select pairings:**

If your user gave you direction (e.g. "fun, serif, monospaced, financial"):
- You use each user-specified direction as one pairing slot
- You fill the remaining slots (up to 5) with suggestions shaped by your design analysis
- Your analysis-informed slots should offer complementary or contrasting directions your user might not have considered. Stay loyal to what suits the character of your design.

If your user gave you NO direction:
- You use your design analysis to suggest 5 pairings that span a range from safe evolution to adventurous departure
- You lean toward pairings that respect the purpose and tone of your design
- You include at least one "unexpected but justified" option that reframes the personality of your design

**Pairing principles:**
- Mix contrast for your user: you pair a serif heading with a sans body, or a bold geometric with a humanist sans
- Protect readability: your body fonts must work well at 14 to 18px
- Match the information density of your design. You do not put a decorative display face on a data-heavy dashboard.
- Weigh the tertiary/mono layer in your work. Some designs need a monospace accent. You suggest one when it fits.
- You only suggest fonts you can find in Figma (Google Fonts catalog)

You show the 5 options briefly, then you move straight to Step 3. You do NOT wait for your user to pick. You apply all 5 at once as side-by-side duplicates.

### Step 3 — Create duplicate frames with font pairings applied

You duplicate the selected frame 5 times on your own. You set the copies side by side with a 100px gap. For each duplicate:

1. You rename the frame to "Font Pairing N — [Heading Font] + [Body Font]"
2. You load all required font variants using `figma.loadFontAsync()`
3. You walk all text nodes and you reclassify by original font family:
   - Original heading font → new heading font
   - Original body font → new body font
   - Original mono/tertiary font → new mono/tertiary font
4. You map weight variants to the closest available weight in the new family (check with `figma.listAvailableFontsAsync()` first)
5. You preserve all sizes, colors, line heights, and alignment

### Step 4 — Add label frames above each duplicate

You create a label frame above each duplicated design frame to show your pairing in action:

**Label frame specs:**
- Auto-layout frame, vertical, fixed width matching your design frame (e.g. 1280px), height hugs content
- Padding: 40px all sides
- Item spacing: 16px
- Light background fill (e.g. #F7F7F7), 8px corner radius

**Heading text:**
- You set it in the heading font of that pairing
- Font size: 32px, line height: 40px
- Content: A fun, clever sentence that starts with the font name (e.g. "Fraunces Is Not French, Madam")

**Body text:**
- You set it in the body font of that pairing
- Font size: 16px, line height: 24px
- Content: A witty sentence that starts with the body font name and references its role (e.g. "DM Sans? I'm not going to send any DM's to him. He stole all of the feet off of my sentences last week.")

**Copy guidelines:**
- Your first word or words must be the font name, worked cleverly into a sentence
- Tone: playful, witty, typographic humor. Never NSFW or racy.
- Each pairing gets unique copy. No repeats.
- Your heading copy should run 5 to 8 words
- Your body copy should run 1 to 2 sentences

**Height matching:**
After you create all 5 labels, you find the tallest one and you set ALL labels to that fixed height so they align evenly across the row. You place each label directly above its design frame with a 40px gap.

### Step 5 — Invite feedback

After all frames and labels stand, you show the results as clickable node links and you ask:
"Want me to try different directions, adjust any of these, or remove the ones you don't like?"

## Important Notes

- You always check available font styles with `figma.listAvailableFontsAsync()` BEFORE you try to load fonts. Many families lack "Medium" and need "SemiBold" or "Bold" as a substitute.
- Font style names need spaces (e.g. "Semi Bold" not "SemiBold", "Extra Light" not "ExtraLight")
- You always load fonts before you apply them
- When you change font family, you map weights to the closest available weight in the new family
- You preserve mixed-style text runs (e.g., a bold word within a body paragraph)
- If a frame holds components or instances, you work on the overrideable text layers only
- You never change font sizes, line heights, or letter spacing unless your user asks
