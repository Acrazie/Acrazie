import math
import random
import os

def create_hero_banner():
    width = 1200
    height = 340
    cx = width / 2
    cy = height / 2

    random.seed(1337)

    particles_arm1 = []
    particles_arm2 = []
    ambient_stars = []

    colors = ["#FFFFFF", "#E0E7FF", "#C7D2FE", "#818CF8", "#A5B4FC", "#93C5FD", "#FDE68A"]

    num_spiral = 180
    for i in range(num_spiral):
        t = (i / num_spiral) * 3.5 * math.pi
        r = 30 + 38 * t
        
        jitter_r = random.gauss(0, 16 + t * 4)
        jitter_angle = random.gauss(0, 0.12)
        angle1 = t + jitter_angle
        x1 = cx + (r + jitter_r) * math.cos(angle1) * 1.55
        y1 = cy + (r + jitter_r) * math.sin(angle1) * 0.58
        size1 = round(random.uniform(0.8, 2.2), 1)
        opacity1 = round(random.uniform(0.35, 0.95), 2)
        color1 = random.choice(colors[:-1]) if r > 70 else random.choice(colors)
        particles_arm1.append((round(x1, 1), round(y1, 1), size1, opacity1, color1))

        angle2 = t + math.pi + jitter_angle
        x2 = cx + (r + jitter_r) * math.cos(angle2) * 1.55
        y2 = cy + (r + jitter_r) * math.sin(angle2) * 0.58
        size2 = round(random.uniform(0.8, 2.2), 1)
        opacity2 = round(random.uniform(0.35, 0.95), 2)
        color2 = random.choice(colors[:-1]) if r > 70 else random.choice(colors)
        particles_arm2.append((round(x2, 1), round(y2, 1), size2, opacity2, color2))

    for _ in range(70):
        x = random.randint(20, width - 20)
        y = random.randint(15, height - 15)
        if 380 < x < 820 and 100 < y < 240:
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
        '    <radialGradient id="textBackdrop" cx="50%" cy="50%" r="45%">',
        '      <stop offset="0%" stop-color="#05070D" stop-opacity="0.92" />',
        '      <stop offset="65%" stop-color="#05070D" stop-opacity="0.80" />',
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
        f'  <ellipse cx="{cx}" cy="{cy}" rx="320" ry="120" fill="url(#textBackdrop)" />',
        '',
        '  <!-- Foreground Typography (Centered & Mathematically Aligned) -->',
        f'  <g transform="translate({cx}, {cy - 38})" text-anchor="middle">',
        '    <!-- Status indicator pill: 280px wide, centered at x=0 -->',
        '    <g transform="translate(0, -28)">',
        '      <rect x="-140" y="-13" width="280" height="26" rx="13" fill="rgba(15, 23, 42, 0.9)" stroke="rgba(129, 140, 248, 0.35)" stroke-width="1" />',
        '      <text class="font-mono" x="0" y="3.5" fill="#E2E8F0" font-size="10.5px" font-weight="600" letter-spacing="0.08em" text-anchor="middle">AUTONOMOUS AGENTS &amp; SKILLS</text>',
        '    </g>',
        '',
        '    <!-- Name Title -->',
        '    <text class="font-sans" x="0" y="34" fill="#FFFFFF" font-size="44px" font-weight="700" letter-spacing="-0.03em">Mayeul</text>',
        '    <text class="font-mono" x="0" y="60" fill="#818CF8" font-size="13px" font-weight="600" letter-spacing="0.16em">@ACRAZIE</text>',
        '',
        '    <!-- Professional Subtitle -->',
        '    <text class="font-sans" x="0" y="92" fill="#F8FAFC" font-size="15.5px" font-weight="500" letter-spacing="-0.01em">Software Engineer &amp; AI Engineer</text>',
        '    <text class="font-mono" x="0" y="114" fill="#CBD5E1" font-size="12px" opacity="0.9">Agentic Harnesses · Production Skills · High-Reliability Systems</text>',
        '  </g>',
        '</svg>'
    ])
    return '\n'.join(svg)

def create_harness_surface():
    width = 1100
    height = 230
    col_w = 535
    col_h = 100
    gap_x = 18
    gap_y = 12
    x1 = (width - (col_w * 2 + gap_x)) / 2
    x2 = x1 + col_w + gap_x
    y1 = 8
    y2 = y1 + col_h + gap_y

    runtimes = [
        {
            "name": "Claude Code",
            "tag": "AGENTIC CLI",
            "role": "Terminal Coding Agent",
            "line1": "Autonomous feature delivery, iterative refactoring,",
            "line2": "and comprehensive test suites in local repositories.",
            "x": x1,
            "y": y1
        },
        {
            "name": "Codex",
            "tag": "BACKGROUND DEV",
            "role": "Cloud Engineering Harness",
            "line1": "Isolated worktrees, automated background reviews,",
            "line2": "and multi-repo contextual code intelligence.",
            "x": x2,
            "y": y1
        },
        {
            "name": "Hermes",
            "tag": "TOOL RUNTIME",
            "role": "Autonomous Agent Engine",
            "line1": "Local tool execution, custom skill invocation, continuous",
            "line2": "subagent delegation, and memory persistence.",
            "x": x1,
            "y": y2
        },
        {
            "name": "Anti-Gravity",
            "tag": "ORCHESTRATION",
            "role": "Multi-Agent Systems",
            "line1": "Coordinated multi-agent planning, rigorous decision",
            "line2": "trees, safety boundaries, and verifiable deliverables.",
            "x": x2,
            "y": y2
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

    for r in runtimes:
        svg.extend([
            f'  <!-- Card {r["name"]} -->',
            f'  <g transform="translate({r["x"]}, {r["y"]})">',
            f'    <rect width="{col_w}" height="{col_h}" rx="10" fill="#090D16" stroke="rgba(255, 255, 255, 0.09)" stroke-width="1.2" />',
            f'    <rect x="18" y="14" width="6" height="6" rx="3" fill="#818CF8" />',
            f'    <text class="font-mono" x="30" y="20" fill="#818CF8" font-size="10px" font-weight="600" letter-spacing="0.08em">{r["tag"]}</text>',
            f'    <text class="font-sans" x="18" y="42" fill="#FFFFFF" font-size="15px" font-weight="700">{r["name"]}</text>',
            f'    <text class="font-sans" x="145" y="42" fill="#94A3B8" font-size="12.5px" font-weight="500">· {r["role"]}</text>',
            f'    <line x1="18" y1="52" x2="{col_w - 18}" y2="52" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />',
            f'    <text class="font-sans" x="18" y="70" fill="#94A3B8" font-size="12px" font-weight="400">',
            f'      <tspan x="18" dy="0">{r["line1"]}</tspan>',
            f'      <tspan x="18" dy="16">{r["line2"]}</tspan>',
            '    </text>',
            '  </g>'
        ])

    svg.append('</svg>')
    return '\n'.join(svg)

def create_stack_surface():
    width = 1100
    height = 145
    col_w = 535
    col_h = 125
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
        '    <text class="font-mono" x="20" y="24" fill="#818CF8" font-size="10.5px" font-weight="600" letter-spacing="0.08em">FRONTEND &amp; INTERFACE ARCHITECTURE</text>',
        '    <text class="font-sans" x="20" y="44" fill="#F8FAFC" font-size="13.5px" font-weight="600">Client Systems, Reactive UI &amp; State Orchestration</text>',
        '    <line x1="20" y1="56" x2="515" y2="56" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />',
        '',
        '    <!-- Tech Pills -->',
        '    <g transform="translate(20, 72)">',
        '      <rect x="0" y="0" width="76" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="38" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">React</text>',
        '      <rect x="84" y="0" width="102" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="135" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">TypeScript</text>',
        '      <rect x="194" y="0" width="100" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="244" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">JavaScript</text>',
        '      <rect x="302" y="0" width="112" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="358" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Tailwind CSS</text>',
        '      <rect x="422" y="0" width="72" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="458" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">SCSS</text>',
        '    </g>',
        '  </g>',
        '',
        '  <!-- Column 2: Backend, Systems & Data -->',
        f'  <g transform="translate({x2}, {y})">',
        f'    <rect width="{col_w}" height="{col_h}" rx="10" fill="#090D16" stroke="rgba(255, 255, 255, 0.09)" stroke-width="1.2" />',
        '    <text class="font-mono" x="20" y="24" fill="#818CF8" font-size="10.5px" font-weight="600" letter-spacing="0.08em">BACKEND, SYSTEMS &amp; DATA PIPELINES</text>',
        '    <text class="font-sans" x="20" y="44" fill="#F8FAFC" font-size="13.5px" font-weight="600">Deterministic APIs, Services &amp; Relational Data</text>',
        '    <line x1="20" y1="56" x2="515" y2="56" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />',
        '',
        '    <!-- Tech Pills -->',
        '    <g transform="translate(20, 72)">',
        '      <rect x="0" y="0" width="82" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="41" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Python</text>',
        '      <rect x="90" y="0" width="92" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="136" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Symfony</text>',
        '      <rect x="190" y="0" width="88" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="234" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">Node.js</text>',
        '      <rect x="286" y="0" width="116" height="26" rx="5" fill="rgba(255, 255, 255, 0.04)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1" />',
        '      <text class="font-mono" x="344" y="17" fill="#E2E8F0" font-size="11px" font-weight="500" text-anchor="middle">PostgreSQL</text>',
        '    </g>',
        '  </g>',
        '</svg>'
    ]
    return '\n'.join(svg)

def create_divider():
    width = 1100
    height = 24
    cx = width / 2
    cy = 12
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '  <defs>',
        '    <linearGradient id="laserLine" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#4F46E5" stop-opacity="0" />',
        '      <stop offset="15%" stop-color="#6366F1" stop-opacity="0.25" />',
        '      <stop offset="35%" stop-color="#818CF8" stop-opacity="0.8" />',
        '      <stop offset="48%" stop-color="#C7D2FE" stop-opacity="0.95" />',
        '      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="1" />',
        '      <stop offset="52%" stop-color="#C7D2FE" stop-opacity="0.95" />',
        '      <stop offset="65%" stop-color="#818CF8" stop-opacity="0.8" />',
        '      <stop offset="85%" stop-color="#6366F1" stop-opacity="0.25" />',
        '      <stop offset="100%" stop-color="#4F46E5" stop-opacity="0" />',
        '    </linearGradient>',
        '    <radialGradient id="opticGlow" cx="50%" cy="50%" r="50%">',
        '      <stop offset="0%" stop-color="#818CF8" stop-opacity="0.55" />',
        '      <stop offset="30%" stop-color="#6366F1" stop-opacity="0.3" />',
        '      <stop offset="70%" stop-color="#4F46E5" stop-opacity="0.08" />',
        '      <stop offset="100%" stop-color="#05070D" stop-opacity="0" />',
        '    </radialGradient>',
        '    <radialGradient id="coreSparkle" cx="50%" cy="50%" r="50%">',
        '      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />',
        '      <stop offset="40%" stop-color="#C7D2FE" stop-opacity="0.4" />',
        '      <stop offset="100%" stop-color="#818CF8" stop-opacity="0" />',
        '    </radialGradient>',
        '  </defs>',
        '',
        '  <!-- Atmospheric glow ellipse behind the laser -->',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="320" ry="10" fill="url(#opticGlow)" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="80" ry="4" fill="url(#coreSparkle)" />',
        '',
        '  <!-- Crisp laser beam lines -->',
        f'  <line x1="0" y1="{cy}" x2="{width}" y2="{cy}" stroke="url(#laserLine)" stroke-width="1.5" />',
        f'  <line x1="{cx - 160}" y1="{cy}" x2="{cx + 160}" y2="{cy}" stroke="#FFFFFF" stroke-width="0.8" stroke-opacity="0.75" />',
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
    print("Successfully generated refined assets.")
