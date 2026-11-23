"""Scene 5: registers hold numbers, the ALU does the maths.

Class `Alu` (~18s). The engine room: a bank of REGISTERS (small fast slots
holding numbers) feeding an ALU box that computes (e.g. "5 + 3 = 8" lighting
up), with a CONTROL UNIT directing. Values flow registers -> ALU -> back to a
register. Caption: "registers hold numbers, the ALU does the maths".

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
    Polygon,
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


class Alu(Scene):
    def construct(self):
        title = Text("Registers & the ALU", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- REGISTERS bank on the left -------------------------------------
        reg_names = ["R0", "R1", "R2", "R3"]
        reg_boxes = []
        reg_vals = []
        reg_grp = VGroup()
        reg_x = -4.6
        for i, nm in enumerate(reg_names):
            y = 1.5 - i * 0.95
            box = RoundedRectangle(corner_radius=0.08, width=1.7, height=0.7,
                                   stroke_color=TEAL, stroke_width=2,
                                   fill_color="#0E1A1A", fill_opacity=0.9)
            box.move_to([reg_x, y, 0])
            name = Text(nm, font=MONO, color=SECOND).scale(0.26)
            name.move_to(box.get_left() + RIGHT * 0.32)
            val = Text("0", font=MONO, color=TEAL).scale(0.38)
            val.move_to(box.get_right() + LEFT * 0.42)
            reg_grp.add(box, name, val)
            reg_boxes.append(box)
            reg_vals.append(val)
        reg_lbl = Text("REGISTERS", font=MONO, color=TEAL).scale(0.3)
        reg_lbl.move_to([reg_x, 2.3, 0])
        reg_sub = Text("fast slots", font=MONO, color=SECOND).scale(0.24)
        reg_sub.next_to(reg_lbl, DOWN, buff=0.08)
        self.play(FadeIn(reg_grp), FadeIn(reg_lbl), FadeIn(reg_sub),
                  run_time=1.0)

        # --- ALU box (trapezoid-ish) in the centre --------------------------
        alu_c = np.array([1.2, 0.0, 0.0])
        alu = Polygon(
            alu_c + np.array([-1.4, 1.0, 0]),
            alu_c + np.array([1.4, 1.0, 0]),
            alu_c + np.array([1.4, -1.0, 0]),
            alu_c + np.array([-1.4, -1.0, 0]),
            stroke_color=VIOLET, stroke_width=2.8,
            fill_color="#15101F", fill_opacity=0.92,
        )
        alu_lbl = Text("ALU", font=MONO, color=VIOLET).scale(0.42)
        alu_lbl.move_to(alu_c + UP * 0.55)
        calc = Text("5 + 3 = 8", font=MONO, color=INK).scale(0.5)
        calc.move_to(alu_c + DOWN * 0.1)
        self.play(Create(alu), FadeIn(alu_lbl), FadeIn(calc), run_time=0.9)

        # --- CONTROL UNIT directing from the top ----------------------------
        cu_box = RoundedRectangle(corner_radius=0.1, width=2.4, height=0.7,
                                  stroke_color=AMBER, stroke_width=2,
                                  fill_color="#1A1405", fill_opacity=0.9)
        cu_box.move_to([1.2, 2.4, 0])
        cu_lbl = Text("CONTROL UNIT", font=MONO, color=AMBER).scale(0.28)
        cu_lbl.move_to(cu_box.get_center())
        cu_line = Line(cu_box.get_bottom(), alu_c + UP * 1.0,
                       stroke_color=AMBER, stroke_width=2,
                       stroke_opacity=0.5)
        self.play(Create(cu_box), FadeIn(cu_lbl), Create(cu_line),
                  run_time=0.8)

        # --- flow wires: registers -> ALU -> back ---------------------------
        in_a = Line(reg_boxes[0].get_right(),
                    alu_c + np.array([-1.4, 0.45, 0]),
                    stroke_color=SECOND, stroke_width=2, stroke_opacity=0.35)
        in_b = Line(reg_boxes[1].get_right(),
                    alu_c + np.array([-1.4, -0.45, 0]),
                    stroke_color=SECOND, stroke_width=2, stroke_opacity=0.35)
        out_w = Line(alu_c + np.array([1.4, 0.0, 0]),
                     reg_boxes[2].get_right() + RIGHT * 1.6,
                     stroke_color=SECOND, stroke_width=2, stroke_opacity=0.35)
        # result flows back to R2
        back_w = Line(alu_c + np.array([1.4, 0.0, 0]),
                      reg_boxes[2].get_top() + UP * 0.0,
                      stroke_color=SECOND, stroke_width=2, stroke_opacity=0.0)
        self.play(Create(in_a), Create(in_b), Create(out_w), run_time=0.7)

        # moving value tokens
        tok_a = Dot(reg_boxes[0].get_right(), color=TEAL, radius=0.09)
        tok_b = Dot(reg_boxes[1].get_right(), color=TEAL, radius=0.09)
        tok_r = Dot(alu_c + np.array([1.4, 0.0, 0]), color=VIOLET,
                    radius=0.1)
        self.add(tok_a, tok_b, tok_r)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        LOOP = 3.0
        ops = [(5, 3, "+"), (9, 4, "-"), (6, 2, "*"), (7, 1, "+"),
               (8, 8, "+")]

        def op_for(tt):
            n = int(tt / LOOP) % len(ops)
            return ops[n]

        def compute(a, b, o):
            if o == "+":
                return a + b
            if o == "-":
                return a - b
            if o == "*":
                return a * b
            return 0

        a_start = reg_boxes[0].get_right()
        b_start = reg_boxes[1].get_right()
        alu_in_a = alu_c + np.array([-1.4, 0.45, 0])
        alu_in_b = alu_c + np.array([-1.4, -0.45, 0])
        alu_out = alu_c + np.array([1.4, 0.0, 0])
        r2_pos = reg_boxes[2].get_right()

        def tok_a_upd(m):
            ph = (t.get_value() / LOOP) % 1.0
            f = min(1.0, ph / 0.3)
            m.move_to(a_start + (alu_in_a - a_start) * f)
            m.set_opacity(1.0 if ph < 0.35 else 0.0)
        tok_a.add_updater(tok_a_upd)

        def tok_b_upd(m):
            ph = (t.get_value() / LOOP) % 1.0
            f = min(1.0, ph / 0.3)
            m.move_to(b_start + (alu_in_b - b_start) * f)
            m.set_opacity(1.0 if ph < 0.35 else 0.0)
        tok_b.add_updater(tok_b_upd)

        def tok_r_upd(m):
            ph = (t.get_value() / LOOP) % 1.0
            if ph < 0.6:
                m.set_opacity(0.0)
                m.move_to(alu_out)
            else:
                f = (ph - 0.6) / 0.4
                m.move_to(alu_out + (r2_pos - alu_out) * f)
                m.set_opacity(1.0)
        tok_r.add_updater(tok_r_upd)

        # ALU computation text + glow when result ready
        c_alu_dim = ManimColor("#15101F")
        c_alu_hot = ManimColor(VIOLET)

        def calc_upd(m):
            a, b, o = op_for(t.get_value())
            res = compute(a, b, o)
            ph = (t.get_value() / LOOP) % 1.0
            if ph < 0.5:
                txt = f"{a} {o} {b}"
                col = SECOND
            else:
                txt = f"{a} {o} {b} = {res}"
                col = INK
            new = Text(txt, font=MONO, color=col).scale(0.46)
            new.move_to(alu_c + DOWN * 0.1)
            m.become(new)
        calc.add_updater(calc_upd)

        def alu_box_upd(m):
            ph = (t.get_value() / LOOP) % 1.0
            hot = ph >= 0.5
            glow = max(0.0, 1.0 - abs(ph - 0.55) * 6.0) if hot else 0.0
            m.set_stroke(interpolate_color(c_alu_dim, c_alu_hot,
                         0.5 + 0.5 * glow), width=2.8 + 2.0 * glow)
            m.set_fill(interpolate_color(c_alu_dim, c_alu_hot, 0.1 + 0.2 *
                       glow), opacity=0.92)
        alu.add_updater(alu_box_upd)

        # register values update: R0,R1 are operands, R2 gets result
        def make_reg_val(idx):
            def _upd(m):
                a, b, o = op_for(t.get_value())
                res = compute(a, b, o)
                ph = (t.get_value() / LOOP) % 1.0
                if idx == 0:
                    v = a
                    col = TEAL
                elif idx == 1:
                    v = b
                    col = TEAL
                elif idx == 2:
                    v = res if ph >= 0.95 else (
                        res if ph >= 0.6 else "-")
                    col = VIOLET if ph >= 0.6 else SECOND
                else:
                    v = "-"
                    col = SECOND
                new = Text(str(v), font=MONO, color=col).scale(0.38)
                new.move_to(reg_boxes[idx].get_right() + LEFT * 0.42)
                m.become(new)
            return _upd
        for i, val in enumerate(reg_vals):
            val.add_updater(make_reg_val(i))

        # control-unit line pulses as it directs
        def cu_upd(m):
            s = 0.5 + 0.5 * np.sin(2 * np.pi * (t.get_value() / LOOP))
            m.set_stroke(opacity=0.3 + 0.5 * s)
        cu_line.add_updater(cu_upd)

        # input wires pulse when feeding
        def make_wire(lo, hi):
            def _upd(m):
                ph = (t.get_value() / LOOP) % 1.0
                active = lo <= ph < hi
                m.set_stroke(opacity=0.6 if active else 0.25,
                             width=2.5 if active else 2)
            return _upd
        in_a.add_updater(make_wire(0.0, 0.4))
        in_b.add_updater(make_wire(0.0, 0.4))
        out_w.add_updater(make_wire(0.6, 1.0))

        # caption
        cap = Text("registers hold numbers, the ALU does the maths",
                   font=HEAD, color=SECOND).scale(0.38)
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
