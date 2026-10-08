# Animation Audit Playbook

Here are your eight audit categories. You will learn what to check in each one. You will cite the exact target values in your findings and plans. This comes from Emil Kowalski's design engineering philosophy ([emilkowal.ski](https://emilkowal.ski/)). Listen. Never guess at a value you find here. Copy it.

## 1. Purpose & frequency

Ask this of every animation you wrote: why does this animate. You owe your user a straight answer. That means spatial consistency, state indication, feedback, explanation, or preventing a jarring change. "It looks cool" on an element you see all day is not a purpose.

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette toggle) | No animation. Ever. |
| Tens of times/day (hover effects, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, feedback, celebrations) | Can add delight |

Look for this in your work. Watch for animations on keyboard actions. Watch for command palettes with open and close transitions. Raycast has none, and that is correct. Watch for decorative motion on list items or hover states your user hits all day. Ask what the honest fix is. Often the strongest fix is **delete the animation**.

## 2. Easing & duration

Settle easing in this order. Ask what the element is doing. Then pick:

- Entering or exiting → **`ease-out`** (it starts fast, so your user feels the response right away)
- Moving / morphing on screen → **`ease-in-out`** (you stay steady through the middle of the move)
- Hover / color change → **`ease`** (small change, a plain curve is enough)
- Constant motion (marquee, progress) → **`linear`** (your user expects steady motion with no surprises)
- Default → **`ease-out`** (when in doubt, stay responsive)

Treat **`ease-in` on UI as always a finding**. It starts slow. It stalls at the exact moment your user is watching. The built-in CSS easings are too weak for deliberate motion. Your plans should introduce strong custom curves as tokens. Match your repo conventions:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer curve */
```

Your duration budgets are firm. **UI animations stay under 300ms**. Respect what your user will sit through:

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| Marketing / explanatory | Can be longer |

Look for this in your work. Look for `ease-in` anywhere. Look for bare `ease`/`linear` on entrances. Look for durations over 300ms on UI elements. Look for tooltip delay plus animation on every tooltip in a toolbar. After the first one, your user wants them instant.

## 3. Physicality & origin

- **Never `scale(0)`**. Nothing real comes from nothing. Your target is `scale(0.9–0.97)` + `opacity: 0`.
- **Popovers/dropdowns/tooltips scale from their trigger**, not from center:
  ```css
  .popover { transform-origin: var(--transform-origin); } /* Base UI */
  ```
  **Modals are exempt**. They appear centered, so `transform-origin: center` is correct there. Do not report it.
- **Press feedback**: `transform: scale(0.97)` on `:active` with `transition: transform 160ms ease-out`. Keep it subtle for your user (0.95 to 0.98).

Look for this in your work. Look for `scale(0)`. Look for pure-fade entrances with no initial transform. Look for `transform-origin: center` (or none) on trigger-anchored elements. Look for pressable elements with no press feedback for your user.

## 4. Interruptibility

CSS **transitions** retarget from where you are mid-animation. **Keyframes** restart you from zero. So anything your user triggers fast or reverses mid-motion needs transitions or springs. Think toasts stacking, toggles, drags, expand/collapse.

- Entry without JS means `@starting-style` (legacy fallback is a `data-mounted` attribute set in `useEffect`).
- Gesture-driven motion should use springs. They carry your velocity when you interrupt them.
- Spring configs, Apple-style (recommended): `{ type: "spring", duration: 0.5, bounce: 0.2 }`. Keep bounce subtle for your user (0.1 to 0.3). Save visible bounce for drag-to-dismiss and playful moments.
- **Asymmetric timing**: your deliberate phases (press, hold, destructive confirm) animate slower, then the system answers fast. Symmetric timing on press-and-release is a finding. Why? Your user decides slowly and expects the machine to answer fast.

Look for this in your work: `@keyframes` on toasts/toggles/rapidly-triggered UI, gesture handlers that tween with fixed-duration keyframes, drags without velocity-based dismissal (dismiss on `Math.abs(distance)/elapsedMs > ~0.11`, not distance thresholds alone), hard stops at drag boundaries instead of rising friction for your user.

## 5. Performance

- **Animate `transform` and `opacity` only.** `width`/`height`/`margin`/`padding`/`top`/`left` force layout plus paint plus composite on your user.
- **`transition: all`** animates properties you never meant off-GPU — always a finding in your work.
- **Framer Motion `x`/`y`/`scale` shorthands are not hardware-accelerated** — they run on the main thread and drop frames under load. Your target is the full transform string, `animate={{ transform: "translateX(100px)" }}`.
- **Do not drive child transforms via a CSS variable on the parent** — you recalc styles for all children. Set `transform` directly on the element you mean to move.
- CSS (and WAAPI) beat rAF-based JS under load — use CSS for motion you decided in advance, JS/springs for dynamic and gesture-driven motion.
- Keep transition-time `filter: blur()` under 20px — heavy blur costs you, especially in Safari.

Look for this in your work: `transition: all`, animated layout properties, Framer Motion shorthand props on busy pages, `setProperty('--x', …)` driving child transforms, rAF loops doing what CSS could do for you.

## 6. Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity/color, drop movement */
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* touch fires false hovers on tap */
}
```

Reduced motion means fewer and gentler animations for your user, **not zero** — keep the transitions that aid comprehension, remove the position changes. In JS: `useReducedMotion()` and branch your transform values.

Look for this in your work: movement with no `prefers-reduced-motion` handling, ungated `:hover` motion, reduced-motion implementations that strip all feedback from your user.

## 7. Cohesion & tokens

- Motion should match your product's personality — your playful side can be bouncier, your dashboard stays crisp. When components disagree about who you are, that mismatch is a finding.
- Curves and durations should live as shared tokens you reuse. Five hand-typed cubic-beziers that almost match is a consolidation finding. Would you tolerate five near-copies of a function?
- Everything-at-once group entrances where your user deserves a **30–80ms stagger**. Stagger is decorative — it must never block interaction.
- A jarring crossfade that shows your user two overlapping states can be masked with subtle `filter: blur(2px)` during the transition.

Look for this in your work: duplicated near-identical easings/durations, one bouncy component in your crisp app, list/grid entrances with no stagger, crossfades that visibly double-expose.

## 8. Missed opportunities

This is the additive category — places that sit still but should speak to your user:

- State changes that teleport your user (content swaps, layout jumps) where a brief transition would prevent a jarring change.
- Spatially-connected UI (a panel that appears from its trigger) with no motion explaining to your user where it came from.
- Rare, high-emotion moments for your user (first-run, success, celebration) rendered with none of the delight budget they are allowed.
- `translate` percentages (`translateY(100%)` = element's own height) and `clip-path: inset()` reveals as your tools for these — no hardcoded pixel offsets.

Report at most a handful, grounded in real UX seams you watched your user hit — not a wishlist.
