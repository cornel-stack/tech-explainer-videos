"""Scene: the trade-offs — strengths vs costs, balanced on a scale.

Class `Tradeoffs` (~18s). A two-column scorecard. LEFT green header STRENGTHS
with tick rows (scales to 1000s of machines, self-healing, portable — no
lock-in). RIGHT coral header COSTS with cross rows (genuinely complex, needs a
team, control-plane overhead when idle). Between them a simple balance/scale —
a beam on a pivot — gently tilts back and forth via sin(t). Bottom caption
cycles emphasis. Rows fade in staggered, then the continuous tilt + pulsing
check/cross phase runs.

Dark palette only, TEXT labels only, continuous motion. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Line,
    Dot,
    RegularPolygon,
    Text,
    VGroup,
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


class Tradeoffs(Scene):
    def construct(self):
        title = Text("The trade-offs — when it's worth it",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- headers ----------------------------------------------------------
        s_head = Text("STRENGTHS", font=MONO, color=GREEN,
                      weight="BOLD").scale(0.4)
        s_head.move_to(UP * 1.9 + LEFT * 4.0)
        c_head = Text("COSTS", font=MONO, color=CORAL,
                      weight="BOLD").scale(0.4)
        c_head.move_to(UP * 1.9 + RIGHT * 4.0)
        self.play(FadeIn(s_head), FadeIn(c_head), run_time=0.5)

        # --- strength rows (ticks) -------------------------------------------
        strengths = ["scales to 1000s of machines",
                     "self-healing",
                     "portable — no lock-in"]
        s_rows = VGroup()
        s_marks = []
        for s in strengths:
            mark = Text("✓", font=MONO, color=GREEN, weight="BOLD").scale(0.32)
            txt = Text(s, font=MONO, color=INK).scale(0.26)
            row = VGroup(mark, txt).arrange(RIGHT, buff=0.2)
            s_rows.add(row)
            s_marks.append(mark)
        s_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        s_rows.move_to(UP * 0.4 + LEFT * 4.0)
        for r in s_rows:
            r.align_to(s_head, LEFT)

        # --- cost rows (crosses) ---------------------------------------------
        costs = ["genuinely complex",
                 "needs a team",
                 "control-plane overhead when idle"]
        c_rows = VGroup()
        c_marks = []
        for c in costs:
            mark = Text("✕", font=MONO, color=CORAL, weight="BOLD").scale(0.32)
            txt = Text(c, font=MONO, color=INK).scale(0.26)
            row = VGroup(mark, txt).arrange(RIGHT, buff=0.2)
            c_rows.add(row)
            c_marks.append(mark)
        c_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        c_rows.move_to(UP * 0.4 + RIGHT * 3.4)
        for r in c_rows:
            r.align_to(c_head, LEFT)

        # staggered fade-in
        self.play(*[FadeIn(r, shift=RIGHT * 0.2) for r in s_rows],
                  lag_ratio=0.3, run_time=1.0)
        self.play(*[FadeIn(r, shift=LEFT * 0.2) for r in c_rows],
                  lag_ratio=0.3, run_time=1.0)

        # --- balance scale in the centre -------------------------------------
        pivot = np.array([0.0, -1.6, 0])
        post = Line(pivot + DOWN * 0.6, pivot, stroke_color=SILVER,
                    stroke_width=4)
        base = Line(pivot + DOWN * 0.6 + LEFT * 0.5,
                    pivot + DOWN * 0.6 + RIGHT * 0.5,
                    stroke_color=SILVER, stroke_width=4)
        fulcrum = RegularPolygon(n=3, start_angle=np.pi / 2,
                                 stroke_color=SILVER, stroke_width=3,
                                 fill_color=SILVER, fill_opacity=0.3)
        fulcrum.scale(0.18).move_to(pivot + DOWN * 0.05)
        beam = Line(pivot + LEFT * 2.0, pivot + RIGHT * 2.0,
                    stroke_color=GOLD, stroke_width=5)
        pan_l = Dot(point=pivot + LEFT * 2.0, color=GREEN, radius=0.14)
        pan_r = Dot(point=pivot + RIGHT * 2.0, color=CORAL, radius=0.14)
        self.play(Create(post), Create(base), FadeIn(fulcrum),
                  Create(beam), FadeIn(pan_l), FadeIn(pan_r), run_time=0.7)

        # --- caption ----------------------------------------------------------
        cap = Text("big, variable workload -> worth it",
                   font=HEAD, color=GREEN).scale(0.34)
        cap.to_edge(DOWN, buff=0.4)
        cap._key = ""
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        def beam_angle(tt):
            return 0.18 * np.sin(tt * 1.1)  # radians, gentle

        def rot_point(base_pt, ang):
            dx = base_pt[0] - pivot[0]
            dy = base_pt[1] - pivot[1]
            rx = dx * np.cos(ang) - dy * np.sin(ang)
            ry = dx * np.sin(ang) + dy * np.cos(ang)
            return pivot + np.array([rx, ry, 0])

        left_base = pivot + LEFT * 2.0
        right_base = pivot + RIGHT * 2.0

        def beam_upd(m):
            ang = beam_angle(t.get_value())
            lp = rot_point(left_base, ang)
            rp = rot_point(right_base, ang)
            m.put_start_and_end_on(lp, rp)
        beam.add_updater(beam_upd)

        def pan_l_upd(m):
            ang = beam_angle(t.get_value())
            m.move_to(rot_point(left_base, ang))
        pan_l.add_updater(pan_l_upd)

        def pan_r_upd(m):
            ang = beam_angle(t.get_value())
            m.move_to(rot_point(right_base, ang))
        pan_r.add_updater(pan_r_upd)

        # pulsing ticks and crosses
        def make_mark_upd(phase):
            def _upd(m):
                p = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + phase)
                m.set_opacity(0.55 + 0.45 * p)
            return _upd

        for i, mk in enumerate(s_marks):
            mk.add_updater(make_mark_upd(i * 0.9))
        for i, mk in enumerate(c_marks):
            mk.add_updater(make_mark_upd(3.0 + i * 0.9))

        # headers glow slightly with the tilt direction
        def s_head_upd(m):
            ang = beam_angle(t.get_value())
            m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 * np.sign(ang) * abs(ang) / 0.18))
        s_head.add_updater(s_head_upd)

        def c_head_upd(m):
            ang = beam_angle(t.get_value())
            m.set_opacity(0.7 + 0.3 * (0.5 - 0.5 * np.sign(ang) * abs(ang) / 0.18))
        c_head.add_updater(c_head_upd)

        # caption cycles emphasis between the two verdicts
        def cap_upd(m):
            phase = int(t.get_value() // 3.0) % 2
            key = "worth" if phase == 0 else "overkill"
            if key != m._key:
                m._key = key
                if phase == 0:
                    new = Text("big, variable workload -> worth it",
                               font=HEAD, color=GREEN).scale(0.34)
                else:
                    new = Text("simple site -> overkill",
                               font=HEAD, color=CORAL).scale(0.34)
                new.to_edge(DOWN, buff=0.4)
                m.become(new)
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 3.0)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
