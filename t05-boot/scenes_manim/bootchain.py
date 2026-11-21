"""BootChain — the MASTER hand-off diagram (~26s).

A vertical chain of 5 labelled stages with a glowing pulse travelling down the
spine on a loop:

    FIRMWARE (UEFI/BIOS) [amber] -> BOOTLOADER [teal] -> KERNEL [green]
        -> PID 1 / init [violet] -> USER SPACE [silver]

At the BOOTLOADER->KERNEL step the diagram branches into three labelled OS
columns (text only, no logos). The main pulse flows down the spine
continuously; the three columns gently pulse.
"""

from manim import (
    VGroup,
    RoundedRectangle,
    Line,
    Dot,
    Text,
    Scene,
    ValueTracker,
    Create,
    FadeIn,
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


class BootChain(Scene):
    def construct(self):
        self.camera.background_color = BG
        clock = ValueTracker(0.0)

        title = head("THE BOOT CHAIN", size=36, color=INK).to_edge(UP, buff=0.5)
        sub = mono("// five hand-offs, power to prompt", size=20, color=INK2)
        sub.next_to(title, DOWN, buff=0.16)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(sub), run_time=0.4)

        # ----- Spine stages (left column) -----
        stages = [
            ("FIRMWARE (UEFI/BIOS)", AMBER),
            ("BOOTLOADER", TEAL),
            ("KERNEL", GREEN),
            ("PID 1 / init", VIOLET),
            ("USER SPACE", SILVER),
        ]
        spine_x = -4.2
        top_y = 2.35
        gap = 1.18

        nodes = []
        node_group = VGroup()
        for i, (label, col) in enumerate(stages):
            y = top_y - i * gap
            glow = RoundedRectangle(
                width=3.5, height=0.82, corner_radius=0.14,
                stroke_color=col, stroke_width=9, stroke_opacity=0.16,
                fill_opacity=0.0,
            ).move_to([spine_x, y, 0])
            box = RoundedRectangle(
                width=3.4, height=0.74, corner_radius=0.12,
                stroke_color=col, stroke_width=2.2,
                fill_color=col, fill_opacity=0.06,
            ).move_to([spine_x, y, 0])
            lbl = mono(label, size=19, color=col).move_to(box.get_center())
            nodes.append((glow, box, lbl, col, np.array([spine_x, y, 0])))
            node_group.add(glow, box, lbl)

        # Connectors between stages
        connectors = VGroup()
        for i in range(len(nodes) - 1):
            a = nodes[i][1].get_bottom()
            b = nodes[i + 1][1].get_top()
            ln = Line(a, b, stroke_color=INK2, stroke_width=1.6,
                      stroke_opacity=0.45)
            connectors.add(ln)

        self.play(Create(connectors), run_time=0.5)
        for (glow, box, lbl, col, pos) in nodes:
            self.play(FadeIn(glow), Create(box), FadeIn(lbl), run_time=0.32)

        # ----- Three OS columns branching at BOOTLOADER -> KERNEL -----
        boot_node = nodes[1]
        kern_node = nodes[2]
        branch_src = (boot_node[4] + kern_node[4]) / 2.0

        os_cols = [
            ("Windows", ["bootmgr", "winload", "ntoskrnl", "smss"], TEAL),
            ("Linux", ["GRUB", "vmlinuz", "systemd"], GREEN),
            ("macOS", ["iBoot", "kernel", "launchd"], VIOLET),
        ]
        col_xs = [-0.3, 2.6, 5.4]
        col_top = 2.1
        col_group = VGroup()
        col_items = []
        for (name, steps, col), cx in zip(os_cols, col_xs):
            hdr = mono(name, size=22, color=col).move_to([cx, col_top, 0])
            underline = Line([cx - 1.05, col_top - 0.3, 0],
                             [cx + 1.05, col_top - 0.3, 0],
                             stroke_color=col, stroke_width=1.5,
                             stroke_opacity=0.6)
            steps_g = VGroup()
            for j, s in enumerate(steps):
                sy = col_top - 0.9 - j * 0.72
                chip = RoundedRectangle(
                    width=2.1, height=0.52, corner_radius=0.1,
                    stroke_color=col, stroke_width=1.6,
                    fill_color=col, fill_opacity=0.05,
                ).move_to([cx, sy, 0])
                st = mono(s, size=17, color=INK).move_to(chip.get_center())
                steps_g.add(chip, st)
                if j < len(steps) - 1:
                    arr = Line([cx, sy - 0.26, 0], [cx, sy - 0.46, 0],
                               stroke_color=INK2, stroke_width=1.4,
                               stroke_opacity=0.5)
                    steps_g.add(arr)
            col_group.add(hdr, underline, steps_g)
            col_items.append((cx, col, steps_g))

        # Branch connectors from spine midpoint to each column header
        branch_lines = VGroup()
        for cx, col, _ in col_items:
            bl = Line(branch_src + RIGHT * 1.75,
                      [cx, col_top + 0.3, 0],
                      stroke_color=col, stroke_width=1.4,
                      stroke_opacity=0.4)
            branch_lines.add(bl)

        self.play(Create(branch_lines), run_time=0.5)
        self.play(FadeIn(col_group), run_time=0.8)

        # ===================== CONTINUOUS MOTION =====================
        # Main pulse travels down the spine on a loop.
        spine_pts = [n[4] for n in nodes]
        n_seg = len(spine_pts) - 1
        pulse = Dot(radius=0.11, color=INK).set_z_index(5)

        def spine_pulse(m):
            t = clock.get_value()
            frac = (t / 3.0) % 1.0  # full trip every 3s
            pos = frac * n_seg
            seg = min(int(pos), n_seg - 1)
            local = pos - seg
            a = spine_pts[seg]
            b = spine_pts[seg + 1]
            p = a + (b - a) * rate_functions.ease_in_out_sine(local)
            m.move_to(p)
            # color = destination stage color
            m.set_color(nodes[min(seg + 1, len(nodes) - 1)][3])
        pulse.add_updater(spine_pulse)

        # Highlight the active spine node as the pulse passes.
        for i, (glow, box, lbl, col, pos) in enumerate(nodes):
            def make(gg=glow, bb=box, idx=i):
                def up(m):
                    t = clock.get_value()
                    frac = (t / 3.0) % 1.0
                    active = frac * n_seg
                    dist = abs(active - idx)
                    bright = max(0.0, 1.0 - dist)
                    gg.set_stroke(width=9 + 10 * bright,
                                  opacity=0.16 + 0.35 * bright)
                    bb.set_stroke(width=2.2 + 2.0 * bright)
                return up
            glow.add_updater(make())

        # Gentle pulsing of the three OS columns.
        for k, (cx, col, steps_g) in enumerate(col_items):
            def make_col(sg=steps_g, cc=col, ph=k * 1.1):
                def up(m):
                    t = clock.get_value()
                    o = 0.05 + 0.08 * (0.5 + 0.5 * np.sin(t * 1.8 + ph))
                    for sub_m in m:
                        if isinstance(sub_m, RoundedRectangle):
                            sub_m.set_fill(cc, opacity=o)
                return up
            steps_g.add_updater(make_col())

        # Travelling pulses down each OS column (offset phases).
        col_pulses = VGroup()
        for k, (cx, col, steps_g) in enumerate(col_items):
            cp = Dot(radius=0.07, color=col).set_z_index(5)
            boxes = [s for s in steps_g if isinstance(s, RoundedRectangle)]
            if not boxes:
                continue
            ys = [bx.get_center()[1] for bx in boxes]
            ytop, ybot = max(ys), min(ys)

            def make_cp(xx=cx, yt=ytop, yb=ybot, ph=k * 0.9):
                def up(m):
                    t = clock.get_value()
                    frac = ((t + ph) / 2.4) % 1.0
                    y = yt + (yb - yt) * frac
                    m.move_to([xx, y, 0])
                return up
            cp.add_updater(make_cp())
            col_pulses.add(cp)

        # HUD tick counter.
        counter = mono("stage 0/5", size=20, color=INK2)
        counter.to_corner(DOWN + LEFT, buff=0.6)

        def counter_up(m):
            t = clock.get_value()
            frac = (t / 3.0) % 1.0
            stage = min(int(frac * n_seg) + 1, 5)
            new = mono(f"stage {stage}/5  >>", size=20,
                       color=nodes[min(stage - 1, 4)][3])
            new.move_to(m, aligned_edge=LEFT)
            m.become(new)
        counter.add_updater(counter_up)

        self.add(pulse, col_pulses, counter)

        self.play(clock.animate.set_value(15.0),
                  run_time=15.0, rate_func=rate_functions.linear)

        # Clean final frame.
        pulse.clear_updaters()
        counter.clear_updaters()
        for cp in col_pulses:
            cp.clear_updaters()
            cp.set_opacity(0.0)
        for (glow, box, lbl, col, pos) in nodes:
            glow.clear_updaters()
        for (cx, col, steps_g) in col_items:
            steps_g.clear_updaters()
        pulse.set_opacity(0.0)
        self.wait(0.3)
