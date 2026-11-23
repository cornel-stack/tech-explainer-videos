"""Scene: the mobile-network generation speed ladder on a LOG scale.

Class `Timeline` (~20s). Rungs for 1G -> 6G climb up-and-right, each carrying
the "G" name, its year, peak speed and the capability it unlocked. A log-scaled
bandwidth bar grows on each rung so the whole 1,000,000x range stays legible. A
climbing marker ascends the ladder on a loop while a big readout builds toward
"~ 1,000,000x faster in ~40 years". Faint enough to sit behind an intro title,
rich enough to stand alone.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Line,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    interpolate_color,
    FadeIn,
    Create,
    GrowFromCenter,
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


class Timeline(Scene):
    def construct(self):
        title = Text("1G to 6G — a million times faster in forty years",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- data: each generation -------------------------------------------
        # (name, year, kbps peak, unlocked word, colour)
        gens = [
            ("1G",   "1980s", 2.4,       "voice",     SILVER),
            ("2G",   "1991",  64.0,      "text",      TEAL),
            ("2.5G", "2000",  200.0,     "data",      TEAL),
            ("3G",   "2001",  7_000.0,   "web",       GREEN),
            ("3.5G", "2008",  21_000.0,  "apps",      GREEN),
            ("4G",   "2009",  150_000.0, "streaming", AMBER),
            ("4.5G", "2013",  600_000.0, "HD",        AMBER),
            ("5G",   "2019",  1_000_000.0, "IoT",     VIOLET),
            ("6G",   "~2030", 1_000_000_000.0, "sensing", CORAL),
        ]
        n = len(gens)

        # log-scale helper over the full kbps range -> 0..1
        lo = np.log10(gens[0][2])
        hi = np.log10(gens[-1][2])

        def lognorm(kbps):
            return (np.log10(kbps) - lo) / (hi - lo)

        # --- ladder geometry: rungs climb up-and-right -----------------------
        x_lo, x_hi = -5.9, 1.2
        y_lo, y_hi = -3.0, 2.0
        rung_pts = []
        for i in range(n):
            f = i / (n - 1)
            x = x_lo + (x_hi - x_lo) * f
            y = y_lo + (y_hi - y_lo) * f
            rung_pts.append(np.array([x, y, 0]))

        # faint diagonal spine the marker rides along
        spine = Line(rung_pts[0] + DOWN * 0.1, rung_pts[-1] + UP * 0.1,
                     stroke_color=SECOND, stroke_width=1.5, stroke_opacity=0.35)
        self.play(Create(spine), run_time=0.6)

        # --- build each rung --------------------------------------------------
        rungs = []
        bars = []
        for i, (name, year, kbps, word, col) in enumerate(gens):
            pt = rung_pts[i]

            node = Dot(point=pt, color=col, radius=0.08)

            # name + year stacked just above-left of the node
            name_lbl = Text(name, font=MONO, color=col, weight="BOLD").scale(0.34)
            name_lbl.next_to(pt, UP, buff=0.1).shift(LEFT * 0.05)
            year_lbl = Text(year, font=MONO, color=SECOND).scale(0.2)
            year_lbl.next_to(name_lbl, UP, buff=0.05)

            # peak-speed readout + unlocked word to the right of the node
            if kbps >= 1_000_000:
                if kbps >= 1_000_000_000:
                    sp = "~1 Tbps"
                else:
                    sp = "~1 Gbps"
            elif kbps >= 1000:
                sp = f"{kbps / 1000:.0f} Mbps" if kbps >= 10000 else \
                     f"{kbps / 1000:.1f} Mbps"
            else:
                sp = f"{kbps:.0f} kbps" if kbps >= 10 else f"{kbps:.1f} kbps"
            speed_lbl = Text(sp, font=MONO, color=INK).scale(0.24)
            speed_lbl.next_to(pt, RIGHT, buff=0.22)
            word_lbl = Text(word, font=HEAD, color=col).scale(0.22)
            word_lbl.next_to(speed_lbl, DOWN, buff=0.06).align_to(speed_lbl, LEFT)

            # log-scaled bandwidth bar behind the speed label
            bar_w = 0.25 + lognorm(kbps) * 1.55
            bar = RoundedRectangle(
                corner_radius=0.04, width=bar_w, height=0.14,
                stroke_width=0, fill_color=col, fill_opacity=0.9,
            )
            bar.next_to(speed_lbl, DOWN, buff=0.28).align_to(speed_lbl, LEFT)
            bar.shift(RIGHT * bar_w / 2 - RIGHT * 0.0)
            bar.align_to(speed_lbl, LEFT)

            g = VGroup(node, name_lbl, year_lbl, bar, speed_lbl, word_lbl)
            rungs.append(g)
            bars.append((bar, col, bar_w))

        # reveal rungs climbing up-and-right
        self.play(
            *[GrowFromCenter(r) for r in rungs],
            lag_ratio=0.12, run_time=1.8,
        )

        # --- big readout (builds as the marker climbs) -----------------------
        readout = Text("~ 1x", font=MONO, color=GOLD, weight="BOLD").scale(0.62)
        readout.to_corner(RIGHT + DOWN, buff=0.55)
        readout._shown = ""
        self.add(readout)

        sub = Text("faster since 1G", font=HEAD, color=SECOND).scale(0.28)
        sub.next_to(readout, UP, buff=0.12).align_to(readout, RIGHT)
        self.add(sub)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # bandwidth bars pulse (subtle breathing on opacity)
        for i, (bar, col, bw) in enumerate(bars):
            def make_pulse(b, phase):
                def _upd(m):
                    tt = t.get_value()
                    b.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                                               np.sin(2.0 * tt + phase)))
                return _upd
            bar.add_updater(make_pulse(bar, i * 0.6))

        # rung nodes breathe too
        for i, g in enumerate(rungs):
            node = g[0]
            base_r = node.radius

            def make_node(nd, br, phase):
                def _upd(m):
                    tt = t.get_value()
                    s = 0.5 + 0.5 * np.sin(2.4 * tt + phase)
                    nd.set_opacity(0.55 + 0.45 * s)
                return _upd
            node.add_updater(make_node(node, base_r, i * 0.7))

        # climbing marker ascends the ladder on a loop
        marker = Dot(color=GOLD, radius=0.14)
        marker_glow = Dot(color=GOLD, radius=0.26).set_opacity(0.25)
        climb_period = 7.0

        def marker_frac():
            tt = t.get_value() % climb_period
            return rate_functions.ease_in_out_sine(tt / climb_period)

        def marker_pos(frac):
            # interpolate along the piecewise rung points
            seg = frac * (n - 1)
            i0 = int(np.clip(np.floor(seg), 0, n - 2))
            local = seg - i0
            return rung_pts[i0] * (1 - local) + rung_pts[i0 + 1] * local

        def marker_upd(m):
            m.move_to(marker_pos(marker_frac()))
        marker.add_updater(marker_upd)

        def glow_upd(m):
            m.move_to(marker_pos(marker_frac()))
            tt = t.get_value()
            m.set_opacity(0.18 + 0.14 * (0.5 + 0.5 * np.sin(4.0 * tt)))
        marker_glow.add_updater(glow_upd)
        self.add(marker_glow, marker)

        # a faint trail colour-blends along the climb (demonstrates ManimColor)
        trail = VGroup(*[Dot(radius=0.05) for _ in range(14)])
        for d in trail:
            d.set_opacity(0.0)
        self.add(trail)

        def trail_upd(m):
            base = marker_frac()
            for k, d in enumerate(m):
                back = base - (k + 1) * 0.015
                if back <= 0:
                    d.set_opacity(0.0)
                    continue
                d.move_to(marker_pos(back))
                col = interpolate_color(ManimColor(GOLD), ManimColor(CORAL),
                                        k / (len(m) - 1))
                d.set_color(col)
                d.set_opacity(0.4 * (1 - k / len(m)))
        trail.add_updater(trail_upd)

        # big readout builds its multiplier as the marker climbs the ladder
        def readout_upd(m):
            frac = marker_frac()
            # map climb fraction onto the full speed range in log space
            factor = 10 ** (frac * (hi - lo))
            if factor >= 1_000_000:
                txt = f"~ {factor / 1_000_000:,.0f},000,000x"
                txt = "~ 1,000,000x" if factor >= 900_000 else txt
            elif factor >= 1000:
                txt = f"~ {factor / 1000:,.0f},000x"
            else:
                txt = f"~ {factor:,.0f}x"
            if txt != m._shown:
                m._shown = txt
                new = Text(txt, font=MONO, color=GOLD,
                           weight="BOLD").scale(0.58)
                new.move_to(m.get_right(), aligned_edge=RIGHT)
                m.become(new)
        readout.add_updater(readout_upd)

        # footer: the headline the readout is building toward
        foot = Text("each G ~ 10x the last, compounding for 40 years",
                    font=MONO, color=SECOND).scale(0.26)
        foot.next_to(title, DOWN, buff=0.12)

        def foot_upd(m):
            m.set_opacity(0.5 + 0.4 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 1.4)))
        foot.add_updater(foot_upd)
        self.add(foot)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
