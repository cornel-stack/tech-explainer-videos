"""Scene: tokens -> vectors on a map of meaning.

Class `Embed` (~18s). Each token number maps to a VIOLET vector (short column
of numbers). A few labelled points are plotted on a 2D "map of meaning" where
king/queen and Paris/France sit close; an arrow shows
"king - man + woman ~= queen". Caption: "tokens become vectors on a map of
meaning".

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
    DashedLine,
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
        width=txt.width + 0.32,
        height=0.58,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.08,
    )
    txt.move_to(box.get_center())
    return VGroup(box, txt)


def vector_col(nums, color=VIOLET, scale=0.34):
    """A VIOLET column of numbers = a vector."""
    rows = VGroup()
    for n in nums:
        rows.add(Text(f"{n:+.2f}", font=MONO, color=color).scale(scale))
    rows.arrange(DOWN, buff=0.08)
    box = RoundedRectangle(
        corner_radius=0.08,
        width=rows.width + 0.26,
        height=rows.height + 0.22,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.05,
    )
    rows.move_to(box.get_center())
    return VGroup(box, rows)


class Embed(Scene):
    def construct(self):
        title = Text("Vectors on a map of meaning", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- LEFT: token -> vector mapping ----------------------------------
        pill = token_pill("king", TEAL)
        pill.move_to([-5.2, 1.4, 0])
        idn = Text("4412", font=MONO, color=SECOND).scale(0.32)
        idn.next_to(pill, DOWN, buff=0.16)
        self.play(FadeIn(pill), FadeIn(idn), run_time=0.6)

        vec = vector_col([0.21, -0.74, 0.55, 0.12, -0.33], VIOLET)
        vec.move_to([-5.15, -1.1, 0])
        vec_lbl = Text("vector", font=MONO, color=VIOLET).scale(0.26)
        vec_lbl.next_to(vec, DOWN, buff=0.14)
        arrow_map = Arrow(idn.get_bottom(), vec.get_top(), buff=0.12,
                          stroke_width=3, color=SECOND,
                          max_tip_length_to_length_ratio=0.18)
        self.play(Create(arrow_map), FadeIn(vec), FadeIn(vec_lbl),
                  run_time=0.9)

        # --- RIGHT: the 2D map of meaning -----------------------------------
        origin = np.array([2.1, -1.4, 0.0])
        ax_x = Line(origin, origin + RIGHT * 4.4, stroke_color=SECOND,
                    stroke_width=1.5, stroke_opacity=0.5)
        ax_y = Line(origin, origin + UP * 3.3, stroke_color=SECOND,
                    stroke_width=1.5, stroke_opacity=0.5)
        map_lbl = Text("map of meaning", font=MONO, color=SECOND).scale(0.26)
        map_lbl.move_to(origin + RIGHT * 2.2 + DOWN * 0.3)
        self.play(Create(ax_x), Create(ax_y), FadeIn(map_lbl), run_time=0.7)

        # labelled points (x,y offsets in map space)
        def P(dx, dy):
            return origin + RIGHT * dx + UP * dy

        points = {
            "king":  (P(1.0, 2.5), VIOLET),
            "queen": (P(2.1, 2.3), VIOLET),
            "man":   (P(0.8, 0.9), TEAL),
            "woman": (P(1.9, 0.7), TEAL),
            "Paris": (P(3.3, 2.0), GOLD),
            "France": (P(3.7, 1.3), GOLD),
        }
        dots = {}
        labels = {}
        for name, (pos, col) in points.items():
            d = Dot(pos, color=col, radius=0.07)
            lb = Text(name, font=MONO, color=col).scale(0.28)
            lb.next_to(d, UP, buff=0.08)
            dots[name] = d
            labels[name] = lb
        self.play(*[FadeIn(d) for d in dots.values()],
                  *[FadeIn(lb) for lb in labels.values()],
                  lag_ratio=0.06, run_time=1.1)

        # analogy arrows: king - man + woman ~= queen
        a1 = Arrow(dots["man"].get_center(), dots["king"].get_center(),
                   buff=0.08, stroke_width=3, color=AMBER,
                   max_tip_length_to_length_ratio=0.18)
        a2 = Arrow(dots["woman"].get_center(), dots["queen"].get_center(),
                   buff=0.08, stroke_width=3, color=AMBER,
                   max_tip_length_to_length_ratio=0.18)
        eqn = Text("king - man + woman  ~=  queen", font=MONO,
                   color=AMBER).scale(0.3)
        eqn.move_to(origin + RIGHT * 2.1 + UP * 3.55)
        self.play(Create(a1), Create(a2), FadeIn(eqn), run_time=0.9)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # vector numbers subtly shimmer (the vector is "alive")
        rows_group = vec[1]
        for i, r in enumerate(rows_group):
            def make_row(phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + phase)
                    m.set_color(interpolate_color(
                        ManimColor(VIOLET), ManimColor(INK), 0.2 * s))
                return _upd
            r.add_updater(make_row(i * 0.7))

        vec[0].add_updater(lambda m: m.set_stroke(
            opacity=0.55 + 0.45 * (0.5 + 0.5 * np.sin(2.6 * t.get_value()))))

        # pill pulse
        pill[0].add_updater(lambda m: m.set_stroke(
            opacity=0.55 + 0.45 * (0.5 + 0.5 * np.sin(2.2 * t.get_value()))))

        # map dots pulse by color group
        pulse_sets = [
            (["king", "queen"], VIOLET, 0.0),
            (["man", "woman"], TEAL, 1.3),
            (["Paris", "France"], GOLD, 2.6),
        ]
        for names, col, phase in pulse_sets:
            for nm in names:
                def make_dot(base_col, ph):
                    def _upd(m):
                        s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + ph)
                        m.scale_to_fit_width(0.14 * (1.0 + 0.4 * s))
                    return _upd
                dots[nm].add_updater(make_dot(col, phase))

        # analogy arrows pulse amber
        def arr_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value())
            m.set_opacity(0.45 + 0.5 * s)
        a1.add_updater(arr_upd)
        a2.add_updater(arr_upd)
        eqn.add_updater(lambda m: m.set_opacity(
            0.5 + 0.5 * (0.5 + 0.5 * np.sin(2.0 * t.get_value()))))

        # mapping arrow flow
        arrow_map.add_updater(lambda m: m.set_opacity(
            0.4 + 0.5 * (0.5 + 0.5 * np.sin(2.6 * t.get_value()))))

        # caption
        cap = Text("tokens become vectors on a map of meaning",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
