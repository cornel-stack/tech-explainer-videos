"""Scene: Bands — higher frequency = speed minus reach.

Class `Bands` (~20s). Three stacked lanes: 2.4 / 5 / 6 GHz. Each lane has a
travelling wave whose wavelength matches the band (2.4 long, 6 short), a range
ring around a small router (larger for 2.4, smaller for 6), and a speed bar
(short for 2.4, long for 6). Rule: higher band = more speed, less range.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
    Circle,
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


class Bands(Scene):
    def construct(self):
        title = Text("Higher frequency = speed - reach",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # lane definitions: (name, colour, cycles, range_radius, speed_frac)
        lanes = [
            ("2.4 GHz", TEAL, 2.5, 1.35, 0.33),
            ("5 GHz", GREEN, 5.0, 0.95, 0.66),
            ("6 GHz", VIOLET, 8.0, 0.65, 1.0),
        ]

        lane_ys = [2.0, 0.1, -1.8]
        wave_left = -5.6
        wave_right = -0.2
        wave_w = wave_right - wave_left

        # speed bar track
        bar_left = 3.4
        bar_max = 2.6

        routers = []
        labels = VGroup()

        for (name, col, cyc, rad, spd), y in zip(lanes, lane_ys):
            lbl = Text(name, font=MONO, color=col).scale(0.34)
            lbl.move_to([-6.9, y, 0])
            labels.add(lbl)

            # small router box (range centre)
            r = RoundedRectangle(
                corner_radius=0.06, width=0.4, height=0.3,
                stroke_color=col, stroke_width=2.0,
                fill_color=BG, fill_opacity=1.0,
            ).move_to([wave_left - 0.0, y, 0])
            routers.append(r)

        self.play(*[FadeIn(l) for l in labels],
                  *[Create(r) for r in routers], run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        all_mobs = []

        for (name, col, cyc, rad, spd), y, router in zip(lanes, lane_ys,
                                                         routers):
            # --- travelling wave --------------------------------------------
            wave = VMobject(stroke_color=col, stroke_width=2.6)

            def make_wave(colour, cycles, cy):
                def _upd(m):
                    pts = []
                    steps = 200
                    tt = t.get_value()
                    for s in range(steps + 1):
                        frac = s / steps
                        x = wave_left + frac * wave_w
                        yy = cy + 0.45 * np.sin(
                            2.0 * np.pi * cycles * frac - tt * 3.0)
                        pts.append([x, yy, 0])
                    m.set_points_as_corners(pts)
                    m.set_stroke(opacity=0.9)
                return _upd
            wave.add_updater(make_wave(col, cyc, y))
            all_mobs.append(wave)

            # --- range ring (pulsing) ---------------------------------------
            ring = Circle(radius=rad, stroke_color=col, stroke_width=2.5,
                          fill_opacity=0).move_to(router.get_center())

            def make_ring(colour, base_r, cx, cy):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(t.get_value() * 2.2)
                    m.set(width=2.0 * base_r * (0.9 + 0.12 * s))
                    m.move_to([cx, cy, 0])
                    m.set_stroke(opacity=0.35 + 0.25 * s)
                return _upd
            ring.add_updater(make_ring(col, rad,
                                       router.get_center()[0],
                                       router.get_center()[1]))
            all_mobs.append(ring)

            # inner pulse dot travelling outward (range feel)
            pdot = Dot(router.get_center(), radius=0.05, color=col)

            def make_pdot(base_r, cx, cy):
                def _upd(m):
                    frac = (t.get_value() * 0.5) % 1.0
                    m.move_to([cx + base_r * frac, cy, 0])
                    m.set_opacity(np.clip(1.0 - frac, 0.0, 1.0))
                return _upd
            pdot.add_updater(make_pdot(rad, router.get_center()[0],
                                       router.get_center()[1]))
            all_mobs.append(pdot)

            # --- speed bar ---------------------------------------------------
            track = RoundedRectangle(
                corner_radius=0.08, width=bar_max, height=0.26,
                stroke_color=SECOND, stroke_width=1.2, fill_opacity=0,
            )
            track.move_to([bar_left + bar_max / 2.0, y, 0])
            all_mobs.append(track)

            fill = RoundedRectangle(
                corner_radius=0.08, width=0.1, height=0.2,
                stroke_width=0, fill_color=col, fill_opacity=0.85,
            )
            all_mobs.append(fill)

            def make_fill(colour, target_frac, cy):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(t.get_value() * 1.6)
                    w = max(0.08, bar_max * target_frac * (0.85 + 0.15 * s))
                    m.set(width=w)
                    m.move_to([bar_left + w / 2.0, cy, 0])
                    m.set_fill(colour, opacity=0.85)
                return _upd
            fill.add_updater(make_fill(col, spd, y))
            all_mobs.append(fill)

        for m in all_mobs:
            self.add(m)

        # column captions
        cap_range = Text("range", font=MONO, color=SILVER).scale(0.26)
        cap_range.move_to([wave_left + wave_w / 2.0, 3.1, 0])
        cap_speed = Text("speed", font=MONO, color=SILVER).scale(0.26)
        cap_speed.move_to([bar_left + bar_max / 2.0, 3.1, 0])
        cap = Text("more cycles -> faster, but dies sooner", font=MONO,
                   color=SILVER).scale(0.3)
        cap.to_edge(DOWN, buff=0.4)
        self.add(cap_range, cap_speed, cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
