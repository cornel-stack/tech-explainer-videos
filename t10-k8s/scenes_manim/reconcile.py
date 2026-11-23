"""Scene: reconciliation — desired vs actual, close the gap forever.

Class `Reconcile` (~24s) — the centrepiece. Two big readouts at top: DESIRED 10
(green, fixed) and ACTUAL N (changes live). Below, a row of 10 pod hexes. A
control loop (circular arrow) spins labelled "compare -> act". Cycle driven by
t: a node under 2 pods dies (those 2 flash coral and vanish) -> ACTUAL drops to
8 and turns coral -> the loop pulses "8 < 10" -> 2 new pods spawn -> ACTUAL
climbs back to 10 and turns green. The die->heal cycle repeats forever. ACTUAL
updates via an updater reading a stepped function of t.

Dark palette only, TEXT labels only, continuous motion. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    RegularPolygon,
    Text,
    VGroup,
    Arc,
    Arrow,
    ValueTracker,
    config,
    FadeIn,
    Create,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    PI,
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


def pod_hex(scale=1.0, color=TEAL):
    hexb = RegularPolygon(n=6, start_angle=PI / 6,
                          stroke_color=color, stroke_width=2.5,
                          fill_color="#0C1A18", fill_opacity=0.9)
    hexb.scale(0.42 * scale)
    return hexb


class Reconcile(Scene):
    def construct(self):
        title = Text("Reconciliation — close the gap, forever",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- readouts ---------------------------------------------------------
        des_lbl = Text("DESIRED", font=MONO, color=GREEN).scale(0.3)
        des_num = Text("10", font=MONO, color=GREEN, weight="BOLD").scale(0.9)
        desired = VGroup(des_lbl, des_num).arrange(DOWN, buff=0.1)
        desired.move_to(UP * 1.7 + LEFT * 3.8)

        act_lbl = Text("ACTUAL", font=MONO, color=SILVER).scale(0.3)
        act_num = Text("10", font=MONO, color=GREEN, weight="BOLD").scale(0.9)
        actual = VGroup(act_lbl, act_num).arrange(DOWN, buff=0.1)
        actual.move_to(UP * 1.7 + RIGHT * 3.8)

        self.play(FadeIn(desired), FadeIn(actual), run_time=0.6)

        # --- row of 10 pod hexes ---------------------------------------------
        pods = VGroup()
        for _ in range(10):
            pods.add(pod_hex(1.0))
        pods.arrange(RIGHT, buff=0.3)
        pods.move_to(DOWN * 0.55)
        self.play(*[FadeIn(p, scale=0.6) for p in pods],
                  lag_ratio=0.05, run_time=0.9)

        # node under pods 4 and 5 (indices) that will "die"
        dying_idx = [4, 5]
        node = RoundedRectangle(
            corner_radius=0.08,
            width=pods[dying_idx[1]].get_right()[0]
            - pods[dying_idx[0]].get_left()[0] + 0.3,
            height=0.3,
            stroke_color=AMBER, stroke_width=1.6,
            fill_color="#141008", fill_opacity=0.5,
        )
        node.next_to(VGroup(pods[dying_idx[0]], pods[dying_idx[1]]),
                     DOWN, buff=0.18)
        node_lbl = Text("node", font=MONO, color=AMBER).scale(0.18)
        node_lbl.next_to(node, DOWN, buff=0.06)
        self.play(FadeIn(node), FadeIn(node_lbl), run_time=0.4)

        # --- control loop (circular arrow) -----------------------------------
        loop = Arc(radius=0.55, start_angle=PI * 0.15, angle=PI * 1.6,
                   stroke_color=VIOLET, stroke_width=4)
        loop.move_to(DOWN * 2.0)
        loop_head = Arrow(start=loop.get_end() + UP * 0.1,
                          end=loop.get_end(),
                          color=VIOLET, buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.5)
        loop_lbl = Text("compare -> act", font=MONO, color=VIOLET).scale(0.24)
        loop_lbl.next_to(loop, DOWN, buff=0.12)
        gap_lbl = Text("", font=MONO, color=CORAL, weight="BOLD").scale(0.3)
        gap_lbl.next_to(loop, RIGHT, buff=0.3)
        self.play(Create(loop), FadeIn(loop_head), FadeIn(loop_lbl),
                  run_time=0.6)
        self.add(gap_lbl)

        # --- caption ----------------------------------------------------------
        cap = Text("desired vs actual — close the gap, forever (self-healing)",
                   font=HEAD, color=GREEN).scale(0.34)
        cap.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        CYCLE = 8.0
        # timeline within a cycle:
        #   0.0-1.5 healthy (10)
        #   1.5-2.0 pods 4,5 flash coral
        #   2.0-4.0 vanished -> ACTUAL 8, loop pulses "8 < 10"
        #   4.0-5.0 two new pods grow back
        #   5.0-8.0 healthy again (10)

        def actual_count(tt):
            if tt < 2.0:
                return 10
            if tt < 4.5:
                return 8
            return 10

        # pods 4 & 5: die and respawn
        def make_dying_upd(pod_m, idx):
            def _upd(m):
                tt = t.get_value() % CYCLE
                breath = 1.0 + 0.04 * np.sin(2.4 * t.get_value() + idx)
                if tt < 1.5:
                    m.set_opacity(0.9)
                    m.set_stroke(color=TEAL, width=2.5, opacity=1.0)
                    m.scale_to_fit_height(0.84 * breath)
                elif tt < 2.0:
                    f = (tt - 1.5) / 0.5
                    m.set_stroke(color=CORAL, width=3.5,
                                 opacity=1.0 - 0.3 * f)
                    m.set_fill(color="#1A0C0A", opacity=0.9 * (1 - f))
                    m.scale_to_fit_height(0.84 * (1 - 0.4 * f))
                elif tt < 4.0:
                    m.set_opacity(0.0)
                    m.set_stroke(opacity=0.0)
                elif tt < 5.0:
                    f = (tt - 4.0) / 1.0
                    e = rate_functions.ease_out_back(f)
                    m.set_opacity(0.9 * f)
                    m.set_stroke(color=GREEN, width=3.0, opacity=f)
                    m.set_fill(color="#0C1A18", opacity=0.9 * f)
                    m.scale_to_fit_height(0.84 * max(e, 0.05))
                else:
                    m.set_opacity(0.9)
                    m.set_stroke(color=TEAL, width=2.5, opacity=1.0)
                    m.set_fill(color="#0C1A18", opacity=0.9)
                    m.scale_to_fit_height(0.84 * breath)
            return _upd

        for idx in dying_idx:
            pods[idx].add_updater(make_dying_upd(pods[idx], idx))

        # healthy pods just breathe
        for i, p in enumerate(pods):
            if i in dying_idx:
                continue

            def make_breath(pm, phase):
                def _upd(m):
                    b = 1.0 + 0.04 * np.sin(2.4 * t.get_value() + phase)
                    m.scale_to_fit_height(0.84 * b)
                return _upd
            p.add_updater(make_breath(p, i * 0.7))

        # node flashes/dies with its pods
        def node_upd(m):
            tt = t.get_value() % CYCLE
            if tt < 1.5:
                m.set_stroke(color=AMBER, opacity=0.8)
                m.set_opacity(0.5)
            elif tt < 2.0:
                m.set_stroke(color=CORAL, opacity=1.0)
            elif tt < 4.0:
                m.set_opacity(0.15)
                m.set_stroke(color=CORAL, opacity=0.4)
            elif tt < 5.0:
                f = (tt - 4.0) / 1.0
                m.set_opacity(0.15 + 0.35 * f)
                m.set_stroke(color=GREEN, opacity=0.4 + 0.4 * f)
            else:
                m.set_stroke(color=AMBER, opacity=0.8)
                m.set_opacity(0.5)
        node.body = node
        node.add_updater(node_upd)

        # ACTUAL number updates live via stepped function of t
        def act_num_upd(m):
            tt = t.get_value() % CYCLE
            n = actual_count(tt)
            col = GREEN if n == 10 else CORAL
            # rebuild only when the value/colour changes
            cur = getattr(m, "_val", None)
            if cur != (n, col):
                m._val = (n, col)
                new = Text(str(n), font=MONO, color=col,
                           weight="BOLD").scale(0.9)
                new.move_to(m)
                m.become(new)
            # subtle pulse while mismatched
            if n != 10:
                m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                              np.sin(9.0 * t.get_value())))
            else:
                m.set_opacity(1.0)
        act_num.add_updater(act_num_upd)

        # loop arrow spins continuously + gap label appears when mismatched
        def loop_upd(m):
            spin = (t.get_value() * 1.4) % (2 * PI)
            m.move_to(DOWN * 2.0)
            m.rotate(0.0)  # keep centre; rotation applied via set via become
            # rotate arc by resetting start_angle
            new = Arc(radius=0.55, start_angle=spin, angle=PI * 1.6,
                      stroke_color=VIOLET, stroke_width=4)
            new.move_to(DOWN * 2.0)
            m.become(new)
        loop.add_updater(loop_upd)

        def loop_head_upd(m):
            m.move_to(loop.get_end())
        loop_head.add_updater(loop_head_upd)

        def gap_upd(m):
            tt = t.get_value() % CYCLE
            n = actual_count(tt)
            if n != 10:
                txt = f"{n} < 10"
                if getattr(m, "_txt", None) != txt:
                    m._txt = txt
                    new = Text(txt, font=MONO, color=CORAL,
                               weight="BOLD").scale(0.32)
                    new.next_to(loop, RIGHT, buff=0.3)
                    m.become(new)
                m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                              np.sin(9.0 * t.get_value())))
            else:
                m.set_opacity(0.0)
        gap_lbl.add_updater(gap_upd)

        def cap_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 1.5)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(24.0), run_time=24.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
