"""Generate the two decorative README assets; all body copy stays native."""
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ('#A8BFFF', '#C5B9F5', '#7295F5', '#626CE8', '#101116', '#F8F9FF')


def background(width, height):
    return f'''<defs>
<linearGradient id="base" x2="1" y2=".5"><stop stop-color="#A8BFFF"/><stop offset="1" stop-color="#C5B9F5"/></linearGradient>
<radialGradient id="blue"><stop stop-color="#7295F5"/><stop offset="1" stop-color="#7295F5" stop-opacity="0"/></radialGradient>
<radialGradient id="iris"><stop stop-color="#626CE8" stop-opacity=".65"/><stop offset="1" stop-color="#626CE8" stop-opacity="0"/></radialGradient>
</defs><rect width="{width}" height="{height}" fill="url(#base)"/>
<ellipse cx="80" cy="{height}" rx="700" ry="{height}" fill="url(#blue)"/>
<ellipse cx="{width}" cy="0" rx="620" ry="{height}" fill="url(#iris)"/>'''


def hero():
    rng = random.Random(42)
    dots = []
    for _ in range(180):
        x, y = rng.uniform(0, 1200), rng.uniform(0, 380)
        if 310 < x < 890 and 70 < y < 310:
            continue
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(.6,1.8):.1f}" fill="#F8F9FF" opacity="{rng.uniform(.3,.85):.2f}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="auto" overflow="hidden" viewBox="0 0 1200 380" role="img" aria-labelledby="title">
<title id="title">Mayeul — Software Engineer &amp; AI Engineer</title>
{background(1200,380)}
<style>@keyframes drift{{50%{{transform:translate(8px,-8px)}}}}.particles{{animation:drift 14s ease-in-out infinite}}@media(prefers-reduced-motion:reduce){{.particles{{animation:none}}}}</style>
<g class="particles">{''.join(dots)}</g>
<g fill="#101116" text-anchor="middle" font-family="Arial,Helvetica,sans-serif">
<text x="600" y="110" font-size="17" letter-spacing="4">@ACRAZIE</text>
<text x="600" y="210" font-size="88" font-weight="700" letter-spacing="-4">Mayeul</text>
<text x="600" y="266" font-size="26">Software Engineer &amp; AI Engineer</text>
</g></svg>'''


# Original modular display alphabet: shared stroke, open counters, diagonal cuts.
GLYPHS = {
 'A': 'M0 70 0 20 20 0 40 0 60 20 60 70 M0 40H60',
 'C': 'M60 5H20L0 25V50L20 70H60',
 'R': 'M0 70V0H40L60 15V25L40 40H0 M35 40 60 70',
 'Z': 'M0 0H60L0 70H60',
 'I': 'M10 0H50 M30 0V70 M10 70H50',
 'E': 'M60 0H0V70H60 M0 35H45',
 'S': 'M60 0H15L0 15V25L15 35H45L60 45V55L45 70H0',
 'K': 'M0 0V70 M60 0 0 40 M25 25 60 70',
 'L': 'M0 0V70H60',
}


def wordmark():
    paths = []
    for word, y in [('ACRAZIE', 43), ('SKILLS', 145)]:
        for i, char in enumerate(word):
            paths.append(f'<path transform="translate({52+i*88},{y})" d="{GLYPHS[char]}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="auto" overflow="hidden" viewBox="0 0 1200 270" role="img" aria-labelledby="title">
<title id="title">Acrazie / Skills</title>{background(1200,270)}
<g fill="none" stroke="#101116" stroke-width="10" stroke-linejoin="miter" stroke-linecap="square">{''.join(paths)}</g>
<path d="M740 42 686 218" fill="none" stroke="#F8F9FF" stroke-width="12"/>
<g fill="#101116" opacity=".65"><path d="M856 94h220v2H856z M856 116h170v2H856z M856 138h220v2H856z M856 160h120v2H856z"/></g>
</svg>'''


if __name__ == '__main__':
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)
    for name, content in [('hero-banner.svg', hero()), ('skills-wordmark.svg', wordmark())]:
        (assets / name).write_text(content, encoding='utf-8')
        print(f'Generated assets/{name}')
