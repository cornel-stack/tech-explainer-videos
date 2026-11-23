"""Scene: The honest 5G scorecard.

Class `Real` (~18s). Rows with check/cross marks: mid-band 5G a genuine
upgrade (GREEN), crowds & capacity (GREEN), low latency (GREEN), mmWave
gigabit rare / stadiums only (CORAL), 6G already in research (AMBER). A
balanced summary card; a highlight sweeps the rows on a loop. Caption:
"mid-band is the real deal — ignore the icon".

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


class Real(Scene):
    def construct(self):
        title = Text("The honest scorecard", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # rows: (text, mark, color)
        rows = [
            ("mid-band 5G — a genuine upgrade", "check", GREEN),
            ("crowds & capacity", "check", GREEN),
            ("low latency", "check", GREEN),
            ("mmWave gigabit — rare, stadiums only", "cross", CORAL),
            ("6G — already in research", "arrow", AMBER),
        ]

        row_group = VGroup()
        row_cards = []
        marks = []
        for text, mark, col in rows:
            card = RoundedRectangle(corner_radius=0.12, width=8.4, height=0.82,
                                    stroke_color=col, stroke_width=2,
                                    fill_color="#101216", fill_opacity=0.8)
            sym = {"check": "v", "cross": "x", "arrow": ">"}[mark]
            mk = Text(sym, font=MONO, color=col, weight="BOLD").scale(0.5)
            mk.move_to(card.get_left() + RIGHT * 0.5)
            lbl = Text(text, font=HEAD, color=INK).scale(0.4)
            lbl.next_to(mk, RIGHT, buff=0.35)
            g = VGroup(card, mk, lbl)
            row_group.add(g)
            row_cards.append(card)
            marks.append((mk, col))
        row_group.arrange(DOWN, buff=0.28)
        row_group.move_to([0, 0.2, 0])

        self.play(*[FadeIn(g, shift=RIGHT * 0.3) for g in row_group],
                  lag_ratio=0.15, run_time=1.4)

        # summary card
        summary = RoundedRectangle(corner_radius=0.14, width=8.4, height=0.8,
                                   stroke_color=TEAL, stroke_width=2.5,
                                   fill_color="#0C1413", fill_opacity=0.85)
        summary.next_to(row_group, DOWN, buff=0.35)
        sum_lbl = Text("real, useful, oversold — all at once", font=HEAD,
                       color=TEAL, weight="SEMIBOLD").scale(0.4)
        sum_lbl.move_to(summary)
        self.play(FadeIn(summary), FadeIn(sum_lbl), run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        n_rows = len(row_cards)
        SWEEP = 4.0  # seconds per full sweep

        # highlight sweeps down the rows: the active row brightens
        for i, card in enumerate(row_cards):
            col = rows[i][2]

            def make_card(cardm, idx, basecol):
                def _upd(m):
                    pos = (t.get_value() / SWEEP) % 1.0
                    active = int(pos * n_rows)
                    if active == idx:
                        local = (pos * n_rows) - idx
                        s = np.sin(local * np.pi)  # peak mid-dwell
                        m.set_stroke(width=2.0 + 3.5 * s)
                        m.set_fill(opacity=0.8 + 0.15 * s)
                    else:
                        m.set_stroke(width=2.0)
                        m.set_fill(opacity=0.75)
                return _upd
            card.add_updater(make_card(card, i, col))

        # marks pulse on a loop (check/cross/arrow)
        for i, (mk, col) in enumerate(marks):
            def make_mark(mkm, basecol, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + phase)
                    m.set_opacity(0.6 + 0.4 * s)
                    m.scale_to_fit_height(0.4 * (0.92 + 0.12 * s))
                return _upd
            mk.add_updater(make_mark(mk, col, i * 0.8))

        # summary card border shimmers teal<->green
        def sum_upd(m):
            s = 0.5 + 0.5 * np.sin(1.8 * t.get_value())
            c = interpolate_color(ManimColor(TEAL), ManimColor(GREEN), s)
            m.set_stroke(c, width=2.0 + 2.0 * s)
        summary.add_updater(sum_upd)

        # caption
        cap = Text("mid-band is the real deal — ignore the icon", font=HEAD,
                   color=SECOND).scale(0.38)
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
