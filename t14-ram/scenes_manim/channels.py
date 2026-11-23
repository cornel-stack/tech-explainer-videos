"""Scene: single vs dual channel — same capacity, twice the highway.

Class `Channels` (~18s). Top: one RAM stick -> ONE lane -> CPU, data
trickling slowly. Bottom: a MATCHED PAIR of sticks -> TWO lanes -> CPU, data
flowing at ~2x the rate. Labels "1x16 GB — one lane" vs "2x8 GB — two lanes,
2x bandwidth". Caption "same capacity, twice the highway — buy in matched
pairs".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Line,
    Text,
    VGroup,
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


def ram_stick(width, color, label):
    body = RoundedRectangle(
        corner_radius=0.06, width=width, height=0.9,
        stroke_color=color, stroke_width=2.5,
        fill_color=BG, fill_opacity=0.6,
    )
    # chips on the stick
    chips = VGroup()
    n = 4
    for i in range(n):
        chip = Rectangle(
            width=width / (n + 1.5), height=0.4, stroke_width=0,
            fill_color=color, fill_opacity=0.35,
        )
        chips.add(chip)
    chips.arrange(RIGHT, buff=width / (n * 3))
    chips.move_to(body.get_center())
    lbl = Text(label, font=MONO, color=color).scale(0.24)
    lbl.next_to(body, UP, buff=0.12)
    return VGroup(body, chips, lbl)


class Channels(Scene):
    def construct(self):
        title = Text("Single vs dual channel — same GB, more lanes",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- CPU boxes (right) ----------------------------------------------
        def cpu_box(y):
            box = RoundedRectangle(
                corner_radius=0.1, width=1.5, height=1.3,
                stroke_color=INK, stroke_width=2.5,
                fill_color="#141418", fill_opacity=0.8,
            )
            box.move_to(np.array([4.6, y, 0]))
            lbl = Text("CPU", font=MONO, color=INK,
                       weight="BOLD").scale(0.3)
            lbl.move_to(box.get_center())
            return VGroup(box, lbl)

        top_y = 1.6
        bot_y = -1.8

        cpu_top = cpu_box(top_y)
        cpu_bot = cpu_box(bot_y)

        # --- single channel (top) -------------------------------------------
        stick1 = ram_stick(2.2, SILVER, "1x16 GB")
        stick1.move_to(np.array([-4.4, top_y, 0]))
        lane_top = Rectangle(
            width=5.2, height=0.3, stroke_width=0,
            fill_color="#141418", fill_opacity=1.0,
        ).move_to(np.array([0.0, top_y, 0]))
        one_lane_lbl = Text("one lane", font=MONO, color=SECOND).scale(0.26)
        one_lane_lbl.next_to(lane_top, DOWN, buff=0.1)

        # --- dual channel (bottom) ------------------------------------------
        stickA = ram_stick(2.0, GREEN, "2x8 GB")
        stickB = ram_stick(2.0, GREEN, "")
        pair = VGroup(stickA, stickB).arrange(DOWN, buff=0.25)
        pair.move_to(np.array([-4.4, bot_y, 0]))
        lane_bot1 = Rectangle(
            width=5.2, height=0.28, stroke_width=0,
            fill_color="#141418", fill_opacity=1.0,
        ).move_to(np.array([0.0, bot_y + 0.3, 0]))
        lane_bot2 = Rectangle(
            width=5.2, height=0.28, stroke_width=0,
            fill_color="#141418", fill_opacity=1.0,
        ).move_to(np.array([0.0, bot_y - 0.3, 0]))
        two_lane_lbl = Text("two lanes, 2x bandwidth", font=MONO,
                            color=GREEN).scale(0.26)
        two_lane_lbl.next_to(lane_bot2, DOWN, buff=0.1)

        self.play(FadeIn(stick1), FadeIn(pair),
                  Create(lane_top), Create(lane_bot1), Create(lane_bot2),
                  FadeIn(cpu_top), FadeIn(cpu_bot),
                  FadeIn(one_lane_lbl), FadeIn(two_lane_lbl),
                  run_time=1.2)

        caption = Text(
            "same capacity, twice the highway — buy in matched pairs",
            font=MONO, color=SECOND).scale(0.3)
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        lane_left = -2.6
        lane_right = 2.6
        span = lane_right - lane_left

        # --- single channel: slow trickle (few packets, slow speed) ----------
        top_pkts = VGroup()
        top_meta = []
        rng = np.random.default_rng(3)
        for k in range(3):
            dot = Dot(color=SILVER, radius=0.08)
            top_pkts.add(dot)
            speed = 1.3
            offset = rng.uniform(0, span)
            top_meta.append((speed, offset))

        def make_top(speed, offset):
            def _upd(m):
                x = lane_left + ((t.get_value() * speed + offset) % span)
                m.move_to(np.array([x, top_y, 0]))
            return _upd
        for dot, (speed, offset) in zip(top_pkts, top_meta):
            dot.add_updater(make_top(speed, offset))
        self.add(top_pkts)

        # --- dual channel: ~2x throughput (two lanes, faster + denser) -------
        bot_pkts = VGroup()
        bot_meta = []
        for lane_i, ly in enumerate([bot_y + 0.3, bot_y - 0.3]):
            for k in range(4):
                dot = Dot(color=GREEN, radius=0.08)
                bot_pkts.add(dot)
                speed = 2.6
                offset = rng.uniform(0, span)
                bot_meta.append((ly, speed, offset))

        def make_bot(ly, speed, offset):
            def _upd(m):
                x = lane_left + ((t.get_value() * speed + offset) % span)
                m.move_to(np.array([x, ly, 0]))
            return _upd
        for dot, (ly, speed, offset) in zip(bot_pkts, bot_meta):
            dot.add_updater(make_bot(ly, speed, offset))
        self.add(bot_pkts)

        # throughput counters
        top_count = Text("~1x", font=MONO, color=SILVER).scale(0.34)
        top_count.next_to(cpu_top, RIGHT, buff=0.25)
        bot_count = Text("~2x", font=MONO, color=GREEN).scale(0.34)
        bot_count.next_to(cpu_bot, RIGHT, buff=0.25)

        def bot_pulse(m):
            m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 *
                                       np.sin(3 * t.get_value())))
        bot_count.add_updater(bot_pulse)
        self.add(top_count, bot_count)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
