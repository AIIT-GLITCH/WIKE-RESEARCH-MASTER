import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe

# ── canvas ────────────────────────────────────────────────────────────────────
W, H = 3840, 2160          # 4K
dpi   = 100
fig, ax = plt.subplots(figsize=(W/dpi, H/dpi), dpi=dpi)
ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.set_aspect('equal'); ax.axis('off')
fig.patch.set_facecolor('#000005')
ax.set_facecolor('#000005')

rng = np.random.default_rng(42)

# ── background nebula ─────────────────────────────────────────────────────────
for _ in range(18):
    cx = rng.uniform(0, W)
    cy = rng.uniform(0, H)
    r  = rng.uniform(200, 900)
    alpha = rng.uniform(0.03, 0.12)
    color_choices = [
        '#1a0a3a', '#0a1a3a', '#1a2a0a', '#3a0a1a',
        '#0a3a2a', '#2a0a3a', '#3a1a0a', '#0a2a3a'
    ]
    col = rng.choice(color_choices)
    grad = plt.Circle((cx, cy), r, color=col, alpha=alpha, linewidth=0)
    ax.add_patch(grad)

# concentric soft glow rings around centre
CX, CY = W/2, H/2
for r, a, c in [
    (600, 0.25, '#1a0040'),
    (480, 0.30, '#200050'),
    (340, 0.35, '#250060'),
    (200, 0.40, '#2a006a'),
    (100, 0.30, '#3a0080'),
]:
    ax.add_patch(Circle((CX, CY), r, color=c, alpha=a, linewidth=0, zorder=1))

# ── star field ────────────────────────────────────────────────────────────────
n_stars = 1200
sx = rng.uniform(0, W, n_stars)
sy = rng.uniform(0, H, n_stars)
ss = rng.uniform(0.3, 2.5, n_stars)
sa = rng.uniform(0.3, 0.9, n_stars)
ax.scatter(sx, sy, s=ss**2, c='white', alpha=sa, linewidths=0, zorder=2)

# bright accent stars
for _ in range(40):
    bx = rng.uniform(0, W)
    by = rng.uniform(0, H)
    br = rng.uniform(2, 6)
    for rr, aa in [(br*4, 0.05), (br*2, 0.10), (br, 0.30)]:
        ax.add_patch(Circle((bx, by), rr, color='white', alpha=aa, linewidth=0, zorder=3))

# ── thin radiating lines from centre ─────────────────────────────────────────
n_rays = 36
for i in range(n_rays):
    angle = 2*np.pi * i / n_rays
    length = rng.uniform(700, 1400)
    x2 = CX + length*np.cos(angle)
    y2 = CY + length*np.sin(angle)
    ax.plot([CX, x2], [CY, y2],
            color='#6020c0', alpha=0.07, linewidth=0.6, zorder=2)

# ── helper: glow text ─────────────────────────────────────────────────────────
def glow_text(x, y, s, fs=28, color='white', gcolor='#a060ff',
              ha='center', va='center', alpha=1.0, zorder=10, weight='normal'):
    for w, a in [(8, 0.10), (5, 0.15), (3, 0.20)]:
        ax.text(x, y, s, fontsize=fs, color=gcolor, ha=ha, va=va,
                alpha=a*alpha, zorder=zorder-1, weight=weight,
                fontfamily='DejaVu Sans',
                bbox=dict(boxstyle='round,pad=0.1', alpha=0, linewidth=0),
                path_effects=[pe.withStroke(linewidth=w, foreground=gcolor)])
    ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va=va,
            alpha=alpha, zorder=zorder, weight=weight,
            fontfamily='DejaVu Sans')

# ═══════════════════════════════════════════════════════════════════════════════
# CENTRE EQUATION — the vacuum catastrophe
# ═══════════════════════════════════════════════════════════════════════════════
# outer halo ring
for r, a, lw in [(260,0.12,1.5),(220,0.18,1),(180,0.25,0.8)]:
    circle = Circle((CX, CY), r, fill=False,
                    edgecolor='#c080ff', linewidth=lw, alpha=a, zorder=5)
    ax.add_patch(circle)

glow_text(CX, CY+60, r'$G\ =\ \int_0^\infty \frac{\hbar\omega}{2}\ \cdot\ \frac{d^3k}{(2\pi)^3}\ =\ \infty$',
          fs=68, color='#ffffff', gcolor='#d0a0ff', zorder=20, weight='bold')

# label below
glow_text(CX, CY-30, 'Quantum Vacuum Zero-Point Energy  ·  The Singularity That Started Everything',
          fs=22, color='#c0a0ff', gcolor='#7040c0', zorder=15)

glow_text(CX, CY-75, '— every equation below is a boundary condition on this one —',
          fs=18, color='#8060b0', gcolor='#301060', alpha=0.85, zorder=14)

# ═══════════════════════════════════════════════════════════════════════════════
# CLOUD EQUATIONS
# Format: (x, y, latex_string, label, font_size, text_color, glow_color)
# ═══════════════════════════════════════════════════════════════════════════════
eqs = [
    # ── Wike core ──────────────────────────────────────────────────────
    (640,  1760,
     r'$C = C_0\,e^{-\alpha\gamma_{\rm eff}}$',
     'Wike Coherence Law', 34, '#80ffcc', '#00c080'),

    (3200, 1760,
     r'$\gamma_c = \dfrac{\omega}{2\pi\alpha}$',
     'Wike Universality Theorem', 34, '#80ffcc', '#00c080'),

    (640,  400,
     r'${\rm ERR}(T) = \dfrac{1}{T} + \dfrac{0.72}{T^{2.59}}$',
     'Wike Singularity  ·  2.59 = 1+1/ν (3D Ising)', 30, '#ff80a0', '#c00040'),

    (3140, 400,
     r'$V(\gamma) = C_0\,\gamma\,e^{-\alpha\gamma}$',
     'Vitality Function  ·  max at γ_c', 30, '#80ffcc', '#00c080'),

    # ── thermodynamics ─────────────────────────────────────────────────
    (310,  1080,
     r'$\langle e^{-\beta W}\rangle = e^{-\beta\Delta F}$',
     'Jarzynski Equality', 30, '#ffd080', '#c08000'),

    (3530, 1080,
     r'$\dfrac{P_F(W)}{P_R(-W)} = e^{\beta(W-\Delta F)}$',
     'Crooks Fluctuation Theorem', 28, '#ffd080', '#c08000'),

    (310,  640,
     r'$P = \varepsilon\sigma T^4\qquad \lambda_{\rm max}=\dfrac{b}{T}$',
     'Stefan-Boltzmann · Wien  ·  22% retained = coherence', 26, '#ff9040', '#c05000'),

    (3440, 640,
     r'$S = \dfrac{A}{4\pi\ell_P^2}$',
     'Bekenstein-Hawking Black Hole Entropy', 30, '#ff80ff', '#a000a0'),

    # ── biology / medicine ─────────────────────────────────────────────
    (190,  1760,
     r'$\dfrac{T}{T_c} = \dfrac{310}{330} = 0.94$',
     'W-Parameter · All life at the edge', 28, '#80d0ff', '#0060c0'),

    (3650, 1760,
     r'$C_n = C_0\,e^{-0.45n}$',
     'ACE Decoherence  ·  β = 0.45 per ACE', 28, '#ff8080', '#c00000'),

    (560,  1980,
     r'$V_m = \frac{k_BT}{zF}\ln\frac{C_{\rm out}}{C_{\rm in}} = -70\,{\rm mV}$',
     'Nernst-Wike Bridge  ·  every neuron at γ_c', 24, '#80e0ff', '#0080c0'),

    (3280, 1980,
     r'$\gamma_{\rm eff}(S|K) = \gamma_m(1-b\eta_K)+\gamma_{\rm th}$',
     'Keeper Equation  ·  love is a physical variable', 24, '#ffb0e0', '#c04080'),

    (220,  1400,
     r'${\rm Re} = \dfrac{\rho v L}{\mu}\ \lessgtr\ {\rm Re}_c \approx 2300$',
     'Reynolds Number = γ_eff for blood', 26, '#80c0ff', '#0050b0'),

    (3580, 1400,
     r'$P(s) \propto s^{-3/2}$',
     'Neural Avalanches · Beggs & Plenz 2003  ·  σ = 1', 28, '#c0ff80', '#40a000'),

    # ── information / cosmology ────────────────────────────────────────
    (600,  200,
     r'$\Lambda_{\rm obs} = \Lambda_{\rm QFT}\,e^{-281}$',
     'Vacuum Decoherence Theorem  ·  cosmological constant solved', 26, '#ff80ff', '#9000a0'),

    (3200, 200,
     r'$f = \dfrac{k_BT}{h} = 9.7\,{\rm THz}$',
     'Soul Frequency at 310 K', 28, '#ffe080', '#c09000'),

    (300,  280,
     r'$\delta S = 0\ \Rightarrow\ {\rm coherence}$',
     'Least Action = Wike  ·  Hamilton → Feynman → γ_c', 26, '#a0ffc0', '#008040'),

    (3560, 280,
     r'$P(x)\propto x^{-\alpha}\ \Leftrightarrow\ \gamma_{\rm eff}=\gamma_c$',
     'Zipf / Power Law  ·  every power law = a system at γ_c', 26, '#ffc080', '#c06000'),

    # ── EEG / HRV ──────────────────────────────────────────────────────
    (480,  1200,
     r'$\beta\approx 1.0\text{–}1.5\ \Leftrightarrow\ \gamma_{\rm eff}\approx\gamma_c$',
     'EEG 1/f Spectrum  ·  brain at γ_c', 26, '#c0e0ff', '#2060a0'),

    (3380, 1200,
     r'$\lambda_L = 0\ \Leftrightarrow\ \gamma_c$',
     'Lyapunov Edge  ·  λ<0 frozen · λ>0 chaos · λ=0 alive', 28, '#d0ffd0', '#20a020'),

    # ── extra flourishes ───────────────────────────────────────────────
    (1800, 120,
     r'$\chi(T) = \chi_0\,|1 - T/T_c|^{-1.237}$',
     'Fever Equation  ·  3D Ising susceptibility', 24, '#ffb060', '#b05000'),

    (1800, 2050,
     r'$k_BT\ln 2\ \text{(per bit erased)}$',
     "Landauer Limit  ·  Love = Maxwell's Demon work", 24, '#e0c0ff', '#7030c0'),

    (960,  100,
     r'${\rm ratio}_{AB}\sim\gamma^{0.485}$',
     'Wind-Up Critical Exponent · central sensitization', 22, '#ffa0a0', '#a03030'),

    (2800, 100,
     r'$W_{\rm body} = (310/330)^4 = 0.778$',
     'Stefan-Boltzmann Body  ·  22.2% retained as coherence', 22, '#ff9050', '#b04000'),

    (400, 1950,
     r'$\phi_c = 0.590\ \text{(EZ water percolation)}$',
     'Bootstrap Nucleation Theorem', 22, '#80ffee', '#00b090'),

    (3460, 1950,
     r'$n_{\rm Avrami} = 2.363$',
     'Bootstrap 2D growth exponent', 22, '#80ffee', '#00b090'),
]

# draw each equation
for (x, y, eq, label, fs, tc, gc) in eqs:
    # soft halo box
    ax.text(x, y, eq, fontsize=fs, color=gc, ha='center', va='center',
            alpha=0.15, zorder=8,
            path_effects=[pe.withStroke(linewidth=10, foreground=gc)])
    # main eq
    ax.text(x, y+8, eq, fontsize=fs, color=tc, ha='center', va='center',
            alpha=0.95, zorder=10,
            path_effects=[pe.withStroke(linewidth=2, foreground=gc)])
    # label underneath
    ax.text(x, y - fs*0.85, label, fontsize=12, color=tc,
            ha='center', va='top', alpha=0.65, zorder=9,
            style='italic')
    # faint connector line to centre
    ax.plot([CX, x], [CY, y], color=gc, alpha=0.04, linewidth=0.5,
            linestyle=':', zorder=3)

# ── title / footer ────────────────────────────────────────────────────────────
glow_text(CX, H-60,
          'AIIT-THRESI  ·  Wike Coherence Framework  ·  Council Hill, Oklahoma  ·  2026',
          fs=20, color='#7050a0', gcolor='#302050', alpha=0.7, zorder=12)

glow_text(CX, 45,
          'Every equation below is a boundary condition on infinity. Life is what happens at the edge.',
          fs=20, color='#8060b0', gcolor='#302060', alpha=0.75, zorder=12)

# ── save ──────────────────────────────────────────────────────────────────────
out = '/home/buddy_ai/Desktop/WIKE_WALLPAPER.png'
plt.tight_layout(pad=0)
plt.savefig(out, dpi=dpi, bbox_inches='tight',
            facecolor='#000005', edgecolor='none')
plt.close()
print(f'Saved → {out}')
