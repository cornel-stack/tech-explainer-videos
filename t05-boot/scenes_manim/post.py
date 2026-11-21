"""Post — the COLD OPEN. Power-on self-test (POST).

A stylized firmware/board: a central amber chip with component nodes lighting
up in sequence as power surges in, beside a POST checklist that ticks line by
line with a small flash on each OK.

Telemetry-dark palette. Continuous motion for the whole ~22s via a master-clock
ValueTracker driving travelling power pulses and breathing nodes.
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
    GrowFromCenter,
    rate_functions,
    there_and_back,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
)
import numpy as np

# --- Telemetry-dark palette ---------------------------------------------------
BG = "#08080B"
INK = "#EDECE6"
INK2 = "#8E8E8A"
AMBER = "#FFB020"
TEAL = "#2DD4BF"
GREEN = "#35FF9E"
VIOLET = "#9B8CFF"
CORAL = "#FF6B4A"
SILVER = "#C9CDD4"

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


class Post(Scene):
    def construct(self):
        self.camera.background_color = BG

        clock = ValueTracker(0.0)

        # --- Heading ----------------------------------------------------------
        title = head("POWER-ON SELF-TEST", size=36, color=INK)
        title.to_edge(UP, buff=0.55)
        sub = mono("// ignition — first milliseconds", size=20, color=INK2)
        sub.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)

        # ============================ LEFT: BOARD ============================
        board = RoundedRectangle(
            width=6.2, height=5.4, corner_radius=0.18,
            stroke_color=INK2, stroke_width=1.5, fill_opacity=0.0,
        )
        board.move_to(LEFT * 3.4 + DOWN * 0.35)

        # Central chip (amber), soft glow behind a crisp square.
        chip_glow = RoundedRectangle(
            width=2.1, height=2.1, corner_radius=0.12,
            stroke_color=AMBER, stroke_width=10, stroke_opacity=0.18,
            fill_opacity=0.0,
        ).move_to(board.get_center())
        chip = RoundedRectangle(
            width=2.0, height=2.0, corner_radius=0.1,
            stroke_color=AMBER, stroke_width=2.5,
            fill_color=AMBER, fill_opacity=0.08,
        ).move_to(board.get_center())
        chip_lbl = mono("CPU", size=24, color=AMBER).move_to(chip.get_center())

        # Chip pins (little ticks around the square).
        pins = VGroup()
        for side, axis in ((UP, RIGHT), (DOWN, RIGHT), (LEFT, UP), (RIGHT, UP)):
            edge = chip.get_edge_center(side)
            for k in (-0.6, -0.2, 0.2, 0.6):
                base = edge + axis * k
                tick = Line(base, base + side * 0.14,
                            stroke_color=AMBER, stroke_width=2,
                            stroke_opacity=0.6)
                pins.add(tick)

        # Component nodes around the chip (light up in sequence).
        node_specs = [
            ("RAM", UP * 1.9 + LEFT * 1.7, TEAL),
            ("ROM", UP * 1.9 + RIGHT * 1.7, AMBER),
            ("I/O", DOWN * 1.9 + LEFT * 1.7, VIOLET),
            ("GPU", DOWN * 1.9 + RIGHT * 1.7, GREEN),
            ("CLK", UP * 2.05, SILVER),
            ("PWR", DOWN * 2.05, CORAL),
        ]
        nodes = VGroup()
        node_items = []
        for name, off, col in node_specs:
            pos = board.get_center() + off
            n = RoundedRectangle(
                width=1.0, height=0.6, corner_radius=0.08,
                stroke_color=col, stroke_width=1.8,
                fill_color=col, fill_opacity=0.05,
            ).move_to(pos)
            nl = mono(name, size=16, color=col).move_to(pos)
            # connector from chip toward node
            conn = Line(chip.get_center(), pos,
                        stroke_color=INK2, stroke_width=1.2,
                        stroke_opacity=0.35)
            conn.set_z_index(-1)
            nodes.add(conn, n, nl)
            node_items.append((n, nl, conn, col))

        self.play(Create(board), run_time=0.7)
        self.play(
            FadeIn(chip_glow), Create(chip), FadeIn(chip_lbl),
            Create(pins), run_time=0.9,
        )
        self.play(*[FadeIn(c) for (_, _, c, _) in node_items], run_time=0.5)
        self.play(
            *[GrowFromCenter(VGroup(n, nl)) for (n, nl, _, _) in node_items],
            run_time=0.9,
        )

        # ========================= RIGHT: CHECKLIST =========================
        panel = RoundedRectangle(
            width=6.0, height=5.4, corner_radius=0.16,
            stroke_color=INK2, stroke_width=1.5, fill_opacity=0.0,
        )
        panel.move_to(RIGHT * 3.6 + DOWN * 0.35)
        panel_hdr = mono("POST CHECKLIST", size=22, color=INK)
        panel_hdr.move_to(panel.get_top() + DOWN * 0.5)
        hdr_rule = Line(panel.get_left() + DOWN * 0.95,
                        panel.get_right() + DOWN * 0.95,
                        stroke_color=INK2, stroke_width=1,
                        stroke_opacity=0.4)
        hdr_rule.set_x(panel.get_x())

        self.play(Create(panel), FadeIn(panel_hdr), Create(hdr_rule),
                  run_time=0.6)

        check_specs = [
            "CPU ........ OK",
            "RAM ........ OK",
            "VIDEO ...... OK",
            "KEYBOARD ... OK",
            "BOOT ORDER . OK",
        ]
        rows = VGroup()
        checks = []
        y0 = panel.get_top()[1] - 1.5
        for i, txt in enumerate(check_specs):
            row = mono(txt, size=24, color=INK2)
            row.move_to(panel.get_center())
            row.set_x(panel.get_left()[0] + 2.5)
            row.set_y(y0 - i * 0.85)
            # The trailing "OK" starts hidden-ish; we recolor on tick.
            mark = mono("[ ]", size=22, color=INK2)
            mark.next_to(row, LEFT, buff=0.3)
            flash = Dot(radius=0.12, color=GREEN).move_to(mark.get_center())
            flash.set_opacity(0.0)
            rows.add(mark, row, flash)
            checks.append((mark, row, flash))

        self.play(FadeIn(rows), run_time=0.5)

        # Tick each line with a small flash + power surge to a board node.
        order = [0, 1, 5, 4, 3]  # which node pulses alongside each check
        for i, (mark, row, flash) in enumerate(checks):
            # recolor row to show it's confirmed OK
            new_mark = mono("[x]", size=22, color=GREEN).move_to(mark.get_center())
            # light the related node brighter
            idx = order[i % len(order)]
            node, nl, _, col = node_items[idx]
            self.play(
                flash.animate.set_opacity(0.9),
                mark.animate.set_opacity(0.0),
                FadeIn(new_mark),
                row.animate.set_color(INK),
                node.animate.set_fill(col, opacity=0.22).set_stroke(width=3.2),
                run_time=0.34,
            )
            self.play(
                flash.animate.set_opacity(0.0),
                node.animate.set_stroke(width=1.8),
                run_time=0.24,
            )
            mark.become(new_mark)

        # ===================== CONTINUOUS MOTION CORE =====================
        # A travelling power pulse that cycles from PWR through the chip to
        # each node, plus breathing on the chip glow.
        pulse = Dot(radius=0.09, color=AMBER)
        pulse.set_z_index(3)
        center = chip.get_center()
        pwr_pos = node_items[5][0].get_center()
        ring_nodes = [node_items[k][0].get_center() for k in (0, 1, 3, 4, 2)]

        def pulse_updater(m):
            t = clock.get_value()
            phase = t % 2.0
            if phase < 1.0:
                # PWR -> chip
                a = phase
                p = pwr_pos + (center - pwr_pos) * rate_functions.ease_in_out_sine(a)
            else:
                # chip -> a rotating target node
                a = phase - 1.0
                idx = int(t // 2.0) % len(ring_nodes)
                tgt = ring_nodes[idx]
                p = center + (tgt - center) * rate_functions.ease_in_out_sine(a)
            m.move_to(p)

        pulse.add_updater(pulse_updater)

        def glow_updater(m):
            t = clock.get_value()
            w = 10 + 6 * (0.5 + 0.5 * np.sin(t * 2.4))
            m.set_stroke(width=w)
        chip_glow.add_updater(glow_updater)

        # Breathing nodes — subtle fill opacity oscillation.
        for k, (n, nl, conn, col) in enumerate(node_items):
            def make(nn=n, cc=col, ph=k * 0.8):
                def up(m):
                    t = clock.get_value()
                    o = 0.10 + 0.10 * (0.5 + 0.5 * np.sin(t * 2.0 + ph))
                    m.set_fill(cc, opacity=o)
                return up
            n.add_updater(make())

        # A HUD counter ticking up (telemetry register).
        counter = mono("0x0000", size=20, color=AMBER)
        counter.next_to(panel, DOWN, buff=0.25).set_x(panel.get_x())

        def counter_updater(m):
            t = clock.get_value()
            val = int(t * 4096) & 0xFFFF
            new = mono(f"0x{val:04X}", size=20, color=AMBER)
            new.move_to(m)
            m.become(new)
        counter.add_updater(counter_updater)
        self.add(pulse, counter)

        # Sweep highlight bar travelling down the checklist.
        sweep = Rectangle(
            width=panel.width - 0.4, height=0.7,
            stroke_width=0, fill_color=AMBER, fill_opacity=0.08,
        )
        sweep.set_z_index(-1)

        def sweep_updater(m):
            t = clock.get_value()
            frac = (np.sin(t * 1.1) * 0.5 + 0.5)
            top = y0 + 0.2
            bot = y0 - 4 * 0.85 - 0.2
            m.set_x(panel.get_x())
            m.set_y(top + (bot - top) * frac)
        sweep.add_updater(sweep_updater)
        self.add(sweep)

        # Drive the master clock for the remainder of the runtime.
        self.play(clock.animate.set_value(12.0),
                  run_time=12.0, rate_func=rate_functions.linear)

        # --- Clean final frame: clear updaters --------------------------------
        for m in (pulse, chip_glow, counter, sweep, *[n for (n, *_rest) in node_items]):
            m.clear_updaters()
        pulse.set_opacity(0.0)
        sweep.set_opacity(0.0)
        self.wait(0.3)
