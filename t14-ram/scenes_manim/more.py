"""Scene: performance vs RAM installed — the cliff, the plateau, and the
wasted territory. THE CENTREPIECE.

Class `More` (~22s). X-axis "RAM installed", Y-axis "performance". Curve: a
CORAL cliff on the left (too little RAM -> swapping to disk), rising steeply
to a GREEN plateau once past an "enough" marker, flat forever after. A marker
dot slides along the curve (driven by t) from too-little up over the cliff to
the flat top, then keeps going into "wasted" territory where extra SILVER RAM
blocks stack up empty. A small desk-metaphor inset pairs it. Caption cycles:
"too little = cliff · enough = fast · more = wasted".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Line,
    VMobject,
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

# curve geometry in scene coords
X0 = -5.6          # axis origin x
X1 = 2.2           # curve end x (performance curve)
Y0 = -2.6          # axis origin y
YMAX = 2.4         # top of plot
ENOUGH_X = -2.6    # "enough" marker x


def perf_at(x):
    """Performance (scene y) as a function of x along the plot."""
    # normalized position 0..1 from X0..X1
    u = (x - X0) / (X1 - X0)
    enough_u = (ENOUGH_X - X0) / (X1 - X0)
    if u <= enough_u:
        # cliff: crashed low, rising steeply near the enough point
        r = u / enough_u  # 0..1
        val = 0.05 + 0.95 * rate_functions.ease_in_quad(r) ** 1.6
    else:
        # plateau: flat high
        val = 1.0
    return Y0 + 0.15 + val * (YMAX - Y0 - 0.3)


class More(Scene):
    def construct(self):
        title = Text("More RAM isn't always faster",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- axes ------------------------------------------------------------
        x_axis = Line(np.array([X0, Y0, 0]), np.array([4.9, Y0, 0]),
                      stroke_color=SECOND, stroke_width=2)
        y_axis = Line(np.array([X0, Y0, 0]), np.array([X0, YMAX, 0]),
                      stroke_color=SECOND, stroke_width=2)
        x_lbl = Text("RAM installed ->", font=MONO, color=SECOND).scale(0.28)
        x_lbl.next_to(x_axis, DOWN, buff=0.18).align_to(x_axis, RIGHT)
        y_lbl = Text("performance", font=MONO, color=SECOND).scale(0.28)
        y_lbl.rotate(np.pi / 2).next_to(y_axis, LEFT, buff=0.18)
        self.play(Create(x_axis), Create(y_axis),
                  FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)

        # --- the curve: cliff (coral) + plateau (green) ----------------------
        xs = np.linspace(X0, X1, 120)
        cliff_pts = []
        plateau_pts = []
        for x in xs:
            p = np.array([x, perf_at(x), 0])
            if x <= ENOUGH_X:
                cliff_pts.append(p)
            else:
                plateau_pts.append(p)
        # include the join point in both for continuity
        if cliff_pts and plateau_pts:
            plateau_pts = [cliff_pts[-1]] + plateau_pts

        cliff = VMobject(stroke_color=CORAL, stroke_width=5)
        cliff.set_points_as_corners(cliff_pts)
        plateau = VMobject(stroke_color=GREEN, stroke_width=5)
        plateau.set_points_as_corners(plateau_pts)

        self.play(Create(cliff), run_time=0.8)
        self.play(Create(plateau), run_time=0.8)

        # "enough" marker (vertical dashed-ish line)
        enough_line = Line(
            np.array([ENOUGH_X, Y0, 0]),
            np.array([ENOUGH_X, perf_at(ENOUGH_X), 0]),
            stroke_color=TEAL, stroke_width=2, stroke_opacity=0.6)
        enough_lbl = Text("enough", font=MONO, color=TEAL).scale(0.26)
        enough_lbl.next_to(enough_line, UP, buff=0.1)

        cliff_lbl = Text("swapping to disk", font=MONO, color=CORAL).scale(0.26)
        cliff_lbl.move_to(np.array([X0 + 1.0, Y0 + 0.7, 0]))
        plat_lbl = Text("fast & flat", font=MONO, color=GREEN).scale(0.26)
        plat_lbl.move_to(np.array([0.2, perf_at(0.0) + 0.3, 0]))
        self.play(Create(enough_line), FadeIn(enough_lbl),
                  FadeIn(cliff_lbl), FadeIn(plat_lbl), run_time=0.6)

        # --- wasted territory: empty SILVER RAM blocks stack to the right ----
        waste_x = 3.2
        waste_lbl = Text("wasted", font=MONO, color=SILVER).scale(0.26)
        waste_lbl.move_to(np.array([waste_x + 0.3, perf_at(X1) + 0.4, 0]))
        self.add(waste_lbl)

        waste_blocks = VGroup()
        for i in range(6):
            blk = Rectangle(
                width=0.9, height=0.3, stroke_color=SILVER,
                stroke_width=2, fill_color=BG, fill_opacity=0.3,
            )
            blk.move_to(np.array([waste_x + 0.3, Y0 + 0.2 + i * 0.36, 0]))
            waste_blocks.add(blk)
        self.add(waste_blocks)

        # --- desk metaphor inset (bottom-left) ------------------------------
        desk_ok = RoundedRectangle(
            corner_radius=0.05, width=1.7, height=0.1, stroke_width=0,
            fill_color=TEAL, fill_opacity=0.9,
        ).move_to(np.array([-4.9, -3.2, 0]))
        desk_ok_lbl = Text("desk fits -> space to spare", font=MONO,
                           color=TEAL).scale(0.2)
        desk_ok_lbl.next_to(desk_ok, UP, buff=0.08)
        desk_bad = RoundedRectangle(
            corner_radius=0.05, width=0.9, height=0.1, stroke_width=0,
            fill_color=CORAL, fill_opacity=0.9,
        ).move_to(np.array([-1.9, -3.2, 0]))
        desk_bad_lbl = Text("too small -> papers fall off (disk)",
                            font=MONO, color=CORAL).scale(0.2)
        desk_bad_lbl.next_to(desk_bad, UP, buff=0.08)
        self.add(desk_ok, desk_ok_lbl, desk_bad, desk_bad_lbl)

        # caption (cycles)
        caption = Text("too little = cliff", font=MONO, color=CORAL).scale(0.34)
        caption.to_edge(DOWN, buff=0.25)
        self.add(caption)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        period = 7.0  # one full sweep

        # marker dot slides along curve, then into wasted territory
        marker = Dot(color=INK, radius=0.11)

        # overshoot region: x goes X0 -> X1 -> waste_x+0.6
        max_x = waste_x + 0.9

        def marker_upd(m):
            p = (t.get_value() % period) / period
            # 0..0.75 slide along curve X0->X1; 0.75..1.0 into waste flat
            if p < 0.72:
                a = p / 0.72
                x = X0 + a * (X1 - X0)
                y = perf_at(x)
            else:
                a = (p - 0.72) / 0.28
                x = X1 + a * (max_x - X1)
                y = perf_at(X1)
            m.move_to(np.array([x, y, 0]))
        marker.add_updater(marker_upd)
        self.add(marker)

        # empty waste blocks appear progressively as marker passes
        for i, blk in enumerate(waste_blocks):
            idx = i

            def make_blk(idx, blk):
                def _upd(m):
                    p = (t.get_value() % period) / period
                    # reveal in the waste phase
                    if p >= 0.72:
                        a = (p - 0.72) / 0.28
                        show = a * 6
                        if idx < show:
                            m.set_opacity(0.5)
                            m.set_stroke(opacity=0.9)
                        else:
                            m.set_opacity(0.0)
                            m.set_stroke(opacity=0.0)
                    else:
                        m.set_opacity(0.0)
                        m.set_stroke(opacity=0.0)
                return _upd
            blk.add_updater(make_blk(idx, blk))

        # caption cycles through 3 messages
        cap = caption
        cap_state = {"i": -1}
        cap_msgs = [
            ("too little = cliff", CORAL),
            ("enough = fast", GREEN),
            ("more = wasted", SILVER),
        ]

        def cap_upd(m):
            p = (t.get_value() % period) / period
            if p < 0.33:
                i = 0
            elif p < 0.72:
                i = 1
            else:
                i = 2
            if i != cap_state["i"]:
                cap_state["i"] = i
                txt, col = cap_msgs[i]
                new = Text(txt, font=MONO, color=col).scale(0.34)
                new.move_to(m.get_center())
                m.become(new)
        cap.add_updater(cap_upd)

        # plateau gently breathes to stay alive
        pl = plateau

        def plat_breathe(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value())
            m.set_stroke(opacity=0.7 + 0.3 * s)
        pl.add_updater(plat_breathe)

        self.play(t.animate.set_value(22.0), run_time=22.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
