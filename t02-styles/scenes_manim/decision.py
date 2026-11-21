"""Interlude scene: the "which style do I pick?" decision table.

Class `Decision` — a rounded table that builds row by row, then a glowing
highlight travels CONTINUOUSLY down the PICK column on a loop, pulsing each
chip as it passes, while a soft shimmer sweeps across the header. Nothing
ever freezes. ~24s.

Dark design system (no blue, no white).
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Line,
    Text,
    VGroup,
    ValueTracker,
    config,
    FadeIn,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    rate_functions,
)

BG = "#0A0A0C"
INK = "#EDE7DB"
SECOND = "#9A958C"
AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

config.background_color = BG

# Column centre x-positions and widths (within a ~13-wide usable frame).
COL_X = {"scenario": -4.4, "pick": 0.3, "why": 4.2}
COL_W = {"scenario": 4.6, "pick": 3.0, "why": 4.2}
ROW_H = 0.78


class Decision(Scene):
    def construct(self):
        title = Text("Which style do I pick?",
                     font="Inter", color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)

        rows_data = [
            ("Public API", "REST", AMBER, "simple, cacheable"),
            ("Mobile app, nested data", "GraphQL", MAGENTA,
             "one query, no over-fetch"),
            ("Microservices (internal)", "gRPC", MINT,
             "binary + HTTP/2, fast"),
            ("Chat / live prices", "WebSocket", VIOLET,
             "two-way, persistent"),
            ("Notify me when X happens", "Webhook", CORAL,
             "server calls you"),
            ("Video / screen share", "WebRTC", GOLD, "peer-to-peer"),
        ]

        top_y = 2.35

        def cell_text(s, color, scale, weight="NORMAL"):
            return Text(s, font="Inter", color=color,
                        weight=weight).scale(scale)

        # --- Header row ------------------------------------------------------
        header_y = top_y
        header = VGroup()
        header_cells = {}
        for key, label in (("scenario", "SCENARIO"),
                           ("pick", "PICK"), ("why", "WHY")):
            tcell = cell_text(label, INK, 0.34, weight="BOLD")
            tcell.move_to([COL_X[key], header_y, 0])
            header.add(tcell)
            header_cells[key] = tcell
        header_rule = Line([-6.9, header_y - ROW_H / 2, 0],
                           [6.6, header_y - ROW_H / 2, 0],
                           color=SECOND, stroke_width=1.5, stroke_opacity=0.6)
        self.play(FadeIn(header), FadeIn(header_rule), run_time=0.6)

        # --- Body rows (build fast, in two quick batches) -------------------
        pick_cells = []   # (row_bg, p_cell, accent, y)
        row_builders = []
        for i, (scenario, pick, accent, why) in enumerate(rows_data):
            ry = header_y - (i + 1) * ROW_H

            row_bg = RoundedRectangle(
                corner_radius=0.08,
                width=COL_W["pick"], height=ROW_H - 0.1,
                stroke_color=accent, stroke_width=1.5, stroke_opacity=0.35,
                fill_color=accent, fill_opacity=0.06,
            )
            row_bg.move_to([COL_X["pick"], ry, 0])

            s_cell = cell_text(scenario, INK, 0.3)
            s_cell.move_to([COL_X["scenario"], ry, 0])
            s_cell.align_to([COL_X["scenario"] - COL_W["scenario"] / 2 + 0.1,
                             ry, 0], LEFT)

            p_cell = cell_text(pick, accent, 0.36, weight="BOLD")
            p_cell.move_to([COL_X["pick"], ry, 0])

            w_cell = cell_text(why, SECOND, 0.28)
            w_cell.move_to([COL_X["why"], ry, 0])

            pick_cells.append((row_bg, p_cell, accent, ry))
            row_builders.append(
                [FadeIn(row_bg), FadeIn(s_cell, shift=RIGHT * 0.2),
                 FadeIn(p_cell), FadeIn(w_cell, shift=LEFT * 0.2)]
            )

        # Pop rows in snappy pairs (~2.4s for all six rows).
        for i in range(0, len(row_builders), 2):
            anims = []
            for b in row_builders[i:i + 2]:
                anims.extend(b)
            self.play(*anims, lag_ratio=0.1, run_time=0.8)
        # Full table on screen by ~5s.

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # A glowing bar slides endlessly down the PICK column. Each pick chip
        # flares (brighter stroke + scale) as the bar passes, and a bright
        # shimmer sweeps left-to-right across the header labels on a loop.
        # =====================================================================
        t = ValueTracker(0.0)

        ys = np.array([pc[3] for pc in pick_cells])
        y_hi, y_lo = ys[0], ys[-1]
        pick_w = COL_W["pick"]

        # Travelling highlight bar.
        hl = RoundedRectangle(
            corner_radius=0.08, width=pick_w + 0.12, height=ROW_H - 0.04,
            stroke_color=INK, stroke_width=2.5, stroke_opacity=0.0,
            fill_color=INK, fill_opacity=0.0,
        )
        hl.move_to([COL_X["pick"], y_hi, 0])

        sweep_period = 3.2  # seconds for the bar to travel top->bottom

        def hl_upd(m):
            # Triangle wave 0..1..0 so it sweeps down then back up forever.
            phase = (t.get_value() / sweep_period) % 2.0
            frac = phase if phase <= 1.0 else 2.0 - phase
            frac = rate_functions.ease_in_out_sine(frac)
            y = y_hi * (1 - frac) + y_lo * frac
            m.move_to([COL_X["pick"], y, 0])
            m.set_stroke(opacity=0.55)
            m.set_fill(opacity=0.08)
        hl.add_updater(hl_upd)
        self.add(hl)

        # Each pick chip + its bg flares as the travelling bar passes its row.
        for row_bg, p_cell, accent, ry in pick_cells:
            bw = p_cell.width
            bh = p_cell.height
            center = p_cell.get_center().copy()

            def make_simple(row_bg=row_bg, p_cell=p_cell, ry=ry,
                            bw=bw, bh=bh, center=center):
                def _upd(_m):
                    phase = (t.get_value() / sweep_period) % 2.0
                    frac = phase if phase <= 1.0 else 2.0 - phase
                    frac = rate_functions.ease_in_out_sine(frac)
                    bar_y = y_hi * (1 - frac) + y_lo * frac
                    prox = max(0.0, 1.0 - abs(bar_y - ry) / (ROW_H * 0.9))
                    row_bg.set_fill(opacity=0.06 + 0.22 * prox)
                    row_bg.set_stroke(opacity=0.35 + 0.5 * prox)
                    s = 1.0 + 0.12 * prox
                    p_cell.set_width(bw * s)
                    p_cell.move_to(center)
                return _upd

            row_bg.add_updater(make_simple())

        # Header shimmer: a bright token slides across SCENARIO/PICK/WHY.
        head_keys = ["scenario", "pick", "why"]
        head_xs = np.array([COL_X[k] for k in head_keys])

        def make_head_upd(key, x):
            def _upd(m):
                sweep_x = -7.0 + ((t.get_value() * 3.5) % 14.0)
                prox = max(0.0, 1.0 - abs(sweep_x - x) / 3.0)
                # Flare ink brightness via opacity + stroke glint.
                m.set_opacity(0.75 + 0.25 * prox)
            return _upd
        for k in head_keys:
            header_cells[k].add_updater(make_head_upd(k, COL_X[k]))

        header_rule.add_updater(
            lambda m: m.set_stroke(
                opacity=0.4 + 0.3 * (0.5 + 0.5 * np.sin(2.4 * t.get_value()))
            )
        )

        # Drive ~18s of unbroken sweeping motion.
        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
