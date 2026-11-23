"""Scene: The daily Git workflow as an annotated developer's-day pipeline.

Class `Workflow` (~18s). The same core loop as `Flow`, but richer: each step
is annotated with what a developer actually does during the day:

  git pull (get latest)
  git switch -c feature (new branch)
  edit · git add · git commit (small snapshots)
  git push (share)
  pull request -> review -> merge
  delete branch -> repeat

Laid out left-to-right as a pipeline that wraps to a second row. A glowing
token flows through each step lighting it up. A big caption cycles
"pull · branch · commit · push · merge" and "~99% of Git in practice".
Continuous loop, driven by a master ValueTracker.

Dark palette only, TEXT labels only.
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
    Line,
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


class Workflow(Scene):
    def construct(self):
        title = Text("A developer's day in Git", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- steps -----------------------------------------------------------
        # (command line, annotation line, accent colour)
        steps = [
            ("git pull", "get latest", GREEN),
            ("git switch -c feature", "new branch", VIOLET),
            ("edit · add · commit", "small snapshots", AMBER),
            ("git push", "share", GOLD),
            ("PR → review → merge", "team checks", TEAL),
            ("delete branch → repeat", "loop", SECOND),
        ]
        n = len(steps)

        # left-to-right pipeline that wraps: row 0 = steps 0..2, row 1 = 3..5
        per_row = 3
        col_x = [-4.3, 0.0, 4.3]
        row_y = [0.85, -1.9]

        card_w = 3.7
        nodes = []
        node_boxes = []
        node_cmds = []
        node_ann = []
        node_colors = []
        positions = []

        for i, (cmd, ann, col) in enumerate(steps):
            r = i // per_row
            c = i % per_row
            pos = np.array([col_x[c], row_y[r], 0])
            positions.append(pos)

            cmd_lbl = Text(cmd, font=MONO, color=col, weight="BOLD").scale(0.30)
            if cmd_lbl.width > card_w - 0.4:
                cmd_lbl.scale_to_fit_width(card_w - 0.4)
            ann_lbl = Text(ann, font=HEAD, color=SECOND).scale(0.26)

            box = RoundedRectangle(
                corner_radius=0.14,
                width=card_w, height=1.15,
                stroke_color=col, stroke_width=2.2,
                fill_color="#121214", fill_opacity=0.92,
            )
            box.move_to(pos)
            inner = VGroup(cmd_lbl, ann_lbl).arrange(DOWN, buff=0.14)
            inner.move_to(pos)

            grp = VGroup(box, inner)
            nodes.append(grp)
            node_boxes.append(box)
            node_cmds.append(cmd_lbl)
            node_ann.append(ann_lbl)
            node_colors.append(col)

        node_group = VGroup(*nodes)

        # --- connecting lines between consecutive steps ----------------------
        connectors = VGroup()
        for i in range(n):
            j = (i + 1) % n
            p0 = positions[i]
            p1 = positions[j]
            ri, rj = i // per_row, j // per_row
            box_i = node_boxes[i]
            box_j = node_boxes[j]
            if i == n - 1:
                # wrap from last back to first: route under, up the left
                start = box_i.get_bottom() + DOWN * 0.02
                end = box_j.get_left() + LEFT * 0.02
                line = Line(start, end, stroke_color=SECOND,
                            stroke_width=1.8, stroke_opacity=0.28)
            elif ri == rj:
                start = box_i.get_right()
                end = box_j.get_left()
                line = Line(start, end, stroke_color=SECOND,
                            stroke_width=2.0, stroke_opacity=0.4)
            else:
                # row wrap: right edge of last-in-row down to next row
                start = box_i.get_right()
                end = box_j.get_left()
                line = Line(start, end, stroke_color=SECOND,
                            stroke_width=1.8, stroke_opacity=0.28)
            connectors.add(line)

        self.play(Create(connectors), run_time=0.8)
        self.play(*[GrowFromCenter(nd) for nd in nodes],
                  lag_ratio=0.08, run_time=1.1)

        # --- big cycling caption at the bottom -------------------------------
        caption = Text("pull · branch · commit · push · merge",
                       font=MONO, color=INK, weight="BOLD").scale(0.44)
        caption.to_edge(DOWN, buff=0.45)
        caption._phase = 0
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        seg = 2.0  # seconds per step

        # Node highlight + breathing (closure factory, locals captured).
        def make_node_updater(box_m, cmd_m, ann_m, base_col, idx):
            bright = ManimColor(base_col)
            ink = ManimColor(INK)
            base_fill = ManimColor("#121214")

            def _upd(m):
                tt = t.get_value()
                phase = (tt / seg) % n
                d = min((idx - phase) % n, (phase - idx) % n)
                near = np.clip(1.0 - d, 0.0, 1.0)
                breathe = 0.5 + 0.5 * np.sin(1.3 * tt + idx * 0.6)
                sw = 2.0 + 1.2 * breathe + 4.5 * near
                box_m.set_stroke(color=base_col, width=sw)
                box_m.set_fill(
                    color=interpolate_color(base_fill, bright, 0.20 * near),
                    opacity=0.92,
                )
                cmd_m.set_color(interpolate_color(bright, ink, 0.5 * near))
                ann_m.set_opacity(0.55 + 0.45 * near)
            return _upd

        for i in range(n):
            node_boxes[i].add_updater(
                make_node_updater(node_boxes[i], node_cmds[i], node_ann[i],
                                  node_colors[i], i))

        # --- flowing token ---------------------------------------------------
        token = Dot(color=INK, radius=0.13)
        token.move_to(positions[0])
        self.add(token)

        def token_updater(m):
            tt = t.get_value()
            prog = (tt / seg) % n
            i0 = int(np.floor(prog)) % n
            i1 = (i0 + 1) % n
            frac = prog - np.floor(prog)
            eased = rate_functions.ease_in_out_cubic(frac)
            p0 = positions[i0]
            p1 = positions[i1]
            pos = p0 * (1 - eased) + p1 * eased
            # arc a touch above the straight line for a lively path
            lift = 0.35 * np.sin(np.pi * frac)
            m.move_to(pos + UP * lift)
            col = ManimColor(node_colors[i1])
            m.set_color(interpolate_color(ManimColor(INK), col, 0.55))
            m.set_opacity(0.82 + 0.18 * np.sin(6.0 * tt))

        token.add_updater(token_updater)

        # --- caption cycling between two lines -------------------------------
        cap_lines = [
            ("pull · branch · commit · push · merge", INK),
            ("~99% of Git in practice", GREEN),
        ]

        def caption_updater(m):
            idx = int(t.get_value() // 3.0) % len(cap_lines)
            if idx != m._phase:
                m._phase = idx
                text, col = cap_lines[idx]
                new = Text(text, font=MONO, color=col,
                           weight="BOLD").scale(0.44)
                new.to_edge(DOWN, buff=0.45)
                new._phase = idx
                m.become(new)
                m._phase = idx
            # gentle pulse
            m.set_opacity(0.8 + 0.2 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 2.0)))

        caption.add_updater(caption_updater)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
