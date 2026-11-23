"""Scene: Every Version of Windows — a time axis from 1985 to today.

Class `Timeline` (~20s). A horizontal TIME AXIS from 1985 to 2025 with year
ticks. The 12 versions are plotted as labelled node dots at their real year,
coloured by reputation (green loved / coral hated / amber-silver meh). Above
the long-reigning classics (95, XP, 7, 10) a longer "reign" bar; above the
short-lived duds (ME, Vista, 8) a short stub. A scan marker sweeps left->right
on a loop; as it passes a node, that node pulses/enlarges and its label
brightens. Title "1985 -> today" with a small legend.

Dark palette only, TEXT labels only (no logos), continuous motion driven by a
master ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Line,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    rate_functions,
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

# verdict -> colour
VERD = {"loved": GREEN, "hated": CORAL, "meh": AMBER}

# (label, year, verdict, reign_years)  reign used for the bar length above node
VERSIONS = [
    ("1.0", 1985, "meh", 2),
    ("3.1", 1992, "loved", 3),
    ("95", 1995, "loved", 3),
    ("98", 1998, "loved", 2),
    ("ME", 2000, "hated", 1),
    ("2000", 2000, "loved", 3),
    ("XP", 2001, "loved", 8),
    ("Vista", 2007, "hated", 2),
    ("7", 2009, "loved", 6),
    ("8", 2012, "hated", 2),
    ("10", 2015, "loved", 6),
    ("11", 2021, "meh", 4),
]

Y0, Y1 = 1985, 2025


class Timeline(Scene):
    def construct(self):
        title = Text("1985 -> today", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- geometry of the axis -------------------------------------------
        x_left, x_right = -6.4, 6.4
        axis_y = -0.9

        def x_of(year):
            frac = (year - Y0) / (Y1 - Y0)
            return x_left + frac * (x_right - x_left)

        axis = Line([x_left, axis_y, 0], [x_right, axis_y, 0],
                    stroke_color=SILVER, stroke_width=3)
        self.play(Create(axis), run_time=0.7)

        # --- year ticks every 5 years ---------------------------------------
        ticks = VGroup()
        tick_lbls = VGroup()
        for yr in range(1985, 2026, 5):
            xx = x_of(yr)
            tk = Line([xx, axis_y - 0.12, 0], [xx, axis_y + 0.12, 0],
                      stroke_color=SECOND, stroke_width=2)
            ticks.add(tk)
            tl = Text(str(yr), font=MONO, color=SECOND).scale(0.24)
            tl.next_to(tk, DOWN, buff=0.12)
            tick_lbls.add(tl)
        self.play(*[Create(t) for t in ticks],
                  *[FadeIn(l) for l in tick_lbls], run_time=0.8)

        # --- version nodes ---------------------------------------------------
        node_dots = []        # the pulsing dot per version
        node_labels = []      # the brightening name label per version
        node_x = []           # axis x of each node
        base_r = 0.11
        long_reign = {"95", "XP", "7", "10"}
        short_reign = {"ME", "Vista", "8"}

        bars = VGroup()
        anims = []
        for name, year, verdict, reign in VERSIONS:
            col = VERD[verdict]
            xx = x_of(year)
            node_x.append(xx)

            dot = Dot([xx, axis_y, 0], color=col, radius=base_r)
            node_dots.append(dot)

            # name label alternates above/below to avoid crowding at 2000.
            lbl = Text(name, font=MONO, color=col, weight="BOLD").scale(0.3)
            lbl.move_to([xx, axis_y, 0])
            node_labels.append(lbl)

            # reign bar above the node: long for classics, stub for duds.
            if name in long_reign:
                span = (reign / (Y1 - Y0)) * (x_right - x_left)
                bar = Line([xx, axis_y + 0.55, 0],
                           [xx + span, axis_y + 0.55, 0],
                           stroke_color=col, stroke_width=7)
            elif name in short_reign:
                span = 0.28
                bar = Line([xx, axis_y + 0.55, 0],
                           [xx + span, axis_y + 0.55, 0],
                           stroke_color=col, stroke_width=7)
            else:
                span = 0.5
                bar = Line([xx, axis_y + 0.55, 0],
                           [xx + span, axis_y + 0.55, 0],
                           stroke_color=col, stroke_width=3,
                           stroke_opacity=0.5)
            bars.add(bar)
            anims.append(GrowFromCenter(dot))

        # place labels: stagger up/down so near-collisions (ME/2000) read.
        up_down = [1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1]
        for lbl, dot, ud in zip(node_labels, node_dots, up_down):
            if ud > 0:
                lbl.next_to(dot, UP, buff=0.24)
            else:
                lbl.next_to(dot, DOWN, buff=0.5)

        self.play(*anims, lag_ratio=0.06, run_time=1.2)
        self.play(*[Create(b) for b in bars],
                  *[FadeIn(l) for l in node_labels],
                  lag_ratio=0.04, run_time=1.2)

        # --- scan marker -----------------------------------------------------
        scan = Line([x_left, axis_y - 1.3, 0], [x_left, axis_y + 1.9, 0],
                    stroke_color=TEAL, stroke_width=3, stroke_opacity=0.8)
        self.add(scan)

        # --- legend ----------------------------------------------------------
        def chip(col, word):
            d = Dot(color=col, radius=0.09)
            w = Text(word, font=MONO, color=SECOND).scale(0.26)
            w.next_to(d, RIGHT, buff=0.12)
            return VGroup(d, w)

        legend = VGroup(chip(GREEN, "loved"),
                        chip(CORAL, "hated"),
                        chip(AMBER, "meh")).arrange(RIGHT, buff=0.6)
        legend.to_edge(UP, buff=0.42).to_edge(RIGHT, buff=0.6)
        self.play(FadeIn(legend), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        SWEEP = 6.0         # seconds per left->right sweep
        x0, x1 = x_left, x_right
        node_x_arr = np.array(node_x)

        # scan marker sweeps left->right on a loop.
        def scan_upd(m):
            frac = (t.get_value() % SWEEP) / SWEEP
            xx = x0 + frac * (x1 - x0)
            m.move_to([xx, axis_y + 0.3, 0])
        scan.add_updater(scan_upd)

        # nodes: breathe always; pulse + brighten as the scan passes.
        for i, dot in enumerate(node_dots):
            nx = node_x_arr[i]

            def make_dot_upd(d, nxx, phase):
                def _upd(m):
                    tt = t.get_value()
                    frac = (tt % SWEEP) / SWEEP
                    scan_x = x0 + frac * (x1 - x0)
                    prox = np.exp(-((scan_x - nxx) ** 2) / 0.09)
                    breathe = 0.5 + 0.5 * np.sin(2.0 * tt + phase)
                    s = 1.0 + 0.18 * breathe + 1.1 * prox
                    d.set(width=2 * base_r * s)
                    d.set_opacity(np.clip(0.75 + 0.25 * breathe + prox, 0, 1))
                return _upd
            dot.add_updater(make_dot_upd(dot, nx, i * 0.5))

        for i, (lbl, col) in enumerate(zip(node_labels,
                                           [VERD[v[2]] for v in VERSIONS])):
            nx = node_x_arr[i]

            def make_lbl_upd(nxx, c):
                def _upd(m):
                    frac = (t.get_value() % SWEEP) / SWEEP
                    scan_x = x0 + frac * (x1 - x0)
                    prox = np.exp(-((scan_x - nxx) ** 2) / 0.09)
                    m.set_opacity(np.clip(0.45 + 0.55 * prox, 0, 1))
                return _upd
            lbl.add_updater(make_lbl_upd(nx, col))

        # subtle legend breathing keeps the frame alive.
        def legend_upd(m):
            m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 1.4)))
        legend.add_updater(legend_upd)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
