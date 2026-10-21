#!/usr/bin/env python3
"""QA a FrontPage-style site: broken links, offline assets, accessibility basics, honesty labels,
and "modern site in a 90s costume" smells.

  python3 check_site.py path/to/site_or_page.html [--strict] [--source original.html]

--source: for conversions, lists every text passage of the original page that no longer appears
anywhere in the new site (so nothing real gets lost in the restyle).

Exit code 1 if any ERROR (or any WARN with --strict). Stdlib only.
"""
import os
import re
import sys
from html.parser import HTMLParser

EMOJI = re.compile('[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-⛿✀-➿]')
# characters in the Misc Symbols ranges that existed in 1990s fonts and read as period-correct
PERIOD_SYMBOLS = set('★☆☎☺☻♠♣♥♦♪♫☼►◄▲▼✓✔✗✘✉✈☐☑☒♀♂☞☜✂✍✎✏✶✦✧❖❤')
MODERN_FONTS = re.compile(r'\b(Inter|Roboto|Poppins|Montserrat|Open Sans|Lato|Nunito|Space Grotesk|IBM Plex|DM Sans|Manrope|system-ui|-apple-system|BlinkMacSystemFont|SF Pro|Segoe UI Variable)\b', re.I)
COUNTER_HINT = re.compile(r'visit|visita|contador|counter|besucher|visiteur', re.I)
HONEST_HINT = re.compile(r'local|demo|este navegador|this browser|ce navigateur|neste navegador|ficticio|fictional|ilustrativ|decorativ', re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets, self.imgs_no_alt, self.tags = set(), [], [], [], {}
        self.meta_viewport = self.meta_charset = False
        self.text, self.styles, self.scripts, self.inline_style_attrs = [], [], [], []
        self._in = None
        self.classes, self.attrs_seen = set(), set()
        self.forms = []
        self.autoplay = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        for k in ('id', 'name'):
            if a.get(k) and (k == 'id' or tag in ('a', 'map')):
                self.ids.add(a[k])
        for c in (a.get('class') or '').split():
            self.classes.add(c)
        for k in a:
            if k.startswith('data-fp'):
                self.attrs_seen.add(k)
        if a.get('style'):
            self.inline_style_attrs.append(a['style'])
        if tag == 'meta':
            if (a.get('name') or '').lower() == 'viewport':
                self.meta_viewport = True
            if 'charset' in a or 'charset' in (a.get('content') or '').lower():
                self.meta_charset = True
        if tag in ('a', 'area') and a.get('href') is not None:
            self.links.append((tag, a['href'], a))
        if tag == 'img':
            if a.get('src'):
                self.assets.append(('img', a['src']))
            if 'alt' not in a:
                self.imgs_no_alt.append(a.get('src', '?'))
        if tag == 'script' and a.get('src'):
            self.assets.append(('script', a['src']))
        if tag == 'link' and a.get('href') and 'stylesheet' in (a.get('rel') or ''):
            self.assets.append(('stylesheet', a['href']))
        if tag in ('iframe', 'frame', 'embed', 'source', 'audio', 'video') and a.get('src'):
            self.assets.append((tag, a['src']))
        if tag == 'form':
            self.forms.append(a)
        if tag in ('audio', 'video', 'bgsound') and (tag == 'bgsound' or 'autoplay' in a):
            self.autoplay = True
        if tag in ('style', 'script'):
            self._in = tag

    def handle_endtag(self, tag):
        if tag in ('style', 'script'):
            self._in = None

    def handle_data(self, data):
        if self._in == 'style':
            self.styles.append(data)
        elif self._in == 'script':
            self.scripts.append(data)
        else:
            self.text.append(data)


def is_external(url):
    return bool(re.match(r'^(https?:)?//', url, re.I))


def local_target(base_dir, url):
    path = url.split('#')[0].split('?')[0]
    if not path or re.match(r'^[a-z][a-z0-9+.-]*:', path, re.I):
        return None
    return os.path.normpath(os.path.join(base_dir, path))


pages_src = {}


def check(path, pages_cache):
    out = []
    E = lambda m: out.append(('ERROR', m))
    W = lambda m: out.append(('WARN', m))
    I = lambda m: out.append(('INFO', m))
    base = os.path.dirname(path)
    p = pages_cache[path]
    css = '\n'.join(p.styles)
    for kind, url in p.assets:
        if kind == 'stylesheet' and url.endswith('.css'):
            tgt = local_target(base, url)
            if tgt and os.path.exists(tgt):
                css += '\n' + open(tgt, encoding='utf-8', errors='replace').read()
    css_all = css + '\n' + '\n'.join(p.inline_style_attrs)
    js = '\n'.join(p.scripts)
    text = ' '.join(p.text)

    if not p.meta_charset:
        W('no <meta charset="utf-8"> — accented text may break')
    if not p.meta_viewport:
        E('no <meta name="viewport"> — the page will render tiny on phones')

    # links
    for tag, href, attrs in p.links:
        if href.startswith('#'):
            if href not in ('#', '#top') and href[1:] not in p.ids:
                E('anchor %s has no matching id/name on this page' % href)
            elif href == '#' and 'role' not in attrs:
                W('link with href="#" goes nowhere — give it a real target or make it a <span>')
            continue
        tgt = local_target(base, href)
        if tgt:
            if not os.path.exists(tgt):
                E('link to missing local file: %s' % href)
            elif '#' in href and tgt.endswith(('.html', '.htm')) and tgt in pages_cache:
                frag = href.split('#', 1)[1]
                if frag and frag not in pages_cache[tgt].ids:
                    E('link %s points to an id that does not exist in that page' % href)
        if href.lower().startswith('javascript:'):
            W('javascript: link (%s) — use a button or a real URL' % href[:40])

    # assets
    for kind, url in p.assets:
        if url.startswith('data:'):
            continue
        if is_external(url):
            W('%s loads from the network (%s) — site will not work offline; bundle it or use inline SVG/CSS' % (kind, url[:70]))
        else:
            tgt = local_target(base, url)
            if tgt and not os.path.exists(tgt):
                E('missing local %s: %s' % (kind, url))
    for url in re.findall(r'url\(\s*["\']?(https?://[^"\')]+)', css_all):
        W('CSS url() loads from the network: %s' % url[:70])
    if re.search(r'fonts\.googleapis|fonts\.gstatic|use\.typekit', css_all + ' '.join(u for _, u in p.assets)):
        W('web fonts are anachronistic here — 90s pages used installed fonts (Times, Arial, Verdana, Comic Sans, Courier)')

    # accessibility
    for src in p.imgs_no_alt:
        E('<img> without alt: %s' % src[:60])
    anim = re.search(r'animation\s*:|@keyframes|<marquee', css_all + js, re.I) or p.tags.get('marquee') or \
        ({'fp-marquee', 'fp-blink', 'fp-flyin', 'fp-transition', 'fp-spin'} & p.classes)
    if anim and 'prefers-reduced-motion' not in css_all + js:
        E('motion without a prefers-reduced-motion fallback')
    if p.tags.get('marquee'):
        W('<marquee> used — prefer the kit\'s .fp-marquee (pausable, honors reduced motion)')
    if re.search(r'outline\s*:\s*(none|0)\b', css_all) and 'focus-visible' not in css_all:
        W('focus outline removed — keyboard users lose their place')
    if re.search(r'\.innerHTML\s*=|insertAdjacentHTML|document\.write', js):
        W('innerHTML/insertAdjacentHTML/document.write in scripts — if any user text flows there it is an XSS hole; prefer textContent')
    if re.search(r'mailto:[^"\'>]*@example\.(com|org|net)', ' '.join(h for _, h, _ in p.links)):
        W('mailto: link to a placeholder @example address — use the real address or leave the mail line out')
    if p.autoplay or re.search(r'\.autoplay\s*=\s*true', js):
        E('auto-playing sound — browsers block it and visitors hate it; use a play button')

    # honesty
    src = pages_src[path]
    for m in re.finditer(r'data-fp-counter', src):
        chunk = src[max(0, m.start() - 500):m.end() + 700]
        near = re.sub(r'<[^>]+>', ' ', chunk) + ' ' + ' '.join(re.findall(r'title="([^"]*)"', chunk))
        if not HONEST_HINT.search(near):
            W('hit counter without "local / demo / this browser" wording right next to it — do not imply global stats')
    if 'data-fp-guestbook' in p.attrs_seen and not HONEST_HINT.search(text):
        W('guestbook present but text never says entries are local/demo — say where entries are stored')
    for f in p.forms:
        action = (f.get('action') or '').strip()
        handled = any(k in f for k in ('data-fp-demo', 'data-fp-guestbook', 'data-fp-search', 'data-fp-compose', 'onsubmit'))
        if not handled and not action:
            W('a <form> has no action and no data-fp-demo/compose/guestbook/search handler — submitting it will just reload the page')
        if re.search(r'example\.(com|org|net)', action):
            W('form posts to a placeholder domain (%s) — use a real endpoint or data-fp-demo/data-fp-compose' % action)

    # period authenticity smells
    radii = [float(x) for x in re.findall(r'border-radius\s*:\s*([\d.]+)px', css_all)]
    big = [r for r in radii if r > 14]
    if big and 'fp-btn-radius' not in css_all:
        W('large border-radius (%spx) — rounded cards read as modern; FrontPage boxes were square' % int(max(big)))
    if re.search(r'box-shadow\s*:[^;]*\b(\d{2,})px', css_all):
        W('soft blurred box-shadow — a modern tell; use bevels (outset/inset borders) or hard 1-2px offsets')
    if re.search(r'backdrop-filter|glassmorphism', css_all):
        W('backdrop-filter / glass effects are anachronistic')
    m = MODERN_FONTS.search(css_all)
    if m:
        W('modern font "%s" — use Times New Roman, Arial, Verdana, Trebuchet MS, Georgia, Comic Sans MS, Courier New, Impact' % m.group(0))
    emo = sorted(set(ch for ch in EMOJI.findall(text) if ch not in PERIOD_SYMBOLS))
    if emo:
        W('emoji %s — emoji did not exist on 1990s web pages; use GIF-style SVG clip art or ★ ☎ ✉ ► symbols' % ' '.join(emo[:8]))
    if not p.tags.get('table') and 'fp-frameset' not in p.classes:
        W('no <table> at all — FrontPage pages were built from tables; use one for the main layout')
    if re.search(r'display\s*:\s*grid', css_all) and 'fp-frameset' not in css_all:
        I('CSS grid in use — fine for responsiveness, but keep the visible layout table-like')
    if re.search(r'(?i)\b(on|in) the (left|right)\b|menu (at|on) the (left|right)|a la (izquierda|derecha)|à (esquerda|direita)|del lado (izquierdo|derecho)', text):
        I('copy says "left/right" — on phones the left border moves to the top; prefer "the menu" / "el menú"')
    if p.tags.get('font') or p.tags.get('center'):
        I('uses <font>/<center> period markup (%d/%d)' % (p.tags.get('font', 0), p.tags.get('center', 0)))
    todos = re.findall(r'<!--\s*(?:TODO|EDITAR|EDIT|FIXME)\b.*?-->|\$\s?X{2,}[.,X]*', src, re.I | re.S)
    todos += re.findall(r'\[[^\]\[]{0,12}\b(?:TODO|EDITAR|EDIT|a completar|completar|legenda|caption|your|su|tu|seu|sua|insert|agregar|add|aqu[ií]|here|XX+)\b[^\]\[]{0,40}\]', text, re.I)
    if re.search(r'<!--\s*FP:CONTENT', src):
        W('scaffold placeholder <!-- FP:CONTENT --> still present — that section was never written')
    if todos:
        I('%d placeholder(s) left for the user — list them in your reply: %s' % (len(todos), '; '.join(sorted(set(re.sub(r'\s+', ' ', x.strip())[:90] for x in todos))[:12])))
    for m in re.finditer(r'<img\b[^>]*>', src, re.I):
        tag = m.group(0)
        s_, w_, h_ = (re.search(r'\b%s\s*=\s*["\']?([^"\'\s>]+)' % k, tag, re.I) for k in ('src', 'width', 'height'))
        if not (s_ and w_ and h_) or not s_.group(1).lower().endswith('.svg'):
            continue
        svgp = local_target(base, s_.group(1))
        if not svgp or not os.path.exists(svgp):
            continue
        head = open(svgp, encoding='utf-8', errors='replace').read(600)
        vb = re.search(r'viewBox\s*=\s*["\']\s*[\d.-]+[ ,]+[\d.-]+[ ,]+([\d.]+)[ ,]+([\d.]+)', head)
        try:
            ratio_svg = float(vb.group(1)) / float(vb.group(2)) if vb else None
            ratio_img = float(w_.group(1)) / float(h_.group(1))
        except (ValueError, ZeroDivisionError):
            continue
        if ratio_svg and abs(ratio_img - ratio_svg) / ratio_svg > 0.15:
            W('%s shown at %sx%s distorts its %.2f:1 shape — fix width/height' % (s_.group(1), w_.group(1), h_.group(1), ratio_svg))
    I('tables: %d, images: %d, forms: %d, links: %d' % (p.tags.get('table', 0), p.tags.get('img', 0) + p.tags.get('svg', 0), len(p.forms), len(p.links)))
    return out


class Blocks(HTMLParser):
    """Text passages of a page, split at block elements; skips script/style."""
    BLOCK = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'th', 'dt', 'dd', 'div', 'section', 'header', 'footer',
             'nav', 'blockquote', 'pre', 'title', 'button', 'label', 'figcaption', 'br', 'tr', 'ul', 'ol', 'form'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.cur, self.skip = [], [], 0

    def flush(self):
        s = re.sub(r'\s+', ' ', ''.join(self.cur)).strip()
        if s:
            self.parts.append(s)
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in self.BLOCK:
            self.flush()
        else:
            self.cur.append(' ')  # <span>Python</span><span>SQL</span> are separate words

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        if tag in self.BLOCK:
            self.flush()
        else:
            self.cur.append(' ')

    def handle_data(self, data):
        if not self.skip:
            self.cur.append(data)


def norm(s):
    s = EMOJI.sub('', s).lower()
    return re.sub(r'[^\w$%@.+#&/-]+', ' ', s).strip()


def compare_source(src_path, pages):
    b = Blocks()
    b.feed(open(src_path, encoding='utf-8', errors='replace').read())
    b.flush()
    site_text = norm(' '.join(' '.join(pg.text) for pg in pages.values()))
    missing = []
    for part in b.parts:
        n = norm(part)
        if len(n) < 3 or n in site_text:
            continue
        # tolerate re-punctuated passages: every 3+ char word must still appear
        words = [w for w in n.split() if len(w) > 2]
        if words and all(w in site_text for w in words):
            continue
        missing.append(part)
    print('== source comparison with %s' % os.path.basename(src_path))
    if not missing:
        print('  ok: every text passage of the original appears in the new site')
    for m in missing:
        print('  WARN  missing from the new site: "%s"' % m[:110])
    return len(missing)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--source' in sys.argv:
        args = [a for a in args if a != sys.argv[sys.argv.index('--source') + 1]]
    strict = '--strict' in sys.argv
    if '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__)
        return
    if not args:
        sys.exit(__doc__)
    target = os.path.abspath(args[0])
    files = []
    if os.path.isdir(target):
        for root, _, names in os.walk(target):
            files += [os.path.join(root, n) for n in names if n.lower().endswith(('.html', '.htm'))]
    else:
        files = [target]
    pages = {}
    for f in sorted(files):
        pg = Page()
        pg.feed(open(f, encoding='utf-8', errors='replace').read())
        pages[f] = pg
        pages_src[f] = open(f, encoding='utf-8', errors='replace').read()
    n_err = n_warn = 0
    if os.path.isdir(target):  # files nobody references (e.g. clip art copied but never used)
        blob = '\n'.join(pages_src.values())
        for root, _, names in os.walk(target):
            for n in names:
                fp = os.path.join(root, n)
                if fp.lower().endswith(('.html', '.htm')) or n.startswith('.'):
                    continue
                if fp.endswith('.css'):
                    blob += open(fp, encoding='utf-8', errors='replace').read()
        for root, _, names in os.walk(target):
            for n in names:
                fp = os.path.join(root, n)
                if fp.lower().endswith(('.html', '.htm', '.css', '.js')) or n.startswith('.') or n.lower() in ('readme.md', 'readme.txt'):
                    continue
                if n not in blob:
                    print('  WARN  unused file shipped with the site: %s' % os.path.relpath(fp, target))
                    n_warn += 1
    for f in sorted(files):
        res = check(f, pages)
        rel = os.path.relpath(f, target if os.path.isdir(target) else os.path.dirname(target))
        print('== %s' % rel)
        for level, msg in res:
            print('  %-5s %s' % (level, msg))
            n_err += level == 'ERROR'
            n_warn += level == 'WARN'
    if '--source' in sys.argv:
        src_path = sys.argv[sys.argv.index('--source') + 1]
        n_warn += compare_source(src_path, pages)
    print('\n%d page(s), %d error(s), %d warning(s)' % (len(files), n_err, n_warn))
    sys.exit(1 if n_err or (strict and n_warn) else 0)


if __name__ == '__main__':
    main()
