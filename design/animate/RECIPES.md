# Animation Recipes

These are ready-to-build implementations for the cases you will meet most. You start from the recipe, then you adapt. Do not rebuild from scratch. That is wasted craft.

Curves are the `--ease-out`, `--ease-in-out`, and `--ease-drawer` tokens defined in SKILL.md. You use those tokens. You do not invent new ones.

---

## Button press

Any pressable element. You give instant feedback that your interface heard your user. That is your job.

```css
.button {
  transition: transform 160ms var(--ease-out);
}

.button:active {
  transform: scale(0.97);
}
```

`scale()` scales children too — your label and icons come along, which is what makes it read as a physical press to your user.

You need no hover gating here: `:active` is a real press on touch. You gate any `:hover` styling separately. Keep the two apart.

---

## Dropdown, popover, menu, select

It scales out of its trigger, not out of thin air. Your user should see where it came from.

```css
.popover {
  transform-origin: var(--transform-origin); /* Base UI supplies this */
  transition:
    opacity 200ms var(--ease-out),
    transform 200ms var(--ease-out);
}

.popover[data-starting-style],
.popover[data-ending-style] {
  opacity: 0;
  transform: scale(0.95);
}
```

The `transform-origin` is the whole point — your panel should look like it came out of the thing your user clicked. Get that right.

---

## Tooltip

Same shape as a popover, faster, plus the detail your peers miss most. Pay attention here.

```css
.tooltip {
  transform-origin: var(--transform-origin);
  transition:
    transform 125ms var(--ease-out),
    opacity 125ms var(--ease-out);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

/* Once one tooltip is open, neighbours open instantly */
.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

The initial delay prevents accidental activation. After that, you skip both the delay and the animation. That makes your whole toolbar feel faster to your user.

---

## Modal

The one popover that stays centered. You keep it centered for your user.

```css
.modal {
  transform-origin: center; /* exempt — not anchored to a trigger */
  transition:
    opacity 250ms var(--ease-out),
    transform 250ms var(--ease-out);
}

.modal[data-starting-style],
.modal[data-ending-style] {
  opacity: 0;
  transform: scale(0.96);
}

.backdrop {
  transition: opacity 250ms var(--ease-out);
}
```

You animate the backdrop's opacity alongside it so they read as one surface to your user. Two pieces. One motion.

---

## Drawer / sheet

```css
.drawer {
  transform: translateY(0);
  transition: transform 500ms var(--ease-drawer);
}

.drawer[data-closed] {
  transform: translateY(100%);
}
```

This is how Vaul hides a drawer before you animate it in. Learn from it.

You add drag and it becomes a gesture problem for your user — see **Drag to dismiss** below. Treat it as one.

---

## Toast

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 400ms ease,
    transform 400ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

- `ease` rather than `ease-out`, slightly slower than typical UI: you tune Sonner to read as elegant partly because its motion fits the component's personality rather than the generic UI budget.
- If `@starting-style` isn't available, you fall back to the mount flag:

```jsx
useEffect(() => { setMounted(true); }, []);
// <div data-mounted={mounted}>
```

When your toasts stack and your list reflows, your opacity change has to work against the height change. There is no formula for that pair — you adjust until it feels right to you, then you check it again the next day with fresh eyes.

---

## Accordion / collapse

```css
.content {
  overflow: hidden;
  transition:
    height 200ms var(--ease-out),
    opacity 200ms var(--ease-out);
}
```

You keep it short — this is one of the few animations that costs layout on every frame, so a long duration costs your user twice, in expense and in sluggishness. You measure the content height in JS (or you use a headless primitive that supplies it) rather than animating to `auto`.

---

## Stagger a group entrance

For a list or grid your user sees occasionally — not for a list they scroll past all day. Ask how often they will see it.

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms var(--ease-out) forwards;
}

.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
.item:nth-child(4) { animation-delay: 150ms; }

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Stagger is decorative — you must never block your user's interaction while it plays. That is the rule.

---

## Hold to confirm

For destructive actions where your user's plain click fires too easy by accident. You protect them.

```css
.overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out); /* release: snappy */
}

.button:active .overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;             /* press: slow and deliberate */
}

.button:active {
  transform: scale(0.97);
}
```

`linear` is correct here — your fill is a progress indicator, and progress should not ease. Be honest with your user.

---

## Tab indicator with a color transition

Timing individual color transitions across a tab list never quite lands for your user. You clip instead. That is the craftsman's fix.

You duplicate the tab list. You style the copy as the active state — different background, different text color. You clip the copy so only the active tab shows, and you animate the clip on change:

```css
.tabs-active-copy {
  clip-path: inset(0 60% 0 20%); /* driven by the active tab's position */
  transition: clip-path 250ms var(--ease-in-out);
}
```

Your text and background change together, in perfect sync, because they are one element being revealed rather than two colors being interpolated. Your user feels the difference.

---

## Scroll reveal

Marketing surfaces only. You do not do this to functional UI your user visits daily. Leave daily work alone.

```css
.reveal {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 600ms var(--ease-in-out);
}

.reveal[data-visible] {
  clip-path: inset(0 0 0 0);
}
```

You trigger with `IntersectionObserver`, or Motion's `useInView` with `{ once: true, margin: "-100px" }`. You fire it once — re-animating on every scroll-by is your interface fighting its reader.

---

## Drag to dismiss

The gesture recipe. You use springs, not durations, because your user can reverse mid-motion. Respect that.

```js
// Dismiss on a flick, not just on distance
const timeTaken = Date.now() - dragStartTime.current;
const velocity = Math.abs(swipeAmount) / timeTaken;

if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

```js
// Set transform on the dragged element directly.
// Driving it through a CSS variable on the parent recalcs styles for every child.
element.style.transform = `translateY(${distance}px)`;
```

Four details that separate a good drag from a bad one:

- **Pointer capture** once the drag starts, so it continues when the pointer leaves the element's bounds.
- **Multi-touch protection** — `if (isDragging) return` on new touch points, or switching fingers mid-drag makes the element jump.
- **Damping past boundaries** — dragging beyond a natural edge moves the element less the further it goes. Real things slow before they stop.
- **Friction, not a wall** — allow the over-drag with rising resistance rather than refusing it.

Settle with a spring so an interrupted drag keeps its velocity:

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }
```

---

## Masking a crossfade that won't settle

When two states overlap visibly during a transition and no amount of easing or duration tuning fixes it, blur the seam:

```css
.content {
  transition:
    filter 200ms ease,
    opacity 200ms ease;
}

.content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

Without blur the eye reads two distinct objects swapping. Blur blends them into one perceived transformation. Keep it under 20px — heavy blur is expensive, especially in Safari.

---

## Programmatic, without a library

When the motion needs JS control but not a dependency, WAAPI gives you CSS-grade performance:

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
);
```

Hardware-accelerated, interruptible, no bundle cost.
