"""Scheduler — CPU scheduler as a Gantt time-slice chart (~24s).

A horizontal time axis with tiny coloured slices alternating between processes
T0/T1/T2/T3 (different accent colours), a moving NOW cursor sweeping right, a
time-quantum tick, and a caption:
    "~1000 switches/sec — the air-traffic controller".

The slice bar scrolls/advances continuously so it never stops.
"""

from manim import (
    VGroup,
    RoundedRectangle,
    Rectangle,
    Line,
    Dot,
    Text,
    Scene,
    ValueTracker,
    Create,
    FadeIn,
    always_redraw,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)
import numpy as np

BG = "#08080B"
INK = "#EDECE6"
INK2 = "#8E8E8A"
AMBER = "#FFB020"
TEAL = "#2DD4BF"
GREEN = "#35FF9E"
VIOLET = "#9B8CFF"
CORAL = "#FF6B4A"
SILVER = "#C9CDD4"

PROC_COLORS = [TEAL, GREEN, VIOLET, AMBER]
PROC_NAMES = ["T0", "T1", "T2", "T3"]

MONO = "JetBrains Mono"
HEAD = "Inter"


def mono(txt, size=22, color=INK):
    try:
        return Text(txt, font=MONO, font_size=size, color=color)
    except Exception:
        return Text(txt, font="Courier New", font_size=size, color=color)


def head(txt, size=34, color=INK, weight="BOLD"):
    try:
        return Text(txt, font=HEAD, font_size=size, color=color, weight=weight)
    except Exception:
        return Text(txt, font_size=size, color=color, weight=weight)


class Scheduler(Scene):
    def construct(self):
        self.camera.background_color = BG
        clock = ValueTracker(0.0)

        title = head("THE CPU SCHEDULER", size=36, color=INK).to_edge(UP, buff=0.5)
        sub = mono("// ~1000 switches/sec — the air-traffic controller",
                   size=19, color=INK2)
        sub.next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(sub), run_time=0.4)

        # ---- Chart frame ----
        axis_y = -1.2
        axis_left = -6.2
        axis_right = 6.2
        bar_h = 1.2
        bar_top = axis_y + 0.1 + bar_h

        axis = Line([axis_left, axis_y, 0], [axis_right, axis_y, 0],
                    stroke_color=INK2, stroke_width=1.6)
        axis_lbl = mono("time ->", size=16, color=INK2)
        axis_lbl.next_to([axis_right, axis_y, 0], DOWN, buff=0.2)

        # Tick marks along the axis (time quanta).
        ticks = VGroup()
        tick_labels = VGroup()
        n_ticks = 13
        for i in range(n_ticks):
            x = axis_left + (axis_right - axis_left) * i / (n_ticks - 1)
            tk = Line([x, axis_y, 0], [x, axis_y - 0.14, 0],
                      stroke_color=INK2, stroke_width=1.2, stroke_opacity=0.6)
            ticks.add(tk)

        self.play(Create(axis), FadeIn(axis_lbl), Create(ticks), run_time=0.7)

        # ---- Process legend / lanes on the left ----
        legend = VGroup()
        for i, (name, col) in enumerate(zip(PROC_NAMES, PROC_COLORS)):
            ly = bar_top + 0.55 + (3 - i) * 0.0  # single row legend near top of bar
            sw = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.05,
                                  stroke_color=col, stroke_width=1.5,
                                  fill_color=col, fill_opacity=0.5)
            sw.move_to([axis_left + i * 1.6, bar_top + 0.6, 0])
            nl = mono(name, size=16, color=col).next_to(sw, RIGHT, buff=0.12)
            legend.add(sw, nl)
        self.play(FadeIn(legend), run_time=0.5)

        # ---- Quantum caption ----
        q_lbl = mono("time quantum", size=15, color=SILVER)
        q_lbl.move_to([axis_left + 1.2, axis_y - 0.55, 0])

        # ===================== CONTINUOUS SCROLLING SLICES =====================
        # We model a time-slice schedule as a deterministic sequence and draw
        # the visible window [t_window, t_window + span] scrolling left.
        slice_w = 0.9        # visual width of one quantum
        span = axis_right - axis_left
        scroll_speed = 0.9   # quanta per second

        # Deterministic schedule: which process runs in quantum k.
        def proc_at(k):
            # Mostly round-robin with occasional repeats / priority bumps.
            pattern = [0, 1, 2, 3, 1, 0, 2, 1, 3, 2, 0, 1, 3, 0]
            return pattern[k % len(pattern)]

        slices_holder = VGroup()
        self.add(slices_holder)

        def redraw_slices():
            t = clock.get_value()
            offset = t * scroll_speed  # in quanta
            grp = VGroup()
            # Draw enough quanta to fill the window plus a margin.
            k0 = int(np.floor(offset))
            n_vis = int(span / slice_w) + 3
            for j in range(-1, n_vis + 1):
                k = k0 + j
                # x position: newest quanta enter from the right, scroll left.
                frac = (offset - k)
                x_right = axis_right - frac * slice_w
                x_left = x_right - slice_w
                if x_right < axis_left - slice_w or x_left > axis_right:
                    continue
                # clamp visible extents
                xl = max(x_left, axis_left)
                xr = min(x_right, axis_right)
                w = xr - xl
                if w <= 0.01:
                    continue
                pidx = proc_at(k)
                col = PROC_COLORS[pidx]
                rect = Rectangle(
                    width=w, height=bar_h,
                    stroke_color=col, stroke_width=1.4,
                    fill_color=col, fill_opacity=0.35,
                )
                rect.move_to([(xl + xr) / 2, axis_y + 0.1 + bar_h / 2, 0])
                grp.add(rect)
                # process label if slice wide enough
                if w > 0.5:
                    pl = mono(PROC_NAMES[pidx], size=15, color=INK)
                    pl.move_to(rect.get_center())
                    grp.add(pl)
            return grp

        slices = always_redraw(redraw_slices)
        self.add(slices)

        # ---- NOW cursor sweeping (sits near right edge, pulsing) ----
        now_x = axis_right - 0.0
        now_line = Line([now_x, bar_top + 0.1, 0], [now_x, axis_y - 0.3, 0],
                        stroke_color=CORAL, stroke_width=2.5)
        now_lbl = mono("NOW", size=16, color=CORAL)
        now_lbl.next_to([now_x, bar_top + 0.1, 0], UP, buff=0.12)
        now_glow = Line([now_x, bar_top + 0.1, 0], [now_x, axis_y - 0.3, 0],
                        stroke_color=CORAL, stroke_width=9, stroke_opacity=0.2)

        def now_glow_up(m):
            t = clock.get_value()
            m.set_stroke(width=7 + 6 * (0.5 + 0.5 * np.sin(t * 6)))
        now_glow.add_updater(now_glow_up)

        # A context-switch flash: a small spark at NOW when the process changes.
        switch_dot = Dot(radius=0.0, color=CORAL).move_to([now_x, axis_y + 0.1 + bar_h / 2, 0])

        def switch_up(m):
            t = clock.get_value()
            offset = t * scroll_speed
            k = int(np.floor(offset))
            # proximity to a quantum boundary (switch moment)
            frac = offset - k
            near = min(frac, 1 - frac)
            changed = proc_at(k) != proc_at(k - 1)
            if changed and near < 0.12:
                m.set_width(0.5)
                m.set_opacity(0.8 * (1 - near / 0.12))
            else:
                m.set_opacity(0.0)
        switch_dot.add_updater(switch_up)

        # ---- Quantum bracket under one slice ----
        q_bracket = always_redraw(lambda: self._quantum_bracket(
            clock.get_value(), scroll_speed, slice_w, axis_right, axis_y))

        # ---- HUD switch counter ----
        counter = mono("ctx switches: 0", size=18, color=CORAL)
        counter.to_corner(DOWN + RIGHT, buff=0.5)

        def counter_up(m):
            t = clock.get_value()
            val = int(t * scroll_speed)  # one switch per quantum, roughly
            # Scale to feel like ~1000/s in real terms (annotate x).
            new = mono(f"ctx switches: {val}", size=18, color=CORAL)
            new.move_to(m, aligned_edge=RIGHT)
            m.become(new)
        counter.add_updater(counter_up)

        self.add(now_glow, now_line, now_lbl, switch_dot, q_bracket,
                 q_lbl, counter)

        self.play(clock.animate.set_value(16.0),
                  run_time=16.0, rate_func=rate_functions.linear)

        # Clean final frame.
        slices.clear_updaters()
        q_bracket.clear_updaters()
        now_glow.clear_updaters()
        switch_dot.clear_updaters()
        counter.clear_updaters()
        switch_dot.set_opacity(0.0)
        self.wait(0.3)

    # Helper: a little quantum-width bracket that scrolls with the chart.
    def _quantum_bracket(self, t, scroll_speed, slice_w, axis_right, axis_y):
        offset = t * scroll_speed
        frac = offset - np.floor(offset)
        x_right = axis_right - frac * slice_w
        x_left = x_right - slice_w
        y = axis_y - 0.38
        grp = VGroup()
        base = Line([x_left, y, 0], [x_right, y, 0],
                    stroke_color=SILVER, stroke_width=1.6)
        lcap = Line([x_left, y - 0.08, 0], [x_left, y + 0.08, 0],
                    stroke_color=SILVER, stroke_width=1.6)
        rcap = Line([x_right, y - 0.08, 0], [x_right, y + 0.08, 0],
                    stroke_color=SILVER, stroke_width=1.6)
        grp.add(base, lcap, rcap)
        return grp
