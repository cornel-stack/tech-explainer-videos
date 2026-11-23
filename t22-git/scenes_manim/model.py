"""Scene: the big picture — Git stores snapshots, not diffs.

Class `Model` (~18s). Three snapshot frames of a small file set appear one
after another, stacking into a glowing "SNAPSHOT" tower. To the left, a
crossed-out "diff / delta" idea dims out as the snapshot stack glows.
Caption: "Git stores snapshots, not diffs — as objects in .git".

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
    Text,
    VGroup,
    Line,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
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


def file_card(name, color, scale=1.0):
    box = RoundedRectangle(corner_radius=0.06, width=1.1 * scale,
                           height=0.28 * scale, stroke_color=color,
                           stroke_width=2, fill_color="#121319",
                           fill_opacity=0.9)
    lbl = Text(name, font=MONO, color=color).scale(0.22 * scale)
    lbl.move_to(box.get_center())
    return VGroup(box, lbl)


def snapshot_frame(center, color, scale=1.0):
    """A small folder snapshot: a frame holding three file cards."""
    frame = RoundedRectangle(corner_radius=0.1, width=1.5 * scale,
                             height=1.35 * scale, stroke_color=color,
                             stroke_width=2.5, fill_color=color,
                             fill_opacity=0.04)
    frame.move_to(center)
    names = ["app.py", "utils.py", "README"]
    cards = VGroup()
    for i, nm in enumerate(names):
        c = file_card(nm, INK, scale=scale * 0.95)
        c.move_to(center + np.array([0, (0.34 - i * 0.34) * scale, 0]))
        cards.add(c)
    return VGroup(frame, cards), frame


class Model(Scene):
    def construct(self):
        title = Text("How Git stores your project", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- LEFT: the crossed-out "diff / delta" idea ----------------------
        diff_c = np.array([-4.3, 0.2, 0.0])
        diff_box = RoundedRectangle(corner_radius=0.1, width=2.4, height=1.8,
                                    stroke_color=SECOND, stroke_width=2,
                                    fill_color=SECOND, fill_opacity=0.03)
        diff_box.move_to(diff_c)
        diff_title = Text("diff / delta", font=MONO, color=SECOND).scale(0.32)
        diff_title.move_to(diff_c + UP * 0.6)
        diff_rows = VGroup()
        for i, (sgn, col) in enumerate([("- old line", CORAL),
                                        ("+ new line", GREEN),
                                        ("- gone", CORAL)]):
            r = Text(sgn, font=MONO, color=col).scale(0.24)
            r.move_to(diff_c + np.array([0, 0.1 - i * 0.33, 0]))
            diff_rows.add(r)
        self.play(Create(diff_box), FadeIn(diff_title), FadeIn(diff_rows),
                  run_time=0.8)

        # red cross over the diff idea
        cross1 = Line(diff_box.get_corner(UP + LEFT),
                      diff_box.get_corner(DOWN + RIGHT),
                      stroke_color=CORAL, stroke_width=5)
        cross2 = Line(diff_box.get_corner(UP + RIGHT),
                      diff_box.get_corner(DOWN + LEFT),
                      stroke_color=CORAL, stroke_width=5)
        not_this = Text("not how Git thinks", font=MONO, color=CORAL).scale(0.26)
        not_this.next_to(diff_box, DOWN, buff=0.2)
        self.play(Create(cross1), Create(cross2), FadeIn(not_this),
                  run_time=0.7)

        # --- RIGHT: three snapshot frames stacking into a tower -------------
        stack_centers = [
            np.array([2.0, -1.0, 0.0]),
            np.array([2.4, -0.1, 0.0]),
            np.array([2.8, 0.8, 0.0]),
        ]
        frames = []
        frame_boxes = []
        colors = [VIOLET, TEAL, AMBER]
        for i, (ctr, col) in enumerate(zip(stack_centers, colors)):
            grp, fr = snapshot_frame(ctr, col, scale=1.0)
            frames.append(grp)
            frame_boxes.append(fr)
            self.play(GrowFromCenter(grp), run_time=0.6)

        stack_lbl = Text("SNAPSHOT stack", font=MONO, color=GOLD).scale(0.34)
        stack_lbl.move_to([3.1, 1.9, 0])
        each_lbl = Text("each = full picture", font=MONO,
                        color=SECOND).scale(0.26)
        each_lbl.move_to([4.6, -1.5, 0])
        self.play(FadeIn(stack_lbl), FadeIn(each_lbl), run_time=0.6)

        git_dir = Text("stored as objects in  .git", font=MONO,
                       color=SILVER).scale(0.3)
        git_dir.move_to([-0.2, -2.3, 0])
        self.play(FadeIn(git_dir), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # snapshot frames glow in sequence (the "stack" feels alive)
        for i, fr in enumerate(frame_boxes):
            def make_frame(frm, col, phase):
                base = ManimColor(col)
                hot = ManimColor(GOLD)

                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(1.6 * t.get_value() + phase)
                    m.set_stroke(color=interpolate_color(base, hot, 0.4 * s),
                                 opacity=0.6 + 0.4 * s)
                    m.set_fill(opacity=0.03 + 0.06 * s)
                return _upd
            fr.add_updater(make_frame(fr, colors[i], i * 1.1))

        # the whole snapshot group gently floats up/down
        for i, grp in enumerate(frames):
            def make_float(g, phase, ctr):
                def _upd(m):
                    dy = 0.05 * np.sin(1.0 * t.get_value() + phase)
                    m.move_to(ctr + np.array([0, dy, 0]))
                return _upd
            grp.add_updater(make_float(grp, i * 0.8, stack_centers[i]))

        # stack label pulses gold
        def stack_upd(m):
            s = 0.5 + 0.5 * np.sin(1.8 * t.get_value())
            m.set_opacity(0.6 + 0.4 * s)
        stack_lbl.add_updater(stack_upd)

        # diff idea keeps dimming (fades toward dead grey)
        def diff_grp_upd(group):
            def _upd(m):
                s = 0.5 + 0.5 * np.sin(0.9 * t.get_value())
                m.set_opacity(0.25 + 0.12 * s)
            return _upd
        diff_fade = VGroup(diff_box, diff_title, diff_rows)
        diff_fade.add_updater(diff_grp_upd(diff_fade))

        def cross_upd(m):
            s = 0.5 + 0.5 * np.sin(0.9 * t.get_value())
            m.set_stroke(opacity=0.5 + 0.3 * s)
        cross1.add_updater(cross_upd)
        cross2.add_updater(cross_upd)

        # caption
        cap = Text("Git stores snapshots, not diffs — as objects in .git",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

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
