"""Scene: silicon binning — one die, many products.

Class `Binning` (~24s). One silicon die is drawn as a grid of core tiles.
The SAME die becomes different products: all cores lit = the top chip; then
some cores grey out / get an X (defective or disabled) = a lower product. The
disabled set keeps cycling continuously so the scene never freezes.

Silicon-dark palette (no pure blue, no white). IP-safe: TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A (alive)  coral #FF5C47 (dead)  silver #C9CDD4  amber #FFB020
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
    GrowFromCenter,
    Create,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    rate_functions,
)

# --- palette -----------------------------------------------------------------
BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#35E08A"
CORAL = "#FF5C47"
SILVER = "#C9CDD4"
AMBER = "#FFB020"
TEAL = "#2DD4BF"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG

ROWS = 4
COLS = 6


class Binning(Scene):
    def construct(self):
        # --- Title -----------------------------------------------------------
        title = Text("Binning", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.66)
        title.to_edge(UP, buff=0.45)
        sub = Text("one die, sorted by how many cores survive",
                   font=HEAD, color=SECOND).scale(0.34)
        sub.next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)

        # --- Die outline -----------------------------------------------------
        die = RoundedRectangle(
            corner_radius=0.16, width=7.6, height=5.0,
            stroke_color=SILVER, stroke_width=2.5,
            fill_color="#111114", fill_opacity=0.5,
        ).shift(DOWN * 0.3)
        die_glow = RoundedRectangle(
            corner_radius=0.16, width=7.6, height=5.0,
            stroke_color=SILVER, stroke_width=10, stroke_opacity=0.08,
            fill_opacity=0,
        ).move_to(die)
        self.play(Create(die), FadeIn(die_glow), run_time=0.7)

        # --- Core grid -------------------------------------------------------
        core_cells = []  # each: dict(tile, glow, x1, x2, group index)

        def make_core():
            tile = RoundedRectangle(
                corner_radius=0.08, width=0.95, height=0.85,
                stroke_color=GREEN, stroke_width=2,
                fill_color="#0D1A12", fill_opacity=0.9,
            )
            glow = RoundedRectangle(
                corner_radius=0.08, width=0.95, height=0.85,
                stroke_color=GREEN, stroke_width=8, stroke_opacity=0.14,
                fill_opacity=0,
            ).move_to(tile)
            # Pre-built X (hidden) for when the core is disabled.
            x1 = Line(tile.get_corner(UP + LEFT), tile.get_corner(DOWN + RIGHT),
                      color=CORAL, stroke_width=3)
            x2 = Line(tile.get_corner(UP + RIGHT), tile.get_corner(DOWN + LEFT),
                      color=CORAL, stroke_width=3)
            x1.set_opacity(0)
            x2.set_opacity(0)
            grp = VGroup(glow, tile, x1, x2)
            grp.tile = tile
            grp.glow = glow
            grp.x1 = x1
            grp.x2 = x2
            return grp

        grid = VGroup()
        for _ in range(ROWS * COLS):
            grid.add(make_core())
        grid.arrange_in_grid(rows=ROWS, cols=COLS, buff=0.18)
        grid.move_to(die.get_center())
        # Re-anchor each X to its tile after the grid layout moved tiles.
        for c in grid:
            c.x1.put_start_and_end_on(c.tile.get_corner(UP + LEFT),
                                      c.tile.get_corner(DOWN + RIGHT))
            c.x2.put_start_and_end_on(c.tile.get_corner(UP + RIGHT),
                                      c.tile.get_corner(DOWN + LEFT))
            c.x1.set_opacity(0)
            c.x2.set_opacity(0)
            core_cells.append(c)

        self.play(*[GrowFromCenter(c) for c in grid],
                  lag_ratio=0.03, run_time=1.4)

        # --- Product label (changes as cores disable) -----------------------
        total = ROWS * COLS
        product = Text(f"top chip  ·  {total} / {total} cores",
                       font=MONO, color=GREEN).scale(0.4)
        product.next_to(die, DOWN, buff=0.35)
        self.play(FadeIn(product, shift=UP * 0.2), run_time=0.5)

        caption = Text("disable the bad ones, sell it cheaper",
                       font=HEAD, color=SECOND).scale(0.3)
        caption.next_to(product, DOWN, buff=0.18)
        self.play(FadeIn(caption), run_time=0.4)
        # Full die lit, ~6.5s in.

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # The set of disabled cores cycles through named "bins". For each bin we
        # precompute which core indices are dead; an updater keyed on the master
        # clock smoothly fades those cores to grey + reveals their X, restores
        # the others, and swaps the product label. Live cores shimmer so the
        # die is never still.
        # =====================================================================
        t = ValueTracker(0.0)

        # Define product bins: (label, accent, list of DEAD core indices).
        # Indices chosen so the "surviving" layout reads as a smaller product.
        rng = np.random.default_rng(3)
        all_idx = list(range(total))

        def dead_set(n_dead, seed):
            r = np.random.default_rng(seed)
            return set(int(i) for i in r.choice(all_idx, size=n_dead,
                                                replace=False))

        bins = [
            ("top chip", GREEN, set()),
            ("mid chip", AMBER, dead_set(6, 11)),
            ("budget chip", TEAL, dead_set(14, 22)),
            ("mid chip", AMBER, dead_set(8, 31)),
        ]
        bin_dwell = 3.4  # seconds per bin

        # Per-core shimmer phase for the living shimmer.
        shimmer_phase = [i * 0.37 for i in range(total)]

        def bin_at(tt):
            idx = int(tt / bin_dwell) % len(bins)
            local = (tt / bin_dwell) % 1.0
            return idx, local

        # Core updater: fade between alive/dead based on current bin + a short
        # transition window so cores visibly flip rather than snap.
        for i, c in enumerate(core_cells):
            tile = c.tile
            glow = c.glow
            x1 = c.x1
            x2 = c.x2
            ci = i

            def make_core_upd(tile=tile, glow=glow, x1=x1, x2=x2, ci=ci):
                def _upd(m):
                    tt = t.get_value()
                    bidx, local = bin_at(tt)
                    dead_now = ci in bins[bidx][2]
                    # Transition progress in/out over first 0.7 of the dwell.
                    trans = rate_functions.ease_in_out_sine(
                        min(local / 0.35, 1.0))
                    if dead_now:
                        # Grey + X revealed.
                        tile.set_stroke(color=SECOND,
                                        opacity=1.0, width=1.5)
                        tile.set_fill("#141416", opacity=0.9)
                        x1.set_opacity(0.85 * trans)
                        x2.set_opacity(0.85 * trans)
                        glow.set_stroke(opacity=0.0)
                    else:
                        accent = bins[bidx][1]
                        tile.set_stroke(color=accent, opacity=1.0, width=2)
                        tile.set_fill("#0D1A12", opacity=0.9)
                        x1.set_opacity(0)
                        x2.set_opacity(0)
                        sh = 0.5 + 0.5 * np.sin(2.3 * tt + shimmer_phase[ci])
                        glow.set_stroke(color=accent,
                                        opacity=0.08 + 0.14 * sh)
                return _upd
            c.add_updater(make_core_upd())

        # Product label updater — rewrite text as the bin changes.
        # Manim Text can't cheaply re-render per frame, so we swap discrete
        # Text mobjects keyed off the current bin index.
        label_versions = {}
        for bidx, (name, accent, dead) in enumerate(bins):
            alive = total - len(dead)
            txt = Text(f"{name}  ·  {alive} / {total} cores",
                       font=MONO, color=accent).scale(0.4)
            txt.move_to(product)
            txt.set_opacity(0)
            label_versions[bidx] = txt
            self.add(txt)
        self.remove(product)

        state = {"shown": 0}

        def label_upd(m):
            tt = t.get_value()
            bidx, local = bin_at(tt)
            for k, txt in label_versions.items():
                if k == bidx:
                    txt.set_opacity(np.clip(local / 0.25, 0.0, 1.0))
                else:
                    txt.set_opacity(max(0.0, txt.get_fill_opacity() - 0.08))
        # Attach the label driver to a hidden anchor so it ticks every frame.
        anchor = label_versions[0]
        anchor.add_updater(label_upd)

        # Caption gently pulses.
        def cap_upd(m):
            m.set_opacity(0.5 + 0.4 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 1.5)))
        caption.add_updater(cap_upd)

        # Drive ~16s — several full bin cycles.
        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
