"""Scene: the memory hierarchy — a ladder of tiers, fast+small on top,
slow+big on the bottom, with RAM highlighted as the fast workspace that
bridges the CPU<->storage speed gap.

Class `Hierarchy` (~20s). A stacked pyramid of tiers: Registers, L1/L2/L3
cache, RAM, SSD, HDD. Axis labels "faster ^" and "bigger v". The RAM tier
glows GREEN and carries a "volatile" tag. Packets travel CPU->RAM fast and
RAM->SSD slow, showing the gap RAM bridges.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
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


class Hierarchy(Scene):
    def construct(self):
        title = Text("The memory hierarchy — RAM bridges the speed gap",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the tiers: top = fast+small, bottom = slow+big ------------------
        tiers = [
            ("Registers", GOLD, 2.0),
            ("L1 / L2 / L3 cache", TEAL, 3.2),
            ("RAM", GREEN, 4.6),
            ("SSD", VIOLET, 6.0),
            ("HDD", SILVER, 7.4),
        ]
        rows = VGroup()
        ram_row = None
        ram_glow = None
        tier_y = {}
        top_y = 2.4
        step = 1.05
        for i, (name, col, w) in enumerate(tiers):
            y = top_y - i * step
            tier_y[name] = y
            glow = RoundedRectangle(
                corner_radius=0.1, width=w + 0.3, height=0.9,
                stroke_color=col, stroke_width=10, stroke_opacity=0.0,
                fill_opacity=0,
            ).move_to(np.array([0.0, y, 0]))
            bar = RoundedRectangle(
                corner_radius=0.1, width=w, height=0.78,
                stroke_color=col, stroke_width=2.5,
                fill_color=BG, fill_opacity=0.85,
            ).move_to(np.array([0.0, y, 0]))
            lbl = Text(name, font=MONO, color=col, weight="BOLD").scale(0.34)
            lbl.move_to(bar.get_center())
            g = VGroup(glow, bar, lbl)
            rows.add(g)
            if name == "RAM":
                ram_row = bar
                ram_glow = glow

        self.play(*[GrowFromCenter(g) for g in rows],
                  lag_ratio=0.12, run_time=1.4)

        # --- axis labels -----------------------------------------------------
        faster = Text("faster  ^", font=MONO, color=INK).scale(0.3)
        faster.move_to(np.array([-4.6, top_y, 0]))
        bigger = Text("bigger  v", font=MONO, color=SECOND).scale(0.3)
        bigger.move_to(np.array([4.6, top_y - 4 * step, 0]))
        self.play(FadeIn(faster, shift=UP * 0.2),
                  FadeIn(bigger, shift=DOWN * 0.2), run_time=0.5)

        # --- RAM tags --------------------------------------------------------
        work_tag = Text("the fast workspace", font=HEAD,
                        color=GREEN).scale(0.3)
        work_tag.next_to(ram_row, RIGHT, buff=0.3)
        vol_tag = Text("volatile — power off clears it", font=MONO,
                       color=SECOND).scale(0.26)
        vol_tag.next_to(ram_row, LEFT, buff=0.3)
        self.play(FadeIn(work_tag), FadeIn(vol_tag), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # RAM glow pulses.
        glow_mob = ram_glow

        def ram_pulse(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            m.set_stroke(opacity=0.15 + 0.5 * s)
        glow_mob.add_updater(ram_pulse)

        ram_bar = ram_row

        def ram_fill(m):
            s = 0.5 + 0.5 * np.sin(2.2 * t.get_value())
            m.set_fill(color=interpolate_color(
                ManimColor(BG), ManimColor(GREEN), 0.08 + 0.12 * s))
        ram_bar.add_updater(ram_fill)

        # --- fast packet CPU -> RAM (short hop, quick) -----------------------
        cpu_y = tier_y["Registers"]
        ram_yv = tier_y["RAM"]
        ssd_y = tier_y["SSD"]
        fast_from = np.array([-2.6, cpu_y, 0])
        fast_to = np.array([-2.0, ram_yv, 0])

        fast_pkt = Dot(color=GREEN, radius=0.09)

        def fast_upd(m):
            period = 1.0
            frac = (t.get_value() % period) / period
            eased = rate_functions.ease_in_out_quad(frac)
            pos = fast_from * (1 - eased) + fast_to * eased
            m.move_to(pos)
            m.set_opacity(np.clip(1.4 * (1 - frac) + 0.2, 0, 1))
        fast_pkt.add_updater(fast_upd)
        self.add(fast_pkt)

        fast_lbl = Text("CPU->RAM: fast", font=MONO, color=GREEN).scale(0.24)
        fast_lbl.move_to(np.array([-3.4, (cpu_y + ram_yv) / 2, 0]))
        self.add(fast_lbl)

        # --- slow packet RAM -> SSD (long hop, slow) -------------------------
        slow_from = np.array([1.8, ram_yv, 0])
        slow_to = np.array([2.2, ssd_y, 0])

        slow_pkt = Dot(color=VIOLET, radius=0.09)

        def slow_upd(m):
            period = 3.4
            frac = (t.get_value() % period) / period
            eased = rate_functions.ease_in_out_quad(min(frac * 1.1, 1.0))
            pos = slow_from * (1 - eased) + slow_to * eased
            m.move_to(pos)
            m.set_opacity(np.clip(1.4 * (1 - frac) + 0.2, 0, 1))
        slow_pkt.add_updater(slow_upd)
        self.add(slow_pkt)

        slow_lbl = Text("RAM->SSD: slow", font=MONO, color=VIOLET).scale(0.24)
        slow_lbl.move_to(np.array([3.5, (ram_yv + ssd_y) / 2, 0]))
        self.add(slow_lbl)

        # work tag breathes
        wt = work_tag

        def wt_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                                       np.sin(2.2 * t.get_value())))
        wt.add_updater(wt_upd)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
