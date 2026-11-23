"""Scene: The family tree of programming languages.

Class `Tree` (~20s). A tidy top-down influence graph: C is the root near the
top, descendants fan downward. A glowing influence pulse travels DOWN each edge
from parent to child on a loop, lighting the child node as it arrives; every
node gently breathes. Also sits faintly behind the intro title, so it must stay
legible.

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
    Line,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
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


class Tree(Scene):
    def construct(self):
        # --- node layout -----------------------------------------------------
        # Each node: (name, color, x, y). A tidy top-down tree: roots high,
        # descendants lower. Coordinates in Manim units (screen ~[-7,7]x[-4,4]).
        nodes_spec = {
            # systems branch (left of centre), C as the root up top
            "C":            (SILVER, -2.6,  2.7),
            "C++":          (CORAL,  -4.6,  1.1),
            "Objective-C":  (CORAL,  -5.6, -0.6),
            "Swift":        (CORAL,  -5.6, -2.3),
            "Java":         (AMBER,  -2.9,  1.1),
            "C#":           (TEAL,   -2.9, -0.6),
            "Go":           (TEAL,   -1.0,  1.1),
            "Rust":         (AMBER,   0.6,  1.1),
            # scripting branch (right side), separate roots
            "Python":       (GREEN,   2.3,  2.7),
            "Perl":         (CORAL,   4.1,  2.7),
            "PHP":          (VIOLET,  4.1,  1.0),
            "Ruby":         (CORAL,   2.3,  1.0),
            "JavaScript":   (GOLD,    6.0,  2.7),
            "TypeScript":   (VIOLET,  6.0,  1.0),
        }

        # influence / descent edges (parent -> child)
        edges_spec = [
            ("C", "C++"),
            ("C++", "Objective-C"),
            ("Objective-C", "Swift"),
            ("C", "Java"),
            ("Java", "C#"),
            ("C", "Go"),
            ("C", "Rust"),
            ("Python", "Ruby"),
            ("Perl", "PHP"),
            ("JavaScript", "TypeScript"),
        ]

        # --- build nodes -----------------------------------------------------
        node_groups = {}
        node_glows = {}
        node_color = {}
        for name, (color, x, y) in nodes_spec.items():
            lbl = Text(name, font=MONO, color=color, weight="BOLD").scale(0.3)
            w = lbl.width + 0.34
            h = 0.5
            box = RoundedRectangle(
                corner_radius=0.1, width=w, height=h,
                stroke_color=color, stroke_width=2,
                fill_color="#101014", fill_opacity=0.92,
            )
            glow = RoundedRectangle(
                corner_radius=0.1, width=w, height=h,
                stroke_color=color, stroke_width=9, stroke_opacity=0.0,
                fill_opacity=0,
            )
            g = VGroup(glow, box, lbl)
            g.move_to(np.array([x, y, 0.0]))
            node_groups[name] = g
            node_glows[name] = glow
            node_color[name] = color

        # --- build edges (lines parent-bottom -> child-top) ------------------
        edge_lines = []
        edge_meta = []  # (parent, child, start, end, color)
        for parent, child in edges_spec:
            pg = node_groups[parent]
            cg = node_groups[child]
            start = pg.get_bottom() + DOWN * 0.02
            end = cg.get_top() + UP * 0.02
            col = node_color[parent]
            line = Line(start, end, stroke_color=col, stroke_width=1.6)
            line.set_stroke(opacity=0.35)
            edge_lines.append(line)
            edge_meta.append((parent, child, np.array(start), np.array(end), col))

        edges_vg = VGroup(*edge_lines)
        nodes_vg = VGroup(*node_groups.values())

        # --- title -----------------------------------------------------------
        title = Text("THE FAMILY TREE", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.62)
        title.to_edge(UP, buff=0.28)

        sub = Text("influence flows downward — every language descends from another",
                   font=MONO, color=SECOND).scale(0.26)
        sub.next_to(title, DOWN, buff=0.12)

        # --- intro -----------------------------------------------------------
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.3)
        self.play(Create(edges_vg), run_time=0.9)
        self.play(*[GrowFromCenter(g) for g in node_groups.values()],
                  lag_ratio=0.05, run_time=1.2)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        PERIOD = 4.0  # seconds for one full pulse down every edge

        # --- travelling pulses along each edge -------------------------------
        pulse_dots = VGroup()
        for i, (parent, child, start, end, col) in enumerate(edge_meta):
            dot = Dot(color=col, radius=0.07)

            def make_pulse(p_start, p_end, phase):
                s = p_start
                e = p_end

                def _upd(m):
                    tt = (t.get_value() + phase) % PERIOD
                    frac = tt / PERIOD
                    eased = rate_functions.ease_in_out_sine(frac)
                    pos = s * (1 - eased) + e * eased
                    m.move_to(pos)
                    # bright at travel, fade near endpoints
                    glow = np.sin(np.pi * frac)
                    m.set_opacity(np.clip(0.2 + 0.8 * glow, 0.0, 1.0))
                return _upd

            dot.add_updater(make_pulse(start, end, (i % 5) * 0.8))
            pulse_dots.add(dot)
        self.add(pulse_dots)

        # --- node breathing + "arrival" light-up -----------------------------
        # Map each child to the edges arriving at it and their phase, so the
        # node brightens as a pulse lands.
        arrivals = {}  # child -> list of phases
        for i, (parent, child, start, end, col) in enumerate(edge_meta):
            arrivals.setdefault(child, []).append((i % 5) * 0.8)

        for name, g in node_groups.items():
            glow = node_glows[name]
            col = node_color[name]
            base_col = ManimColor(col)
            white = ManimColor("#FFFFFF")
            phases = arrivals.get(name, [])

            def make_node_upd(gl, phase_list, idx_seed):
                def _upd(m):
                    tt = t.get_value()
                    # gentle breathing baseline
                    breath = 0.5 + 0.5 * np.sin(1.3 * tt + idx_seed)
                    base_op = 0.04 + 0.10 * breath
                    # arrival flashes: strongest when a pulse reaches end
                    flash = 0.0
                    for ph in phase_list:
                        fr = ((tt + ph) % PERIOD) / PERIOD
                        flash = max(flash, np.sin(np.pi * fr) ** 6)
                    gl.set_stroke(opacity=np.clip(base_op + 0.85 * flash, 0, 1))
                    gl.set_stroke(color=interpolate_color(base_col, white,
                                                          0.5 * flash))
                return _upd

            glow.add_updater(make_node_upd(glow, phases,
                                           (abs(hash(name)) % 10) * 0.6))

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
