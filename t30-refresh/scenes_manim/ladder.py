"""Scene: THE REFRESH LADDER — smoothness comparison + a ladder of rates.

Class `Ladder` (~20s). LEFT a stack of 3-4 horizontal tracks, each with a dot
moving left->right at a different update granularity. Each dot is snapped to a
grid of 1/rate steps from the master t, so 60Hz visibly strobes in coarse jumps
while 240Hz glides nearly continuously. Each track is labelled with its Hz and
frame time (16.7ms / 8.3ms / 4.2ms). RIGHT a vertical bar ladder of refresh
rates (60/75/120/144/240/360/540) growing taller, tinted SILVER->GREEN->GOLD,
with a highlight sweeping up and a "diminishing returns" bracket near the top.

Dark palette only, TEXT labels only, continuous motion from a master
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
    interpolate_color,
    FadeIn,
    Create,
    GrowFromEdge,
    LEFT,
    RIGHT,
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


class Ladder(Scene):
    def construct(self):
        title = Text("REFRESH RATES", font=HEAD, color=INK,
                     weight="BOLD").scale(0.8)
        title.to_edge(UP, buff=0.35)
        sub = Text("more updates per second = smoother motion",
                   font=MONO, color=SECOND).scale(0.3)
        sub.next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.3)

        # =====================================================================
        # LEFT: smoothness comparison tracks
        # =====================================================================
        track_x_left = -6.2
        track_x_right = -0.8
        track_len = track_x_right - track_x_left
        track_defs = [
            (60.0, "60 Hz", "16.7 ms", SILVER),
            (120.0, "120 Hz", "8.3 ms", GREEN),
            (240.0, "240 Hz", "4.2 ms", GOLD),
        ]
        track_ys = [1.4, -0.1, -1.6]

        tracks = VGroup()
        track_dots = []
        for (rate, hz, ft, col), ty in zip(track_defs, track_ys):
            rail = Line(
                [track_x_left, ty, 0], [track_x_right, ty, 0],
                stroke_color=SECOND, stroke_width=2, stroke_opacity=0.5,
            )
            # Tick marks hint at the update grid density of this rate.
            ticks = VGroup()
            n_ticks = int(round(rate / 10.0))
            for i in range(n_ticks + 1):
                fx = i / n_ticks
                tx = track_x_left + fx * track_len
                tk = Line([tx, ty - 0.08, 0], [tx, ty + 0.08, 0],
                          stroke_color=col, stroke_width=1.2,
                          stroke_opacity=0.22)
                ticks.add(tk)
            dot = Dot([track_x_left, ty, 0], color=col, radius=0.13)
            trail = VGroup()
            for j in range(6):
                td = Dot([track_x_left, ty, 0], color=col,
                         radius=0.13 - 0.012 * j)
                td.set_opacity(0.0)
                trail.add(td)
            lbl = Text(hz, font=MONO, color=col, weight="BOLD").scale(0.34)
            lbl.next_to(rail, LEFT, buff=0.3).shift(UP * 0.0)
            ftlbl = Text(ft, font=MONO, color=SECOND).scale(0.26)
            ftlbl.next_to(lbl, DOWN, buff=0.08)
            tracks.add(VGroup(rail, ticks, trail, dot, lbl, ftlbl))
            track_dots.append((dot, trail, rate, col, ty))

        self.play(*[Create(tr[0]) for tr in tracks],
                  *[FadeIn(tr[1]) for tr in tracks],
                  *[FadeIn(tr[4]) for tr in tracks],
                  *[FadeIn(tr[5]) for tr in tracks],
                  run_time=0.9)
        self.add(tracks)

        # =====================================================================
        # RIGHT: vertical bar ladder of refresh rates
        # =====================================================================
        rates = [60, 75, 120, 144, 240, 360, 540]
        base_x = 2.4
        base_y = -2.0
        bar_w = 0.52
        bar_gap = 0.66
        max_h = 4.2
        max_rate = max(rates)

        bars = VGroup()
        bar_meta = []
        for i, r in enumerate(rates):
            h = max_h * (r / max_rate)
            frac = i / (len(rates) - 1)
            if frac < 0.5:
                col = interpolate_color(ManimColor(SILVER), ManimColor(GREEN),
                                        frac / 0.5)
            else:
                col = interpolate_color(ManimColor(GREEN), ManimColor(GOLD),
                                        (frac - 0.5) / 0.5)
            bx = base_x + i * bar_gap
            bar = Rectangle(width=bar_w, height=h,
                            stroke_color=col, stroke_width=2,
                            fill_color=col, fill_opacity=0.28)
            bar.move_to([bx, base_y + h / 2.0, 0])
            rlbl = Text(str(r), font=MONO, color=col).scale(0.26)
            rlbl.next_to(bar, UP, buff=0.1)
            hzlbl = Text("Hz", font=MONO, color=SECOND).scale(0.18)
            hzlbl.next_to(bar, DOWN, buff=0.1)
            bars.add(VGroup(bar, rlbl, hzlbl))
            bar_meta.append((bar, col, bx, h))

        self.play(*[GrowFromEdge(bm[0][0], DOWN) for bm in
                    [(VGroup(b[0]),) for b in bars]],
                  run_time=0.9, lag_ratio=0.08)
        self.play(*[FadeIn(b[1]) for b in bars],
                  *[FadeIn(b[2]) for b in bars], run_time=0.4)

        # Diminishing returns bracket near the top bars (240/360/540).
        br_left_x = base_x + 4 * bar_gap - bar_w * 0.6
        br_right_x = base_x + 6 * bar_gap + bar_w * 0.6
        br_y = base_y + max_h + 0.55
        bracket = VGroup(
            Line([br_left_x, br_y - 0.12, 0], [br_left_x, br_y, 0],
                 stroke_color=CORAL, stroke_width=2),
            Line([br_left_x, br_y, 0], [br_right_x, br_y, 0],
                 stroke_color=CORAL, stroke_width=2),
            Line([br_right_x, br_y, 0], [br_right_x, br_y - 0.12, 0],
                 stroke_color=CORAL, stroke_width=2),
        )
        dim_lbl = Text("diminishing returns", font=MONO, color=CORAL).scale(0.24)
        dim_lbl.next_to(bracket, UP, buff=0.08)
        self.play(Create(bracket), FadeIn(dim_lbl), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # --- smoothness tracks: snap each dot to a 1/rate step grid ----------
        # We scale real refresh to a visible sweep: one left->right pass every
        # SWEEP seconds. Steps per sweep = rate / SCALE, so 60Hz strobes and
        # 240Hz glides.
        SWEEP = 2.0
        SCALE = 12.0  # compress real Hz into a visible number of steps

        def make_track_upd(dot, trail, rate, col, ty):
            steps = max(1, int(round(rate / SCALE)))
            td_list = list(trail)

            def _upd(m):
                tt = t.get_value()
                raw = (tt % SWEEP) / SWEEP  # 0..1 continuous sweep progress
                # Snap to this rate's discrete update grid.
                snapped = np.floor(raw * steps) / steps
                x = track_x_left + snapped * track_len
                dot.move_to([x, ty, 0])
                # Motion-blur style trail: samples just behind current step.
                for j, td in enumerate(td_list):
                    back = (snapped - (j + 1) * (1.0 / steps))
                    back = max(back, 0.0)
                    bx = track_x_left + back * track_len
                    td.move_to([bx, ty, 0])
                    td.set_opacity(max(0.0, 0.35 - 0.05 * j))
            return _upd

        for dot, trail, rate, col, ty in track_dots:
            dot.add_updater(make_track_upd(dot, trail, rate, col, ty))

        # --- bar ladder: highlight sweeping up + gentle bar breathing --------
        def make_bar_upd(bar, col, idx, h):
            base_op = 0.28

            def _upd(m):
                tt = t.get_value()
                # A highlight band climbs the ladder over time.
                pos = (tt * 1.2) % (len(rates) + 2)
                d = abs(pos - idx)
                boost = max(0.0, 1.0 - d / 1.2)
                bar.set_fill(opacity=base_op + 0.5 * boost)
                bar.set_stroke(width=2 + 3 * boost)
            return _upd

        for i, (bar, col, bx, h) in enumerate(bar_meta):
            bar.add_updater(make_bar_upd(bar, col, i, h))

        # Sub-caption pulses to keep life in the lower band.
        verdict = Text("the eye's smoothness gains shrink past ~240 Hz",
                       font=MONO, color=SECOND).scale(0.26)
        verdict.to_edge(DOWN, buff=0.28)

        def verdict_upd(m):
            m.set_opacity(0.5 + 0.4 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 1.4)))
        verdict.add_updater(verdict_upd)
        self.add(verdict)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
