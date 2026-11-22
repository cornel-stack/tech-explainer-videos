"""Scene: Every Illegal Operating System — the three legal-status badges.

Class `Legend` (~18s). A top title "THE THREE BADGES" over three horizontal
rounded-rectangle cards stacked vertically. Each card has a glowing traffic
light DOT on the left, a big bold TAG, a one-line meaning and a small examples
line, left-aligned:
  RED    ILLEGAL    to distribute or possess        pirated Windows · Phantom Secure
  AMBER  DUAL-USE   legal to own · illegal to misuse Kali · Parrot · Tails · Whonix
  GREEN  LEGAL*     legal, but state-controlled...   Red Star · Astra · NeoKylin

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. Cards stagger in, then the continuous phase runs: dots breathe,
borders breathe, a soft scan bar sweeps top-to-bottom brightening whichever
card it is over, and a bottom caption gently pulses. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  red #FF5C47  amber #FFB020  green #35E08A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    config,
    FadeIn,
    GrowFromCenter,
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
RED = "#FF5C47"
AMBER = "#FFB020"
GREEN = "#35E08A"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Legend(Scene):
    def construct(self):
        # --- title -----------------------------------------------------------
        title = Text("THE THREE BADGES", font=MONO, color=SECOND,
                     weight="BOLD").scale(0.5)
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- card data -------------------------------------------------------
        rows = [
            (RED, "#1A0D0B", "ILLEGAL",
             "to distribute or possess",
             "pirated Windows  ·  Phantom Secure"),
            (AMBER, "#1A140A", "DUAL-USE",
             "legal to own  ·  illegal to misuse",
             "Kali  ·  Parrot  ·  Tails  ·  Whonix"),
            (GREEN, "#0B1A12", "LEGAL*",
             "legal, but state-controlled / banned somewhere",
             "Red Star  ·  Astra  ·  NeoKylin"),
        ]

        CARD_W = 10.0
        CARD_H = 1.9
        GAP = 0.45
        total_h = 3 * CARD_H + 2 * GAP
        top_y = total_h / 2 - CARD_H / 2 - 0.35  # nudge down from title

        cards = []           # VGroups (grouped for stagger-in)
        borders = []         # outer rounded rects (border breathing)
        glows = []           # soft outer glow rings on the dot
        dots = []            # traffic-light dots
        card_colors = []
        card_centers = []

        for i, (col, fill, tag, meaning, examples) in enumerate(rows):
            cy = top_y - i * (CARD_H + GAP)

            border = RoundedRectangle(
                corner_radius=0.18, width=CARD_W, height=CARD_H,
                stroke_color=col, stroke_width=2.5, stroke_opacity=0.7,
                fill_color=fill, fill_opacity=0.5,
            )
            border.move_to(np.array([0.0, cy, 0.0]))

            # glowing traffic-light dot on the left
            dot_x = border.get_left()[0] + 0.85
            glow = Dot(color=col, radius=0.42)
            glow.set_opacity(0.18)
            glow.move_to(np.array([dot_x, cy, 0.0]))
            dot = Dot(color=col, radius=0.22)
            dot.move_to(np.array([dot_x, cy, 0.0]))

            # left edge of the text column
            text_x = dot_x + 0.65

            tag_t = Text(tag, font=MONO, color=col, weight="BOLD").scale(0.52)
            tag_t.move_to(np.array([text_x, cy + 0.42, 0.0]),
                          aligned_edge=LEFT)

            mean_t = Text(meaning, font=HEAD, color=INK).scale(0.34)
            mean_t.move_to(np.array([text_x, cy + 0.02, 0.0]),
                           aligned_edge=LEFT)

            ex_t = Text(examples, font=MONO, color=SECOND).scale(0.28)
            ex_t.move_to(np.array([text_x, cy - 0.42, 0.0]),
                         aligned_edge=LEFT)

            group = VGroup(border, glow, dot, tag_t, mean_t, ex_t)
            cards.append(group)
            borders.append(border)
            glows.append(glow)
            dots.append(dot)
            card_colors.append(col)
            card_centers.append(cy)

        # --- staggered intro -------------------------------------------------
        for g in cards:
            self.play(GrowFromCenter(g), run_time=0.55)

        # --- bottom caption --------------------------------------------------
        caption = Text("most of this list is amber or green", font=MONO,
                       color=SILVER).scale(0.34)
        caption.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        scan_half = CARD_H / 2 + GAP / 2      # vertical reach around a center
        sweep_top = card_centers[0] + CARD_H / 2 + 0.3
        sweep_bot = card_centers[2] - CARD_H / 2 - 0.3
        sweep_span = sweep_top - sweep_bot
        sweep_period = 5.0

        def scan_y(tt):
            # sweep top -> bottom then jump back (loop)
            frac = (tt % sweep_period) / sweep_period
            return sweep_top - frac * sweep_span

        # soft horizontal scan highlight bar
        scan_bar = RoundedRectangle(
            corner_radius=0.08, width=CARD_W + 0.4, height=0.5,
            stroke_opacity=0.0, fill_color=INK, fill_opacity=0.08,
        )

        def scan_upd(m):
            m.move_to(np.array([0.0, scan_y(t.get_value()), 0.0]))
        scan_bar.add_updater(scan_upd)
        self.add(scan_bar)

        # dots pulse (breathing glow via sin)
        for i, (dot, glow, col) in enumerate(zip(dots, glows, card_colors)):
            def make_dot_breath(d, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + phase)
                    d.set_opacity(0.6 + 0.4 * s)
                return _upd
            dot.add_updater(make_dot_breath(dot, i * 1.3))

            def make_glow_breath(gl, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + phase)
                    gl.set_opacity(0.1 + 0.22 * s)
                return _upd
            glow.add_updater(make_glow_breath(glow, i * 1.3))

        # card borders breathe, brightened when scan bar is over the card
        for i, (border, cy) in enumerate(zip(borders, card_centers)):
            def make_border_breath(b, center, phase):
                def _upd(m):
                    tt = t.get_value()
                    base = 0.55 + 0.2 * (0.5 + 0.5 *
                                         np.sin(1.8 * tt + phase))
                    dist = abs(scan_y(tt) - center)
                    near = max(0.0, 1.0 - dist / scan_half)
                    op = np.clip(base + 0.4 * near, 0.0, 1.0)
                    b.set_stroke(opacity=op)
                    b.set_fill(opacity=np.clip(0.4 + 0.3 * near, 0.0, 1.0))
                return _upd
            border.add_updater(make_border_breath(border, cy, i * 0.9))

        # bottom caption gently pulses
        def caption_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 1.6)
            m.set_opacity(0.55 + 0.45 * s)
        caption.add_updater(caption_upd)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
