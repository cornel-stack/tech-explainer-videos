"""Interlude scene: the API-style decision map (2x2 axes).

Class `Axis` — a 2x2 decision map with chips popping into quadrants, then a
CONTINUOUSLY animated phase: pulses travel along both axes, chips bob/pulse
in place, a soft highlight ring sweeps quadrant to quadrant, and the WebRTC
peers keep exchanging a dot. Nothing ever freezes. ~24s.

Dark design system (no blue, no white):
  bg      #0A0A0C
  ink     #EDE7DB (cream)   secondary #9A958C
  accents amber #FFC24B  magenta #FF3E7F  mint #3DE0B0
          violet #B06BFF  coral #FF6B4A  gold #E8C24A
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Line,
    Text,
    VGroup,
    Dot,
    Circle,
    ValueTracker,
    config,
    FadeIn,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    rate_functions,
)

# --- palette -----------------------------------------------------------------
BG = "#0A0A0C"
INK = "#EDE7DB"
SECOND = "#9A958C"
AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

config.background_color = BG


def chip(label, accent, scale=1.0):
    """A rounded-rectangle chip with a simulated glow behind a crisp stroke."""
    txt = Text(label, font="Inter", color=INK, weight="MEDIUM").scale(0.34 * scale)
    w = max(txt.width + 0.5, 1.2)
    h = 0.62 * scale
    body = RoundedRectangle(
        corner_radius=0.16,
        width=w,
        height=h,
        stroke_color=accent,
        stroke_width=3,
        fill_color=BG,
        fill_opacity=0.9,
    )
    glow = RoundedRectangle(
        corner_radius=0.16,
        width=w,
        height=h,
        stroke_color=accent,
        stroke_width=11,
        stroke_opacity=0.18,
        fill_opacity=0,
    )
    group = VGroup(glow, body, txt)
    group.glow = glow
    group.accent = accent
    group.home = ORIGIN
    return group


class Axis(Scene):
    def construct(self):
        # --- Title -----------------------------------------------------------
        title = Text("Who starts? How long does it last?",
                     font="Inter", color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)

        # --- Axes ------------------------------------------------------------
        # Cross centred slightly left to leave room for the WebRTC side note.
        cx, cy = -1.6, -0.35
        span_x = 4.2
        span_y = 2.8

        x_axis = Line([cx - span_x, cy, 0], [cx + span_x, cy, 0],
                      color=INK, stroke_width=2.5)
        y_axis = Line([cx, cy - span_y, 0], [cx, cy + span_y, 0],
                      color=INK, stroke_width=2.5)

        # Faint quadrant outlines.
        quad_group = VGroup()
        quad_centers = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                q = RoundedRectangle(
                    corner_radius=0.1,
                    width=span_x - 0.1,
                    height=span_y - 0.1,
                    stroke_color=SECOND,
                    stroke_width=1,
                    stroke_opacity=0.25,
                    fill_opacity=0,
                )
                qc = [cx + sx * span_x / 2, cy + sy * span_y / 2, 0]
                q.move_to(qc)
                quad_group.add(q)
                quad_centers.append(np.array(qc))

        # Axis end labels.
        x_left = Text("client starts", font="Inter", color=SECOND).scale(0.3)
        x_left.next_to([cx - span_x, cy, 0], DOWN, buff=0.18).shift(RIGHT * 0.9)
        x_right = Text("server starts  →", font="Inter", color=SECOND).scale(0.3)
        x_right.next_to([cx + span_x, cy, 0], DOWN, buff=0.18).shift(LEFT * 0.9)

        y_top = Text("one-shot", font="Inter", color=SECOND).scale(0.3)
        y_top.next_to([cx, cy + span_y, 0], LEFT, buff=0.18).shift(UP * 0.1)
        y_bot = Text("persistent  ↓", font="Inter", color=SECOND).scale(0.3)
        y_bot.next_to([cx, cy - span_y, 0], LEFT, buff=0.18).shift(DOWN * 0.1)

        # Build fast: axes + quadrants + labels in two snappy beats (~1.4s).
        self.play(
            GrowFromCenter(x_axis), GrowFromCenter(y_axis),
            run_time=0.7,
        )
        self.play(
            FadeIn(quad_group),
            FadeIn(x_left), FadeIn(x_right), FadeIn(y_top), FadeIn(y_bot),
            run_time=0.6,
        )

        # --- Quadrant chip clusters ------------------------------------------
        # Top-left (client-starts, one-shot): amber cluster.
        tl = VGroup(
            chip("REST", AMBER),
            chip("SOAP", AMBER),
            chip("GraphQL", AMBER),
            chip("gRPC (unary)", AMBER),
        ).arrange_in_grid(rows=2, cols=2, buff=0.22)
        tl.move_to([cx - span_x / 2, cy + span_y / 2, 0])

        # Bottom-left (client-starts, persistent): mint.
        bl = VGroup(
            chip("WebSocket", MINT),
            chip("gRPC streams", MINT),
        ).arrange(DOWN, buff=0.28)
        bl.move_to([cx - span_x / 2, cy - span_y / 2, 0])

        # Top-right (server-starts, one-shot): coral.
        tr = chip("Webhook", CORAL)
        tr.move_to([cx + span_x / 2, cy + span_y / 2, 0])

        # Bottom-right (server-starts, persistent): gold.
        br = chip("SSE", GOLD)
        br.move_to([cx + span_x / 2, cy - span_y / 2, 0])

        # Pop chips quickly in small overlapping batches (~2.4s total).
        all_chips = [c for c in tl] + [c for c in bl] + [tr, br]
        for c in all_chips:
            c.home = c.get_center().copy()
        self.play(*[GrowFromCenter(c) for c in tl], lag_ratio=0.12, run_time=0.9)
        self.play(*[GrowFromCenter(c) for c in bl], lag_ratio=0.15, run_time=0.7)
        self.play(GrowFromCenter(tr), GrowFromCenter(br), run_time=0.6)

        # --- Peer-to-peer side note (WebRTC, violet) -------------------------
        side_x = cx + span_x + 2.1
        p2p_label = Text("peer ↔ peer\n(no server in the middle)",
                         font="Inter", color=SECOND, line_spacing=0.8).scale(0.28)
        p2p_label.move_to([side_x, cy + 0.9, 0])

        webrtc = chip("WebRTC", VIOLET)
        webrtc.move_to([side_x, cy + 0.1, 0])
        webrtc.home = webrtc.get_center().copy()

        # Two peer dots connected directly, to reinforce "no server".
        peer_a = Dot(color=VIOLET, radius=0.07).move_to([side_x - 0.8, cy - 0.7, 0])
        peer_b = Dot(color=VIOLET, radius=0.07).move_to([side_x + 0.8, cy - 0.7, 0])
        peer_link = Line(peer_a.get_center(), peer_b.get_center(),
                         color=VIOLET, stroke_width=2.5, stroke_opacity=0.7)

        self.play(
            FadeIn(p2p_label, shift=UP * 0.2),
            GrowFromCenter(webrtc),
            run_time=0.6,
        )
        self.play(
            FadeIn(peer_a), FadeIn(peer_b), GrowFromCenter(peer_link),
            run_time=0.5,
        )
        # Core diagram fully on screen by ~7s.

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # A single master clock (ValueTracker) drives every updater so the
        # scene is never still: chips bob + glow-breathe, axis pulses travel,
        # a highlight ring sweeps the quadrants, peers trade a dot.
        # =====================================================================
        t = ValueTracker(0.0)

        # --- Chips gently bob + breathe, each with its own phase ------------
        for i, c in enumerate(all_chips + [webrtc]):
            phase = i * 0.7
            glow = c.glow

            def make_bob(home, ph, g):
                def _upd(m):
                    tt = t.get_value()
                    m.move_to(home + np.array([0, 0.045 * np.sin(1.6 * tt + ph), 0]))
                    g.set_stroke(
                        opacity=0.18 + 0.16 * (0.5 + 0.5 * np.sin(2.1 * tt + ph))
                    )
                return _upd

            c.add_updater(make_bob(c.home, phase, glow))

        # --- Pulses travelling outward along the two axes -------------------
        # Four runners: +x, -x, +y, -y. Each is a dot that repeatedly sweeps
        # from the origin to an axis end, driven by the master clock.
        origin_pt = np.array([cx, cy, 0])
        axis_dirs = [
            (np.array([span_x, 0, 0]), AMBER, 0.0),
            (np.array([-span_x, 0, 0]), MINT, 1.0),
            (np.array([0, span_y, 0]), CORAL, 2.0),
            (np.array([0, -span_y, 0]), GOLD, 3.0),
        ]
        axis_pulses = VGroup()
        for vec, col, ph in axis_dirs:
            p = Dot(color=col, radius=0.065)

            def make_axis(vec=vec, ph=ph):
                def _upd(m):
                    frac = ((t.get_value() * 0.5 + ph) % 1.0)
                    m.move_to(origin_pt + vec * frac)
                    # Fade in near origin, out near the end.
                    m.set_opacity(np.sin(np.pi * frac) ** 0.5)
                return _upd

            p.add_updater(make_axis())
            axis_pulses.add(p)
        self.add(axis_pulses)

        # --- A soft highlight ring that sweeps from quadrant to quadrant ----
        ring = Circle(radius=1.15, color=INK, stroke_width=3, stroke_opacity=0.0)
        ring.move_to(quad_centers[0])

        def ring_upd(m):
            tt = t.get_value()
            seg = 1.4  # seconds spent drifting toward each quadrant
            idx = int((tt / seg)) % 4
            nxt = (idx + 1) % 4
            local = (tt / seg) % 1.0
            eased = rate_functions.ease_in_out_sine(local)
            pos = quad_centers[idx] * (1 - eased) + quad_centers[nxt] * eased
            m.move_to(pos)
            # Breathe opacity so the ring pulses as it lands.
            m.set_stroke(opacity=0.12 + 0.22 * np.sin(np.pi * local) ** 2)
        ring.add_updater(ring_upd)
        self.add(ring)

        # --- WebRTC peers keep trading a dot back and forth -----------------
        trade = Dot(color=VIOLET, radius=0.08)
        pa = peer_a.get_center()
        pb = peer_b.get_center()

        def trade_upd(m):
            # Ping-pong 0..1..0 along the peer link.
            frac = 0.5 - 0.5 * np.cos(t.get_value() * 2.4)
            m.move_to(pa * (1 - frac) + pb * frac)
            m.set_opacity(0.6 + 0.4 * np.sin(t.get_value() * 2.4) ** 2)
        trade.add_updater(trade_upd)

        def link_upd(m):
            m.set_stroke(opacity=0.5 + 0.4 * (0.5 + 0.5 *
                                              np.sin(t.get_value() * 2.4)))
        peer_link.add_updater(link_upd)
        self.add(trade)

        # Drive the clock continuously for ~17s of unbroken motion.
        self.play(t.animate.set_value(17.0), run_time=17.0,
                  rate_func=rate_functions.linear)

        # Clean stop so the final frame isn't mid-jitter.
        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
