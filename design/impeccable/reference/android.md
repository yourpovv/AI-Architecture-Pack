# Android platform

You build for native Android apps: Jetpack Compose, Android Views, React Native, Expo, and Flutter shipping to Android hardware. You build for a real device in a real hand.

On native, the visitor mode narrows what your expression may override. Material Design 3 governs your structure, your navigation, and your interaction in every mode. Your brand speaks through Material theming: color roles, type scale, shape, and motion. A Material-everywhere cross-platform app that also ships to iPhone still owes iOS its OS guarantees on that hardware: safe-area insets, Reduce Motion, and edge-swipe back. Why? Your user trusts the platform.

## The Android slop test

Would a fluent Android user trust your app, or trip on off-spec components? Listen. The most common tell is an iOS app wearing Android skin: a bottom-only navigation copied from iPhone, a back arrow that ignores the system Back gesture, Cupertino-shaped switches and dialogs. Material 3 is your rulebook. You follow its components. You theme your brand through it. That is discipline.

## Layout & structure

- **Material navigation, matched to size.** You use a navigation bar (bottom, 3 to 5 destinations) on compact width. You use a navigation rail or drawer on expanded width. You never ship a phone bottom-bar untouched on a tablet.
- **System Back always works.** You honor the predictive Back gesture and the Back button. You never trap your user. You never hijack the gesture.
- **Edge-to-edge with window insets.** You apply the status bar, navigation bar, display cutout, and IME insets so content never hides behind system bars or the keyboard.
- **Top app bar for screen context**. You pair it with a FAB when the screen has a single primary action.

## Touch targets

- **48×48 dp minimum** for every touch target you ship, with at least 8 dp between them.

## Typography

- **Material type scale.** Display, Headline, Title, Body, and Label roles (large, medium, and small each). You map text to roles. You never hand-pick sizes per screen.
- **Roboto is the system face**. You theme a brand face in through the type scale, keeping body, labels, and controls legible and consistent.
- **sp units, never fixed px**, so your type follows the system font-size setting your user chose.

## Color & theming

- **Material color roles** (primary, on-primary, surface, surface-variant, secondary-container, outline, error). Role tokens resolve light, dark, and contrast variants on their own. Raw hex breaks there, so you do not use it.
- **Dynamic Color (Material You)** where it fits: you derive the scheme from the wallpaper of your user on Android 12 and later, with a static fallback.
- **Dark theme is a first-class scheme.** You design it. You test it. You never ship a quick invert.
- **Tonal elevation.** You convey elevation through the standard surface tonal levels (plus shadow where appropriate). You use no arbitrary drop shadows.

## Components & motion

- **Material components.** You use buttons (filled, tonal, outlined, and text), FAB, switches, chips, snackbars, bottom sheets, Material dialogs, and navigation bar, rail, and drawer. You never port iOS controls. You invent no equivalents.
- **One FAB, one primary action.** You never stack FABs. You never spend one on a secondary task.
- **Snackbars for transient feedback** (actionable when useful, never a toast for that). You use dialogs only for decisions that must interrupt.
- **Material motion patterns.** Container transform, shared-axis, and fade-through, with standard easing and durations. You honor the system Remove animations setting with a crossfade or instant cut.

## Verifying the build

- **Screenshots come from the emulator or a connected device, never a browser.** You build and install. Then you capture with `adb exec-out screencap -p > <path>` (pick a device with `adb -s <serial>` when several are attached). You capture every device class your app ships to, at least one phone and, when tablets are a target, one tablet. You write the files where the review flow expects them.
- **Dark theme and font scale belong in the pass.** `adb shell cmd uimode night yes` flips the theme. `adb shell settings put system font_scale 1.3` (restore `1.0` after) catches the clipped labels a fixed layout hides. With several targets attached, the capture `-s <serial>` goes on these commands too.
- **Emulators give you breadth. Gestures, refresh rates, and performance need hardware.** You say which one produced your evidence.
