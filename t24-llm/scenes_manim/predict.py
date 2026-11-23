"""Scene: the core predict-next-word loop.

Class `Predict` (~18s). A prompt "The sky is" sits on a line. The model box
emits the next word "blue" with a probability; the word is appended and the
sentence grows word-by-word, looping predict -> append -> repeat.
Caption: "an LLM just predicts the next word, over and over".

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


def token_pill(word, color=TEAL):
    """A TEAL mono token pill (text-only, rounded box)."""
    txt = Text(word, font=MONO, color=color).scale(0.42)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=txt.width + 0.34,
        height=0.6,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.08,
    )
    g = VGroup(box, txt)
    txt.move_to(box.get_center())
    return g


class Predict(Scene):
    def construct(self):
        title = Text("Predict the next word", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the model box in the middle ------------------------------------
        model = RoundedRectangle(corner_radius=0.18, width=2.6, height=1.6,
                                 stroke_color=VIOLET, stroke_width=2.5,
                                 fill_color=VIOLET, fill_opacity=0.06)
        model.move_to([0, 0.4, 0])
        model_lbl = Text("LLM", font=HEAD, color=VIOLET,
                         weight="SEMIBOLD").scale(0.5)
        model_lbl.move_to(model.get_center() + UP * 0.18)
        model_sub = Text("next-word predictor", font=MONO, color=SECOND).scale(0.24)
        model_sub.move_to(model.get_center() + DOWN * 0.28)
        self.play(Create(model), FadeIn(model_lbl), FadeIn(model_sub),
                  run_time=0.8)

        # --- the growing sentence on a baseline -----------------------------
        base_y = -2.2
        start_x = -5.4
        words_full = ["The", "sky", "is", "blue", "and", "clear", "today"]
        # first three are the given prompt
        pills = []
        x = start_x
        sentence = VGroup()
        for i, w in enumerate(words_full[:3]):
            col = SECOND if False else TEAL
            p = token_pill(w, col)
            p.move_to([x + p.width / 2, base_y, 0])
            x = x + p.width + 0.22
            pills.append(p)
            sentence.add(p)
        prompt_lbl = Text("prompt", font=MONO, color=SECOND).scale(0.26)
        prompt_lbl.next_to(sentence, UP, buff=0.18)
        self.play(*[FadeIn(p) for p in pills], FadeIn(prompt_lbl),
                  run_time=0.9)

        # feed arrow up into model, emit arrow down
        feed = Arrow(sentence.get_top() + UP * 0.05, model.get_bottom(),
                     buff=0.1, stroke_width=3, color=SECOND,
                     max_tip_length_to_length_ratio=0.12)
        self.play(Create(feed), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # emitted-word display next to the model (the prediction)
        emit = token_pill("blue", GREEN)
        emit.move_to([2.9, 0.9, 0])
        prob = Text("p = 0.62", font=MONO, color=GREEN).scale(0.30)
        prob.next_to(emit, DOWN, buff=0.14)
        emit_lbl = Text("next word", font=MONO, color=SECOND).scale(0.24)
        emit_lbl.next_to(emit, UP, buff=0.14)
        self.add(emit, prob, emit_lbl)

        emit_arrow = Arrow(model.get_right(), emit.get_left() + LEFT * 0.05,
                           buff=0.1, stroke_width=3, color=GREEN,
                           max_tip_length_to_length_ratio=0.2)
        self.add(emit_arrow)

        # The cycle: every CYCLE seconds a new word is "appended" to sentence.
        CYCLE = 2.4
        # pre-build the words that appear over time (4 more)
        appended = []
        base_count = 3
        xcursor = {"x": x}
        # positions computed lazily; build pill mobjects now, hidden
        future_words = words_full[3:]
        future_probs = ["0.62", "0.48", "0.55", "0.41"]
        future_pills = []
        fx = x
        for w in future_words:
            fp = token_pill(w, TEAL)
            fp.move_to([fx + fp.width / 2, base_y, 0])
            fx = fx + fp.width + 0.22
            fp.set_opacity(0.0)
            future_pills.append(fp)
            self.add(fp)

        # model pulse
        def model_upd(m):
            s = 0.5 + 0.5 * np.sin(2.6 * t.get_value())
            m.set_stroke(opacity=0.6 + 0.4 * s)
            m.set_fill(VIOLET, opacity=0.04 + 0.08 * s)
        model.add_updater(model_upd)

        # emit pill + prob cycle through the future words
        def emit_upd(m):
            tt = t.get_value()
            idx = int(tt // CYCLE) % len(future_words)
            phase = (tt % CYCLE) / CYCLE
            word = future_words[idx]
            if m.submobjects:
                old = m[1].text if len(m) > 1 else ""
            m.become(token_pill(word, GREEN).move_to([2.9, 0.9, 0]))
            pop = np.sin(min(phase * 3.2, np.pi)) if phase < 1.0 else 0.0
            m.scale(1.0 + 0.12 * max(pop, 0.0))
        emit.add_updater(emit_upd)

        def prob_upd(m):
            tt = t.get_value()
            idx = int(tt // CYCLE) % len(future_words)
            new = Text("p = 0." + future_probs[idx].split(".")[1],
                       font=MONO, color=GREEN).scale(0.30)
            new.move_to([2.9, 0.9, 0]).next_to(emit, DOWN, buff=0.14)
            m.become(new)
        prob.add_updater(prob_upd)

        # feed arrow pulses
        def feed_upd(m):
            s = 0.5 + 0.5 * np.sin(2.6 * t.get_value())
            m.set_opacity(0.4 + 0.5 * s)
        feed.add_updater(feed_upd)
        emit_arrow.add_updater(lambda m: m.set_opacity(
            0.4 + 0.5 * (0.5 + 0.5 * np.sin(2.6 * t.get_value()))))

        # reveal appended words one CYCLE apart
        def make_reveal(fp, reveal_at):
            def _upd(m):
                tt = t.get_value()
                if tt >= reveal_at:
                    a = min((tt - reveal_at) / 0.5, 1.0)
                    m.set_opacity(a)
                else:
                    m.set_opacity(0.0)
            return _upd
        for k, fp in enumerate(future_pills):
            fp.add_updater(make_reveal(fp, CYCLE * (k + 0.9)))

        # loop label going predict -> append -> repeat
        loop_lbl = Text("predict  ->  append  ->  repeat", font=MONO,
                        color=AMBER).scale(0.30)
        loop_lbl.move_to([0, -3.2, 0])

        def loop_upd(m):
            m.set_opacity(0.5 + 0.5 * (0.5 + 0.5 *
                          np.sin(1.6 * t.get_value())))
        loop_lbl.add_updater(loop_upd)
        self.add(loop_lbl)

        # caption
        cap = Text("an LLM just predicts the next word, over and over",
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
