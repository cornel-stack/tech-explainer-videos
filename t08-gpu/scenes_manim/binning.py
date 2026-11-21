"""Scene: silicon binning — same die, fewer working cores, cheaper tier.

Class `Binning` (~18s). A single square die grid of ~36 core tiles, all green
and lit. Over time some tiles develop a coral defect mark and go dark; as the
working-core count drops, a big tier label steps DOWN through RTX xx90 ->
RTX xx80 -> RTX xx70. Tiles breathe; defects appear progressively driven by a
master ValueTracker. Nothing freezes.

Dark palette only, TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  red #FF5C47  amber #FFB020  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Line,
    ValueTracker,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    rate_functions,
)

BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#76D64A"
RED = "#FF5C47"
AMBER = "#FFB020"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Binning(Scene):
    def construct(self):
        title = Text("Silicon binning", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- Die outline -----------------------------------------------------
        die = RoundedRectangle(
            corner_radius=0.16, width=5.4, height=5.4,
            stroke_color=SILVER, stroke_width=2.5,
            fill_color="#111114", fill_opacity=0.5,
        ).shift(LEFT * 3.0 + DOWN * 0.2)
        self.play(Create(die), run_time=0.7)

        # --- 6x6 = 36 core tiles --------------------------------------------
        N = 36
        tiles = VGroup()
        tile_data = []  # per tile group
        for _ in range(N):
            tile = RoundedRectangle(
                corner_radius=0.06, width=0.66, height=0.66,
                stroke_color=GREEN, stroke_width=2,
                fill_color="#122111", fill_opacity=0.9,
            )
            glow = RoundedRectangle(
                corner_radius=0.06, width=0.66, height=0.66,
                stroke_color=GREEN, stroke_width=7, stroke_opacity=0.12,
                fill_opacity=0,
            ).move_to(tile)
            l1 = Line(np.array([-0.18, -0.18, 0]), np.array([0.18, 0.18, 0]),
                      stroke_color=RED, stroke_width=3)
            l2 = Line(np.array([-0.18, 0.18, 0]), np.array([0.18, -0.18, 0]),
                      stroke_color=RED, stroke_width=3)
            xmark = VGroup(l1, l2).set_opacity(0)
            g = VGroup(glow, tile, xmark)
            g.tile = tile
            g.glow = glow
            g.xmark = xmark
            tiles.add(g)
            tile_data.append(g)
        tiles.arrange_in_grid(rows=6, cols=6, buff=0.14)
        tiles.move_to(die.get_center())
        # Re-anchor X marks to tile centers after the grid moved.
        for g in tile_data:
            c = g.tile.get_center()
            g.xmark[0].put_start_and_end_on(
                c + np.array([-0.18, -0.18, 0]), c + np.array([0.18, 0.18, 0]))
            g.xmark[1].put_start_and_end_on(
                c + np.array([-0.18, 0.18, 0]), c + np.array([0.18, -0.18, 0]))

        self.play(*[GrowFromCenter(g) for g in tiles],
                  lag_ratio=0.02, run_time=1.0)

        # --- Tier label + working-core counter (right side) ------------------
        tier = Text("RTX xx90", font=HEAD, color=GREEN,
                    weight="BOLD").scale(0.9)
        tier.move_to(RIGHT * 3.4 + UP * 0.6)
        tier._text = "RTX xx90"

        counter = Text("working cores: 36", font=MONO, color=INK).scale(0.4)
        counter.next_to(tier, DOWN, buff=0.5)
        counter._n = 36

        cap = Text("Same die — fewer working cores becomes a cheaper tier.",
                   font=HEAD, color=SECOND).scale(0.32)
        cap.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(tier), FadeIn(counter), FadeIn(cap, shift=UP * 0.2),
                  run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        rng = np.random.default_rng(5)
        death_order = list(range(N))
        rng.shuffle(death_order)

        PHASE = 14.0

        def dead_count(tt):
            frac = np.clip(tt / PHASE, 0.0, 1.0)
            return int(round(18 * frac))

        for i, g in enumerate(tile_data):
            rank = death_order.index(i)

            def make_tile_upd(gg, rnk, phase):
                def _upd(m):
                    tt = t.get_value()
                    nd = dead_count(tt)
                    if rnk < nd:
                        gg.tile.set_stroke(color=SECOND, opacity=0.5)
                        gg.tile.set_fill("#0E0E10", opacity=0.9)
                        gg.glow.set_stroke(opacity=0.0)
                        gg.xmark.set_opacity(0.9)
                    else:
                        gg.tile.set_stroke(color=GREEN, opacity=1.0)
                        gg.tile.set_fill("#122111", opacity=0.9)
                        gg.glow.set_stroke(
                            color=GREEN,
                            opacity=0.1 + 0.14 *
                            (0.5 + 0.5 * np.sin(1.8 * tt + phase)))
                        gg.xmark.set_opacity(0.0)
                return _upd
            g.add_updater(make_tile_upd(g, rank, i * 0.4))

        def counter_upd(m):
            n = N - dead_count(t.get_value())
            if n != m._n:
                m._n = n
                new = Text("working cores: %d" % n, font=MONO,
                           color=INK).scale(0.4)
                new.move_to(m)
                m.become(new)
        counter.add_updater(counter_upd)

        def tier_for(n):
            if n >= 30:
                return "RTX xx90", GREEN
            if n >= 24:
                return "RTX xx80", AMBER
            return "RTX xx70", RED

        def tier_upd(m):
            n = N - dead_count(t.get_value())
            name, col = tier_for(n)
            if name != m._text:
                m._text = name
                new = Text(name, font=HEAD, color=col,
                           weight="BOLD").scale(0.9)
                new.move_to(m)
                m.become(new)
            else:
                m.set_color(col)
        tier.add_updater(tier_upd)

        self.play(t.animate.set_value(PHASE), run_time=PHASE,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
