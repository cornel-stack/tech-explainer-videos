"""Scene: random access — an 8x8 grid of cells, addressed by row then column.

Class `Grid` (~20s). A memory controller box sends an AMBER address packet.
A whole ROW activates, then a COLUMN activates, and the cell at the
intersection flashes GREEN; a "byte" pops out to the right. Each cycle picks a
DIFFERENT row+column via t. Label: "random access: any cell, ~the same time".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    rate_functions,
    interpolate_color,
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

N = 8


class Grid(Scene):
    def construct(self):
        title = Text("Random access: find any cell by row + column",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the grid --------------------------------------------------------
        cells = {}
        grid = VGroup()
        for r in range(N):
            for c in range(N):
                d = Dot(color=SECOND, radius=0.085)
                cells[(r, c)] = d
                grid.add(d)
        grid.arrange_in_grid(rows=N, cols=N, buff=0.34)
        grid.move_to(DOWN * 0.3)

        self.play(*[GrowFromCenter(d) for d in grid],
                  lag_ratio=0.01, run_time=1.2)

        # positions by (row, col): row 0 = top
        def cell_pos(r, c):
            return cells[(r, c)].get_center()

        # --- memory controller box (left) -----------------------------------
        ctrl = RoundedRectangle(
            corner_radius=0.1, width=1.9, height=1.1,
            stroke_color=AMBER, stroke_width=2.5,
            fill_color="#17130A", fill_opacity=0.5,
        )
        ctrl.move_to(np.array([-5.0, grid.get_center()[1], 0]))
        ctrl_lbl = Text("memory\ncontroller", font=MONO,
                        color=AMBER).scale(0.26)
        ctrl_lbl.move_to(ctrl.get_center())
        self.play(Create(ctrl), FadeIn(ctrl_lbl), run_time=0.5)

        access_lbl = Text("random access: any cell, ~the same time",
                          font=MONO, color=SECOND).scale(0.3)
        access_lbl.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(access_lbl, shift=UP * 0.2), run_time=0.5)

        # byte output anchor (right)
        byte_x = grid.get_right()[0] + 1.4
        addr_label = Text("addr", font=MONO, color=AMBER).scale(0.26)
        addr_label.next_to(ctrl, UP, buff=0.15)
        self.add(addr_label)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        cycle = 2.4  # seconds per access

        # deterministic but varying target per cycle
        def target_rc(k):
            r = (k * 3 + 1) % N
            c = (k * 5 + 2) % N
            return r, c

        grid_left = grid.get_left()[0]
        grid_right = grid.get_right()[0]
        grid_top = grid.get_top()[1]
        grid_bot = grid.get_bottom()[1]

        # per-cell updater: light up if in active row/col; flash green at target
        for (r, c), dot in cells.items():
            rr, cc = r, c

            def make_cell(rr, cc, d):
                def _upd(m):
                    tt = t.get_value()
                    k = int(tt // cycle)
                    p = (tt % cycle) / cycle
                    tr, tc = target_rc(k)
                    # phases: 0-0.3 row, 0.3-0.6 col, 0.6-0.9 intersection flash
                    col = ManimColor(SECOND)
                    rad = 0.085
                    if p < 0.35:
                        if rr == tr:
                            a = p / 0.35
                            col = interpolate_color(
                                ManimColor(SECOND), ManimColor(AMBER), float(a))
                            rad = 0.085 + 0.03 * a
                    elif p < 0.65:
                        if rr == tr:
                            col = ManimColor(AMBER)
                            rad = 0.11
                        if cc == tc:
                            a = (p - 0.35) / 0.30
                            col = interpolate_color(
                                col, ManimColor(TEAL), float(a))
                            rad = 0.085 + 0.04 * a
                    else:
                        if rr == tr and cc == tc:
                            fl = 0.5 + 0.5 * np.sin((p - 0.65) * 30)
                            col = interpolate_color(
                                ManimColor(TEAL), ManimColor(GREEN),
                                float(np.clip(0.4 + 0.6 * fl, 0, 1)))
                            rad = 0.13
                        elif rr == tr:
                            col = interpolate_color(
                                ManimColor(AMBER), ManimColor(SECOND),
                                float((p - 0.65) / 0.35))
                            rad = 0.095
                        elif cc == tc:
                            col = interpolate_color(
                                ManimColor(TEAL), ManimColor(SECOND),
                                float((p - 0.65) / 0.35))
                            rad = 0.095
                    m.set_color(col)
                    m.scale_to_fit_width(rad * 2)
                return _upd
            dot.add_updater(make_cell(rr, cc, dot))

        # --- address packet: controller -> grid (amber) ---------------------
        addr_pkt = Dot(color=AMBER, radius=0.1)

        def addr_upd(m):
            tt = t.get_value()
            k = int(tt // cycle)
            p = (tt % cycle) / cycle
            tr, tc = target_rc(k)
            start = ctrl.get_right()
            # aim at the active row's left edge
            row_y = cell_pos(tr, 0)[1]
            end = np.array([grid_left - 0.15, row_y, 0])
            if p < 0.35:
                a = rate_functions.ease_in_out_quad(p / 0.35)
                m.move_to(start * (1 - a) + end * a)
                m.set_opacity(1.0)
            else:
                m.set_opacity(0.0)
        addr_pkt.add_updater(addr_upd)
        self.add(addr_pkt)

        # --- byte pops out to the right at intersection ----------------------
        byte_box = RoundedRectangle(
            corner_radius=0.06, width=1.5, height=0.7,
            stroke_color=GREEN, stroke_width=2.5,
            fill_color="#0D170F", fill_opacity=0.85,
        )
        byte_txt = Text("10110010", font=MONO, color=GREEN).scale(0.26)
        byte_grp = VGroup(byte_box, byte_txt)

        bits_cache = {"k": -1, "s": "10110010"}

        def byte_upd(m):
            tt = t.get_value()
            k = int(tt // cycle)
            p = (tt % cycle) / cycle
            tr, tc = target_rc(k)
            target = cell_pos(tr, tc)
            rest = np.array([byte_x + 0.3, grid.get_center()[1], 0])
            if p >= 0.65:
                a = rate_functions.ease_out_quad((p - 0.65) / 0.35)
                if k != bits_cache["k"]:
                    bits_cache["k"] = k
                    rng = np.random.default_rng(k)
                    bits_cache["s"] = "".join(
                        str(int(x)) for x in rng.integers(0, 2, 8))
                pos = target * (1 - a) + rest * a
                m.move_to(pos)
                m.set_opacity(np.clip(a * 1.4, 0, 1))
                new = Text(bits_cache["s"], font=MONO,
                           color=GREEN).scale(0.26)
                new.move_to(byte_box.get_center())
                byte_txt.become(new)
            else:
                m.set_opacity(0.0)
        byte_grp.add_updater(byte_upd)
        self.add(byte_grp)

        byte_out_lbl = Text("byte out", font=MONO, color=GREEN).scale(0.24)
        byte_out_lbl.move_to(np.array([byte_x + 0.3, grid.get_center()[1] + 0.6, 0]))

        def outlbl_upd(m):
            p = (t.get_value() % cycle) / cycle
            m.set_opacity(1.0 if p >= 0.65 else 0.0)
        byte_out_lbl.add_updater(outlbl_upd)
        self.add(byte_out_lbl)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
