"""Scene: AI upscaling — render low, show high.

Class `Upscale` (~18s). Left-to-right pipeline: a small low-res pixel grid
labelled "render 1080p · 2.1M px" -> an "AI upscaler (tensor cores)" box ->
a large high-res grid labelled "output 4K · 8.3M px". A cost tag pulses
"+FPS · slight artifacts". Frame packets flow through the pipeline repeatedly;
the output grid's pixels shimmer/densify. Continuous motion, no freeze.

Dark palette only, TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  amber #FFB020  teal #2DD4BF  violet #B06BFF  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Dot,
    Arrow,
    ValueTracker,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
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
AMBER = "#FFB020"
TEAL = "#2DD4BF"
VIOLET = "#B06BFF"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Upscale(Scene):
    def construct(self):
        title = Text("AI upscaling", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- Low-res grid (left) --------------------------------------------
        def make_grid(n, cell, color, fill):
            grp = VGroup()
            for _ in range(n * n):
                px = Rectangle(width=cell, height=cell,
                               stroke_color=color, stroke_width=1,
                               fill_color=fill, fill_opacity=0.7)
                grp.add(px)
            grp.arrange_in_grid(rows=n, cols=n, buff=0.0)
            return grp

        lo = make_grid(6, 0.3, TEAL, "#0C1917")
        lo.move_to(LEFT * 4.6 + DOWN * 0.2)
        lo_lbl = Text("render 1080p · 2.1M px", font=MONO,
                      color=TEAL).scale(0.26)
        lo_lbl.next_to(lo, DOWN, buff=0.25)

        # --- Upscaler box (middle) ------------------------------------------
        box = RoundedRectangle(
            corner_radius=0.12, width=2.6, height=2.0,
            stroke_color=VIOLET, stroke_width=2.5,
            fill_color="#15102099", fill_opacity=0.8,
        ).move_to(DOWN * 0.2)
        box_glow = RoundedRectangle(
            corner_radius=0.12, width=2.6, height=2.0,
            stroke_color=VIOLET, stroke_width=10, stroke_opacity=0.12,
            fill_opacity=0,
        ).move_to(box)
        box_lbl = Text("AI upscaler\n(tensor cores)", font=MONO, color=VIOLET,
                       line_spacing=0.8).scale(0.3)
        box_lbl.move_to(box.get_center())

        # --- High-res grid (right) ------------------------------------------
        hi = make_grid(12, 0.21, GREEN, "#122111")
        hi.move_to(RIGHT * 4.6 + DOWN * 0.2)
        hi_lbl = Text("output 4K · 8.3M px", font=MONO,
                      color=GREEN).scale(0.26)
        hi_lbl.next_to(hi, DOWN, buff=0.25)

        # Arrows.
        a1 = Arrow(lo.get_right(), box.get_left(), color=SECOND,
                   stroke_width=3, buff=0.2, max_tip_length_to_length_ratio=0.2)
        a2 = Arrow(box.get_right(), hi.get_left(), color=SECOND,
                   stroke_width=3, buff=0.2, max_tip_length_to_length_ratio=0.2)

        self.play(GrowFromCenter(lo), run_time=0.6)
        self.play(Create(box), FadeIn(box_glow), FadeIn(box_lbl),
                  Create(a1), run_time=0.6)
        self.play(GrowFromCenter(hi), Create(a2), run_time=0.6)
        self.play(FadeIn(lo_lbl), FadeIn(hi_lbl), run_time=0.4)

        # --- Cost tag --------------------------------------------------------
        cost = Text("+FPS · slight artifacts", font=HEAD,
                    color=AMBER).scale(0.34)
        cost.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cost, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Box glow breathing.
        def box_breath(m):
            tt = t.get_value()
            box_glow.set_stroke(opacity=0.1 + 0.16 *
                                (0.5 + 0.5 * np.sin(2.2 * tt)))
        box_glow.add_updater(box_breath)

        # Low-res pixels shimmer.
        for i, px in enumerate(lo):
            def make_lo(p, phase):
                def _upd(m):
                    tt = t.get_value()
                    p.set_fill(opacity=0.45 + 0.35 *
                               (0.5 + 0.5 * np.sin(1.6 * tt + phase)))
                return _upd
            px.add_updater(make_lo(px, (i % 11) * 0.5))

        # High-res pixels densify/shimmer faster (finer detail).
        for i, px in enumerate(hi):
            def make_hi(p, phase):
                def _upd(m):
                    tt = t.get_value()
                    p.set_fill(opacity=0.4 + 0.45 *
                               (0.5 + 0.5 * np.sin(3.0 * tt + phase)))
                return _upd
            px.add_updater(make_hi(px, (i % 29) * 0.35))

        # --- Frame packets flow through the pipeline repeatedly --------------
        route = [lo.get_center(), box.get_center(), hi.get_center()]
        y = lo.get_center()[1]
        packets = VGroup()
        PACKET_N = 6
        meta = []
        for k in range(PACKET_N):
            dot = Dot(color=AMBER, radius=0.09)
            packets.add(dot)
            period = 4.5
            offset = k * (period / PACKET_N)
            meta.append((period, offset))

        xs = [route[0][0], route[1][0], route[2][0]]

        def make_packet(mt):
            period, offset = mt

            def _upd(m):
                frac = ((t.get_value() + offset) % period) / period
                # Travel left->right across the full pipeline x-span.
                x = xs[0] + (xs[2] - xs[0]) * frac
                m.move_to([x, y, 0])
                # Change hue as it crosses the upscaler.
                if x >= xs[1]:
                    m.set_color(GREEN)
                else:
                    m.set_color(AMBER)
                edge = min(frac, 1 - frac) * 2
                m.set_opacity(np.clip(0.3 + 1.2 * edge, 0.2, 1.0))
            return _upd

        for dot, mt in zip(packets, meta):
            dot.add_updater(make_packet(mt))
        self.add(packets)

        # Cost tag pulse.
        def cost_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                                         np.sin(t.get_value() * 2.4)))
        cost.add_updater(cost_upd)

        self.play(t.animate.set_value(14.0), run_time=14.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
