"""Scene: a TREE object = a folder mapping names -> hashes.

Class `Tree` (~18s). A TEAL tree object shown as a table of rows
(filename -> blob hash), including a nested sub-tree row. Arrows from tree
rows to their VIOLET blob boxes. The tree itself gets its own hash at the
top. Caption: "a tree = a folder: names -> hashes".

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


def small_blob(hash_str, center, color=VIOLET):
    box = RoundedRectangle(corner_radius=0.07, width=1.35, height=0.72,
                           stroke_color=color, stroke_width=2.2,
                           fill_color=color, fill_opacity=0.08)
    box.move_to(center)
    kind = Text("blob", font=MONO, color=color).scale(0.2)
    kind.move_to(center + UP * 0.17)
    hsh = Text(hash_str, font=MONO, color=INK).scale(0.24)
    hsh.move_to(center + DOWN * 0.13)
    return VGroup(box, kind, hsh), box


class Tree(Scene):
    def construct(self):
        title = Text("A tree object", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the TREE table (left) ------------------------------------------
        tree_c = np.array([-3.6, -0.1, 0.0])
        rows_data = [
            ("app.py", "a1b3f9", VIOLET, "blob"),
            ("README", "7e02cd", VIOLET, "blob"),
            ("src/", "c4d8e1", TEAL, "tree"),
        ]
        row_h = 0.62
        table_w = 3.4
        n = len(rows_data)
        table_h = row_h * n + 0.5

        tree_box = RoundedRectangle(corner_radius=0.1, width=table_w,
                                    height=table_h, stroke_color=TEAL,
                                    stroke_width=3, fill_color=TEAL,
                                    fill_opacity=0.05)
        tree_box.move_to(tree_c)

        tree_kind = Text("tree", font=MONO, color=TEAL).scale(0.28)
        tree_kind.move_to(tree_c + UP * (table_h / 2 - 0.3) + LEFT * 1.1)
        tree_hash = Text("9fb2a0", font=MONO, color=INK).scale(0.3)
        tree_hash.move_to(tree_c + UP * (table_h / 2 - 0.3) + RIGHT * 0.7)
        tree_hash_tag = Text("tree hash:", font=MONO, color=SECOND).scale(0.22)
        tree_hash_tag.next_to(tree_hash, LEFT, buff=0.1)

        self.play(Create(tree_box), FadeIn(tree_kind), run_time=0.7)
        self.play(FadeIn(tree_hash_tag), FadeIn(tree_hash), run_time=0.5)

        row_mobs = []
        top_y = tree_c[1] + table_h / 2 - 0.75
        for i, (name, h, col, kind) in enumerate(rows_data):
            ry = top_y - i * row_h
            name_t = Text(name, font=MONO, color=INK).scale(0.26)
            name_t.move_to([tree_c[0] - 0.8, ry, 0])
            hash_t = Text(h, font=MONO, color=col).scale(0.26)
            hash_t.move_to([tree_c[0] + 0.85, ry, 0])
            sep = Line([tree_c[0] - table_w / 2 + 0.1, ry - row_h / 2 + 0.05, 0],
                       [tree_c[0] + table_w / 2 - 0.1, ry - row_h / 2 + 0.05, 0],
                       stroke_color=SECOND, stroke_width=1, stroke_opacity=0.3)
            row_mobs.append((name_t, hash_t, np.array([tree_c[0] + 0.85, ry, 0]),
                             col, kind))
            self.play(FadeIn(name_t), FadeIn(hash_t),
                      Create(sep) if i < n else FadeIn(sep), run_time=0.4)

        # --- the VIOLET blobs + nested sub-tree (right) ---------------------
        targets = [
            np.array([3.4, 1.5, 0.0]),
            np.array([3.4, 0.0, 0.0]),
            np.array([3.4, -1.5, 0.0]),
        ]
        blob_boxes = []
        arrows = []
        for i, (name_t, hash_t, src, col, kind) in enumerate(row_mobs):
            tgt = targets[i]
            if kind == "blob":
                grp, box = small_blob(rows_data[i][1], tgt, color=VIOLET)
            else:
                # nested sub-tree: render as a mini tree object (teal)
                box = RoundedRectangle(corner_radius=0.08, width=1.6,
                                       height=0.95, stroke_color=TEAL,
                                       stroke_width=2.2, fill_color=TEAL,
                                       fill_opacity=0.07).move_to(tgt)
                k = Text("tree", font=MONO, color=TEAL).scale(0.2)
                k.move_to(tgt + UP * 0.3)
                hh = Text(rows_data[i][1], font=MONO, color=INK).scale(0.24)
                hh.move_to(tgt + UP * 0.02)
                sub = Text("main.py -> ...", font=MONO, color=SECOND).scale(0.18)
                sub.move_to(tgt + DOWN * 0.25)
                grp = VGroup(box, k, hh, sub)
            blob_boxes.append((box, col, kind))
            arr = Arrow(src + RIGHT * 0.45, box.get_left(), color=SILVER,
                        stroke_width=2.5, buff=0.12,
                        max_tip_length_to_length_ratio=0.12)
            arrows.append(arr)
            self.play(GrowArrow(arr), FadeIn(grp), run_time=0.5)

        folder_lbl = Text("names -> hashes", font=MONO, color=TEAL).scale(0.26)
        folder_lbl.next_to(tree_box, DOWN, buff=0.2)
        self.play(FadeIn(folder_lbl), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # tree box glows teal
        def tree_upd(m):
            s = 0.5 + 0.5 * np.sin(1.6 * t.get_value())
            m.set_stroke(opacity=0.6 + 0.4 * s)
            m.set_fill(opacity=0.03 + 0.05 * s)
        tree_box.add_updater(tree_upd)

        # tree hash pulses gold-teal
        def thash_upd(m):
            base = ManimColor(INK)
            hot = ManimColor(GOLD)
            s = 0.5 + 0.5 * np.sin(1.8 * t.get_value())
            m.set_color(interpolate_color(base, hot, 0.4 * s))
        tree_hash.add_updater(thash_upd)

        # each arrow + its target pulse in sequence (data flowing down rows)
        for i, (arr, (box, col, kind)) in enumerate(zip(arrows, blob_boxes)):
            def make_arr(a, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + phase)
                    m.set_stroke(opacity=0.4 + 0.5 * s)
                return _upd
            arr.add_updater(make_arr(arr, i * 1.0))

            def make_box(b, c, phase):
                base = ManimColor(c)

                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + phase)
                    m.set_stroke(opacity=0.6 + 0.4 * s)
                    m.set_fill(opacity=0.05 + 0.06 * s)
                return _upd
            box.add_updater(make_box(box, col, i * 1.0))

        # the row hashes shimmer
        for i, (name_t, hash_t, src, col, kind) in enumerate(row_mobs):
            def make_row(h, phase):
                def _upd(m):
                    m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 *
                                  np.sin(2.2 * t.get_value() + phase)))
                return _upd
            hash_t.add_updater(make_row(hash_t, i * 0.9))

        # caption
        cap = Text("a tree = a folder: names -> hashes",
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
