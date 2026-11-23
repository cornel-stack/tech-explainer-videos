"""Scene: The compiled <-> interpreted spectrum.

Class `Spectrum` (~18s). A horizontal axis runs from COMPILED (left, AMBER,
"close to the metal") to INTERPRETED (right, GREEN, "human-friendly"), with a
FAST <-> EASY sub-label. Language name-tags sit along the axis at sensible
positions. A scanning highlight sweeps left->right, lighting each tag in its
own colour as it passes; a caption cycles through three philosophy lines on a
continuous loop; tags bob gently.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Text,
    VGroup,
    Line,
    Dot,
    Triangle,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    UP,
    DOWN,
    LEFT,
    RIGHT,
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


class Spectrum(Scene):
    def construct(self):
        # --- axis geometry ---------------------------------------------------
        X_LEFT = -5.6
        X_RIGHT = 5.6
        AXIS_Y = -0.2

        def x_at(frac):
            return X_LEFT + (X_RIGHT - X_LEFT) * frac

        # --- title -----------------------------------------------------------
        title = Text("THE SPECTRUM", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.62)
        title.to_edge(UP, buff=0.3)

        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.6)

        # --- gradient-ish axis bar -------------------------------------------
        axis = Line([X_LEFT, AXIS_Y, 0], [X_RIGHT, AXIS_Y, 0],
                    stroke_width=3)
        axis.set_stroke(color=[AMBER, GOLD, GREEN])

        left_lbl = Text("COMPILED", font=MONO, color=AMBER,
                        weight="BOLD").scale(0.36)
        left_sub = Text("close to the metal", font=MONO, color=SECOND).scale(0.24)
        left_grp = VGroup(left_lbl, left_sub).arrange(DOWN, buff=0.08)
        left_grp.move_to([x_at(0.0), AXIS_Y + 1.7, 0]).align_to(
            [X_LEFT, 0, 0], LEFT)

        right_lbl = Text("INTERPRETED", font=MONO, color=GREEN,
                         weight="BOLD").scale(0.36)
        right_sub = Text("human-friendly", font=MONO, color=SECOND).scale(0.24)
        right_grp = VGroup(right_lbl, right_sub).arrange(DOWN, buff=0.08)
        right_grp.move_to([x_at(1.0), AXIS_Y + 1.7, 0]).align_to(
            [X_RIGHT, 0, 0], RIGHT)

        fast_easy = Text("FAST  <->  EASY", font=MONO, color=SILVER).scale(0.3)
        fast_easy.move_to([0, AXIS_Y + 2.0, 0])

        self.play(Create(axis), run_time=0.8)
        self.play(FadeIn(left_grp), FadeIn(right_grp),
                  FadeIn(fast_easy), run_time=0.5)

        # --- language tags along the axis ------------------------------------
        # (name, color, frac along axis). Alternate above/below to avoid
        # overlap. Left = fast/compiled, right = easy/interpreted.
        langs_spec = [
            ("C",          CORAL,   0.04),
            ("Rust",       AMBER,   0.11),
            ("C++",        CORAL,   0.18),
            ("Go",         TEAL,    0.34),
            ("C#",         TEAL,    0.44),
            ("Java",       AMBER,   0.52),
            ("Swift",      CORAL,   0.60),
            ("TypeScript", VIOLET,  0.70),
            ("Python",     GREEN,   0.82),
            ("JavaScript", GOLD,    0.88),
            ("Ruby",       CORAL,   0.94),
            ("PHP",        VIOLET,  0.99),
        ]

        tags = []  # (group, label_mobj, color, frac, above)
        tag_groups = VGroup()
        for i, (name, color, frac) in enumerate(langs_spec):
            above = (i % 2 == 0)
            x = x_at(frac)
            tick = Line([x, AXIS_Y - 0.1, 0], [x, AXIS_Y + 0.1, 0],
                        stroke_color=SECOND, stroke_width=2)
            lbl = Text(name, font=MONO, color=color, weight="BOLD").scale(0.26)
            dy = 0.55 if above else -0.55
            lbl.move_to([x, AXIS_Y + dy, 0])
            connector = Line([x, AXIS_Y + (0.1 if above else -0.1), 0],
                             [x, AXIS_Y + (dy - 0.13 if above else dy + 0.13), 0],
                             stroke_color=SECOND, stroke_width=1)
            connector.set_stroke(opacity=0.3)
            g = VGroup(tick, connector, lbl)
            tag_groups.add(g)
            tags.append((g, lbl, color, frac, above, AXIS_Y + dy))

        self.play(*[GrowFromCenter(g) for g in tag_groups],
                  lag_ratio=0.04, run_time=1.1)

        # --- caption ---------------------------------------------------------
        caption = Text("the best tech doesn't exist", font=HEAD,
                       color=INK).scale(0.4)
        caption.move_to([0, AXIS_Y - 2.3, 0])
        self.add(caption)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        SWEEP_PERIOD = 6.0  # one full left->right scan

        # --- scanning highlight marker (vertical line + head dot) ------------
        scan = Line([X_LEFT, AXIS_Y - 1.1, 0], [X_LEFT, AXIS_Y + 1.1, 0],
                    stroke_color=INK, stroke_width=2)
        scan.set_stroke(opacity=0.5)
        scan_head = Triangle(color=GREEN, fill_opacity=1.0).scale(0.12)
        scan_head.rotate(np.pi)  # point down

        def scan_frac():
            return (t.get_value() % SWEEP_PERIOD) / SWEEP_PERIOD

        def scan_upd(m):
            fr = scan_frac()
            x = x_at(fr)
            m.put_start_and_end_on([x, AXIS_Y - 1.1, 0], [x, AXIS_Y + 1.1, 0])
            m.set_stroke(opacity=0.35 + 0.25 * (0.5 + 0.5 *
                                                np.sin(t.get_value() * 4)))
        scan.add_updater(scan_upd)

        def scan_head_upd(m):
            fr = scan_frac()
            x = x_at(fr)
            m.move_to([x, AXIS_Y + 1.25, 0])
        scan_head.add_updater(scan_head_upd)
        self.add(scan, scan_head)

        # --- tags light up as the scan passes + bob --------------------------
        white = ManimColor("#FFFFFF")
        for idx, (g, lbl, color, frac, above, base_y) in enumerate(tags):
            dim_col = ManimColor(color)

            def make_tag_upd(label, c_base, c_lit, f_pos, base_yy, seed):
                def _upd(m):
                    fr = scan_frac()
                    # proximity of scan to this tag along the axis
                    d = abs(fr - f_pos)
                    prox = np.clip(1.0 - d / 0.07, 0.0, 1.0)
                    lit = prox ** 2
                    # color brightens toward white when lit
                    label.set_color(interpolate_color(c_base, c_lit, 0.6 * lit))
                    label.set_opacity(0.55 + 0.45 * (0.4 + 0.6 * lit))
                    # gentle bob
                    bob = 0.06 * np.sin(1.8 * t.get_value() + seed)
                    label.move_to([x_at(f_pos), base_yy + bob, 0])
                return _upd

            lbl.add_updater(make_tag_upd(lbl, dim_col, white, frac, base_y,
                                         idx * 0.7))

        # --- cycling philosophy caption --------------------------------------
        lines = [
            "the best tech doesn't exist",
            "only the right tool for the job",
            "pick your trade-off",
        ]
        caption._idx = 0

        def caption_upd(m):
            idx = int(t.get_value() // 3.0) % len(lines)
            if idx != m._idx:
                m._idx = idx
                new = Text(lines[idx], font=HEAD, color=INK).scale(0.4)
                new.move_to([0, AXIS_Y - 2.3, 0])
                m.become(new)
            # subtle pulse
            m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 2.0)))
        caption.add_updater(caption_upd)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
