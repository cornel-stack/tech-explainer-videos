"""Scene: Wi-Fi names & frequency bands decoded.

Class `Bands` (~18s). TOP a decoder that maps the 802.11 codenames to the
marketing Wi-Fi N names, rows lighting up in turn. BOTTOM three concentric
coverage rings radiating from a central ROUTER showing the frequency/range
trade-off: 2.4 GHz (largest, GREEN), 5 GHz (medium, TEAL), 6 GHz (smallest,
VIOLET). A signal pulse sweeps outward through the rings while the decoder
rows cycle. Continuous loop driven by a master ValueTracker.

Dark palette only, TEXT labels only. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Circle,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    Arrow,
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
    ORIGIN,
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


class Bands(Scene):
    def construct(self):
        title = Text("NAMES & BANDS, DECODED", font=HEAD, color=INK,
                     weight="BOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # =====================================================================
        # TOP HALF — the name decoder
        # =====================================================================
        # (codename, marketing name, color)
        rows_data = [
            ("802.11n", "Wi-Fi 4", AMBER),
            ("802.11ac", "Wi-Fi 5", TEAL),
            ("802.11ax", "Wi-Fi 6", GREEN),
            ("+6 GHz", "Wi-Fi 6E", VIOLET),
            ("802.11be", "Wi-Fi 7", GOLD),
        ]
        nr = len(rows_data)

        decoder = VGroup()
        row_mobs = []
        for code, name, col in rows_data:
            card = RoundedRectangle(
                corner_radius=0.1, width=5.6, height=0.6,
                stroke_color=col, stroke_width=2,
                fill_color=col, fill_opacity=0.06,
            )
            code_t = Text(code, font=MONO, color=SILVER).scale(0.32)
            code_t.move_to(card.get_left() + RIGHT * 1.25)
            arrow = Arrow(
                start=ORIGIN, end=RIGHT * 0.9, buff=0,
                stroke_width=4, color=col, max_tip_length_to_length_ratio=0.35,
            )
            arrow.move_to(card.get_center())
            name_t = Text(name, font=MONO, color=col, weight="BOLD").scale(0.34)
            name_t.move_to(card.get_right() + LEFT * 1.25)
            g = VGroup(card, code_t, arrow, name_t)
            decoder.add(g)
            row_mobs.append((card, code_t, arrow, name_t, col))
        decoder.arrange(DOWN, buff=0.14)
        decoder.next_to(title, DOWN, buff=0.3).shift(LEFT * 0.0)
        decoder.to_edge(LEFT, buff=0.9)

        for g in decoder:
            self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.22)

        # =====================================================================
        # BOTTOM / RIGHT — coverage rings from a router
        # =====================================================================
        center = np.array([3.4, -1.1, 0])

        # (label, detail, radius, color)
        rings_data = [
            ("2.4 GHz", "far · slow · walls", 2.9, GREEN),
            ("5 GHz", "fast · medium", 1.95, TEAL),
            ("6 GHz", "fastest · short", 1.1, VIOLET),
        ]

        ring_mobs = []
        for label, detail, r, col in rings_data:
            ring = Circle(radius=r, stroke_color=col, stroke_width=2.5,
                          fill_color=col, fill_opacity=0.04)
            ring.move_to(center)
            lbl = Text(label, font=MONO, color=col, weight="BOLD").scale(0.3)
            lbl.move_to(center + UP * r + DOWN * 0.0)
            lbl.shift(UP * 0.02)
            det = Text(detail, font=MONO, color=SECOND).scale(0.2)
            det.next_to(lbl, DOWN, buff=0.06)
            ring_mobs.append((ring, lbl, det, r, col))

        # largest first so inner rings draw on top.
        for ring, lbl, det, r, col in ring_mobs:
            self.play(Create(ring), FadeIn(lbl), FadeIn(det), run_time=0.35)

        router = RoundedRectangle(
            corner_radius=0.08, width=0.75, height=0.5,
            stroke_color=INK, stroke_width=2.5,
            fill_color="#141418", fill_opacity=1.0,
        ).move_to(center)
        router_lbl = Text("ROUTER", font=MONO, color=INK).scale(0.2)
        router_lbl.next_to(router, DOWN, buff=0.1)
        self.play(GrowFromCenter(router), FadeIn(router_lbl), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        cycle = 2.2  # seconds a decoder row stays lit

        # --- decoder rows light up in turn -----------------------------------
        for i in range(nr):
            card, code_t, arrow, name_t, col = row_mobs[i]
            cm = ManimColor(col)
            ink = ManimColor(INK)

            def make_row_upd(r_card, r_name, r_arrow, r_col, r_ink, ri):
                def _upd(m):
                    tt = t.get_value()
                    active = int(tt // cycle) % nr
                    phase = (tt % cycle) / cycle
                    on = 1.0 if active == ri else 0.0
                    # smooth pulse while active
                    pulse = 0.5 + 0.5 * np.sin(phase * np.pi) if on else 0.0
                    r_card.set_fill(opacity=0.06 + 0.3 * pulse)
                    r_card.set_stroke(width=2 + 2.5 * pulse)
                    hot = interpolate_color(r_col, r_ink, 0.5 * pulse)
                    r_name.set_color(hot)
                    r_arrow.set_opacity(0.4 + 0.6 * (0.3 + 0.7 * on))
                return _upd
            card.add_updater(make_row_upd(card, name_t, arrow, cm, ink, i))

        # --- router power light breathing ------------------------------------
        core = Dot(color=GREEN, radius=0.07).move_to(center)

        def core_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 4.0)
            m.scale_to_fit_width(2 * (0.05 + 0.03 * s))
            m.set_opacity(0.5 + 0.5 * s)
        core.add_updater(core_upd)
        self.add(core)

        # --- signal pulses radiating outward through the rings ---------------
        pulse_period = 3.2
        r_max = rings_data[0][2] + 0.25

        def band_color_at(radius):
            """Color a pulse should take based on which ring it is crossing."""
            if radius <= rings_data[2][2]:
                return ManimColor(VIOLET)
            if radius <= rings_data[1][2]:
                return ManimColor(TEAL)
            return ManimColor(GREEN)

        pulses = []
        n_pulses = 3
        for k in range(n_pulses):
            p = Circle(radius=0.1, stroke_color=GREEN, stroke_width=3,
                       fill_opacity=0)
            p.move_to(center)
            pulses.append(p)

        def make_pulse(offset):
            def _upd(m):
                tt = (t.get_value() + offset) % pulse_period
                frac = tt / pulse_period
                radius = 0.1 + frac * r_max
                m.scale_to_fit_width(2 * radius)
                m.move_to(center)
                m.set_stroke(color=band_color_at(radius),
                             opacity=np.clip(1.1 * (1 - frac), 0.0, 0.9))
            return _upd

        for k, p in enumerate(pulses):
            p.add_updater(make_pulse(k * pulse_period / n_pulses))
        self.add(*pulses)

        # --- caption ---------------------------------------------------------
        cap = Text("higher frequency = more data, less range", font=HEAD,
                   color=INK).scale(0.4)
        cap.to_edge(DOWN, buff=0.4)

        def cap_upd(m):
            g = 0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 1.6))
            m.set_opacity(g)
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(15.0), run_time=15.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
