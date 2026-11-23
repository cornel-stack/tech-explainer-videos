"""Scene: one DRAM cell — a single capacitor + a single transistor, and the
leak/refresh loop that makes it 'dynamic'.

Class `Cell` (~20s). Draw one capacitor (two plates / a little tank) and one
transistor (a gate switch). A charge bar shows the stored bit: full = "1"
(GREEN), empty = "0" (SECOND). The charge visibly drains over ~1.5s, then a
TEAL "REFRESH" pulse tops it back up — forever.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Line,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
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


class Cell(Scene):
    def construct(self):
        title = Text("Inside one cell: a capacitor + a transistor",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- transistor (gate switch) on the left ----------------------------
        gate_box = RoundedRectangle(
            corner_radius=0.1, width=2.0, height=1.6,
            stroke_color=AMBER, stroke_width=2.5,
            fill_color="#17130A", fill_opacity=0.5,
        ).shift(LEFT * 3.4 + DOWN * 0.2)
        gate_lbl = Text("transistor\n(gate switch)", font=MONO,
                        color=AMBER).scale(0.26)
        gate_lbl.move_to(gate_box.get_center())
        wire = Line(gate_box.get_right(),
                    gate_box.get_right() + RIGHT * 1.9,
                    stroke_color=SILVER, stroke_width=3)

        # --- capacitor (tank with two plates) on the right -------------------
        tank_x = 1.0
        tank_y = -0.2
        tank_w = 2.2
        tank_h = 2.4
        tank = RoundedRectangle(
            corner_radius=0.12, width=tank_w, height=tank_h,
            stroke_color=TEAL, stroke_width=2.5,
            fill_color=BG, fill_opacity=0.4,
        ).move_to(np.array([tank_x, tank_y, 0]))
        # two plates framing the tank (capacitor symbol)
        plate_top = Line(
            np.array([tank_x - 0.7, tank_y + tank_h / 2 + 0.25, 0]),
            np.array([tank_x + 0.7, tank_y + tank_h / 2 + 0.25, 0]),
            stroke_color=SILVER, stroke_width=4)
        plate_bot = Line(
            np.array([tank_x - 0.7, tank_y - tank_h / 2 - 0.25, 0]),
            np.array([tank_x + 0.7, tank_y - tank_h / 2 - 0.25, 0]),
            stroke_color=SILVER, stroke_width=4)
        cap_lbl = Text("capacitor", font=MONO, color=TEAL).scale(0.26)
        cap_lbl.next_to(plate_bot, DOWN, buff=0.18)

        # charge fill inside the tank
        base_y = tank_y - tank_h / 2 + 0.06
        charge = Rectangle(
            width=tank_w - 0.16, height=tank_h - 0.12,
            stroke_width=0, fill_color=GREEN, fill_opacity=0.8,
        )
        charge.move_to(np.array([tank_x, tank_y, 0]))

        self.play(Create(gate_box), Create(tank), run_time=0.8)
        self.play(FadeIn(gate_lbl), Create(wire),
                  Create(plate_top), Create(plate_bot),
                  FadeIn(cap_lbl), run_time=0.6)
        self.add(charge)

        # bit readout
        bit = Text("1", font=MONO, color=GREEN, weight="BOLD").scale(0.9)
        bit.next_to(tank, RIGHT, buff=0.9)
        bit_lbl = Text("stored bit", font=MONO, color=SECOND).scale(0.26)
        bit_lbl.next_to(bit, DOWN, buff=0.2)
        self.add(bit, bit_lbl)

        # refresh tag (fades in on pulses)
        refresh_tag = Text("REFRESH", font=MONO, color=TEAL,
                           weight="BOLD").scale(0.4)
        refresh_tag.next_to(title, DOWN, buff=0.25)
        self.add(refresh_tag)

        caption = Text(
            "it leaks in milliseconds -> refreshed thousands of times a "
            "second  (the 'dynamic' in DRAM)",
            font=MONO, color=SECOND).scale(0.28)
        caption.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        full_h = tank_h - 0.12
        full_w = tank_w - 0.16
        cx = tank_x

        # leak/refresh cycle: drain over ~1.5s, snap up (refresh) over ~0.35s.
        period = 1.85
        drain_frac = 1.5 / period

        def level_at(tt):
            p = (tt % period) / period
            if p < drain_frac:
                # drains from 1.0 down to ~0.18
                return 1.0 - (p / drain_frac) * 0.82
            else:
                # refresh pulse tops it back up to 1.0
                r = (p - drain_frac) / (1 - drain_frac)
                return 0.18 + 0.82 * rate_functions.ease_out_quad(r)

        ch = charge

        def charge_upd(m):
            lvl = level_at(t.get_value())
            h = max(full_h * lvl, 0.02)
            m.set(width=full_w, height=h)
            m.move_to(np.array([cx, base_y + h / 2, 0]))
            col = interpolate_color(
                ManimColor(SECOND), ManimColor(GREEN), float(np.clip(lvl, 0, 1)))
            m.set_fill(color=col, opacity=0.85)
        ch.add_updater(charge_upd)

        bm = bit

        def bit_upd(m):
            lvl = level_at(t.get_value())
            if lvl > 0.5:
                new = Text("1", font=MONO, color=GREEN,
                           weight="BOLD").scale(0.9)
            else:
                new = Text("0", font=MONO, color=SECOND,
                           weight="BOLD").scale(0.9)
            new.move_to(m.get_center())
            m.become(new)
        bm.add_updater(bit_upd)

        rt = refresh_tag

        def refresh_upd(m):
            p = (t.get_value() % period) / period
            if p >= drain_frac:
                m.set_opacity(1.0)
            else:
                m.set_opacity(0.0)
        rt.add_updater(refresh_upd)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
