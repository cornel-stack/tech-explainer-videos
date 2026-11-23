"""Scene: Hype vs reality — promised vs real 5G speed.

Class `Slower` (~18s). A big speedometer with a PROMISED needle pinned at
"2 Gbps" (ghostly) and a REAL needle wobbling down at "~200 Mbps". A phone's
"5G" icon is revealed to be low-band (a tag "= 4G+"). A callout "'5G E' =
just 4G". A bar chart: promised ~2000 vs typical ~200 Mbps, the gap shaded
CORAL. Caption: "the icon lies — most '5G' is mid/low-band".

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
    Rectangle,
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


class Slower(Scene):
    def construct(self):
        title = Text("Hype vs reality", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- big speedometer (left) -----------------------------------------
        gauge_c = np.array([-3.6, -0.4, 0.0])
        R = 2.1
        arc = Arc(radius=R, start_angle=PI, angle=-PI, arc_center=gauge_c,
                  stroke_color=SECOND, stroke_width=5)
        lo_lbl = Text("0", font=MONO, color=SECOND).scale(0.3)
        lo_lbl.next_to(arc.get_start(), LEFT, buff=0.15)
        hi_lbl = Text("2 Gbps", font=MONO, color=SECOND).scale(0.3)
        hi_lbl.next_to(arc.get_end(), RIGHT, buff=0.15)

        # promised needle (ghostly, pinned near max)
        prom_frac = 0.92
        prom_ang = PI - prom_frac * PI
        prom_tip = gauge_c + np.array([np.cos(prom_ang),
                                       np.sin(prom_ang), 0]) * R * 0.9
        prom_needle = Line(gauge_c, prom_tip, stroke_color=SILVER,
                           stroke_width=4, stroke_opacity=0.35)
        prom_lbl = Text("PROMISED  2 Gbps", font=MONO, color=SILVER).scale(0.26)
        prom_lbl.move_to(gauge_c + UP * 1.2 + RIGHT * 1.4)
        prom_lbl.set_opacity(0.4)

        # real needle (wobbles low)
        real_needle = Line(gauge_c, gauge_c + RIGHT * R * 0.9,
                           stroke_color=CORAL, stroke_width=6)
        real_lbl = Text("REAL  ~200 Mbps", font=MONO, color=CORAL,
                        weight="BOLD").scale(0.28)
        real_lbl.move_to(gauge_c + DOWN * 1.0 + RIGHT * 1.5)
        hub = Dot(gauge_c, color=INK, radius=0.08)

        self.play(Create(arc), FadeIn(lo_lbl), FadeIn(hi_lbl),
                  Create(prom_needle), FadeIn(prom_lbl),
                  Create(real_needle), FadeIn(real_lbl), FadeIn(hub),
                  run_time=1.0)

        # --- phone "5G" icon revealed as low-band (right-top) ---------------
        phone = RoundedRectangle(corner_radius=0.16, width=1.4, height=2.5,
                                 stroke_color=SILVER, stroke_width=2.5,
                                 fill_color="#111318", fill_opacity=0.9)
        phone.move_to([2.7, 1.1, 0])
        icon = Text("5G", font=MONO, color=GREEN, weight="BOLD").scale(0.6)
        icon.move_to(phone.get_top() + DOWN * 0.5)
        tag = Text("= 4G+", font=MONO, color=AMBER, weight="BOLD").scale(0.32)
        tag.next_to(icon, DOWN, buff=0.2)
        callout = Text("'5G E' = just 4G", font=HEAD, color=CORAL,
                       weight="SEMIBOLD").scale(0.36)
        callout.next_to(phone, RIGHT, buff=0.4)
        self.play(FadeIn(phone), FadeIn(icon), run_time=0.6)
        self.play(FadeIn(tag, shift=UP * 0.2), FadeIn(callout), run_time=0.6)

        # --- bar chart (right-bottom): promised vs typical ------------------
        base_y = -2.2
        bar_x = 1.6
        max_h = 1.9
        # promised ~2000, typical ~200 -> heights
        prom_h = max_h
        typ_h = max_h * (200 / 2000)
        prom_bar = Rectangle(width=0.7, height=prom_h, stroke_width=0,
                             fill_color=SILVER, fill_opacity=0.35)
        prom_bar.move_to([bar_x, base_y + prom_h / 2, 0])
        typ_bar = Rectangle(width=0.7, height=typ_h, stroke_width=0,
                            fill_color=GREEN, fill_opacity=0.9)
        typ_bar.move_to([bar_x + 1.2, base_y + typ_h / 2, 0])
        # gap shading (coral) above typical, up to promised
        gap = Rectangle(width=0.7, height=prom_h - typ_h, stroke_width=0,
                        fill_color=CORAL, fill_opacity=0.3)
        gap.move_to([bar_x + 1.2, base_y + typ_h + (prom_h - typ_h) / 2, 0])
        p_lbl = Text("promised\n~2000", font=MONO, color=SILVER).scale(0.22)
        p_lbl.next_to(prom_bar, DOWN, buff=0.12)
        ty_lbl = Text("typical\n~200", font=MONO, color=GREEN).scale(0.22)
        ty_lbl.next_to(typ_bar, DOWN, buff=0.12).align_to(p_lbl, UP)
        self.play(FadeIn(prom_bar), FadeIn(typ_bar), FadeIn(gap),
                  FadeIn(p_lbl), FadeIn(ty_lbl), run_time=0.9)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # real needle wobbles down low (~0.1 frac) with jitter
        def real_upd(m):
            tt = t.get_value()
            frac = 0.12 + 0.05 * (0.5 + 0.5 * np.sin(3.0 * tt)) \
                + 0.02 * np.sin(7.0 * tt)
            ang = PI - frac * PI
            tip = gauge_c + np.array([np.cos(ang), np.sin(ang), 0]) * R * 0.9
            m.put_start_and_end_on(gauge_c, tip)
        real_needle.add_updater(real_upd)

        # promised needle ghost flickers faintly
        def prom_upd(m):
            m.set_stroke(opacity=0.2 + 0.2 * (0.5 + 0.5 *
                         np.sin(1.5 * t.get_value())))
        prom_needle.add_updater(prom_upd)

        # the gap pulses coral
        def gap_upd(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            m.set_fill(CORAL, opacity=0.2 + 0.3 * s)
        gap.add_updater(gap_upd)

        # tag and callout pulse
        def tag_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.6 * t.get_value())))
        tag.add_updater(tag_upd)

        def call_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + 1.0)
            c = interpolate_color(ManimColor(CORAL), ManimColor(AMBER), s)
            m.set_color(c)
        callout.add_updater(call_upd)

        # 5G icon flickers suspiciously
        def icon_upd(m):
            s = 0.5 + 0.5 * np.sin(4.0 * t.get_value())
            c = interpolate_color(ManimColor(GREEN), ManimColor(AMBER), s)
            m.set_color(c)
        icon.add_updater(icon_upd)

        # caption
        cap = Text("the icon lies — most '5G' is mid/low-band", font=HEAD,
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
