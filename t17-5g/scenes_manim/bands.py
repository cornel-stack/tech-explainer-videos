"""Scene: The three 5G bands — range vs speed trade-off.

Class `Bands` (~20s). Three rows, each a small tower, a RANGE RING and a
SPEED BAR. LOW (<1 GHz) huge ring, tiny bar. MID (1-6 GHz) medium ring, long
bar, highlighted GREEN as "the real 5G". HIGH / mmWave (24 GHz+) tiny ring,
massive bar. Range and speed trade off. Caption: "low reaches far · mmWave is
fast but tiny".

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
    Circle,
    Triangle,
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


class Bands(Scene):
    def construct(self):
        title = Text("Three bands, one trade-off", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # rows: (name, freq, ring_radius, bar_len, color, highlight)
        rows = [
            ("LOW-BAND", "< 1 GHz", 1.55, 0.7, VIOLET, False),
            ("MID-BAND", "1 - 6 GHz", 1.0, 2.4, GREEN, True),
            ("HIGH / mmWave", "24 GHz +", 0.5, 3.6, AMBER, False),
        ]
        row_ys = [1.55, -0.1, -1.75]
        ring_cx = -4.2
        bar_x0 = -0.6

        ring_data = []  # (ring, color, radius)
        bar_data = []   # (bar, target_len, color)
        all_create = []

        for (name, freq, rr, blen, col, hi), y in zip(rows, row_ys):
            # tower
            mast = Line([ring_cx, y - 0.25, 0], [ring_cx, y + 0.35, 0],
                        stroke_color=col, stroke_width=3)
            base = Triangle(color=col, fill_opacity=0.0).scale(0.18)
            base.next_to([ring_cx, y - 0.25, 0], DOWN, buff=0.0)
            # range ring
            ring = Circle(radius=rr, stroke_color=col, stroke_width=2.5,
                          fill_opacity=0.0).move_to([ring_cx, y, 0])
            ring_data.append((ring, col, rr))
            # name + freq label
            nm = Text(name, font=HEAD, color=col if hi else INK,
                      weight="SEMIBOLD").scale(0.34)
            fq = Text(freq, font=MONO, color=SECOND).scale(0.26)
            lab = VGroup(nm, fq).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            lab.move_to([bar_x0 - 0.2, y + 0.55, 0]).align_to(
                [bar_x0, 0, 0], LEFT)
            # speed bar (track + fill)
            track = Rectangle(width=3.8, height=0.34, stroke_color=SECOND,
                              stroke_width=1.2, fill_color="#111318",
                              fill_opacity=0.8)
            track.move_to([bar_x0 + 1.9, y - 0.15, 0], aligned_edge=LEFT)
            bar = Rectangle(width=max(blen, 0.001), height=0.34,
                            stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to(track.get_left(), aligned_edge=LEFT)
            bar_data.append((bar, blen, col))

            if hi:
                tag = Text("the real 5G", font=MONO, color=GREEN,
                           weight="BOLD").scale(0.3)
                tag.next_to(track, RIGHT, buff=0.3)
            else:
                tag = VGroup()

            all_create += [mast, base, ring, lab, track, bar, tag]

        self.play(*[Create(m) if isinstance(m, (Line, Circle, Triangle,
                   Rectangle)) else FadeIn(m) for m in all_create],
                  lag_ratio=0.02, run_time=1.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Rings pulse outward (expanding wavefront that resets), cadence set by
        # band: low-band slow wide, mmWave fast tight.
        for i, (ring, col, rr) in enumerate(ring_data):
            cadence = 0.9 + i * 0.7  # waves per second-ish

            def make_ring(ringm, basecol, base_r, cad, phase):
                def _upd(m):
                    s = (0.5 + 0.5 * np.sin(cad * t.get_value() + phase))
                    m.set_stroke(opacity=0.25 + 0.55 * s, width=1.5 + 3.0 * s)
                    m.scale_to_fit_width((base_r * 2) * (0.92 + 0.12 * s))
                return _upd
            ring.add_updater(make_ring(ring, col, rr, cadence, i * 1.1))

        # Travelling "wave" dots emitted from each tower, cadence per band.
        wave_dots = VGroup()
        wave_meta = []
        for i, ((name, freq, rr, blen, col, hi), y) in enumerate(
                zip(rows, row_ys)):
            n = 3
            for k in range(n):
                seg = Line([ring_cx, y, 0], [ring_cx + 0.3, y, 0],
                           stroke_color=col, stroke_width=3)
                wave_dots.add(seg)
                period = 1.6 + i * 0.0  # all travel, mmWave shorter reach
                reach = rr
                wave_meta.append((ring_cx, y, reach, 1.4 + i * 0.5,
                                  k / n, col))
        self.add(wave_dots)

        def make_wave(meta):
            cx, y, reach, period, off, col = meta

            def _upd(m):
                frac = ((t.get_value() / period) + off) % 1.0
                r = 0.15 + frac * reach
                m.put_start_and_end_on([cx + r - 0.15, y, 0],
                                       [cx + r + 0.15, y, 0])
                m.set_stroke(opacity=np.clip(1.0 - frac, 0.0, 1.0))
            return _upd

        for seg, meta in zip(wave_dots, wave_meta):
            seg.add_updater(make_wave(meta))

        # Speed bars breathe slightly, colour shimmer on mid-band (highlight).
        for i, (bar, blen, col) in enumerate(bar_data):
            track_left_x = bar_x0 + 1.9  # left edge x of each bar

            def make_bar(barm, length, basecol, phase, is_mid):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + phase)
                    w = length * (0.96 + 0.04 * s)
                    left = barm.get_left()
                    m.scale_to_fit_width(max(w, 0.001))
                    m.move_to(left, aligned_edge=LEFT)
                    if is_mid:
                        c = interpolate_color(ManimColor(GREEN),
                                              ManimColor(TEAL), s)
                        m.set_fill(c, opacity=0.9)
                return _upd
            bar.add_updater(make_bar(bar, blen, col, i * 0.8, rows[i][5]))

        # caption
        cap = Text("low reaches far  ·  mmWave is fast but tiny",
                   font=HEAD, color=SECOND).scale(0.4)
        cap.to_edge(DOWN, buff=0.35)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
