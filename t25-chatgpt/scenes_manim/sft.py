"""Scene: Supervised fine-tuning (SFT).

Class `Sft` (~18s). A stack of example conversations (human-written ideal
Q&A pairs) flows into the VIOLET model, nudging it; label "imitate the
ideal answer". Caption: "fine-tune on thousands of ideal example chats".

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


class Sft(Scene):
    def construct(self):
        title = Text("Supervised fine-tuning", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- stack of example conversations on the left --------------------
        cards = []
        card_group = VGroup()
        base_y = 1.5
        for i in range(5):
            y = base_y - i * 0.78
            card = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.62,
                                    stroke_color=TEAL, stroke_width=2,
                                    fill_color=TEAL, fill_opacity=0.06)
            card.move_to([-4.4, y, 0])
            # two tiny rows: a teal 'Q' dot + green 'A' dot
            q = Dot([-5.6, y + 0.12, 0], color=TEAL, radius=0.05)
            a = Dot([-5.6, y - 0.12, 0], color=GREEN, radius=0.05)
            ql = Line([-5.45, y + 0.12, 0], [-3.2, y + 0.12, 0],
                      stroke_color=TEAL, stroke_width=2, stroke_opacity=0.6)
            al = Line([-5.45, y - 0.12, 0], [-3.6, y - 0.12, 0],
                      stroke_color=GREEN, stroke_width=2, stroke_opacity=0.6)
            g = VGroup(card, q, a, ql, al)
            card_group.add(g)
            cards.append((card, g, y))
        self.play(*[FadeIn(g, shift=RIGHT * 0.2) for _, g, _ in cards],
                  lag_ratio=0.12, run_time=1.2)

        stack_lbl = Text("ideal example chats", font=MONO, color=SECOND).scale(0.3)
        stack_lbl.move_to([-4.4, base_y + 0.65, 0])
        self.play(FadeIn(stack_lbl), run_time=0.4)

        # --- the VIOLET model on the right ----------------------------------
        model_c = np.array([3.3, 0.0, 0.0])
        box = RoundedRectangle(corner_radius=0.22, width=3.0, height=2.4,
                               stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.08)
        box.move_to(model_c)
        m_lbl = Text("MODEL", font=MONO, color=VIOLET,
                     weight="BOLD").scale(0.42)
        m_lbl.move_to(model_c + UP * 0.25)
        m_sub = Text("imitate the\nideal answer", font=MONO,
                     color=SECOND).scale(0.3)
        m_sub.move_to(model_c + DOWN * 0.4)
        self.play(Create(box), FadeIn(m_lbl), FadeIn(m_sub), run_time=0.9)

        # a feed arrow from stack toward model
        feed = Arrow([-2.7, 0.0, 0], box.get_left() + LEFT * 0.05,
                     color=TEAL, stroke_width=3, buff=0.1,
                     max_tip_length_to_length_ratio=0.1)
        self.play(Create(feed), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # flowing example packets from stack into the model
        packets = VGroup()
        for i in range(6):
            p = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.26,
                                 stroke_color=TEAL, stroke_width=1.5,
                                 fill_color=TEAL, fill_opacity=0.25)
            packets.add(p)
        self.add(packets)

        start_x = -2.7
        end_x = box.get_left()[0]

        def make_packet_upd(idx):
            def _upd(m):
                tt = t.get_value()
                phase = (tt * 0.6 + idx / 6.0) % 1.0
                x = start_x + (end_x - start_x) * phase
                m.move_to([x, 0.0, 0])
                fade = np.sin(np.pi * phase)
                m.set_opacity(0.2 + 0.7 * fade)
            return _upd
        for i, p in enumerate(packets):
            p.add_updater(make_packet_upd(i))

        # model pulses stronger as it's nudged
        v_base = ManimColor(VIOLET)
        v_hi = ManimColor(GREEN)

        def box_upd(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            nudge = np.clip(t.get_value() / 18.0, 0.0, 1.0)
            m.set_stroke(color=interpolate_color(v_base, v_hi, 0.3 * nudge))
            m.set_fill(VIOLET, opacity=0.06 + 0.1 * s)
        box.add_updater(box_upd)

        def feed_upd(m):
            s = 0.5 + 0.5 * np.sin(3.5 * t.get_value())
            m.set_opacity(0.5 + 0.5 * s)
        feed.add_updater(feed_upd)

        # cards gently glow in sequence
        for i, (card, g, y) in enumerate(cards):
            def make_card_upd(phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + phase)
                    m.set_stroke(opacity=0.5 + 0.5 * s)
                    m.set_fill(TEAL, opacity=0.04 + 0.08 * s)
                return _upd
            card.add_updater(make_card_upd(i * 0.7))

        # caption
        cap = Text("fine-tune on thousands of ideal example chats",
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
