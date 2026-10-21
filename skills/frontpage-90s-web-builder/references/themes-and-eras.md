# Themes, eras and personas

## Pick a theme (assets/themes/*.css)

| Theme | Feel | Reach for it when |
|---|---|---|
| `classic` | gray desktop, white panel, navy masthead, gray bevel buttons ("no theme") | small business, school, club, "my uncle's company site", any doubt |
| `blueprint` | drafting grid, navy ink, outlined caps buttons | engineering, architecture, IT, consultants, B2B |
| `expedition` | khaki parchment, browns, Book Antiqua | travel, outdoors, history, family businesses, workshops, wineries |
| `industrial` | diamond plate, hazard stripes, Impact | mechanics, construction, hardware, metalwork, gaming clans |
| `citrus-punch` | orange + lime on cream, Trebuchet | cafés, juice bars, kids, camps, parties, summer events |
| `sumi-painting` | rice paper, ink brush banner, red seal | restaurants, tea, martial arts, poetry, quiet portfolios |
| `romanesque` | marble, burgundy + gold, Palatino caps | law, churches, museums, weddings, hotels, fine dining |
| `network-blitz` | midnight circuit board, neon green, Courier | hackers, LAN parties, ISPs, sci-fi, tech fan pages |
| `capsules` | pale blue, glossy pill buttons, Verdana | clinics, software, services, newsletters, FP2000 corporate |
| `starfield` | black stars, neon, Comic Sans, rainbow rule | GeoCities personal pages, fan sites, hobby shrines, joke pages |

Names like Blueprint/Expedition/Industrial are homages to the feel of FrontPage's bundled themes,
recreated from scratch in CSS/SVG — describe them as "inspired by", not as the original files.

**Customizing:** keep the theme file and override `--fp-*` variables in `theme/site.css` (multi-page,
created by the scaffold) or the page `<style>` block (single page). Swap one color *role* consistently —
e.g. a brand maroon replacing navy everywhere navy appears (`--fp-banner-bg`, `--fp-h`, `--fp-table-head`,
`--fp-btn-current-bg`…) — rather than sprinkling unrelated colors: FrontPage themes were coherent sets,
and that coherence is what reads as "a theme" instead of chaos.
**New theme:** copy the closest file, rename, adjust variables + the tile SVG. Keep every tile tiny
(16–120px) and low-contrast behind body text.

## Eras (when the user names a year or version)

- **FrontPage 97 (1996–97)** — Times body, gray `#C0C0C0` or white backgrounds, plain bullet lists,
  `<hr>`, few images, Hover Buttons, Marquee, Hit Counter, "Under Construction", Netscape-vs-IE badges.
  Themes barely exist yet → `classic` or `starfield`.
- **FrontPage 98 (1997–99)** — Themes arrive (Blueprint, Expedition, Industrial, Citrus Punch, Sumi
  Painting…), shared borders with navigation bars and page banners everywhere, Banner Ad Manager,
  Search Form, Feedback/Guest Book templates, DHTML fly-ins, page transitions. **Default era.**
- **FrontPage 2000 (1999–2001)** — Verdana/Tahoma 10pt body, more white space (still compact), theme
  CSS files, collapsible outlines, Capsules-style glossy buttons, "Best viewed with IE 5" era.
- **FrontPage 2002/2003 (2001–03)** — Photo Gallery component, more corporate tables, early
  web-standards polish. Still tables, still no rounded cards or big hero photos.

## Personas (who "made" the site)

Write the copy and choose density as if a specific person built it in a weekend:
- **Small-business owner / nephew-built site** — proud, a bit formal ("Welcome to our Home Page!"),
  hours/prices/phone up top, "Click here for directions", Feedback form, last-modified line.
- **Teenager's personal homepage** — loud theme, "Welcome to my corner of the Web!", about me, cool
  links, guestbook, web ring, counter, "best viewed in 800x600", a blinking NEW!.
- **School / club webmaster** — news box, events table, officers list, "e-mail the webmaster",
  under-construction notice on one section.
- **Corporate intranet (FP2000)** — capsules/blueprint/classic, frames or left nav, department
  tables, search form, collapsible policy outline, very little decoration.

## Period voice cheat-sheet

Use 2–4 of these per page, adapted to the user's language — not all of them:
"Welcome to our Home Page!" · "You are visitor number…" · "This site is best viewed at 800x600" ·
"Click here!" · "Please sign our guestbook" · "Bookmark this page!" · "What's New?" ·
"Last updated:" · "Send mail to the webmaster" · "Under construction — check back soon!" ·
Spanish: "¡Bienvenidos a nuestra Página Principal!", "Usted es el visitante número…", "¡Firme nuestro
libro de visitas!", "Haga clic aquí", "Lo nuevo", "Agréguenos a sus Favoritos", "Página en construcción".
Real facts the user gave (address, hours, prices, names) always win over flavor text.
