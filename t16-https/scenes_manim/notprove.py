"""Scene: what the padlock does NOT prove.

Class `Notprove` (~18s). Two browser address bars side by side, BOTH with a
GREEN padlock. LEFT is the real bank; RIGHT is a scam look-alike domain with an
equally valid padlock but a CORAL warning outline. A big label spells out that
the padlock only means "encrypted to THIS domain" — not "safe". An arrow points
at the differing domain text.

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


class Notprove(Scene):
    def construct(self):
        title = Text("Both have a padlock. Only one is your bank.",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        def address_bar(lock_text, domain, outline_col, x, note, note_col):
            bar = RoundedRectangle(corner_radius=0.2, width=5.4, height=0.95,
                                   stroke_color=outline_col, stroke_width=3,
                                   fill_color="#141018", fill_opacity=0.95)
            bar.move_to([x, 1.1, 0])
            lock = Text(lock_text, font=MONO, color=GREEN,
                        weight="BOLD").scale(0.36)
            lock.move_to(bar.get_left() + RIGHT * 0.55)
            dom = Text(domain, font=MONO, color=INK).scale(0.36)
            dom.next_to(lock, RIGHT, buff=0.3)
            note_t = Text(note, font=MONO, color=note_col).scale(0.3)
            note_t.next_to(bar, DOWN, buff=0.3)
            return VGroup(bar, lock, dom, note_t), bar, lock, dom, note_t

        left_g, left_bar, left_lock, left_dom, left_note = address_bar(
            "\U0001f512", "yourbank.com", GREEN, -3.4,
            "the real site", GREEN)
        right_g, right_bar, right_lock, right_dom, right_note = address_bar(
            "\U0001f512", "your-bank-login.com", CORAL, 3.4,
            "⚠ a scam", CORAL)

        self.play(FadeIn(left_g), FadeIn(right_g), run_time=0.8)

        # big central label
        big = Text("padlock = encrypted to THIS domain — NOT “safe”",
                   font=HEAD, color=AMBER, weight="SEMIBOLD").scale(0.44)
        big.move_to([0, -0.7, 0])
        self.play(FadeIn(big, shift=UP * 0.2), run_time=0.5)

        # arrow pointing at the different domain text
        arrow = Arrow(big.get_corner(DOWN + RIGHT) + DOWN * 0.1,
                      right_dom.get_bottom() + DOWN * 0.1,
                      buff=0.1, stroke_color=CORAL, stroke_width=4,
                      max_tip_length_to_length_ratio=0.15)
        self.add(arrow)

        caption = Text("a scammer gets a valid padlock in minutes — check the domain",
                       font=HEAD, color=SECOND).scale(0.36)
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 18.0

        # both padlocks pulse green (both valid certs)
        def make_lock_pulse(lock, phase):
            def _upd(m):
                tt = t.get_value()
                p = 0.6 + 0.4 * (0.5 + 0.5 * np.sin(2.4 * tt + phase))
                m.set_opacity(p)
            return _upd
        left_lock.add_updater(make_lock_pulse(left_lock, 0.0))
        right_lock.add_updater(make_lock_pulse(right_lock, 1.2))

        # real bar: steady green outline; scam bar: coral outline that flares
        def left_bar_upd(m):
            m.set_stroke(GREEN, width=3)
        left_bar.add_updater(left_bar_upd)

        def right_bar_upd(m):
            tt = t.get_value()
            p = 0.5 + 0.5 * np.sin(2.8 * tt)
            m.set_stroke(CORAL, width=3 + 2.5 * p)
        right_bar.add_updater(right_bar_upd)

        # highlight the differing part of the scam domain by cycling its color
        def right_dom_upd(m):
            tt = t.get_value()
            g = 0.5 + 0.5 * np.sin(3.0 * tt)
            m.set_color(interpolate_color(ManimColor(INK), ManimColor(CORAL), g))
        right_dom.add_updater(right_dom_upd)

        def left_dom_upd(m):
            tt = t.get_value()
            g = 0.5 + 0.5 * np.sin(3.0 * tt)
            m.set_color(interpolate_color(ManimColor(INK), ManimColor(GREEN),
                                          0.5 * g))
        left_dom.add_updater(left_dom_upd)

        # arrow throbs toward the scam domain
        def arrow_upd(m):
            tt = t.get_value()
            p = 0.5 + 0.5 * np.sin(2.8 * tt)
            m.set_stroke(CORAL, width=3 + 2.5 * p, opacity=0.6 + 0.4 * p)
        arrow.add_updater(arrow_upd)

        # big label breathes amber
        def big_upd(m):
            tt = t.get_value()
            g = 0.7 + 0.3 * (0.5 + 0.5 * np.sin(1.8 * tt))
            m.set_opacity(g)
        big.add_updater(big_upd)

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
