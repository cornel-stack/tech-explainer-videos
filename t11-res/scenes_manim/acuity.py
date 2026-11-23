"""Scene: where your eyes give up.

Class `Acuity` (~22s). LEFT a simple side-view: a small triangle figure (the
viewer) at a distance from a tall screen rectangle, a VISION CONE (two lines)
from the eye to the screen edges, and a label "~1 arcminute - the eye's limit".
A horizontal DISTANCE axis under the figure carries a marker that slides
(driven by t) between "close" and "sofa (2.5 m)".

RIGHT two small screens side by side labelled "4K" and "8K", each filled with a
dot grid (8K twice as dense). As the distance marker moves toward "sofa", the
8K grid's dots shrink below a drawn "acuity line" and fade to grey (labelled
"below what your eye can resolve"), while the 4K grid stays just at the limit.

A caption lands: "at 2.5 m from a 65-inch TV, the limit is ~4K - 8K is
invisible."

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Line,
    Triangle,
    Dot,
    Text,
    VGroup,
    ValueTracker,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
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


class Acuity(Scene):
    def construct(self):
        title = Text("Where your eyes give up", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # =====================================================================
        # LEFT: side-view — viewer, screen, vision cone, distance axis
        # =====================================================================
        # Screen edges (a tall rectangle seen edge-on, drawn as a bar).
        screen = Rectangle(width=0.22, height=3.2,
                           stroke_color=SILVER, stroke_width=2.5,
                           fill_color=SILVER, fill_opacity=0.08)
        screen.shift(LEFT * 1.6 + DOWN * 0.3)
        screen_top = screen.get_top()
        screen_bot = screen.get_bottom()
        screen_lbl = Text("screen", font=MONO, color=SILVER).scale(0.24)
        screen_lbl.next_to(screen, UP, buff=0.12)

        # Viewer: a small triangle (eye) pointing toward the screen.
        viewer = Triangle(stroke_color=TEAL, stroke_width=2.5,
                          fill_color=TEAL, fill_opacity=0.35).scale(0.22)
        viewer.rotate(-90 * np.pi / 180.0)  # point toward +x (the screen)
        viewer_lbl = Text("you", font=MONO, color=TEAL).scale(0.22)

        # Distance travel range along x for the viewer.
        near_x = screen.get_right()[0] + 1.1   # "close"
        far_x = screen.get_right()[0] + 4.9    # "sofa (2.5 m)"
        eye_y = screen.get_center()[1]

        # Distance axis under the figure.
        axis = Line([near_x, -3.0, 0], [far_x, -3.0, 0],
                    stroke_color=SECOND, stroke_width=2)
        tick_near = Line([near_x, -2.9, 0], [near_x, -3.1, 0],
                         stroke_color=SECOND, stroke_width=2)
        tick_far = Line([far_x, -2.9, 0], [far_x, -3.1, 0],
                        stroke_color=SECOND, stroke_width=2)
        lbl_near = Text("close", font=MONO, color=SECOND).scale(0.22)
        lbl_near.next_to(tick_near, DOWN, buff=0.1)
        lbl_far = Text("sofa (2.5 m)", font=MONO, color=SECOND).scale(0.22)
        lbl_far.next_to(tick_far, DOWN, buff=0.1)
        marker = Dot(color=AMBER, radius=0.09)
        marker.move_to([near_x, -3.0, 0])

        # Vision cone lines (eye -> screen top/bottom), filled later by updater.
        cone_top = Line([near_x, eye_y, 0], screen_top,
                        stroke_color=TEAL, stroke_width=1.6,
                        stroke_opacity=0.6)
        cone_bot = Line([near_x, eye_y, 0], screen_bot,
                        stroke_color=TEAL, stroke_width=1.6,
                        stroke_opacity=0.6)

        acuity_lbl = Text("~1 arcminute - the eye's limit",
                          font=MONO, color=TEAL).scale(0.24)
        acuity_lbl.next_to(screen, DOWN, buff=0.1).shift(RIGHT * 1.9)

        self.play(Create(screen), FadeIn(screen_lbl), run_time=0.6)
        self.play(Create(axis), Create(tick_near), Create(tick_far),
                  FadeIn(lbl_near), FadeIn(lbl_far), run_time=0.6)
        viewer.move_to([near_x, eye_y, 0])
        viewer_lbl.next_to(viewer, UP, buff=0.1)
        self.play(GrowFromCenter(viewer), FadeIn(viewer_lbl),
                  GrowFromCenter(marker), run_time=0.5)
        self.play(Create(cone_top), Create(cone_bot),
                  FadeIn(acuity_lbl), run_time=0.6)

        # =====================================================================
        # RIGHT: two small screens, 4K and 8K grids (8K twice as dense)
        # =====================================================================
        panel_w, panel_h = 2.5, 1.8
        panel_4k = Rectangle(width=panel_w, height=panel_h,
                             stroke_color=CORAL, stroke_width=2.2,
                             fill_color="#17100E", fill_opacity=0.5)
        panel_8k = Rectangle(width=panel_w, height=panel_h,
                             stroke_color=GOLD, stroke_width=2.2,
                             fill_color="#151206", fill_opacity=0.5)
        panel_4k.shift(RIGHT * 4.0 + UP * 1.0)
        panel_8k.shift(RIGHT * 4.0 + DOWN * 1.35)

        lbl_4k = Text("4K", font=MONO, color=CORAL, weight="BOLD").scale(0.3)
        lbl_8k = Text("8K", font=MONO, color=GOLD, weight="BOLD").scale(0.3)
        lbl_4k.next_to(panel_4k, UP, buff=0.1).align_to(panel_4k, LEFT)
        lbl_8k.next_to(panel_8k, DOWN, buff=0.1).align_to(panel_8k, LEFT)

        self.play(Create(panel_4k), Create(panel_8k),
                  FadeIn(lbl_4k), FadeIn(lbl_8k), run_time=0.7)

        def make_grid(panel, rows, cols, color, r):
            g = VGroup()
            for _ in range(rows * cols):
                g.add(Dot(color=color, radius=r))
            g.arrange_in_grid(rows=rows, cols=cols, buff=0.08)
            g.scale_to_fit_width(panel_w - 0.3)
            if g.height > panel_h - 0.3:
                g.scale_to_fit_height(panel_h - 0.3)
            g.move_to(panel.get_center())
            return g

        grid_4k = make_grid(panel_4k, 6, 9, CORAL, 0.05)
        grid_8k = make_grid(panel_8k, 12, 18, GOLD, 0.035)

        self.play(*[GrowFromCenter(d) for d in grid_4k],
                  *[GrowFromCenter(d) for d in grid_8k],
                  lag_ratio=0.004, run_time=1.0)

        # Acuity threshold line drawn across the 8K panel.
        acuity_line = Line(panel_8k.get_left() + RIGHT * 0.1,
                           panel_8k.get_right() + LEFT * 0.1,
                           stroke_color=TEAL, stroke_width=1.6,
                           stroke_opacity=0.0)
        acuity_line.move_to(panel_8k.get_center())
        acuity_note = Text("below what your eye can resolve",
                           font=HEAD, color=SECOND).scale(0.24)
        acuity_note.next_to(panel_8k, RIGHT, buff=0.2)
        acuity_note.scale_to_fit_width(
            min(acuity_note.width, 2.6))
        self.add(acuity_line, acuity_note)

        # --- caption ---------------------------------------------------------
        cap = Text("at 2.5 m from a 65-inch TV, the limit is ~4K "
                   "- 8K is invisible", font=HEAD, color=INK).scale(0.32)
        cap.to_edge(DOWN, buff=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        LOOP = 8.0  # seconds for one close<->sofa round trip

        def distance_frac(tt):
            # 0 = close, 1 = sofa. Smooth back-and-forth.
            phase = (tt % LOOP) / LOOP
            tri = 1.0 - abs(2.0 * phase - 1.0)  # 0..1..0
            return 0.5 - 0.5 * np.cos(np.pi * tri)  # ease

        # Capture geometry locals for updaters.
        s_top = np.array(screen_top)
        s_bot = np.array(screen_bot)
        base_r8 = grid_8k[0].radius
        base_r4 = grid_4k[0].radius
        line_pos = acuity_line.get_center()
        note_pos = acuity_note.get_center()

        # Viewer + marker slide along the distance axis.
        def viewer_upd(m):
            f = distance_frac(t.get_value())
            x = near_x + (far_x - near_x) * f
            m.move_to([x, eye_y, 0])
        viewer.add_updater(viewer_upd)

        def viewer_lbl_upd(m):
            m.next_to(viewer, UP, buff=0.1)
        viewer_lbl.add_updater(viewer_lbl_upd)

        def marker_upd(m):
            f = distance_frac(t.get_value())
            x = near_x + (far_x - near_x) * f
            m.move_to([x, -3.0, 0])
        marker.add_updater(marker_upd)

        # Vision cone follows the eye and pulses.
        def cone_top_upd(m):
            f = distance_frac(t.get_value())
            x = near_x + (far_x - near_x) * f
            m.put_start_and_end_on(np.array([x, eye_y, 0]), s_top)
            pulse = 0.4 + 0.3 * (0.5 + 0.5 * np.sin(t.get_value() * 3.0))
            m.set_stroke(opacity=pulse)
        cone_top.add_updater(cone_top_upd)

        def cone_bot_upd(m):
            f = distance_frac(t.get_value())
            x = near_x + (far_x - near_x) * f
            m.put_start_and_end_on(np.array([x, eye_y, 0]), s_bot)
            pulse = 0.4 + 0.3 * (0.5 + 0.5 * np.sin(t.get_value() * 3.0))
            m.set_stroke(opacity=pulse)
        cone_bot.add_updater(cone_bot_upd)

        # 8K dots: as distance -> sofa, shrink below acuity line and fade grey.
        for d in grid_8k:
            def make_8k(dot, br):
                def _upd(m):
                    f = distance_frac(t.get_value())
                    # Past ~0.5 distance, 8K detail drops below acuity.
                    fade = np.clip((f - 0.35) / 0.4, 0.0, 1.0)
                    dot.scale_to_fit_width(2.0 * br * (1.0 - 0.6 * fade))
                    # Blend gold -> grey, and drop opacity.
                    grey = np.array([0.55, 0.56, 0.58])
                    gold = np.array([0.91, 0.76, 0.29])
                    rgb = gold * (1.0 - fade) + grey * fade
                    dot.set_color(
                        "#%02X%02X%02X" % tuple(int(c * 255) for c in rgb))
                    dot.set_opacity(0.95 - 0.55 * fade)
                return _upd
            d.add_updater(make_8k(d, br=base_r8))

        # 4K dots: stay just at the limit — gentle, steady.
        for d in grid_4k:
            def make_4k(dot, br, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(t.get_value() * 1.6 + phase)
                    dot.set_opacity(0.8 + 0.18 * s)
                return _upd
            d.add_updater(make_4k(d, base_r4, (id(d) % 17) * 0.3))

        # Acuity line appears across the 8K panel when past the threshold.
        def line_upd(m):
            f = distance_frac(t.get_value())
            vis = np.clip((f - 0.35) / 0.4, 0.0, 1.0)
            m.set_stroke(opacity=0.2 + 0.5 * vis)
        acuity_line.add_updater(line_upd)

        def note_upd(m):
            f = distance_frac(t.get_value())
            vis = np.clip((f - 0.4) / 0.35, 0.0, 1.0)
            m.set_opacity(0.2 + 0.7 * vis)
        acuity_note.add_updater(note_upd)

        # Caption fades in strongly as we settle at the sofa.
        cap.set_opacity(0.0)
        self.add(cap)

        def cap_upd(m):
            f = distance_frac(t.get_value())
            m.set_opacity(np.clip((f - 0.45) / 0.3, 0.0, 1.0) * 0.95 + 0.05)
        cap.add_updater(cap_upd)

        # Acuity label breathes.
        def acuity_lbl_upd(m):
            m.set_opacity(0.6 + 0.35 * (0.5 + 0.5 *
                                        np.sin(t.get_value() * 1.3)))
        acuity_lbl.add_updater(acuity_lbl_upd)

        self.play(t.animate.set_value(22.0), run_time=22.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
