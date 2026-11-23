"""Scene: Modulation — cleaner signal, more bits per nudge (QAM).

Class `Modulation` (~20s). A horizontal carrier sine wave (VMobject of points
driven by t, so it scrolls/oscillates). Above it a bitstream "1011 0010". The
wave is modulated: segments change amplitude to encode each symbol. On the
right, a 16-point QAM constellation; one dot lights GREEN per symbol in time.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    Text,
    VGroup,
    VMobject,
    Dot,
    Line,
    ValueTracker,
    config,
    FadeIn,
    Create,
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


class Modulation(Scene):
    def construct(self):
        title = Text("Cleaner signal -> more bits per nudge (QAM)",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- geometry -------------------------------------------------------
        wave_left = -6.2
        wave_right = 1.4
        wave_y = -0.6
        wave_w = wave_right - wave_left

        # symbols drive the amplitude of each wave segment
        symbols = [0.35, 0.7, 0.5, 1.0, 0.25, 0.85, 0.6, 0.45]
        n_sym = len(symbols)

        # baseline axis
        axis = Line([wave_left, wave_y, 0], [wave_right, wave_y, 0],
                    stroke_color=SECOND, stroke_width=1.2)
        self.play(Create(axis), run_time=0.5)

        # --- bitstream above the wave ---------------------------------------
        bit_groups = ["1011", "0010", "1101", "0110",
                      "1001", "0111", "1010", "0001"]
        bits_row = VGroup()
        for i in range(n_sym):
            g = Text(bit_groups[i % len(bit_groups)], font=MONO,
                     color=TEAL).scale(0.3)
            cx = wave_left + (i + 0.5) * (wave_w / n_sym)
            g.move_to([cx, wave_y + 2.0, 0])
            bits_row.add(g)
        self.play(*[FadeIn(b, shift=DOWN * 0.1) for b in bits_row],
                  lag_ratio=0.08, run_time=0.8)

        # --- QAM constellation (right) --------------------------------------
        const_center = np.array([4.1, wave_y + 0.2, 0.0])
        grid = VGroup()
        qam_dots = []
        step = 0.42
        for r in range(4):
            for c in range(4):
                x = const_center[0] + (c - 1.5) * step
                y = const_center[1] + (1.5 - r) * step
                d = Dot([x, y, 0], radius=0.07, color=SECOND)
                d.set_opacity(0.5)
                grid.add(d)
                qam_dots.append(d)
        qbox_lbl = Text("16-QAM", font=MONO, color=VIOLET).scale(0.3)
        qbox_lbl.next_to(grid, UP, buff=0.35)
        self.play(*[FadeIn(d) for d in grid], FadeIn(qbox_lbl),
                  lag_ratio=0.02, run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        sym_period = 0.9  # seconds a symbol is "active"

        def amp_at(frac):
            # frac in [0,1] across the wave; returns amplitude from symbols,
            # smoothly stepped per symbol segment.
            pos = frac * n_sym
            idx = int(np.clip(pos, 0, n_sym - 1))
            local = pos - idx
            a0 = symbols[idx]
            a1 = symbols[min(idx + 1, n_sym - 1)]
            blend = 0.5 - 0.5 * np.cos(np.pi * np.clip(local * 2 - 0.5, 0, 1))
            return a0 * (1 - blend) + a1 * blend

        # --- travelling carrier wave ----------------------------------------
        carrier = VMobject(stroke_color=TEAL, stroke_width=2.6)

        def carrier_upd(m):
            pts = []
            steps = 220
            tt = t.get_value()
            for s in range(steps + 1):
                frac = s / steps
                x = wave_left + frac * wave_w
                amp = 0.95 * amp_at(frac)
                phase = 2.0 * np.pi * 7.0 * frac - tt * 4.0
                y = wave_y + amp * np.sin(phase)
                pts.append([x, y, 0])
            m.set_points_as_corners(pts)
            m.set_stroke(opacity=0.9)
        carrier.add_updater(carrier_upd)
        self.add(carrier)

        # envelope (upper amplitude outline) to make modulation readable
        env = VMobject(stroke_color=GOLD, stroke_width=1.6)

        def env_upd(m):
            pts = []
            steps = 120
            for s in range(steps + 1):
                frac = s / steps
                x = wave_left + frac * wave_w
                y = wave_y + 0.95 * amp_at(frac)
                pts.append([x, y, 0])
            m.set_points_as_corners(pts)
            m.set_stroke(opacity=0.45)
        env.add_updater(env_upd)
        self.add(env)

        # moving "now" cursor that scans symbols left to right
        cursor = Line([0, wave_y - 1.1, 0], [0, wave_y + 1.1, 0],
                      stroke_color=GREEN, stroke_width=2.0)

        def cursor_upd(m):
            frac = (t.get_value() / (n_sym * sym_period)) % 1.0
            x = wave_left + frac * wave_w
            m.put_start_and_end_on([x, wave_y - 1.1, 0],
                                   [x, wave_y + 1.1, 0])
            m.set_stroke(opacity=0.6)
        cursor.add_updater(cursor_upd)
        self.add(cursor)

        # bit groups light up as the cursor passes
        def make_bit_glow(idx):
            def _upd(m):
                frac = (t.get_value() / (n_sym * sym_period)) % 1.0
                active = int(frac * n_sym)
                if active == idx:
                    m.set_color(GREEN)
                    m.set_opacity(1.0)
                else:
                    m.set_color(TEAL)
                    m.set_opacity(0.55)
            return _upd
        for i, b in enumerate(bits_row):
            b.add_updater(make_bit_glow(i))

        # constellation: one dot lights per symbol in time
        # map each symbol index to a constellation cell deterministically
        sym_to_cell = [5, 10, 6, 15, 0, 11, 9, 2]

        def make_const(cell_idx):
            def _upd(m):
                frac = (t.get_value() / (n_sym * sym_period)) % 1.0
                active = int(frac * n_sym)
                lit = sym_to_cell[active % len(sym_to_cell)]
                if cell_idx == lit:
                    m.set_color(GREEN)
                    m.set_opacity(1.0)
                    m.scale_to_fit_width(0.22)
                else:
                    m.set_color(SECOND)
                    m.set_opacity(0.45)
                    m.scale_to_fit_width(0.14)
            return _upd
        for i, d in enumerate(qam_dots):
            d.add_updater(make_const(i))

        cap = Text("each nudge carries 4 bits", font=MONO,
                   color=SILVER).scale(0.3)
        cap.to_edge(DOWN, buff=0.5)
        self.add(cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
