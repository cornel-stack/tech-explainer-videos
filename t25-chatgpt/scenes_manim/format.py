"""Scene: The chat format — roles in a transcript.

Class `Format` (~18s). A transcript with coloured role tags: a SILVER
"system:" line, a TEAL "user:" bubble, a GREEN "assistant:" bubble. A
bracket/arrow shows the model predicts the assistant turn. Caption:
"frame the chat as roles → predict the assistant's reply".

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


def bubble(role, text, role_col, x_edge, y, width=4.4):
    """Build a chat bubble VGroup: role tag + body, left-aligned."""
    tag = Text(role, font=MONO, color=role_col, weight="BOLD").scale(0.32)
    body = Text(text, font=MONO, color=INK).scale(0.3)
    inner = VGroup(tag, body).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.14,
                           width=max(width, inner.width + 0.5),
                           height=inner.height + 0.4,
                           stroke_color=role_col, stroke_width=2.2,
                           fill_color=role_col, fill_opacity=0.07)
    inner.move_to(box.get_center())
    g = VGroup(box, inner)
    g.move_to([x_edge, y, 0], aligned_edge=LEFT)
    return g, box


class Format(Scene):
    def construct(self):
        title = Text("The chat format", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        left_x = -5.4
        sys_g, sys_box = bubble("system:", "You are a helpful assistant.",
                                SILVER, left_x, 1.85, width=5.0)
        usr_g, usr_box = bubble("user:", "What is the capital of France?",
                                TEAL, left_x, 0.35, width=5.0)
        asst_g, asst_box = bubble("assistant:", "The capital of France is Paris.",
                                  GREEN, left_x, -1.25, width=5.0)

        self.play(FadeIn(sys_g, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(usr_g, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(asst_g, shift=UP * 0.15), run_time=0.6)

        # --- bracket on the assistant turn ----------------------------------
        bx = asst_box.get_right()[0] + 0.25
        top = asst_box.get_top()[1]
        bot = asst_box.get_bottom()[1]
        br = VGroup(
            Line([bx, top, 0], [bx + 0.18, top, 0], stroke_color=VIOLET,
                 stroke_width=3),
            Line([bx + 0.18, top, 0], [bx + 0.18, bot, 0], stroke_color=VIOLET,
                 stroke_width=3),
            Line([bx + 0.18, bot, 0], [bx, bot, 0], stroke_color=VIOLET,
                 stroke_width=3),
        )
        predict_lbl = Text("model predicts\nthis turn", font=MONO, color=VIOLET,
                           weight="BOLD").scale(0.3)
        predict_lbl.move_to([bx + 1.7, (top + bot) / 2, 0])
        arr = Arrow([bx + 0.95, (top + bot) / 2, 0],
                    [bx + 0.3, (top + bot) / 2, 0], color=VIOLET,
                    stroke_width=3, buff=0.05,
                    max_tip_length_to_length_ratio=0.35)
        self.play(Create(br), FadeIn(predict_lbl), Create(arr), run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        def make_box_pulse(mob, col, rate, phase):
            base = ManimColor(col)
            hi = ManimColor(INK)

            def _upd(m):
                s = 0.5 + 0.5 * np.sin(rate * t.get_value() + phase)
                m.set_stroke(color=interpolate_color(base, hi, 0.2 * s))
                m.set_fill(col, opacity=0.05 + 0.07 * s)
            return _upd
        sys_box.add_updater(make_box_pulse(sys_box, SILVER, 1.8, 0.0))
        usr_box.add_updater(make_box_pulse(usr_box, TEAL, 2.1, 1.2))
        asst_box.add_updater(make_box_pulse(asst_box, GREEN, 2.4, 2.4))

        def br_upd(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_stroke(opacity=0.5 + 0.5 * s)
        br.add_updater(br_upd)
        arr.add_updater(br_upd)

        def pl_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(3.0 * t.get_value())))
        predict_lbl.add_updater(pl_upd)

        # caption
        cap = Text("frame the chat as roles → predict the assistant's reply",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
