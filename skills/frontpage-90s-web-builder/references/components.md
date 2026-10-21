# FrontPage component recipes

Markup for every component the kit supports. All classes come from `assets/fp-kit.css`; behaviors
marked **(JS)** come from `assets/fp-kit.js`. Copy the snippet, change the words, keep the structure.

Contents: Shared borders · Page Banner · Navigation Bar · Hover Button · Hit Counter · Marquee ·
Banner Ad Manager · Timestamp · Search Form · Feedback form + Confirmation · Contact via WhatsApp/e-mail ·
Background MIDI (click to play) · Guest Book ·
Collapsible outline · Table of contents · Boxes & tables · Under construction · WordArt · Badges 88x31 ·
Clip art & bespoke pixel art · Photo Gallery · Web ring · Frames · DHTML effects & page transitions · Period markup habits

---

## Shared borders (the FrontPage skeleton)

FrontPage's signature: every page repeats the same **top border** (page banner + nav bar), optional
**left border** (vertical nav), and **bottom border** (text nav, webmaster mail line, copyright,
last-modified). `scripts/scaffold.py` generates exactly this; when hand-building, keep the borders
byte-identical across pages — the kit's JS marks the current page's button automatically.

```html
<div class="fp-page">
<table class="fp-layout" width="100%" border="0" cellspacing="0" cellpadding="8">
<tr><td colspan="2" class="fp-border-top"> …banner… </td></tr>
<tr><td class="fp-side"> …vertical nav, counter, badges… </td>
    <td class="fp-main" id="content"> …page content… </td></tr>
<tr><td colspan="2" class="fp-border-bottom">
  <hr>
  <p class="fp-textnav">[&nbsp;<a href="index.html">Home</a>&nbsp;] [&nbsp;<a href="products.html">Products</a>&nbsp;]</p>
  <p>Send mail to <a href="mailto:webmaster@example.com">webmaster@example.com</a> with questions or comments about this web site.<br>
  Copyright &copy; 1999 Acme Widgets. All rights reserved.<br>
  Last modified: December 14, 1998</p>
</td></tr>
</table>
</div>
```
On screens under 700px the kit stacks the table cells and wraps the nav into rows — no extra work.

## Page Banner

FrontPage drew the page title onto the theme's banner graphic. Optional `<small>` tagline.
```html
<div class="fp-banner" role="banner">Acme Widgets Inc.<small>Quality widgets since 1957</small></div>
```

## Navigation Bar

Theme buttons (horizontal under the banner, or vertical in the left border):
```html
<nav class="fp-navbar" aria-label="Main">   <!-- or class="fp-navbar-v" -->
  <a class="fp-btn" href="index.html">Home</a>
  <a class="fp-btn" href="about.html">About Us</a>
  <a class="fp-btn" href="contact.html">Contact</a>
</nav>
```
Text style (bottom border): `<p class="fp-textnav">[&nbsp;<a href="…">Home</a>&nbsp;] …</p>`.
Single-page sites: point buttons at section ids (`href="#services"`); the "current page" marking only
applies to file links.

## Hover Button (JS-free)

FrontPage 97/98 made these with a Java applet; the kit emulates its effects in CSS.
```html
<a class="fp-hoverbtn" href="order.html">Order Now!</a>                       <!-- glow -->
<a class="fp-hoverbtn fp-hoverbtn--fill" href="specials.html">Specials</a>    <!-- color fill -->
<a class="fp-hoverbtn fp-hoverbtn--bevel" href="faq.html">FAQ</a>             <!-- bevel in/out -->
```
Min 130px wide, grows with the label. Keep labels to 1–3 words like the applet did.

## Hit Counter (JS)

Counts page loads **in this browser** (localStorage). Write the honest label right next to it.
```html
<p class="fp-center fp-counter-label">You are visitor number
<span class="fp-counter" data-fp-counter="home" data-digits="6">000001</span><br>
<span class="fp-note">(demo counter — counts visits from this browser only)</span></p>
```
Styles: default white-on-black, `fp-counter--led` (green LED), `fp-counter--odometer`.
`data-start="1000"` adds an offset — only for an obviously fictional/period page, never a real business.
For real global counts the user needs a server or an analytics service; say so.

## Marquee

```html
<div class="fp-marquee"><span>*** GRAND OPENING SALE — 20% OFF ALL WIDGETS THIS WEEK ONLY ***</span></div>
```
Pauses on hover/focus, becomes static text under `prefers-reduced-motion`. Speed: `style="--fp-marquee-speed:12s"`.
Like the original tag's attributes: `fp-marquee--right` (direction="right") and `fp-marquee--alternate`
(behavior="alternate", text bounces edge to edge — use a short phrase). Ticker-style news line:
put it right under the banner with `style="--fp-marquee-bg:#000080;--fp-marquee-text:#ffff00"`.
Blinking text (`<span class="fp-blink">NEW!</span>`): at most one or two per page.

## Banner Ad Manager (JS)

Rotates 2+ children every N ms (min 2.5s), pauses on hover/focus, does not rotate under reduced motion.
`.fp-ad` is the classic 468x60 banner — put it in the main column or under the banner. In the 150px left
border use 120x60 "button" ads (`.fp-ad--button`; any `.fp-ad` inside `.fp-side` shrinks automatically).
```html
<div class="fp-adrotator" data-fp-rotator="4000" aria-label="Sponsors">
  <a class="fp-ad" href="#specials" style="background:#ff0;color:#c00">CLICK HERE for this week's specials!</a>
  <a class="fp-ad" href="#contact" style="background:#000080;color:#fff">Free estimates — call 555-0199</a>
</div>
```
Every ad must link somewhere real on the site (or be a `<span>`), never to fake external sites.

## Countdown (JS)

```html
<p class="fp-center">Only <span class="fp-countdown" data-fp-countdown="2027-03-13T21:00:00-03:00"
  data-units="días|horas|min|seg" data-done="¡Es hoy!"></span> to the party!</p>
```
Always include the UTC offset of the event's city. Date but no time given: count down to the day
(`data-units="días"`, target 00:00) and flag the missing time. Only for future dates — if the date already passed
(or looks like a typo for next year), leave the countdown out and flag the date in your reply. The ticking digits are text (no motion), so they're fine
under reduced motion. Y2K countdowns on 1999-dated pages: show a fixed number as plain text instead.

## Map / directions button

FrontPage sites linked to MapQuest; today link to a map search for the exact address the user gave
(no API key, no embed, no tracking scripts). Venue name but no street address: search
"venue, city" and ask the user to confirm the address in your reply.
```html
<a class="fp-hoverbtn" href="https://www.google.com/maps/search/?api=1&query=Serrano%201146%2C%20CABA%2C%20Argentina"
   target="_blank" rel="noopener">Ver el mapa</a>
```

## Greeting (JS)

`<p class="fp-center" data-fp-greeting="¡Buenos días!|¡Buenas tardes!|¡Buenas noches!"></p>` prints a
greeting for the visitor's local time of day — a favorite 1998 JavaScript trick.

## Timestamp (JS)

`<span data-fp-timestamp="long"></span>` prints the file's real modification date in the page language
(`"short"` gives `10/21/26`). For a fictional 1998 period piece, type the date as plain text instead.

## Search Form (JS)

FrontPage's search component. The kit's version searches the current page's headings/sections.
```html
<form class="fp-form" data-fp-search="#content" data-results="search-results" role="search">
  <label for="q">Search for:</label> <input type="search" id="q" name="q" size="20">
  <input class="fp-btn" type="submit" value="Start Search"> <input class="fp-btn" type="reset" value="Reset">
  <div id="search-results" class="fp-search-results"></div>
</form>
```
Localize the result label with `data-found="Documentos encontrados:"`. Matching ignores case and accents.
Put search tips inside the `<form>` or a `class="fp-noindex"` box so they don't show up as results.

**Whole-site search** (works from file://, no server): run `python3 scripts/build_search_index.py SITE_DIR`
(writes `theme/search-index.js`; re-run after editing pages), load it before the kit, and use `site` mode:
```html
<script src="theme/search-index.js"></script> <script src="theme/fp-kit.js"></script>
<form class="fp-form" data-fp-search="site" data-results="sr" data-found="Documentos encontrados:"
      data-col-title="Documento" data-col-page="Página" data-target="main">  <!-- data-target only inside frames -->
  <label for="q">Buscar:</label> <input type="search" id="q" name="q"> <input class="fp-btn" type="submit" value="Iniciar búsqueda">
  <div id="sr" class="fp-search-results"></div></form>
```

## Feedback form + Confirmation page (JS)

FrontPage's Feedback template. Without a backend use `data-fp-demo`: on submit it shows a
FrontPage-style confirmation listing what was typed and states nothing was sent.
```html
<form class="fp-form" data-fp-demo data-confirm="fb-confirm">
  <fieldset><legend>What kind of comment would you like to send?</legend>
  <label><input type="radio" name="kind" value="Complaint"> Complaint</label>
  <label><input type="radio" name="kind" value="Suggestion" checked> Suggestion</label>
  <label><input type="radio" name="kind" value="Praise"> Praise</label></fieldset>
  <table><tr><td><label for="fb-name">Name</label></td><td><input type="text" id="fb-name" name="name" size="30"></td></tr>
  <tr><td><label for="fb-mail">E-mail</label></td><td><input type="email" id="fb-mail" name="email" size="30"></td></tr></table>
  <p><label for="fb-msg">Enter your comments in the space provided below:</label><br>
  <textarea id="fb-msg" name="message" rows="5" cols="50"></textarea></p>
  <p><input class="fp-btn" type="submit" value="Submit Comments"> <input class="fp-btn" type="reset" value="Clear Form"></p>
  <p class="fp-note">Demo form: nothing is sent. To actually receive messages, connect a form service or use the e-mail link below.</p>
</form>
<div id="fb-confirm" class="fp-confirm" hidden><b>Thank you for your feedback!</b>
  <p>This is what you entered (demo only — nothing was sent):</p><dl></dl>
  <p><a href="#content">Return to the page</a></p></div>
```
With a real endpoint (Formspree, Netlify Forms, own server), drop `data-fp-demo`, set `action`/`method`.
A plain `mailto:` link is the honest zero-backend alternative.

## Contact via WhatsApp or e-mail (JS) — the honest small-business contact form

For a real business with no form backend, this beats a demo form: the visitor fills a FrontPage-looking
form and the kit opens WhatsApp (or their mail program) with the message ready; they press send there.
```html
<form class="fp-form" data-fp-compose="whatsapp:5491100000000" data-subject="Consulta desde la web">
  <table><tr><td><label for="c-name">Nombre:</label></td><td><input type="text" id="c-name" name="nombre" size="30" required></td></tr>
  <tr><td><label for="c-car">Vehículo:</label></td><td><input type="text" id="c-car" name="vehiculo" size="30"></td></tr></table>
  <p><label for="c-msg">Consulta:</label><br><textarea id="c-msg" name="mensaje" rows="4" cols="50" required></textarea></p>
  <p><input class="fp-btn" type="submit" value="Enviar por WhatsApp"> <input class="fp-btn" type="reset" value="Borrar"></p>
  <p class="fp-note">Al enviar se abre WhatsApp con su mensaje listo; esta página no envía nada por sí sola.</p>
</form>
```
Message keys come from each field's `data-label`, else the radio/checkbox group's `<legend>`, else its
`<label>` — keep labels short. `data-fp-compose="mailto:owner@realdomain.com"` does the same with the visitor's e-mail program. Only use
numbers/addresses the user actually gave you. WhatsApp numbers are digits with country code (AR: 549 + area + number).

## Background MIDI (JS) — click to play, never autoplay

The `<bgsound>` era, minus the ambush. A square-wave chiptune via WebAudio, started and stopped by the visitor.
```html
<p class="fp-center"><button class="fp-btn" type="button" data-fp-midi="E5 D5 C5 D5 E5 E5 E5:2 D5 D5 D5:2 E5 G5 G5:2"
  data-tempo="170" data-stop-label="&#9632; Stop music">&#9834; Play background MIDI</button></p>
```
Notes = letter + optional `#`/`b` + octave 0–8 (`C4`, `F#5`, `Bb3`), `:2` = two beats, `-` = rest. Sounds best in octaves 4–6. Write an original little tune or a public-domain
melody (folk songs, classical themes) — not copyrighted pop songs.

## Guest Book (JS)

FrontPage shipped a Guest Book template. The kit saves entries in this browser only.
```html
<h2 id="guestbook">Sign My Guestbook!</h2>
<form class="fp-form" data-fp-guestbook="mysite" data-list="gb-list"
      data-thanks="Thanks for signing! (Saved in this browser only.)">
  <table><tr><td><label for="gb-name">Your name:</label></td><td><input type="text" id="gb-name" name="name" size="30" required></td></tr>
  <tr><td><label for="gb-from">Where are you from?</label></td><td><input type="text" id="gb-from" name="from" size="30"></td></tr></table>
  <p><label for="gb-msg">Comments:</label><br><textarea id="gb-msg" name="message" rows="4" cols="50" required></textarea></p>
  <p><input class="fp-btn" type="submit" value="Sign Guestbook"> <input class="fp-btn" type="reset" value="Clear"></p>
  <p class="fp-note">Local demo guestbook: entries are stored only in your browser and nobody else can see them.</p>
</form>
<div id="gb-list" class="fp-gb-entries"></div>
```
Localize every message: `data-thanks`, `data-error` (missing name/message) and `data-nostore` (browser
blocks storage), e.g. `data-error="Completá tu nombre y un mensaje."`.
Pre-filled sample entries (`<div class="fp-gb-entry">…</div>` inside the list) are fine on fictional or
personal-fun pages if labeled as samples. On a **real business** site never invent customer entries or
testimonials — that reads as fake reviews.

## Collapsible outline (FrontPage 2000 DHTML)

```html
<details class="fp-outline" open><summary>Services</summary>
  <ul class="fp-bullets"><li>Brakes</li><li>Oil change</li></ul>
</details>
```

Searchable chapters: put the heading inside the summary — `<summary><h3 id="cap3">3. Vacaciones</h3></summary>`
(the kit keeps it inline). Links and search results pointing at `#cap3` open the closed chapter automatically.

## Table of contents

FrontPage's Table of Contents component: a nested bullet list of every page/section.
```html
<ul class="fp-bullets"><li><a href="#about">About Us</a>
  <ul class="fp-bullets"><li><a href="#history">Our History</a></li></ul></li></ul>
```

## Boxes & tables

```html
<div class="fp-box"><span class="fp-box-title">What's New</span> <p>…</p></div>

<div class="fp-scroll"><table class="fp-table" border="1" cellpadding="4" cellspacing="0">
<tr><th>Service</th><th>Price</th></tr><tr><td>Oil change</td><td>$19.95</td></tr></table></div>
```
Multi-column content = a nested `<table class="fp-cols">` with `<td width="50%" valign="top">` cells, as
FrontPage users did; `fp-cols` stacks the cells on phones (a plain nested table would not).

## Under construction

```html
<div class="fp-construction"><img src="images/construction.svg" alt="" width="48" height="40">
  <b>This section is under construction.</b> Check back soon!</div>
```
Use for genuinely unfinished sections only, at most once per page.

## Photo Gallery (FrontPage 2002) — also for "photos coming later"

```html
<div class="fp-gallery">
  <figure class="fp-photo"><img src="images/team.jpg" alt="Our team at the 1998 picnic" width="160" height="120">
    <figcaption>Company picnic, 1998</figcaption></figure>
  <figure class="fp-photo"><div class="fp-photo-empty">Photo coming soon</div>
    <figcaption>[caption to add]</figcaption></figure>  <!-- TODO: photo from the user -->
</div>
```
Use real photos the user provides; for missing ones use `.fp-photo-empty` frames and list them as
placeholders. Testimonials "to be collected later" work the same way: an empty, clearly labeled box —
never sample quotes attributed to real people.

## WordArt headings

Office 97 WordArt, pasted into FrontPage as an image. Use for one big title, not body headings — in a
`<p>` (or an `<h2>`), since the Page Banner is already the page's `<h1>`.
```html
<p class="fp-center"><span class="fp-wordart fp-wordart--rainbow">The Dial-Up Tones</span></p>
```
Variants: `--rainbow`, `--chrome`, `--fire`, `--ocean`; add `fp-wordart--slant` or `--wave` for the
skewed/arched look. Plain `.fp-wordart` = yellow with hard navy shadow.

## Badges 88x31

```html
<div class="fp-badges">
  <span class="fp-badge fp-badge--gray">Best viewed<b>800x600</b></span>
  <span class="fp-badge fp-badge--black">Made with<b>Notepad</b></span>
  <a class="fp-badge" href="#guestbook">Sign my<b>Guestbook</b></a>
</div>
```
Variants: default navy, `--gray`, `--black`, `--green`, `--red`. 88x31 fits ~14 characters on the small line and ~10 on the bold `<b>` line: keep each line short
("Hecho con" / "<b>FrontPage</b>"), never a sentence. `screenshot.py` reports any badge/ad/button whose
text gets clipped. Text-only homages like
"Best viewed with Internet Explorer" or "Made with FrontPage" are fine; never copy real logos.

## Clip art

Translate the starbursts by editing the `<text>` (`NUEVO!`, `NOVO!`); for words longer than 4 letters
lower `font-size` to 8 and `textLength` to ~24 so they stay inside the burst. `assets/clipart/` holds (natural size in px): `new.svg` 52x34, `hot.svg` 46x24, `email.svg` 36x26,
`construction.svg` 48x40, `globe.svg` 32x32, `arrow.svg` 20x14. Multi-page: `scaffold.py --clipart new,email`
copies the ones you name into `images/` (don't ship unused files).
For single-file output paste the SVG inline (decorative → `aria-hidden="true"`, meaningful → keep
`role="img"` + `aria-label`). For multi-page output copy them to `images/` and use `<img alt="…">`.
`<span class="fp-spin">…globe…</span>` = the spinning globe GIF. Draw new clip art the same way:
small, flat, thick outlines, 3–5 colors, `shape-rendering="crispEdges"` for pixel feel.

### Bespoke pixel-art clip art (do this — it's what makes a page feel hand-made)

Every 90s site had a few images specific to its subject: a little car for a garage, a CD for a band,
a coffee cup for a café. For real people draw objects or generic silhouettes, not "portraits" that
invent what they look like — their own photos go in a Photo Gallery frame. Draw 1–4 of them as inline SVG on a 16x16–32x32
grid of `<rect>`s — flat colors, a dark 1px outline, no gradients — then scale them up with `width`.
```html
<svg width="64" height="32" viewBox="0 0 16 8" shape-rendering="crispEdges" role="img" aria-label="Red car">
  <rect x="4" y="1" width="7" height="2" fill="#c00"/><rect x="5" y="1" width="2" height="1" fill="#9cf"/>
  <rect x="8" y="1" width="2" height="1" fill="#9cf"/><rect x="1" y="3" width="14" height="3" fill="#c00"/>
  <rect x="14" y="3" width="1" height="1" fill="#ff0"/><rect x="3" y="5" width="3" height="3" fill="#222"/>
  <rect x="10" y="5" width="3" height="3" fill="#222"/><rect x="4" y="6" width="1" height="1" fill="#aaa"/>
  <rect x="11" y="6" width="1" height="1" fill="#aaa"/>
</svg>
```
On dark themes give the art a light outline (`#ffffff`/`#cccccc`) instead of a dark one.
Faster: draw it as a text grid and run `python3 scripts/pixelart.py art.txt --scale 4 --label "Red car"`
(see its `--help` for the grid format). Keep them small (16–96px on screen). Real photos the user provides go in a bordered table cell with a
caption, at most ~240px wide — the way a 1998 scanner photo looked.

## Web ring

```html
<table class="fp-table" align="center"><tr><td class="fp-center">
  This site is a member of the <b>Classic Cars Web Ring</b><br>
  <span class="fp-note">[ Previous | Random | Next | List Sites ]</span></td></tr></table>
```
Only link the items to real destinations; otherwise render them as plain text like above.

## Frames

`scaffold.py --layout frames --pages "inicio.html=Inicio,…"` builds this for you: `index.html` holds the
banner frame, the contents frame (buttons with `target="main"`, current one highlighted on click) and
`<iframe name="main">`; every page also opens on its own with a "[ View with frames ]" link that hides
itself inside the frame. Two honest options:
1. **Real frames feel for multi-page sites** — a contents column with `target="main"` links and an
   `<iframe name="main" class="fp-frame-target" src="home.html" title="Main content">`, inside
   `.fp-frameset` (`.fp-frame--banner`, `.fp-frame--contents`, `.fp-frame`). Every framed page must
   also work on its own (it is what search engines and phones open).
2. **Single page** — the same `.fp-frameset` grid with scrolling panes and anchor links, no iframe.
Never use `<frameset>`.

## DHTML effects & page transitions

- `<body class="fp-transition">` = FrontPage's "Page Enter: Blend" transition (fade in once).
- `class="fp-flyin"` / `fp-flyin--right`, delays `fp-flyin--d1..d3` = "Fly in from left/right" on load.
- `<span class="fp-spin">` = spinning GIF.
All are disabled under `prefers-reduced-motion`. Use one or two effects per page, not all of them.

## Period markup habits (what FrontPage actually wrote)

Mixing these into your HTML is what makes the source and the rendering feel 1998. They all still render:
`<p align="center">`, `<div align="center">`, `<font face="Verdana, Arial" size="2" color="#000080">`,
`<b><font size="5">`, `<table border="0" cellpadding="0" cellspacing="0" width="100%">`,
`<td width="150" valign="top" bgcolor="#C0C0C0">`, `<img border="0" width="88" height="31">`,
`&nbsp;&nbsp;&nbsp;` indents, `<br clear="all">`, `<hr size="1" noshade>`, `<center>`.
Prefer the kit classes for anything themed (colors, buttons) so the theme stays coherent; use the
period attributes for alignment, sizes, and small one-off color accents.
