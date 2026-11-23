"""Scene: The daily Git workflow as a clean cycle ring.

Class `Flow` (~18s). Core daily loop laid out as a ring of labelled command
nodes: pull -> branch -> add -> commit -> push -> merge -> (back to pull).
A glowing token orbits the ring, lighting each command node as it arrives.
Arrows connect the nodes in order. Title "THE DAILY WORKFLOW". Legible enough
to sit faintly behind an intro title.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  second #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    Arc,
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
    PI,
    TAU,
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


class Flow(Scene):
    def construct(self):
        title = Text("THE DAILY WORKFLOW", font=HEAD, color=INK,
                     weight="BOLD").scale(0.62)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- ring geometry ---------------------------------------------------
        center = DOWN * 0.45
        radius = 2.75
        # order: pull -> branch -> add -> commit -> push -> merge -> back
        steps = [
            ("git pull", GREEN),
            ("git branch", VIOLET),
            ("git add", AMBER),
            ("git commit", AMBER),
            ("git push", GOLD),
            ("git merge", TEAL),
        ]
        n = len(steps)
        # Start at top, go clockwise.
        angles = [PI / 2 - i * TAU / n for i in range(n)]
        positions = [center + radius * np.array([np.cos(a), np.sin(a), 0])
                     for a in angles]

        # --- node mobjects ---------------------------------------------------
        nodes = []            # list of VGroup
        node_boxes = []       # box per node (for glow control)
        node_labels = []      # label per node
        node_colors = []
        for i, (cmd, col) in enumerate(steps):
            lbl = Text(cmd, font=MONO, color=col, weight="BOLD").scale(0.34)
            box = RoundedRectangle(
                corner_radius=0.12,
                width=lbl.width + 0.5, height=0.72,
                stroke_color=col, stroke_width=2.2,
                fill_color="#121214", fill_opacity=0.92,
            )
            box.move_to(positions[i])
            lbl.move_to(positions[i])
            grp = VGroup(box, lbl)
            nodes.append(grp)
            node_boxes.append(box)
            node_labels.append(lbl)
            node_colors.append(col)

        node_group = VGroup(*nodes)

        # --- connecting arcs between consecutive nodes -----------------------
        arcs = VGroup()
        for i in range(n):
            a0 = angles[i]
            # trimmed clockwise arc segment toward the next node, kept off boxes
            arc = Arc(
                radius=radius,
                start_angle=a0 - 0.30,
                angle=-(TAU / n) + 0.60,
                arc_center=center,
                stroke_color=SECOND, stroke_width=2.0, stroke_opacity=0.35,
            )
            arcs.add(arc)

        self.play(Create(arcs), run_time=0.8)
        self.play(*[GrowFromCenter(nd) for nd in nodes],
                  lag_ratio=0.08, run_time=1.0)

        caption = Text("pull  ·  branch  ·  add  ·  commit  ·  push  ·  merge",
                       font=MONO, color=SECOND).scale(0.30)
        caption.next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(caption), run_time=0.4)

        # --- glowing orbiting token -----------------------------------------
        token = Dot(color=INK, radius=0.14)
        token.move_to(positions[0])
        self.add(token)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Node breathing + arrival highlight updaters (closure factory).
        def make_node_updater(box_m, lbl_m, base_col, idx):
            dim = ManimColor(SECOND)
            bright = ManimColor(base_col)
            ink = ManimColor(INK)

            def _upd(m):
                tt = t.get_value()
                # token progresses one node every `seg` seconds
                seg = 1.9
                phase = (tt / seg) % n
                # distance (in node steps) from current token slot
                d = min((idx - phase) % n, (phase - idx) % n)
                near = np.clip(1.0 - d, 0.0, 1.0)  # 1 when token on this node
                breathe = 0.5 + 0.5 * np.sin(1.4 * tt + idx * 0.7)
                sw = 2.0 + 1.4 * breathe + 4.5 * near
                box_m.set_stroke(color=base_col, width=sw)
                box_m.set_fill(
                    color=interpolate_color(ManimColor("#121214"),
                                            bright, 0.18 * near),
                    opacity=0.92,
                )
                lbl_m.set_color(interpolate_color(bright, ink, 0.55 * near))
            return _upd

        for i in range(n):
            node_boxes[i].add_updater(
                make_node_updater(node_boxes[i], node_labels[i],
                                  node_colors[i], i))

        # Token orbit updater: glide around the ring, easing into each node.
        def token_updater(m):
            tt = t.get_value()
            seg = 1.9
            prog = (tt / seg) % n
            i0 = int(np.floor(prog)) % n
            i1 = (i0 + 1) % n
            frac = prog - np.floor(prog)
            a0 = angles[i0]
            a1 = angles[i1]
            # unwrap so clockwise step is a short negative arc
            da = a1 - a0
            if da > 0:
                da -= TAU
            eased = rate_functions.ease_in_out_cubic(frac)
            a = a0 + da * eased
            pos = center + radius * np.array([np.cos(a), np.sin(a), 0])
            m.move_to(pos)
            # pulse colour by the node it is heading toward
            col = ManimColor(node_colors[i1])
            glow = 0.55 + 0.45 * np.sin(6.0 * tt)
            m.set_color(interpolate_color(ManimColor(INK), col, 0.6))
            m.set_opacity(0.8 + 0.2 * glow)

        token.add_updater(token_updater)

        # faint center hub label
        hub = Text("repo", font=MONO, color=SECOND).scale(0.30)
        hub.move_to(center)

        def hub_upd(m):
            m.set_opacity(0.35 + 0.25 * (0.5 + 0.5 *
                                         np.sin(t.get_value() * 1.2)))
        hub.add_updater(hub_upd)
        self.add(hub)

        # 18s ~ a bit more than one full lap (6 nodes * 1.9s = 11.4s/lap)
        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
