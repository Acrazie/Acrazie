import math
import random
import os

def create_hero_banner():
    width = 1200
    height = 340
    cx = width / 2
    cy = height / 2

    # Deterministic seed for reproducible aesthetic distribution
    random.seed(1337)

    # 1. Generate spiral arms particles (Galaxy vortex)
    # 2 arms, logarithmic spiral + dispersion
    particles_arm1 = []
    particles_arm2 = []
    ambient_stars = []

    # Palette: crisp white, icy blue, lavender/indigo, subtle amber core
    colors = ["#FFFFFF", "#E0E7FF", "#C7D2FE", "#818CF8", "#A5B4FC", "#93C5FD", "#FDE68A"]

    # Spiral particles
    num_spiral = 180
    for i in range(num_spiral):
        t = (i / num_spiral) * 3.5 * math.pi
        r = 30 + 38 * t
        
        # Arm 1
        jitter_r = random.gauss(0, 16 + t * 4)
        jitter_angle = random.gauss(0, 0.12)
        angle1 = t + jitter_angle
        x1 = cx + (r + jitter_r) * math.cos(angle1) * 1.55
        y1 = cy + (r + jitter_r) * math.sin(angle1) * 0.58
        size1 = round(random.uniform(0.8, 2.2), 1)
        opacity1 = round(random.uniform(0.35, 0.95), 2)
        color1 = random.choice(colors[:-1]) if r > 70 else random.choice(colors)
        particles_arm1.append((round(x1, 1), round(y1, 1), size1, opacity1, color1))

        # Arm 2 (offset by pi)
        angle2 = t + math.pi + jitter_angle
        x2 = cx + (r + jitter_r) * math.cos(angle2) * 1.55
        y2 = cy + (r + jitter_r) * math.sin(angle2) * 0.58
        size2 = round(random.uniform(0.8, 2.2), 1)
        opacity2 = round(random.uniform(0.35, 0.95), 2)
        color2 = random.choice(colors[:-1]) if r > 70 else random.choice(colors)
        particles_arm2.append((round(x2, 1), round(y2, 1), size2, opacity2, color2))

    # Ambient floating stars
    for _ in range(70):
        x = random.randint(20, width - 20)
        y = random.randint(15, height - 15)
        # Avoid clustering directly over text center
        if 420 < x < 780 and 110 < y < 230:
            continue
        size = round(random.uniform(0.6, 1.6), 1)
        opacity = round(random.uniform(0.2, 0.65), 2)
        color = random.choice(["#FFFFFF", "#94A3B8", "#818CF8", "#C7D2FE"])
        ambient_stars.append((x, y, size, opacity, color))

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '  <defs>',
        '    <radialGradient id="spaceCore" cx="50%" cy="50%" r="50%">',
        '      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />',
        '      <stop offset="12%" stop-color="#818CF8" stop-opacity="0.45" />',
        '      <stop offset="45%" stop-color="#312E81" stop-opacity="0.25" />',
        '      <stop offset="100%" stop-color="#05070D" stop-opacity="0" />',
        '    </radialGradient>',
        '    <radialGradient id="nebulaGlow" cx="50%" cy="50%" r="60%">',
        '      <stop offset="0%" stop-color="#4F46E5" stop-opacity="0.18" />',
        '      <stop offset="60%" stop-color="#0E1322" stop-opacity="0.05" />',
        '      <stop offset="100%" stop-color="#05070D" stop-opacity="0" />',
        '    </radialGradient>',
        '    <!-- Backdrop filter for text legibility -->',
        '    <radialGradient id="textBackdrop" cx="50%" cy="50%" r="45%">',
        '      <stop offset="0%" stop-color="#05070D" stop-opacity="0.88" />',
        '      <stop offset="65%" stop-color="#05070D" stop-opacity="0.75" />',
        '      <stop offset="100%" stop-color="#05070D" stop-opacity="0" />',
        '    </radialGradient>',
        '    <style>',
        '      @keyframes galaxyRotate {',
        '        from { transform: rotate(0deg); }',
        '        to { transform: rotate(360deg); }',
        '      }',
        '      @keyframes pulseCore {',
        '        0%, 100% { transform: scale(1); opacity: 0.8; }',
        '        50% { transform: scale(1.15); opacity: 1; }',
        '      }',
        '      .galaxy-arms {',
        f'        transform-origin: {cx}px {cy}px;',
        '        animation: galaxyRotate 120s linear infinite;',
        '      }',
        '      .core-glow {',
        f'        transform-origin: {cx}px {cy}px;',
        '        animation: pulseCore 8s ease-in-out infinite;',
        '      }',
        '      .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }',
        '      .font-mono { font-family: "SF Mono", Monaco, "Cascadia Code", "Fira Code", monospace; }',
        '    </style>',
        '  </defs>',
        '',
        '  <!-- Background -->',
        f'  <rect width="{width}" height="{height}" rx="14" fill="#05070D" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1.2" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="550" ry="160" fill="url(#nebulaGlow)" />',
        '',
        '  <!-- Ambient stationary stars -->',
        '  <g>',
    ]

    for x, y, s, op, col in ambient_stars:
        svg.append(f'    <circle cx="{x}" cy="{y}" r="{s}" fill="{col}" opacity="{op}" />')

    svg.extend([
        '  </g>',
        '',
        '  <!-- Rotating spiral galaxy arms -->',
        '  <g class="galaxy-arms">',
    ])

    for x, y, s, op, col in particles_arm1:
        svg.append(f'    <circle cx="{x}" cy="{y}" r="{s}" fill="{col}" opacity="{op}" />')
    for x, y, s, op, col in particles_arm2:
        svg.append(f'    <circle cx="{x}" cy="{y}" r="{s}" fill="{col}" opacity="{op}" />')

    svg.extend([
        '  </g>',
        '',
        '  <!-- Core glow -->',
        f'  <ellipse class="core-glow" cx="{cx}" cy="{cy}" rx="140" ry="70" fill="url(#spaceCore)" />',
        '',
        '  <!-- Text legibility backdrop shield -->',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="280" ry="110" fill="url(#textBackdrop)" />',
        '',
        '  <!-- Foreground Typography (Mayeul / Software & AI Engineer) -->',
        f'  <g transform="translate({cx}, {cy - 38})" text-anchor="middle">',
        '    <!-- Status indicator pill -->',
        '    <g transform="translate(0, -28)">',
        '      <rect x="-160" y="-12" width="320" height="24" rx="12" fill="rgba(15, 23, 42, 0.85)" stroke="rgba(129, 140, 248, 0.3)" stroke-width="1" />',
        '      <circle cx="-140" cy="0" r="3.5" fill="#10B981" />',
        '      <circle cx="-140" cy="0" r="6" fill="#10B981" opacity="0.25" />',
        '      <text class="font-mono" x="-124" y="3.5" fill="#CBD5E1" font-size="10.5px" font-weight="500" letter-spacing="0.06em">AUTONOMOUS AGENTS &amp; SKILLS</text>',
        '    </g>',
        '',
        '    <!-- Name Title -->',
        '    <text class="font-sans" x="0" y="34" fill="#FFFFFF" font-size="44px" font-weight="700" letter-spacing="-0.03em">Mayeul</text>',
        '    <text class="font-mono" x="0" y="60" fill="#818CF8" font-size="13px" font-weight="600" letter-spacing="0.16em">@ACRAZIE</text>',
        '',
        '    <!-- Professional Subtitle -->',
        '    <text class="font-sans" x="0" y="92" fill="#E2E8F0" font-size="15px" font-weight="500" letter-spacing="-0.01em">Software Engineer &amp; AI Engineer</text>',
        '    <text class="font-mono" x="0" y="112" fill="#94A3B8" font-size="12px" opacity="0.85">Agentic Harnesses · Production Skills · High-Reliability Systems</text>',
        '  </g>',
        '</svg>'
    ])
    return '\n'.join(svg)

def create_harness_surface():
    width = 1100
    height = 145
    card_w = 260
    card_h = 125
    gap = 13
    start_x = (width - (4 * card_w + 3 * gap)) / 2
    y = 10

    runtimes = [
        {
            "name": "Claude Code",
            "tag": "AGENTIC CLI",
            "role": "Terminal coding agent",
            "desc": "Autonomous feature work, iterative refactors, and test validation in local repos."
        },
        {
            "name": "Codex",
            "tag": "BACKGROUND DEV",
            "role": "Cloud engineering harness",
            "desc": "Parallel worktrees, background CI/CD operations, and repo-scale code intelligence."
        },
        {
            "name": "Hermes",
            "tag": "TOOL RUNTIME",
            "role": "Autonomous agent engine",
            "desc": "Local tool execution, custom skill invocation, continuous subagent delegation."
        },
        {
            "name": "Anti-Gravity",
            "tag": "ORCHESTRATION",
            "role": "Multi-agent systems",
            "desc": "Coordinated multi-agent planning, rigorous decision trees, and verifiable outputs."
        }
    ]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '  <defs>',
        '    <style>',
        '      .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }',
        '      .font-mono { font-family: "SF Mono", Monaco, "Cascadia Code", "Fira Code", monospace; }',
        '    </style>',
        '  </defs>',
    ]

    for i, r in enumerate(runtimes):
        cx = start_x + i * (card_w + gap)
        svg.extend([
            f'  <!-- Card {r["name"]} -->',
            f'  <g transform="translate({cx}, {y})">',
            f'    <rect width="{card_w}" height="{card_h}" rx="10" fill="#090D16" stroke="rgba(255, 255, 255, 0.09)" stroke-width="1.2" />',
            f'    <!-- Header bar -->',
            f'    <rect x="14" y="14" width="6" height="6" rx="3" fill="#818CF8" />',
            f'    <text class="font-mono" x="26" y="20" fill="#818CF8" font-size="9.5px" font-weight="600" letter-spacing="0.08em">{r["tag"]}</text>',
            f'    <text class="font-sans" x="14" y="44" fill="#FFFFFF" font-size="16px" font-weight="700">{r["name"]}</text>',
            f'    <text class="font-sans" x="14" y="62" fill="#94A3B8" font-size="12px" font-weight="500">{r["role"]}</text>',
            f'    <line x1="14" y1="74" x2="{card_w - 14}" y2="74" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />',
            f'    <text class="font-sans" x="14" y="93" fill="#64748B" font-size="11px" font-weight="400">',
        ])
        
        # Word wrap desc
        words = r["desc"].split(" ")
        line1 = " ".join(words[:5])
        line2 = " ".join(words[5:])
        svg.append(f'      <tspan x="14" dy="0">{line1}</tspan>')
        if line2:
            svg.append(f'      <tspan x="14" dy="14">{line2}</tspan>')
            
        svg.extend([
            '    </text>',
            '  </g>'
        ])

    svg.append('</svg>')
    return '\n'.join(svg)

def create_stack_surface():
    width = 1100
    height = 160
    col_w = 535
    col_h = 140
    y = 10
    x1 = (width - (col_w * 2 + 18)) / 2
    x2 = x1 + col_w + 18

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '  <defs>',
        '    <style>',
        '      .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }',
        '      .font-mono { font-family: "SF Mono", Monaco, "Cascadia Code", "Fira Code", monospace; }',
        '    </style>',
        '  </defs>',
        '',
        '  <!-- Column 1: Frontend & Interface Architecture -->',
        f'  <g transform="translate({x1}, {y})">',
        f'    <rect width="{col_w}" height="{col_h}" rx="10" fill="#090D16" stroke="rgba(255, 255, 255, 0.09)" stroke-width="1.2" />',
        '    <text class="font-mono" x="20" y="26" fill="#818CF8" font-size="10.5px" font-weight="600" letter-spacing="0.08em">FRONTEND &amp; INTERFACE ARCHITECTURE</text>',
        '    <text class="font-sans" x="20" y="48" fill="#F8FAFC" font-size="14.5px" font-weight="600">Client Systems, Reactive UI &amp; State Orchestration</text>',
        '    <line x1="20" y1="62" x2="515" y2="62" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />',
        '',
        '    <!-- Tech Pills -->',
        '    <g transform="translate(20, 78)">',
        '      <!-- React -->',
        '      <rect x="0" y="0" width="76" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="38" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">React</text>',
        '      <!-- TypeScript -->',
        '      <rect x="84" y="0" width="102" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="135" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">TypeScript</text>',
        '      <!-- JavaScript -->',
        '      <rect x="194" y="0" width="100" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="244" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">JavaScript</text>',
        '      <!-- Tailwind CSS -->',
        '      <rect x="302" y="0" width="112" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="358" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Tailwind CSS</text>',
        '      <!-- SCSS -->',
        '      <rect x="422" y="0" width="72" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="458" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">SCSS</text>',
        '    </g>',
        '  </g>',
        '',
        '  <!-- Column 2: Backend, Systems & Data -->',
        f'  <g transform="translate({x2}, {y})">',
        f'    <rect width="{col_w}" height="{col_h}" rx="10" fill="#090D16" stroke="rgba(255, 255, 255, 0.09)" stroke-width="1.2" />',
        '    <text class="font-mono" x="20" y="26" fill="#818CF8" font-size="10.5px" font-weight="600" letter-spacing="0.08em">BACKEND, SYSTEMS &amp; DATA PIPELINES</text>',
        '    <text class="font-sans" x="20" y="48" fill="#F8FAFC" font-size="14.5px" font-weight="600">Deterministic APIs, Services &amp; Relational Data</text>',
        '    <line x1="20" y1="62" x2="515" y2="62" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />',
        '',
        '    <!-- Tech Pills -->',
        '    <g transform="translate(20, 78)">',
        '      <!-- Python -->',
        '      <rect x="0" y="0" width="82" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="41" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Python</text>',
        '      <!-- Symfony -->',
        '      <rect x="90" y="0" width="92" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="136" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Symfony</text>',
        '      <!-- Node.js -->',
        '      <rect x="190" y="0" width="88" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="234" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Node.js</text>',
        '      <!-- PostgreSQL -->',
        '      <rect x="286" y="0" width="116" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="344" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">PostgreSQL</text>',
        '    </g>',
        '  </g>',
        '</svg>'
    ]
    return '\n'.join(svg)

def create_divider():
    width = 1100
    height = 3
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '  <defs>',
        '    <linearGradient id="laserGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#4F46E5" stop-opacity="0" />',
        '      <stop offset="25%" stop-color="#6366F1" stop-opacity="0.35" />',
        '      <stop offset="50%" stop-color="#A5B4FC" stop-opacity="0.8" />',
        '      <stop offset="75%" stop-color="#6366F1" stop-opacity="0.35" />',
        '      <stop offset="100%" stop-color="#4F46E5" stop-opacity="0" />',
        '    </linearGradient>',
        '  </defs>',
        f'  <line x1="0" y1="1.5" x2="{width}" y2="1.5" stroke="url(#laserGrad)" stroke-width="1.2" />',
        '</svg>'
    ]
    return '\n'.join(svg)

if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    with open('assets/hero-banner.svg', 'w') as f:
        f.write(create_hero_banner())
    with open('assets/harness-surface.svg', 'w') as f:
        f.write(create_harness_surface())
    with open('assets/stack-surface.svg', 'w') as f:
        f.write(create_stack_surface())
    with open('assets/divider.svg', 'w') as f:
        f.write(create_divider())
    print("Successfully generated all assets.")
