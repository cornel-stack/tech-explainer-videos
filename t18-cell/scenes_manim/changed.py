"""Scene: what each mobile generation unlocked, as a CUMULATIVE STACK.

Class `Changed` (~18s). Starts with "1G: voice". Each generation adds a new
capability card on top of a growing stack ("+ text (2G)", "+ web (3G)", ...),
the stack visibly rising as each is added and every earlier card staying lit —
the point is accumulation. A highlight sweeps up the stack on a loop under the
caption "each G turns a luxury into an assumption".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    ValueTracker,
    ManimColor,
    config,
    interpolate_color,
    FadeIn,
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


class Changed(Scene):
    def construct(self):
        title = Text("Every generation turns a luxury into an assumption",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.5)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the cumulative capability cards ---------------------------------
        # (label, generation tag, colour)
        caps = [
            ("voice",              "1G", SILVER),
            ("+ text",             "2G", TEAL),
            ("+ web",              "3G", GREEN),
            ("+ streaming",        "4G", AMBER),
            ("+ IoT / low-latency", "5G", VIOLET),
            ("+ sensing / AI",     "6G", CORAL),
        ]
        n = len(caps)

        card_w = 5.6
        card_h = 0.72
        gap = 0.18
        base_y = -3.0  # bottom of the stack

        cards = []
        for i, (label, tag, col) in enumerate(caps):
            y = base_y + i * (card_h + gap)

            box = RoundedRectangle(
                corner_radius=0.1, width=card_w, height=card_h,
                stroke_color=col, stroke_width=2.5,
                fill_color=BG, fill_opacity=1.0,
            )
            # tint fill toward the card colour (via ManimColor blend)
            tint = interpolate_color(ManimColor(BG), ManimColor(col), 0.12)
            box.set_fill(tint, opacity=1.0)

            cap_lbl = Text(label, font=HEAD, color=INK,
                           weight="SEMIBOLD").scale(0.38)
            cap_lbl.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.3)

            tag_lbl = Text(tag, font=MONO, color=col, weight="BOLD").scale(0.34)
            tag_lbl.move_to(box.get_center()).align_to(box, RIGHT).shift(LEFT * 0.3)

            card = VGroup(box, cap_lbl, tag_lbl)
            card.move_to(np.array([0.0, y, 0]))
            card.set_opacity(0.0)  # start hidden; t drives the build-in
            cards.append(card)
            self.add(card)

        # running "stack height" meter on the left
        meter_lbl = Text("stack", font=MONO, color=SECOND).scale(0.26)
        meter_lbl.to_edge(LEFT, buff=0.6).shift(DOWN * 2.6)
        self.add(meter_lbl)

        # caption beneath the title
        caption = Text("each G turns a luxury into an assumption",
                       font=MONO, color=SECOND).scale(0.3)
        caption.next_to(title, DOWN, buff=0.14)
        self.add(caption)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # --- the stack builds: each card fades/rises in on its own beat ------
        build_start = 0.6     # first card appears
        build_step = 1.7      # seconds between successive cards

        def make_build(card, idx, col):
            target_y = base_y + idx * (card_h + gap)

            def _upd(m):
                tt = t.get_value()
                start = build_start + idx * build_step
                frac = np.clip((tt - start) / 0.9, 0.0, 1.0)
                eased = rate_functions.ease_out_back(frac) if frac < 1 else 1.0
                # rise up into place from slightly below
                y = target_y - (1 - eased) * 0.5
                card.move_to(np.array([0.0, y, 0]))
                card.set_opacity(np.clip(frac * 1.2, 0.0, 1.0))
            return _upd

        for i, card in enumerate(cards):
            card.add_updater(make_build(card, i, caps[i][2]))

        # --- stack-height meter grows with the count of lit cards ------------
        meter_bar = RoundedRectangle(
            corner_radius=0.04, width=0.16, height=0.1,
            stroke_width=0, fill_color=GOLD, fill_opacity=0.9,
        )
        meter_bar.move_to(meter_lbl.get_center() + UP * 0.35)
        meter_bar._shown_h = 0.1
        self.add(meter_bar)

        full_h = n * (card_h + gap)

        def meter_upd(m):
            tt = t.get_value()
            lit = 0
            for i in range(n):
                start = build_start + i * build_step
                if tt >= start + 0.6:
                    lit += 1
            frac = lit / n
            target_h = 0.1 + frac * (full_h - 0.1)
            new = RoundedRectangle(
                corner_radius=0.04, width=0.16, height=max(target_h, 0.1),
                stroke_width=0, fill_color=GOLD, fill_opacity=0.9,
            )
            new.move_to(np.array([m.get_center()[0],
                                  base_y - card_h / 2 + target_h / 2, 0]))
            m.become(new)
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(tt * 2.0)))
        meter_bar.add_updater(meter_upd)

        # --- highlight sweep rides up the stack on a loop --------------------
        sweep = RoundedRectangle(
            corner_radius=0.1, width=card_w + 0.18, height=card_h + 0.14,
            stroke_color=GOLD, stroke_width=4, fill_opacity=0.0,
        )
        sweep.set_opacity(0.0)
        self.add(sweep)

        sweep_period = 4.5
        full_build = build_start + (n - 1) * build_step + 1.2

        def sweep_upd(m):
            tt = t.get_value()
            # only start sweeping once the whole stack is built
            if tt < full_build:
                m.set_stroke(opacity=0.0)
                return
            local = (tt - full_build) % sweep_period
            frac = local / sweep_period
            seg = frac * n
            idx = int(np.clip(np.floor(seg), 0, n - 1))
            y = base_y + idx * (card_h + gap)
            m.move_to(np.array([0.0, y, 0]))
            # blend the sweep colour toward the card it sits on
            col = interpolate_color(ManimColor(GOLD),
                                    ManimColor(caps[idx][2]), 0.5)
            m.set_stroke(col)
            local_in = seg - idx
            glow = np.sin(local_in * np.pi)
            m.set_stroke(opacity=0.25 + 0.75 * glow)
        sweep.add_updater(sweep_upd)

        # lit cards keep a gentle breathing glow after they arrive
        for i, card in enumerate(cards):
            box = card[0]
            col = caps[i][2]

            def make_breath(b, idx, c):
                def _upd(m):
                    tt = t.get_value()
                    start = build_start + idx * build_step
                    if tt < start + 0.6:
                        return
                    b.set_stroke(width=2.5 + 1.2 *
                                 (0.5 + 0.5 * np.sin(2.2 * tt + idx * 0.8)))
                return _upd
            box.add_updater(make_breath(box, i, col))

        # caption breathes so it reads as a living line
        def caption_upd(m):
            m.set_opacity(0.55 + 0.4 * (0.5 + 0.5 *
                                        np.sin(t.get_value() * 1.5)))
        caption.add_updater(caption_upd)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
