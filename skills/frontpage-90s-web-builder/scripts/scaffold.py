#!/usr/bin/env python3
"""Scaffold a FrontPage-style site: theme + kit wired in, shared borders and navigation bars
identical on every page, content left as clearly marked placeholders for you to write.

Examples
  # one self-contained page with in-page sections (kit + theme inlined)
  python3 scaffold.py out/ --theme starfield --title "Kevin's Cool Page" \
      --sections "about=About Me,links=Cool Links,guestbook=Guestbook" --lang en

  # multi-page site (shared theme/fp.css + theme/fp-kit.js, like FrontPage's _themes folder)
  python3 scaffold.py out/ --theme industrial --title "Gomería Don Pepe" --lang es \
      --pages "index.html=Inicio,servicios.html=Servicios,contacto.html=Contacto" --phone "+54 341 400-0000"

  python3 scaffold.py --list-themes

Stdlib only. Never overwrites an existing file unless --force is given.
"""
import argparse
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, '..', 'assets'))
THEMES = os.path.join(ASSETS, 'themes')

STRINGS = {
    'en': {'mail': 'Send mail to {email} with questions or comments about this web site.',
           'copy': 'Copyright &copy; {year} {owner} All rights reserved.', 'updated': 'Last modified:',
           'content': 'Write this page\'s content here.', 'top': 'Back to top', 'home': 'Home', 'nav': 'Main menu', 'phone': 'Phone:', 'frames': 'View with frames', 'main': 'Main content'},
    'es': {'mail': 'Envíe un correo a {email} con preguntas o comentarios sobre este sitio web.',
           'copy': 'Copyright &copy; {year} {owner} Todos los derechos reservados.', 'updated': 'Última modificación:',
           'content': 'Escriba aquí el contenido de esta página.', 'top': 'Volver arriba', 'home': 'Inicio', 'nav': 'Menú principal', 'phone': 'Teléfono:', 'frames': 'Ver con marcos', 'main': 'Contenido principal'},
    'pt': {'mail': 'Envie um e-mail para {email} com perguntas ou comentários sobre este site.',
           'copy': 'Copyright &copy; {year} {owner} Todos os direitos reservados.', 'updated': 'Última modificação:',
           'content': 'Escreva aqui o conteúdo desta página.', 'top': 'Voltar ao topo', 'home': 'Início', 'nav': 'Menu principal', 'phone': 'Telefone:', 'frames': 'Ver com quadros', 'main': 'Conteúdo principal'},
}


# FrontPage version -> (GENERATOR meta, typical copyright year)
ERAS = {'97': ('Microsoft FrontPage 2.0', '1997'), '98': ('Microsoft FrontPage 3.0', '1998'),
        '2000': ('Microsoft FrontPage 4.0', '2000'), '2002': ('Microsoft FrontPage 5.0', '2002')}


def esc(text):
    """Escape for HTML without double-escaping labels that already contain entities."""
    return html.escape(html.unescape(text), quote=False).replace('"', '&quot;')


def themes():
    return sorted(f[:-4] for f in os.listdir(THEMES) if f.endswith('.css'))


def theme_blurb(name):
    with open(os.path.join(THEMES, name + '.css'), encoding='utf-8') as f:
        m = re.search(r'/\*\s*Theme:\s*(.*?)\*/', f.read(), re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def parse_pairs(spec):
    out = []
    for part in [p.strip() for p in (spec or '').split(',') if p.strip()]:
        key, _, label = part.partition('=')
        out.append((key.strip(), (label or key).strip()))
    return out


def nav_buttons(items, vertical, label):
    cls = 'fp-navbar-v' if vertical else 'fp-navbar'
    links = '\n'.join('  <a class="fp-btn" href="%s">%s</a>' % (esc(h), esc(t)) for h, t in items)
    return '<nav class="%s" aria-label="%s">\n%s\n</nav>' % (cls, esc(label), links)


def text_nav(items):
    return '<p class="fp-textnav">' + ' '.join(
        '[&nbsp;<a href="%s">%s</a>&nbsp;]' % (esc(h), esc(t)) for h, t in items) + '</p>'


def build_page(a, s, items, page_title, body_inner, css_block, js_block):
    vertical = a.layout == 'left'
    # Page Banner = the page's title as the page's <h1>; inner pages carry the site name underneath
    sub = a.tagline if page_title == a.title else a.title
    banner = '<div class="fp-banner" role="banner"><h1>%s</h1>%s</div>' % (
        esc(page_title), '<small>%s</small>' % esc(sub) if sub else '')
    owner = esc(a.owner or a.title)
    owner = owner if owner.endswith(('.', '!', '?')) else owner + '.'
    updated = esc(a.updated) if a.updated else '<span data-fp-timestamp="long"></span>'
    lines = []
    if a.email:  # never invent an address: the mail line only appears when the user gave one
        email = esc(a.email)
        lines.append(s['mail'].format(email='<a href="mailto:%s">%s</a>' % (email, email)))
    if a.phone:
        digits = re.sub(r'[^0-9+]', '', a.phone)
        lines.append('%s <a href="tel:%s">%s</a>' % (s['phone'], digits, esc(a.phone)))
    lines.append(s['copy'].format(year=esc(a.year), owner=owner))
    lines.append(s['updated'] + ' ' + updated)
    bottom = '\n'.join(['<hr>', text_nav(items), '<p>' + '<br>\n'.join(lines) + '</p>'])
    if a.layout == 'frames':  # framed page: content + bottom border; banner and menu live in index.html
        bottom = '\n'.join(['<hr>', '<div data-fp-noframes-only>', text_nav(items),
                             '<p class="fp-textnav">[&nbsp;<a href="index.html" target="_top">%s</a>&nbsp;]</p>' % s['frames'], '</div>',
                             '<p>' + '<br>\n'.join(lines) + '</p>'])
        rows = ('<tr><td class="fp-main" id="content">\n%s\n</td></tr>\n'
                '<tr><td class="fp-border-bottom">\n%s\n</td></tr>') % (body_inner, bottom)
    elif vertical:
        rows = (
            '<tr><td colspan="2" class="fp-border-top">\n%s\n</td></tr>\n'
            '<tr>\n<td class="fp-side">\n%s\n<!-- FP:SIDEBAR (optional: counter, badges, 120x60 ads, small boxes) -->\n</td>\n'
            '<td class="fp-main" id="content">\n%s\n</td>\n</tr>\n'
            '<tr><td colspan="2" class="fp-border-bottom">\n%s\n</td></tr>'
        ) % (banner, nav_buttons(items, True, s['nav']), body_inner, bottom)
    else:
        rows = (
            '<tr><td class="fp-border-top">\n%s\n%s\n</td></tr>\n'
            '<tr><td class="fp-main" id="content">\n%s\n</td></tr>\n'
            '<tr><td class="fp-border-bottom">\n%s\n</td></tr>'
        ) % (banner, nav_buttons(items, False, s['nav']), body_inner, bottom)
    return head(a, page_title, css_block) + '''<body{body_cls}>
<div class="fp-page">
<table class="fp-layout" width="100%" border="0" cellspacing="0" cellpadding="8">
{rows}
</table>
</div>
{js}
</body>
</html>
'''.format(rows=rows, js=js_block, body_cls='' if a.era == '97' else ' class="fp-transition"')


def head(a, page_title, css_block):
    title = page_title if page_title == a.title else '%s - %s' % (page_title, a.title)
    return '''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="GENERATOR" content="{generator}">
<meta name="ProgId" content="FrontPage.Editor.Document">
{theme_meta}{og}<title>{title}</title>
{css}
</head>
'''.format(lang=esc(a.lang), generator=ERAS[a.era][0], title=esc(title), css=css_block,
           # themes and page transitions arrived with FrontPage 98
           theme_meta='' if a.era == '97' else '<meta name="Microsoft Theme" content="%s">\n' % esc(a.theme),
           # link previews for pages shared on WhatsApp / social networks
           og='' if not a.description else '<meta name="description" content="%s">\n<meta property="og:title" content="%s">\n'
              '<meta property="og:description" content="%s">\n<meta property="og:type" content="website">\n'
              % (esc(a.description), esc(title), esc(a.description)))


def build_frameset(a, s, items, css_block, js_block):
    """index.html: banner frame + contents frame + <iframe name="main"> — FrontPage's
    "Banner and Contents" frames template, done without <frameset> so it works everywhere."""
    links = '\n'.join('  <a class="fp-btn" href="%s" target="main">%s</a>' % (esc(h), esc(t)) for h, t in items)
    return head(a, a.title, css_block) + '''<body>
<div class="fp-frameset">
<div class="fp-frame fp-frame--banner"><div class="fp-banner" role="banner">{title}{tag}</div></div>
<div class="fp-frame fp-frame--contents">
<nav class="fp-navbar-v" aria-label="{nav}">
{links}
</nav>
<!-- FP:SIDEBAR (optional: quick search, counter, badges) -->
</div>
<div class="fp-frame" style="padding:0"><iframe name="main" class="fp-frame-target" src="{first}" title="{main}"></iframe></div>
</div>
{js}
</body>
</html>
'''.format(title=esc(a.title), tag='<small>%s</small>' % esc(a.tagline) if a.tagline else '', nav=esc(s['nav']), links=links,
           first=esc(items[0][0]), main=esc(s['main']), js=js_block)


SAFE_PAGE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]*\.html?$')
SAFE_ID = re.compile(r'^[A-Za-z][A-Za-z0-9_-]*$')
OUT_ROOT = None  # set in main(); every write must stay inside it


def write(path, text, force):
    real = os.path.realpath(path)
    if OUT_ROOT is None or os.path.commonpath([OUT_ROOT, real]) != OUT_ROOT:
        sys.exit('refusing to write outside the output directory: %s' % path)
    if os.path.exists(path) and not force:
        sys.exit('refusing to overwrite %s (use --force)' % path)
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', path)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('out', nargs='?')
    p.add_argument('--theme', default='classic')
    p.add_argument('--title', default='Welcome to My Home Page!', help='site name, plain text (no HTML)')
    p.add_argument('--description', default='', help='one sentence for the description + og: link-preview tags')
    p.add_argument('--tagline', default='', help='plain text shown under the banner title (no HTML)')
    p.add_argument('--pages', help='comma list file=Label; first is home. Omit for a single page.')
    p.add_argument('--sections', help='single-page mode: comma list id=Label for in-page sections')
    p.add_argument('--layout', choices=['left', 'top', 'frames'], default='left',
                   help='left = vertical nav in a left shared border; top = buttons under the banner; '
                        'frames = index.html with banner + contents frame + main frame (pages must not include index.html)')
    p.add_argument('--lang', default='en')
    p.add_argument('--email', default='', help='webmaster e-mail for the bottom border; omitted if not given (never invent one)')
    p.add_argument('--phone', default='', help='phone for the bottom border (rendered as a tel: link)')
    p.add_argument('--owner', default='', help='copyright holder (default: --title)')
    p.add_argument('--era', choices=sorted(ERAS), default='98', help='FrontPage version: sets the GENERATOR meta and default year')
    p.add_argument('--year', default='', help='copyright year (default: the era\'s year; use the real year for real businesses)')
    p.add_argument('--updated', default='', help='fixed "last modified" text (e.g. a fictional 1998 date); default = real file date')
    p.add_argument('--mode', choices=['inline', 'shared'], help='inline CSS/JS in each page, or shared theme/ files (default: inline for 1 page, shared for several)')
    p.add_argument('--clipart', default='', help='copy clip art into images/: comma list (new,email,construction,globe,hot,arrow) or "all"')
    p.add_argument('--force', action='store_true')
    p.add_argument('--list-themes', action='store_true')
    a = p.parse_args()

    if a.list_themes:
        for t in themes():
            print('%-14s %s' % (t, theme_blurb(t)))
        return
    if not a.out:
        p.error('output directory is required')
    if a.theme not in themes():
        p.error('unknown theme %r; choose from: %s' % (a.theme, ', '.join(themes())))
    s = STRINGS.get(a.lang.split('-')[0], STRINGS['en'])
    a.year = a.year or ERAS[a.era][1]
    global OUT_ROOT
    OUT_ROOT = os.path.realpath(a.out)
    pages = parse_pairs(a.pages) or [('index.html', a.title)]
    for fname, _ in pages:  # plain file names only: no folders, no "..", no absolute paths
        if not SAFE_PAGE.match(fname):
            p.error('invalid page file name %r: use names like "about.html" (letters, digits, - and _)' % fname)
    for sid, _ in parse_pairs(a.sections):
        if not SAFE_ID.match(sid):
            p.error('invalid section id %r: start with a letter; letters, digits, - and _ only' % sid)
    mode = a.mode or ('inline' if len(pages) == 1 and a.layout != 'frames' else 'shared')
    kit_css, theme_css, kit_js = read(os.path.join(ASSETS, 'fp-kit.css')), read(os.path.join(THEMES, a.theme + '.css')), read(os.path.join(ASSETS, 'fp-kit.js'))

    if mode == 'inline':
        css_block = '<style>\n%s\n%s\n/* ---- page-specific styles below ---- */\n</style>' % (kit_css, theme_css)
        js_block = '<script>\n%s\n</script>' % kit_js
    else:
        write(os.path.join(a.out, 'theme', 'fp.css'), kit_css + '\n' + theme_css, a.force)
        write(os.path.join(a.out, 'theme', 'fp-kit.js'), kit_js, a.force)
        # theme/site.css = your site-wide tweaks (recolors, extra components), shared by every page
        if not os.path.exists(os.path.join(a.out, 'theme', 'site.css')):
            write(os.path.join(a.out, 'theme', 'site.css'), '/* Site-wide styles shared by every page: --fp-* overrides, custom classes. */\n:root{}\n', False)
        css_block = '<link rel="stylesheet" href="theme/fp.css">\n<link rel="stylesheet" href="theme/site.css">'
        js_block = '<script src="theme/fp-kit.js"></script>'

    if a.clipart and mode == 'inline':
        print('note: single-file mode — paste clip art inline from assets/clipart/*.svg instead of linking images/')
        a.clipart = ''
    if a.clipart:  # copy only the clip art you'll use: <img src="images/new.svg" width="48" height="30" alt="New!">
        clip = os.path.join(ASSETS, 'clipart')
        names = sorted(f[:-4] for f in os.listdir(clip) if f.endswith('.svg'))
        want = names if a.clipart == 'all' else [n.strip() for n in a.clipart.split(',') if n.strip()]
        for n in want:
            if n not in names:
                p.error('unknown clip art %r; available: %s' % (n, ', '.join(names)))
            if not os.path.exists(os.path.join(a.out, 'images', n + '.svg')):
                write(os.path.join(a.out, 'images', n + '.svg'), read(os.path.join(clip, n + '.svg')), False)

    if a.layout == 'frames':
        if any(f == 'index.html' for f, _ in pages):
            p.error('with --layout frames, index.html is the frameset; name the first page e.g. inicio.html or home.html')
        write(os.path.join(a.out, 'index.html'), build_frameset(a, s, pages, css_block, js_block), a.force)
        for fname, label in pages:
            body = '<!-- FP:CONTENT %s -->\n<h1>%s</h1>\n<p>%s</p>' % (esc(fname), esc(label), s['content'])  # framed pages have no banner
            write(os.path.join(a.out, fname), build_page(a, s, pages, label, body, css_block, js_block), a.force)
    elif len(pages) == 1 and a.sections:
        secs = parse_pairs(a.sections)
        items = [('#content', s['home'])] + [('#' + i, t) for i, t in secs]
        body = ['<!-- FP:CONTENT intro -->', '<p>%s</p>' % s['content']]
        for i, t in secs:
            body += ['', '<h2 id="%s">%s</h2>' % (esc(i), esc(t)), '<!-- FP:CONTENT %s -->' % esc(i),
                     '<p>%s</p>' % s['content'], '<p class="fp-small"><a href="#content">%s</a></p>' % s['top']]
        write(os.path.join(a.out, pages[0][0]), build_page(a, s, items, a.title, '\n'.join(body), css_block, js_block), a.force)
    else:
        items = pages
        for i, (fname, label) in enumerate(pages):
            title = a.title if i == 0 else label
            body = '<!-- FP:CONTENT %s -->\n<p>%s</p>' % (esc(fname), s['content'])  # the banner is this page's <h1>
            write(os.path.join(a.out, fname), build_page(a, s, items, title, body, css_block, js_block), a.force)
    print('theme:', a.theme, '| mode:', mode, '| layout:', a.layout)
    print('next: replace every <!-- FP:CONTENT --> block, then run scripts/check_site.py', a.out)


if __name__ == '__main__':
    main()
