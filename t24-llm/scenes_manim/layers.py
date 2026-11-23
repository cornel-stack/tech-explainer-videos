"""Scene: a deep stack of transformer blocks -> probabilities.

Class `Layers` (~19s). A deep STACK of N transformer blocks (labelled
rectangles) with tokens flowing up through them, refining; at the top the last
token fans out into a tall bar-chart of probabilities over the vocabulary, and
one bar ("blue") is sampled/highlighted. Caption: "a deep stack -> a
probability for every next token".

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
    Rectangle,
    Text,
    VGroup,
    Line,
    Dot,
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


class Layers(Scene):
    def construct(self):
        title = Text("A deep stack of blocks", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the stack of transformer blocks (left/center) -----------------
        stack_x = -3.6
        n_blocks = 6
        block_h = 0.62
        gap = 0.18
        bottom_y = -2.6
        blocks = []
        block_group = VGroup()
        for i in range(n_blocks):
            y = bottom_y + i * (block_h + gap)
            box = RoundedRectangle(corner_radius=0.08, width=3.0,
                                   height=block_h, stroke_color=VIOLET,
                                   stroke_width=2, fill_color=VIOLET,
                                   fill_opacity=0.05)
            box.move_to([stack_x, y, 0])
            lbl = Text(f"transformer block {i + 1}", font=MONO,
                       color=SECOND).scale(0.24)
            lbl.move_to(box.get_center())
            blocks.append((box, y))
            block_group.add(box, lbl)
        # the top shows "... x96" to imply depth
        depth_lbl = Text("x 96 layers", font=MONO, color=VIOLET).scale(0.28)
        depth_lbl.next_to(block_group, UP, buff=0.22)
        self.play(*[FadeIn(b, shift=UP * 0.15) for b in block_group],
                  lag_ratio=0.06, run_time=1.3)
        self.play(FadeIn(depth_lbl), run_time=0.4)

        stack_top_y = bottom_y + (n_blocks - 1) * (block_h + gap) + block_h / 2
        stack_bot_y = bottom_y - block_h / 2

        # --- probability bar-chart (right) ---------------------------------
        vocab = ["blue", "clear", "grey", "falling", "high", "the"]
        probs = [0.62, 0.15, 0.10, 0.06, 0.04, 0.03]
        chart_x = 2.6
        bar_w = 0.34
        bar_gap = 0.5
        max_h = 3.2
        base_chart_y = -2.4
        bars = []
        bar_group = VGroup()
        for i, (word, p) in enumerate(zip(vocab, probs)):
            bx = chart_x + i * bar_gap
            h = 0.3 + max_h * p
            col = GREEN if word == "blue" else SECOND
            bar = Rectangle(width=bar_w, height=h, stroke_width=0,
                            fill_color=col, fill_opacity=0.85)
            bar.move_to([bx, base_chart_y + h / 2, 0])
            wl = Text(word, font=MONO, color=col).scale(0.22)
            wl.next_to(bar, DOWN, buff=0.1)
            bars.append((bar, word, p, bx, col))
            bar_group.add(bar, wl)
        chart_lbl = Text("P(next token)", font=MONO, color=SECOND).scale(0.28)
        chart_lbl.move_to([chart_x + 1.1, base_chart_y + max_h + 0.3, 0])
        self.play(*[FadeIn(b) for b in bar_group], FadeIn(chart_lbl),
                  lag_ratio=0.05, run_time=1.1)

        # fan-out arrow from stack top to chart
        fan = Arrow([stack_x + 1.5, stack_top_y, 0],
                    [chart_x - 0.5, base_chart_y + max_h * 0.4, 0],
                    buff=0.1, stroke_width=3, color=SECOND,
                    max_tip_length_to_length_ratio=0.1)
        self.play(Create(fan), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # --- tokens flowing UP through the stack ---------------------------
        flow_dots = VGroup()
        n_flow = 4
        for k in range(n_flow):
            d = Dot([stack_x, stack_bot_y, 0], color=TEAL, radius=0.09)
            flow_dots.add(d)
            self.add(d)
        span = stack_top_y - stack_bot_y

        for k, d in enumerate(flow_dots):
            def make_flow(dot, offset):
                def _upd(m):
                    tt = t.get_value()
                    frac = ((0.35 * tt + offset) % 1.0)
                    y = stack_bot_y + frac * span
                    dot.move_to([stack_x, y, 0])
                    # refine: color teal -> green as it rises
                    dot.set_color(interpolate_color(
                        ManimColor(TEAL), ManimColor(GREEN), frac))
                    dot.set_opacity(0.4 + 0.6 * np.sin(frac * np.pi))
                return _upd
            d.add_updater(make_flow(d, k / n_flow))

        # blocks pulse in an upward travelling wave (processing)
        for i, (box, y) in enumerate(blocks):
            def make_block(bx, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() - phase)
                    bx.set_stroke(opacity=0.5 + 0.4 * s)
                    bx.set_fill(VIOLET, opacity=0.03 + 0.09 * s)
                return _upd
            box.add_updater(make_block(box, i * 0.8))

        # bars subtly wobble; "blue" bar pulses green (being sampled)
        for bar, word, p, bx, col in bars:
            if word == "blue":
                def blue_upd(m):
                    s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
                    m.set_fill(GREEN, opacity=0.7 + 0.3 * s)
                    base_h = 0.3 + max_h * p
                    hh = base_h * (1.0 + 0.04 * s)
                    m.scale_to_fit_height(hh)
                    m.move_to([bx, base_chart_y + hh / 2, 0])
                bar.add_updater(blue_upd)
            else:
                def make_bar(barx, ph, base_h):
                    def _upd(m):
                        s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + ph)
                        m.set_fill(SECOND, opacity=0.5 + 0.25 * s)
                    return _upd
                bar.add_updater(make_bar(bx, bx, 0.3 + max_h * p))

        # "sampled" marker on the blue bar
        blue_bar = bars[0][0]
        sampled = Text("sampled", font=MONO, color=GREEN).scale(0.26)
        sampled.move_to([chart_x, base_chart_y + max_h + 0.3, 0])

        def sampled_upd(m):
            m.next_to(blue_bar, UP, buff=0.12)
            m.set_opacity(0.5 + 0.5 * (0.5 + 0.5 *
                          np.sin(3.0 * t.get_value())))
        sampled.add_updater(sampled_upd)
        self.add(sampled)

        # fan arrow flows
        fan.add_updater(lambda m: m.set_opacity(
            0.4 + 0.5 * (0.5 + 0.5 * np.sin(2.4 * t.get_value()))))
        depth_lbl.add_updater(lambda m: m.set_opacity(
            0.6 + 0.4 * (0.5 + 0.5 * np.sin(1.6 * t.get_value()))))

        # caption
        cap = Text("a deep stack -> a probability for every next token",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

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
