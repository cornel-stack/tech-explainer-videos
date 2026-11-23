"""Scene: Every Version of Windows — the every-other-one curse.

Class `Tocktick` (~20s). The modern versions sit in a row left->right:
98, ME, XP, Vista, 7, 8, 10, 11. They form a ZIGZAG / step line that rises to
a green GOOD level for loved releases and drops to a coral BAD level for hated
ones (11 at a middle amber level). A check mark sits on each up node, a cross
on each down node, the version label under each. A metronome / pendulum arm at
the top swings GOOD<->BAD via sin(t) with a ticking GOOD / BAD label flipping
in time. A highlight travels along the step line on a loop, pulsing the nodes
in sequence.

Dark palette only, TEXT labels only (no logos), continuous motion driven by a
master ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Line,
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

# (label, verdict)  good -> up/green, bad -> down/coral, meh -> middle/amber
STEPS = [
    ("98", "good"),
    ("ME", "bad"),
    ("XP", "good"),
    ("Vista", "bad"),
    ("7", "good"),
    ("8", "bad"),
    ("10", "good"),
    ("11", "meh"),
]

Y_GOOD = 1.3
Y_BAD = -1.3
Y_MEH = 0.1


class Tocktick(Scene):
    def construct(self):
        title = Text("the every-other-one curse", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- level guide lines ----------------------------------------------
        x_left, x_right = -6.2, 6.2
        good_line = Line([x_left, Y_GOOD, 0], [x_right, Y_GOOD, 0],
                         stroke_color=GREEN, stroke_width=1.5,
                         stroke_opacity=0.25)
        bad_line = Line([x_left, Y_BAD, 0], [x_right, Y_BAD, 0],
                        stroke_color=CORAL, stroke_width=1.5,
                        stroke_opacity=0.25)
        good_tag = Text("GOOD", font=MONO, color=GREEN).scale(0.28)
        good_tag.next_to(good_line, LEFT, buff=0.18)
        bad_tag = Text("BAD", font=MONO, color=CORAL).scale(0.28)
        bad_tag.next_to(bad_line, LEFT, buff=0.18)
        self.play(Create(good_line), Create(bad_line),
                  FadeIn(good_tag), FadeIn(bad_tag), run_time=0.7)

        # --- node positions along the zigzag --------------------------------
        n = len(STEPS)
        xs = np.linspace(x_left + 1.1, x_right - 0.3, n)
        pts = []
        for (name, verd), xx in zip(STEPS, xs):
            if verd == "good":
                yy = Y_GOOD
            elif verd == "bad":
                yy = Y_BAD
            else:
                yy = Y_MEH
            pts.append(np.array([xx, yy, 0]))

        # --- step / zigzag line connecting the nodes ------------------------
        segs = VGroup()
        for a, b in zip(pts[:-1], pts[1:]):
            seg = Line(a, b, stroke_color=SILVER, stroke_width=3)
            segs.add(seg)
        self.play(*[Create(s) for s in segs], lag_ratio=0.1, run_time=1.2)

        # --- nodes + marks + labels -----------------------------------------
        node_dots = []
        node_cols = []
        marks = VGroup()
        labels = VGroup()
        grow = []
        for (name, verd), p in zip(STEPS, pts):
            if verd == "good":
                col, sym = GREEN, "check"
            elif verd == "bad":
                col, sym = CORAL, "cross"
            else:
                col, sym = AMBER, "tilde"
            node_cols.append(col)

            dot = Dot(p, color=col, radius=0.14)
            node_dots.append(dot)
            grow.append(GrowFromCenter(dot))

            # mark symbol built from text (TEXT LABELS ONLY, no shapes needed).
            if sym == "check":
                mk = Text("OK", font=MONO, color=GREEN, weight="BOLD").scale(0.3)
                mk.next_to(dot, UP, buff=0.18)
            elif sym == "cross":
                mk = Text("X", font=MONO, color=CORAL, weight="BOLD").scale(0.36)
                mk.next_to(dot, DOWN, buff=0.18)
            else:
                mk = Text("~", font=MONO, color=AMBER, weight="BOLD").scale(0.4)
                mk.next_to(dot, UP, buff=0.12)
            marks.add(mk)

            lbl = Text(name, font=MONO, color=col, weight="BOLD").scale(0.32)
            # labels under the node (below BAD level so the row reads flat)
            lbl.move_to([p[0], Y_BAD - 0.75, 0])
            labels.add(lbl)

        self.play(*grow, lag_ratio=0.08, run_time=1.2)
        self.play(*[FadeIn(m) for m in marks],
                  *[FadeIn(l) for l in labels],
                  lag_ratio=0.05, run_time=1.0)

        # --- metronome / pendulum at the top --------------------------------
        pivot = np.array([0.0, title.get_bottom()[1] - 0.25, 0])
        arm_len = 0.95
        arm = Line(pivot, pivot + DOWN * arm_len,
                   stroke_color=GOLD, stroke_width=4)
        bob = Dot(pivot + DOWN * arm_len, color=GOLD, radius=0.12)
        pivot_dot = Dot(pivot, color=SILVER, radius=0.05)
        self.add(arm, bob, pivot_dot)

        # ticking GOOD / BAD label beside the pendulum.
        tick_lbl = Text("GOOD", font=MONO, color=GREEN, weight="BOLD").scale(0.4)
        tick_lbl.next_to(pivot, RIGHT, buff=2.6)
        tick_lbl._state = "GOOD"
        self.add(tick_lbl)

        # --- highlight runner that travels the step line --------------------
        runner = Dot(pts[0], color=TEAL, radius=0.18)
        runner.set_opacity(0.9)
        self.add(runner)

        # --- caption ---------------------------------------------------------
        cap = Text("a great one, then a dud, then a great one again — "
                   "fans brace for each new release",
                   font=HEAD, color=SECOND).scale(0.3)
        cap.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.6)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        SWING = 2.4            # seconds per half-swing of the pendulum
        max_ang = 0.6         # radians

        # pendulum arm + bob swing via sin(t).
        px, py = pivot[0], pivot[1]

        def arm_upd(m):
            ang = max_ang * np.sin(2 * np.pi * t.get_value() / (2 * SWING))
            end = np.array([px + arm_len * np.sin(ang),
                            py - arm_len * np.cos(ang), 0])
            m.put_start_and_end_on(pivot, end)
        arm.add_updater(arm_upd)

        def bob_upd(m):
            ang = max_ang * np.sin(2 * np.pi * t.get_value() / (2 * SWING))
            end = np.array([px + arm_len * np.sin(ang),
                            py - arm_len * np.cos(ang), 0])
            m.move_to(end)
            s = 0.5 + 0.5 * np.sin(4.0 * t.get_value())
            m.set_opacity(0.7 + 0.3 * s)
        bob.add_updater(bob_upd)

        # ticking label flips GOOD / BAD in time with the swing.
        def tick_upd(m):
            ang = np.sin(2 * np.pi * t.get_value() / (2 * SWING))
            want = "GOOD" if ang >= 0 else "BAD"
            if want != m._state:
                m._state = want
                col = GREEN if want == "GOOD" else CORAL
                new = Text(want, font=MONO, color=col,
                           weight="BOLD").scale(0.4)
                new.move_to(m)
                m.become(new)
        tick_lbl.add_updater(tick_upd)

        # highlight runner loops along the zigzag, pulsing nodes in sequence.
        node_x = np.array([p[0] for p in pts])
        node_y = np.array([p[1] for p in pts])
        LOOP = 7.0

        def runner_upd(m):
            frac = (t.get_value() % LOOP) / LOOP
            seg_f = frac * (n - 1)
            i = int(np.floor(seg_f))
            i = min(i, n - 2)
            local = seg_f - i
            pos = pts[i] * (1 - local) + pts[i + 1] * local
            m.move_to(pos)
            s = 0.5 + 0.5 * np.sin(6.0 * t.get_value())
            m.set_opacity(0.6 + 0.35 * s)
        runner.add_updater(runner_upd)

        # nodes pulse as the runner passes; constant breathing otherwise.
        base_r = 0.14
        for i, dot in enumerate(node_dots):
            nx, ny = node_x[i], node_y[i]

            def make_node_upd(d, nxx, nyy, phase):
                def _upd(m):
                    tt = t.get_value()
                    frac = (tt % LOOP) / LOOP
                    seg_f = frac * (n - 1)
                    rx = np.interp(seg_f, np.arange(n), node_x)
                    ry = np.interp(seg_f, np.arange(n), node_y)
                    dist2 = (rx - nxx) ** 2 + (ry - nyy) ** 2
                    prox = np.exp(-dist2 / 0.18)
                    breathe = 0.5 + 0.5 * np.sin(2.4 * tt + phase)
                    s = 1.0 + 0.15 * breathe + 0.9 * prox
                    d.set(width=2 * base_r * s)
                    d.set_opacity(np.clip(0.75 + 0.25 * breathe + prox, 0, 1))
                return _upd
            dot.add_updater(make_node_upd(dot, nx, ny, i * 0.6))

        # marks brighten as the runner passes their node.
        for i, mk in enumerate(marks):
            nx, ny = node_x[i], node_y[i]

            def make_mark_upd(nxx, nyy):
                def _upd(m):
                    frac = (t.get_value() % LOOP) / LOOP
                    seg_f = frac * (n - 1)
                    rx = np.interp(seg_f, np.arange(n), node_x)
                    ry = np.interp(seg_f, np.arange(n), node_y)
                    dist2 = (rx - nxx) ** 2 + (ry - nyy) ** 2
                    prox = np.exp(-dist2 / 0.18)
                    m.set_opacity(np.clip(0.5 + 0.5 * prox, 0, 1))
                return _upd
            mk.add_updater(make_mark_upd(nx, ny))

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
