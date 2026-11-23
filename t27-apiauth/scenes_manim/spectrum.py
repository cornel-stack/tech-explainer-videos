"""Scene: THE STRENGTH LADDER — auth methods ranked weak -> strong.

Class `Spectrum` (~18s). A diagonal ladder climbs from bottom-left
"WEAK / simple" (CORAL) to top-right "STRONG / complex" (GREEN). Rungs,
bottom -> top:
  No Auth, API Key, Basic, Bearer, Session, JWT, OAuth 2.0, HMAC, mTLS
Each rung is a MONO label, tinted along a CORAL -> AMBER -> GREEN gradient
as it climbs. A highlight driven by `t` climbs the ladder, lighting each
rung in turn. A side axis shows "security ↑" and "complexity ↑" rising
together. Caption cycles:
  "stronger locks cost more complexity" -> "match the lock to the value".
Continuous loop.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Line,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    rate_functions,
    interpolate_color,
)

# --- palette -----------------------------------------------------------------
BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#35E08A"
TEAL = "#2DD4BF"
VIOLET = "#B06BFF"
AMBER = "#FFB020"
CORAL = "#FF5C47"
GOLD = "#E8C24A"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Spectrum(Scene):
    def construct(self):
        title = Text("The strength ladder: weak to strong",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.5)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        rungs = [
            "No Auth", "API Key", "Basic", "Bearer", "Session",
            "JWT", "OAuth 2.0", "HMAC", "mTLS",
        ]
        n = len(rungs)

        # gradient endpoints CORAL -> AMBER -> GREEN
        c_coral = ManimColor(CORAL)
        c_amber = ManimColor(AMBER)
        c_green = ManimColor(GREEN)

        def grad(frac):
            # two-segment gradient coral->amber->green
            if frac < 0.5:
                return interpolate_color(c_coral, c_amber, frac / 0.5)
            return interpolate_color(c_amber, c_green, (frac - 0.5) / 0.5)

        # --- ladder geometry: diagonal bottom-left -> top-right -------------
        x0, y0 = -5.0, -2.7   # bottom-left (weak)
        x1, y1 = 2.6, 2.4     # top-right (strong)

        rail_l = Line(
            np.array([x0 - 0.35, y0 - 0.15, 0]),
            np.array([x1 - 0.35, y1 - 0.15, 0]),
            stroke_color=SECOND, stroke_width=2, stroke_opacity=0.4,
        )
        rail_r = Line(
            np.array([x0 + 0.35, y0 + 0.15, 0]),
            np.array([x1 + 0.35, y1 + 0.15, 0]),
            stroke_color=SECOND, stroke_width=2, stroke_opacity=0.4,
        )
        self.play(Create(rail_l), Create(rail_r), run_time=0.6)

        # --- build rungs -----------------------------------------------------
        rung_groups = []
        rung_centers = []
        rung_colors = []
        for i, name in enumerate(rungs):
            frac = i / (n - 1)
            col = grad(frac)
            rung_colors.append(col)
            cx = x0 + (x1 - x0) * frac
            cy = y0 + (y1 - y0) * frac
            rung_centers.append(np.array([cx, cy, 0]))

            bar = RoundedRectangle(
                corner_radius=0.08, width=2.4, height=0.5,
                stroke_color=col, stroke_width=2.2,
                fill_color=col, fill_opacity=0.12,
            ).move_to(np.array([cx, cy, 0]))
            lbl = Text(name, font=MONO, color=col).scale(0.34)
            lbl.move_to(bar.get_center())
            g = VGroup(bar, lbl)
            rung_groups.append(g)

        self.play(*[FadeIn(g, shift=UP * 0.15) for g in rung_groups],
                  lag_ratio=0.08, run_time=1.4)

        # --- weak / strong endpoint labels ----------------------------------
        weak = VGroup(
            Text("WEAK", font=MONO, color=CORAL, weight="BOLD").scale(0.36),
            Text("simple", font=MONO, color=SECOND).scale(0.26),
        ).arrange(DOWN, buff=0.08)
        weak.move_to(np.array([x0 - 0.1, y0 - 0.95, 0]))

        strong = VGroup(
            Text("STRONG", font=MONO, color=GREEN, weight="BOLD").scale(0.36),
            Text("complex", font=MONO, color=SECOND).scale(0.26),
        ).arrange(DOWN, buff=0.08)
        strong.move_to(np.array([x1 + 0.3, y1 + 0.9, 0]))
        self.play(FadeIn(weak), FadeIn(strong), run_time=0.5)

        # --- side axis (right edge): security / complexity rising -----------
        axis = Line(
            np.array([5.6, -2.7, 0]), np.array([5.6, 2.6, 0]),
            stroke_color=SILVER, stroke_width=2.5,
        )
        sec_ax = Text("security", font=MONO, color=GREEN).scale(0.28)
        sec_ax.move_to(np.array([5.0, 2.3, 0]))
        cplx_ax = Text("complexity", font=MONO, color=AMBER).scale(0.26)
        cplx_ax.move_to(np.array([4.85, 1.7, 0]))
        arrow_up = Text("UP", font=MONO, color=SILVER).scale(0.26)
        arrow_up.move_to(np.array([5.6, 2.95, 0]))
        self.play(Create(axis), FadeIn(sec_ax), FadeIn(cplx_ax),
                  FadeIn(arrow_up), run_time=0.5)

        # a marker that climbs the side axis
        axis_marker = Dot(color=GREEN, radius=0.09)
        axis_marker.move_to(np.array([5.6, -2.7, 0]))
        self.add(axis_marker)

        # --- caption ---------------------------------------------------------
        caption = Text("stronger locks cost more complexity", font=HEAD,
                       color=SILVER).scale(0.36)
        caption.to_edge(DOWN, buff=0.4)
        caption._key = ""
        self.add(caption)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # highlight climbs the ladder: one full climb every CLIMB seconds
        CLIMB = 7.2

        # --- rung highlight updaters (factory captures locals) --------------
        def rung_factory(bar, lbl, idx, col):
            step = idx / (n - 1)

            def _upd(m):
                # climbing position 0..1 (loops)
                climb = (t.get_value() % CLIMB) / CLIMB
                # distance of this rung from the climbing head
                d = climb - step
                # light up when the head is at/above this rung, with a trail
                if d < 0:
                    glow = 0.0
                else:
                    glow = np.clip(1.0 - d * 3.0, 0.0, 1.0)
                bar.set_fill(opacity=0.12 + 0.6 * glow)
                bar.set_stroke(width=2.2 + 3.5 * glow)
                lbl.set_opacity(0.55 + 0.45 * glow)
                # brighten label toward white when lit
                lit = interpolate_color(col, ManimColor(INK), 0.55 * glow)
                lbl.set_color(lit)
            return _upd
        for i, g in enumerate(rung_groups):
            bar, lbl = g[0], g[1]
            g.add_updater(rung_factory(bar, lbl, i, rung_colors[i]))

        # --- climbing head dot on the ladder --------------------------------
        head = Dot(color=INK, radius=0.11)
        self.add(head)

        def head_upd(m):
            climb = (t.get_value() % CLIMB) / CLIMB
            cx = x0 + (x1 - x0) * climb
            cy = y0 + (y1 - y0) * climb
            m.move_to(np.array([cx, cy, 0]))
            col = grad(climb)
            m.set_color(col)
            m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 4.0)))
        head.add_updater(head_upd)

        # --- axis marker climbs in lockstep ---------------------------------
        def marker_upd(m):
            climb = (t.get_value() % CLIMB) / CLIMB
            y = -2.7 + (2.6 - (-2.7)) * climb
            m.move_to(np.array([5.6, y, 0]))
            m.set_color(grad(climb))
        axis_marker.add_updater(marker_upd)

        # --- rails breathe so scene reads "alive" ---------------------------
        def rail_upd(m):
            m.set_stroke(opacity=0.3 + 0.2 * (0.5 + 0.5 *
                                              np.sin(t.get_value() * 2.0)))
        rail_l.add_updater(rail_upd)
        rail_r.add_updater(rail_upd)

        # --- caption cycles --------------------------------------------------
        cap_texts = [
            "stronger locks cost more complexity",
            "match the lock to the value",
        ]

        def cap_upd(m):
            idx = int(t.get_value() // (CLIMB / 2)) % len(cap_texts)
            txt = cap_texts[idx]
            if txt != m._key:
                m._key = txt
                new = Text(txt, font=HEAD, color=SILVER).scale(0.36)
                new.to_edge(DOWN, buff=0.4)
                m.become(new)
        caption.add_updater(cap_upd)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
