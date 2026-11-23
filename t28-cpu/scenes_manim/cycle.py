"""Scene 4: fetch, decode, execute -- repeat, billions of times.

Class `Cycle` (~19s). THE core loop: three stages FETCH -> DECODE -> EXECUTE
arranged in a cycle. An instruction token travels from MEMORY into FETCH, to
DECODE (control unit reads it), to EXECUTE, then loops back for the next. A
pulse runs the loop repeatedly. Caption: "fetch, decode, execute -- repeat,
billions of times".

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
    Square,
    Dot,
    Arc,
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


class Cycle(Scene):
    def construct(self):
        title = Text("The fetch-decode-execute loop", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- MEMORY on the left ---------------------------------------------
        mem_box = RoundedRectangle(corner_radius=0.12, width=1.5, height=2.6,
                                   stroke_color=TEAL, stroke_width=2.5,
                                   fill_color="#111318", fill_opacity=0.9)
        mem_box.move_to([-5.0, 0.0, 0])
        mem_lbl = Text("MEMORY", font=MONO, color=TEAL).scale(0.3)
        mem_lbl.next_to(mem_box, UP, buff=0.15)
        mem_cells = VGroup()
        instrs = ["LD", "ADD", "ST", "JMP", "MUL"]
        mem_tx = []
        for i in range(5):
            c = Square(side_length=0.42, stroke_color=TEAL, stroke_width=1.5,
                       fill_color="#0E1A1A", fill_opacity=0.9)
            c.move_to(mem_box.get_center() + UP * ((2 - i) * 0.5))
            tx = Text(instrs[i], font=MONO, color=TEAL).scale(0.22)
            tx.move_to(c.get_center())
            mem_cells.add(c, tx)
            mem_tx.append(tx)
        self.play(Create(mem_box), FadeIn(mem_lbl), FadeIn(mem_cells),
                  run_time=1.0)

        # --- three stages arranged around a cycle ---------------------------
        center = np.array([1.3, -0.1, 0.0])
        radius = 2.0
        stage_pos = {
            "FETCH": center + np.array([0.0, radius, 0.0]),
            "DECODE": center + np.array([radius * 0.87,
                                         -radius * 0.5, 0.0]),
            "EXECUTE": center + np.array([-radius * 0.87,
                                          -radius * 0.5, 0.0]),
        }
        stage_colors = {"FETCH": GREEN, "DECODE": VIOLET, "EXECUTE": AMBER}
        stage_boxes = {}
        stage_grp = VGroup()
        for name, pos in stage_pos.items():
            box = RoundedRectangle(corner_radius=0.12, width=1.8, height=0.95,
                                   stroke_color=stage_colors[name],
                                   stroke_width=2.5, fill_color="#111318",
                                   fill_opacity=0.9).move_to(pos)
            lbl = Text(name, font=MONO, color=stage_colors[name]).scale(0.32)
            lbl.move_to(pos)
            stage_boxes[name] = box
            stage_grp.add(box, lbl)

        dc_lbl = Text("control unit reads it", font=MONO,
                      color=VIOLET).scale(0.24)
        dc_lbl.next_to(stage_boxes["DECODE"], DOWN, buff=0.18)
        stage_grp.add(dc_lbl)
        self.play(FadeIn(stage_grp), run_time=1.0)

        # --- cyclic arrows between stages -----------------------------------
        order = ["FETCH", "DECODE", "EXECUTE"]
        arcs = VGroup()
        for i in range(3):
            a = stage_pos[order[i]]
            b = stage_pos[order[(i + 1) % 3]]
            mid = (a + b) / 2
            out = mid - center
            out = out / np.linalg.norm(out)
            ctrl = mid + out * 0.5
            arc = Line(a, b, stroke_color=SECOND, stroke_width=2,
                       stroke_opacity=0.4)
            arcs.add(arc)
        self.play(Create(arcs), run_time=0.7)

        # --- feed line memory -> FETCH --------------------------------------
        feed = Line(mem_box.get_right(), stage_pos["FETCH"] + LEFT * 0.9,
                    stroke_color=SECOND, stroke_width=2, stroke_opacity=0.4)
        self.add(feed)

        # instruction token
        token = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.44,
                                 stroke_color=INK, stroke_width=2,
                                 fill_color="#1A1A20", fill_opacity=1.0)
        token_tx = Text("ADD", font=MONO, color=INK).scale(0.22)
        token.move_to(mem_box.get_center())
        token_tx.move_to(token.get_center())
        token.set_z_index(10)
        token_tx.set_z_index(11)
        self.add(token, token_tx)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        LOOP = 3.0  # seconds per full fetch-decode-execute loop
        instr_cycle = ["LD", "ADD", "ST", "JMP", "MUL"]

        mem_right = mem_box.get_right()
        fetch_p = stage_pos["FETCH"]
        decode_p = stage_pos["DECODE"]
        execute_p = stage_pos["EXECUTE"]

        def token_pos(tt):
            ph = (tt / LOOP) % 1.0
            # 0.00-0.25 memory->fetch, 0.25-0.50 fetch->decode,
            # 0.50-0.75 decode->execute, 0.75-1.0 execute->memory(loop)
            if ph < 0.25:
                f = ph / 0.25
                return mem_right + (fetch_p - mem_right) * f
            elif ph < 0.5:
                f = (ph - 0.25) / 0.25
                return fetch_p + (decode_p - fetch_p) * f
            elif ph < 0.75:
                f = (ph - 0.5) / 0.25
                return decode_p + (execute_p - decode_p) * f
            else:
                f = (ph - 0.75) / 0.25
                return execute_p + (mem_right - execute_p) * f

        def current_instr(tt):
            loop_n = int(tt / LOOP)
            return instr_cycle[loop_n % len(instr_cycle)]

        def token_upd(m):
            m.move_to(token_pos(t.get_value()))
        token.add_updater(token_upd)

        def token_tx_upd(m):
            new = Text(current_instr(t.get_value()), font=MONO,
                       color=INK).scale(0.22)
            new.move_to(token_pos(t.get_value()))
            m.become(new)
        token_tx.add_updater(token_tx_upd)

        # each stage lights up while the token is in its quarter
        def make_stage_upd(name, lo, hi, color):
            c_dim = ManimColor("#2A2A30")
            c_hot = ManimColor(color)

            def _upd(m):
                ph = (t.get_value() / LOOP) % 1.0
                active = lo <= ph < hi
                target = c_hot if active else c_dim
                m.set_stroke(interpolate_color(c_dim, c_hot,
                             1.0 if active else 0.35),
                             width=3.0 if active else 2.0)
                m.set_fill("#15151C" if active else "#111318", opacity=0.9)
            return _upd
        stage_boxes["FETCH"].add_updater(
            make_stage_upd("FETCH", 0.0, 0.5, GREEN))
        stage_boxes["DECODE"].add_updater(
            make_stage_upd("DECODE", 0.5, 0.75, VIOLET))
        stage_boxes["EXECUTE"].add_updater(
            make_stage_upd("EXECUTE", 0.75, 1.0, AMBER))

        # arrows pulse around the loop
        for i, arc in enumerate(arcs):
            def make_arc(phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(
                        2 * np.pi * (t.get_value() / LOOP) - phase)
                    m.set_stroke(opacity=0.25 + 0.45 * s)
                return _upd
            arc.add_updater(make_arc(i * 2 * np.pi / 3))

        # memory cell being read highlights
        c_mem_dim = ManimColor("#0E1A1A")
        c_mem_hot = ManimColor(TEAL)

        def make_mem_cell(idx):
            def _upd(m):
                loop_n = int(t.get_value() / LOOP)
                reading = (loop_n % len(mem_tx)) == idx
                ph = (t.get_value() / LOOP) % 1.0
                hot = reading and ph < 0.25
                m.set_color(interpolate_color(c_mem_hot, ManimColor(INK),
                            0.6) if hot else c_mem_hot)
                m.set_opacity(1.0 if hot else 0.7)
            return _upd
        for i, tx in enumerate(mem_tx):
            tx.add_updater(make_mem_cell(i))

        # loop counter
        loop_txt = Text("loops: 0", font=MONO, color=SECOND).scale(0.3)
        loop_txt.move_to([1.3, -2.9, 0])

        def loop_upd(m):
            n = int(t.get_value() / LOOP)
            new = Text(f"loops: {n}", font=MONO, color=SECOND).scale(0.3)
            new.move_to([1.3, -2.9, 0])
            m.become(new)
        loop_txt.add_updater(loop_upd)
        self.add(loop_txt)

        # caption
        cap = Text("fetch, decode, execute -- repeat, billions of times",
                   font=HEAD, color=SECOND).scale(0.38)
        cap.to_edge(DOWN, buff=0.22)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
