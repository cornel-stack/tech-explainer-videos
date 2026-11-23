"""Scene: The 5G promise — a phone upgrades 4G -> 5G and three promise badges.

Class `Whatis` (~18s). A phone icon swaps its "4G" label for "5G"; three big
promise badges pulse in on a loop: gigabit speed, near-zero lag, a billion
devices. A speedometer needle jumps from a low 4G value toward a huge 5G value.
Caption: "that was the pitch".

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Line,
    Arc,
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
    PI,
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


class Whatis(Scene):
    def construct(self):
        title = Text("The promise of 5G", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- phone on the left ----------------------------------------------
        phone_body = RoundedRectangle(
            corner_radius=0.22, width=2.0, height=3.6,
            stroke_color=SILVER, stroke_width=3,
            fill_color="#111318", fill_opacity=0.9,
        ).shift(LEFT * 4.6 + DOWN * 0.3)
        screen = RoundedRectangle(
            corner_radius=0.12, width=1.6, height=3.0,
            stroke_color=SECOND, stroke_width=1.5,
            fill_color="#0C0E12", fill_opacity=0.9,
        ).move_to(phone_body)
        gen_lbl = Text("4G", font=MONO, color=SECOND, weight="BOLD").scale(0.9)
        gen_lbl.move_to(screen)
        self.play(Create(phone_body), Create(screen), run_time=0.7)
        self.play(FadeIn(gen_lbl), run_time=0.4)

        # upgrade: swap 4G -> 5G
        new_gen = Text("5G", font=MONO, color=GREEN, weight="BOLD").scale(1.0)
        new_gen.move_to(screen)
        self.play(FadeIn(new_gen, shift=UP * 0.3),
                  gen_lbl.animate.set_opacity(0.0).shift(UP * 0.3),
                  run_time=0.7)
        self.remove(gen_lbl)

        # --- three promise badges (right-top) -------------------------------
        promises = [
            ("gigabit speed", GREEN),
            ("= 0 ms lag", TEAL),
            ("1 billion devices", VIOLET),
        ]
        badges = VGroup()
        for txt, col in promises:
            card = RoundedRectangle(
                corner_radius=0.14, width=3.6, height=0.95,
                stroke_color=col, stroke_width=2.5,
                fill_color="#101216", fill_opacity=0.85,
            )
            lbl = Text(txt, font=HEAD, color=col, weight="SEMIBOLD").scale(0.42)
            lbl.move_to(card)
            badges.add(VGroup(card, lbl))
        badges.arrange(DOWN, buff=0.3)
        badges.to_edge(RIGHT, buff=0.9).shift(UP * 0.6)
        self.play(*[GrowFromCenter(b) for b in badges],
                  lag_ratio=0.2, run_time=1.0)

        # --- speedometer (center-bottom) ------------------------------------
        gauge_c = np.array([0.4, -1.9, 0.0])
        R = 1.6
        arc = Arc(radius=R, start_angle=PI, angle=-PI, arc_center=gauge_c,
                  stroke_color=SECOND, stroke_width=5)
        # tick labels
        lo_lbl = Text("4G", font=MONO, color=SECOND).scale(0.3)
        lo_lbl.next_to(arc.get_start(), LEFT, buff=0.15)
        hi_lbl = Text("5G", font=MONO, color=GREEN).scale(0.3)
        hi_lbl.next_to(arc.get_end(), RIGHT, buff=0.15)
        needle = Line(gauge_c, gauge_c + RIGHT * R * 0.9,
                      stroke_color=AMBER, stroke_width=6)
        hub = Dot(gauge_c, color=INK, radius=0.07)
        self.play(Create(arc), FadeIn(lo_lbl), FadeIn(hi_lbl),
                  Create(needle), FadeIn(hub), run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Needle swings from low (4G) toward high (5G) then wobbles near high.
        def needle_upd(m):
            tt = t.get_value()
            # overall ramp 0..1 over first ~6s, then hover high w/ wobble
            ramp = np.clip(tt / 6.0, 0.0, 1.0)
            wobble = 0.05 * np.sin(2.5 * tt)
            frac = np.clip(0.12 + ramp * 0.82 + wobble * ramp, 0.0, 1.0)
            ang = PI - frac * PI  # from PI (left) to 0 (right)
            tip = gauge_c + np.array([np.cos(ang), np.sin(ang), 0.0]) * R * 0.9
            col = interpolate_color(ManimColor(AMBER), ManimColor(GREEN), frac)
            m.put_start_and_end_on(gauge_c, tip)
            m.set_stroke(color=col)
        needle.add_updater(needle_upd)

        # Promise badges pulse on a loop (stagger per index).
        for i, b in enumerate(badges):
            card = b[0]

            def make_pulse(cardm, phase):
                base = cardm.get_stroke_width()

                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.2 * t.get_value() + phase)
                    cardm.set_stroke(width=2.0 + 2.5 * s)
                    cardm.set_fill(opacity=0.7 + 0.2 * s)
                return _upd
            card.add_updater(make_pulse(card, i * 1.5))

        # "5G" screen label breathes.
        def gen_upd(m):
            m.set_opacity(0.75 + 0.25 * (0.5 + 0.5 *
                          np.sin(1.8 * t.get_value())))
        new_gen.add_updater(gen_upd)

        # caption
        cap = Text("that was the pitch", font=HEAD, color=SECOND).scale(0.4)
        cap.to_edge(DOWN, buff=0.4)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.4 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
