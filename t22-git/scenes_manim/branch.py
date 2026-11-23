"""Scene: a branch is just a pointer to a commit.

Class `Branch` (~18s). The same commit chain, now with small GREEN pointer
tags ("main", "feature") sitting ON commits, and a "HEAD -> main" pointer.
A new commit appears and the "main" pointer SLIDES forward onto it.
Emphasise "41 bytes". Caption: "a branch is just a pointer to a commit".

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
    Arrow,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowArrow,
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


def branch_tag(name, color=GREEN):
    box = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.4,
                           stroke_color=color, stroke_width=2.2,
                           fill_color=color, fill_opacity=0.12)
    lbl = Text(name, font=MONO, color=color).scale(0.24)
    lbl.move_to(box.get_center())
    return VGroup(box, lbl)


class Branch(Scene):
    def construct(self):
        title = Text("A branch is a pointer", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- commit chain (4 commits, room for a 5th) -----------------------
        n = 4
        hashes = ["1a2b3c", "4d5e6f", "7a8b9c", "0d1e2f"]
        xs = np.array([-5.0, -2.9, -0.8, 1.3])
        y = -0.2
        boxes = []
        box_centers = []
        for i in range(n):
            ctr = np.array([xs[i], y, 0.0])
            box_centers.append(ctr)
            box = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.95,
                                   stroke_color=AMBER, stroke_width=2.5,
                                   fill_color=AMBER, fill_opacity=0.06)
            box.move_to(ctr)
            k = Text("commit", font=MONO, color=AMBER).scale(0.22)
            k.move_to(ctr + UP * 0.22)
            hsh = Text(hashes[i], font=MONO, color=INK).scale(0.24)
            hsh.move_to(ctr + DOWN * 0.18)
            boxes.append(VGroup(box, k, hsh))
            self.play(FadeIn(boxes[i]), run_time=0.3)

        arrows = []
        for i in range(1, n):
            a = Arrow(box_centers[i] + LEFT * 0.75,
                      box_centers[i - 1] + RIGHT * 0.75,
                      color=SILVER, stroke_width=2.5, buff=0.05,
                      max_tip_length_to_length_ratio=0.18)
            arrows.append(a)
            self.play(GrowArrow(a), run_time=0.25)

        # --- GREEN branch pointer tags sitting ON commits -------------------
        main_tag = branch_tag("main", GREEN)
        main_tag.next_to(boxes[n - 1][0], UP, buff=0.5)
        main_arr = Arrow(main_tag.get_bottom(), boxes[n - 1][0].get_top(),
                         color=GREEN, stroke_width=3, buff=0.08,
                         max_tip_length_to_length_ratio=0.3)

        feat_tag = branch_tag("feature", GREEN)
        feat_tag.next_to(boxes[1][0], DOWN, buff=0.5)
        feat_arr = Arrow(feat_tag.get_top(), boxes[1][0].get_bottom(),
                         color=GREEN, stroke_width=3, buff=0.08,
                         max_tip_length_to_length_ratio=0.3)

        self.play(FadeIn(main_tag), GrowArrow(main_arr), run_time=0.5)
        self.play(FadeIn(feat_tag), GrowArrow(feat_arr), run_time=0.5)

        # --- HEAD -> main pointer -------------------------------------------
        head_tag = branch_tag("HEAD", SILVER)
        head_tag.next_to(main_tag, UP, buff=0.45)
        head_arr = Arrow(head_tag.get_bottom(), main_tag.get_top(),
                         color=SILVER, stroke_width=2.5, buff=0.06,
                         max_tip_length_to_length_ratio=0.3)
        head_lbl = Text("HEAD -> main", font=MONO, color=SILVER).scale(0.22)
        head_lbl.next_to(head_tag, RIGHT, buff=0.2)
        self.play(FadeIn(head_tag), GrowArrow(head_arr), FadeIn(head_lbl),
                  run_time=0.5)

        # --- "41 bytes" emphasis --------------------------------------------
        bytes_lbl = Text("just 41 bytes: a hash + newline", font=MONO,
                         color=GREEN).scale(0.28)
        bytes_lbl.move_to([0, -2.4, 0])
        self.play(FadeIn(bytes_lbl), run_time=0.5)

        # --- a NEW commit appears; main slides forward ----------------------
        new_ctr = np.array([3.4, y, 0.0])
        new_box = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.95,
                                   stroke_color=AMBER, stroke_width=2.5,
                                   fill_color=AMBER, fill_opacity=0.06)
        new_box.move_to(new_ctr)
        nk = Text("commit", font=MONO, color=AMBER).scale(0.22)
        nk.move_to(new_ctr + UP * 0.22)
        nh = Text("5e6f7a", font=MONO, color=INK).scale(0.24)
        nh.move_to(new_ctr + DOWN * 0.18)
        new_commit = VGroup(new_box, nk, nh)
        new_arr = Arrow(new_ctr + LEFT * 0.75, box_centers[n - 1] + RIGHT * 0.75,
                        color=SILVER, stroke_width=2.5, buff=0.05,
                        max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(new_commit), GrowArrow(new_arr), run_time=0.6)

        # main tag + its arrow slide forward onto the new commit
        main_tag_target = main_tag.copy().next_to(new_box, UP, buff=0.5)
        new_main_arr = Arrow(main_tag_target.get_bottom(), new_box.get_top(),
                             color=GREEN, stroke_width=3, buff=0.08,
                             max_tip_length_to_length_ratio=0.3)
        head_tag_target = head_tag.copy().next_to(main_tag_target, UP, buff=0.45)
        new_head_arr = Arrow(head_tag_target.get_bottom(),
                             main_tag_target.get_top(), color=SILVER,
                             stroke_width=2.5, buff=0.06,
                             max_tip_length_to_length_ratio=0.3)

        self.play(
            main_tag.animate.move_to(main_tag_target.get_center()),
            main_arr.animate.become(new_main_arr),
            head_tag.animate.move_to(head_tag_target.get_center()),
            head_lbl.animate.next_to(head_tag_target, RIGHT, buff=0.2),
            head_arr.animate.become(new_head_arr),
            run_time=1.1,
        )
        box_centers.append(new_ctr)
        boxes.append(new_commit)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # branch tags gently bob (pointers feel light / cheap)
        main_home = main_tag.get_center()
        feat_home = feat_tag.get_center()
        head_home = head_tag.get_center()

        def make_bob(mob, home, phase, amp=0.05):
            def _upd(m):
                dy = amp * np.sin(1.4 * t.get_value() + phase)
                m.move_to(home + np.array([0, dy, 0]))
            return _upd
        main_tag.add_updater(make_bob(main_tag, main_home, 0.0))
        feat_tag.add_updater(make_bob(feat_tag, feat_home, 1.0))
        head_tag.add_updater(make_bob(head_tag, head_home, 2.0, amp=0.04))

        # the green tags glow
        for tag, phase in [(main_tag, 0.0), (feat_tag, 1.3)]:
            def make_glow(tg, ph):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(1.9 * t.get_value() + ph)
                    m[0].set_stroke(opacity=0.6 + 0.4 * s)
                    m[0].set_fill(opacity=0.08 + 0.1 * s)
                return _upd
            tag.add_updater(make_glow(tag, phase))

        # commit boxes keep a soft amber pulse
        for i, bx in enumerate(boxes):
            def make_cpulse(group, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(1.6 * t.get_value() + phase)
                    m[0].set_stroke(opacity=0.55 + 0.4 * s)
                return _upd
            bx.add_updater(make_cpulse(bx, i * 0.7))

        # 41 bytes label pulses green
        def bytes_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.1 * t.get_value())))
        bytes_lbl.add_updater(bytes_upd)

        # caption
        cap = Text("a branch is just a pointer to a commit",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.22)

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
