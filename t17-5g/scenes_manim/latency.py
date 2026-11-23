"""Scene: Latency race, edge computing and network slicing.

Class `Latency` (~18s). Two lanes: "4G ~50 ms" (a data ball starts after a
long delay) vs "5G ~a few ms" (starts almost instantly) — 5G clearly wins.
Below: EDGE computing — a server moved CLOSE to the phone vs a far data
centre. And NETWORK SLICING — one pipe split into 3 labelled virtual lanes.
Caption: "5G's real gift is responsiveness".

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
    Rectangle,
    Text,
    VGroup,
    Line,
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


class Latency(Scene):
    def construct(self):
        title = Text("The latency race", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- two race lanes (top) -------------------------------------------
        lane_x0, lane_x1 = -5.2, 2.0
        lane_4g_y = 2.4
        lane_5g_y = 1.5

        def lane(y, name, col):
            track = Line([lane_x0, y, 0], [lane_x1, y, 0], stroke_color=SECOND,
                         stroke_width=2, stroke_opacity=0.4)
            lbl = Text(name, font=MONO, color=col).scale(0.3)
            lbl.next_to([lane_x0, y, 0], LEFT, buff=0.2)
            flag = Line([lane_x1, y - 0.2, 0], [lane_x1, y + 0.2, 0],
                        stroke_color=col, stroke_width=3)
            ball = Dot([lane_x0, y, 0], color=col, radius=0.12)
            return track, lbl, flag, ball

        t4, l4, f4, b4 = lane(lane_4g_y, "4G  ~50 ms", CORAL)
        t5, l5, f5, b5 = lane(lane_5g_y, "5G  ~a few ms", GREEN)
        self.play(Create(t4), Create(t5), FadeIn(l4), FadeIn(l5),
                  Create(f4), Create(f5), FadeIn(b4), FadeIn(b5),
                  run_time=0.9)

        # --- edge computing (middle-left) -----------------------------------
        edge_y = -0.3
        phone = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.7,
                                 stroke_color=INK, stroke_width=2,
                                 fill_color="#111318", fill_opacity=0.9)
        phone.move_to([-5.4, edge_y, 0])
        edge_srv = RoundedRectangle(corner_radius=0.06, width=0.6, height=0.8,
                                    stroke_color=GREEN, stroke_width=2,
                                    fill_color="#0D170F", fill_opacity=0.9)
        edge_srv.move_to([-4.2, edge_y, 0])
        far_srv = RoundedRectangle(corner_radius=0.06, width=0.6, height=0.8,
                                   stroke_color=SECOND, stroke_width=2,
                                   fill_color="#111318", fill_opacity=0.9)
        far_srv.move_to([-0.6, edge_y, 0])
        edge_lbl = Text("edge server (close)", font=MONO,
                        color=GREEN).scale(0.24)
        edge_lbl.next_to(edge_srv, UP, buff=0.12)
        far_lbl = Text("far data centre", font=MONO, color=SECOND).scale(0.24)
        far_lbl.next_to(far_srv, UP, buff=0.12)
        edge_link = Line(phone.get_right(), edge_srv.get_left(),
                         stroke_color=GREEN, stroke_width=2)
        far_link = Line(edge_srv.get_right(), far_srv.get_left(),
                        stroke_color=SECOND, stroke_width=1.5,
                        stroke_opacity=0.5)
        self.play(FadeIn(phone), FadeIn(edge_srv), FadeIn(far_srv),
                  FadeIn(edge_lbl), FadeIn(far_lbl),
                  Create(edge_link), Create(far_link), run_time=1.0)

        # --- network slicing (middle-right / bottom) ------------------------
        pipe_c = np.array([3.9, 0.4, 0.0])
        pipe_in = Line(pipe_c + LEFT * 1.2, pipe_c, stroke_color=SILVER,
                       stroke_width=6)
        slices = [
            ("emergency · low-latency", CORAL, 0.75),
            ("video · bulk", VIOLET, 0.0),
            ("IoT", TEAL, -0.75),
        ]
        slice_group = VGroup()
        slice_items = []
        for name, col, dy in slices:
            start = pipe_c
            end = pipe_c + np.array([2.6, dy, 0])
            ln = Line(start, end, stroke_color=col, stroke_width=4)
            lbl = Text(name, font=MONO, color=col).scale(0.24)
            lbl.next_to(end, RIGHT, buff=0.12)
            slice_group.add(VGroup(ln, lbl))
            slice_items.append((start, end, col))
        slice_title = Text("network slicing", font=MONO, color=SILVER).scale(0.26)
        slice_title.next_to(pipe_in, UP, buff=0.3).shift(RIGHT * 0.6)
        self.play(Create(pipe_in), FadeIn(slice_title),
                  *[Create(s[0]) for s in slice_group],
                  *[FadeIn(s[1]) for s in slice_group],
                  run_time=1.1)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Race loop period
        LAP = 3.0

        def ball_upd(ball, y, delay, speed):
            def _upd(m):
                tt = t.get_value() % LAP
                # 4G waits "delay"; 5G starts near-instant
                run = max(tt - delay, 0.0)
                frac = np.clip(run / speed, 0.0, 1.0)
                x = lane_x0 + (lane_x1 - lane_x0) * frac
                m.move_to([x, y, 0])
                m.set_opacity(0.3 + 0.7 * (1.0 if frac < 1.0 else 0.4))
            return _upd
        b4.add_updater(ball_upd(b4, lane_4g_y, 1.1, 1.6))
        b5.add_updater(ball_upd(b5, lane_5g_y, 0.08, 1.2))

        # edge link packets zip quickly; far link slow
        edge_pk = Dot(color=GREEN, radius=0.08)
        far_pk = Dot(color=SECOND, radius=0.07)

        def edge_pk_upd(m):
            frac = (t.get_value() * 1.5) % 1.0
            a = phone.get_right()
            b = edge_srv.get_left()
            m.move_to(a + (b - a) * frac)
        edge_pk.add_updater(edge_pk_upd)

        def far_pk_upd(m):
            frac = (t.get_value() * 0.4) % 1.0
            a = edge_srv.get_right()
            b = far_srv.get_left()
            m.move_to(a + (b - a) * frac)
        far_pk.add_updater(far_pk_upd)
        self.add(edge_pk, far_pk)

        # slicing: packets flow down each virtual lane at its own cadence
        slice_dots = VGroup()
        slice_meta = []
        cadences = [1.8, 1.1, 0.7]
        for (start, end, col), cad in zip(slice_items, cadences):
            for k in range(2):
                d = Dot(color=col, radius=0.06)
                slice_dots.add(d)
                slice_meta.append((start.copy(), end.copy(), cad, k * 0.5))
        self.add(slice_dots)

        def make_slice_dot(meta):
            start, end, cad, off = meta

            def _upd(m):
                frac = ((t.get_value() * cad) + off) % 1.0
                m.move_to(start + (end - start) * frac)
                m.set_opacity(np.clip(1.2 - frac, 0.2, 1.0))
            return _upd
        for d, meta in zip(slice_dots, slice_meta):
            d.add_updater(make_slice_dot(meta))

        # edge server pulses green
        def edge_pulse(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_stroke(width=1.8 + 1.6 * s)
        edge_srv.add_updater(edge_pulse)

        # caption
        cap = Text("5G's real gift is responsiveness", font=HEAD,
                   color=SECOND).scale(0.4)
        cap.to_edge(DOWN, buff=0.35)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
