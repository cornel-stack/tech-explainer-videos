"""Scene: Interference — full bars, still slow (the crowded 2.4 GHz band).

Class `Interference` (~20s). A horizontal channel axis (channels 1..11) with
overlapping bell-shaped humps (networks) colliding in coral. Around it, noisy
sources blast the band: a microwave box, a Bluetooth dot, neighbour routers
#1/#2/#3 each emitting bursts that clash. Collisions flash coral.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Line,
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


class Interference(Scene):
    def construct(self):
        title = Text("Full bars, still slow",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- channel axis (1..11) -------------------------------------------
        axis_left = -5.6
        axis_right = 5.6
        axis_y = -1.8
        axis_w = axis_right - axis_left
        axis = Line([axis_left, axis_y, 0], [axis_right, axis_y, 0],
                    stroke_color=SECOND, stroke_width=1.5)

        ticks = VGroup()
        ch_labels = VGroup()
        for ch in range(1, 12):
            x = axis_left + (ch - 1) / 10.0 * axis_w
            tk = Line([x, axis_y - 0.08, 0], [x, axis_y + 0.08, 0],
                      stroke_color=SECOND, stroke_width=1.2)
            ticks.add(tk)
            lb = Text(str(ch), font=MONO, color=SECOND).scale(0.22)
            lb.move_to([x, axis_y - 0.28, 0])
            ch_labels.add(lb)
        axis_lbl = Text("2.4 GHz channels", font=MONO, color=SILVER).scale(0.26)
        axis_lbl.move_to([0, axis_y - 0.7, 0])

        self.play(Create(axis), *[Create(t) for t in ticks],
                  run_time=0.6)
        self.play(*[FadeIn(l) for l in ch_labels], FadeIn(axis_lbl),
                  run_time=0.4)

        def ch_x(ch):
            return axis_left + (ch - 1) / 10.0 * axis_w

        # --- overlapping network humps (bell curves) ------------------------
        # (centre channel, colour, width)
        nets = [
            (1, TEAL, 1.3),
            (6, VIOLET, 1.3),
            (11, GREEN, 1.3),
            (4, AMBER, 1.3),
            (9, GOLD, 1.3),
        ]

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        humps = VGroup()
        for ci, (ctr, col, wid) in enumerate(nets):
            h = VMobject(stroke_color=col, stroke_width=2.4)
            humps.add(h)

            def make_hump(center_ch, colour, width, phase):
                cx = ch_x(center_ch)
                sigma = (width / 10.0 * axis_w)

                def _upd(m):
                    pts = []
                    steps = 80
                    breathe = 0.85 + 0.15 * np.sin(t.get_value() * 2.0 + phase)
                    amp = 1.5 * breathe
                    span = 2.2
                    for s in range(steps + 1):
                        x = cx - span + (2 * span) * (s / steps)
                        y = axis_y + amp * np.exp(-((x - cx) ** 2)
                                                  / (2 * (sigma * 0.5) ** 2))
                        pts.append([x, y, 0])
                    m.set_points_as_corners(pts)
                    m.set_stroke(opacity=0.7)
                return _upd
            h.add_updater(make_hump(ctr, col, wid, ci * 1.1))
        self.add(humps)

        # collision flashes where humps overlap (between 1&4, 4&6, 6&9, 9&11)
        overlap_chs = [2.5, 5.0, 7.5, 10.0]
        flashes = VGroup()
        for oi, oc in enumerate(overlap_chs):
            f = Dot([ch_x(oc), axis_y + 0.9, 0], radius=0.14, color=CORAL)
            flashes.add(f)

            def make_flash(phase):
                def _upd(m):
                    s = np.sin(t.get_value() * 3.5 + phase)
                    on = s > 0.4
                    m.set_opacity(0.9 if on else 0.08)
                    m.scale_to_fit_width(0.3 if on else 0.14)
                    m.set_color(CORAL)
                return _upd
            f.add_updater(make_flash(oi * 1.3))
        self.add(flashes)

        # --- noisy sources around the band ----------------------------------
        # each: (label, colour, position, burst_phase)
        sources = [
            ("microwave", CORAL, np.array([-5.2, 2.2, 0.0]), 0.0),
            ("Bluetooth", TEAL, np.array([-1.8, 2.6, 0.0]), 1.1),
            ("neighbour #1", AMBER, np.array([1.8, 2.6, 0.0]), 2.0),
            ("neighbour #2", VIOLET, np.array([4.2, 2.2, 0.0]), 0.7),
            ("neighbour #3", GOLD, np.array([5.4, 0.6, 0.0]), 1.6),
        ]

        for name, col, pos, phase in sources:
            box = RoundedRectangle(
                corner_radius=0.06, width=0.34, height=0.26,
                stroke_color=col, stroke_width=2.0,
                fill_color=BG, fill_opacity=1.0,
            ).move_to(pos)
            lbl = Text(name, font=MONO, color=col).scale(0.22)
            lbl.next_to(box, UP, buff=0.08)
            self.add(box, lbl)

            # bursts: rings radiating toward the band
            for k in range(2):
                ring = Circle(radius=0.15, stroke_color=col, stroke_width=2.0,
                              fill_opacity=0).move_to(pos)

                def make_burst(colour, origin, ph, kk):
                    def _upd(m):
                        period = 1.8
                        tt = (t.get_value() + ph + kk * 0.9) % period
                        frac = tt / period
                        m.set(width=0.3 + frac * 1.6)
                        m.move_to(origin)
                        m.set_stroke(colour,
                                     opacity=np.clip((1 - frac) * 0.7,
                                                     0.0, 0.7))
                    return _upd
                ring.add_updater(make_burst(col, pos, phase, k))
                self.add(ring)

            # box pulse
            def make_box(colour, ph):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(t.get_value() * 3.0 + ph)
                    m.set_stroke(colour, opacity=0.5 + 0.5 * s)
                return _upd
            box.add_updater(make_box(col, phase))

        cap = Text("waiting for a gap", font=MONO, color=CORAL).scale(0.32)
        cap.to_edge(DOWN, buff=0.35)

        def cap_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 2.5)
            m.set_opacity(0.6 + 0.4 * s)
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
