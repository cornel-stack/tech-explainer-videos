"""Scene: Exploded-view PC build that assembles, holds, explodes and loops.

Class `Assembly` (~20s). Labelled part rectangles — Motherboard (a larger
board), CPU, RAM, GPU, PSU, SSD, Cooler, Case fans — start spread APART
(exploded) and, driven by a master ValueTracker, slide IN and click into
their seated positions on/around the motherboard inside a Case outline,
forming a complete PC. Then they gently explode back apart and repeat on a
loop. Each part lights GREEN as it seats; parts pulse continuously.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92  green #35E08A  teal #2DD4BF
  violet #B06BFF  amber #FFB020  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    interpolate_color,
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


class Assembly(Scene):
    def construct(self):
        title = Text("Every part — snapped into place", font=HEAD,
                     color=INK, weight="SEMIBOLD").scale(0.5)
        title.to_edge(UP, buff=0.38)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.6)

        # --- Case outline ----------------------------------------------------
        case = RoundedRectangle(
            corner_radius=0.18, width=11.6, height=6.6,
            stroke_color=SILVER, stroke_width=2.0,
            fill_color="#0E0F12", fill_opacity=0.35,
        ).shift(DOWN * 0.3)
        case_lbl = Text("Case", font=MONO, color=SILVER).scale(0.3)
        case_lbl.next_to(case, UP, buff=0.1).align_to(case, UP)
        case_lbl.shift(UP * 0.02)
        self.play(Create(case), run_time=0.7)
        self.add(case_lbl)

        board_center = case.get_center() + np.array([-1.6, 0.0, 0])

        # --- Motherboard (the big board everything seats on) -----------------
        board = RoundedRectangle(
            corner_radius=0.1, width=6.4, height=5.6,
            stroke_color=TEAL, stroke_width=2.2,
            fill_color="#0A1413", fill_opacity=0.55,
        ).move_to(board_center)
        board_lbl = Text("Motherboard", font=MONO, color=TEAL).scale(0.3)
        board_lbl.move_to(board.get_corner(UP) + DOWN * 0.26)

        # Part spec: name, seated size, seated offset (rel board_center),
        # colour, exploded direction (unit-ish vector).
        PARTS = [
            ("CPU",       2.0, 1.4, (-1.0, 1.3),  AMBER,  (-2.6, 2.4)),
            ("Cooler",    2.2, 1.0, (-1.0, 2.35), VIOLET, (-2.2, 3.4)),
            ("RAM",       0.5, 3.4, (1.7, 0.9),   CORAL,  (3.6, 2.6)),
            ("GPU",       4.6, 1.3, (-0.2, -1.5), GREEN,  (-0.2, -3.6)),
            ("SSD",       1.8, 0.7, (1.9, -1.9),  GOLD,   (3.8, -2.4)),
        ]

        parts = []  # list of dicts

        def make_part(name, w, h, seat_off, col, exp_dir):
            body = RoundedRectangle(
                corner_radius=0.08, width=w, height=h,
                stroke_color=col, stroke_width=2.2,
                fill_color="#101014", fill_opacity=0.92,
            )
            glow = RoundedRectangle(
                corner_radius=0.08, width=w, height=h,
                stroke_color=GREEN, stroke_width=9, stroke_opacity=0.0,
                fill_opacity=0,
            )
            lbl = Text(name, font=MONO, color=col).scale(
                min(0.3, 0.34 * w / max(len(name) * 0.42, 1)))
            grp = VGroup(glow, body, lbl)
            seat = board_center + np.array([seat_off[0], seat_off[1], 0])
            d = np.array([exp_dir[0], exp_dir[1], 0])
            n = np.linalg.norm(d)
            exploded = case.get_center() + (d / (n if n else 1.0)) * 4.3
            return {
                "grp": grp, "glow": glow, "body": body, "col": col,
                "seat": seat, "exploded": exploded,
            }

        # PSU seats at the bottom of the case (right of board).
        psu = make_part("PSU", 2.6, 1.1, (3.0, -1.95), SILVER, (3.6, -3.6))
        # Case fans along the right edge.
        fans = make_part("Case fans", 0.9, 4.2, (4.1, 0.3), SILVER, (5.4, 0.6))

        for spec in PARTS:
            parts.append(make_part(*spec))
        parts.append(psu)
        parts.append(fans)

        # Reveal board, then all parts at their exploded positions.
        self.play(Create(board), run_time=0.7)
        self.add(board_lbl)
        for p in parts:
            p["grp"].move_to(p["exploded"])
        self.play(*[FadeIn(p["grp"]) for p in parts],
                  lag_ratio=0.05, run_time=1.0)

        caption = Text("exploded view — then every piece clicks home",
                       font=HEAD, color=SECOND).scale(0.3)
        caption.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        GREEN_C = ManimColor(GREEN)
        PERIOD = 10.0  # assemble -> hold -> explode -> hold, then loop.

        # Phase progress -> "seatedness" 0..1 with holds at each end.
        def seatedness(tt, delay):
            cyc = tt % PERIOD
            # 0..3.2 assemble, 3.2..5.0 hold seated, 5.0..8.2 explode,
            # 8.2..10 hold exploded.
            local = cyc - delay
            if local <= 0.0:
                return 0.0
            if local < 3.2:
                return rate_functions.ease_in_out_quad(
                    np.clip(local / 3.2, 0.0, 1.0))
            if cyc < 5.0:
                return 1.0
            if cyc < 8.2:
                return rate_functions.ease_in_out_quad(
                    1.0 - np.clip((cyc - 5.0) / 3.2, 0.0, 1.0))
            return 0.0

        def make_part_updater(p, delay, phase):
            seat = p["seat"]
            exploded = p["exploded"]
            base_col = ManimColor(p["col"])
            body = p["body"]
            glow = p["glow"]

            def _upd(m):
                tt = t.get_value()
                s = seatedness(tt, delay)
                pos = exploded * (1 - s) + seat * s
                m.move_to(pos)
                # Colour toward green as it seats; a bright click near s==1.
                col = interpolate_color(base_col, GREEN_C, s)
                body.set_stroke(color=col)
                # Seated pulse + a click flash when fully home.
                click = 1.0 if s > 0.985 else 0.0
                breathe = 0.5 + 0.5 * np.sin(2.0 * tt + phase)
                glow.set_stroke(
                    opacity=(0.1 + 0.25 * breathe) * s + 0.35 * click)
            return _upd

        rng = np.random.default_rng(7)
        for i, p in enumerate(parts):
            delay = 0.18 * i
            phase = rng.uniform(0, 6.28)
            p["grp"].add_updater(make_part_updater(p, delay, phase))

        # Board gentle breathe so the whole build feels alive.
        def board_upd(m):
            tt = t.get_value()
            m.set_stroke(opacity=0.7 + 0.3 * (0.5 + 0.5 * np.sin(1.3 * tt)))
        board.add_updater(board_upd)

        # Progress readout.
        status = Text("assembling…", font=MONO, color=GREEN).scale(0.28)
        status.next_to(title, DOWN, buff=0.12)
        status._idx = -1

        def status_upd(m):
            cyc = t.get_value() % PERIOD
            if cyc < 3.2:
                idx, txt, col = 0, "assembling…", GREEN
            elif cyc < 5.0:
                idx, txt, col = 1, "complete PC", GREEN
            elif cyc < 8.2:
                idx, txt, col = 2, "exploding…", AMBER
            else:
                idx, txt, col = 3, "parts laid out", SECOND
            if idx != m._idx:
                m._idx = idx
                new = Text(txt, font=MONO, color=col).scale(0.28)
                new.move_to(m)
                m.become(new)
        status.add_updater(status_upd)
        self.add(status)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
