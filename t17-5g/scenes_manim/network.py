"""Scene: Dense small cells + massive MIMO beamforming.

Class `Network` (~20s). Left: one big 4G tower with wide weak coverage.
Right: many SMALL CELLS (dots on lampposts/buildings) with tight strong
coverage. A massive-MIMO panel (small grid of antennas) focuses a BEAM that
TRACKS a moving phone back and forth. Labels: small cells, massive MIMO,
beamforming. Caption: "more cells, each smarter — but slow & costly to build".

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
    Text,
    VGroup,
    Line,
    Circle,
    Dot,
    Polygon,
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


class Network(Scene):
    def construct(self):
        title = Text("Dense small cells & beamforming", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        divider = Line([0, -3.0, 0], [0, 2.3, 0], stroke_color=SECOND,
                       stroke_width=1, stroke_opacity=0.3)
        self.add(divider)

        # --- LEFT: one big 4G tower, wide weak coverage ---------------------
        tow_base = np.array([-3.8, -2.1, 0.0])
        mast = Line(tow_base, tow_base + UP * 2.4, stroke_color=SECOND,
                    stroke_width=4)
        tow_top = tow_base + UP * 2.4
        wide = Circle(radius=2.6, stroke_color=SECOND, stroke_width=2,
                      stroke_opacity=0.5, fill_color=SECOND,
                      fill_opacity=0.05).move_to(tow_top)
        l_lbl = Text("one big 4G tower", font=MONO, color=SECOND).scale(0.3)
        l_lbl.next_to(mast, DOWN, buff=0.12)
        l_sub = Text("wide · weak", font=MONO, color=SECOND).scale(0.26)
        l_sub.next_to(l_lbl, DOWN, buff=0.08)
        self.play(Create(mast), Create(wide), FadeIn(l_lbl), FadeIn(l_sub),
                  run_time=0.9)

        # --- RIGHT: many small cells, tight strong coverage -----------------
        rng = np.random.default_rng(5)
        cell_group = VGroup()
        cells = []
        positions = [
            (1.6, 1.4), (2.8, 0.6), (4.4, 1.2), (2.0, -0.6),
            (3.6, -0.2), (5.0, -0.8), (1.4, -1.6), (3.0, -1.8),
            (4.6, -1.7),
        ]
        for (cx, cy) in positions:
            post = Line([cx, cy - 0.5, 0], [cx, cy, 0], stroke_color=GREEN,
                        stroke_width=2.5)
            node = Dot([cx, cy, 0], color=GREEN, radius=0.08)
            cov = Circle(radius=0.75, stroke_color=GREEN, stroke_width=1.5,
                         stroke_opacity=0.5, fill_color=GREEN,
                         fill_opacity=0.06).move_to([cx, cy, 0])
            g = VGroup(post, node, cov)
            cell_group.add(g)
            cells.append((node, cov, np.array([cx, cy, 0])))
        self.play(*[GrowFromCenter(g) for g in cell_group],
                  lag_ratio=0.08, run_time=1.2)

        r_lbl = Text("small cells", font=MONO, color=GREEN).scale(0.3)
        r_lbl.move_to([3.2, 2.0, 0])
        self.play(FadeIn(r_lbl), run_time=0.4)

        # --- massive MIMO panel (grid of antennas) on the right edge --------
        panel_c = np.array([5.6, 0.2, 0.0])
        antennas = VGroup()
        for r in range(4):
            for c in range(4):
                d = Dot(panel_c + np.array([(c - 1.5) * 0.14,
                        (r - 1.5) * 0.14, 0]), color=TEAL, radius=0.035)
                antennas.add(d)
        panel_box = RoundedRectangle(corner_radius=0.06, width=0.75,
                                     height=0.75, stroke_color=TEAL,
                                     stroke_width=2,
                                     fill_opacity=0.0).move_to(panel_c)
        mimo_lbl = Text("massive MIMO", font=MONO, color=TEAL).scale(0.26)
        mimo_lbl.next_to(panel_box, DOWN, buff=0.12)
        self.play(Create(panel_box), *[FadeIn(a) for a in antennas],
                  FadeIn(mimo_lbl), run_time=0.8)

        # --- moving phone the beam will track -------------------------------
        phone = RoundedRectangle(corner_radius=0.08, width=0.5, height=0.95,
                                 stroke_color=INK, stroke_width=2.5,
                                 fill_color="#111318", fill_opacity=0.9)
        phone_y = 0.2
        phone.move_to([2.4, phone_y, 0])
        self.play(FadeIn(phone), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        x_lo, x_hi = 1.4, 4.6

        def phone_x(tt):
            # back and forth, triangle wave
            s = 0.5 + 0.5 * np.sin(0.8 * tt)
            return x_lo + (x_hi - x_lo) * s

        def phone_upd(m):
            m.move_to([phone_x(t.get_value()), phone_y, 0])
        phone.add_updater(phone_upd)

        # Beamforming wedge from MIMO panel to the phone (it visibly follows).
        beam = Polygon(panel_c, panel_c, panel_c, stroke_width=0,
                       fill_color=TEAL, fill_opacity=0.25)

        def beam_upd(m):
            px = phone_x(t.get_value())
            target = np.array([px, phone_y, 0.0])
            direc = target - panel_c
            dist = np.linalg.norm(direc)
            direc = direc / dist
            perp = np.array([-direc[1], direc[0], 0.0])
            halfw = 0.35
            p1 = panel_c + perp * 0.1
            p2 = target + perp * halfw
            p3 = target - perp * halfw
            p4 = panel_c - perp * 0.1
            new = Polygon(p1, p2, p3, p4, stroke_width=0,
                          fill_color=TEAL)
            pulse = 0.5 + 0.5 * np.sin(5.0 * t.get_value())
            new.set_fill(TEAL, opacity=0.15 + 0.25 * pulse)
            m.become(new)
        beam.add_updater(beam_upd)
        self.add(beam)
        phone.set_z_index(5)

        beam_lbl = Text("beamforming", font=MONO, color=TEAL).scale(0.26)
        beam_lbl.move_to([2.6, -2.4, 0])

        def beam_lbl_upd(m):
            m.set_opacity(0.5 + 0.5 * (0.5 + 0.5 *
                          np.sin(2.0 * t.get_value())))
        beam_lbl.add_updater(beam_lbl_upd)
        self.add(beam_lbl)

        # small cells pulse
        for i, (node, cov, pos) in enumerate(cells):
            def make_cell(covm, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.2 * t.get_value() + phase)
                    m.set_stroke(opacity=0.3 + 0.4 * s)
                    m.set_fill(opacity=0.03 + 0.08 * s)
                return _upd
            cov.add_updater(make_cell(cov, i * 0.6))

        # wide 4G coverage dims (weak) by comparison
        def wide_upd(m):
            s = 0.5 + 0.5 * np.sin(1.2 * t.get_value())
            m.set_stroke(opacity=0.25 + 0.2 * s)
        wide.add_updater(wide_upd)

        # MIMO antennas twinkle
        for i, a in enumerate(antennas):
            def make_ant(phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(4.0 * t.get_value() + phase)
                    m.set_opacity(0.4 + 0.6 * s)
                return _upd
            a.add_updater(make_ant(i * 0.4))

        # caption
        cap = Text("more cells, each smarter — but slow & costly to build",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

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
