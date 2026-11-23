"""Scene: The raw base model is just a next-word predictor.

Class `Base` (~18s). A big VIOLET "BASE MODEL" box labelled "next-word
predictor". A question is fed in — "What is the capital of France?" — and
instead of answering, the model rambles, continuing the text with MORE
questions (text streaming out chaotically). Caption: "a raw model just
continues text — it's not an assistant".

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


class Base(Scene):
    def construct(self):
        title = Text("The raw base model", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the VIOLET base model box --------------------------------------
        model_c = np.array([-3.6, 0.1, 0.0])
        box = RoundedRectangle(corner_radius=0.22, width=3.0, height=2.3,
                               stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.08)
        box.move_to(model_c)
        m_lbl = Text("BASE MODEL", font=MONO, color=VIOLET,
                     weight="BOLD").scale(0.42)
        m_lbl.move_to(model_c + UP * 0.35)
        m_sub = Text("next-word predictor", font=MONO, color=SECOND).scale(0.3)
        m_sub.move_to(model_c + DOWN * 0.3)
        self.play(Create(box), FadeIn(m_lbl), FadeIn(m_sub), run_time=0.9)

        # --- the prompt fed in ----------------------------------------------
        prompt = Text("What is the capital of France?", font=MONO,
                      color=TEAL).scale(0.34)
        prompt.move_to(model_c + UP * 1.75)
        feed = Arrow(prompt.get_bottom() + DOWN * 0.02,
                     box.get_top() + UP * 0.02, color=TEAL,
                     stroke_width=3, buff=0.08, max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(prompt), Create(feed), run_time=0.7)

        # --- the output stream: chaotic continuation ------------------------
        out_arrow = Arrow(box.get_right() + RIGHT * 0.02,
                          box.get_right() + RIGHT * 0.9, color=VIOLET,
                          stroke_width=3, buff=0.0,
                          max_tip_length_to_length_ratio=0.3)
        self.play(Create(out_arrow), run_time=0.4)

        out_x = 2.9
        out_top = 2.2
        lines_txt = [
            "What is the capital of France?",
            "What is the capital of Spain?",
            "What is the largest city in Europe?",
            "List ten rivers in France.",
            "Where is the Eiffel Tower located?",
            "What language do they speak?",
            "How many people live there?",
        ]
        out_lines = VGroup()
        for i, s in enumerate(lines_txt):
            col = INK if i == 0 else SECOND
            ln = Text(s, font=MONO, color=col).scale(0.3)
            ln.move_to([out_x, out_top - i * 0.5, 0], aligned_edge=LEFT)
            ln.set_opacity(0.0)
            out_lines.add(ln)
        self.add(out_lines)

        frame = RoundedRectangle(corner_radius=0.12, width=5.1, height=4.0,
                                 stroke_color=SECOND, stroke_width=1.2,
                                 stroke_opacity=0.35, fill_opacity=0.0)
        frame.move_to([out_x + 2.1, out_top - 1.5, 0])
        self.add(frame)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        v_dark = ManimColor(VIOLET)
        v_hi = ManimColor(INK)

        def box_upd(m):
            s = 0.5 + 0.5 * np.sin(2.4 * t.get_value())
            m.set_stroke(color=interpolate_color(v_dark, v_hi, 0.25 * s))
            m.set_fill(VIOLET, opacity=0.06 + 0.08 * s)
        box.add_updater(box_upd)

        def feed_upd(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_opacity(0.5 + 0.5 * s)
        feed.add_updater(feed_upd)

        # stream the output lines in one after another, continuously
        def make_line_upd(idx):
            reveal = 1.2 + idx * 1.9

            def _upd(m):
                tt = t.get_value()
                a = np.clip((tt - reveal) / 0.9, 0.0, 1.0)
                flick = 0.85 + 0.15 * np.sin(9.0 * tt + idx)
                m.set_opacity(a * flick)
            return _upd
        for i, ln in enumerate(out_lines):
            ln.add_updater(make_line_upd(i))

        # a blinking cursor trailing the stream
        cursor = Line([0, 0, 0], [0, 0.32, 0], stroke_color=VIOLET,
                      stroke_width=3)
        self.add(cursor)

        def cursor_upd(m):
            tt = t.get_value()
            idx = int(np.clip((tt - 1.2) / 1.9, 0, len(lines_txt) - 1))
            y = out_top - idx * 0.5
            m.move_to([out_x + 4.0, y, 0])
            m.set_opacity(0.5 + 0.5 * np.sign(np.sin(6.0 * tt)))
        cursor.add_updater(cursor_upd)

        # caption
        cap = Text("a raw model just continues text — it's not an assistant",
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
