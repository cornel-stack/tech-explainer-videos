"""Scene: the buying scorecard — how much RAM, and two takeaways.

Class `Buy` (~18s). Capacity tiers as labelled bars: "8 GB — tight",
"16 GB — most people" (GREEN, highlighted), "32 GB — heavy / creative",
"64 GB+ — empty desk for most" (SILVER). Two takeaways with checks: "run a
dual-channel PAIR" and "speed helps gaming + integrated graphics (a little)".
A highlight sweep crosses the tiers, the 16 GB bar pulses, checks blink.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromEdge,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    rate_functions,
    interpolate_color,
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


class Buy(Scene):
    def construct(self):
        title = Text("How much RAM should you buy?",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- capacity tiers as bars -----------------------------------------
        tiers = [
            ("8 GB", "tight", CORAL, 2.0),
            ("16 GB", "most people", GREEN, 3.6),
            ("32 GB", "heavy / creative", VIOLET, 5.0),
            ("64 GB+", "empty desk for most", SILVER, 6.2),
        ]
        rows = VGroup()
        bar_mobs = []
        top_y = 1.9
        step = 1.0
        left_x = -5.4
        for i, (cap, note, col, w) in enumerate(tiers):
            y = top_y - i * step
            bar = RoundedRectangle(
                corner_radius=0.08, width=w, height=0.66,
                stroke_color=col, stroke_width=2.5,
                fill_color=col, fill_opacity=0.18,
            )
            bar.move_to(np.array([left_x + w / 2, y, 0]))
            cap_txt = Text(cap, font=MONO, color=col,
                           weight="BOLD").scale(0.34)
            cap_txt.next_to(bar, LEFT, buff=0.0)
            cap_txt.move_to(np.array([left_x - 0.9, y, 0]))
            note_txt = Text(note, font=HEAD, color=col).scale(0.3)
            note_txt.next_to(bar, RIGHT, buff=0.25)
            g = VGroup(bar, cap_txt, note_txt)
            rows.add(g)
            bar_mobs.append((bar, col, y, w))

        self.play(*[GrowFromEdge(g[0], LEFT) for g in rows],
                  *[FadeIn(g[1]) for g in rows],
                  *[FadeIn(g[2]) for g in rows],
                  lag_ratio=0.12, run_time=1.4)

        # --- two takeaways with checks --------------------------------------
        check1 = Text("v", font=MONO, color=GREEN,
                      weight="BOLD").scale(0.4)
        take1 = Text("run a dual-channel PAIR", font=HEAD,
                     color=INK).scale(0.34)
        row1 = VGroup(check1, take1).arrange(RIGHT, buff=0.25)
        row1.move_to(np.array([-2.0, -2.5, 0]))

        check2 = Text("v", font=MONO, color=GREEN,
                      weight="BOLD").scale(0.4)
        take2 = Text("speed helps gaming + integrated graphics (a little)",
                     font=HEAD, color=INK).scale(0.34)
        row2 = VGroup(check2, take2).arrange(RIGHT, buff=0.25)
        row2.move_to(np.array([-0.8, -3.2, 0]))

        self.play(FadeIn(row1, shift=UP * 0.2),
                  FadeIn(row2, shift=UP * 0.2), run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        sweep_period = 4.0
        bar_base_x = -5.4

        # highlight sweep: a moving stroke-brightness across the tiers
        for idx, (bar, col, y, w) in enumerate(bar_mobs):
            bi = idx

            def make_sweep(bi, bar, col, y, w):
                is_hero = (bi == 1)  # 16 GB

                def _upd(m):
                    tt = t.get_value()
                    cur = int(tt // (sweep_period / 4)) % 4
                    base = 0.14
                    if cur == bi:
                        a = (tt % (sweep_period / 4)) / (sweep_period / 4)
                        glow = 0.14 + 0.35 * (0.5 + 0.5 * np.sin(a * np.pi))
                        m.set_fill(opacity=glow)
                        m.set_stroke(width=4.0)
                    else:
                        m.set_fill(opacity=base)
                        m.set_stroke(width=2.5)
                    if is_hero:
                        # 16 GB bar always pulses + widens slightly
                        pulse = 0.5 + 0.5 * np.sin(3.0 * tt)
                        extra = 0.18 * pulse
                        m.set(width=w + extra, height=0.66)
                        m.move_to(np.array([bar_base_x + (w + extra) / 2, y, 0]))
                        m.set_fill(opacity=max(m.fill_opacity, 0.22 + 0.2 * pulse))
                return _upd
            bar.add_updater(make_sweep(bi, bar, col, y, w))

        # checks blink
        for ci, chk in enumerate([check1, check2]):
            phase = ci * 1.3

            def make_blink(chk, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + phase)
                    m.set_opacity(0.4 + 0.6 * s)
                return _upd
            chk.add_updater(make_blink(chk, phase))

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
