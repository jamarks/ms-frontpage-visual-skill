#!/usr/bin/env python3
"""Turn a text grid into crisp pixel-art SVG — for the bespoke clip art every 90s page had.

  python3 pixelart.py art.txt [--scale 4] [--label "Red car"] > car.svg

art.txt: optional palette lines `X=#rrggbb`, then the grid; one character per pixel, `.` or space =
transparent. Rows may differ in length. Example:

  R=#cc0000
  B=#99ccff
  K=#222222
  ....RRRRRRR.....
  ....RBBRBBR.....
  .RRRRRRRRRRRRRR.
  .RRRRRRRRRRRRRR.
  ...KKK....KKK...

Output: <svg> with one <rect> per horizontal run, shape-rendering="crispEdges", role="img" + aria-label
(or aria-hidden="true" when --label is omitted). Paste it inline or save it to images/. Stdlib only.
"""
import html
import re
import sys

DEFAULT = {'K': '#000000', 'W': '#ffffff', 'R': '#cc0000', 'G': '#008000', 'B': '#0000cc', 'Y': '#ffff00',
           'C': '#00ffff', 'M': '#ff00ff', 'O': '#ff8000', 'N': '#804000', 'S': '#c0c0c0', 'D': '#808080'}


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        sys.exit(__doc__)
    scale, label = 4, ''
    if '--scale' in args:
        i = args.index('--scale'); scale = int(args[i + 1]); del args[i:i + 2]
    if '--label' in args:
        i = args.index('--label'); label = args[i + 1]; del args[i:i + 2]
    pal, rows = dict(DEFAULT), []
    for line in open(args[0], encoding='utf-8').read().splitlines():
        m = re.match(r'^\s*(\S)\s*=\s*(#[0-9a-fA-F]{3,8}|[a-z]+)\s*$', line)
        if m:
            pal[m.group(1)] = m.group(2)
        elif line.strip():
            rows.append(line.rstrip('\n'))
    w = max(len(r) for r in rows)
    h = len(rows)
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            if ch in '. ':
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == ch:
                run += 1
            if ch not in pal:
                sys.exit('no color for %r (row %d); add a line like %s=#rrggbb' % (ch, y + 1, ch))
            rects.append('<rect x="%d" y="%d" width="%d" height="1" fill="%s"/>' % (x, y, run, pal[ch]))
            x += run
    a11y = 'role="img" aria-label="%s"' % html.escape(label) if label else 'aria-hidden="true"'
    print('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" shape-rendering="crispEdges" %s>%s</svg>'
          % (w * scale, h * scale, w, h, a11y, ''.join(rects)))


if __name__ == '__main__':
    main()
