"""Scene 7: just switches + a clock + one loop -- the brain.

Class `Modern` (~19s). Zoom-out: a CPU die (a square chip grid of glowing
cores + cache blocks) pulsing with the clock, labelled "tens of billions of
transistors", "many cores", "one loop, billions/sec". A gentle reveal
assembling all prior concepts into the whole chip. Caption: "just switches +
a clock + one loop -- the brain".

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92  green #35E08A
  teal #2DD4BF  violet #B06BFF  amber #FFB020  coral #FF5C47
  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Line,
    Square,
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
    interpolate_color,
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


class Modern(Scene):
    def construct(self):
        title = Text("The whole chip", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the CPU die: outer package + inner grid ------------------------
        die_c = np.array([-1.3, -0.2, 0.0])
        package = RoundedRectangle(corner_radius=0.18, width=4.6, height=4.6,
                                   stroke_color=SILVER, stroke_width=3,
                                   fill_color="#101014", fill_opacity=0.95)
        package.move_to(die_c)
        die_lbl = Text("CPU die", font=MONO, color=SILVER).scale(0.3)
        die_lbl.next_to(package, DOWN, buff=0.2)
        self.play(Create(package), FadeIn(die_lbl), run_time=0.9)

        # inner grid of blocks: cores (green) + cache (teal) + control (amber)
        grid = VGroup()
        blocks = []  # (mobject, kind, phase)
        n = 6
        cell = 0.66
        origin = die_c + np.array([-(n - 1) / 2 * cell,
                                   (n - 1) / 2 * cell, 0])
        rng = np.random.default_rng(7)
        kinds = []
        for r in range(n):
            for c in range(n):
                # outer ring -> cache, inner -> cores, a few control cells
                edge = (r == 0 or r == n - 1 or c == 0 or c == n - 1)
                if edge:
                    kind = "cache"
                else:
                    kind = "core"
                kinds.append(kind)
        # sprinkle a couple of control cells in the interior
        interior_idx = [i for i, k in enumerate(kinds) if k == "core"]
        for ci in rng.choice(interior_idx, size=3, replace=False):
            kinds[ci] = "ctrl"

        col_map = {"core": GREEN, "cache": TEAL, "ctrl": AMBER}
        fill_map = {"core": "#0E1A14", "cache": "#0E1A1A",
                    "ctrl": "#1A1405"}
        for idx in range(n * n):
            r = idx // n
            c = idx % n
            kind = kinds[idx]
            pos = origin + np.array([c * cell, -r * cell, 0])
            sq = Square(side_length=cell * 0.82,
                        stroke_color=col_map[kind], stroke_width=1.6,
                        fill_color=fill_map[kind], fill_opacity=0.9)
            sq.move_to(pos)
            grid.add(sq)
            blocks.append((sq, kind, (r + c) * 0.5 + idx * 0.05))
        self.play(FadeIn(grid, lag_ratio=0.02), run_time=1.4)

        # --- side labels, revealed as the build assembles -------------------
        lab_x = 3.6
        trans_lbl = Text("tens of billions", font=MONO,
                         color=SILVER).scale(0.32)
        trans_lbl.move_to([lab_x, 1.7, 0])
        trans_sub = Text("of transistors", font=MONO,
                         color=SECOND).scale(0.26)
        trans_sub.next_to(trans_lbl, DOWN, buff=0.08)

        cores_lbl = Text("many cores", font=MONO, color=GREEN).scale(0.32)
        cores_lbl.move_to([lab_x, 0.5, 0])

        loop_lbl = Text("one loop,", font=MONO, color=VIOLET).scale(0.32)
        loop_lbl.move_to([lab_x, -0.7, 0])
        loop_sub = Text("billions/sec", font=MONO, color=AMBER).scale(0.28)
        loop_sub.next_to(loop_lbl, DOWN, buff=0.08)

        self.play(FadeIn(trans_lbl), FadeIn(trans_sub), run_time=0.5)
        self.play(FadeIn(cores_lbl), run_time=0.4)
        self.play(FadeIn(loop_lbl), FadeIn(loop_sub), run_time=0.5)

        # --- clock indicator driving the whole die -------------------------
        clk_dot = Dot(package.get_corner(UP + LEFT) + np.array([0.3, -0.3, 0]),
                      color=AMBER, radius=0.1)
        clk_txt = Text("clock", font=MONO, color=AMBER).scale(0.24)
        clk_txt.next_to(clk_dot, RIGHT, buff=0.12)
        self.play(FadeIn(clk_dot), FadeIn(clk_txt), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        TICK = 1.6

        def clock_phase(tt):
            return (TICK * tt) % 1.0

        # whole die pulses with the clock; a wave sweeps across the grid
        dim_map = {"core": ManimColor("#163024"),
                   "cache": ManimColor("#123030"),
                   "ctrl": ManimColor("#2A2008")}
        hot_map = {"core": ManimColor(GREEN),
                   "cache": ManimColor(TEAL),
                   "ctrl": ManimColor(AMBER)}

        def make_block(sq_m, kind, phase, pos):
            c_dim = dim_map[kind]
            c_hot = hot_map[kind]
            # diagonal wave position
            wave_base = (pos[0] - die_c[0]) + (die_c[1] - pos[1])

            def _upd(m):
                ph = TICK * t.get_value()
                s = 0.5 + 0.5 * np.sin(2 * np.pi *
                                       (ph - wave_base * 0.35) + phase * 0.0)
                m.set_stroke(interpolate_color(c_dim, c_hot, 0.3 + 0.7 * s),
                             width=1.4 + 1.2 * s)
                m.set_fill(interpolate_color(ManimColor("#0E0E12"), c_dim,
                           0.5 + 0.5 * s), opacity=0.9)
            return _upd
        for sq, kind, phase in blocks:
            sq.add_updater(make_block(sq, kind, phase, sq.get_center()))

        # clock dot flashes each rising edge
        c_clk_dim = ManimColor("#3A2A08")
        c_clk_hot = ManimColor(AMBER)

        def clk_upd(m):
            frac = clock_phase(t.get_value())
            flash = max(0.0, 1.0 - frac * 4.0)
            m.set_color(interpolate_color(c_clk_dim, c_clk_hot,
                        0.4 + 0.6 * flash))
            m.scale_to_fit_width(0.18 + 0.1 * flash)
        clk_dot.add_updater(clk_upd)

        # package edge subtly breathes
        c_pkg_dim = ManimColor("#4A4A52")
        c_pkg_hot = ManimColor(SILVER)

        def pkg_upd(m):
            s = 0.5 + 0.5 * np.sin(2 * np.pi * TICK * t.get_value())
            m.set_stroke(interpolate_color(c_pkg_dim, c_pkg_hot, 0.5 + 0.5
                         * s), width=3)
        package.add_updater(pkg_upd)

        # side labels gently pulse
        def make_lbl_pulse(phase):
            def _upd(m):
                m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                              np.sin(1.6 * t.get_value() + phase)))
            return _upd
        cores_lbl.add_updater(make_lbl_pulse(0.0))
        loop_lbl.add_updater(make_lbl_pulse(1.0))
        loop_sub.add_updater(make_lbl_pulse(1.0))
        trans_lbl.add_updater(make_lbl_pulse(2.0))

        # a summary line assembling the prior concepts
        summary = Text("switches -> gates -> bits -> clock -> loop -> chip",
                       font=MONO, color=SECOND).scale(0.3)
        summary.move_to([-1.3, -2.9, 0])

        def sum_upd(m):
            m.set_opacity(0.4 + 0.5 * (0.5 + 0.5 *
                          np.sin(1.2 * t.get_value())))
        summary.add_updater(sum_upd)
        self.add(summary)

        # caption
        cap = Text("just switches + a clock + one loop -- the brain",
                   font=HEAD, color=SECOND).scale(0.38)
        cap.to_edge(DOWN, buff=0.22)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
