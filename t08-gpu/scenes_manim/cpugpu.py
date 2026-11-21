"""Scene: CPU vs GPU — a few big cores vs thousands of simple cores.

Class `Cpugpu` (~24s). LEFT a CPU die outline with ~12 big labelled cores;
tasks trickle through them one at a time. RIGHT a GPU die outline packed with
a dense grid of ~200 tiny glowing dots; a flood of packets rains into the grid
in parallel. A hierarchy caption on the GPU side cycles die -> GPC -> SM ->
cores and surfaces real GA102 counts.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  red #FF5C47  blue #5AA9FF  amber #FFB020
  teal #2DD4BF  violet #B06BFF  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    rate_functions,
)

# --- palette -----------------------------------------------------------------
BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#76D64A"
RED = "#FF5C47"
BLUE = "#5AA9FF"
AMBER = "#FFB020"
TEAL = "#2DD4BF"
VIOLET = "#B06BFF"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Cpugpu(Scene):
    def construct(self):
        title = Text("A few big cores vs thousands of simple ones",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- CPU die (left) --------------------------------------------------
        cpu_die = RoundedRectangle(
            corner_radius=0.16, width=5.0, height=5.0,
            stroke_color=AMBER, stroke_width=2.5,
            fill_color="#17130A", fill_opacity=0.5,
        ).shift(LEFT * 3.5 + DOWN * 0.35)
        cpu_lbl = Text("CPU", font=MONO, color=AMBER, weight="BOLD").scale(0.4)
        cpu_lbl.next_to(cpu_die, UP, buff=0.12)

        # --- GPU die (right) -------------------------------------------------
        gpu_die = RoundedRectangle(
            corner_radius=0.16, width=5.0, height=5.0,
            stroke_color=GREEN, stroke_width=2.5,
            fill_color="#0D170A", fill_opacity=0.5,
        ).shift(RIGHT * 3.5 + DOWN * 0.35)
        gpu_lbl = Text("GPU", font=MONO, color=GREEN, weight="BOLD").scale(0.4)
        gpu_lbl.next_to(gpu_die, UP, buff=0.12)

        self.play(Create(cpu_die), Create(gpu_die), run_time=0.8)
        self.play(FadeIn(cpu_lbl), FadeIn(gpu_lbl), run_time=0.3)

        # --- CPU cores: 12 big labelled tiles (3x4) --------------------------
        cpu_cores = VGroup()
        cpu_glows = []
        for _ in range(12):
            tile = RoundedRectangle(
                corner_radius=0.08, width=1.05, height=0.9,
                stroke_color=AMBER, stroke_width=2,
                fill_color="#1A160D", fill_opacity=0.9,
            )
            glow = RoundedRectangle(
                corner_radius=0.08, width=1.05, height=0.9,
                stroke_color=AMBER, stroke_width=8, stroke_opacity=0.1,
                fill_opacity=0,
            ).move_to(tile)
            lbl = Text("CORE", font=MONO, color=AMBER).scale(0.2)
            lbl.move_to(tile.get_center())
            g = VGroup(glow, tile, lbl)
            g.glow = glow
            cpu_cores.add(g)
            cpu_glows.append(glow)
        cpu_cores.arrange_in_grid(rows=4, cols=3, buff=0.18)
        cpu_cores.move_to(cpu_die.get_center())

        # --- GPU cores: dense grid of ~200 tiny dots (14x15) -----------------
        gpu_dots = VGroup()
        G_ROWS, G_COLS = 14, 15
        for _ in range(G_ROWS * G_COLS):
            d = Dot(color=GREEN, radius=0.045)
            gpu_dots.add(d)
        gpu_dots.arrange_in_grid(rows=G_ROWS, cols=G_COLS, buff=0.14)
        gpu_dots.scale_to_fit_width(4.4)
        gpu_dots.move_to(gpu_die.get_center() + UP * 0.1)

        self.play(*[GrowFromCenter(c) for c in cpu_cores],
                  lag_ratio=0.05, run_time=1.0)
        self.play(*[GrowFromCenter(d) for d in gpu_dots],
                  lag_ratio=0.004, run_time=1.0)

        # --- Captions --------------------------------------------------------
        cap_cpu = Text("CPU — a few powerful cores", font=HEAD,
                       color=AMBER).scale(0.32)
        cap_gpu = Text("GPU — thousands of simple cores", font=HEAD,
                       color=GREEN).scale(0.32)
        cap_cpu.to_edge(DOWN, buff=0.5).shift(LEFT * 3.5)
        cap_gpu.to_edge(DOWN, buff=0.5).shift(RIGHT * 3.5)
        self.play(FadeIn(cap_cpu, shift=UP * 0.2),
                  FadeIn(cap_gpu, shift=UP * 0.2), run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # CPU core glow breathing.
        for i, g in enumerate(cpu_glows):
            def make_breath(gl, phase):
                def _upd(m):
                    tt = t.get_value()
                    gl.set_stroke(opacity=0.08 + 0.12 *
                                  (0.5 + 0.5 * np.sin(1.6 * tt + phase)))
                return _upd
            g.add_updater(make_breath(g, i * 0.5))

        # GPU dot twinkle (breathing glow via radius + opacity).
        for i, d in enumerate(gpu_dots):
            base = d.radius

            def make_twinkle(dot, base_r, phase):
                def _upd(m):
                    tt = t.get_value()
                    s = 0.5 + 0.5 * np.sin(2.4 * tt + phase)
                    dot.set_opacity(0.45 + 0.55 * s)
                return _upd
            d.add_updater(make_twinkle(d, base, (i % 37) * 0.31))

        # --- CPU: a few task packets trickle through cores, one at a time ----
        cpu_targets = [c.get_center() for c in cpu_cores]
        cpu_spawn = np.array([cpu_die.get_center()[0],
                              cpu_die.get_top()[1] - 0.15, 0])
        cpu_packets = VGroup()
        cpu_meta = []
        # Only 3 packets => serial trickle, one at a time feel.
        for k in range(3):
            dot = Dot(color=AMBER, radius=0.1)
            cpu_packets.add(dot)
            period = 6.0
            offset = k * 2.0
            cpu_meta.append((period, offset))

        def make_cpu_packet(meta, kk):
            period, offset = meta

            def _upd(m):
                tt = (t.get_value() + offset) % period
                # Which core this trip visits (cycles).
                trip = int((t.get_value() + offset) // period)
                target = np.array(cpu_targets[(kk + trip * 3) % len(cpu_targets)])
                frac = tt / period
                eased = rate_functions.ease_in_out_quad(min(frac * 1.2, 1.0))
                pos = cpu_spawn * (1 - eased) + target * eased
                m.move_to(pos)
                m.set_opacity(np.clip(1.5 * (1 - frac) + 0.15, 0.0, 1.0))
            return _upd

        for kk, (dot, meta) in enumerate(zip(cpu_packets, cpu_meta)):
            dot.add_updater(make_cpu_packet(meta, kk))
        self.add(cpu_packets)

        # --- GPU: a flood of packets rains into the grid in parallel ---------
        gpu_targets = [d.get_center() for d in gpu_dots]
        gpu_spawn_y = gpu_die.get_top()[1] - 0.1
        gpu_packets = VGroup()
        gpu_meta = []
        rng = np.random.default_rng(11)
        for k in range(48):
            dot = Dot(color=TEAL, radius=0.055)
            gpu_packets.add(dot)
            period = 1.4 + 0.6 * rng.random()
            offset = rng.uniform(0, period)
            target = np.array(gpu_targets[rng.integers(0, len(gpu_targets))])
            sx = float(rng.uniform(gpu_die.get_left()[0] + 0.5,
                                   gpu_die.get_right()[0] - 0.5))
            gpu_meta.append((period, offset, target, sx))

        def make_gpu_packet(meta):
            period, offset, target, sx = meta
            start = np.array([sx, gpu_spawn_y, 0])

            def _upd(m):
                tt = (t.get_value() + offset) % period
                frac = tt / period
                eased = rate_functions.ease_in_quad(min(frac * 1.1, 1.0))
                pos = start * (1 - eased) + target * eased
                m.move_to(pos)
                m.set_opacity(np.clip(1.4 * (1 - frac) + 0.1, 0.0, 1.0))
            return _upd

        for dot, meta in zip(gpu_packets, gpu_meta):
            dot.add_updater(make_gpu_packet(meta))
        self.add(gpu_packets)

        # --- Hierarchy caption on GPU side: cycles the chain -----------------
        chain = ["die", "GPC", "SM", "cores"]
        hier = Text("die", font=MONO, color=SILVER).scale(0.32)
        hier.next_to(gpu_die, DOWN, buff=0.12).align_to(gpu_die, LEFT)
        hier._idx = -1

        def hier_upd(m):
            idx = int(t.get_value() // 2.2) % len(chain)
            if idx != m._idx:
                m._idx = idx
                new = Text(" -> ".join(chain[:idx + 1]), font=MONO,
                           color=SILVER).scale(0.3)
                new.move_to(m.get_left(), aligned_edge=LEFT)
                m.become(new)
        hier.add_updater(hier_upd)
        self.add(hier)

        # Real GA102 counts, always on screen.
        counts = Text("10,752 shader  ·  336 tensor  ·  84 RT cores",
                      font=MONO, color=GREEN).scale(0.26)
        counts.next_to(hier, DOWN, buff=0.14).align_to(hier, LEFT)

        def counts_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 1.5)))
        counts.add_updater(counts_upd)
        self.add(counts)

        # Parallelism hint under title.
        hint = Text("one task at a time   vs   everything at once",
                    font=MONO, color=SECOND).scale(0.26)
        hint.next_to(title, DOWN, buff=0.12)
        self.add(hint)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
