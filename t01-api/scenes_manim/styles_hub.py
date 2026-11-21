"""StylesHub scene for "What Is an API?".

Concept: there are many API *styles* (REST, SOAP, GraphQL, gRPC, MQTT) but
they all honour the same contract — a request goes in, a response comes back.
A central node holds the contract; five style nodes orbit it in a pentagon,
each connected by a line that pulses a light inward.

Dark design system (shared with the Remotion video):
  bg      #0A0A0C
  ink     warm cream #EDE7DB   secondary #9A958C
  accents amber #FFC24B, magenta #FF3E7F, mint #3DE0B0,
          violet #B06BFF, coral #FF6B4A, gold #E8C24A
  (NO blue, NO pure white)

Rendered at 1920x1080. No external assets. Builds over ~12s then holds with
gently pulsing connector lines. Approximate runtime: ~26 seconds.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Circle,
    Text,
    VGroup,
    Dot,
    Line,
    MoveAlongPath,
    Create,
    FadeIn,
    GrowFromCenter,
    smooth,
    linear,
    there_and_back,
    UP,
    DOWN,
    ORIGIN,
)

# ---- Dark palette ------------------------------------------------------------
BG = "#0A0A0C"
INK = "#EDE7DB"
INK_SOFT = "#9A958C"

AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

FONT = "Inter"


def style_node(label, color, width=2.2, height=1.0):
    """A glowing rounded card for one API style."""
    halo = RoundedRectangle(
        corner_radius=0.2, width=width, height=height,
        stroke_color=color, stroke_width=10, stroke_opacity=0.18,
        fill_opacity=0.0,
    )
    body = RoundedRectangle(
        corner_radius=0.2, width=width, height=height,
        stroke_color=color, stroke_width=2.8,
        fill_color=color, fill_opacity=0.10,
    )
    txt = Text(label, font=FONT, font_size=28, color=INK)
    txt.move_to(body.get_center())
    return VGroup(halo, body, txt)


class StylesHub(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Central contract node ------------------------------------------
        ring_halo = Circle(radius=1.55, stroke_color=MAGENTA,
                           stroke_width=12, stroke_opacity=0.16)
        ring = Circle(radius=1.5, stroke_color=MAGENTA, stroke_width=3.0,
                      fill_color=MAGENTA, fill_opacity=0.06)
        center_text = VGroup(
            Text("Same contract", font=FONT, font_size=26, color=INK),
            Text("request -> response", font=FONT, font_size=22,
                 color=INK_SOFT),
        ).arrange(DOWN, buff=0.18)
        center_text.move_to(ORIGIN)
        center = VGroup(ring_halo, ring, center_text)

        self.play(GrowFromCenter(center), run_time=1.0)

        # --- Pentagon of five orbiting style nodes --------------------------
        styles = [
            ("REST", AMBER),
            ("SOAP", VIOLET),
            ("GraphQL", MAGENTA),
            ("gRPC", MINT),
            ("MQTT", CORAL),
        ]
        orbit_r = 3.55
        nodes = []
        connectors = []  # (line, color) kept for the ambient hold

        # Start at the top and go clockwise for an even pentagon.
        for i, (label, color) in enumerate(styles):
            angle = np.pi / 2 - i * (2 * np.pi / 5)
            pos = np.array([orbit_r * np.cos(angle),
                            orbit_r * np.sin(angle), 0.0])
            node = style_node(label, color)
            node.move_to(pos)

            # Connector from the ring edge toward the node.
            direction = pos / np.linalg.norm(pos)
            line_start = direction * 1.55
            line_end = pos - direction * 1.15
            line = Line(line_start, line_end, stroke_color=color,
                        stroke_width=2.2, stroke_opacity=0.35)

            # Pop the node in, draw its line, send a pulse inward.
            self.play(
                FadeIn(node, scale=0.7),
                Create(line),
                run_time=0.55,
            )
            self._pulse_inward(line, color, run_time=0.5)

            nodes.append(node)
            connectors.append((line, color))

        self.wait(0.6)

        # --- HOLD: connector lines gently pulse light inward, looping -------
        for _ in range(4):
            # Fire pulses on all five lines together (staggered via run_time).
            pulses = []
            moves = []
            for line, color in connectors:
                pulse, move = self._make_inward_pulse(line, color,
                                                       run_time=1.1)
                pulses.append(pulse)
                moves.append(move)
            # Also give the central ring a soft breath.
            self.play(
                *moves,
                ring.animate.set_stroke(width=4.5, opacity=0.9),
                rate_func=there_and_back,
                run_time=1.1,
            )
            for p in pulses:
                self.remove(p)
            self.wait(0.4)

        self.wait(1.0)

    # ---- pulse helpers -----------------------------------------------------
    def _make_inward_pulse(self, line, color, run_time=1.0):
        """Build a glowing dot + its MoveAlongPath (node -> center)."""
        start = line.get_end()
        end = line.get_start()
        path = Line(start, end)
        glow = Dot(start, radius=0.09, color=color)
        glow.set_fill(color, opacity=1.0)
        halo = Circle(radius=0.18, stroke_width=0,
                      fill_color=color, fill_opacity=0.22)
        halo.move_to(start)
        pulse = VGroup(halo, glow)
        return pulse, MoveAlongPath(pulse, path, rate_func=linear,
                                    run_time=run_time)

    def _pulse_inward(self, line, color, run_time=0.5):
        pulse, move = self._make_inward_pulse(line, color, run_time=run_time)
        self.play(move, run_time=run_time)
        self.remove(pulse)
