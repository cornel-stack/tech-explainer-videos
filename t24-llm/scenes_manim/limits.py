"""Scene: brilliant but wrong — the limits.

Class `Limits` (~17s). Three labelled failure cards: "HALLUCINATION:
plausible != true", "STALE: frozen at training time", "MATHS: pattern, not
calculation"; a core label "it predicts, it doesn't understand". A scan
highlights each card in turn; cards pulse. Caption: "a pattern-completer, not
a mind".

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


def make_card(head, body, accent, width=3.5):
    box = RoundedRectangle(corner_radius=0.14, width=width, height=2.3,
                           stroke_color=accent, stroke_width=2,
                           fill_color=accent, fill_opacity=0.05)
    htxt = Text(head, font=HEAD, color=accent, weight="SEMIBOLD").scale(0.42)
    btxt = Text(body, font=MONO, color=INK).scale(0.3)
    htxt.move_to(box.get_center() + UP * 0.45)
    btxt.move_to(box.get_center() + DOWN * 0.25)
    # keep text inside the card
    if btxt.width > width - 0.4:
        btxt.scale_to_fit_width(width - 0.4)
    return VGroup(box, htxt, btxt)


class Limits(Scene):
    def construct(self):
        title = Text("Brilliant, but not a mind", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- three failure cards -------------------------------------------
        card_specs = [
            ("HALLUCINATION", "plausible != true", CORAL),
            ("STALE", "frozen at training time", AMBER),
            ("MATHS", "pattern, not calculation", VIOLET),
        ]
        cards = []
        for head, body, accent in card_specs:
            cards.append(make_card(head, body, accent))
        card_group = VGroup(*cards).arrange(RIGHT, buff=0.45)
        card_group.move_to([0, 0.55, 0])
        self.play(*[FadeIn(c, shift=UP * 0.2) for c in cards],
                  lag_ratio=0.15, run_time=1.3)

        # --- core label ----------------------------------------------------
        core = Text("it predicts — it doesn't understand", font=HEAD,
                    color=SILVER, weight="SEMIBOLD").scale(0.5)
        core.move_to([0, -2.1, 0])
        core_box = RoundedRectangle(corner_radius=0.12,
                                    width=core.width + 0.7, height=0.9,
                                    stroke_color=SILVER, stroke_width=2,
                                    fill_color=SILVER, fill_opacity=0.04)
        core_box.move_to(core.get_center())
        self.play(Create(core_box), FadeIn(core), run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        accents = [CORAL, AMBER, VIOLET]
        centers_x = [c.get_center()[0] for c in cards]

        # a scan highlights each card in turn (period per card)
        SCAN = 2.2

        for i, c in enumerate(cards):
            box = c[0]
            htxt = c[1]
            accent = accents[i]

            def make_card_upd(cbox, ctxt, acc, idx):
                def _upd(m):
                    tt = t.get_value()
                    active = int((tt / SCAN) % len(cards)) == idx
                    breathe = 0.5 + 0.5 * np.sin(2.6 * tt + idx * 1.1)
                    if active:
                        pulse = 0.5 + 0.5 * np.sin(6.0 * tt)
                        cbox.set_stroke(acc, width=2.5 + 1.5 * pulse,
                                        opacity=0.85 + 0.15 * pulse)
                        cbox.set_fill(acc, opacity=0.1 + 0.08 * pulse)
                        ctxt.set_opacity(1.0)
                    else:
                        cbox.set_stroke(acc, width=2.0,
                                        opacity=0.4 + 0.25 * breathe)
                        cbox.set_fill(acc, opacity=0.03 + 0.04 * breathe)
                        ctxt.set_opacity(0.7 + 0.2 * breathe)
                return _upd
            box_and_head = VGroup(box, htxt)
            box_and_head.add_updater(make_card_upd(box, htxt, accent, i))

        # scan bar sweeping across the cards
        scan_bar = Line([0, 1.7, 0], [0, -0.6, 0], stroke_color=INK,
                        stroke_width=3, stroke_opacity=0.5)
        x_lo = cards[0].get_left()[0]
        x_hi = cards[-1].get_right()[0]

        def scan_upd(m):
            tt = t.get_value()
            phase = (tt / SCAN) % len(cards) / len(cards)
            x = x_lo + (x_hi - x_lo) * phase
            new = Line([x, 1.9, 0], [x, -0.75, 0], stroke_color=INK,
                       stroke_width=3)
            glow = 0.3 + 0.4 * (0.5 + 0.5 * np.sin(6.0 * tt))
            new.set_stroke(opacity=glow)
            m.become(new)
        scan_bar.add_updater(scan_upd)
        self.add(scan_bar)

        # core label breathes silver
        def core_upd(m):
            s = 0.5 + 0.5 * np.sin(1.8 * t.get_value())
            m.set_color(interpolate_color(
                ManimColor(SECOND), ManimColor(SILVER), 0.5 + 0.5 * s))
        core.add_updater(core_upd)
        core_box.add_updater(lambda m: m.set_stroke(
            opacity=0.45 + 0.4 * (0.5 + 0.5 * np.sin(1.8 * t.get_value()))))

        # caption
        cap = Text("a pattern-completer, not a mind", font=HEAD,
                   color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

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
