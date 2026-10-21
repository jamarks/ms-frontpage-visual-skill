#!/usr/bin/env python3
"""Render a page in headless Chrome/Chromium/Edge: screenshots + a horizontal-overflow check.

  python3 screenshot.py site/index.html [--out DIR] [--sizes 1024x1400,390x1600]
  python3 screenshot.py site/            # every .html page in the folder
  python3 screenshot.py site/recipe.html --print   # also save the print version as PDF (check it!)
  python3 screenshot.py page.html --motion         # don't freeze animations (to see marquees mid-scroll)

Screenshots are full-page: WxH sets the width and the minimum height (pages are captured to their end,
up to 8000px).

For each page and size it writes DIR/<page>-<w>x<h>.png and prints whether anything sticks out past the
viewport (the usual culprits: wide ads/tables/marquees inside the layout table). DIR defaults to a
temp folder so screenshots never end up inside the deliverable. Motion is frozen (reduced motion).

The page is rendered inside an iframe of the exact width, because headless Chrome on macOS will not
make a window narrower than 500px — a plain --window-size=390 silently renders at 500px.
Stdlib only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.request import pathname2url

CANDIDATES = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'microsoft-edge', 'chrome',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
]

WRAPPER = '''<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="margin:0;background:#808080">
<iframe id="f" src="%(src)s" style="width:%(w)dpx;height:%(h)dpx;border:0;display:block;background:#fff"></iframe>
<pre id="out" style="display:none">PENDING</pre>
<script>
document.getElementById('f').onload = function () {
  setTimeout(function () {
    var out = document.getElementById('out');
    try {
      var win = document.getElementById('f').contentWindow, d = win.document, W = win.innerWidth;
      var sw = Math.max(d.documentElement.scrollWidth, d.body ? d.body.scrollWidth : 0), bad = [];
      if (sw > W + 1) {
        var all = d.querySelectorAll('body *');
        for (var i = 0; i < all.length; i++) {
          var e = all[i], r = e.getBoundingClientRect();
          if (r.width && r.right > W + 1) {
            var childBad = false;
            for (var j = 0; j < e.children.length; j++) { var cr = e.children[j].getBoundingClientRect(); if (cr.width && cr.right > W + 1) { childBad = true; break; } }
            if (!childBad) bad.push(e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && e.className.baseVal === undefined && e.className ? '.' + String(e.className).trim().split(/\\s+/).join('.') : '') + ' (' + Math.round(r.width) + 'px wide, right edge ' + Math.round(r.right) + 'px)');
          }
        }
      }
      var sh = Math.max(d.documentElement.scrollHeight, d.body ? d.body.scrollHeight : 0), clipped = [];
      var boxes = d.querySelectorAll('.fp-badge, .fp-ad, .fp-hoverbtn, .fp-btn, .fp-digit, .fp-banner');
      for (var k = 0; k < boxes.length; k++) {
        var b = boxes[k];
        if (b.offsetParent && (b.scrollHeight > b.clientHeight + 2 || b.scrollWidth > b.clientWidth + 2))
          clipped.push((b.className.split(' ')[0]) + ' "' + b.textContent.trim().replace(/\\s+/g, ' ').slice(0, 40) + '"');
      }
      out.textContent = JSON.stringify({viewport: W, scrollWidth: sw, scrollHeight: sh, offenders: bad.slice(0, 8), clipped: clipped.slice(0, 10)});
    } catch (err) { out.textContent = JSON.stringify({error: String(err)}); }
  }, 900);
};
</script></body></html>'''


def find_browser():
    for c in CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        w = shutil.which(c)
        if w:
            return w
    return None


def main():
    argv = sys.argv[1:]
    sizes, outdir = '1024x1400,390x1600', None
    do_print = '--print' in argv
    global MOTION
    MOTION = '--motion' in argv
    argv = [x for x in argv if x not in ('--print', '--motion')]
    if '-h' in argv or '--help' in argv:
        print(__doc__)
        return
    if '--sizes' in argv:
        i = argv.index('--sizes'); sizes = argv[i + 1]; del argv[i:i + 2]
    if '--out' in argv:
        i = argv.index('--out'); outdir = argv[i + 1]; del argv[i:i + 2]
    if not argv:
        sys.exit(__doc__)
    target = os.path.abspath(argv[0])
    if not os.path.exists(target):
        sys.exit('not found: ' + target)
    if os.path.isdir(target):
        pages = sorted(os.path.join(r, n) for r, _, ns in os.walk(target) for n in ns
                       if n.lower().endswith(('.html', '.htm')) and not n.startswith('_'))
    else:
        pages = [target]
    outdir = os.path.abspath(outdir or os.path.join(tempfile.gettempdir(), 'fp-screenshots'))
    os.makedirs(outdir, exist_ok=True)
    browser = find_browser()
    if not browser:
        sys.exit('No Chrome/Chromium/Edge found. Open the page in any browser (or a browser tool) instead.')
    problems = 0
    for page in pages:
        problems += shoot(browser, page, outdir, sizes)
        if do_print:
            pdf = os.path.join(outdir, os.path.splitext(os.path.basename(page))[0] + '-print.pdf')
            subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--run-all-compositor-stages-before-draw',
                            '--virtual-time-budget=3000', '--print-to-pdf=' + pdf, 'file://' + pathname2url(page)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
            print(('  print PDF: ' if os.path.exists(pdf) else '  print PDF FAILED: ') + pdf)
    print('%d page(s), %d overflow problem(s); screenshots in %s' % (len(pages), problems, outdir))
    sys.exit(1 if problems else 0)


MOTION = False


def shoot(browser, page, outdir, sizes):
    base = os.path.splitext(os.path.basename(page))[0]
    src = 'file://' + pathname2url(page)
    problems = 0
    print('== ' + os.path.basename(page))
    for size in sizes.split(','):
        w, h = [int(x) for x in size.lower().split('x')]
        wrapper = os.path.join(outdir, '_wrap-%s-%dx%d.html' % (base, w, h))

        def run(height, extra):
            with open(wrapper, 'w', encoding='utf-8') as f:
                f.write(WRAPPER % {'src': src, 'w': w, 'h': height})
            cmd = [browser, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                   '--no-first-run', '--no-default-browser-check', '--window-size=%d,%d' % (max(w, 500), height),
                   '--virtual-time-budget=4000'] + ([] if MOTION else ['--force-prefers-reduced-motion'])
            return subprocess.run(cmd + extra + ['file://' + pathname2url(wrapper)], capture_output=True, text=True, timeout=90).stdout

        dom = run(h, ['--dump-dom'])
        m = re.search(r'<pre id="out"[^>]*>(.*?)</pre>', dom, re.S)
        info = {}
        try:
            info = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')) if m else {}
        except ValueError:
            pass
        full = min(max(h, int(info.get('scrollHeight') or h)), 8000)
        png = os.path.join(outdir, '%s-%dx%d.png' % (base, w, h))
        run(full, ['--screenshot=' + png])
        print(('wrote ' if os.path.exists(png) else 'FAILED ') + png + '  (full page: %dpx tall)' % full + ('  (page is %dpx wide inside a %dpx canvas)' % (w, max(w, 500)) if w < 500 else ''))
        if 'scrollWidth' in info:
            if info['scrollWidth'] > info['viewport'] + 1:
                problems += 1
                print('  OVERFLOW at %dpx: content is %dpx wide. Culprits:' % (info['viewport'], info['scrollWidth']))
                for o in info['offenders']:
                    print('    - ' + o)
            else:
                print('  ok: no horizontal overflow at %dpx' % info['viewport'])
        else:
            print('  (overflow check unavailable: %s)' % (info.get('error') or 'no result'))
        if info.get('clipped'):
            problems += 1
            print('  CLIPPED text at %dpx (shorten it or use a wider box):' % w)
            for c in info['clipped']:
                print('    - ' + c)
        os.remove(wrapper)
    return problems


if __name__ == '__main__':
    main()
