"""Rings — CPU privilege rings (~24s).

Four concentric privilege rings like a target:
    Ring 0 (centre) = KERNEL (green), Ring 1/2 = drivers / services,
    Ring 3 (outer)  = USER APPS (silver).

"most privileged" at centre, "least privileged" outside. A system call crosses
from Ring 3 inward through a small gate to Ring 0, with a response back, on a
loop. Rings breathe/pulse continuously.
"""

from manim import (
    VGroup,
    Circle,
    Annulus,
    Line,
    Dot,
    Arc,
    Text,
    Scene,
    ValueTracker,
    Create,
    FadeIn,
    GrowFromCenter,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    TAU,
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


class Rings(Scene):
    def construct(self):
        self.camera.background_color = BG
        clock = ValueTracker(0.0)
        center = DOWN * 0.3

        title = head("PRIVILEGE RINGS", size=36, color=INK).to_edge(UP, buff=0.5)
        sub = mono("// who the CPU trusts, in layers", size=20, color=INK2)
        sub.next_to(title, DOWN, buff=0.16)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(sub), run_time=0.4)

        # Radii for four rings (0 = innermost disk).
        radii = [0.95, 1.85, 2.75, 3.55]
        ring_specs = [
            ("KERNEL", GREEN),          # ring 0 (disk)
            ("drivers", TEAL),          # ring 1
            ("services", VIOLET),       # ring 2
            ("USER APPS", SILVER),      # ring 3
        ]

        ring_mobs = []
        glow_mobs = []
        # Outer-to-inner draw so inner sits on top.
        # Ring 0 is a filled disk; rings 1-3 are annuli.
        disk = Circle(radius=radii[0], stroke_color=GREEN, stroke_width=3,
                      fill_color=GREEN, fill_opacity=0.12).move_to(center)
        disk_glow = Circle(radius=radii[0] + 0.08, stroke_color=GREEN,
                           stroke_width=10, stroke_opacity=0.18,
                           fill_opacity=0.0).move_to(center)

        annuli = []
        for i in range(1, 4):
            col = ring_specs[i][1]
            an = Annulus(inner_radius=radii[i - 1], outer_radius=radii[i],
                         stroke_color=col, stroke_width=2.2,
                         fill_color=col, fill_opacity=0.045).move_to(center)
            an_glow = Circle(radius=radii[i], stroke_color=col,
                             stroke_width=8, stroke_opacity=0.12,
                             fill_opacity=0.0).move_to(center)
            annuli.append((an, an_glow, col, i))

        # Draw outer first.
        self.play(Create(annuli[2][0]), FadeIn(annuli[2][1]), run_time=0.45)
        self.play(Create(annuli[1][0]), FadeIn(annuli[1][1]), run_time=0.45)
        self.play(Create(annuli[0][0]), FadeIn(annuli[0][1]), run_time=0.45)
        self.play(FadeIn(disk_glow), GrowFromCenter(disk), run_time=0.5)

        ring_mobs = [disk] + [a[0] for a in annuli]
        glow_mobs = [disk_glow] + [a[1] for a in annuli]

        # Ring labels: centre label + ring band labels placed along top.
        labels = VGroup()
        kern_lbl = mono("KERNEL", size=20, color=GREEN).move_to(center)
        labels.add(kern_lbl)
        band_angle = PI / 2  # place along top
        for i in range(1, 4):
            name, col = ring_specs[i]
            r_mid = (radii[i - 1] + radii[i]) / 2
            pos = center + np.array([np.cos(band_angle), np.sin(band_angle), 0]) * r_mid
            bl = mono(name, size=17, color=col).move_to(pos)
            labels.add(bl)
        self.play(FadeIn(labels), run_time=0.5)

        # Ring number ticks (Ring 0..3) along the right radius.
        ringnums = VGroup()
        for i in range(4):
            r = radii[i] - (radii[i] - (radii[i - 1] if i else 0)) / 2
            pos = center + RIGHT * r
            t = mono(f"R{i}", size=14, color=INK2).move_to(pos)
            ringnums.add(t)
        self.play(FadeIn(ringnums), run_time=0.4)

        # Privilege annotations.
        most = mono("most privileged", size=16, color=GREEN)
        most.next_to([center[0], center[1] - radii[0] - 0.0, 0], ORIGIN)
        most.move_to(center + DOWN * 0.0)  # near centre, offset below label
        most.next_to(kern_lbl, DOWN, buff=0.12)
        least = mono("least privileged", size=16, color=SILVER)
        least.move_to(center + DOWN * (radii[3] + 0.35))
        self.play(FadeIn(most), FadeIn(least), run_time=0.45)

        # A small "gate" on the ring boundaries where syscalls pass through.
        gate_angle = -PI / 2 + 0.35
        gate_dir = np.array([np.cos(gate_angle), np.sin(gate_angle), 0])
        gate = Line(center + gate_dir * (radii[0] - 0.15),
                    center + gate_dir * radii[3],
                    stroke_color=AMBER, stroke_width=2.5,
                    stroke_opacity=0.5)
        gate_lbl = mono("syscall gate", size=14, color=AMBER)
        gate_lbl.move_to(center + gate_dir * (radii[3] + 0.5))
        self.play(Create(gate), FadeIn(gate_lbl), run_time=0.5)

        # ===================== CONTINUOUS MOTION =====================
        # Syscall packet: from outer (R3) inward to centre, then response back.
        start = center + gate_dir * radii[3]
        end = center + gate_dir * (radii[0] - 0.1)

        req = Dot(radius=0.1, color=SILVER).set_z_index(6).move_to(start)
        resp = Dot(radius=0.09, color=GREEN).set_z_index(6).move_to(end)
        resp.set_opacity(0.0)
        req_trail = mono("syscall", size=13, color=SILVER).set_z_index(6)

        def syscall_up(m):
            t = clock.get_value()
            phase = t % 3.0
            if phase < 1.3:
                a = rate_functions.ease_in_out_sine(phase / 1.3)
                p = start + (end - start) * a
                m.move_to(p)
                m.set_opacity(1.0)
                m.set_color(SILVER)
            else:
                m.set_opacity(0.0)
        req.add_updater(syscall_up)

        def resp_up(m):
            t = clock.get_value()
            phase = t % 3.0
            if 1.5 <= phase < 2.8:
                a = rate_functions.ease_in_out_sine((phase - 1.5) / 1.3)
                p = end + (start - end) * a
                m.move_to(p)
                m.set_opacity(1.0)
            else:
                m.set_opacity(0.0)
        resp.add_updater(resp_up)

        def trail_up(m):
            m.next_to(req, RIGHT, buff=0.12)
            m.set_opacity(req.get_fill_opacity())
        req_trail.add_updater(trail_up)

        # Breathing rings — stroke width + glow oscillation, phase-staggered.
        for i, (rm, gm) in enumerate(zip(ring_mobs, glow_mobs)):
            def make(gg=gm, ph=i * 0.7):
                def up(m):
                    t = clock.get_value()
                    w = 8 + 7 * (0.5 + 0.5 * np.sin(t * 1.6 + ph))
                    gg.set_stroke(width=w)
                return up
            gm.add_updater(make())

        # Flash the kernel disk when a syscall arrives at centre.
        def disk_flash(m):
            t = clock.get_value()
            phase = t % 3.0
            if 1.3 <= phase < 1.6:
                m.set_fill(GREEN, opacity=0.4)
                m.set_stroke(width=5)
            else:
                m.set_fill(GREEN, opacity=0.12)
                m.set_stroke(width=3)
        disk.add_updater(disk_flash)

        # Slow sweeping radar line for telemetry feel.
        sweep = Line(center, center + RIGHT * radii[3],
                     stroke_color=AMBER, stroke_width=1.2,
                     stroke_opacity=0.25).set_z_index(1)

        def sweep_up(m):
            t = clock.get_value()
            ang = (t * 0.6) % TAU
            d = np.array([np.cos(ang), np.sin(ang), 0])
            m.put_start_and_end_on(center, center + d * radii[3])
        sweep.add_updater(sweep_up)

        # HUD ring/mode indicator.
        mode = mono("CPL: 3 (user)", size=18, color=SILVER)
        mode.to_corner(DOWN + RIGHT, buff=0.6)

        def mode_up(m):
            t = clock.get_value()
            phase = t % 3.0
            if phase < 1.3 or phase >= 2.8:
                txt, col = "CPL: 3 (user)", SILVER
            else:
                txt, col = "CPL: 0 (kernel)", GREEN
            new = mono(txt, size=18, color=col)
            new.move_to(m, aligned_edge=RIGHT)
            m.become(new)
        mode.add_updater(mode_up)

        self.add(sweep, req, resp, req_trail, mode)

        self.play(clock.animate.set_value(13.5),
                  run_time=13.5, rate_func=rate_functions.linear)

        # Clean final frame.
        for m in (req, resp, req_trail, sweep, mode, disk, *glow_mobs):
            m.clear_updaters()
        req.set_opacity(0.0)
        resp.set_opacity(0.0)
        req_trail.set_opacity(0.0)
        sweep.set_opacity(0.0)
        self.wait(0.3)
