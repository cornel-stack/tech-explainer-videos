"""Scene 1: a CPU is just switches -> logic gates.

Class `Transistor` (~18s). A single transistor shown as an ON/OFF SWITCH
toggling (GREEN = on/1, dim = off/0). Then a few switches combine into
labelled logic gates AND, OR, NOT, showing their behaviour (AND lights only
when both inputs on). Caption: "a CPU is just switches -> logic gates".

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92  green #35E08A
  teal #2DD4BF  violet #B06BFF  amber #FFB020  coral #FF5C47
  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Line,
    Circle,
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

DIM = "#1C2A22"  # dim green (off state)


class Transistor(Scene):
    def construct(self):
        title = Text("A transistor is a switch", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- LEFT: a single transistor as a switch --------------------------
        sw_c = np.array([-4.2, 0.5, 0.0])
        wire_in = Line(sw_c + LEFT * 1.3, sw_c + LEFT * 0.55,
                       stroke_color=SECOND, stroke_width=3)
        wire_out = Line(sw_c + RIGHT * 0.55, sw_c + RIGHT * 1.3,
                        stroke_color=SECOND, stroke_width=3)
        term_l = Dot(sw_c + LEFT * 0.55, color=SECOND, radius=0.07)
        term_r = Dot(sw_c + RIGHT * 0.55, color=SECOND, radius=0.07)
        # the movable switch arm
        arm = Line(sw_c + LEFT * 0.55, sw_c + RIGHT * 0.5 + UP * 0.45,
                   stroke_color=GREEN, stroke_width=4)
        bulb = Dot(sw_c + RIGHT * 1.3 + RIGHT * 0.35, color=DIM, radius=0.16)
        sw_lbl = Text("1 transistor", font=MONO, color=SECOND).scale(0.3)
        sw_lbl.next_to(wire_in, UP, buff=0.9).shift(RIGHT * 0.3)
        state_lbl = Text("0", font=MONO, color=SECOND).scale(0.5)
        state_lbl.next_to(bulb, UP, buff=0.3)

        self.play(Create(wire_in), Create(wire_out), FadeIn(term_l),
                  FadeIn(term_r), Create(arm), FadeIn(bulb), FadeIn(sw_lbl),
                  FadeIn(state_lbl), run_time=1.0)

        # --- RIGHT: three gates built from switches -------------------------
        def make_gate(center, name, color):
            box = RoundedRectangle(corner_radius=0.12, width=1.5, height=1.1,
                                   stroke_color=color, stroke_width=2.5,
                                   fill_color="#111318",
                                   fill_opacity=0.9).move_to(center)
            lbl = Text(name, font=MONO, color=color).scale(0.4)
            lbl.move_to(center)
            out_dot = Dot(center + RIGHT * 1.15, color=DIM, radius=0.11)
            out_wire = Line(center + RIGHT * 0.75, out_dot.get_center(),
                            stroke_color=SECOND, stroke_width=2.5)
            return VGroup(box, lbl, out_wire, out_dot)

        and_c = np.array([2.0, 1.9, 0.0])
        or_c = np.array([2.0, 0.3, 0.0])
        not_c = np.array([2.0, -1.3, 0.0])
        and_g = make_gate(and_c, "AND", GREEN)
        or_g = make_gate(or_c, "OR", TEAL)
        not_g = make_gate(not_c, "NOT", VIOLET)

        # input dots for each gate (AND/OR have 2, NOT has 1)
        def in_dots(center, n):
            dots = []
            if n == 2:
                ys = [0.3, -0.3]
            else:
                ys = [0.0]
            for y in ys:
                d = Dot(center + LEFT * 1.15 + UP * y, color=DIM, radius=0.1)
                w = Line(center + LEFT * 1.15 + UP * y,
                         center + LEFT * 0.75 + UP * y,
                         stroke_color=SECOND, stroke_width=2.5)
                dots.append((d, w, y))
            return dots

        and_in = in_dots(and_c, 2)
        or_in = in_dots(or_c, 2)
        not_in = in_dots(not_c, 1)

        gates_grp = VGroup(and_g, or_g, not_g)
        for d, w, _ in and_in + or_in + not_in:
            gates_grp.add(w, d)
        self.play(FadeIn(gates_grp), run_time=1.0)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        c_on = ManimColor(GREEN)
        c_off = ManimColor(DIM)

        def lerp_state(on_frac):
            return interpolate_color(c_off, c_on, on_frac)

        # single switch toggles on/off (square-ish via sin threshold)
        def switch_state(tt):
            return 1.0 if np.sin(1.4 * tt) > 0 else 0.0

        def arm_upd(m):
            on = switch_state(t.get_value())
            if on > 0.5:
                end = sw_c + RIGHT * 0.55
                m.set_stroke(GREEN)
            else:
                end = sw_c + RIGHT * 0.5 + UP * 0.45
                m.set_stroke(SECOND)
            m.put_start_and_end_on(sw_c + LEFT * 0.55, end)
        arm.add_updater(arm_upd)

        def bulb_upd(m):
            on = switch_state(t.get_value())
            m.set_color(lerp_state(on))
        bulb.add_updater(bulb_upd)

        def state_upd(m):
            on = switch_state(t.get_value())
            txt = "1" if on > 0.5 else "0"
            new = Text(txt, font=MONO,
                       color=GREEN if on > 0.5 else SECOND).scale(0.5)
            new.move_to(m.get_center())
            m.become(new)
        state_lbl.add_updater(state_upd)

        # gate inputs drive at different rates so combinations vary
        def gate_a(tt):
            return 1.0 if np.sin(0.9 * tt) > 0 else 0.0

        def gate_b(tt):
            return 1.0 if np.sin(0.55 * tt + 1.0) > 0 else 0.0

        def drive_inputs(dots, fn_a, fn_b):
            for d, w, y in dots:
                def make(dot, yy):
                    def _upd(m):
                        a = fn_a(t.get_value())
                        b = fn_b(t.get_value())
                        val = a if yy >= 0 else b
                        m.set_color(lerp_state(val))
                    return _upd
                d.add_updater(make(d, y))

        drive_inputs(and_in, gate_a, gate_b)
        drive_inputs(or_in, gate_a, gate_b)
        drive_inputs(not_in, gate_a, gate_a)

        # outputs reflect the logic
        and_out = and_g[3]
        or_out = or_g[3]
        not_out = not_g[3]

        def and_out_upd(m):
            a = gate_a(t.get_value())
            b = gate_b(t.get_value())
            m.set_color(lerp_state(1.0 if (a > 0.5 and b > 0.5) else 0.0))
        and_out.add_updater(and_out_upd)

        def or_out_upd(m):
            a = gate_a(t.get_value())
            b = gate_b(t.get_value())
            m.set_color(lerp_state(1.0 if (a > 0.5 or b > 0.5) else 0.0))
        or_out.add_updater(or_out_upd)

        def not_out_upd(m):
            a = gate_a(t.get_value())
            m.set_color(lerp_state(0.0 if a > 0.5 else 1.0))
        not_out.add_updater(not_out_upd)

        # arrow label pointing from switch cluster to gates
        bridge = Text("many switches ->", font=MONO, color=SECOND).scale(0.3)
        bridge.move_to([-1.1, -1.9, 0])

        def bridge_upd(m):
            m.set_opacity(0.4 + 0.4 * (0.5 + 0.5 *
                          np.sin(1.5 * t.get_value())))
        bridge.add_updater(bridge_upd)
        self.add(bridge)

        hint = Text("AND lights only when BOTH inputs are 1",
                    font=MONO, color=GREEN).scale(0.28)
        hint.move_to([2.0, 3.0, 0])

        def hint_upd(m):
            a = gate_a(t.get_value())
            b = gate_b(t.get_value())
            m.set_opacity(0.9 if (a > 0.5 and b > 0.5) else 0.25)
        hint.add_updater(hint_upd)
        self.add(hint)

        # caption
        cap = Text("a CPU is just switches -> logic gates",
                   font=HEAD, color=SECOND).scale(0.4)
        cap.to_edge(DOWN, buff=0.3)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
