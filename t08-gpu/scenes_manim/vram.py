"""Scene: VRAM you actually need — a drawn bar chart.

Class `Vram` (~16s). A vertical bar chart titled "VRAM you actually need".
Four bars with labels and GB values: 1080p High 8 GB (green), 1440p High 12 GB
(teal), 4K High 16 GB (amber), 4K + Ray tracing 20 GB (coral). Bars grow in on
a continuous rising/settling motion, then gently pulse; a moving guide line
sweeps. Values appear atop each bar. Caption on buying enough VRAM. Continuous
motion via a master ValueTracker, no freeze.

Dark palette only, TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  red #FF5C47  amber #FFB020  teal #2DD4BF  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Text,
    VGroup,
    Line,
    ValueTracker,
    config,
    FadeIn,
    Create,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    rate_functions,
)

BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#76D64A"
RED = "#FF5C47"
AMBER = "#FFB020"
TEAL = "#2DD4BF"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Vram(Scene):
    def construct(self):
        title = Text("VRAM you actually need", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- Chart geometry --------------------------------------------------
        base_y = -2.6
        MAX_GB = 24.0
        CHART_H = 4.6
        H_PER = CHART_H / MAX_GB  # vertical units per GB

        specs = [("1080p High", 8, GREEN),
                 ("1440p High", 12, TEAL),
                 ("4K High", 16, AMBER),
                 ("4K + Ray tracing", 20, RED)]
        xs = [-4.2, -1.4, 1.4, 4.2]
        bar_w = 1.6

        # Axis line.
        axis = Line([-6.0, base_y, 0], [6.0, base_y, 0],
                    stroke_color=SECOND, stroke_width=2)
        self.play(Create(axis), run_time=0.4)

        bars = []
        bar_groups = VGroup()
        for (name, gb, col), bx in zip(specs, xs):
            full_h = gb * H_PER
            rect = Rectangle(width=bar_w, height=0.01, stroke_color=col,
                             stroke_width=2, fill_color=col, fill_opacity=0.35)
            rect.move_to([bx, base_y + 0.005, 0])
            val = Text("%d GB" % gb, font=MONO, color=col,
                       weight="BOLD").scale(0.32)
            nm = Text(name, font=MONO, color=SECOND).scale(0.24)
            nm.move_to([bx, base_y - 0.3, 0])
            grp = VGroup(rect, val, nm)
            grp.rect = rect
            grp.val = val
            grp.full_h = full_h
            grp.bx = bx
            grp.col = col
            bars.append(grp)
            bar_groups.add(grp)
            self.add(grp)

        cap = Text("buy enough VRAM for your resolution — it ages the card.",
                   font=HEAD, color=SECOND).scale(0.3)
        cap.to_edge(DOWN, buff=0.35)

        # Moving guide line (horizontal sweep up/down).
        guide = Line([-6.0, base_y, 0], [6.0, base_y, 0],
                     stroke_color=SILVER, stroke_width=1.5,
                     stroke_opacity=0.5)
        self.add(guide)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # Bars rise and settle (0..~4s), then pulse gently; guide sweeps.
        # =====================================================================
        t = ValueTracker(0.0)

        for i, b in enumerate(bars):
            def make_bar(bb, phase):
                full_h = bb.full_h

                def _upd(m):
                    tt = t.get_value()
                    # Rising/settling: ease to full height over ~3.5s, with a
                    # slight overshoot, then gentle breathing pulse.
                    rise = min(tt / 3.5, 1.0)
                    eased = rate_functions.ease_out_back(rise)
                    pulse = 1.0 + 0.02 * np.sin(2.0 * tt + phase)
                    h = max(full_h * eased * pulse, 0.01)
                    bb.rect.stretch_to_fit_height(h)
                    bb.rect.move_to([bb.bx, base_y + h / 2, 0])
                    bb.val.move_to([bb.bx, base_y + h + 0.28, 0])
                    bb.val.set_opacity(np.clip(rise * 1.5, 0.0, 1.0))
                return _upd
            b.add_updater(make_bar(b, i * 0.8))

        # Guide line sweeps up and down the chart.
        def guide_upd(m):
            tt = t.get_value()
            frac = 0.5 + 0.5 * np.sin(tt * 0.9)
            y = base_y + frac * CHART_H
            m.put_start_and_end_on([-6.0, y, 0], [6.0, y, 0])
            m.set_stroke(opacity=0.25 + 0.3 * frac)
        guide.add_updater(guide_upd)

        self.play(t.animate.set_value(12.5), run_time=12.5,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
