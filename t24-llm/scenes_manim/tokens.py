"""Scene: text -> tokens -> numbers.

Class `Tokens` (~17s). A sentence is chopped into TEAL token pills; one word
"Running" visibly splits into "Run" + "ning"; each pill gets a numeric ID
below it. Caption: "text -> tokens -> numbers (it never sees letters)".

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
    Transform,
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


def token_pill(word, color=TEAL, scale=0.42):
    txt = Text(word, font=MONO, color=color).scale(scale)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=txt.width + 0.34,
        height=0.62,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.08,
    )
    txt.move_to(box.get_center())
    return VGroup(box, txt)


class Tokens(Scene):
    def construct(self):
        title = Text("Text becomes tokens", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- raw text line --------------------------------------------------
        raw = Text("Running late tonight", font=HEAD, color=INK).scale(0.6)
        raw.move_to([0, 1.7, 0])
        raw_lbl = Text("raw text", font=MONO, color=SECOND).scale(0.26)
        raw_lbl.next_to(raw, UP, buff=0.18)
        self.play(FadeIn(raw), FadeIn(raw_lbl), run_time=0.7)

        # --- chop into token pills -----------------------------------------
        # "Running" splits into "Run" + "ning"
        tok_words = ["Run", "ning", "late", "tonight"]
        ids = ["18923", "1251", "3245", "9087"]
        pills = []
        base_y = 0.1
        total_w = 0
        tmp = []
        for w in tok_words:
            p = token_pill(w, TEAL)
            tmp.append(p)
            total_w += p.width + 0.26
        total_w -= 0.26
        x = -total_w / 2
        for p in tmp:
            p.move_to([x + p.width / 2, base_y, 0])
            x += p.width + 0.26
            pills.append(p)

        tok_lbl = Text("tokens", font=MONO, color=TEAL).scale(0.28)
        tok_lbl.move_to([0, base_y + 0.75, 0])

        # animate the chop: raw -> pills (lag)
        self.play(FadeIn(tok_lbl), run_time=0.4)
        self.play(*[FadeIn(p, shift=DOWN * 0.3) for p in pills],
                  lag_ratio=0.12, run_time=1.2)

        # highlight the split: a bracket under Run+ning
        split_line = Line(pills[0].get_bottom() + DOWN * 0.08,
                          pills[1].get_bottom() + DOWN * 0.08,
                          stroke_color=AMBER, stroke_width=2.5)
        split_lbl = Text("one word -> two tokens", font=MONO,
                         color=AMBER).scale(0.24)
        split_lbl.next_to(split_line, DOWN, buff=0.1)
        self.play(Create(split_line), FadeIn(split_lbl), run_time=0.7)

        # --- number IDs below each pill ------------------------------------
        id_labels = []
        id_y = -1.7
        for p, idv in zip(pills, ids):
            idt = Text(idv, font=MONO, color=VIOLET).scale(0.38)
            idt.move_to([p.get_center()[0], id_y, 0])
            id_labels.append(idt)
        connectors = []
        for p, idt in zip(pills, id_labels):
            c = Line([p.get_center()[0], p.get_bottom()[1] - 0.15, 0],
                     [p.get_center()[0], idt.get_top()[1] + 0.08, 0],
                     stroke_color=SECOND, stroke_width=1.5,
                     stroke_opacity=0.5)
            connectors.append(c)
        num_lbl = Text("numbers (IDs)", font=MONO, color=VIOLET).scale(0.28)
        num_lbl.move_to([0, id_y - 0.55, 0])
        self.play(*[Create(c) for c in connectors],
                  *[FadeIn(i) for i in id_labels],
                  FadeIn(num_lbl), run_time=1.0)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # pills pulse in sequence (left to right)
        for i, p in enumerate(pills):
            def make_pill(box, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + phase)
                    box.set_stroke(opacity=0.55 + 0.45 * s)
                    box.set_fill(TEAL, opacity=0.05 + 0.1 * s)
                return _upd
            p.add_updater(make_pill(p[0], -i * 0.9))

        # IDs glow in the same wave (handing off from pill to number)
        for i, idt in enumerate(id_labels):
            def make_id(phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + phase)
                    m.set_color(interpolate_color(
                        ManimColor(SECOND), ManimColor(VIOLET), 0.3 + 0.7 * s))
                return _upd
            idt.add_updater(make_id(-i * 0.9 - 0.6))

        # split line pulses amber
        def split_upd(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_stroke(opacity=0.4 + 0.5 * s)
        split_line.add_updater(split_upd)
        split_lbl.add_updater(lambda m: m.set_opacity(
            0.5 + 0.5 * (0.5 + 0.5 * np.sin(3.0 * t.get_value()))))

        # connectors flow
        for i, c in enumerate(connectors):
            def make_con(phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + phase)
                    m.set_stroke(opacity=0.25 + 0.4 * s)
                return _upd
            c.add_updater(make_con(-i * 0.9 - 0.3))

        # caption
        cap = Text("text -> tokens -> numbers (it never sees letters)",
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
