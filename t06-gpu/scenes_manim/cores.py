"""Cores — CPU (few big cores, sequential) vs GPU (many tiny cores, parallel).

The signature scene. LEFT: a CPU with a few big coral cores processing a task
token ONE AT A TIME. RIGHT: a GPU grid of many tiny green cores that ALL light
up AT ONCE processing a whole batch. Both loop continuously so the contrast
sequential-vs-parallel never stops. ~24s.
"""

import math

from manim import (
    Scene,
    VGroup,
    RoundedRectangle,
    Text,
    Line,
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
CORAL = "#FF6B4A"

MONO = "JetBrains Mono"
HEAD = "Inter"


class Cores(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("One at a time  vs  all at once", font=HEAD,
                     color=INK, weight="BOLD").scale(0.8).to_edge(UP, buff=0.45)
        self.play(Write(title, run_time=0.8))

        divider = Line([0, -3.2, 0], [0, 2.4, 0], color=SUB, stroke_width=1.2)
        divider.set_opacity(0.4)
        self.add(divider)

        # ---------------- LEFT: CPU, a few big cores, sequential ----------
        cpu_label = Text("CPU", font=HEAD, color=CORAL, weight="BOLD").scale(0.7)
        cpu_label.move_to([-4.0, 1.9, 0])
        cpu_sub = Text("4-24 big cores", font=MONO, color=SUB).scale(0.4)
        cpu_sub.next_to(cpu_label, DOWN, buff=0.15)

        n_cpu = 4
        cpu_cores = VGroup()
        cpu_y = 0.0
        cpu_xs = [-5.6, -4.4, -3.2, -2.0]
        for x in cpu_xs:
            glow = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.12,
                                    stroke_color=CORAL, stroke_width=10,
                                    fill_opacity=0.0).set_stroke(opacity=0.0)
            core = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1,
                                    stroke_color=CORAL, stroke_width=2,
                                    fill_color=CORAL, fill_opacity=0.08)
            core.move_to([x, cpu_y, 0])
            glow.move_to([x, cpu_y, 0])
            cpu_cores.add(VGroup(glow, core))

        self.play(FadeIn(cpu_label), FadeIn(cpu_sub),
                  Create(cpu_cores, run_time=1.0))

        # Task token that marches through each core in turn.
        token = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08,
                                 stroke_color=INK, stroke_width=2,
                                 fill_color=CORAL, fill_opacity=0.9)
        token.move_to([cpu_xs[0], cpu_y + 1.4, 0])
        self.add(token)

        # ---------------- RIGHT: GPU, big grid, all parallel --------------
        gpu_label = Text("GPU", font=HEAD, color=GREEN, weight="BOLD").scale(0.7)
        gpu_label.move_to([4.0, 1.9, 0])
        gpu_sub = Text("thousands of small cores", font=MONO, color=SUB).scale(0.4)
        gpu_sub.next_to(gpu_label, DOWN, buff=0.15)

        cols, rows = 12, 8
        cell = 0.34
        gap = 0.06
        grid = VGroup()
        gx0 = 1.4
        gy0 = 1.0
        for r in range(rows):
            for c in range(cols):
                sq = RoundedRectangle(
                    width=cell, height=cell, corner_radius=0.05,
                    stroke_color=GREEN, stroke_width=1.2,
                    fill_color=GREEN, fill_opacity=0.08)
                sq.move_to([gx0 + c * (cell + gap),
                            gy0 - r * (cell + gap), 0])
                grid.add(sq)
        grid.move_to([4.0, 0.0, 0])

        self.play(FadeIn(gpu_label), FadeIn(gpu_sub),
                  FadeIn(grid, run_time=0.9))

        batch_cap = Text("whole batch in parallel", font=MONO,
                         color=GREEN).scale(0.42)
        batch_cap.move_to([4.0, -2.6, 0])
        seq_cap = Text("one task, then the next", font=MONO,
                       color=CORAL).scale(0.42)
        seq_cap.move_to([-3.8, -2.6, 0])
        self.play(FadeIn(batch_cap), FadeIn(seq_cap))

        # ---------------- Master clock drives both loops ------------------
        clock = ValueTracker(0.0)
        period = 4.0  # seconds per full CPU sweep / GPU pulse cycle

        def cpu_updater(mob):
            t = clock.get_value()
            phase = (t % period) / period  # 0..1 across the 4 cores
            active = min(n_cpu - 1, int(phase * n_cpu))
            frac = (phase * n_cpu) - active  # 0..1 within current core
            # Move token horizontally core to core; drop into the active core.
            x = cpu_xs[active]
            # ease a little travel between cores
            if active < n_cpu - 1:
                x = cpu_xs[active] + frac * (cpu_xs[active + 1] - cpu_xs[active]) * 0.0
            mob.move_to([x, cpu_y, 0])

        token.add_updater(cpu_updater)

        def cpu_core_updater_factory(idx):
            glow, core = cpu_cores[idx]

            def upd(m):
                t = clock.get_value()
                phase = (t % period) / period
                active = min(n_cpu - 1, int(phase * n_cpu))
                on = (idx == active)
                glow, core = m
                if on:
                    core.set_fill(CORAL, opacity=0.65)
                    glow.set_stroke(CORAL, opacity=0.35)
                else:
                    core.set_fill(CORAL, opacity=0.08)
                    glow.set_stroke(CORAL, opacity=0.0)
            return upd

        for i in range(n_cpu):
            cpu_cores[i].add_updater(cpu_core_updater_factory(i))

        def grid_updater(m):
            t = clock.get_value()
            # All cells pulse TOGETHER (parallel) — one shared pulse.
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (t % period) / period)
            op = 0.1 + 0.7 * pulse
            sw = 1.2 + 2.2 * pulse
            for sq in m:
                sq.set_fill(GREEN, opacity=op)
                sq.set_stroke(GREEN, width=sw, opacity=0.6 + 0.4 * pulse)

        grid.add_updater(grid_updater)

        # Run the loop continuously for the full duration.
        total = 20.0
        steps = 5
        for i in range(steps):
            self.play(clock.animate.set_value((i + 1) * total / steps),
                      run_time=total / steps, rate_func=rate_functions.linear)

        # Clean final frame.
        token.clear_updaters()
        grid.clear_updaters()
        for i in range(n_cpu):
            cpu_cores[i].clear_updaters()
        for sq in grid:
            sq.set_fill(GREEN, opacity=0.75)
            sq.set_stroke(GREEN, width=2.0, opacity=0.9)
        self.wait(0.3)
