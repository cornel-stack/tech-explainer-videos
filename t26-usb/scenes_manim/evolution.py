"""Scene: THE CONNECTORS, SHRINKING — the USB connector story on a timeline.

Class `Evolution` (~20s). A left-to-right timeline carries simple outline
silhouettes of the USB connectors shrinking over time: USB-A (flat wide rect),
USB-B (tall near-square), Mini-USB (small trapezoid), Micro-USB (small flatter
trapezoid) and USB-C (small rounded stadium). Each has a MONO name + year.
A highlight sweep rides the timeline lighting each connector as it "arrives";
when it reaches USB-C it does a little reversible flip to show it goes in
either way.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    RoundedRectangle,
    Polygon,
    Line,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
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


class Evolution(Scene):
    def construct(self):
        title = Text("THE CONNECTORS, SHRINKING",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- timeline axis ---------------------------------------------------
        x_left, x_right = -5.8, 5.8
        axis_y = -2.9
        axis = Line([x_left, axis_y, 0], [x_right, axis_y, 0],
                    stroke_color=SECOND, stroke_width=2.5)
        self.play(Create(axis), run_time=0.6)

        # five connectors, positioned left -> right, shrinking over time.
        # each: (name, year, colour, builder, scale, slot x)
        slots_x = np.linspace(x_left + 1.2, x_right - 1.2, 5)

        def build_usb_a(col):
            # flat wide rectangle with inner tongue
            body = Rectangle(width=1.9, height=0.75,
                             stroke_color=col, stroke_width=3,
                             fill_color=BG, fill_opacity=1.0)
            tongue = Rectangle(width=1.55, height=0.28,
                               stroke_color=col, stroke_width=2,
                               fill_opacity=0).move_to(body).shift(UP * 0.08)
            return VGroup(body, tongue)

        def build_usb_b(col):
            # tall near-square with a chamfered top
            body = Polygon(
                [-0.55, -0.6, 0], [0.55, -0.6, 0], [0.55, 0.35, 0],
                [0.3, 0.62, 0], [-0.3, 0.62, 0], [-0.55, 0.35, 0],
                stroke_color=col, stroke_width=3,
                fill_color=BG, fill_opacity=1.0)
            inner = Rectangle(width=0.55, height=0.4,
                              stroke_color=col, stroke_width=2,
                              fill_opacity=0).move_to(body)
            return VGroup(body, inner)

        def build_mini(col):
            # small trapezoid (wider top)
            body = Polygon(
                [-0.62, 0.28, 0], [0.62, 0.28, 0],
                [0.5, -0.28, 0], [-0.5, -0.28, 0],
                stroke_color=col, stroke_width=3,
                fill_color=BG, fill_opacity=1.0)
            inner = Rectangle(width=0.78, height=0.12,
                              stroke_color=col, stroke_width=2,
                              fill_opacity=0).move_to(body)
            return VGroup(body, inner)

        def build_micro(col):
            # small flatter trapezoid
            body = Polygon(
                [-0.58, 0.16, 0], [0.58, 0.16, 0],
                [0.48, -0.16, 0], [-0.48, -0.16, 0],
                stroke_color=col, stroke_width=3,
                fill_color=BG, fill_opacity=1.0)
            inner = Rectangle(width=0.74, height=0.08,
                              stroke_color=col, stroke_width=2,
                              fill_opacity=0).move_to(body)
            return VGroup(body, inner)

        def build_usb_c(col):
            # small rounded stadium (oval-ish)
            body = RoundedRectangle(corner_radius=0.22, width=0.95, height=0.42,
                                    stroke_color=col, stroke_width=3,
                                    fill_color=BG, fill_opacity=1.0)
            inner = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.14,
                                     stroke_color=col, stroke_width=2,
                                     fill_opacity=0).move_to(body)
            return VGroup(body, inner)

        specs = [
            ("USB-A", "1996", SILVER, build_usb_a, 1.0),
            ("USB-B", "1996", SILVER, build_usb_b, 0.85),
            ("Mini-USB", "2000s", AMBER, build_mini, 0.72),
            ("Micro-USB", "2007", CORAL, build_micro, 0.6),
            ("USB-C", "2014", TEAL, build_usb_c, 0.52),
        ]

        connectors = []   # list of dicts with mobjects + metadata
        for i, (name, year, col, builder, sc) in enumerate(specs):
            shape = builder(col).scale(sc)
            cx = slots_x[i]
            # vertical tick on timeline
            tick = Line([cx, axis_y - 0.12, 0], [cx, axis_y + 0.12, 0],
                        stroke_color=SECOND, stroke_width=2)
            shape.move_to([cx, axis_y + 1.0, 0])
            name_lbl = Text(name, font=MONO, color=col).scale(0.3)
            name_lbl.next_to(shape, UP, buff=0.14)
            year_lbl = Text(year, font=MONO, color=SECOND).scale(0.26)
            year_lbl.next_to(tick, DOWN, buff=0.14)
            connectors.append({
                "shape": shape, "name": name_lbl, "year": year_lbl,
                "tick": tick, "col": col, "x": cx,
            })

        all_ticks = VGroup(*[c["tick"] for c in connectors])
        all_shapes = VGroup(*[c["shape"] for c in connectors])
        all_names = VGroup(*[c["name"] for c in connectors])
        all_years = VGroup(*[c["year"] for c in connectors])
        self.play(Create(all_ticks), run_time=0.5)
        self.play(FadeIn(all_shapes, shift=UP * 0.15),
                  FadeIn(all_names), FadeIn(all_years),
                  lag_ratio=0.08, run_time=1.2)

        caption = Text("same family, every connector smaller",
                       font=HEAD, color=SECOND).scale(0.34)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        TOTAL = 20.0
        # sweep travels across all five slots then returns, continuously.
        x0, x1 = slots_x[0] - 0.6, slots_x[-1] + 0.6

        # moving highlight marker riding the timeline
        sweep = Dot(color=INK, radius=0.09).move_to([x0, axis_y, 0])

        def sweep_upd(m):
            tt = t.get_value()
            # one full pass over ~11s, then dwell/flip phase, subtle oscillation
            phase = min(tt / 11.0, 1.0)
            eased = rate_functions.ease_in_out_sine(phase)
            x = x0 + (x1 - x0) * eased
            m.move_to([x, axis_y, 0])
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(tt * 3.0)))
        sweep.add_updater(sweep_upd)
        self.add(sweep)

        # glowing trail segment behind the sweep along the axis
        trail = Line([x0, axis_y, 0], [x0, axis_y, 0],
                     stroke_color=TEAL, stroke_width=4)

        def trail_upd(m):
            tt = t.get_value()
            phase = min(tt / 11.0, 1.0)
            eased = rate_functions.ease_in_out_sine(phase)
            x = x0 + (x1 - x0) * eased
            m.put_start_and_end_on([x0, axis_y, 0], [max(x, x0 + 0.001), axis_y, 0])
            m.set_stroke(opacity=0.55)
        trail.add_updater(trail_upd)
        self.add(trail)

        # each connector lights up as the sweep reaches its slot.
        INK_C = ManimColor(INK)
        for i, c in enumerate(connectors):
            def make_light(entry, slot_x, base_col):
                shape = entry["shape"]
                name = entry["name"]
                tick = entry["tick"]
                base = ManimColor(base_col)
                hot = ManimColor(INK)

                def _upd(m):
                    tt = t.get_value()
                    phase = min(tt / 11.0, 1.0)
                    eased = rate_functions.ease_in_out_sine(phase)
                    sx = x0 + (x1 - x0) * eased
                    # proximity of sweep to this slot -> brightness
                    d = abs(sx - slot_x)
                    glow = float(np.clip(1.0 - d / 0.9, 0.0, 1.0))
                    col = interpolate_color(base, hot, 0.55 * glow)
                    for sub in shape:
                        sub.set_stroke(color=col,
                                       width=2 + 2.5 * glow)
                    name.set_color(col)
                    tick.set_stroke(color=interpolate_color(
                        ManimColor(SECOND), hot, glow))
                    # arrived connectors keep a gentle lift
                    arrived = 1.0 if sx >= slot_x - 0.1 else 0.0
                    shape.set_opacity(1.0)
                    name.set_opacity(0.5 + 0.5 * max(glow, arrived))
                return _upd
            c["shape"].add_updater(make_light(c, c["x"], c["col"]))

        # --- USB-C reversible flip --------------------------------------------
        # once the sweep has reached USB-C (after ~11s), flip the C connector
        # back and forth to emphasise it goes in either way.
        c_entry = connectors[-1]
        c_shape = c_entry["shape"]
        c_center = c_shape.get_center().copy()

        rev_lbl = Text("reversible", font=MONO, color=TEAL).scale(0.3)
        rev_lbl.move_to([c_entry["x"], c_entry["name"].get_top()[1] + 0.55, 0])
        rev_lbl.set_opacity(0.0)

        def rev_lbl_upd(m):
            tt = t.get_value()
            on = float(np.clip((tt - 11.0) / 0.8, 0.0, 1.0))
            m.set_opacity(on * (0.65 + 0.35 * (0.5 + 0.5 * np.sin(tt * 4.0))))
        rev_lbl.add_updater(rev_lbl_upd)
        self.add(rev_lbl)

        # reversible flip: squash the C connector horizontally through zero so
        # it appears to rotate about its vertical axis and go in either way.
        # Done against a stored upright copy to stay stable frame-to-frame.
        arrow = Text("<->", font=MONO, color=TEAL).scale(0.5)
        arrow.move_to([c_entry["x"],
                       c_entry["shape"].get_bottom()[1] - 0.55, 0])
        arrow.set_opacity(0.0)

        def arrow_upd(m):
            tt = t.get_value()
            on = float(np.clip((tt - 11.0) / 0.8, 0.0, 1.0))
            m.set_opacity(on * (0.6 + 0.4 * (0.5 + 0.5 * np.sin(tt * 4.0))))
        arrow.add_updater(arrow_upd)
        self.add(arrow)

        c_shape_upright = c_shape.copy()

        def c_flip_clean(m):
            tt = t.get_value()
            base = c_shape_upright.copy()
            if tt >= 11.0:
                ph = (tt - 11.0)
                squash = np.cos(ph * 2.4)            # -1 .. +1 (mirror through 0)
                sx = max(abs(squash), 0.12)
                base.stretch_to_fit_width(c_shape_upright.width * sx)
                base.move_to(c_center)
            m.become(base)
        c_shape.add_updater(c_flip_clean)

        self.play(t.animate.set_value(TOTAL), run_time=TOTAL,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
