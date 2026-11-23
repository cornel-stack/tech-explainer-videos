"""Scene 3: every tick, the CPU steps forward once.

Class `Clock` (~18s). A clock/metronome ticking; a square-wave clock signal
pulsing; on each rising edge the whole CPU (a block) advances one step. Shows
"3 GHz = 3,000,000,000 ticks/sec" counting. Caption: "every tick, the CPU
steps forward once".

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


class Clock(Scene):
    def construct(self):
        title = Text("The clock sets the pace", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- metronome / clock face on the left -----------------------------
        clk_c = np.array([-4.3, 0.6, 0.0])
        face = Circle(radius=0.95, stroke_color=AMBER, stroke_width=3,
                      fill_color="#111318", fill_opacity=0.9).move_to(clk_c)
        pivot = Dot(clk_c, color=AMBER, radius=0.06)
        hand = Line(clk_c, clk_c + UP * 0.8, stroke_color=AMBER,
                    stroke_width=4)
        clk_lbl = Text("clock", font=MONO, color=AMBER).scale(0.32)
        clk_lbl.next_to(face, DOWN, buff=0.2)
        self.play(Create(face), FadeIn(pivot), Create(hand), FadeIn(clk_lbl),
                  run_time=0.9)

        # --- square wave clock signal (centre-top) --------------------------
        wave_lbl = Text("clock signal", font=MONO, color=AMBER).scale(0.28)
        wave_lbl.move_to([0.6, 2.2, 0])
        wx0, wx1 = -1.8, 3.2
        wy = 1.4
        wave = Line([wx0, wy, 0], [wx1, wy, 0], stroke_color=AMBER,
                    stroke_width=3)
        axis = Line([wx0 - 0.1, wy - 0.55, 0], [wx1 + 0.1, wy - 0.55, 0],
                    stroke_color=SECOND, stroke_width=1, stroke_opacity=0.3)
        self.play(Create(wave), Create(axis), FadeIn(wave_lbl), run_time=0.7)

        # --- the CPU block that advances one step per rising edge -----------
        cpu_box = RoundedRectangle(corner_radius=0.14, width=2.3, height=1.4,
                                   stroke_color=INK, stroke_width=2.5,
                                   fill_color="#111318", fill_opacity=0.9)
        cpu_box.move_to([1.0, -1.4, 0])
        cpu_lbl = Text("CPU", font=MONO, color=INK).scale(0.4)
        cpu_lbl.move_to(cpu_box.get_center() + UP * 0.35)
        step_lbl = Text("step 0", font=MONO, color=GREEN).scale(0.42)
        step_lbl.move_to(cpu_box.get_center() + DOWN * 0.2)
        self.play(Create(cpu_box), FadeIn(cpu_lbl), FadeIn(step_lbl),
                  run_time=0.8)

        # --- GHz counter ----------------------------------------------------
        ghz_lbl = Text("3 GHz =", font=MONO, color=SECOND).scale(0.34)
        ghz_lbl.move_to([4.4, 0.6, 0])
        ticks_txt = Text("0", font=MONO, color=TEAL).scale(0.44)
        ticks_txt.move_to([4.4, 0.05, 0])
        ticks_sub = Text("ticks/sec", font=MONO, color=SECOND).scale(0.26)
        ticks_sub.move_to([4.4, -0.4, 0])
        self.play(FadeIn(ghz_lbl), FadeIn(ticks_txt), FadeIn(ticks_sub),
                  run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        TICK_RATE = 1.6  # visual ticks per second

        def phase(tt):
            return TICK_RATE * tt

        def tick_count(tt):
            return int(np.floor(phase(tt)))

        # metronome hand swings; clicks at each half-swing
        def hand_upd(m):
            ang = 0.55 * np.sin(np.pi * phase(t.get_value()))
            end = clk_c + np.array([np.sin(ang) * 0.8,
                                    np.cos(ang) * 0.8, 0.0])
            m.put_start_and_end_on(clk_c, end)
        hand.add_updater(hand_upd)

        # clock face glows on each rising edge
        c_dim = ManimColor("#3A2A08")
        c_hot = ManimColor(AMBER)

        def face_upd(m):
            frac = phase(t.get_value()) % 1.0
            glow = max(0.0, 1.0 - frac * 4.0)
            m.set_stroke(interpolate_color(c_dim, c_hot, 0.4 + 0.6 * glow),
                         width=3 + 2 * glow)
        face.add_updater(face_upd)

        # square-wave clock signal scrolling under the hand
        def wave_upd(m):
            pts = []
            steps = 120
            ph = phase(t.get_value())
            for k in range(steps + 1):
                fx = k / steps
                x = wx0 + (wx1 - wx0) * fx
                # cycles over the visible window, scrolling with time
                cyc = (fx * 6.0 - ph) % 1.0
                high = cyc < 0.5
                y = wy + (0.45 if high else -0.45)
                pts.append([x, y, 0])
            # build a proper square shape with vertical edges
            sq = []
            prev_y = None
            for p in pts:
                if prev_y is not None and abs(p[1] - prev_y) > 1e-6:
                    sq.append([p[0], prev_y, 0])
                sq.append(p)
                prev_y = p[1]
            m.set_points_as_corners(sq)
        wave.add_updater(wave_upd)

        # a marker dot riding the rising edges
        edge_dot = Dot([wx0, wy + 0.45, 0], color=GREEN, radius=0.08)

        def edge_upd(m):
            ph = phase(t.get_value())
            frac = ph % 1.0
            # position of current rising edge sweeping across
            x = wx0 + (wx1 - wx0) * (frac)
            m.move_to([x, wy + 0.45, 0])
            flash = max(0.0, 1.0 - frac * 6.0)
            m.set_opacity(0.3 + 0.7 * flash)
        edge_dot.add_updater(edge_upd)
        self.add(edge_dot)

        # CPU step counter advances once per tick; box flashes on each tick
        def step_upd(m):
            n = tick_count(t.get_value())
            new = Text(f"step {n}", font=MONO, color=GREEN).scale(0.42)
            new.move_to(cpu_box.get_center() + DOWN * 0.2)
            m.become(new)
        step_lbl.add_updater(step_upd)

        c_cpu_dim = ManimColor("#2A2A30")
        c_cpu_hot = ManimColor(GREEN)

        def cpu_upd(m):
            frac = phase(t.get_value()) % 1.0
            flash = max(0.0, 1.0 - frac * 4.0)
            m.set_stroke(interpolate_color(c_cpu_dim, c_cpu_hot, flash),
                         width=2.5 + 2.0 * flash)
        cpu_box.add_updater(cpu_upd)

        # GHz counter ramps up toward 3,000,000,000
        def ticks_upd(m):
            frac = min(1.0, t.get_value() / 10.0)
            val = int(frac * 3_000_000_000)
            new = Text(f"{val:,}", font=MONO, color=TEAL).scale(0.44)
            new.move_to([4.4, 0.05, 0])
            m.become(new)
        ticks_txt.add_updater(ticks_upd)

        def ghz_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.0 * t.get_value())))
        ghz_lbl.add_updater(ghz_upd)

        # caption
        cap = Text("every tick, the CPU steps forward once",
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
