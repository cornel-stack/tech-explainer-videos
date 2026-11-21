"""Scene: generation beats tier.

Class `GenTier` (~24s). Two horizontal performance bars: a "14th-gen i3"
drawn slightly LONGER than a "10th-gen i5", making the point that a newer
low tier can out-run an older higher tier. The bars grow, then shimmer with a
travelling highlight; a label reads "newer generation > higher tier". Marked
"illustrative — not exact benchmark". Motion is continuous throughout.

Silicon-dark palette (no pure blue, no white). IP-safe: TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  teal #2DD4BF (i3)  green #35E08A (i5)  amber #FFB020  gold #E8C24A
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Line,
    ValueTracker,
    config,
    FadeIn,
    GrowFromEdge,
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
TEAL = "#2DD4BF"
GREEN = "#35E08A"
AMBER = "#FFB020"
GOLD = "#E8C24A"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class GenTier(Scene):
    def construct(self):
        # --- Title -----------------------------------------------------------
        title = Text("Generation beats tier", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.64)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- Track geometry --------------------------------------------------
        track_x = -4.6          # left origin of both bars
        max_len = 8.4           # full-scale track length
        bar_h = 0.95

        # Illustrative performance fractions (NOT a real benchmark):
        # the newer i3 edges out the older i5.
        i3_frac = 0.82          # 14th-gen i3
        i5_frac = 0.70          # 10th-gen i5

        def make_track(y):
            return Line([track_x, y, 0], [track_x + max_len, y, 0],
                        color=SECOND, stroke_width=1.5, stroke_opacity=0.4)

        y_top = 1.15
        y_bot = -1.15
        track_top = make_track(y_top)
        track_bot = make_track(y_bot)

        def make_bar(y, frac, accent):
            length = max_len * frac
            bar = RoundedRectangle(
                corner_radius=0.12, width=length, height=bar_h,
                stroke_color=accent, stroke_width=2.5,
                fill_color=accent, fill_opacity=0.22,
            )
            # Left-align the bar to the track origin.
            bar.move_to([track_x + length / 2, y, 0])
            glow = RoundedRectangle(
                corner_radius=0.12, width=length, height=bar_h,
                stroke_color=accent, stroke_width=11, stroke_opacity=0.14,
                fill_opacity=0,
            ).move_to(bar)
            grp = VGroup(glow, bar)
            grp.bar = bar
            grp.glow = glow
            grp.accent = accent
            grp.length = length
            grp.y = y
            return grp

        bar_i3 = make_bar(y_top, i3_frac, TEAL)
        bar_i5 = make_bar(y_bot, i5_frac, GREEN)

        # Labels at the left of each bar.
        lbl_i3 = Text("14th-gen  i3", font=MONO, color=TEAL,
                      weight="BOLD").scale(0.4)
        lbl_i3.next_to([track_x, y_top, 0], UP, buff=0.14).align_to(
            [track_x, 0, 0], LEFT)
        lbl_i5 = Text("10th-gen  i5", font=MONO, color=GREEN,
                      weight="BOLD").scale(0.4)
        lbl_i5.next_to([track_x, y_bot, 0], DOWN, buff=0.14).align_to(
            [track_x, 0, 0], LEFT)

        # --- Build: tracks, labels, then bars grow from their left edge -----
        self.play(FadeIn(track_top), FadeIn(track_bot),
                  FadeIn(lbl_i3), FadeIn(lbl_i5), run_time=0.6)
        self.play(
            GrowFromEdge(bar_i3, LEFT),
            GrowFromEdge(bar_i5, LEFT),
            run_time=1.3,
            rate_func=rate_functions.ease_out_cubic,
        )

        # --- Verdict label ---------------------------------------------------
        verdict = Text("newer generation  >  higher tier", font=HEAD,
                       color=INK, weight="SEMIBOLD").scale(0.44)
        verdict.to_edge(DOWN, buff=0.9)
        self.play(FadeIn(verdict, shift=UP * 0.2), run_time=0.6)

        disclaimer = Text("illustrative — not exact benchmark", font=MONO,
                          color=SECOND).scale(0.26)
        disclaimer.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(disclaimer), run_time=0.4)
        # Core content on screen (~4.5s in). Leave lots of continuous motion.

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # Bars shimmer: a bright highlight band travels left→right along each
        # bar; the glow breathes; a small "lead" marker sits at the end of the
        # i3 bar and pulses to emphasise that it is ahead; the verdict ">"
        # throbs. A master clock drives all of it.
        # =====================================================================
        t = ValueTracker(0.0)

        # Travelling highlight band for each bar (a thin bright rectangle that
        # sweeps across the filled region, clipped to the bar length).
        def add_shimmer(barobj, speed, offset):
            band = Rectangle(
                width=0.5, height=bar_h - 0.08,
                stroke_width=0, fill_color=INK, fill_opacity=0.0,
            )
            left = track_x
            right = track_x + barobj.length

            def _upd(m):
                frac = ((t.get_value() * speed + offset) % 1.2) / 1.0
                # Sweep slightly beyond so it visibly enters/exits.
                xcur = left + (right - left + 0.5) * np.clip(frac, 0, 1) - 0.25
                m.move_to([np.clip(xcur, left, right), barobj.y, 0])
                # Bright only while inside the bar.
                inside = 1.0 if (left <= xcur <= right) else 0.0
                m.set_fill(opacity=0.22 * inside)
            band.add_updater(_upd)
            self.add(band)
            return band

        add_shimmer(bar_i3, 0.55, 0.0)
        add_shimmer(bar_i5, 0.5, 0.6)

        # Glow breathing on both bars.
        for i, b in enumerate([bar_i3, bar_i5]):
            glow = b.glow

            def make_breath(gl, phase):
                def _upd(m):
                    tt = t.get_value()
                    gl.set_stroke(opacity=0.1 + 0.14 *
                                  (0.5 + 0.5 * np.sin(1.8 * tt + phase)))
                return _upd
            b.add_updater(make_breath(glow, i * 1.4))

        # "lead" marker at the end of the i3 bar.
        lead_x = track_x + bar_i3.length
        lead = Text("ahead", font=MONO, color=TEAL).scale(0.28)
        lead.move_to([lead_x + 0.55, y_top, 0])
        arrow = Line([lead_x + 0.08, y_top, 0], [lead_x + 0.3, y_top, 0],
                     color=TEAL, stroke_width=3)

        def lead_upd(m):
            tt = t.get_value()
            pulse = 0.5 + 0.5 * np.sin(2.6 * tt)
            m.set_opacity(0.5 + 0.5 * pulse)
            m.move_to([lead_x + 0.55 + 0.06 * pulse, y_top, 0])
        lead.add_updater(lead_upd)

        def arrow_upd(m):
            m.set_stroke(opacity=0.4 + 0.5 * (0.5 + 0.5 *
                                              np.sin(2.6 * t.get_value())))
        arrow.add_updater(arrow_upd)
        self.add(lead, arrow)

        # Verdict ">" throb (scale the whole verdict subtly).
        verdict_home = verdict.get_center().copy()
        base_h = verdict.height

        def verdict_upd(m):
            tt = t.get_value()
            s = 1.0 + 0.03 * np.sin(2.0 * tt)
            m.set(height=base_h * s)
            m.move_to(verdict_home)
        verdict.add_updater(verdict_upd)

        # A faint "gap" bracket between the two bar ends, pulsing, to make the
        # difference legible without claiming an exact number.
        gap_top = track_x + bar_i3.length
        gap_bot = track_x + bar_i5.length
        gap_line = Line([gap_bot, y_bot + bar_h / 2, 0],
                        [gap_top, y_top - bar_h / 2, 0],
                        color=GOLD, stroke_width=1.5, stroke_opacity=0.0)

        def gap_upd(m):
            m.set_stroke(opacity=0.15 + 0.2 * (0.5 + 0.5 *
                                               np.sin(1.6 * t.get_value())))
        gap_line.add_updater(gap_upd)
        self.add(gap_line)

        # Drive ~18s of unbroken shimmer.
        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
