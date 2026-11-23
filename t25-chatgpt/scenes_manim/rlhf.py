"""Scene: RLHF — humans rank answers, a reward model, tune to score high.

Class `Rlhf` (~19s). The VIOLET model emits 2-4 candidate answers (A/B/C/D),
a human picks the best (a GREEN check on one), those comparisons train an
AMBER "REWARD MODEL", and an arrow loops back: "tune to maximise reward".
Shows the preference → reward → policy loop. Caption: "humans rank answers
→ a reward model → tune to score high".

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
    CurvedArrow,
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


class Rlhf(Scene):
    def construct(self):
        title = Text("RLHF — learning from human preference", font=HEAD,
                     color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the VIOLET model (policy) on the left --------------------------
        model_c = np.array([-4.4, 0.6, 0.0])
        box = RoundedRectangle(corner_radius=0.2, width=2.3, height=1.5,
                               stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.08)
        box.move_to(model_c)
        m_lbl = Text("MODEL", font=MONO, color=VIOLET,
                     weight="BOLD").scale(0.36)
        m_lbl.move_to(model_c + UP * 0.2)
        m_sub = Text("policy", font=MONO, color=SECOND).scale(0.28)
        m_sub.move_to(model_c + DOWN * 0.3)
        self.play(Create(box), FadeIn(m_lbl), FadeIn(m_sub), run_time=0.8)

        # --- candidate answers A/B/C/D --------------------------------------
        cand = []
        cand_group = VGroup()
        labels = ["A", "B", "C", "D"]
        best = 2  # which candidate the human picks
        for i, lab in enumerate(labels):
            y = 1.9 - i * 1.0
            c = RoundedRectangle(corner_radius=0.1, width=1.9, height=0.7,
                                 stroke_color=SECOND, stroke_width=2,
                                 fill_color=SECOND, fill_opacity=0.05)
            c.move_to([-1.6, y, 0])
            txt = Text(lab, font=MONO, color=INK, weight="BOLD").scale(0.36)
            txt.move_to([-2.2, y, 0])
            bar = Line([-1.95, y, 0], [-0.75, y, 0], stroke_color=SECOND,
                       stroke_width=2.5, stroke_opacity=0.6)
            g = VGroup(c, txt, bar)
            cand_group.add(g)
            cand.append((c, g, y, lab))
        # arrows from model to candidates
        em_arrows = VGroup()
        for _, g, y, _ in cand:
            a = Arrow(box.get_right() + RIGHT * 0.02, g.get_left() + LEFT * 0.02,
                      color=VIOLET, stroke_width=2, buff=0.1,
                      max_tip_length_to_length_ratio=0.12, stroke_opacity=0.6)
            em_arrows.add(a)
        self.play(*[FadeIn(g) for _, g, _, _ in cand],
                  *[Create(a) for a in em_arrows], run_time=1.0)

        emit_lbl = Text("emits candidates", font=MONO, color=VIOLET).scale(0.28)
        emit_lbl.move_to([-1.6, 2.6, 0])
        self.play(FadeIn(emit_lbl), run_time=0.4)

        # --- human picks the best (green check) -----------------------------
        bc, bg, by, _ = cand[best]
        check = VGroup(
            Line([0.1, by - 0.03, 0], [0.28, by - 0.2, 0], stroke_color=GREEN,
                 stroke_width=4),
            Line([0.28, by - 0.2, 0], [0.62, by + 0.24, 0], stroke_color=GREEN,
                 stroke_width=4),
        )
        human_lbl = Text("human picks best", font=MONO, color=GREEN).scale(0.28)
        human_lbl.move_to([0.6, by - 0.6, 0])
        self.play(bc.animate.set_stroke(GREEN).set_fill(GREEN, opacity=0.12),
                  Create(check), FadeIn(human_lbl), run_time=0.8)

        # --- AMBER reward model ---------------------------------------------
        rm_c = np.array([3.6, 0.6, 0.0])
        rm = RoundedRectangle(corner_radius=0.2, width=2.6, height=1.5,
                              stroke_color=AMBER, stroke_width=3,
                              fill_color=AMBER, fill_opacity=0.08)
        rm.move_to(rm_c)
        rm_lbl = Text("REWARD MODEL", font=MONO, color=AMBER,
                      weight="BOLD").scale(0.32)
        rm_lbl.move_to(rm_c + UP * 0.2)
        rm_sub = Text("scores answers", font=MONO, color=SECOND).scale(0.26)
        rm_sub.move_to(rm_c + DOWN * 0.3)
        pref_arrow = Arrow([1.3, by + 0.3, 0], rm.get_left() + LEFT * 0.02,
                           color=GREEN, stroke_width=3, buff=0.1,
                           max_tip_length_to_length_ratio=0.1)
        self.play(Create(rm), FadeIn(rm_lbl), FadeIn(rm_sub),
                  Create(pref_arrow), run_time=0.9)
        comp_lbl = Text("comparisons train it", font=MONO, color=GREEN).scale(0.26)
        comp_lbl.move_to([2.3, 1.7, 0])
        self.play(FadeIn(comp_lbl), run_time=0.4)

        # --- loop back: tune to maximise reward -----------------------------
        loop = CurvedArrow(rm.get_bottom() + DOWN * 0.1,
                           box.get_bottom() + DOWN * 0.1, color=AMBER,
                           stroke_width=3, angle=-1.0)
        loop_lbl = Text("tune to maximise reward", font=MONO, color=AMBER,
                        weight="BOLD").scale(0.3)
        loop_lbl.move_to([-0.4, -2.3, 0])
        self.play(Create(loop), FadeIn(loop_lbl), run_time=0.9)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        v_base = ManimColor(VIOLET)
        v_hi = ManimColor(INK)

        def box_upd(m):
            s = 0.5 + 0.5 * np.sin(2.3 * t.get_value())
            m.set_stroke(color=interpolate_color(v_base, v_hi, 0.2 * s))
            m.set_fill(VIOLET, opacity=0.06 + 0.08 * s)
        box.add_updater(box_upd)

        a_base = ManimColor(AMBER)
        a_hi = ManimColor(INK)

        def rm_upd(m):
            s = 0.5 + 0.5 * np.sin(2.3 * t.get_value() + 1.5)
            m.set_stroke(color=interpolate_color(a_base, a_hi, 0.25 * s))
            m.set_fill(AMBER, opacity=0.06 + 0.1 * s)
        rm.add_updater(rm_upd)

        # loop arrow pulses to show the cycle
        def loop_upd(m):
            s = 0.5 + 0.5 * np.sin(2.6 * t.get_value())
            m.set_stroke(opacity=0.4 + 0.6 * s)
        loop.add_updater(loop_upd)

        def ll_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.6 * t.get_value())))
        loop_lbl.add_updater(ll_upd)

        # candidate bars shimmer; the picked one glows green steadily
        for i, (c, g, y, lab) in enumerate(cand):
            def make_cand_upd(idx):
                is_best = (idx == best)

                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + idx)
                    if is_best:
                        m.set_stroke(opacity=0.7 + 0.3 * s)
                        m.set_fill(GREEN, opacity=0.08 + 0.1 * s)
                    else:
                        m.set_stroke(opacity=0.3 + 0.3 * s)
                return _upd
            c.add_updater(make_cand_upd(i))

        # a reward token travels the loop back to the model
        token = RoundedRectangle(corner_radius=0.06, width=0.34, height=0.24,
                                 stroke_color=AMBER, stroke_width=1.5,
                                 fill_color=AMBER, fill_opacity=0.3)
        self.add(token)
        loop_start = rm.get_bottom() + DOWN * 0.1
        loop_end = box.get_bottom() + DOWN * 0.1
        mid = np.array([(loop_start[0] + loop_end[0]) / 2,
                        loop_start[1] - 1.1, 0.0])

        def token_upd(m):
            tt = (t.get_value() * 0.4) % 1.0
            # quadratic bezier through mid
            p = ((1 - tt) ** 2 * loop_start + 2 * (1 - tt) * tt * mid
                 + tt ** 2 * loop_end)
            m.move_to(p)
            m.set_opacity(0.3 + 0.6 * np.sin(np.pi * tt))
        token.add_updater(token_upd)

        # caption
        cap = Text("humans rank answers → a reward model → tune to score high",
                   font=HEAD, color=SECOND).scale(0.34)
        cap.to_edge(DOWN, buff=0.25)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
