import math
import random

def generate_banner(theme='light'):
    width = 1200
    height = 360
    
    # Codex palette definition
    if theme == 'light':
        bg_base = "#FBFBFD"
        card_border = "#E2E8F0"
        card_bg = "rgba(255, 255, 255, 0.75)"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        text_accent = "#6366F1"
        tag_bg = "rgba(99, 102, 241, 0.08)"
        tag_border = "rgba(99, 102, 241, 0.2)"
        tag_text = "#4F46E5"
        grid_color = "rgba(148, 163, 184, 0.12)"
        glow_1 = "rgba(165, 180, 252, 0.35)" # soft indigo
        glow_2 = "rgba(196, 181, 253, 0.30)" # soft violet
        glow_3 = "rgba(186, 230, 253, 0.25)" # soft sky
        ascii_colors = ["#64748B", "#818CF8", "#A78BFA", "#94A3B8", "#475569"]
    else:
        bg_base = "#090D16"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_bg = "rgba(15, 23, 42, 0.65)"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        text_accent = "#818CF8"
        tag_bg = "rgba(129, 140, 248, 0.12)"
        tag_border = "rgba(129, 140, 248, 0.25)"
        tag_text = "#A5B4FC"
        grid_color = "rgba(255, 255, 255, 0.04)"
        glow_1 = "rgba(79, 70, 229, 0.22)"  # deep indigo glow
        glow_2 = "rgba(124, 58, 237, 0.18)"  # deep purple glow
        glow_3 = "rgba(14, 165, 233, 0.15)"  # cyan glow
        ascii_colors = ["#64748B", "#818CF8", "#C084FC", "#38BDF8", "#94A3B8"]

    random.seed(42) # deterministic generation
    
    # ASCII characters set similar to Codex particle field (escaped for XML/SVG)
    chars = ['*', '+', '~', '·', '/', '\\', '_', '^', '{', '}', ':', '&gt;', '&lt;', '0', '1', '≠', '≈', '§', '#', '∆']
    
    # Generate 55 animated particles distributed across the canvas
    particles = []
    for i in range(55):
        # Distribute mostly in background, avoiding tight center where text is
        x = random.randint(30, width - 30)
        y = random.randint(25, height - 25)
        # Avoid clustering directly behind center text
        if 420 < x < 780 and 110 < y < 250:
            if random.random() < 0.7:
                x = random.choice([random.randint(30, 410), random.randint(790, width - 30)])
        
        char = random.choice(chars)
        color = random.choice(ascii_colors)
        size = random.choice([10, 11, 12, 13, 14, 15, 17])
        opacity = round(random.uniform(0.25, 0.75), 2)
        
        # Kinetic animation parameters (floating / subtle physical drift)
        duration = round(random.uniform(5.0, 10.0), 1)
        delay = round(random.uniform(-10.0, 0.0), 1)
        dx = random.randint(-18, 18)
        dy = random.randint(-22, 22)
        rot = random.randint(-35, 35)
        
        particles.append({
            'char': char, 'x': x, 'y': y, 'color': color, 'size': size,
            'opacity': opacity, 'duration': duration, 'delay': delay,
            'dx': dx, 'dy': dy, 'rot': rot, 'id': f"p{i}"
        })
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '  <defs>',
        f'    <radialGradient id="meshGlow1_{theme}" cx="20%" cy="30%" r="65%">',
        f'      <stop offset="0%" stop-color="{glow_1}" />',
        f'      <stop offset="100%" stop-color="{glow_1}" stop-opacity="0" />',
        '    </radialGradient>',
        f'    <radialGradient id="meshGlow2_{theme}" cx="85%" cy="40%" r="60%">',
        f'      <stop offset="0%" stop-color="{glow_2}" />',
        f'      <stop offset="100%" stop-color="{glow_2}" stop-opacity="0" />',
        '    </radialGradient>',
        f'    <radialGradient id="meshGlow3_{theme}" cx="50%" cy="95%" r="55%">',
        f'      <stop offset="0%" stop-color="{glow_3}" />',
        f'      <stop offset="100%" stop-color="{glow_3}" stop-opacity="0" />',
        '    </radialGradient>',
        f'    <pattern id="grid_{theme}" width="32" height="32" patternUnits="userSpaceOnUse">',
        f'      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{grid_color}" stroke-width="1" />',
        '    </pattern>',
        '    <style>',
        '      @keyframes pulseGlow { 0%, 100% { transform: scale(1); opacity: 0.85; } 50% { transform: scale(1.08); opacity: 1; } }',
        '      .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }',
        '      .font-mono { font-family: "SF Mono", Monaco, Inconsolata, "Fira Code", monospace; }',
    ]
    
    for p in particles:
        svg.append(
            f'      @keyframes float_{p["id"]} {{ '
            f'0%, 100% {{ transform: translate(0px, 0px) rotate(0deg); }} '
            f'50% {{ transform: translate({p["dx"]}px, {p["dy"]}px) rotate({p["rot"]}deg); }} }}'
        )
        svg.append(
            f'      .{p["id"]} {{ animation: float_{p["id"]} {p["duration"]}s ease-in-out {p["delay"]}s infinite; '
            f'transform-origin: {p["x"]}px {p["y"]}px; }}'
        )
        
    svg.extend([
        '    </style>',
        '  </defs>',
        '',
        f'  <!-- Background canvas -->',
        f'  <rect width="{width}" height="{height}" rx="16" fill="{bg_base}" stroke="{card_border}" stroke-width="1.5" />',
        f'  <rect width="{width}" height="{height}" rx="16" fill="url(#grid_{theme})" />',
        '',
        f'  <!-- Ambient radial gradient mesh -->',
        f'  <rect width="{width}" height="{height}" rx="16" fill="url(#meshGlow1_{theme})" />',
        f'  <rect width="{width}" height="{height}" rx="16" fill="url(#meshGlow2_{theme})" />',
        f'  <rect width="{width}" height="{height}" rx="16" fill="url(#meshGlow3_{theme})" />',
        '',
        '  <!-- Animated ASCII kinetic particles -->',
        '  <g class="font-mono">',
    ])
    
    for p in particles:
        svg.append(
            f'    <text class="{p["id"]}" x="{p["x"]}" y="{p["y"]}" fill="{p["color"]}" '
            f'font-size="{p["size"]}px" font-weight="500" opacity="{p["opacity"]}">{p["char"]}</text>'
        )
        
    svg.extend([
        '  </g>',
        '',
        f'  <!-- Center Glassmorphism Showcase Card -->',
        f'  <g transform="translate(340, 75)">',
        f'    <rect width="520" height="210" rx="14" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2" backdrop-filter="blur(16px)" />',
        '',
        f'    <!-- Minimal badge -->',
        f'    <rect x="180" y="24" width="160" height="26" rx="13" fill="{tag_bg}" stroke="{tag_border}" stroke-width="1" />',
        f'    <circle cx="196" cy="37" r="4" fill="{tag_text}" />',
        f'    <text class="font-mono" x="208" y="41" fill="{tag_text}" font-size="11px" font-weight="600" letter-spacing="0.05em">EPITECH PRE-MSC</text>',
        '',
        f'    <!-- Name / Title -->',
        f'    <text class="font-sans" x="260" y="98" fill="{text_primary}" font-size="34px" font-weight="700" text-anchor="middle" letter-spacing="-0.03em">Mayeul</text>',
        f'    <text class="font-mono" x="260" y="126" fill="{text_accent}" font-size="13px" font-weight="600" text-anchor="middle" letter-spacing="0.12em">@ACRAZIE</text>',
        '',
        f'    <!-- Subtitle -->',
        f'    <text class="font-sans" x="260" y="158" fill="{text_secondary}" font-size="14.5px" font-weight="400" text-anchor="middle">Software Engineering · Next.js · Fullstack &amp; Creative Code</text>',
        f'    <text class="font-mono" x="260" y="184" fill="{text_secondary}" font-size="12px" opacity="0.8" text-anchor="middle">surf · escalade · rando · agentic tech</text>',
        '  </g>',
        '</svg>'
    ])
    
    return '\n'.join(svg)

if __name__ == '__main__':
    import os
    os.makedirs('assets', exist_ok=True)
    with open('assets/hero-light.svg', 'w') as f:
        f.write(generate_banner('light'))
    with open('assets/hero-dark.svg', 'w') as f:
        f.write(generate_banner('dark'))
    print("Successfully generated assets/hero-light.svg and assets/hero-dark.svg")
