"""Simd — Single Instruction, Multiple Data broadcasting to parallel lanes.

ONE instruction box at the top ("x = x * 2") broadcasts down to MANY lanes,
each holding a different data item, all applying the same instruction in
lockstep on a loop. ~24s. green/teal.
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
TEAL = "#2DD4BF"
LIME = "#C6FF4D"

MONO = "JetBrains Mono"
HEAD = "Inter"


class Simd(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Single Instruction, Multiple Data", font=HEAD,
                     color=INK, weight="BOLD").scale(0.78).to_edge(UP, buff=0.4)
        self.play(Write(title, run_time=0.8))

        # ---------------- One instruction box at the top ------------------
        instr_glow = RoundedRectangle(width=3.6, height=1.0, corner_radius=0.14,
                                      stroke_color=TEAL, stroke_width=12,
                                      fill_opacity=0.0).set_stroke(opacity=0.2)
        instr = RoundedRectangle(width=3.4, height=0.9, corner_radius=0.12,
                                 stroke_color=TEAL, stroke_width=2.5,
                                 fill_color=TEAL, fill_opacity=0.1)
        instr_txt = Text("x = x * 2", font=MONO, color=INK).scale(0.6)
        instr_tag = Text("one instruction", font=MONO, color=TEAL).scale(0.35)
        instr_box = VGroup(instr_glow, instr, instr_txt)
        instr_box.move_to([0, 1.9, 0])
        instr_tag.next_to(instr_box, UP, buff=0.12)
        self.play(FadeIn(instr_box, run_time=0.7), FadeIn(instr_tag))

        # ---------------- Many parallel lanes -----------------------------
        n_lanes = 12
        lane_w = 0.78
        gap = 0.12
        total_w = n_lanes * lane_w + (n_lanes - 1) * gap
        x0 = -total_w / 2 + lane_w / 2
        lane_y = -1.3
        data_start = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        lanes = VGroup()
        connectors = VGroup()
        values = VGroup()
        for i in range(n_lanes):
            x = x0 + i * (lane_w + gap)
            glow = RoundedRectangle(width=lane_w + 0.08, height=1.0,
                                    corner_radius=0.08, stroke_color=GREEN,
                                    stroke_width=10, fill_opacity=0.0)
            glow.set_stroke(opacity=0.0)
            cell = RoundedRectangle(width=lane_w, height=0.92, corner_radius=0.07,
                                    stroke_color=GREEN, stroke_width=1.8,
                                    fill_color=GREEN, fill_opacity=0.08)
            grp = VGroup(glow, cell).move_to([x, lane_y, 0])
            lanes.add(grp)

            conn = Line([0, instr_box.get_bottom()[1], 0],
                        [x, lane_y + 0.55, 0], color=SUB, stroke_width=1.4)
            conn.set_opacity(0.3)
            connectors.add(conn)

            val = Text(str(data_start[i]), font=MONO, color=INK).scale(0.5)
            val.move_to([x, lane_y, 0])
            values.add(val)

        self.play(Create(connectors, run_time=0.8))
        self.play(FadeIn(lanes, run_time=0.6), FadeIn(values, run_time=0.6))

        caption = Text(
            "one instruction, thousands of data - because every pixel is independent",
            font=MONO, color=SUB).scale(0.4)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, run_time=0.6))

        # ---------------- Master clock: lockstep broadcast loop -----------
        clock = ValueTracker(0.0)
        period = 3.0  # one broadcast-apply cycle

        def instr_updater(m):
            t = clock.get_value()
            ph = (t % period) / period
            # pulse when the instruction "fires" (start of each cycle)
            fire = max(0.0, 1.0 - ph * 3.0)
            glow, box, txt = m
            glow.set_stroke(TEAL, opacity=0.2 + 0.6 * fire)
            box.set_fill(TEAL, opacity=0.1 + 0.3 * fire)

        instr_box.add_updater(instr_updater)

        def conn_updater(m):
            t = clock.get_value()
            ph = (t % period) / period
            # a pulse travels down all connectors simultaneously (lockstep)
            for conn in m:
                glow = max(0.0, 1.0 - abs(ph - 0.25) * 4.0)
                conn.set_stroke(TEAL, opacity=0.25 + 0.6 * glow,
                                width=1.4 + 2.0 * glow)

        connectors.add_updater(conn_updater)

        def lane_updater_factory(idx):
            def upd(m):
                t = clock.get_value()
                ph = (t % period) / period
                # all lanes light in lockstep at the same phase
                glow_lane = max(0.0, 1.0 - abs(ph - 0.45) * 3.5)
                g, cell = m
                cell.set_fill(GREEN, opacity=0.08 + 0.6 * glow_lane)
                cell.set_stroke(GREEN, width=1.8 + 2.0 * glow_lane,
                                opacity=0.6 + 0.4 * glow_lane)
                g.set_stroke(GREEN, opacity=0.35 * glow_lane)
            return upd

        for i in range(n_lanes):
            lanes[i].add_updater(lane_updater_factory(i))

        # Values double each cycle (then reset) to show the SAME op applied.
        def value_updater_factory(idx):
            base = data_start[idx]

            def upd(m):
                t = clock.get_value()
                cyc = int(t / period)
                ph = (t % period) / period
                # after the apply-pulse (ph>0.5) show doubled value for this cycle
                mult = 2 ** (cyc % 4)
                shown = base * (mult * 2 if ph > 0.5 else mult)
                # keep numbers readable
                new = Text(str(shown), font=MONO, color=INK).scale(0.5)
                new.move_to([x0 + idx * (lane_w + gap), lane_y, 0])
                m.become(new)
            return upd

        for i in range(n_lanes):
            values[i].add_updater(value_updater_factory(i))

        total = 19.0
        steps = 5
        for i in range(steps):
            self.play(clock.animate.set_value((i + 1) * total / steps),
                      run_time=total / steps, rate_func=rate_functions.linear)

        instr_box.clear_updaters()
        connectors.clear_updaters()
        for i in range(n_lanes):
            lanes[i].clear_updaters()
            values[i].clear_updaters()
        for i in range(n_lanes):
            lanes[i][1].set_fill(GREEN, opacity=0.4)
            lanes[i][1].set_stroke(GREEN, width=2.0, opacity=0.9)
        self.wait(0.3)
