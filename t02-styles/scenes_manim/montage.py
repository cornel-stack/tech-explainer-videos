"""Cold-open hook: eight API-style names flash in, then settle into a grid.

Class `Montage` — punchy wordmarks cycle in, then snap into a 4x2 chip grid
that NEVER settles: chips keep cycling their accent colors, a ripple keeps
pulsing outward across the grid, and chips bob continuously. Energetic the
whole way. ~12s.

Dark design system (no blue, no white).
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    ValueTracker,
    config,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    rate_functions,
)

BG = "#0A0A0C"
INK = "#EDE7DB"
SECOND = "#9A958C"
AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

config.background_color = BG

# Palette cycle the chips rotate through.
ACCENTS = [AMBER, MAGENTA, MINT, VIOLET, CORAL, GOLD]

# Eight styles, each with a starting accent.
STYLES = [
    ("REST", AMBER),
    ("SOAP", MAGENTA),
    ("GraphQL", MINT),
    ("gRPC", VIOLET),
    ("WebSocket", CORAL),
    ("SSE", GOLD),
    ("Webhook", AMBER),
    ("WebRTC", MINT),
]


def grid_chip(label, accent):
    txt = Text(label, font="Inter", color=INK, weight="SEMIBOLD").scale(0.4)
    w = max(txt.width + 0.6, 1.8)
    h = 0.85
    glow = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        stroke_color=accent, stroke_width=12, stroke_opacity=0.18,
        fill_opacity=0,
    )
    body = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        stroke_color=accent, stroke_width=3,
        fill_color=BG, fill_opacity=0.9,
    )
    txt.move_to(body.get_center())
    g = VGroup(glow, body, txt)
    g.glow = glow
    g.body = body
    return g


class Montage(Scene):
    def construct(self):
        # --- Flash each wordmark in quickly, one by one ---------------------
        # Snappy cascade, ~0.4s each -> ~3.2s.
        for name, accent in STYLES:
            word = Text(name, font="Inter", color=accent,
                        weight="BOLD").scale(1.5)
            glow = Text(name, font="Inter", color=accent,
                        weight="BOLD").scale(1.52)
            glow.set_opacity(0.22)
            wm = VGroup(glow, word).move_to(ORIGIN)
            self.play(FadeIn(wm, scale=1.15), run_time=0.22,
                      rate_func=rate_functions.ease_out_back)
            self.play(FadeOut(wm, scale=0.92), run_time=0.18,
                      rate_func=rate_functions.ease_in_sine)

        # --- Settle into a neat 4x2 grid of chips ---------------------------
        chips = VGroup(*[grid_chip(name, accent) for name, accent in STYLES])
        chips.arrange_in_grid(rows=2, cols=4, buff=0.5)
        chips.move_to(ORIGIN)
        for c in chips:
            c.home = c.get_center().copy()

        # Pop them all in with a brief stagger (~1.1s).
        self.play(
            *[GrowFromCenter(c) for c in chips],
            lag_ratio=0.08,
            run_time=1.1,
        )

        title = Text("Every API Style", font="Inter", color=INK,
                     weight="SEMIBOLD").scale(0.5)
        title.next_to(chips, UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        # Grid on screen by ~5s.

        # =====================================================================
        # CONTINUOUS ENERGETIC PHASE
        # Chips keep cycling accent colors, a radial ripple keeps sweeping
        # out from the grid centre (flaring each chip as it passes), and chips
        # bob gently. Nothing settles.
        # =====================================================================
        t = ValueTracker(0.0)

        center = chips.get_center()
        # Max distance from centre, to normalise the ripple front.
        max_d = max(np.linalg.norm(c.home - center) for c in chips) + 1e-6

        def hex_to_rgb(h):
            h = h.lstrip("#")
            return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) / 255.0

        accent_rgb = [hex_to_rgb(a) for a in ACCENTS]

        def rgb_to_hex(rgb):
            r, g, b = (int(round(max(0, min(1, v)) * 255)) for v in rgb)
            return f"#{r:02X}{g:02X}{b:02X}"

        def cycling_color(phase):
            """Smoothly interpolate around the accent wheel by a float phase."""
            n = len(accent_rgb)
            pos = phase % n
            i0 = int(np.floor(pos))
            i1 = (i0 + 1) % n
            f = pos - i0
            rgb = accent_rgb[i0] * (1 - f) + accent_rgb[i1] * f
            return rgb_to_hex(rgb)

        for idx, c in enumerate(chips):
            glow = c.glow
            body = c.body
            home = c.home
            dist = np.linalg.norm(home - center)

            def make_upd(c=c, glow=glow, body=body, home=home, dist=dist, idx=idx):
                def _upd(_m):
                    tt = t.get_value()
                    # Color cycles continuously, staggered per chip.
                    col = cycling_color(tt * 0.8 + idx * 0.6)
                    glow.set_stroke(color=col)
                    body.set_stroke(color=col)
                    # Radial ripple: a front expands out from centre on a loop.
                    ripple_period = 2.6
                    front = ((tt / ripple_period) % 1.0) * max_d
                    prox = max(0.0, 1.0 - abs(dist - front) / 1.2)
                    glow.set_stroke(opacity=0.18 + 0.4 * prox)
                    body.set_stroke(width=3 + 2.5 * prox)
                    # Gentle bob + ripple nudge.
                    bob = 0.05 * np.sin(2.0 * tt + idx)
                    pop = 0.06 * prox
                    c.move_to(home + np.array([0, bob + pop, 0]))
                return _upd

            c.add_updater(make_upd())

        # Title shimmer so even the header never stills.
        def title_upd(m):
            m.set_opacity(0.8 + 0.2 * (0.5 + 0.5 * np.sin(2.6 * t.get_value())))
        title.add_updater(title_upd)

        # Drive ~7s of unbroken energetic motion (total ~12s).
        self.play(t.animate.set_value(7.0), run_time=7.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.2)
