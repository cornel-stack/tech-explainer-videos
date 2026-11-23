"""Scene: latency vs bandwidth — a highway analogy.

Class `Latency` (~20s). Top-left: LATENCY = delay before the first car/bit
arrives (start gate, a wait, then a lone first car). Top-right: BANDWIDTH =
cars-per-second once flowing (wide multi-lane road, steady stream). Below,
two meters: LATENCY stays ~FLAT across DDR3/DDR4/DDR5; BANDWIDTH DOUBLES each
step. Caption: "each DDR doubles bandwidth — but not latency".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Line,
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


class Latency(Scene):
    def construct(self):
        title = Text("Latency vs bandwidth — two different speeds",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- LEFT: latency — single narrow road with a start gate ------------
        lat_y = 1.4
        lat_road = Rectangle(
            width=5.0, height=0.55, stroke_width=0,
            fill_color="#141418", fill_opacity=1.0,
        ).move_to(np.array([-3.3, lat_y, 0]))
        gate = Line(
            np.array([-5.6, lat_y - 0.45, 0]),
            np.array([-5.6, lat_y + 0.45, 0]),
            stroke_color=CORAL, stroke_width=4)
        lat_lbl = Text("LATENCY — wait for the first bit", font=HEAD,
                       color=AMBER).scale(0.3)
        lat_lbl.next_to(lat_road, UP, buff=0.18).align_to(lat_road, LEFT)

        # --- RIGHT: bandwidth — wide multi-lane road -------------------------
        bw_y = 1.4
        lanes = VGroup()
        for i in range(3):
            lane = Rectangle(
                width=4.8, height=0.34, stroke_width=0,
                fill_color="#141418", fill_opacity=1.0,
            ).move_to(np.array([3.4, bw_y - 0.45 + i * 0.45, 0]))
            lanes.add(lane)
        bw_lbl = Text("BANDWIDTH — cars per second", font=HEAD,
                      color=GREEN).scale(0.3)
        bw_lbl.next_to(lanes, UP, buff=0.18).align_to(lanes, LEFT)

        self.play(Create(lat_road), Create(gate), FadeIn(lat_lbl),
                  *[Create(l) for l in lanes], FadeIn(bw_lbl),
                  run_time=0.9)

        # --- meters row ------------------------------------------------------
        ddr = ["DDR3", "DDR4", "DDR5"]
        ddr_x = [-4.2, -2.6, -1.0]
        ddr_lbls = VGroup()
        for name, x in zip(ddr, ddr_x):
            txt = Text(name, font=MONO, color=SECOND).scale(0.3)
            txt.move_to(np.array([x, -3.4, 0]))
            ddr_lbls.add(txt)

        lat_meter_lbl = Text("LATENCY", font=MONO, color=AMBER).scale(0.3)
        lat_meter_lbl.move_to(np.array([-4.2, -0.4, 0]))
        bw_meter_lbl = Text("BANDWIDTH", font=MONO, color=GREEN).scale(0.3)
        bw_meter_lbl.move_to(np.array([2.6, -0.4, 0]))

        # latency bars (flat), bandwidth bars (doubling)
        lat_bars = VGroup()
        for x in ddr_x:
            bar = Rectangle(
                width=0.7, height=0.9, stroke_width=0,
                fill_color=AMBER, fill_opacity=0.85,
            )
            bar.move_to(np.array([x, -1.4, 0]))
            lat_bars.add(bar)

        bw_x = [1.4, 3.0, 4.6]
        bw_heights = [0.6, 1.2, 2.4]
        bw_bars = VGroup()
        for x in bw_x:
            bar = Rectangle(
                width=0.7, height=0.1, stroke_width=0,
                fill_color=GREEN, fill_opacity=0.85,
            )
            bar.move_to(np.array([x, -2.9, 0]))
            bw_bars.add(bar)
        bw_ddr_lbls = VGroup()
        for name, x in zip(ddr, bw_x):
            txt = Text(name, font=MONO, color=SECOND).scale(0.3)
            txt.move_to(np.array([x, -3.4, 0]))
            bw_ddr_lbls.add(txt)

        self.play(FadeIn(lat_meter_lbl), FadeIn(bw_meter_lbl),
                  FadeIn(ddr_lbls), FadeIn(bw_ddr_lbls),
                  *[FadeIn(b) for b in lat_bars],
                  *[FadeIn(b) for b in bw_bars], run_time=0.7)

        caption = Text("each DDR doubles bandwidth — but not latency",
                       font=MONO, color=SECOND).scale(0.3)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # --- latency: lone first car after a wait (period with a gap) --------
        lat_start = np.array([-5.6, lat_y, 0])
        lat_end = np.array([-0.9, lat_y, 0])

        first_car = Dot(color=AMBER, radius=0.1)

        def lat_car_upd(m):
            period = 3.0
            wait = 1.2  # latency gap before it starts
            p = t.get_value() % period
            if p < wait:
                m.move_to(lat_start)
                m.set_opacity(0.0)
            else:
                a = (p - wait) / (period - wait)
                pos = lat_start * (1 - a) + lat_end * a
                m.move_to(pos)
                m.set_opacity(1.0)
        first_car.add_updater(lat_car_upd)
        self.add(first_car)

        gap_lbl = Text("<- the wait", font=MONO, color=CORAL).scale(0.24)
        gap_lbl.next_to(lat_road, DOWN, buff=0.12).align_to(lat_road, LEFT)

        def gap_upd(m):
            p = t.get_value() % 3.0
            m.set_opacity(1.0 if p < 1.2 else 0.3)
        gap_lbl.add_updater(gap_upd)
        self.add(gap_lbl)

        # --- bandwidth: steady stream across 3 lanes ------------------------
        bw_cars = VGroup()
        bw_meta = []
        rng = np.random.default_rng(7)
        for lane_i in range(3):
            ly = bw_y - 0.45 + lane_i * 0.45
            for k in range(6):
                dot = Dot(color=TEAL, radius=0.07)
                bw_cars.add(dot)
                speed = 2.0
                offset = rng.uniform(0, 4.8)
                bw_meta.append((ly, speed, offset))

        bw_left = 3.4 - 2.4
        bw_right = 3.4 + 2.4
        span = bw_right - bw_left

        def make_bw(ly, speed, offset):
            def _upd(m):
                x = bw_left + ((t.get_value() * speed + offset) % span)
                m.move_to(np.array([x, ly, 0]))
            return _upd
        for dot, (ly, speed, offset) in zip(bw_cars, bw_meta):
            dot.add_updater(make_bw(ly, speed, offset))
        self.add(bw_cars)

        # --- meters animate: DDR highlight steps; bw bar grows then loops ----
        base_y = -2.9 - 0.05
        for i, bar in enumerate(bw_bars):
            target_h = bw_heights[i]
            bx = bw_x[i]

            def make_bw_bar(bar, target_h, bx):
                def _upd(m):
                    # grow in over the first ~6s then hold with a gentle pulse
                    grow = rate_functions.ease_out_quad(
                        min(t.get_value() / 6.0, 1.0))
                    pulse = 1.0 + 0.04 * np.sin(3 * t.get_value())
                    h = max(target_h * grow * pulse, 0.05)
                    m.set(width=0.7, height=h)
                    m.move_to(np.array([bx, base_y + h / 2 + 0.05, 0]))
                return _upd
            bar.add_updater(make_bw_bar(bar, target_h, bx))

        # DDR step highlight sweeping across both meters
        step_group = VGroup(*ddr_lbls, *bw_ddr_lbls)

        for i, lbl in enumerate(ddr_lbls):
            idx = i

            def make_hl(idx, lbl):
                def _upd(m):
                    cur = int(t.get_value() // 2.2) % 3
                    if cur == idx:
                        m.set_color(GREEN)
                    else:
                        m.set_color(SECOND)
                return _upd
            lbl.add_updater(make_hl(idx, lbl))
        for i, lbl in enumerate(bw_ddr_lbls):
            idx = i

            def make_hl2(idx, lbl):
                def _upd(m):
                    cur = int(t.get_value() // 2.2) % 3
                    if cur == idx:
                        m.set_color(GREEN)
                    else:
                        m.set_color(SECOND)
                return _upd
            lbl.add_updater(make_hl2(idx, lbl))

        # latency bars subtly identical (flat) with a tiny shared breathe
        for bar in lat_bars:
            bx = bar.get_center()[0]

            def make_lat_bar(bar, bx):
                def _upd(m):
                    pulse = 1.0 + 0.02 * np.sin(2.5 * t.get_value())
                    h = 0.9 * pulse
                    m.set(width=0.7, height=h)
                    m.move_to(np.array([bx, -1.9 + h / 2, 0]))
                return _upd
            bar.add_updater(make_lat_bar(bar, bx))

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
