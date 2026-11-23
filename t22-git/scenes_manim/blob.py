"""Scene: content -> hash -> blob. The content-addressable idea.

Class `Blob` (~18s). A file's text box flows through a "hash()" gate and out
pops a mono hash label naming a VIOLET "blob" box. Two identical files
produce the SAME hash (dedup). A changed byte produces a TOTALLY different
hash. Caption: "content-addressable: the hash IS the name".

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


def blob_box(hash_str, center, color=VIOLET):
    box = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.9,
                           stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.08)
    box.move_to(center)
    kind = Text("blob", font=MONO, color=color).scale(0.26)
    kind.move_to(center + UP * 0.22)
    hsh = Text(hash_str, font=MONO, color=INK).scale(0.3)
    hsh.move_to(center + DOWN * 0.18)
    return VGroup(box, kind, hsh), box, hsh


class Blob(Scene):
    def construct(self):
        title = Text("From content to a blob", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the hash() gate (center) ---------------------------------------
        gate = RoundedRectangle(corner_radius=0.12, width=1.5, height=1.4,
                                stroke_color=TEAL, stroke_width=3,
                                fill_color=TEAL, fill_opacity=0.06)
        gate.move_to([0, 1.1, 0])
        gate_lbl = Text("hash()", font=MONO, color=TEAL).scale(0.36)
        gate_lbl.move_to(gate.get_center())
        self.play(Create(gate), FadeIn(gate_lbl), run_time=0.6)

        # --- file A (content) -> gate -> blob -------------------------------
        fileA = RoundedRectangle(corner_radius=0.08, width=1.8, height=1.1,
                                 stroke_color=INK, stroke_width=2,
                                 fill_color="#121319", fill_opacity=0.95)
        fileA.move_to([-4.6, 1.1, 0])
        ta1 = Text("hello", font=MONO, color=SECOND).scale(0.26)
        ta2 = Text("world", font=MONO, color=SECOND).scale(0.26)
        ta1.move_to(fileA.get_center() + UP * 0.2)
        ta2.move_to(fileA.get_center() + DOWN * 0.2)
        fileA_lbl = Text("a.txt", font=MONO, color=INK).scale(0.24)
        fileA_lbl.next_to(fileA, UP, buff=0.12)
        self.play(FadeIn(fileA), FadeIn(ta1), FadeIn(ta2), FadeIn(fileA_lbl),
                  run_time=0.6)

        arrA_in = Arrow(fileA.get_right(), gate.get_left(), color=SILVER,
                        stroke_width=3, buff=0.15, max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arrA_in), run_time=0.5)

        grpA, boxA, hshA = blob_box("a1b3f9", np.array([4.3, 1.1, 0.0]))
        arrA_out = Arrow(gate.get_right(), boxA.get_left(), color=SILVER,
                         stroke_width=3, buff=0.15, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(arrA_out), run_time=0.4)
        self.play(FadeIn(grpA), run_time=0.5)
        name_lbl = Text("the hash names it", font=MONO,
                        color=VIOLET).scale(0.24)
        name_lbl.next_to(grpA[0], UP, buff=0.12)
        self.play(FadeIn(name_lbl), run_time=0.4)

        # --- file B identical content -> SAME hash (dedup) ------------------
        fileB = RoundedRectangle(corner_radius=0.08, width=1.8, height=1.1,
                                 stroke_color=INK, stroke_width=2,
                                 fill_color="#121319", fill_opacity=0.95)
        fileB.move_to([-4.6, -1.3, 0])
        tb1 = Text("hello", font=MONO, color=SECOND).scale(0.26)
        tb2 = Text("world", font=MONO, color=SECOND).scale(0.26)
        tb1.move_to(fileB.get_center() + UP * 0.2)
        tb2.move_to(fileB.get_center() + DOWN * 0.2)
        fileB_lbl = Text("b.txt (same bytes)", font=MONO, color=INK).scale(0.22)
        fileB_lbl.next_to(fileB, DOWN, buff=0.12)
        self.play(FadeIn(fileB), FadeIn(tb1), FadeIn(tb2), FadeIn(fileB_lbl),
                  run_time=0.6)

        arrB = Arrow(fileB.get_right(), boxA.get_corner(DOWN + LEFT) + RIGHT * 0.1,
                     color=GREEN, stroke_width=3, buff=0.2,
                     max_tip_length_to_length_ratio=0.1)
        dedup = Text("same bytes -> same hash (dedup)", font=MONO,
                     color=GREEN).scale(0.24)
        dedup.move_to([0.2, -1.9, 0])
        self.play(GrowArrow(arrB), FadeIn(dedup), run_time=0.7)

        # --- a changed byte -> totally different hash -----------------------
        changed = Text("change 1 byte:", font=MONO, color=CORAL).scale(0.24)
        changed.move_to([-4.6, -2.5, 0])
        grpC, boxC, hshC = blob_box("7e02cd", np.array([4.3, -1.3, 0.0]),
                                    color=VIOLET)
        diff_lbl = Text("hello  W0rld", font=MONO, color=CORAL).scale(0.24)
        diff_lbl.move_to([1.0, -2.5, 0])
        totally = Text("totally different hash", font=MONO,
                       color=CORAL).scale(0.24)
        totally.next_to(grpC[0], DOWN, buff=0.15)
        self.play(FadeIn(changed), FadeIn(diff_lbl), run_time=0.5)
        self.play(FadeIn(grpC), FadeIn(totally), run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # content flows through the gate: ta/tb drift right subtly
        for txt, phase in [(ta1, 0.0), (ta2, 0.7), (tb1, 1.4), (tb2, 2.1)]:
            base_c = txt.get_center()

            def make_drift(mob, home, ph):
                def _upd(m):
                    dx = 0.04 * np.sin(2.4 * t.get_value() + ph)
                    m.move_to(home + np.array([dx, 0, 0]))
                return _upd
            txt.add_updater(make_drift(txt, base_c, phase))

        # the gate glows teal -> gold as it "hashes"
        def gate_upd(m):
            base = ManimColor(TEAL)
            hot = ManimColor(GOLD)
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value())
            m.set_stroke(color=interpolate_color(base, hot, 0.5 * s))
            m.set_fill(opacity=0.04 + 0.08 * s)
        gate.add_updater(gate_upd)

        # the two identical-hash blobs pulse in sync (green link alive)
        def sameA_upd(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            m.set_stroke(opacity=0.6 + 0.4 * s)
        boxA.add_updater(sameA_upd)

        def dedup_arr_upd(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            m.set_stroke(opacity=0.5 + 0.5 * s)
        arrB.add_updater(dedup_arr_upd)

        # the changed blob throbs coral-tinted violet (danger / different)
        def diffC_upd(m):
            base = ManimColor(VIOLET)
            hot = ManimColor(CORAL)
            s = 0.5 + 0.5 * np.sin(2.6 * t.get_value())
            m.set_stroke(color=interpolate_color(base, hot, 0.5 * s),
                         opacity=0.6 + 0.4 * s)
        boxC.add_updater(diffC_upd)

        def totally_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.6 * t.get_value())))
        totally.add_updater(totally_upd)

        # caption
        cap = Text("content-addressable: the hash IS the name",
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
