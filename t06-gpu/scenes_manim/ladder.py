"""Ladder — "how many calculations" climbing on a staggering log-ish scale.

Compute-dark palette. Three rising tiers of calculations-per-second climb
from an old 3D game to a modern GPU, with a rapidly ticking counter and a
climbing marker. Continuous motion for the whole ~22s via a master clock.
"""

from manim import (
    Scene,
    VGroup,
    RoundedRectangle,
    Rectangle,
    Text,
    Line,
    Dot,
    ValueTracker,
    Create,
    Write,
    FadeIn,
    rate_functions,
    always_redraw,
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
AMBER = "#FFB020"

MONO = "JetBrains Mono"
HEAD = "Inter"


def _fmt_calcs(v):
    """Format a calculations/second value into a human, staggering string."""
    if v >= 1e12:
        return f"{v / 1e12:,.1f} trillion/s"
    if v >= 1e9:
        return f"{v / 1e9:,.1f} billion/s"
    if v >= 1e6:
        return f"{v / 1e6:,.0f} million/s"
    return f"{v:,.0f}/s"


class Ladder(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("How many calculations?", font=HEAD, color=INK, weight="BOLD")
        title.scale(0.85).to_edge(UP, buff=0.55)
        sub = Text("per second — climbing a staggering scale",
                   font=MONO, color=SUB).scale(0.4)
        sub.next_to(title, DOWN, buff=0.2)
        self.play(Write(title, run_time=0.9), FadeIn(sub, run_time=0.6))

        # --- Three tiers on a log-ish vertical scale ------------------------
        tiers = [
            ("an old 3D game", 1e8, GREEN),
            ("a modern game", 4e13, LIME),
            ("to draw ONE frame", 2e12, TEAL),
        ]
        # Vertical positions (bottom to top) for the three bars.
        base_y = -2.6
        x_slots = [-4.3, 0.0, 4.3]
        max_h = 4.4

        axis = Line([-6.4, base_y, 0], [6.4, base_y, 0], color=SUB, stroke_width=2)
        self.play(Create(axis, run_time=0.5))

        bars = VGroup()
        caps = VGroup()
        targets = []
        for i, (label, val, col) in enumerate(tiers):
            x = x_slots[i]
            # log-ish height: compress huge range so all fit but still rise hard
            import math
            h = max(0.6, (math.log10(val) - 7.5) / (13.8 - 7.5) * max_h)
            targets.append(h)

            glow = RoundedRectangle(width=1.7, height=0.001, corner_radius=0.08,
                                    stroke_color=col, stroke_width=14,
                                    fill_opacity=0.0)
            glow.set_stroke(opacity=0.18)
            bar = RoundedRectangle(width=1.5, height=0.001, corner_radius=0.06,
                                   stroke_color=col, stroke_width=2.5,
                                   fill_color=col, fill_opacity=0.22)
            grp = VGroup(glow, bar)
            grp.move_to([x, base_y, 0])
            bars.add(grp)

            name = Text(label, font=HEAD, color=INK).scale(0.4)
            name.move_to([x, base_y - 0.45, 0])
            val_t = Text(_fmt_calcs(val), font=MONO, color=col).scale(0.42)
            caps.add(VGroup(name, val_t))

        self.play(FadeIn(bars, run_time=0.5))

        # Grow each bar to its target height anchored at base.
        clock = ValueTracker(0.0)

        def make_bar_updater(index, target_h, col, x):
            def upd(mob):
                t = clock.get_value()
                # staggered start per tier
                start = 0.6 * index
                span = 2.2
                p = max(0.0, min(1.0, (t - start) / span))
                eased = rate_functions.ease_out_cubic(p)
                # add a gentle perpetual breathing once grown
                breathe = 0.04 * __import__("math").sin((t - start - span) * 2.2)
                breathe = breathe if p >= 1.0 else 0.0
                h = max(0.001, target_h * eased * (1 + breathe))
                glow, bar = mob
                for seg in (glow, bar):
                    w = seg.width
                    seg.stretch_to_fit_height(h)
                    seg.move_to([x, base_y + h / 2.0, 0])
            return upd

        for i, grp in enumerate(bars):
            grp.add_updater(make_bar_updater(i, targets[i], tiers[i][2], x_slots[i]))

        # Captions above each bar, following the bar tops.
        def make_cap_updater(index, x):
            cap = caps[index]

            def upd(m):
                top = bars[index][1].get_top()[1]
                m.move_to([x, top + 0.55, 0])
            return upd

        for i in range(3):
            caps[i].add_updater(make_cap_updater(i, x_slots[i]))
        self.play(FadeIn(caps, run_time=0.5))

        # --- Rapid ticking counter + climbing marker -----------------------
        counter_val = always_redraw(
            lambda: Text(
                _fmt_calcs(
                    1e8 * (10 ** (5.6 * rate_functions.ease_in_out_sine(
                        min(1.0, clock.get_value() / 6.0))))
                ),
                font=MONO, color=AMBER,
            ).scale(0.6).to_edge(DOWN, buff=0.5)
        )
        self.add(counter_val)

        # Climbing marker dot that rides up along the tallest (modern) bar.
        marker = always_redraw(
            lambda: Dot(
                point=[x_slots[1] + 1.3,
                       base_y + bars[1][1].height, 0],
                color=AMBER, radius=0.09,
            )
        )
        marker_glow = always_redraw(
            lambda: Dot(
                point=[x_slots[1] + 1.3,
                       base_y + bars[1][1].height, 0],
                color=AMBER, radius=0.2,
            ).set_opacity(0.25)
        )
        self.add(marker_glow, marker)

        # Drive the master clock across the full duration.
        self.play(clock.animate.set_value(6.0),
                  run_time=6.0, rate_func=rate_functions.linear)
        # Keep everything alive & breathing to fill the time budget.
        self.play(clock.animate.set_value(13.5),
                  run_time=7.5, rate_func=rate_functions.linear)
        self.play(clock.animate.set_value(18.0),
                  run_time=4.5, rate_func=rate_functions.linear)

        # Clean final frame: freeze updaters.
        for grp in bars:
            grp.clear_updaters()
        for cap in caps:
            cap.clear_updaters()
        self.wait(0.3)
