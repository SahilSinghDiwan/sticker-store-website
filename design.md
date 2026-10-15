# Design — Sticker Shop

A locked design system for this app. Every page redesign reads this file before
emitting code. Do not regenerate per page — extend or amend this file when the
system needs to grow.

## Genre
playful (atelier / print-studio voice)

## Mood
artistic — craft paper, ink, screen-print vermillion; sticker-sheet energy

## Macrostructure family
- Marketing / auth pages: Photographic studio split (brand panel + form)
- App pages (shop, cart, orders, profile): Workbench — product-forward, irregular rhythm
- Admin pages: denser Workbench — same tokens, tighter spacing, no enrichment

## Theme
- `--color-paper`   oklch(96% 0.02 85)
- `--color-paper-2` oklch(93% 0.025 80)
- `--color-ink`     oklch(22% 0.03 280)
- `--color-ink-2`   oklch(45% 0.02 280)
- `--color-rule`    oklch(82% 0.02 85)
- `--color-accent`  oklch(58% 0.19 35)
- `--color-accent-ink` oklch(98% 0.01 85)
- `--color-focus`   oklch(50% 0.16 250)
- `--color-wash`    oklch(92% 0.04 210)

## Typography
- Display: Fraunces, weight 600–700, style normal
- Body:    DM Sans, weight 400–500
- Mono:    IBM Plex Mono, weight 400–500
- Display tracking: -0.02em
- Type scale anchor: `--text-display` = clamp(2.25rem, 5vw, 3.5rem)

## Spacing
4-point named scale in `Frontend/src/tokens.css`. Pages must use named tokens
(`var(--space-md)`), never raw values where avoidable.

## Motion
- Easings: `--ease-out` cubic-bezier(0.16, 1, 0.3, 1)
- Reveal: fade + slight translate on product images only
- Reduced-motion: opacity-only, ≤ 150 ms

## Microinteractions stance
- silent success preferred; toasts for errors / async cart only
- hover delay 800 ms · focus delay 0 ms
- no `hover:scale-105` on cards; 1px press on buttons instead

## CTA voice
- Primary: flat vermillion fill (`--color-accent`), radius 6px, no soft shadow
- Secondary: ink outline on paper, hairline rule
- Copy pattern: short verbs — "Add", "Sign in", "Checkout"

## Nav / footer
- Nav: N5 floating pill
- Footer: Ft2 inline colophon (no 3-column sitemap)

## Per-page allowances
- Auth / marketing MAY use a studio brand panel (typography + grain, no stock photos invented)
- App pages MUST NOT use enrichment beyond product imagery
- Admin: tokens only, denser spacing

## What pages MUST share
- Wordmark: "Sticker Shop" in display face
- Accent ≤ ~5% of viewport
- Fraunces + DM Sans + IBM Plex Mono
- CTA voice (fill, radius, padding rhythm)

## What pages MAY differ on
- Macrostructure within family
- Auth studio panel composition
- Product grid density

## Exports

### tokens.css
See `Frontend/src/tokens.css` — source of truth for runtime.

### Hallmark stamp format
```css
/* Hallmark · genre: playful · macrostructure: <name> · design-system: design.md · designed-as-app · mood: artistic */
```
