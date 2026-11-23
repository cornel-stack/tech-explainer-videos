"""Scene: a COMMIT object points to a tree + a parent.

Class `Commit` (~18s). An AMBER commit object box lists: tree -> (hash),
parent -> (hash), author/date/message. Arrows: commit -> its tree (TEAL);
commit -> parent commit (AMBER). The commit gets its own hash.
Caption: "a commit points to a tree + a parent".

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


class Commit(Scene):
    def construct(self):
        title = Text("A commit object", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the COMMIT object (center) -------------------------------------
        commit_c = np.array([-0.4, -0.1, 0.0])
        c_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=2.6,
                                 stroke_color=AMBER, stroke_width=3,
                                 fill_color=AMBER, fill_opacity=0.06)
        c_box.move_to(commit_c)

        c_kind = Text("commit", font=MONO, color=AMBER).scale(0.3)
        c_kind.move_to(commit_c + UP * 1.05 + LEFT * 1.0)
        c_hash = Text("3b9a1e", font=MONO, color=INK).scale(0.32)
        c_hash.move_to(commit_c + UP * 1.05 + RIGHT * 0.75)

        lines_data = [
            ("tree", "9fb2a0", TEAL),
            ("parent", "2c7d40", AMBER),
            ("author", "Cornel", SECOND),
            ("date", "2026-11-24", SECOND),
            ("message", "add parser", INK),
        ]
        row_mobs = []
        top_y = commit_c[1] + 0.55
        for i, (k, v, col) in enumerate(lines_data):
            ry = top_y - i * 0.42
            kt = Text(k, font=MONO, color=SECOND).scale(0.24)
            kt.move_to([commit_c[0] - 1.25, ry, 0])
            vt = Text(v, font=MONO, color=col).scale(0.24)
            vt.move_to([commit_c[0] + 0.5, ry, 0])
            row_mobs.append((k, kt, vt, col))

        self.play(Create(c_box), FadeIn(c_kind), FadeIn(c_hash), run_time=0.8)
        for i, (k, kt, vt, col) in enumerate(row_mobs):
            self.play(FadeIn(kt), FadeIn(vt), run_time=0.3)

        # --- the TREE it points to (right) ----------------------------------
        tree_c = np.array([4.3, 1.3, 0.0])
        tree_box = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.1,
                                    stroke_color=TEAL, stroke_width=2.5,
                                    fill_color=TEAL, fill_opacity=0.08)
        tree_box.move_to(tree_c)
        tk = Text("tree", font=MONO, color=TEAL).scale(0.26)
        tk.move_to(tree_c + UP * 0.25)
        th = Text("9fb2a0", font=MONO, color=INK).scale(0.28)
        th.move_to(tree_c + DOWN * 0.18)
        tree_grp = VGroup(tree_box, tk, th)

        tree_vt = row_mobs[0][2]
        arr_tree = Arrow(tree_vt.get_right(), tree_box.get_left(), color=TEAL,
                         stroke_width=3, buff=0.15,
                         max_tip_length_to_length_ratio=0.14)
        self.play(GrowArrow(arr_tree), FadeIn(tree_grp), run_time=0.7)

        # --- the PARENT commit (left) ---------------------------------------
        par_c = np.array([-4.5, -1.3, 0.0])
        par_box = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.1,
                                   stroke_color=AMBER, stroke_width=2.5,
                                   fill_color=AMBER, fill_opacity=0.06)
        par_box.move_to(par_c)
        pk = Text("commit", font=MONO, color=AMBER).scale(0.24)
        pk.move_to(par_c + UP * 0.25)
        ph = Text("2c7d40", font=MONO, color=INK).scale(0.28)
        ph.move_to(par_c + DOWN * 0.18)
        par_grp = VGroup(par_box, pk, ph)

        par_vt = row_mobs[1][2]
        arr_par = Arrow(par_vt.get_left() + LEFT * 0.05,
                        par_box.get_corner(UP + RIGHT) + DOWN * 0.2,
                        color=AMBER, stroke_width=3, buff=0.15,
                        max_tip_length_to_length_ratio=0.14)
        par_lbl = Text("previous commit", font=MONO, color=SECOND).scale(0.22)
        par_lbl.next_to(par_box, DOWN, buff=0.12)
        self.play(GrowArrow(arr_par), FadeIn(par_grp), FadeIn(par_lbl),
                  run_time=0.7)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # commit box glows amber
        def cbox_upd(m):
            s = 0.5 + 0.5 * np.sin(1.6 * t.get_value())
            m.set_stroke(opacity=0.6 + 0.4 * s)
            m.set_fill(opacity=0.04 + 0.06 * s)
        c_box.add_updater(cbox_upd)

        # commit hash shimmers gold
        def chash_upd(m):
            base = ManimColor(INK)
            hot = ManimColor(GOLD)
            s = 0.5 + 0.5 * np.sin(1.9 * t.get_value())
            m.set_color(interpolate_color(base, hot, 0.4 * s))
        c_hash.add_updater(chash_upd)

        # tree arrow + tree pulse teal
        def atree_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value())
            m.set_stroke(opacity=0.5 + 0.5 * s)
        arr_tree.add_updater(atree_upd)

        def treebox_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value())
            m.set_stroke(opacity=0.6 + 0.4 * s)
            m.set_fill(opacity=0.05 + 0.06 * s)
        tree_box.add_updater(treebox_upd)

        # parent arrow + parent pulse amber (offset phase)
        def apar_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + 1.5)
            m.set_stroke(opacity=0.5 + 0.5 * s)
        arr_par.add_updater(apar_upd)

        def parbox_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + 1.5)
            m.set_stroke(opacity=0.6 + 0.4 * s)
            m.set_fill(opacity=0.04 + 0.05 * s)
        par_box.add_updater(parbox_upd)

        # the tree & parent value rows highlight to show they are the links
        tree_vt_m = row_mobs[0][2]
        par_vt_m = row_mobs[1][2]

        def tvt_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.0 * t.get_value())))
        tree_vt_m.add_updater(tvt_upd)

        def pvt_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.0 * t.get_value() + 1.5)))
        par_vt_m.add_updater(pvt_upd)

        # caption
        cap = Text("a commit points to a tree + a parent",
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
