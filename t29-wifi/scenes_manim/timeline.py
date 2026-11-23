"""Scene: Every Wi-Fi generation on a left-to-right timeline.

Class `Timeline` (~20s). Each generation is a node on a horizontal axis with
its dual name (Wi-Fi N / 802.11xx), a year, a peak speed, and a vertical bar
whose height scales log-ishly with speed so the oldest standards are tiny and
Wi-Fi 7 towers. A highlight sweep travels left-to-right lighting each node in
turn. Continuous motion driven by a master ValueTracker.

Dark palette only, TEXT labels only. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Line,
    RoundedRectangle,
    Text,
    VGroup,
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


class Timeline(Scene):
    def construct(self):
        title = Text("EVERY WI-FI GENERATION", font=HEAD, color=INK,
                     weight="BOLD").scale(0.62)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- generation data -------------------------------------------------
        # (dual name, year, speed label, mbps for log scaling, color)
        gens = [
            ("802.11b/g", "1999-2003", "54 Mbps", 54.0, SILVER),
            ("Wi-Fi 4 / 802.11n", "2009", "600 Mbps", 600.0, AMBER),
            ("Wi-Fi 5 / 802.11ac", "2014", "~1.3 Gbps", 1300.0, TEAL),
            ("Wi-Fi 6 / 802.11ax", "2019", "9.6 Gbps", 9600.0, GREEN),
            ("Wi-Fi 6E", "2021", "+6 GHz", 9600.0, VIOLET),
            ("Wi-Fi 7 / 802.11be", "2024", "46 Gbps", 46000.0, GOLD),
        ]
        n = len(gens)

        # --- axis ------------------------------------------------------------
        base_y = -2.55
        x_left = -6.2
        x_right = 6.2
        axis = Line([x_left, base_y, 0], [x_right, base_y, 0],
                    stroke_color=SECOND, stroke_width=2.5)
        self.play(Create(axis), run_time=0.7)

        xs = np.linspace(x_left + 0.9, x_right - 0.9, n)

        # log-ish bar heights: tiny early, towering Wi-Fi 7.
        max_h = 4.1
        min_h = 0.28
        logs = np.array([np.log10(g[3]) for g in gens])
        lo, hi = logs.min(), logs.max()
        heights = min_h + (max_h - min_h) * (logs - lo) / (hi - lo)

        bars = []
        nodes = []
        name_lbls = []
        for i, (name, year, speed, mbps, col) in enumerate(gens):
            x = xs[i]
            h = heights[i]
            bar = RoundedRectangle(
                corner_radius=0.06, width=0.7, height=h,
                stroke_color=col, stroke_width=2,
                fill_color=col, fill_opacity=0.14,
            )
            bar.move_to([x, base_y + h / 2.0, 0])
            bars.append((bar, col))

            node = Dot(color=col, radius=0.11).move_to([x, base_y, 0])
            nodes.append((node, col))

            name = name.replace(" / ", "\n")
            nl = Text(name, font=MONO, color=col, line_spacing=0.7).scale(0.26)
            nl.move_to([x, base_y - 0.42, 0])
            name_lbls.append(nl)

            yr = Text(year, font=MONO, color=SECOND).scale(0.2)
            yr.next_to(nl, DOWN, buff=0.08)

            sp = Text(speed, font=MONO, color=col).scale(0.24)
            sp.move_to([x, base_y + h + 0.26, 0])

            self.play(
                Create(bar),
                FadeIn(node),
                FadeIn(nl),
                FadeIn(yr),
                FadeIn(sp),
                run_time=0.42,
            )
            # keep speed labels bolt to bars for the pulse phase.
            bars[i] = (bar, col, sp, h, x)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        sweep_period = 6.0

        def sweep_pos(tt):
            frac = (tt % sweep_period) / sweep_period
            return x_left + frac * (x_right - x_left)

        # Highlight sweep line travelling along the timeline.
        sweeper = Line([0, base_y - 0.1, 0], [0, base_y + max_h + 0.4, 0],
                       stroke_color=INK, stroke_width=3, stroke_opacity=0.0)

        def make_sweeper():
            def _upd(m):
                tt = t.get_value()
                x = sweep_pos(tt)
                m.put_start_and_end_on(
                    [x, base_y - 0.1, 0], [x, base_y + max_h + 0.4, 0])
                m.set_stroke(opacity=0.35)
            return _upd
        sweeper.add_updater(make_sweeper())
        self.add(sweeper)

        # Each bar/node brightens as the sweep passes, breathing otherwise.
        for i in range(n):
            bar, col, sp, h, x = bars[i]
            node, _ = nodes[i]
            cm = ManimColor(col)
            ink = ManimColor(INK)

            def make_bar_upd(b_bar, b_node, b_sp, b_col, b_ink, bx, bi):
                def _upd(m):
                    tt = t.get_value()
                    sx = sweep_pos(tt)
                    d = abs(sx - bx)
                    near = np.clip(1.0 - d / 1.1, 0.0, 1.0)
                    breath = 0.5 + 0.5 * np.sin(1.5 * tt + bi * 0.8)
                    glow = 0.14 + 0.5 * near + 0.08 * breath
                    b_bar.set_fill(opacity=np.clip(glow, 0.0, 0.85))
                    hot = interpolate_color(b_col, b_ink, 0.6 * near)
                    b_bar.set_stroke(color=hot, width=2 + 2.5 * near)
                    b_node.set_color(hot)
                    radius = 0.11 + 0.08 * near
                    b_node.scale_to_fit_width(2 * radius)
                    b_sp.set_opacity(0.45 + 0.55 * near)
                return _upd
            bar.add_updater(make_bar_upd(bar, node, sp, cm, ink, x, i))

        # Data packets ride up the towering bars to hint throughput.
        rng = np.random.default_rng(29)
        packets = VGroup()
        pkt_meta = []
        for i in range(n):
            _, col, _, h, x = bars[i]
            count = 1 + int(round(3 * heights[i] / max_h))
            for _ in range(count):
                dot = Dot(color=col, radius=0.045)
                packets.add(dot)
                period = 1.3 + 1.2 * rng.random()
                offset = rng.uniform(0, period)
                pkt_meta.append((x, h, period, offset))

        def make_packet(px, ph, period, offset):
            def _upd(m):
                tt = (t.get_value() + offset) % period
                frac = tt / period
                y = base_y + 0.05 + frac * (ph - 0.1)
                m.move_to([px, y, 0])
                m.set_opacity(np.clip(1.3 * (1 - frac), 0.0, 1.0))
            return _upd

        for dot, meta in zip(packets, pkt_meta):
            dot.add_updater(make_packet(*meta))
        self.add(packets)

        # Subtitle under the title.
        sub = Text("from 54 Mbps to 46 Gbps in 25 years", font=MONO,
                   color=SECOND).scale(0.3)
        sub.next_to(title, DOWN, buff=0.14)

        def sub_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                                         np.sin(t.get_value() * 1.4)))
        sub.add_updater(sub_upd)
        self.add(sub)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
