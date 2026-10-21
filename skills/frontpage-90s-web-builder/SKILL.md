---
name: frontpage-90s-web-builder
description: Build or restyle websites so they look made with Microsoft FrontPage 97/98/2000 — FrontPage-style themes (Blueprint, Expedition, Industrial, Citrus Punch…), shared borders, navigation bars with beveled theme buttons, page banners, hover buttons, hit counters, marquees (marquesinas), guestbooks, feedback forms with confirmation pages, banner ad rotators, table layouts, tiled backgrounds, 88x31 badges and under-construction signs — delivered as self-contained HTML that still works offline, on phones and in modern browsers. Use this whenever someone wants a retro, vintage, 90s, late-90s, Y2K-era, "web 1.0", GeoCities/Angelfire/Tripod or "old internet" website, homepage, landing page, fan site, intranet, invitation or joke page, wants to convert a modern page into that look, or says things like "como si fuera de 1998", "estilo FrontPage", "web retro de los 90", "hecha con FrontPage" — even if they never say the word FrontPage.
---

# FrontPage 90s Web Builder

Make pages that someone who used FrontPage in 1998 would recognize instantly — the theme, the
shared borders, the beveled navigation bar, the hit counter — while the page itself is honest,
accessible and works in any modern browser with no plugins, servers or network access.

The bar is: **at first glance it is a late-90s FrontPage site; on closer use nothing is broken or fake.**

## What's in this skill

- `assets/fp-kit.css` + `assets/fp-kit.js` — every component (nav bars, hover buttons, counter,
  marquee, guestbook, search, ad rotator, demo forms, badges, frames, effects) plus mobile stacking
  and reduced-motion handling. Theme-neutral; driven by `--fp-*` CSS variables.
- `assets/themes/*.css` — 10 coherent themes. `python3 scripts/scaffold.py --list-themes` lists them.
- `assets/clipart/*.svg` — NEW!, HOT!, e-mail, construction, globe, arrow.
- `scripts/scaffold.py` — generates the page(s) with theme, kit, shared borders and nav already wired.
- `scripts/build_search_index.py` — whole-site index for the Search Form (works offline/file://).
- `scripts/pixelart.py` — text grid → crisp pixel-art SVG for bespoke clip art.
- `scripts/check_site.py` — QA: broken anchors/files, network assets, alt text, motion, honesty
  labels, modern-design smells. `scripts/screenshot.py` — headless Chrome screenshots (desktop + phone).
- `references/components.md` — copy-paste markup for every component. Read it before building.
- `references/themes-and-eras.md` — theme picker, FrontPage 97/98/2000/2002 differences, personas,
  period phrases (EN/ES). Read it when choosing a theme or when the user names a year/version.

Paths below are relative to this skill's directory.

## Workflow

1. **Read the brief.** Pull out the real content (names, services, prices, hours, links, language),
   the era (default FrontPage 98, ~1998) and who "built" it (small business, teenager, school,
   intranet). Only ask a question if a missing fact would make the first draft useless — otherwise
   choose and say what you chose.
2. **Pick one theme** from `references/themes-and-eras.md` that fits the subject. Commit to it; a
   coherent theme is what separates "FrontPage site" from "random 90s collage".
3. **Plan the structure the FrontPage way**: Home plus a few pages (or one page with sections), a
   navigation bar generated from that structure, shared top/left/bottom borders repeated everywhere.
   Single file by default; multiple pages when the user asks for a site with pages, or when the
   content clearly needs it (e.g. 4+ substantial sections).
4. **Scaffold**, then write content into the placeholders:
   ```bash
   python3 scripts/scaffold.py OUT_DIR --theme citrus-punch --title "Panadería La Espiga" --lang es --era 98 \
     --pages "index.html=Inicio,productos.html=Productos,contacto.html=Contacto" --phone "+54 11 4000-0000" --clipart new
   # single page with sections:  --sections "about=About Me,links=Cool Links,guestbook=Guestbook"
   # options: --layout left|top|frames  --tagline "…"  --email (only a real one)  --owner "Acme Inc."
   #          --year 2026 (real businesses: the real year)  --updated "14/12/1998" (fictional pages)  --mode inline|shared
   ```
   Replace every `<!-- FP:CONTENT … -->` block (and `FP:SIDEBAR` if useful) using recipes from
   `references/components.md`. The Page Banner is each page's `<h1>`: start content with `<h2>`.
   Building by hand is fine too — then inline `fp-kit.css`, one theme file and `fp-kit.js` yourself
   (single page) or link them from a `theme/` folder (multi-page).
5. **Decorate to the brief.** Besides the skeleton (banner, nav bar, shared borders), pick the 4–7
   period components that suit the persona — dense, compact, a bit naive, but readable. When the user asks for "max cheese", "as 90s as
   possible", a joke or fan page, go loud (10–15 components, blinking NEW!, MIDI button, spinning
   globe…) — the user's request wins over restraint — but keep one theme and keep body text legible.
6. **QA — always run it, fix every ERROR, judge every WARN:**
   ```bash
   python3 scripts/check_site.py OUT_DIR
   python3 scripts/screenshot.py OUT_DIR/index.html --out /tmp/fp-shots   # needs Chrome/Chromium/Edge
   ```
   Add `--print` when the page will be printed (recipes, price lists, menus) and read the PDF.
   `screenshot.py` renders 1024px and a true 390px phone width, prints `OVERFLOW … Culprits:` if
   anything sticks out sideways, and keeps the PNGs out of the deliverable. Fix overflow, then look at
   the PNGs (or open the page in a browser tool): does it read as FrontPage at a glance? Is every
   text legible over its background (notes inside gray forms, links on dark themes)? Do badges, ads and
   hover buttons fit their boxes? Check every page of a multi-page site, not just the home page.
7. **Deliver** the files, the chosen theme/era in one line, which features are demo/local-only, and
   how to open it (double-click `index.html`). ZIP multi-file sites if the user wants a download.
   If it will be shared as a link (invitations, real businesses), say it needs hosting — GitHub Pages,
   Netlify Drop or any static host works, since everything is plain files — and add `og:title` /
   `og:description` meta tags (`scaffold.py --description "…"`) so WhatsApp and social previews look right.
   Respond in the user's language; site copy follows the language the user wants for the site.

## What makes it read as *FrontPage* (not just "90s")

Use these signatures; most pages need the first four:
- **A theme**: matching background tile, banner, buttons, bullets, horizontal rule and heading colors.
- **Shared borders**: same banner + nav bar on every page, and the bottom border with
  `[ Home ] [ Products ]` text links, "Send mail to webmaster@… with questions or comments about this
  web site.", copyright and "Last modified:".
- **Navigation bar of theme buttons**, current page highlighted (the kit does it automatically).
- **Table layout** ~760px centered, 150px left column, compact `cellpadding`, `align`/`valign` attributes.
- **Components** as FrontPage named them: Page Banner, Hover Button, Hit Counter, Marquee, Banner Ad
  Manager, Search Form, Feedback Form + confirmation page, Guest Book, Timestamp, Table of Contents,
  collapsible outline, page transition, DHTML fly-in.
- **Hand-made images**: 1–4 bespoke pixel-art SVGs of the subject (the garage's car, the band's CD,
  the café's cup), plus kit clip art (NEW!, e-mail, construction) and maybe one WordArt title.
- **Period copy and markup**: "Welcome to our Home Page!", `<font face="Verdana" size="2">`,
  `<p align="center">`, `&nbsp;` indents. The source should look 1998 too — someone will View Source.

## Modern-site-in-costume tells (avoid unless the user asks)

Rounded cards, soft blurred shadows, big hero photos, oversized whitespace, glassmorphism,
smooth gradients everywhere, hamburger menus, sticky headers, web fonts (Inter, Poppins…), emoji,
icon fonts, CSS-grid card galleries, "trusted by" logo strips. Use installed fonts (Times New Roman,
Arial, Verdana, Trebuchet MS, Georgia, Book Antiqua, Comic Sans MS, Courier New, Impact), bevels,
1–2px borders, tiled backgrounds, GIF-style SVG clip art, and ★ ► ✉ ☎ symbols instead of emoji.

Modern concessions that stay invisible are good: the viewport meta, the kit's stacking under 700px,
`:focus-visible` (styled as the IE dotted focus box), semantic `<nav>`/`<h1>`, reduced-motion.

## Facts the user didn't give you

Never fill a real person's or business's site with invented facts that look real. Missing prices,
e-mails, staff names, years in business: either leave them out, or use an obvious placeholder
(`$ XX.XXX`, `[su e-mail]`) marked with an `<!-- EDITAR / TODO -->` comment, and list every placeholder
in your reply. Don't invent `@example.com` addresses or `555` numbers for a real business (the
scaffold omits the mail line unless you pass `--email`); contact details the user gave you are used
exactly as given. Pass phones with the country code when you know it (`+54 341 …`) so `tel:` and
WhatsApp links work from anywhere. `check_site.py` lists every leftover `TODO`/`EDITAR`/`$ XX`/`[ … ]`
placeholder so you can report them. Fictional pages (a band that doesn't exist, a theater-prop
intranet) can invent freely — that's the point; give invented e-mails and URLs a reserved domain
(`@porvenir.test`, `www.empresa.example`) so they can never reach a real one.

Sanity-check the facts you were given: a weekday that doesn't match its date, an event date already
in the past or an anniversary count that doesn't match the year ("25 years since 2001" in 2025), an end
time before the start, a phone missing digits. Don't silently "fix" them — keep the user's version or
leave the weekday out, and flag the mismatch in your reply.

## Honesty rules (these protect the user, keep them)

A retro page is a costume for the *design*, not for the *facts*. People will actually use these pages.
- **Counters** count this browser only (localStorage) and must say so near the digits. A starting
  offset is only OK on an obviously fictional page. Real global counts need a server — say that.
  These labels exist to protect real visitors; on a pure prop (a theater set, a film screen, a
  screenshot for a joke) the label can be tiny or moved to a `title` tooltip, and you say so in the reply.
- **Guestbook / forms** without a backend: guestbook entries are local-only and labeled. For a real
  business contact form prefer `data-fp-compose` (opens WhatsApp or the mail app with the message
  ready, using the user's real number/address); for fictional pages `data-fp-demo` (FrontPage
  confirmation page that says nothing was sent). Never claim a message was sent. If the user gives
  a real form endpoint, wire it for real and keep it.
- **Shared guestbooks / comments** need a third-party service or a server; offer that as a next step
  instead of pretending the local one is shared. **Real private people** (grandma's bio, staff
  profiles): write only what the user told you; leave the rest as a marked placeholder.
- **No invented social proof for real entities**: no fake testimonials, guestbook entries from
  "customers", awards, press quotes or visitor numbers for a real business. Fictional/personal joke
  pages can have sample entries if labeled as samples.
- **Links go somewhere real**: anchors to existing ids, local files that exist, URLs the user gave.
  Web rings and ads link only to real destinations, otherwise render as plain text.
- **Dates**: "Last modified" is either the real file date (`data-fp-timestamp`) or a clearly
  period/fictional date the user wants. Don't make a live business look abandoned unless asked.
- **No impersonation**: badges and themes are homages; don't copy real logos or pretend to be
  Microsoft/Netscape. If a fictional company name matches a real one, use no branding of theirs and
  mention the clash in one line. No auto-playing audio, pop-up alerts, or links to obsolete plugins.

## Accessibility & compatibility (non-negotiable but invisible)

Contrast that a 1998 user would also find readable (busy tiles go behind a solid panel); `alt` on
every image (`alt=""` for decoration); keyboard-reachable nav with visible focus; motion only via kit
classes (they respect `prefers-reduced-motion`); blinking at most one or two small items; data tables
wrapped in `.fp-scroll`; no `<frameset>`, Java, ActiveX, Flash, `<bgsound>` or FrontPage Server
Extensions — the kit replaces each of them with a working equivalent.

## Converting an existing modern page

Keep all the real content, links, form endpoints and the real copyright year (a real person's or
business's page with no year: the current year), then map: hero → Page Banner + centered welcome
paragraph; nav → navigation bar of theme buttons; feature cards → a 2–3 column table with bullet lists and
small clip art; CTA buttons → hover buttons or bevel buttons; pricing → bordered `fp-table`;
testimonials → keep only real ones, as a boxed quote list; signup/contact form → Feedback form
(real endpoint if the original had one, else demo); footer → bottom shared border. Drop web fonts,
icon fonts, shadows, rounded corners and stock hero photos (or shrink a real product photo to a
bordered 200px image with a caption, the way 1998 did it). A one-page landing can stay one page with
anchor navigation, or split into Home + 3–5 pages if that's what a FrontPage webmaster would have
done with that much content — either is fine; say which you chose. Then prove nothing was lost:
`python3 scripts/check_site.py OUT_DIR --source original.html` lists every passage of the original that
no longer appears — rewording a heading is fine, dropping a sentence is not. If the retro copy is a
fun duplicate of a live page (easter egg), link back to the real one and add
`<meta name="robots" content="noindex">` so search engines don't index two copies.

## Example requests

- "Hazme la web de mi taller mecánico como si la hubiera hecho mi sobrino con FrontPage 98."
- "Make me a GeoCities-style fan page for my band with a guestbook and a hit counter."
- "Convert this landing page HTML into a FrontPage 2000 corporate site with the Blueprint theme."
- "Una invitación de cumpleaños retro, estilo internet de los 90, de una sola página."
