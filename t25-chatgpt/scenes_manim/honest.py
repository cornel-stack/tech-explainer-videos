"""Scene: The honest picture — the whole pipeline as one assistant.

Class `Honest` (~18s). A stack diagram of the whole pipeline (base → chat
format → fine-tune → RLHF → system prompt → tools) lit up as ONE assistant,
with two CORAL caution tags: "sycophancy" and "confidently wrong". Caption:
"a brilliant trained system — an assistant, not an oracle".

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


class Honest(Scene):
    def construct(self):
        title = Text("The honest picture", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the pipeline stack (bottom = base, top = full assistant) ------
        layers = [
            ("base model", VIOLET),
            ("chat format", SILVER),
            ("fine-tune", TEAL),
            ("RLHF", AMBER),
            ("system prompt", SILVER),
            ("tools", GOLD),
        ]
        stack_x = -2.3
        layer_h = 0.66
        base_y = -2.1
        stack = []
        stack_group = VGroup()
        for i, (name, col) in enumerate(layers):
            y = base_y + i * (layer_h + 0.12)
            lay = RoundedRectangle(corner_radius=0.1, width=3.6, height=layer_h,
                                   stroke_color=col, stroke_width=2.2,
                                   fill_color=col, fill_opacity=0.08)
            lay.move_to([stack_x, y, 0])
            lab = Text(name, font=MONO, color=col).scale(0.3)
            lab.move_to([stack_x, y, 0])
            g = VGroup(lay, lab)
            stack_group.add(g)
            stack.append((lay, col, i))
        self.play(*[FadeIn(g, shift=UP * 0.15) for g in stack_group],
                  lag_ratio=0.12, run_time=1.4)

        stack_lbl = Text("one trained system", font=MONO, color=SECOND).scale(0.3)
        stack_lbl.move_to([stack_x, base_y + len(layers) * (layer_h + 0.12)
                           + 0.15, 0])
        self.play(FadeIn(stack_lbl), run_time=0.4)

        # --- lit up as ONE assistant on the right ---------------------------
        asst_c = np.array([3.4, 0.0, 0.0])
        asst = RoundedRectangle(corner_radius=0.24, width=3.2, height=3.4,
                                stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.08)
        asst.move_to(asst_c)
        asst_lbl = Text("ASSISTANT", font=MONO, color=GREEN,
                        weight="BOLD").scale(0.42)
        asst_lbl.move_to(asst_c + UP * 0.2)
        asst_sub = Text("helpful · trained", font=MONO, color=SECOND).scale(0.28)
        asst_sub.move_to(asst_c + DOWN * 0.3)
        bridge = Arrow([stack_x + 1.9, 0.0, 0], asst.get_left() + LEFT * 0.05,
                       color=GREEN, stroke_width=3, buff=0.1,
                       max_tip_length_to_length_ratio=0.12)
        self.play(Create(asst), FadeIn(asst_lbl), FadeIn(asst_sub),
                  Create(bridge), run_time=1.0)

        # --- two CORAL caution tags -----------------------------------------
        caut1 = RoundedRectangle(corner_radius=0.1, width=2.3, height=0.6,
                                 stroke_color=CORAL, stroke_width=2,
                                 fill_color=CORAL, fill_opacity=0.08)
        caut1.move_to([3.4, 2.1, 0])
        caut1_lbl = Text("sycophancy", font=MONO, color=CORAL).scale(0.3)
        caut1_lbl.move_to(caut1.get_center())
        caut2 = RoundedRectangle(corner_radius=0.1, width=2.7, height=0.6,
                                 stroke_color=CORAL, stroke_width=2,
                                 fill_color=CORAL, fill_opacity=0.08)
        caut2.move_to([3.4, -2.1, 0])
        caut2_lbl = Text("confidently wrong", font=MONO, color=CORAL).scale(0.3)
        caut2_lbl.move_to(caut2.get_center())
        self.play(FadeIn(VGroup(caut1, caut1_lbl), shift=DOWN * 0.15),
                  FadeIn(VGroup(caut2, caut2_lbl), shift=UP * 0.15),
                  run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # each stack layer lights in sequence, bottom to top
        for lay, col, idx in stack:
            def make_layer_upd(color, i):
                base = ManimColor(color)
                hi = ManimColor(INK)

                def _upd(m):
                    tt = t.get_value()
                    wave = 0.5 + 0.5 * np.sin(2.0 * tt - i * 0.7)
                    m.set_stroke(color=interpolate_color(base, hi, 0.25 * wave))
                    m.set_fill(color, opacity=0.06 + 0.1 * wave)
                return _upd
            lay.add_updater(make_layer_upd(col, idx))

        g_base = ManimColor(GREEN)
        g_hi = ManimColor(INK)

        def asst_upd(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            m.set_stroke(color=interpolate_color(g_base, g_hi, 0.25 * s))
            m.set_fill(GREEN, opacity=0.06 + 0.1 * s)
        asst.add_updater(asst_upd)

        def bridge_upd(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_opacity(0.5 + 0.5 * s)
        bridge.add_updater(bridge_upd)

        # caution tags blink gently (a warning, not alarming)
        def make_caut_upd(phase):
            def _upd(m):
                s = 0.5 + 0.5 * np.sin(3.5 * t.get_value() + phase)
                m.set_stroke(opacity=0.5 + 0.5 * s)
                m.set_fill(CORAL, opacity=0.05 + 0.08 * s)
            return _upd
        caut1.add_updater(make_caut_upd(0.0))
        caut2.add_updater(make_caut_upd(1.6))

        # caption
        cap = Text("a brilliant trained system — an assistant, not an oracle",
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
