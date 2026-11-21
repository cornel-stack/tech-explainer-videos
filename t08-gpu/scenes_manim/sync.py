"""Scene: display sync — tearing, VSync, and adaptive sync.

Class `Sync` (~18s). Two horizontal lanes with tick marks moving leftward
continuously: top lane "GPU frames ready" (teal ticks, uneven cadence),
bottom lane "monitor refresh" (silver ticks, fixed cadence). A coral "TEAR"
flash appears when a GPU tick lands misaligned with a refresh tick. Two
labelled outcomes cycle: "VSync — GPU waits (adds lag)" and
"G-Sync / FreeSync — monitor adapts (no tear)". Continuous tick motion via a
master ValueTracker. No freeze.

Dark palette only, TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  red #FF5C47  teal #2DD4BF  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Text,
    VGroup,
    Line,
    ValueTracker,
    config,
    FadeIn,
    Create,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    rate_functions,
)

BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#76D64A"
RED = "#FF5C47"
TEAL = "#2DD4BF"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Sync(Scene):
    def construct(self):
        title = Text("Display sync & screen tearing", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        LANE_L = -6.0
        LANE_R = 6.0
        top_y = 1.4
        bot_y = -0.9

        top_lane = Line([LANE_L, top_y, 0], [LANE_R, top_y, 0],
                        stroke_color=SECOND, stroke_width=2)
        bot_lane = Line([LANE_L, bot_y, 0], [LANE_R, bot_y, 0],
                        stroke_color=SECOND, stroke_width=2)
        top_lbl = Text("GPU frames ready", font=MONO, color=TEAL).scale(0.3)
        top_lbl.next_to(top_lane, UP, buff=0.12).align_to(top_lane, LEFT)
        bot_lbl = Text("monitor refresh", font=MONO, color=SILVER).scale(0.3)
        bot_lbl.next_to(bot_lane, DOWN, buff=0.12).align_to(bot_lane, LEFT)

        self.play(Create(top_lane), Create(bot_lane),
                  FadeIn(top_lbl), FadeIn(bot_lbl), run_time=0.7)

        # --- Ticks -----------------------------------------------------------
        SPAN = LANE_R - LANE_L
        TICK_H = 0.55

        # GPU ticks: uneven cadence (phase list), teal.
        gpu_phases = [0.0, 1.3, 1.9, 3.4, 4.0, 5.3, 6.1, 7.2]
        gpu_ticks = VGroup()
        for ph in gpu_phases:
            tk = Line([0, top_y - TICK_H / 2, 0], [0, top_y + TICK_H / 2, 0],
                      stroke_color=TEAL, stroke_width=4)
            tk.base_ph = ph
            gpu_ticks.add(tk)

        # Monitor ticks: fixed cadence (even spacing), silver.
        mon_ticks = VGroup()
        mon_phases = [i * 1.6 for i in range(8)]
        for ph in mon_phases:
            tk = Line([0, bot_y - TICK_H / 2, 0], [0, bot_y + TICK_H / 2, 0],
                      stroke_color=SILVER, stroke_width=4)
            tk.base_ph = ph
            mon_ticks.add(tk)

        self.add(gpu_ticks, mon_ticks)

        # TEAR flash marker.
        tear = Text("TEAR", font=MONO, color=RED, weight="BOLD").scale(0.4)
        tear.move_to([0, (top_y + bot_y) / 2, 0]).set_opacity(0)
        self.add(tear)

        # Outcome label that cycles.
        outcome = Text("VSync — GPU waits (adds lag)", font=HEAD,
                       color=TEAL).scale(0.36)
        outcome.to_edge(DOWN, buff=0.5)
        outcome._idx = -1
        self.add(outcome)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        SPEED = 1.5

        def wrap_x(start_x, tt):
            x = start_x - SPEED * tt
            return LANE_L + ((x - LANE_L) % SPAN)

        # GPU ticks scroll (uneven spacing preserved).
        for tk in gpu_ticks:
            def make_gpu(ticko):
                start_x = LANE_R - ticko.base_ph * 1.5

                def _upd(m):
                    x = wrap_x(start_x, t.get_value())
                    m.put_start_and_end_on([x, top_y - TICK_H / 2, 0],
                                           [x, top_y + TICK_H / 2, 0])
                    edge = min(x - LANE_L, LANE_R - x) / 1.5
                    m.set_opacity(np.clip(edge, 0.0, 1.0))
                return _upd
            tk.add_updater(make_gpu(tk))

        # Monitor ticks scroll (fixed spacing).
        for tk in mon_ticks:
            def make_mon(ticko):
                start_x = LANE_R - ticko.base_ph * 1.5

                def _upd(m):
                    x = wrap_x(start_x, t.get_value())
                    m.put_start_and_end_on([x, bot_y - TICK_H / 2, 0],
                                           [x, bot_y + TICK_H / 2, 0])
                    edge = min(x - LANE_L, LANE_R - x) / 1.5
                    m.set_opacity(np.clip(edge, 0.0, 1.0))
                return _upd
            tk.add_updater(make_mon(tk))

        # TEAR flashes when a GPU tick is near center but a monitor tick is
        # NOT aligned there (misalignment at the scan line).
        def tear_upd(m):
            tt = t.get_value()
            center = (LANE_L + LANE_R) / 2
            gpu_x = [wrap_x(LANE_R - tk.base_ph * 1.5, tt) for tk in gpu_ticks]
            mon_x = [wrap_x(LANE_R - tk.base_ph * 1.5, tt) for tk in mon_ticks]
            gpu_near = min(abs(x - center) for x in gpu_x)
            mon_near = min(abs(x - center) for x in mon_x)
            # Misaligned: a GPU tick at center while no monitor tick is there.
            mis = (gpu_near < 0.25) and (mon_near > 0.9)
            if mis:
                m.set_opacity(0.85 + 0.15 * np.sin(tt * 25))
                m.move_to([center, (top_y + bot_y) / 2, 0])
            else:
                m.set_opacity(0.0)
        tear.add_updater(tear_upd)

        # Outcome label cycles between the two fixes.
        outcomes = [("VSync — GPU waits (adds lag)", TEAL),
                    ("G-Sync / FreeSync — monitor adapts (no tear)", GREEN)]

        def outcome_upd(m):
            idx = int(t.get_value() // 4.0) % len(outcomes)
            if idx != m._idx:
                m._idx = idx
                txt, col = outcomes[idx]
                new = Text(txt, font=HEAD, color=col).scale(0.36)
                new.to_edge(DOWN, buff=0.5)
                m.become(new)
        outcome.add_updater(outcome_upd)

        self.play(t.animate.set_value(14.0), run_time=14.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
