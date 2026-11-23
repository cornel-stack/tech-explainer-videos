"""Scene: the commit DAG + tamper-evidence cascade.

Class `Dag` (~18s). A horizontal chain of 5 COMMIT boxes (AMBER), each with
an arrow pointing to its PARENT (leftward), hashes under each. A pulse
travels the chain. Then: editing one old commit flips its hash and visibly
cascades/relights every downstream hash.
Caption: "change one commit -> every later hash changes".

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
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowArrow,
    Flash,
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


class Dag(Scene):
    def construct(self):
        title = Text("The commit chain", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- build 5 commit boxes left -> right -----------------------------
        n = 5
        orig_hashes = ["1a2b3c", "4d5e6f", "7a8b9c", "0d1e2f", "3a4b5c"]
        tamper_hashes = ["1a2b3c", "4d5e6f", "ff01aa", "9c3d77", "b8e204"]
        xs = np.linspace(-5.0, 5.0, n)
        y = 0.4
        boxes = []
        hash_mobs = []
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
            idx = Text("C" + str(i + 1), font=MONO, color=SECOND).scale(0.2)
            idx.move_to(ctr + DOWN * 0.18)
            hsh = Text(orig_hashes[i], font=MONO, color=INK).scale(0.26)
            hsh.move_to(ctr + DOWN * 0.78)
            boxes.append(VGroup(box, k, idx))
            hash_mobs.append(hsh)
            self.play(FadeIn(boxes[i]), FadeIn(hsh), run_time=0.35)

        # --- parent arrows (each points LEFT to its parent) -----------------
        arrows = []
        for i in range(1, n):
            a = Arrow(box_centers[i] + LEFT * 0.75,
                      box_centers[i - 1] + RIGHT * 0.75,
                      color=SILVER, stroke_width=2.5, buff=0.05,
                      max_tip_length_to_length_ratio=0.18)
            arrows.append(a)
            self.play(GrowArrow(a), run_time=0.3)

        par_lbl = Text("each -> its parent", font=MONO, color=SECOND).scale(0.24)
        par_lbl.move_to([0, -1.6, 0])
        self.play(FadeIn(par_lbl), run_time=0.4)

        # --- the tamper event: edit C3, cascade C3..C5 ----------------------
        tamper_idx = 2
        tamper_mark = Text("edit C3  ->  hash flips", font=MONO,
                           color=CORAL).scale(0.26)
        tamper_mark.move_to([0, -2.3, 0])
        self.play(Flash(boxes[tamper_idx][0], color=CORAL, flash_radius=1.0),
                  FadeIn(tamper_mark), run_time=0.8)

        # flip hashes C3..C5 to the tampered values, cascading
        for i in range(tamper_idx, n):
            new_h = Text(tamper_hashes[i], font=MONO, color=CORAL).scale(0.26)
            new_h.move_to(hash_mobs[i].get_center())
            self.play(FadeIn(new_h),
                      Flash(boxes[i][0], color=CORAL, flash_radius=0.8),
                      run_time=0.4)
            self.remove(hash_mobs[i])
            hash_mobs[i] = new_h

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # a bright pulse travels the chain (moving dot along commit centers)
        pulse = Dot(box_centers[0] + UP * 0.0, color=GOLD, radius=0.09)

        def pulse_upd(m):
            # sweep position 0..n-1 back and forth
            s = 0.5 + 0.5 * np.sin(0.9 * t.get_value())
            pos = s * (n - 1)
            lo = int(np.floor(pos))
            hi = min(lo + 1, n - 1)
            frac = pos - lo
            p = box_centers[lo] * (1 - frac) + box_centers[hi] * frac
            m.move_to(p)
            glow = 0.5 + 0.5 * np.sin(5.0 * t.get_value())
            m.set_opacity(0.6 + 0.4 * glow)
        pulse.add_updater(pulse_upd)
        self.add(pulse)

        # downstream (tampered) hashes RELIGHT coral<->gold to show cascade
        for i in range(n):
            tampered = i >= tamper_idx

            def make_hash(mob, is_tampered, phase):
                if is_tampered:
                    base = ManimColor(CORAL)
                    hot = ManimColor(GOLD)
                else:
                    base = ManimColor(INK)
                    hot = ManimColor(AMBER)

                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + phase)
                    m.set_color(interpolate_color(base, hot, 0.5 * s))
                    if is_tampered:
                        m.set_opacity(0.7 + 0.3 * s)
                return _upd
            # cascade phase: later commits light slightly after earlier ones
            hash_mobs[i].add_updater(make_hash(hash_mobs[i], tampered, i * 0.8))

        # tampered boxes throb coral
        for i in range(n):
            if i >= tamper_idx:
                def make_box(b, phase):
                    base = ManimColor(AMBER)
                    hot = ManimColor(CORAL)

                    def _upd(m):
                        s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + phase)
                        m.set_stroke(color=interpolate_color(base, hot, 0.6 * s),
                                     opacity=0.6 + 0.4 * s)
                    return _upd
                boxes[i][0].add_updater(make_box(boxes[i][0], i * 0.8))
            else:
                def make_ok(b, phase):
                    def _upd(m):
                        s = 0.5 + 0.5 * np.sin(1.8 * t.get_value() + phase)
                        m.set_stroke(opacity=0.6 + 0.4 * s)
                    return _upd
                boxes[i][0].add_updater(make_ok(boxes[i][0], i * 0.8))

        # tamper marker pulses
        def tm_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.4 * t.get_value())))
        tamper_mark.add_updater(tm_upd)

        # caption
        cap = Text("change one commit -> every later hash changes",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.22)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(17.0), run_time=17.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
