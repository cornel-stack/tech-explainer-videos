"""MobileShare — animated horizontal bar chart of mobile OS share.

Illustrative, StatCounter-style relative lengths (NOT exact figures):
  Android ~71% (green), iOS ~28% (silver), Other ~1% (coral).

Bars grow, then continuously shimmer/pulse with a sweeping highlight.
"""

import math

from manim import (
    VGroup,
    Scene,
    RoundedRectangle,
    Text,
    ValueTracker,
    FadeIn,
    always_redraw,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)

BG = "#09090C"
INK = "#E9E8E4"
INK2 = "#90908C"
TEAL = "#2DD4BF"
GREEN = "#35FF9E"
VIOLET = "#9B8CFF"
AMBER = "#FFB020"
SILVER = "#C9CDD4"
CORAL = "#FF6B4A"

FONT = "Inter"
MONO = "DejaVu Sans Mono"


class MobileShare(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Mobile OS share", font=FONT, color=INK, weight="BOLD").scale(0.85)
        title.to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        note = Text("illustrative — StatCounter-style, not exact",
                    font=MONO, color=INK2).scale(0.4)
        note.next_to(title, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)
        self.play(FadeIn(note), run_time=0.4)

        # --- Data (relative lengths, illustrative) ------------------------
        # Android gets the amber/green family: green fill, amber accent.
        data = [
            ("Android", 71, GREEN, AMBER),
            ("iOS", 28, SILVER, SILVER),
            ("Other", 1, CORAL, CORAL),
        ]

        x_left = -5.0
        max_len = 9.0
        bar_h = 1.0
        row_gap = 1.8
        y_top = 1.4

        def length_for(pct):
            return max(0.25, max_len * pct / 100.0)

        clock = ValueTracker(0.0)
        rows = []

        for i, (name, pct, color, accent) in enumerate(data):
            y = y_top - i * row_gap
            full_len = length_for(pct)

            rail = RoundedRectangle(
                width=max_len, height=bar_h, corner_radius=bar_h / 2,
                stroke_opacity=0, fill_color=INK2, fill_opacity=0.06,
            )
            rail.move_to([x_left + max_len / 2, y, 0])

            grow = ValueTracker(0.0)

            label = Text(name, font=FONT, color=INK).scale(0.55)
            label.next_to([x_left, y, 0], LEFT, buff=0.3)

            rows.append({
                "name": name, "pct": pct, "color": color, "accent": accent,
                "y": y, "full_len": full_len, "grow": grow,
                "rail": rail, "label": label,
            })

            self.add(rail)
            self.play(FadeIn(label, shift=RIGHT * 0.15), run_time=0.3)

        def make_bar(row):
            def f():
                g = row["grow"].get_value()
                cur = row["full_len"] * g
                t = clock.get_value()
                base_op = 0.85 + 0.12 * math.sin(t * 2.0 + row["y"])
                bar = RoundedRectangle(
                    width=max(0.001, cur), height=bar_h, corner_radius=bar_h / 2,
                    stroke_color=row["accent"], stroke_width=2.2,
                    fill_color=row["color"], fill_opacity=max(0.0, min(1.0, 0.65 * base_op)),
                )
                bar.move_to([x_left + cur / 2, row["y"], 0])
                glow = RoundedRectangle(
                    width=max(0.001, cur), height=bar_h, corner_radius=bar_h / 2,
                    stroke_color=row["accent"], stroke_width=14, stroke_opacity=0.14,
                    fill_opacity=0.0,
                )
                glow.move_to(bar.get_center())
                return VGroup(glow, bar)
            return f

        def make_pct_label(row):
            def f():
                g = row["grow"].get_value()
                cur = row["full_len"] * g
                lbl = Text(f"{int(round(row['pct'] * g))}%", font=MONO,
                           color=row["accent"], weight="BOLD").scale(0.55)
                lbl.move_to([x_left + cur + 0.65, row["y"], 0])
                return lbl
            return f

        for row in rows:
            self.add(always_redraw(make_bar(row)))
            self.add(always_redraw(make_pct_label(row)))

        for row in rows:
            self.play(row["grow"].animate.set_value(1.0), run_time=0.95,
                      rate_func=rate_functions.ease_out_cubic)

        chart_top = y_top + bar_h
        chart_bot = y_top - (len(data) - 1) * row_gap - bar_h

        def make_sweep():
            t = clock.get_value()
            frac = (t * 0.22) % 1.0
            x = x_left + frac * max_len
            bar = RoundedRectangle(
                width=0.24, height=(chart_top - chart_bot), corner_radius=0.1,
                stroke_opacity=0, fill_color=INK, fill_opacity=0.10,
            )
            bar.move_to([x, (chart_top + chart_bot) / 2, 0])
            return bar

        self.add(always_redraw(make_sweep))

        # Continuous shimmer for the remainder (~24s total).
        self.play(clock.animate.set_value(18.0), run_time=18.0, rate_func=rate_functions.linear)
        self.wait(0.3)
        self.wait(0.2)
