# iOS platform

You build for native iOS and iPadOS apps. You ship SwiftUI, UIKit, React Native, Expo, or Flutter to Apple hardware. You build for a real device in a real hand.

On native, the visitor mode narrows what your expression may override. HIG conformance governs your structure, your navigation, and your interaction in every mode. Your brand speaks through the layer the platform leaves open: tint, type, motion, and content.

## The iOS slop test

Would a fluent iPhone user trust your app, or pause at off-spec controls? The tell is a site ported to a phone. You see it in reinvented navigation bars, custom back gestures, web-shaped buttons, and hover-dependent affordances. You default to the platform components. You depart only for a reason your user would thank you for.

## Layout & structure

- **Safe area.** You lay out inside the safe-area insets. You put no controls under the notch, the Dynamic Island, the home indicator, or the rounded corners.
- **System navigation.** You use a tab bar for 2 to 5 top-level sections, sections and never actions. You use a navigation stack for hierarchy. You use a sheet for a self-contained task. You build no custom global nav. You mix no metaphors.
- **Edge-swipe back stays alive.** The left-edge back gesture is muscle memory. You never disable it. You never cover it.
- **Large titles** on top-level screens, collapsing to inline on scroll. Deep detail screens stay inline.

## Touch targets

- **44×44 pt minimum** for every tappable control you ship, with breathing room between adjacent targets.

## Typography

- **Dynamic Type.** You use the system text styles, Large Title through Caption, so your text follows the reading size your user chose. You hard-code no point sizes.
- **San Francisco carries the UI.** Your body, your labels, and your controls stay on SF Pro and SF Compact. A brand face may appear in display moments.
- **11 pt floor**. Your Body is 17 pt.

## Color & materials

- **Semantic system colors** (label, secondaryLabel, systemBackground, separator, tint). They adapt to Dark Mode and increased contrast on their own. Raw hex breaks there, so you do not use it.
- **Dark Mode is a first-class appearance.** You design it. You test it. You test both appearances.
- **One tint color** drives your interactive elements. Decoration is not its job.
- **System materials** give you blur and translucency behind bars and sheets. You roll no hand-made glassmorphism.

## Components & controls

- **Platform controls.** You use the switch, the segmented control, the stepper, the system pickers, action sheets, alerts, context menus, and swipe actions. Reinventing these for flavor is the most common native slop. You do not ship it.
- **SF Symbols** for your iconography: baseline-aligned, Dynamic Type-aware, with weight and scale variants. You mix in no web icon set.
- **Deliberate modality.** You use a sheet for a focused dismissible sub-task. You use a full-screen cover for immersion. You give a clear Cancel and Done. You honor swipe-to-dismiss unless data loss calls for a guard.
- **Grouped and inset lists** for settings-shaped content. You build no bespoke card stacks.

## Motion

- **System transitions.** A push slides. A sheet rises. A dismiss reverses the entrance. Custom transitions that fight the navigation model disorient your user, so you do not ship them.
- **Honor Reduce Motion.** You crossfade instead of parallax and large slides.

## Verifying the build

- **Screenshots come from the Simulator, never a browser.** You build and run. Then you capture with `xcrun simctl io booted screenshot <path>` (with several running, replace `booted` with the target's UDID from `xcrun simctl list devices booted`; display names can collide, the UDID never does). You capture every device class your app ships to, at least one iPhone and, when iPad is a target, one iPad. You write the files where the review flow expects them.
- **Dark Mode and Dynamic Type belong in the pass.** `xcrun simctl ui booted appearance dark` flips appearance, reusing the capture's UDID when several are booted. A check at a large Dynamic Type size catches the truncation a fixed layout hides.
- **Simulators give you breadth. Posture, gestures, and performance need hardware.** You say which one produced your evidence.
