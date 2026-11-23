"""Scene: Wi-Fi radio — two radios making the air wiggle.

Class `Radio` (~20s). LEFT a router (rounded box with 2 antenna lines) emits
concentric radio-wave rings that expand outward and fade on a loop. RIGHT a
device (rounded rect) receives. A teal bitstream "1 0 1 1 0" flows from the
router, becomes a wave as it crosses the gap, and turns back into bits at the
device. Labels "router = radio" and "device = radio".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
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


class Radio(Scene):
    def construct(self):
        title = Text("Two radios, making the air wiggle",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        router_pos = LEFT * 4.6 + DOWN * 0.3
        device_pos = RIGHT * 4.6 + DOWN * 0.3

        # --- router (left): rounded box + 2 antenna lines -------------------
        r_body = RoundedRectangle(
            corner_radius=0.1, width=1.3, height=0.8,
            stroke_color=TEAL, stroke_width=2.5,
            fill_color="#0A1716", fill_opacity=0.7,
        ).move_to(router_pos)
        ant1 = Line(r_body.get_top() + LEFT * 0.28,
                    r_body.get_top() + LEFT * 0.28 + UP * 0.45,
                    stroke_color=TEAL, stroke_width=2.5)
        ant2 = Line(r_body.get_top() + RIGHT * 0.28,
                    r_body.get_top() + RIGHT * 0.28 + UP * 0.45,
                    stroke_color=TEAL, stroke_width=2.5)
        a1tip = Dot(ant1.get_end(), radius=0.04, color=GREEN)
        a2tip = Dot(ant2.get_end(), radius=0.04, color=GREEN)
        router = VGroup(r_body, ant1, ant2, a1tip, a2tip)
        r_lbl = Text("router = radio", font=MONO, color=TEAL).scale(0.3)
        r_lbl.next_to(router, DOWN, buff=0.3)

        # --- device (right): rounded rect (phone) ---------------------------
        d_body = RoundedRectangle(
            corner_radius=0.12, width=0.95, height=1.5,
            stroke_color=GREEN, stroke_width=2.5,
            fill_color="#0A1711", fill_opacity=0.7,
        ).move_to(device_pos)
        d_screen = RoundedRectangle(
            corner_radius=0.06, width=0.72, height=1.1,
            stroke_color=SECOND, stroke_width=1.2,
            fill_color="#0D140F", fill_opacity=0.8,
        ).move_to(device_pos + UP * 0.1)
        device = VGroup(d_body, d_screen)
        d_lbl = Text("device = radio", font=MONO, color=GREEN).scale(0.3)
        d_lbl.next_to(device, DOWN, buff=0.3)

        self.play(Create(router), Create(device), run_time=0.8)
        self.play(FadeIn(r_lbl), FadeIn(d_lbl), run_time=0.3)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        emit = r_body.get_right() + RIGHT * 0.1
        recv = d_body.get_left()
        emit_pt = np.array([emit[0], emit[1], 0.0])
        recv_pt = np.array([recv[0], recv[1], 0.0])
        gap = recv_pt[0] - emit_pt[0]
        mid_y = (emit_pt[1] + recv_pt[1]) / 2.0

        # --- concentric radio-wave rings, expand + fade on a loop -----------
        N_RINGS = 5
        ring_period = 2.4
        rings = VGroup()
        for i in range(N_RINGS):
            c = Circle(radius=0.2, stroke_color=TEAL, stroke_width=3,
                       fill_opacity=0).move_to(emit_pt)
            rings.add(c)

        def make_ring(idx):
            offset = idx * (ring_period / N_RINGS)

            def _upd(m):
                tt = (t.get_value() + offset) % ring_period
                frac = tt / ring_period
                radius = 0.25 + frac * 4.6
                m.set(width=radius * 2.0)
                m.move_to(emit_pt)
                m.set_stroke(opacity=np.clip((1.0 - frac) * 0.9, 0.0, 0.9))
            return _upd

        for i, c in enumerate(rings):
            c.add_updater(make_ring(i))
        self.add(rings)

        # --- bitstream -> wave -> bits --------------------------------------
        # Region split: first 25% bits, middle 50% wave, last 25% bits.
        seg_bits_out = 0.26
        seg_wave = 0.74
        bit_chars = ["1", "0", "1", "1", "0", "1", "0", "0", "1"]

        def flow_pos(frac):
            # x travels linearly across the gap; y flips to a sine in wave zone.
            x = emit_pt[0] + frac * gap
            if frac < seg_bits_out:
                y = mid_y
            elif frac < seg_wave:
                wf = (frac - seg_bits_out) / (seg_wave - seg_bits_out)
                env = np.sin(np.pi * wf)  # fade in/out of the wiggle
                y = mid_y + 0.55 * env * np.sin(2.0 * np.pi * 3.0 * wf
                                                - t.get_value() * 3.0)
            else:
                y = mid_y
            return np.array([x, y, 0.0])

        # travelling carrier wave drawn across the wave zone
        carrier = VMobject(stroke_color=TEAL, stroke_width=2.5)

        def carrier_upd(m):
            pts = []
            steps = 120
            for s in range(steps + 1):
                frac = seg_bits_out + (seg_wave - seg_bits_out) * (s / steps)
                pts.append(flow_pos(frac))
            m.set_points_as_corners(pts)
            m.set_stroke(opacity=0.55)
        carrier.add_updater(carrier_upd)
        self.add(carrier)

        # flowing bit labels
        bits = VGroup()
        n_bits = 9
        bit_period = 3.4
        for i in range(n_bits):
            lbl = Text(bit_chars[i % len(bit_chars)], font=MONO,
                       color=TEAL).scale(0.34)
            bits.add(lbl)

        def make_bit(idx):
            offset = (idx / n_bits) * bit_period
            char0 = bit_chars[idx % len(bit_chars)]

            def _upd(m):
                tt = (t.get_value() + offset) % bit_period
                frac = tt / bit_period
                pos = flow_pos(frac)
                m.move_to(pos)
                # in the wave zone the bit dissolves into the wiggle
                if seg_bits_out <= frac < seg_wave:
                    op = 0.12
                else:
                    op = 1.0
                m.set_opacity(op)
                # recolour: teal on the way out, green when it arrives
                m.set_color(GREEN if frac >= seg_wave else TEAL)
            return _upd

        for i, b in enumerate(bits):
            b.add_updater(make_bit(i))
        self.add(bits)

        # device screen pulse when bits arrive
        def screen_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 2.6)
            m.set_fill(opacity=0.6 + 0.3 * s)
            m.set_stroke(color=GREEN, opacity=0.4 + 0.5 * s)
        d_screen.add_updater(screen_upd)

        # antenna tips glow
        def make_tip(tip):
            def _upd(m):
                s = 0.5 + 0.5 * np.sin(t.get_value() * 4.0)
                m.set_opacity(0.4 + 0.6 * s)
            return _upd
        a1tip.add_updater(make_tip(a1tip))
        a2tip.add_updater(make_tip(a2tip))

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
