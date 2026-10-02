"""Re-render every profile asset: header.gif, header.png (still) and how-i-work.gif.

Usage: python assets/src/render.py
Needs: pip install playwright && playwright install chromium; ffmpeg on PATH;
the shared recorder at ../../../_kit/record_html.py (C:/Users/Brian/readme-revamp/_kit/record_html.py).
"""
import os
import subprocess
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))
REC = os.path.normpath(os.path.join(HERE, '..', '..', '..', '_kit', 'record_html.py'))


def gif(html, out, w, h, dur, fps=15, colors=128):
    subprocess.run([sys.executable, REC, os.path.join(HERE, html), os.path.join(OUT, out),
                    '--w', str(w), '--h', str(h), '--dur', str(dur), '--fps', str(fps),
                    '--colors', str(colors)], check=True)


def still(html, out, w, h, at_ms):
    """Screenshot the end state (all rows handled) at 2x as a static PNG."""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.goto('file:///' + os.path.join(HERE, html).replace(os.sep, '/'))
        pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(300)
        pg.evaluate('(ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } }', at_ms)
        pg.screenshot(path=os.path.join(OUT, out))
        b.close()
    print('wrote', os.path.join(OUT, out))


if __name__ == '__main__':
    gif('header.html', 'header.gif', 1400, 500, 9)
    still('header.html', 'header.png', 1400, 500, 7000)
    gif('how-i-work.html', 'how-i-work.gif', 1100, 420, 9)
