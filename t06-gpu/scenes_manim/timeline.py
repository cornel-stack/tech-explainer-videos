"""Timeline — the AI explosion. A steeply rising curve from 2012 to today.

From "2012 . AlexNet on 2 gaming GPUs . ~1.5 GB each" rising to
"today . data-centre GPUs . ~141 GB". A climbing counter and a marker ride
the curve, with labelled milestones. Marked "illustrative". ~24s.
amber/violet/green.
"""

import math

from manim import (
    Scene,
    VGroup,
    RoundedRectangle,
    Text,
    Line,
    Dot,
    VMobject,
    ValueTracker,
    Write,
    FadeIn,
    Create,
    always_redraw,
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
VIOLET = "#B06BFF"
AMBER = "#FFB020"

MONO = "JetBrains Mono"
HEAD = "Inter"


class Timeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("The AI explosion", font=HEAD, color=INK,
                     weight="BOLD").scale(0.8).to_edge(UP, buff=0.4)
        illus = Text("illustrative", font=MONO, color=SUB).scale(0.35)
        illus.to_corner(UP + RIGHT, buff=0.5)
        self.play(Write(title, run_time=0.7), FadeIn(illus))

        # ---------------- Axes --------------------------------------------
        x_left, x_right = -6.0, 6.0
        y_bot, y_top = -2.8, 2.6
        x_axis = Line([x_left, y_bot, 0], [x_right, y_bot, 0],
                      color=SUB, stroke_width=2)
        y_axis = Line([x_left, y_bot, 0], [x_left, y_top, 0],
                      color=SUB, stroke_width=2)
        y_label = Text("memory per GPU", font=MONO, color=SUB).scale(0.36)
        y_label.rotate(math.pi / 2).next_to(y_axis, LEFT, buff=0.15)
        self.play(Create(x_axis, run_time=0.4), Create(y_axis, run_time=0.4),
                  FadeIn(y_label))

        # Map curve parameter u in [0,1] -> screen point. Steeply rising.
        def curve_point(u):
            x = x_left + u * (x_right - x_left)
            # exponential-ish steep rise, normalised
            h = (math.exp(2.6 * u) - 1) / (math.exp(2.6) - 1)
            y = y_bot + h * (y_top - y_bot)
            return [x, y, 0]

        # ---------------- Milestones --------------------------------------
        # (u-position, year, text, memory-GB, color)
        milestones = [
            (0.03, "2012", "AlexNet . 2 gaming GPUs", 1.5, AMBER),
            (0.5, "~2018", "big training GPUs", 32, VIOLET),
            (0.97, "today", "data-centre GPUs", 141, GREEN),
        ]

        clock = ValueTracker(0.0)
        reveal = ValueTracker(0.0)  # 0..1 how much of the curve is drawn

        # The rising curve, drawn progressively via `reveal`.
        def make_curve():
            vm = VMobject()
            u_max = max(1e-3, reveal.get_value())
            pts = [curve_point(u_max * i / 40.0) for i in range(41)]
            vm.set_points_smoothly(pts)
            vm.set_stroke(VIOLET, width=4)
            return vm

        curve_glow = always_redraw(
            lambda: make_curve().set_stroke(VIOLET, width=12, opacity=0.18))
        curve = always_redraw(make_curve)
        self.add(curve_glow, curve)

        # Climbing marker that rides the drawn tip of the curve.
        tip = always_redraw(
            lambda: Dot(curve_point(reveal.get_value()), color=AMBER, radius=0.1))
        tip_glow = always_redraw(
            lambda: Dot(curve_point(reveal.get_value()),
                        color=AMBER, radius=0.22).set_opacity(0.3))
        self.add(tip_glow, tip)

        # Climbing memory counter near the marker.
        def counter_text():
            u = reveal.get_value()
            # interpolate memory along the curve (exp-ish between endpoints)
            gb = 1.5 * (141.0 / 1.5) ** u
            p = curve_point(u)
            t = Text(f"~{gb:,.0f} GB", font=MONO, color=AMBER).scale(0.5)
            t.move_to([p[0], p[1] + 0.5, 0])
            return t

        counter = always_redraw(counter_text)
        self.add(counter)

        # Reveal the curve across the first ~7s.
        self.play(reveal.animate.set_value(1.0), run_time=7.0,
                  rate_func=rate_functions.ease_in_out_sine)

        # Place milestone labels + dots now that the curve exists.
        ms_group = VGroup()
        for u, year, txt, gb, col in milestones:
            p = curve_point(u)
            d = Dot(p, color=col, radius=0.08)
            yr = Text(year, font=MONO, color=col, weight="BOLD").scale(0.42)
            lbl = Text(txt, font=MONO, color=INK).scale(0.34)
            mem = Text(f"~{gb:,.0f} GB each", font=MONO, color=SUB).scale(0.3)
            stack = VGroup(yr, lbl, mem).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            # keep labels inside frame
            dx = 0.3 if u < 0.85 else -stack.width - 0.3
            stack.move_to([p[0] + dx + stack.width / 2, p[1] - 0.9, 0])
            ms_group.add(VGroup(d, stack))
        self.play(FadeIn(ms_group, run_time=0.9))

        # ---------------- Continuous motion after reveal ------------------
        # Pulse the curve tip + milestone dots to keep motion going.
        def ms_updater_factory(idx, col):
            def upd(m):
                t = clock.get_value()
                glow = 0.5 + 0.5 * math.sin(t * 3.0 + idx * 1.3)
                m[0].set_stroke(col, opacity=0.6 + 0.4 * glow, width=2 + 2 * glow)
                m[0].scale(1.0)  # keep stable
            return upd

        for i, (u, year, txt, gb, col) in enumerate(milestones):
            ms_group[i].add_updater(ms_updater_factory(i, col))

        # A travelling pulse that keeps sweeping up the finished curve.
        pulse_dot = always_redraw(
            lambda: Dot(
                curve_point((clock.get_value() * 0.22) % 1.0),
                color=GREEN, radius=0.08).set_opacity(0.85))
        self.add(pulse_dot)

        total = 16.0
        steps = 4
        for i in range(steps):
            self.play(clock.animate.set_value((i + 1) * total / steps),
                      run_time=total / steps, rate_func=rate_functions.linear)

        for i in range(len(milestones)):
            ms_group[i].clear_updaters()
        self.remove(pulse_dot)
        self.wait(0.3)
