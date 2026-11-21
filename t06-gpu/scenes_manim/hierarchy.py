"""Hierarchy — zoom into the die: DIE -> GPC -> SM -> WARP -> CUDA CORES.

Nested boxes reveal the fractal hierarchy of a GPU. A highlight descends level
by level on a loop, and the smallest CUDA cores shimmer as a grid. ~24s.
"""

import math

from manim import (
    Scene,
    VGroup,
    RoundedRectangle,
    Text,
    ValueTracker,
    Write,
    FadeIn,
    Create,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

BG = "#07090A"
INK = "#E9EAE6"
SUB = "#8A8C88"
GREEN = "#39FF88"
TEAL = "#2DD4BF"
LIME = "#C6FF4D"

MONO = "JetBrains Mono"
HEAD = "Inter"


class Hierarchy(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Inside the die", font=HEAD, color=INK,
                     weight="BOLD").scale(0.8).to_edge(UP, buff=0.45)
        self.play(Write(title, run_time=0.7))

        # Each level: (name, count, color). Drawn as nested boxes, biggest
        # on the left, zooming inward to the right.
        levels = [
            ("DIE", "1 chip", TEAL),
            ("GPC", "~7 clusters", LIME),
            ("SM", "~14 per GPC", GREEN),
            ("WARP", "32 threads", LIME),
            ("CUDA CORES", "thousands", GREEN),
        ]

        # Build nested concentric rounded rectangles.
        boxes = VGroup()
        labels = VGroup()
        counts = VGroup()
        n = len(levels)
        max_w, max_h = 11.0, 5.4
        for i, (name, count, col) in enumerate(levels):
            shrink = 1.0 - i * 0.165
            w = max_w * shrink
            h = max_h * shrink
            box = RoundedRectangle(width=w, height=h, corner_radius=0.18,
                                   stroke_color=col, stroke_width=2.2,
                                   fill_color=col, fill_opacity=0.03)
            box.move_to([0, -0.25, 0])
            boxes.add(box)

            lbl = Text(name, font=MONO, color=col, weight="BOLD").scale(0.46)
            # place label at top edge of its box
            lbl.move_to([box.get_left()[0] + 0.1 + lbl.width / 2,
                         box.get_top()[1] - 0.26, 0])
            labels.add(lbl)

            cnt = Text(count, font=MONO, color=SUB).scale(0.34)
            cnt.next_to(lbl, RIGHT, buff=0.3)
            counts.add(cnt)

        self.play(Create(boxes, run_time=1.6))
        self.play(FadeIn(labels, run_time=0.8), FadeIn(counts, run_time=0.8))

        # Innermost: a shimmering grid of CUDA cores.
        inner = boxes[-1]
        grid = VGroup()
        gcols, grows = 10, 5
        cs = 0.2
        gp = 0.06
        gw = gcols * (cs + gp)
        gh = grows * (cs + gp)
        ox = inner.get_center()[0] - gw / 2 + cs / 2
        oy = inner.get_center()[1] - gh / 2 + cs / 2 - 0.05
        for r in range(grows):
            for c in range(gcols):
                d = RoundedRectangle(width=cs, height=cs, corner_radius=0.03,
                                     stroke_color=GREEN, stroke_width=0.8,
                                     fill_color=GREEN, fill_opacity=0.1)
                d.move_to([ox + c * (cs + gp), oy + r * (cs + gp), 0])
                grid.add(d)
        self.play(FadeIn(grid, run_time=0.6))

        # ---------------- Master clock: descending highlight loop ---------
        clock = ValueTracker(0.0)
        period = 5.0  # seconds to sweep through all levels once

        def box_updater_factory(idx):
            col = levels[idx][2]

            def upd(m):
                t = clock.get_value()
                active = int((t % period) / period * n) % n
                if idx == active:
                    glow = 0.5 + 0.5 * math.sin(t * 4.0)
                    m.set_stroke(col, width=3.5 + 2.5 * glow, opacity=1.0)
                    m.set_fill(col, opacity=0.1 + 0.08 * glow)
                else:
                    m.set_stroke(col, width=2.2, opacity=0.5)
                    m.set_fill(col, opacity=0.03)
            return upd

        for i in range(n):
            boxes[i].add_updater(box_updater_factory(i))

        def label_updater_factory(idx):
            def upd(m):
                t = clock.get_value()
                active = int((t % period) / period * n) % n
                m.set_opacity(1.0 if idx == active else 0.55)
            return upd

        for i in range(n):
            labels[i].add_updater(label_updater_factory(i))

        def grid_updater(m):
            t = clock.get_value()
            for k, d in enumerate(m):
                # per-cell shimmer phase offset -> twinkling grid
                ph = math.sin(t * 3.0 + k * 0.7)
                op = 0.15 + 0.6 * (0.5 + 0.5 * ph)
                d.set_fill(GREEN, opacity=op)
                d.set_stroke(GREEN, opacity=0.4 + 0.5 * (0.5 + 0.5 * ph))

        grid.add_updater(grid_updater)

        total = 20.0
        steps = 5
        for i in range(steps):
            self.play(clock.animate.set_value((i + 1) * total / steps),
                      run_time=total / steps, rate_func=rate_functions.linear)

        for i in range(n):
            boxes[i].clear_updaters()
            labels[i].clear_updaters()
        grid.clear_updaters()
        for d in grid:
            d.set_fill(GREEN, opacity=0.6)
            d.set_stroke(GREEN, opacity=0.8)
        self.wait(0.3)
