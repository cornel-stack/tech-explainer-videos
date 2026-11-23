"""Scene: Walls — distance and walls kill the signal (the centrepiece).

Class `Walls` (~24s). Top-down house floorplan: Living room (router), Hall,
Kitchen, Bedroom (far corner behind 2 walls). The router emits expanding rings
that (a) fade with distance green->amber->coral and (b) drop sharply where they
cross a wall. The Bedroom sits in a coral dead zone showing "2 bars". Labels
"distance -> 1/4 signal" and "walls absorb".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Line,
    Circle,
    Text,
    VGroup,
    RoundedRectangle,
    Dot,
    ValueTracker,
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


class Walls(Scene):
    def construct(self):
        title = Text("Distance and walls kill the signal",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- floorplan outline ----------------------------------------------
        # overall house: 10 wide x 5.2 tall, centred and slightly low
        hw, hh = 10.0, 5.2
        cx, cy = 0.0, -0.4
        left = cx - hw / 2
        right = cx + hw / 2
        bottom = cy - hh / 2
        top = cy + hh / 2

        house = Rectangle(width=hw, height=hh, stroke_color=SILVER,
                          stroke_width=3.0, fill_color="#0C0D10",
                          fill_opacity=0.6).move_to([cx, cy, 0])

        # vertical wall split: left half (living/hall), right half (kitchen/bed)
        midx = cx  # vertical interior wall at x=0
        # horizontal split on the right half only (kitchen top / bedroom bottom)
        midy = cy  # y of horizontal wall

        # interior walls (thick), each with a doorway gap drawn as two segments
        vwall_top = Line([midx, top, 0], [midx, cy + 0.7, 0],
                         stroke_color=SILVER, stroke_width=6)
        vwall_bot = Line([midx, cy - 0.7, 0], [midx, bottom, 0],
                         stroke_color=SILVER, stroke_width=6)
        hwall_l = Line([midx, midy, 0], [midx - 2.3, midy, 0],
                       stroke_color=SILVER, stroke_width=6)
        hwall_r = Line([right, midy, 0], [midx + 1.0, midy, 0],
                       stroke_color=SILVER, stroke_width=6)

        walls = VGroup(vwall_top, vwall_bot, hwall_l, hwall_r)

        # room labels
        living_lbl = Text("Living room", font=MONO, color=SILVER).scale(0.3)
        living_lbl.move_to([left + 2.4, top - 0.5, 0])
        hall_lbl = Text("Hall", font=MONO, color=SILVER).scale(0.3)
        hall_lbl.move_to([left + 2.4, bottom + 0.5, 0])
        kitchen_lbl = Text("Kitchen", font=MONO, color=SILVER).scale(0.3)
        kitchen_lbl.move_to([right - 2.3, top - 0.5, 0])
        bedroom_lbl = Text("Bedroom", font=MONO, color=CORAL).scale(0.3)
        bedroom_lbl.move_to([right - 2.3, bottom + 0.9, 0])

        # router in living room (top-left area)
        router_pos = np.array([left + 1.6, top - 1.1, 0.0])
        r_body = RoundedRectangle(
            corner_radius=0.06, width=0.5, height=0.36,
            stroke_color=GREEN, stroke_width=2.0,
            fill_color="#0A1711", fill_opacity=1.0,
        ).move_to(router_pos)
        r_lbl = Text("router", font=MONO, color=GREEN).scale(0.24)
        r_lbl.next_to(r_body, DOWN, buff=0.1)

        # bedroom dead-zone tint (bottom-right)
        deadzone = Rectangle(width=4.0, height=1.9, stroke_width=0,
                             fill_color=CORAL, fill_opacity=0.08)
        deadzone.move_to([right - 2.0, bottom + 1.0, 0])

        self.play(Create(house), run_time=0.7)
        self.play(Create(walls), run_time=0.7)
        self.play(FadeIn(living_lbl), FadeIn(hall_lbl),
                  FadeIn(kitchen_lbl), FadeIn(bedroom_lbl),
                  FadeIn(deadzone), run_time=0.5)
        self.play(Create(r_body), FadeIn(r_lbl), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Walls to cross, by x-boundary (vertical wall) that a ring passes.
        vwall_x = midx

        def signal_color(strength):
            # strength in [0,1]: green -> amber -> coral as it weakens
            if strength > 0.55:
                f = (1.0 - strength) / 0.45
                return interpolate_color(GREEN, AMBER, np.clip(f, 0, 1))
            else:
                f = (0.55 - strength) / 0.55
                return interpolate_color(AMBER, CORAL, np.clip(f, 0, 1))

        # expanding rings that fade with distance + step down past the wall
        N_RINGS = 6
        ring_period = 3.0
        max_r = 7.5
        rings = VGroup()
        for i in range(N_RINGS):
            c = Circle(radius=0.2, stroke_width=4, fill_opacity=0,
                       stroke_color=GREEN).move_to(router_pos)
            rings.add(c)

        def make_ring(idx):
            offset = idx * (ring_period / N_RINGS)
            rx, ry = router_pos[0], router_pos[1]

            def _upd(m):
                tt = (t.get_value() + offset) % ring_period
                frac = tt / ring_period
                radius = 0.25 + frac * max_r
                m.set(width=radius * 2.0)
                m.move_to([rx, ry, 0])
                # distance attenuation (inverse-square-ish feel)
                dist_str = np.clip(1.0 - frac, 0.0, 1.0) ** 1.4
                # wall penalty: once the ring radius reaches the vertical wall
                # (router is left of it) strength drops sharply
                wall_gap = vwall_x - rx
                past_wall = radius > wall_gap
                strength = dist_str * (0.35 if past_wall else 1.0)
                m.set_color(signal_color(strength))
                m.set_stroke(opacity=np.clip(strength * 0.95, 0.03, 0.95))
            return _upd

        for i, c in enumerate(rings):
            c.add_updater(make_ring(i))
        self.add(rings)

        # bedroom weak-signal bars that flicker (2 of 4 lit)
        bars = VGroup()
        bar_base = np.array([right - 2.3, bottom + 0.4, 0.0])
        bar_heights = [0.18, 0.3, 0.42, 0.54]
        for i, h in enumerate(bar_heights):
            b = RoundedRectangle(
                corner_radius=0.02, width=0.16, height=h,
                stroke_width=0, fill_color=CORAL, fill_opacity=0.8,
            )
            b.move_to(bar_base + RIGHT * (i * 0.24))
            b.align_to(bar_base, DOWN)
            bars.add(b)

        def make_bar(idx):
            def _upd(m):
                if idx < 2:
                    # the 2 lit bars flicker
                    s = 0.5 + 0.5 * np.sin(t.get_value() * 6.0 + idx)
                    m.set_fill(CORAL, opacity=0.35 + 0.5 * s)
                else:
                    m.set_fill(SECOND, opacity=0.18)
            return _upd
        for i, b in enumerate(bars):
            b.add_updater(make_bar(i))
        self.add(bars)

        bars_lbl = Text("2 bars", font=MONO, color=CORAL).scale(0.26)
        bars_lbl.next_to(bars, UP, buff=0.12)

        def bars_lbl_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 6.0)
            m.set_opacity(0.5 + 0.5 * s)
        bars_lbl.add_updater(bars_lbl_upd)
        self.add(bars_lbl)

        # labels for the rules
        lbl_dist = Text("distance -> 1/4 signal", font=MONO,
                        color=AMBER).scale(0.3)
        lbl_dist.to_edge(DOWN, buff=0.75).shift(LEFT * 3.2)
        lbl_walls = Text("walls absorb", font=MONO, color=CORAL).scale(0.3)
        lbl_walls.to_edge(DOWN, buff=0.75).shift(RIGHT * 3.2)
        self.add(lbl_dist, lbl_walls)

        # router glow
        def router_glow(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 4.0)
            m.set_stroke(GREEN, opacity=0.6 + 0.4 * s)
        r_body.add_updater(router_glow)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
