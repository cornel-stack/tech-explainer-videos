"""Scene: the chain of trust.

Class `Certificate` (~18s). Three stacked cards bottom->top: the site cert,
an intermediate CA, and the root CA that lives in your browser. "signed by →"
arrows link each up to the next. A GREEN check propagates UP the chain and a
check lands on the browser. A side "self-signed" cert gets a CORAL ✗.

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Arrow,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    interpolate_color,
    LEFT,
    RIGHT,
    UP,
    DOWN,
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


class Certificate(Scene):
    def construct(self):
        title = Text("Why your browser trusts a certificate", font=HEAD,
                     color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the chain cards (bottom -> top) --------------------------------
        X = -1.6
        card_defs = [
            ("Site cert\nyourbank.com", -2.0, TEAL),
            ("Intermediate CA", -0.3, VIOLET),
            ("Root CA\n(in your browser)", 1.4, AMBER),
        ]
        cards = []
        checks = []
        for text, y, col in card_defs:
            card = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.1,
                                    stroke_color=col, stroke_width=2.5,
                                    fill_color="#141018", fill_opacity=0.9)
            card.move_to([X, y, 0])
            lbl = Text(text, font=MONO, color=col).scale(0.28)
            lbl.move_to(card.get_center())
            chk = Text("✓", font=MONO, color=GREEN, weight="BOLD").scale(0.5)
            chk.move_to(card.get_right() + LEFT * 0.35)
            chk.set_opacity(0)
            cards.append((card, lbl, chk, col, y))
            checks.append(chk)
            self.add(card, lbl, chk)

        # "signed by ->" arrows pointing up the chain
        arrows = []
        for i in range(len(cards) - 1):
            lo = cards[i][0]
            hi = cards[i + 1][0]
            arr = Arrow(lo.get_top(), hi.get_bottom(), buff=0.05,
                        stroke_color=SECOND, stroke_width=3,
                        max_tip_length_to_length_ratio=0.25)
            slbl = Text("signed by →", font=MONO, color=SECOND).scale(0.22)
            slbl.next_to(arr, RIGHT, buff=0.15)
            arrows.append((arr, slbl))
            self.add(arr, slbl)

        # browser badge at the very top
        browser = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.7,
                                   stroke_color=SILVER, stroke_width=2,
                                   fill_color="#141018", fill_opacity=0.9)
        browser.move_to([X, 2.75, 0])
        blbl = Text("your browser", font=MONO, color=SILVER).scale(0.26)
        blbl.move_to(browser.get_center())
        btop_chk = Text("\U0001f512 trusted", font=MONO, color=GREEN).scale(0.28)
        btop_chk.next_to(browser, RIGHT, buff=0.2)
        btop_chk.set_opacity(0)
        self.add(browser, blbl, btop_chk)

        # --- side example: self-signed cert ---------------------------------
        ss = RoundedRectangle(corner_radius=0.1, width=2.7, height=1.0,
                              stroke_color=CORAL, stroke_width=2.5,
                              fill_color="#1A0F0C", fill_opacity=0.9)
        ss.move_to([4.6, -1.0, 0])
        ss_lbl = Text("self-signed\ncert", font=MONO, color=CORAL).scale(0.26)
        ss_lbl.move_to(ss.get_center())
        ss_warn = Text("✗ ⚠ not trusted", font=MONO, color=CORAL).scale(0.26)
        ss_warn.next_to(ss, DOWN, buff=0.2)
        ss_warn.set_opacity(0)
        self.add(ss, ss_lbl, ss_warn)

        self.play(
            *[FadeIn(c[0]) for c in cards],
            *[FadeIn(a[0]) for a in arrows],
            FadeIn(browser), FadeIn(ss),
            run_time=0.9,
        )

        caption = Text("browser trusts CA · CA vouches for the site",
                       font=HEAD, color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 18.0
        cycle = 6.0  # verification sweep period

        # each chain level lights at a staggered time as the sweep rises
        # stages: 0 site, 1 inter, 2 root, 3 browser  (each ~1.2s apart)
        stage_times = [0.8, 2.0, 3.2, 4.4]

        def make_check(i, chk, col, card):
            def _upd(m):
                tt = t.get_value() % cycle
                on = tt >= stage_times[i]
                if on:
                    pulse = 0.6 + 0.4 * np.sin(4 * tt)
                    m.set_opacity(pulse)
                else:
                    m.set_opacity(0)
            return _upd

        for i, (card, lbl, chk, col, y) in enumerate(cards):
            chk.add_updater(make_check(i, chk, col, card))

            def make_card_glow(c, cc, idx):
                def _upd(m):
                    tt = t.get_value() % cycle
                    lit = tt >= stage_times[idx]
                    g = 1.0 if lit else 0.0
                    base = interpolate_color(ManimColor(cc), ManimColor(GREEN),
                                             0.5 * g)
                    m.set_stroke(base, width=2.5 + 2.0 * g)
                return _upd
            card.add_updater(make_card_glow(card, col, i))

        # browser badge check (stage 3)
        def btop_upd(m):
            tt = t.get_value() % cycle
            on = tt >= stage_times[3]
            m.set_opacity(0.6 + 0.4 * np.sin(4 * tt) if on else 0.0)
        btop_chk.add_updater(btop_upd)

        def browser_upd(m):
            tt = t.get_value() % cycle
            lit = tt >= stage_times[3]
            col = interpolate_color(ManimColor(SILVER), ManimColor(GREEN),
                                    0.6 if lit else 0.0)
            m.set_stroke(col, width=2 + (2 if lit else 0))
        browser.add_updater(browser_upd)

        # arrows light up in sequence as sweep passes them
        def make_arrow(i, arr, slbl):
            def _upd(m):
                tt = t.get_value() % cycle
                on = tt >= stage_times[i] + 0.4
                g = 1.0 if on else 0.0
                c = interpolate_color(ManimColor(SECOND), ManimColor(GREEN), g)
                arr.set_stroke(c, width=3 + 1.5 * g)
                slbl.set_color(c)
                slbl.set_opacity(0.4 + 0.5 * g)
            return _upd
        for i, (arr, slbl) in enumerate(arrows):
            arr.add_updater(make_arrow(i, arr, slbl))

        # self-signed ✗ pulses coral on the same loop
        def ss_box_upd(m):
            tt = t.get_value()
            p = 0.5 + 0.5 * np.sin(2.2 * tt)
            m.set_stroke(CORAL, width=2.5 + 2.0 * p)
        ss.add_updater(ss_box_upd)

        def ss_warn_upd(m):
            tt = t.get_value()
            m.set_opacity(0.5 + 0.5 * (0.5 + 0.5 * np.sin(2.2 * tt)))
        ss_warn.add_updater(ss_warn_upd)

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
