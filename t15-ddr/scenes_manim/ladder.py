"""Scene: the DDR SPEED LADDER — DDR1 -> DDR5 as five climbing rungs.

Class `Ladder` (~20s). Five rungs climb up-and-right, one per generation.
Each rung shows its name (DDR1..DDR5), year, a BANDWIDTH bar that grows each
generation (~3 -> 8 -> 17 -> 25 -> 50+ GB/s, each roughly doubling), and a
VOLTAGE value that drops each generation (2.5 -> 1.8 -> 1.5 -> 1.2 -> 1.1 V).
A climbing marker ascends the rungs on a loop (driven by t); as it reaches a
rung, that rung brightens, its bandwidth bar fills, and the voltage ticks down.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze. Legible enough to sit faintly behind the
intro title.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Dot,
    Line,
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


class Ladder(Scene):
    def construct(self):
        # Per-generation data: name, year, bandwidth GB/s, voltage V, accent.
        gens = [
            ("DDR1", "2000", 3.2, 2.5, VIOLET),
            ("DDR2", "2003", 8.0, 1.8, TEAL),
            ("DDR3", "2007", 17.0, 1.5, AMBER),
            ("DDR4", "2014", 25.6, 1.2, GOLD),
            ("DDR5", "2020", 51.2, 1.1, GREEN),
        ]
        n = len(gens)
        max_bw = 51.2

        title = Text("The DDR speed ladder", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- geometry: rungs climb up-and-right ------------------------------
        x0, x_step = -5.6, 1.35
        y0, y_step = -2.55, 1.05
        rung_positions = [
            np.array([x0 + i * x_step, y0 + i * y_step, 0]) for i in range(n)
        ]

        # Faint guide rail connecting rung anchors.
        rail = VGroup()
        for i in range(n - 1):
            seg = Line(rung_positions[i], rung_positions[i + 1],
                       stroke_color=SECOND, stroke_width=2, stroke_opacity=0.25)
            rail.add(seg)
        self.play(Create(rail), run_time=0.6)

        # --- build each rung -------------------------------------------------
        rungs = []        # list of dicts of mobjects per generation
        bar_w = 3.0       # full-scale bandwidth bar width
        bar_h = 0.26

        for i, (name, year, bw, volt, accent) in enumerate(gens):
            anchor = rung_positions[i]

            plate = RoundedRectangle(
                corner_radius=0.08, width=1.5, height=0.62,
                stroke_color=accent, stroke_width=2.5,
                fill_color=BG, fill_opacity=0.9,
            ).move_to(anchor)

            name_lbl = Text(name, font=MONO, color=accent,
                            weight="BOLD").scale(0.3)
            name_lbl.move_to(plate.get_center() + UP * 0.1)
            year_lbl = Text(year, font=MONO, color=SECOND).scale(0.2)
            year_lbl.move_to(plate.get_center() + DOWN * 0.14)

            # Bandwidth bar: track + fill, anchored to the right of the plate.
            track = Rectangle(
                width=bar_w, height=bar_h,
                stroke_color=SECOND, stroke_width=1.5, stroke_opacity=0.5,
                fill_color=BG, fill_opacity=0.6,
            )
            track.next_to(plate, RIGHT, buff=0.22)
            track_left = track.get_left()

            full_frac = bw / max_bw
            fill = Rectangle(
                width=max(0.001, bar_w * full_frac), height=bar_h - 0.06,
                stroke_width=0, fill_color=accent, fill_opacity=0.9,
            )
            fill.move_to(track_left + RIGHT * (bar_w * full_frac) / 2.0)

            bw_lbl = Text(f"{bw:.1f} GB/s", font=MONO, color=accent).scale(0.2)
            bw_lbl.next_to(track, RIGHT, buff=0.18)

            volt_lbl = Text(f"{volt:.1f} V", font=MONO, color=SILVER).scale(0.2)
            volt_lbl.next_to(bw_lbl, RIGHT, buff=0.3)

            rungs.append({
                "accent": accent,
                "plate": plate,
                "name": name_lbl,
                "year": year_lbl,
                "track": track,
                "fill": fill,
                "track_left": np.array(track_left),
                "full_frac": full_frac,
                "bw": bw_lbl,
                "volt": volt_lbl,
                "anchor": anchor,
            })

        all_build = []
        for r in rungs:
            all_build += [r["plate"], r["name"], r["year"], r["track"],
                          r["fill"], r["bw"], r["volt"]]
        self.play(*[GrowFromCenter(r["plate"]) for r in rungs],
                  lag_ratio=0.12, run_time=1.0)
        self.play(
            *[FadeIn(m) for r in rungs
              for m in (r["name"], r["year"], r["track"], r["bw"], r["volt"])],
            lag_ratio=0.02, run_time=0.8,
        )
        self.add(*[r["fill"] for r in rungs])

        # --- climbing marker -------------------------------------------------
        marker = Dot(color=INK, radius=0.13)
        marker.move_to(rung_positions[0])
        glow = Dot(color=INK, radius=0.26)
        glow.set_opacity(0.0)
        self.add(glow, marker)

        caption = Text("each generation ≈ doubles bandwidth and drops voltage",
                       font=HEAD, color=SECOND).scale(0.34)
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        LOOP = 10.0           # seconds per full climb loop
        per_rung = LOOP / n   # time budget per rung segment

        def climb_phase():
            """Return (seg_index, local_fraction) of the climbing marker."""
            tt = t.get_value() % LOOP
            seg = int(tt // per_rung)
            seg = min(seg, n - 1)
            frac = (tt - seg * per_rung) / per_rung
            return seg, frac

        # Marker climbs the rail, snapping onto each rung anchor.
        def marker_upd(m):
            seg, frac = climb_phase()
            a = rung_positions[seg]
            if seg < n - 1:
                b = rung_positions[seg + 1]
                eased = rate_functions.ease_in_out_quad(frac)
                pos = a * (1 - eased) + b * eased
            else:
                pos = a
            m.move_to(pos)
        marker.add_updater(marker_upd)

        def glow_upd(m):
            seg, frac = climb_phase()
            a = rung_positions[seg]
            if seg < n - 1:
                b = rung_positions[seg + 1]
                eased = rate_functions.ease_in_out_quad(frac)
                pos = a * (1 - eased) + b * eased
            else:
                pos = a
            m.move_to(pos)
            pulse = 0.5 + 0.5 * np.sin(t.get_value() * 4.0)
            m.set_opacity(0.15 + 0.2 * pulse)
        glow.add_updater(glow_upd)

        def reached(i):
            """How fully rung i has been 'reached' by the climbing marker."""
            tt = t.get_value() % LOOP
            arrive = i * per_rung
            if tt < arrive:
                return 0.0
            # fade-in over the first 0.4s after arrival.
            return float(np.clip((tt - arrive) / 0.4, 0.0, 1.0))

        # Each rung brightens as reached; plate stroke + name opacity respond.
        for i, r in enumerate(rungs):
            accent_c = ManimColor(r["accent"])
            dim_c = ManimColor(SECOND)

            def make_plate_upd(rr, ac, dc, idx):
                def _upd(m):
                    amt = reached(idx)
                    base = 0.35 + 0.65 * amt
                    pulse = 0.5 + 0.5 * np.sin(t.get_value() * 3.0 + idx)
                    op = base * (0.85 + 0.15 * pulse)
                    m.set_stroke(opacity=float(np.clip(op, 0.0, 1.0)))
                    col = interpolate_color(dc, ac, amt)
                    m.set_stroke(color=col)
                return _upd
            r["plate"].add_updater(make_plate_upd(r, accent_c, dim_c, i))

            def make_name_upd(idx):
                def _upd(m):
                    amt = reached(idx)
                    m.set_opacity(0.4 + 0.6 * amt)
                return _upd
            r["name"].add_updater(make_name_upd(i))
            r["year"].add_updater(make_name_upd(i))

        # Bandwidth bar fills as its rung is reached, then pulses.
        for i, r in enumerate(rungs):
            full_frac = r["full_frac"]
            track_left = r["track_left"]

            def make_fill_upd(ff, tl, idx):
                def _upd(m):
                    amt = reached(idx)
                    pulse = 0.5 + 0.5 * np.sin(t.get_value() * 2.6 + idx * 0.7)
                    grow = amt * (0.92 + 0.08 * pulse)
                    w = max(0.001, bar_w * ff * grow)
                    m.set(width=w)
                    m.move_to(tl + RIGHT * (w / 2.0))
                    m.set_opacity(0.35 + 0.6 * amt)
                return _upd
            r["fill"].add_updater(make_fill_upd(full_frac, track_left, i))

            def make_bw_upd(idx):
                def _upd(m):
                    amt = reached(idx)
                    m.set_opacity(0.3 + 0.7 * amt)
                return _upd
            r["bw"].add_updater(make_bw_upd(i))

        # Voltage ticks down: brightens (coral->silver) as rung reached.
        for i, r in enumerate(rungs):
            drop_c = ManimColor(GREEN)
            hi_c = ManimColor(CORAL)

            def make_volt_upd(idx):
                def _upd(m):
                    amt = reached(idx)
                    # low-generation voltages run hot (coral), later cool (green)
                    base_warm = idx / (n - 1)  # 0 for DDR1 .. 1 for DDR5
                    col = interpolate_color(hi_c, drop_c, base_warm)
                    m.set_color(col)
                    m.set_opacity(0.3 + 0.7 * amt)
                return _upd
            r["volt"].add_updater(make_volt_upd(i))

        # Running read-out under the title: which generation is active.
        active = Text("DDR1  ↑", font=MONO, color=INK).scale(0.3)
        active.next_to(title, DOWN, buff=0.14)
        active._idx = -1

        def active_upd(m):
            seg, _ = climb_phase()
            if seg != m._idx:
                m._idx = seg
                name, year, bw, volt, accent = gens[seg]
                new = Text(f"{name}  ·  {bw:.1f} GB/s  ·  {volt:.1f} V",
                           font=MONO, color=accent).scale(0.3)
                new.move_to(m.get_center())
                m.become(new)
        active.add_updater(active_upd)
        self.add(active)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
