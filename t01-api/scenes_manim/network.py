"""NetworkField scene for "What Is an API?".

Concept: "software stands on top of other software." An abstract, elegant
lattice of small app nodes connected by thin lines. Pulses of light travel
along the edges continuously; a few nodes light up in sequence. Calm and
ambient — used as an interstitial.

Dark design system (shared with the Remotion video):
  bg      #0A0A0C
  ink     warm cream #EDE7DB   secondary #9A958C
  accents amber #FFC24B, magenta #FF3E7F, mint #3DE0B0,
          violet #B06BFF, coral #FF6B4A, gold #E8C24A
  (NO blue, NO pure white)

Rendered at 1920x1080. No external assets. Reveals then holds with continuous
ambient pulses. Approximate runtime: ~26 seconds.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    VGroup,
    Dot,
    Line,
    Circle,
    MoveAlongPath,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    there_and_back,
    smooth,
    linear,
    ORIGIN,
)

# ---- Dark palette ------------------------------------------------------------
BG = "#0A0A0C"
INK = "#EDE7DB"
INK_SOFT = "#9A958C"
PAPER = "#141418"   # node fill: a touch lighter than the background
LINE = "#2A2A30"

AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

# Aliases so the original animation code reads unchanged.
BLUE = MAGENTA
GREEN = MINT
PINK = CORAL
SKY = GOLD

ACCENTS = [AMBER, MAGENTA, MINT, VIOLET, CORAL, GOLD]

FONT = "Inter"


def node(center, color):
    """A small rounded 'app' tile with a subtle inner dot."""
    tile = RoundedRectangle(
        corner_radius=0.14,
        width=0.68,
        height=0.68,
        fill_color=PAPER,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=2.5,
    )
    inner = Dot(radius=0.09, color=color)
    inner.set_fill(color, opacity=0.9)
    g = VGroup(tile, inner)
    g.move_to(center)
    return g


class NetworkField(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Lay out ~9 nodes loosely across the frame ---------------------
        # Hand-placed positions (x, y) keep the lattice organic but balanced,
        # with comfortable margins inside the 1920x1080 frame.
        positions = [
            (-5.2,  1.9),
            (-3.0,  2.7),
            (-0.4,  2.0),
            ( 2.3,  2.6),
            ( 5.0,  1.6),
            (-4.4, -0.6),
            (-1.6, -1.1),
            ( 1.4, -0.4),
            ( 4.2, -1.7),
        ]
        coords = [np.array([x, y, 0.0]) for (x, y) in positions]

        nodes = VGroup()
        for i, c in enumerate(coords):
            nodes.add(node(c, ACCENTS[i % len(ACCENTS)]))

        # --- Define the edges (which nodes connect) ------------------------
        # A loosely-woven lattice: each node links to a couple of neighbours.
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (1, 6), (2, 6), (2, 7),
            (3, 7), (4, 8), (5, 6), (6, 7),
            (7, 8), (1, 5), (3, 8),
        ]

        edge_lines = VGroup()
        edge_segments = []  # keep plain Line geometry for pulse paths
        for a, b in edges:
            seg = Line(
                coords[a], coords[b],
                stroke_color=LINE,
                stroke_width=1.6,
                stroke_opacity=0.9,
            )
            edge_lines.add(seg)
            edge_segments.append((seg, a, b))

        # --- Reveal: lines draw in, then nodes fade up ---------------------
        self.play(
            Create(edge_lines, lag_ratio=0.06),
            run_time=1.5,
        )
        self.play(
            FadeIn(nodes, scale=0.85, lag_ratio=0.08),
            run_time=1.1,
        )

        # --- Helper: one travelling light pulse along an edge --------------
        def pulse_along(seg, color, run_time=1.1, reverse=False):
            start = seg.get_end() if reverse else seg.get_start()
            end = seg.get_start() if reverse else seg.get_end()
            path = Line(start, end)
            glow = Dot(start, radius=0.08, color=color)
            glow.set_fill(color, opacity=1.0)
            halo = Circle(radius=0.16, stroke_width=0,
                          fill_color=color, fill_opacity=0.22)
            halo.move_to(start)
            pulse = VGroup(halo, glow)
            return pulse, MoveAlongPath(pulse, path, rate_func=linear,
                                        run_time=run_time)

        # --- Ambient phase: continuous pulses + sequenced node lighting -----
        # We run several overlapping waves so motion never fully stops.
        waves = [
            # (edge index, accent color, reverse, node-to-indicate)
            (1, BLUE, False, 2),
            (5, VIOLET, False, 6),
            (3, SKY, True, 3),
            (11, GREEN, False, 7),
            (9, PINK, False, 8),
            (0, AMBER, False, 1),
            (12, BLUE, True, 7),
        ]

        for idx, (ei, col, rev, node_i) in enumerate(waves):
            seg = edge_segments[ei][0]
            pulse, move = pulse_along(seg, col, run_time=0.9, reverse=rev)

            # Light up the destination node as the pulse travels.
            lit = nodes[node_i]
            self.play(
                move,
                Indicate(lit, color=col, scale_factor=1.18,
                         rate_func=there_and_back),
                run_time=0.9,
            )
            self.remove(pulse)

        # --- A final shimmer: a few pulses fire together, then settle ------
        combo = []
        pulses = []
        for ei, col, rev in [(2, GREEN, False), (6, PINK, True),
                             (10, SKY, False)]:
            seg = edge_segments[ei][0]
            pulse, move = pulse_along(seg, col, run_time=1.2, reverse=rev)
            pulses.append(pulse)
            combo.append(move)
        self.play(*combo, run_time=1.2)
        for p in pulses:
            self.remove(p)

        self.wait(0.6)

        # --- HOLD: run continuous overlapping pulse waves across the lattice.
        # This keeps the lattice alive for a long, stable hold so the Remotion
        # compositor can overlay captions and cut wherever it needs to.
        hold_waves = [
            (4, AMBER, False, 4), (7, MINT, False, 7), (8, VIOLET, True, 3),
            (13, CORAL, False, 5), (14, GOLD, False, 8), (2, MAGENTA, False, 3),
            (6, MINT, True, 6), (10, AMBER, False, 6), (0, VIOLET, False, 0),
            (11, CORAL, True, 8), (5, GOLD, False, 5), (1, MAGENTA, True, 1),
        ]

        # Several loops of the wave list give ~10s of ambient motion.
        for loop in range(3):
            for ei, col, rev, node_i in hold_waves:
                seg = edge_segments[ei][0]
                pulse, move = pulse_along(seg, col, run_time=0.75,
                                          reverse=rev)
                lit = nodes[node_i]
                self.play(
                    move,
                    Indicate(lit, color=col, scale_factor=1.14,
                             rate_func=there_and_back),
                    run_time=0.75,
                )
                self.remove(pulse)

        self.wait(1.0)
