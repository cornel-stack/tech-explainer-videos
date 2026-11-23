"""Scene: the learning game.

Class `Training` (~19s). Cover the next word -> guess -> compare -> nudge the
weights. A masked word, a guess vs truth, an error, billions of little weight
dials nudging, and a loss curve descending over time. Then a small second
stage "fine-tune + human feedback". Caption: "guess the next word, trillions
of times, then fine-tune".

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
    Dot,
    Arrow,
    VMobject,
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


def token_pill(word, color=TEAL, scale=0.4):
    txt = Text(word, font=MONO, color=color).scale(scale)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=txt.width + 0.34,
        height=0.6,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.08,
    )
    txt.move_to(box.get_center())
    return VGroup(box, txt)


class Training(Scene):
    def construct(self):
        title = Text("The learning game", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- top: a sentence with the next word masked ---------------------
        words = ["The", "cat", "sat", "on", "the"]
        base_y = 1.9
        pills = []
        tmp = [token_pill(w, TEAL) for w in words]
        mask = token_pill("?????", AMBER)
        total_w = sum(p.width + 0.2 for p in tmp) + mask.width
        x = -total_w / 2
        for p in tmp:
            p.move_to([x + p.width / 2, base_y, 0])
            x += p.width + 0.2
            pills.append(p)
        mask.move_to([x + mask.width / 2, base_y, 0])
        mask_lbl = Text("cover the next word", font=MONO,
                        color=AMBER).scale(0.24)
        mask_lbl.next_to(mask, UP, buff=0.16)
        self.play(*[FadeIn(p) for p in pills], FadeIn(mask),
                  FadeIn(mask_lbl), lag_ratio=0.06, run_time=1.0)

        # --- guess vs truth + error ----------------------------------------
        guess = Text("guess:  mat  (0.31)", font=MONO, color=VIOLET).scale(0.32)
        truth = Text("truth:  mat", font=MONO, color=GREEN).scale(0.32)
        err = Text("error -> nudge", font=MONO, color=CORAL).scale(0.3)
        col = VGroup(guess, truth, err).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        col.move_to([-3.6, 0.1, 0])
        self.play(FadeIn(guess), FadeIn(truth), FadeIn(err), run_time=0.9)

        # --- billions of weight dials (grid of small dots) -----------------
        dials = VGroup()
        dial_list = []
        grid_c = np.array([-3.4, -2.0, 0.0])
        rows, cols = 5, 9
        for r in range(rows):
            for c in range(cols):
                pos = grid_c + np.array([(c - (cols - 1) / 2) * 0.26,
                                         (r - (rows - 1) / 2) * 0.26, 0])
                d = Dot(pos, color=SILVER, radius=0.045)
                dials.add(d)
                dial_list.append(d)
        dials_lbl = Text("billions of weights", font=MONO,
                         color=SILVER).scale(0.24)
        dials_lbl.next_to(dials, DOWN, buff=0.18)
        self.play(*[FadeIn(d) for d in dials], FadeIn(dials_lbl),
                  lag_ratio=0.01, run_time=1.0)

        # --- loss curve axes (right) ---------------------------------------
        ax_o = np.array([1.4, -2.3, 0.0])
        ax_x = Line(ax_o, ax_o + RIGHT * 4.6, stroke_color=SECOND,
                    stroke_width=1.5, stroke_opacity=0.5)
        ax_y = Line(ax_o, ax_o + UP * 3.6, stroke_color=SECOND,
                    stroke_width=1.5, stroke_opacity=0.5)
        loss_lbl = Text("loss", font=MONO, color=CORAL).scale(0.26)
        loss_lbl.next_to(ax_y, UP, buff=0.1)
        step_lbl = Text("training steps", font=MONO, color=SECOND).scale(0.24)
        step_lbl.next_to(ax_x, DOWN, buff=0.12).shift(RIGHT * 1.0)
        self.play(Create(ax_x), Create(ax_y), FadeIn(loss_lbl),
                  FadeIn(step_lbl), run_time=0.7)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # mask word flickers between candidate guesses (the guessing)
        def mask_upd(m):
            cands = ["mat", "rug", "mat", "sun", "mat"]
            idx = int(t.get_value() * 1.5) % len(cands)
            m.become(token_pill(cands[idx], AMBER).move_to(
                [m.get_center()[0], base_y, 0]))
            s = 0.5 + 0.5 * np.sin(4.0 * t.get_value())
            m[0].set_stroke(opacity=0.6 + 0.4 * s)
        mask.add_updater(mask_upd)

        # error label pulses coral
        err.add_updater(lambda m: m.set_opacity(
            0.5 + 0.5 * (0.5 + 0.5 * np.sin(3.2 * t.get_value()))))

        # dials "nudge" — jitter position + color flash green on update
        for i, d in enumerate(dial_list):
            home = d.get_center().copy()
            def make_dial(dot, base, phase):
                def _upd(m):
                    tt = t.get_value()
                    jx = 0.035 * np.sin(6.0 * tt + phase)
                    jy = 0.035 * np.cos(5.0 * tt + phase * 1.3)
                    dot.move_to(base + np.array([jx, jy, 0]))
                    s = 0.5 + 0.5 * np.sin(5.0 * tt + phase)
                    dot.set_color(interpolate_color(
                        ManimColor(SILVER), ManimColor(GREEN), 0.5 * s))
                return _upd
            d.add_updater(make_dial(d, home, i * 0.4))

        # loss curve grows left->right, descending with noise
        def loss_y(frac):
            # exponential-ish decay from high to low
            base = 3.2 * np.exp(-2.6 * frac) + 0.25
            return base

        curve = VMobject(stroke_color=CORAL, stroke_width=3)
        curve.set_points_as_corners([ax_o, ax_o + RIGHT * 0.001])
        self.add(curve)

        head = Dot(ax_o, color=GOLD, radius=0.07)
        self.add(head)

        xspan = 4.4

        def curve_upd(m):
            tt = t.get_value()
            prog = min(tt / 14.0, 1.0)  # fully drawn by ~14s
            pts = []
            steps = max(int(prog * 90), 2)
            for k in range(steps + 1):
                f = (k / steps) * prog
                px = ax_o[0] + f * xspan
                noise = 0.06 * np.sin(22.0 * f)
                py = ax_o[1] + loss_y(f) + noise
                pts.append([px, py, 0])
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
        curve.add_updater(curve_upd)

        def head_upd(m):
            tt = t.get_value()
            prog = min(tt / 14.0, 1.0)
            px = ax_o[0] + prog * xspan
            py = ax_o[1] + loss_y(prog)
            m.move_to([px, py, 0])
            s = 0.5 + 0.5 * np.sin(5.0 * tt)
            m.set_color(interpolate_color(
                ManimColor(GOLD), ManimColor(GREEN), 0.4 * s))
        head.add_updater(head_upd)

        # --- second stage: fine-tune + human feedback (appears later) ------
        ft_box = RoundedRectangle(corner_radius=0.1, width=3.4, height=0.8,
                                  stroke_color=TEAL, stroke_width=2,
                                  fill_color=TEAL, fill_opacity=0.06)
        ft_box.move_to([2.9, 2.5, 0])
        ft_lbl = Text("then: fine-tune + human feedback", font=MONO,
                      color=TEAL).scale(0.26)
        ft_lbl.move_to(ft_box.get_center())
        ft_group = VGroup(ft_box, ft_lbl)
        ft_group.set_opacity(0.0)
        self.add(ft_group)

        def ft_upd(m):
            tt = t.get_value()
            if tt >= 12.0:
                a = min((tt - 12.0) / 1.5, 1.0)
                pulse = 0.5 + 0.5 * np.sin(3.0 * tt)
                ft_box.set_stroke(TEAL, opacity=a * (0.6 + 0.4 * pulse))
                ft_box.set_fill(TEAL, opacity=a * (0.04 + 0.06 * pulse))
                ft_lbl.set_opacity(a)
            else:
                ft_box.set_stroke(opacity=0.0)
                ft_box.set_fill(opacity=0.0)
                ft_lbl.set_opacity(0.0)
        ft_group.add_updater(ft_upd)

        # caption
        cap = Text("guess the next word, trillions of times, then fine-tune",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
