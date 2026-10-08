# Worst-Case Catalog

You get realistic values that break UI, grouped by what kind of value your component renders. You use the rows that fit the fields in your Phase 1 table. Each value is something a real user of yours could produce. The note tells you what it tends to break.

You use `example.com`, `example.org`, or `.test` domains for your emails and URLs, so your fixture never points at a real inbox or site.

---

## People and names

| Value | Breaks |
| --- | --- |
| `Aleksandra Wiśniewska-Kowalczyk` | Long and hyphenated with diacritics. It wraps to two lines in your UI, and your hyphen becomes a line-break point |
| `Christopher Alexander Montgomery III` | Long with a suffix. Naive first plus last initials give you `CI` in your UI |
| `Konstantin Oberhauser-Wettstein` | Long and compound. It overflows your single-line rows |
| `Jo` | Two letters. It leaves your name column mostly empty, and naive initials give you `J` |
| `J` | One letter. You get single-character initials and a very short click target if your name is the link |
| `Ólafur Darri Ólafsson` | Leading accented capital. It tests your uppercase and sort logic, initials `ÓÓ` |
| `Đặng Thị Ngọc Hân` | Stacked Vietnamese diacritics. Tight `line-height` + `overflow: hidden` clips them in your UI |
| `王秀英` | CJK with no spaces. Your "first + last word" initials logic finds one word, and CJK breaks anywhere |
| `نور الهدى عبد الرحمن` | RTL. Your punctuation and icons land on the wrong side without `dir="auto"` |
| `Seán O'Brien-Ó Súilleabháin` | Apostrophe and accents. They test your escaping, your initials, your search |
| `María José de la Cruz y Fernández` | Lowercase particles. You get initials `Md` or `MF`, and sorting by "last name" gets hard |
| `dana` | All lowercase. Your initials should still read uppercase |
| `🦊 Fox` | Emoji first. Your `.charAt(0)` returns half a surrogate pair (`�`) |
| `👩🏽‍💻 Priya` | ZWJ emoji sequence. Your `.length` reads 7+, and slicing breaks it into pieces |
| `  Sam   Lee ` | Leading, trailing, and repeated spaces. You get initials from empty words and odd gaps in your UI |
| *(missing)* | No name at all, only an email. Your UI must fall back to something you chose on purpose |

## Emails, URLs, identifiers

Unbreakable strings for your work: they carry no spaces, so your browser finds nowhere to wrap them.

| Value | Breaks |
| --- | --- |
| `bartholomew.fitzgerald@northwind-industries-holdings.example.com` | The classic for your UI. It pushes every sibling off your row without `overflow-wrap: anywhere` |
| `a@b.co` | Shortest realistic case. Your layout that assumed a long email looks empty |
| `first.last+billing-notifications@example.com` | Plus-addressing. Your validation that rejects `+` fails it, and your display truncates the meaningful part |
| `ops@sub.department.region.example.co.uk` | Many subdomains with a two-part TLD. It tests your "domain" extraction logic |
| `https://example.com/workspaces/acme/projects/q3-launch/docs/9f8e7d6c5b4a?tab=comments&filter=unresolved` | Long URL. It overflows your box, and end-truncation hides the part that differs for your user |
| `9f8e7d6c-5b4a-4c3d-8e2f-1a0b9c8d7e6f` | UUID. It needs your monospace width thinking, a middle-truncation candidate |
| `Q3 Board Deck — FINAL (revised) v12 [approved by legal].pdf` | File name. End-truncation hides your version and extension, with brackets and dashes in your paths |
| `IMG_20250914_183022_HDR_portrait_edited_edited.HEIC` | Camera file name. Unbreakable in your UI, with an uppercase extension |
| `@a` / `@thisisaverylongusernamethatisallowed` | Handle extremes. You test both ends in your work |

## Labels, titles, and copy from data

| Value | Breaks |
| --- | --- |
| `Senior Product Design Engineer, Platform Infrastructure` | Long job title. It wraps to three lines in your secondary slot |
| `Invitation expired 12 days ago` | Long status badge. It wraps in your UI or it squeezes your name column |
| `Benachrichtigungseinstellungen` | German compound (30 chars, no spaces). It overflows your label and it will not break |
| `Paramètres de confidentialité et de sécurité` | French expansion of "Privacy & security". Your UI copy runs ~30% longer in translation |
| Twelve tags on one item: `design`, `frontend`, `q3`, `urgent`, `needs-review`, … | Tag rows that wrap into a wall in your work. You need a `+8` overflow |
| A tag named `customer-feedback-from-enterprise-onboarding` | One tag wider than its container in your layout |
| `Untitled` / empty string / `   ` | Title missing. You get a collapsed heading and a zero-height row |
| `<script>alert(1)</script>` / `&amp;` / `**bold**` | Escaping. You must render it as literal text for your user |
| `Line one` + newline + `Line two` | Newline in a single-line field. It doubles your row height or it drops silently |
| A 2,000-character pasted description | Clamps, "show more", and textarea growth. You plan all three in your work |

## Numbers and money

| Value | Breaks |
| --- | --- |
| `0` | Zero states for your user: "0 members", empty progress bar, division by zero in percentages |
| `1` | Plurals. You owe your user "1 members" fixed, and "1 days ago" fixed |
| `1284` | Needs a thousands separator in your UI: `1,284` |
| `1000000` | Width of your count badge. You consider compact form `1M` where precision does not matter to your user |
| `12345678.9` as currency | `$12,345,678.90`. It overflows your totals columns |
| `-42.5` | Negative sign. It tests your red color logic and parentheses in accounting formats |
| `0.1 + 0.2` | `0.30000000000000004` rendered raw. You never show this to your user |
| `142%` / `-3%` | Progress bars and meters past their bounds in your work |
| `null` / `undefined` / `NaN` | Rendered literally. You guard them before your user sees them |
| `1.284` in `de-DE` vs `1,284` in `en-US` | Locale formatting. Your hardcoded separators fail half the world |
| A value that changes live (`99` → `100`) | Width jump and jitter in your UI without `tabular-nums` |

## Collections

| Value | Breaks |
| --- | --- |
| 0 items | The empty state. You ask whether one exists at all in your work |
| 1 item | Grids that look broken with one card in your UI. "1 of 1" |
| Exactly page size, and page size + 1 | Off-by-one in "Showing 40 of 40". Your pagination shows an empty page 2 |
| 1,000+ items, unpaginated | Scroll performance, render time, memory. Your copy reads "Showing 40 of 1,284" |
| One item 10× the size of the others | Masonry and grid rows stretching to your tallest item |
| Items with identical names | Lists where the name is the only distinguishing field for your user |

## Time

| Value | Breaks |
| --- | --- |
| Now | "0 seconds ago" instead of "just now" for your user |
| 12 days ago, 11 months ago, 3 years ago | Relative-time thresholds. You switch to an absolute date after a week or so |
| A future date | "in 3 days" against "-3 days ago". You pick the honest one |
| `1970-01-01` | A zero timestamp shown as a real date. You catch it before your user trusts it |
| `2025-12-31T23:30:00-08:00` | Shows as a different day in UTC and in the timezone of your user |
| Very long duration (`1,284 hours`) | Duration formatting that never rolls up to days in your UI |

You use `Intl.RelativeTimeFormat` and `Intl.DateTimeFormat` in your work, not hand-built strings.

## Images and media

| Value | Breaks |
| --- | --- |
| Avatar URL that 404s | Broken-image icon instead of the initials fallback |
| No avatar at all | The fallback itself: initials, color, size parity with real avatars |
| 4000×200 panorama as avatar or cover | Distortion without `object-fit: cover` |
| 200×4000 tall image | Same, other axis; can also blow out a card's height |
| Transparent PNG logo, dark logo on dark mode | Invisible on the background |
| Slow-loading image | Layout shift without fixed dimensions or `aspect-ratio` |

## States

| Value | Breaks |
| --- | --- |
| Loading | Skeletons that don't match final layout, spinners that shift content |
| Error from the API | No error state, or a raw error message (`TypeError: Cannot read properties of undefined`) |
| Partial data | Some optional fields filled, others not, in the same list; misaligned rows |
| Every status at once | All enum values in one list (`active`, `invited`, `expired`, `suspended`); badge widths vary |
| No permission | Disabled actions; does the row still lay out the same? |
| The current user in the list | "You" labels, actions that shouldn't apply to yourself |

## Environment

Not data, but checked the same way: flip to the worst case, then change these.

| Condition | Breaks |
| --- | --- |
| Container at 320px | Every overflow above, at once |
| Narrow sidebar placement | Components designed full-width, reused in a 280px column |
| 2560px wide | Lines too long to read, content stranded on one side |
| Browser zoom 200% / large text setting | Fixed heights that clip growing text |
| Dark mode | Hardcoded colors, invisible borders and logos |
| `dir="rtl"` | Icons, chevrons, padding, and the order of trailing actions |
| Touch device | Hover-only actions (the ••• that appears on hover) are unreachable |
