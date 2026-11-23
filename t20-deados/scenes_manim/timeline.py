"""Scene: The Graveyard Timeline — a horizontal memorial of dead operating systems.

Class `Timeline` (~20s). A horizontal time axis from 1974 to 2017. For each dead
OS a small rounded-top headstone sits on the axis at its death year, with its
name in small MONO text and a faint "born -> died" range bar showing how long it
lived. A soft candlelight sweep moves left -> right; as it passes each OS, that
headstone lights up VIOLET then dims back to grey ("it has passed"). The sweep
loops, headstones gently pulse. Kept legible so it can also sit faintly behind
the intro title.

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
    Rectangle,
    Line,
    Text,
    VGroup,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    interpolate_color,
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


class Timeline(Scene):
    def construct(self):
        YEAR_MIN, YEAR_MAX = 1974, 2017

        # --- geometry: time axis across the screen ---------------------------
        X_LEFT, X_RIGHT = -6.2, 6.2
        AXIS_Y = -2.1

        def x_of(year):
            frac = (year - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)
            return X_LEFT + frac * (X_RIGHT - X_LEFT)

        # --- title -----------------------------------------------------------
        title = Text("THE GRAVEYARD  ·  1974–2017", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- ground / axis line ----------------------------------------------
        axis = Line([X_LEFT, AXIS_Y, 0], [X_RIGHT, AXIS_Y, 0],
                    stroke_color=SECOND, stroke_width=2.0, stroke_opacity=0.6)
        self.play(Create(axis), run_time=0.6)

        # --- year ticks ------------------------------------------------------
        ticks = VGroup()
        for yr in (1974, 1985, 1995, 2005, 2017):
            tk = Line([x_of(yr), AXIS_Y - 0.08, 0], [x_of(yr), AXIS_Y + 0.08, 0],
                      stroke_color=SECOND, stroke_width=1.5, stroke_opacity=0.5)
            lab = Text(str(yr), font=MONO, color=SECOND).scale(0.24)
            lab.next_to(tk, DOWN, buff=0.1)
            lab.set_opacity(0.6)
            ticks.add(VGroup(tk, lab))
        self.play(*[FadeIn(t) for t in ticks], run_time=0.5)

        # --- dead OSes: (name, born, died) sorted by death year --------------
        oses = [
            ("CP/M", 1974, 1983),
            ("MS-DOS", 1981, 2000),
            ("Classic Mac OS", 1984, 2001),
            ("OS/2", 1987, 2006),
            ("BeOS", 1995, 2001),
            ("Palm OS", 1996, 2009),
            ("Symbian", 1998, 2012),
            ("BlackBerry OS", 1999, 2013),
            ("webOS", 2009, 2012),
            ("Windows Phone", 2010, 2017),
        ]

        # Alternate headstone heights across two tiers so names don't collide.
        tiers = [1.35, 2.0]

        GREY = ManimColor(SILVER)
        LIT = ManimColor(VIOLET)

        headstones = []   # dicts of captured locals for updaters
        stone_group = VGroup()

        for i, (name, born, died) in enumerate(oses):
            dx = x_of(died)
            bx = x_of(born)
            tier = tiers[i % 2]
            top_y = AXIS_Y + tier

            # Faint lifespan bar from birth to death, just above the axis.
            bar_y = AXIS_Y + 0.14 + (0.0 if i % 2 == 0 else 0.26)
            life_bar = Line([bx, bar_y, 0], [dx, bar_y, 0],
                            stroke_color=SILVER, stroke_width=2.0,
                            stroke_opacity=0.18)

            # Headstone: a rounded-top rectangle. Approximate with a rounded
            # rectangle whose bottom corners are nearly square by keeping the
            # radius modest and letting it sit on the axis.
            stone_w = 0.95
            stone_h = tier
            stone = RoundedRectangle(
                corner_radius=0.42, width=stone_w, height=stone_h,
                stroke_color=SILVER, stroke_width=2.0, stroke_opacity=0.45,
                fill_color="#15151A", fill_opacity=0.9,
            )
            stone.move_to([dx, AXIS_Y + stone_h / 2.0, 0])

            # Square off the bottom so it reads as a tombstone planted in ground.
            foot = Rectangle(
                width=stone_w, height=stone_h * 0.45,
                stroke_width=0, fill_color="#15151A", fill_opacity=0.9,
            )
            foot.move_to([dx, AXIS_Y + stone_h * 0.225, 0])

            # Name in small MONO, stacked near the top of the stone.
            disp = name if len(name) <= 7 else name.replace(" ", "\n")
            label = Text(disp, font=MONO, color=SILVER,
                         line_spacing=0.7).scale(0.18)
            label.move_to([dx, top_y - 0.28, 0])

            # A faint inner glow outline that lights up when the sweep passes.
            glow = RoundedRectangle(
                corner_radius=0.42, width=stone_w, height=stone_h,
                stroke_color=VIOLET, stroke_width=7, stroke_opacity=0.0,
                fill_opacity=0.0,
            ).move_to(stone)

            # Death-year tag under the axis at the stone.
            yr_tag = Text(str(died), font=MONO, color=SECOND).scale(0.17)
            yr_tag.next_to([dx, AXIS_Y, 0], DOWN, buff=0.04)
            yr_tag.set_opacity(0.0)

            g = VGroup(life_bar, foot, stone, glow, label, yr_tag)
            stone_group.add(g)

            headstones.append({
                "stone": stone,
                "glow": glow,
                "label": label,
                "yr_tag": yr_tag,
                "life_bar": life_bar,
                "dx": dx,
            })

        self.play(*[GrowFromCenter(g) for g in stone_group],
                  lag_ratio=0.06, run_time=1.4)

        # --- subcaption ------------------------------------------------------
        sub = Text("ten operating systems, laid to rest", font=HEAD,
                   color=SECOND).scale(0.32)
        sub.next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        SWEEP_PERIOD = 9.0  # seconds for the candlelight to cross once

        def sweep_x(tt):
            frac = (tt % SWEEP_PERIOD) / SWEEP_PERIOD
            return X_LEFT + frac * (X_RIGHT - X_LEFT)

        # --- candlelight sweep: a soft vertical bar of light -----------------
        candle = Line([0, AXIS_Y - 0.5, 0], [0, AXIS_Y + 2.6, 0],
                      stroke_color=GOLD, stroke_width=10, stroke_opacity=0.0)

        def candle_upd(m):
            cx = sweep_x(t.get_value())
            m.put_start_and_end_on([cx, AXIS_Y - 0.5, 0],
                                   [cx, AXIS_Y + 2.6, 0])
            # Soft flicker.
            flick = 0.22 + 0.1 * np.sin(t.get_value() * 9.0)
            m.set_stroke(opacity=flick)
        candle.add_updater(candle_upd)
        self.add(candle)

        # A faint pool of light at the candle's foot on the axis.
        pool = Line([0, AXIS_Y, 0], [0.01, AXIS_Y, 0],
                    stroke_color=GOLD, stroke_width=3, stroke_opacity=0.0)

        def pool_upd(m):
            cx = sweep_x(t.get_value())
            m.put_start_and_end_on([cx - 1.1, AXIS_Y, 0],
                                   [cx + 1.1, AXIS_Y, 0])
            m.set_stroke(opacity=0.12 + 0.05 * np.sin(t.get_value() * 7.0))
        pool.add_updater(pool_upd)
        self.add(pool)

        # --- per-headstone lighting + gentle pulse ---------------------------
        X_SPAN = X_RIGHT - X_LEFT

        for i, h in enumerate(headstones):
            stone = h["stone"]
            glow = h["glow"]
            label = h["label"]
            yr_tag = h["yr_tag"]
            life_bar = h["life_bar"]
            dx = h["dx"]
            phase = i * 0.7

            def make_upd(stone, glow, label, yr_tag, life_bar, dx, phase):
                def _upd(m):
                    tt = t.get_value()
                    cx = sweep_x(tt)
                    # Proximity of the sweep to this stone (0..1, 1 = on top).
                    d = abs(cx - dx)
                    prox = np.clip(1.0 - d / (0.09 * X_SPAN), 0.0, 1.0)
                    prox = prox * prox  # sharpen the halo

                    # Gentle baseline pulse so grey stones still breathe.
                    pulse = 0.5 + 0.5 * np.sin(1.3 * tt + phase)

                    # Stone stroke: grey -> violet as the light passes.
                    col = interpolate_color(GREY, LIT, prox)
                    stone.set_stroke(color=col,
                                     opacity=0.4 + 0.5 * prox + 0.08 * pulse)
                    glow.set_stroke(color=LIT, opacity=0.55 * prox)
                    label.set_color(interpolate_color(GREY, ManimColor(INK),
                                                      prox))
                    label.set_opacity(0.7 + 0.3 * prox)
                    yr_tag.set_opacity(0.2 + 0.8 * prox)
                    life_bar.set_stroke(
                        color=interpolate_color(ManimColor(SILVER), LIT, prox),
                        opacity=0.15 + 0.4 * prox,
                    )
                return _upd

            stone.add_updater(
                make_upd(stone, glow, label, yr_tag, life_bar, dx, phase))

        # --- footer caption cycling the mood --------------------------------
        lines = [
            "gone, but not forgotten",
            "each one shipped to millions",
            "every empire ends",
        ]
        footer = Text(lines[0], font=MONO, color=SECOND).scale(0.28)
        footer.to_edge(DOWN, buff=0.22)
        footer._idx = -1

        def footer_upd(m):
            idx = int(t.get_value() // 4.0) % len(lines)
            if idx != m._idx:
                m._idx = idx
                new = Text(lines[idx], font=MONO, color=SECOND).scale(0.28)
                new.to_edge(DOWN, buff=0.22)
                m.become(new)
            m.set_opacity(0.4 + 0.3 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 1.4)))
        footer.add_updater(footer_upd)
        self.add(footer)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
