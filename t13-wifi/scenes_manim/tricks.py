"""Scene: Tricks — MIMO, beamforming, OFDMA.

Class `Tricks` (~20s). Three ideas shown together:
  (a) MIMO: a router with 3 antennas sends 3 parallel streams to a device.
  (b) BEAMFORMING: omnidirectional rings collapse into a single focused beam
      aimed at the device; the beam sweeps to track it.
  (c) OFDMA: the router serves 3 devices in the SAME time-slot (three arrows
      leaving together) vs a greyed "one-at-a-time" before.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Line,
    Circle,
    Text,
    VGroup,
    VMobject,
    Polygon,
    Dot,
    ValueTracker,
    config,
    FadeIn,
    Create,
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


class Tricks(Scene):
    def construct(self):
        title = Text("Modern Wi-Fi fights back",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # three columns
        col_x = [-4.6, 0.0, 4.6]
        panel_y = 0.1

        panels = VGroup()
        pan_labels = ["MIMO", "beamforming", "OFDMA"]
        pan_cols = [TEAL, VIOLET, GREEN]
        for x, name, col in zip(col_x, pan_labels, pan_cols):
            box = RoundedRectangle(
                corner_radius=0.12, width=4.2, height=4.4,
                stroke_color=col, stroke_width=2.0,
                fill_color="#0C0D10", fill_opacity=0.5,
            ).move_to([x, panel_y, 0])
            lbl = Text(name, font=MONO, color=col, weight="BOLD").scale(0.34)
            lbl.next_to(box, UP, buff=0.14)
            panels.add(VGroup(box, lbl))
        self.play(*[Create(p[0]) for p in panels],
                  *[FadeIn(p[1]) for p in panels], run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # ---- (a) MIMO: router w/ 3 antennas, 3 parallel streams -------------
        mx = col_x[0]
        m_router = RoundedRectangle(
            corner_radius=0.06, width=0.6, height=0.4,
            stroke_color=TEAL, stroke_width=2.0,
            fill_color="#0A1716", fill_opacity=1.0,
        ).move_to([mx - 1.3, panel_y - 0.2, 0])
        m_ants = VGroup()
        for dx in (-0.18, 0.0, 0.18):
            a = Line(m_router.get_top() + RIGHT * dx,
                     m_router.get_top() + RIGHT * dx + UP * 0.3,
                     stroke_color=TEAL, stroke_width=2.0)
            m_ants.add(a)
        m_device = RoundedRectangle(
            corner_radius=0.08, width=0.45, height=0.75,
            stroke_color=GREEN, stroke_width=2.0,
            fill_color="#0A1711", fill_opacity=1.0,
        ).move_to([mx + 1.3, panel_y - 0.2, 0])
        self.add(m_router, m_ants, m_device)

        m_src = np.array([mx - 1.0, panel_y - 0.2, 0.0])
        m_dst = np.array([mx + 1.05, panel_y - 0.2, 0.0])
        stream_ys = [0.55, 0.0, -0.55]
        for si, sy in enumerate(stream_ys):
            # 3 packets flowing per stream
            for k in range(3):
                d = Dot(radius=0.07, color=TEAL)

                def make_stream(offset_y, phase):
                    start = m_src + UP * offset_y
                    end = m_dst + UP * offset_y

                    def _upd(m):
                        period = 2.0
                        tt = (t.get_value() + phase) % period
                        frac = tt / period
                        pos = start * (1 - frac) + end * frac
                        m.move_to(pos)
                        m.set_opacity(np.clip(1.3 * (1 - frac) + 0.1, 0, 1))
                    return _upd
                d.add_updater(make_stream(sy, si * 0.3 + k * 0.66))
                self.add(d)

        # ---- (b) BEAMFORMING: rings collapse into a sweeping beam -----------
        bx = col_x[1]
        b_router = RoundedRectangle(
            corner_radius=0.06, width=0.55, height=0.38,
            stroke_color=VIOLET, stroke_width=2.0,
            fill_color="#130A17", fill_opacity=1.0,
        ).move_to([bx, panel_y + 1.1, 0])
        self.add(b_router)
        b_origin = np.array([bx, panel_y + 0.9, 0.0])

        # device that moves along an arc (the beam tracks it)
        b_device = Dot(radius=0.1, color=GREEN)

        def dev_pos(tt):
            # device sweeps left-right at the bottom of the panel
            sweep = np.sin(tt * 0.8)
            return np.array([bx + sweep * 1.3, panel_y - 1.5, 0.0])

        def b_device_upd(m):
            m.move_to(dev_pos(t.get_value()))
        b_device.add_updater(b_device_upd)
        self.add(b_device)

        # omnidirectional rings that fade as the beam takes over
        for i in range(3):
            ring = Circle(radius=0.3, stroke_color=VIOLET, stroke_width=2.0,
                          fill_opacity=0).move_to(b_origin)

            def make_bring(phase):
                def _upd(m):
                    # focus factor: oscillates so rings pulse but stay faint
                    period = 2.4
                    tt = (t.get_value() + phase) % period
                    frac = tt / period
                    m.set(width=0.6 + frac * 2.2)
                    m.move_to(b_origin)
                    # rings are weak (energy is in the beam)
                    m.set_stroke(opacity=np.clip((1 - frac) * 0.22, 0, 0.22))
                return _upd
            ring.add_updater(make_bring(i * 0.8))
            self.add(ring)

        # the focused beam: a thin triangle from router to device
        beam = Polygon(b_origin, b_origin, b_origin,
                       stroke_width=0, fill_color=VIOLET, fill_opacity=0.3)

        def beam_upd(m):
            tt = t.get_value()
            tip = dev_pos(tt)
            d = tip - b_origin
            length = np.linalg.norm(d)
            if length < 1e-3:
                return
            dirv = d / length
            perp = np.array([-dirv[1], dirv[0], 0.0])
            half = 0.3
            p_left = b_origin + perp * 0.12
            p_right = b_origin - perp * 0.12
            t_left = tip + perp * half
            t_right = tip - perp * half
            m.set_points_as_corners([p_left, t_left, t_right, p_right, p_left])
            s = 0.5 + 0.5 * np.sin(tt * 4.0)
            m.set_fill(VIOLET, opacity=0.25 + 0.3 * s)
        beam.add_updater(beam_upd)
        self.add(beam)

        # ---- (c) OFDMA: 3 devices served in the same slot ------------------
        ox = col_x[2]
        o_router = RoundedRectangle(
            corner_radius=0.06, width=0.55, height=0.38,
            stroke_color=GREEN, stroke_width=2.0,
            fill_color="#0A1711", fill_opacity=1.0,
        ).move_to([ox, panel_y + 1.3, 0])
        self.add(o_router)
        o_src = np.array([ox, panel_y + 1.1, 0.0])

        o_targets = [
            np.array([ox - 1.3, panel_y - 1.1, 0.0]),
            np.array([ox, panel_y - 1.5, 0.0]),
            np.array([ox + 1.3, panel_y - 1.1, 0.0]),
        ]
        for i, tgt in enumerate(o_targets):
            dev = RoundedRectangle(
                corner_radius=0.05, width=0.32, height=0.5,
                stroke_color=GREEN, stroke_width=1.8,
                fill_color="#0A1711", fill_opacity=1.0,
            ).move_to(tgt + DOWN * 0.3)
            self.add(dev)
            # three arrows leaving together (same time-slot)
            pkt = Dot(radius=0.07, color=GREEN)

            def make_ofdma(target):
                def _upd(m):
                    period = 1.8
                    tt = t.get_value() % period
                    frac = tt / period
                    pos = o_src * (1 - frac) + target * frac
                    m.move_to(pos)
                    m.set_opacity(np.clip(1.3 * (1 - frac) + 0.1, 0, 1))
                return _upd
            pkt.add_updater(make_ofdma(tgt))
            self.add(pkt)

        # greyed "one-at-a-time" before caption inside OFDMA panel
        before = Text("vs one-at-a-time", font=MONO, color=SECOND).scale(0.24)
        before.move_to([ox, panel_y + 0.3, 0])
        before.set_opacity(0.4)
        self.add(before)

        cap = Text("three tricks that rescue a crowded band", font=MONO,
                   color=SILVER).scale(0.3)
        cap.to_edge(DOWN, buff=0.35)
        self.add(cap)

        # antenna glow on MIMO
        def ants_glow(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 4.0)
            m.set_stroke(TEAL, opacity=0.5 + 0.5 * s)
        m_ants.add_updater(ants_glow)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
