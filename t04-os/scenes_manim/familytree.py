"""FamilyTree — the OS genealogy as a growing timeline tree.

Three lineages draw themselves then keep pulsing, with light pulses travelling
down the connecting branches continuously:

  UNIX (1969) -> BSD (1977) -> FreeBSD (1993)
  UNIX -> Darwin -> macOS (2001) -> iOS (2007)                 [teal]
  Linux (1991) -> Android (2008) / ChromeOS (2011) / SteamOS (2013)  [green]
  MS-DOS (1981) -> Windows (1985) -> Windows NT (1993)         [violet]
"""

import math

from manim import (
    VGroup,
    Scene,
    RoundedRectangle,
    Line,
    Dot,
    Text,
    ValueTracker,
    FadeIn,
    Create,
    always_redraw,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

BG = "#09090C"
INK = "#E9E8E4"
INK2 = "#90908C"
TEAL = "#2DD4BF"
GREEN = "#35FF9E"
VIOLET = "#9B8CFF"
AMBER = "#FFB020"
SILVER = "#C9CDD4"
CORAL = "#FF6B4A"

FONT = "Inter"
MONO = "DejaVu Sans Mono"


def node(name, year, color, scale=0.5):
    """A rounded node showing name + year, with a soft glow ring."""
    label = Text(name, font=FONT, color=INK, weight="BOLD").scale(scale)
    yr = Text(str(year), font=MONO, color=color).scale(scale * 0.62)
    stack = VGroup(label, yr).arrange(DOWN, buff=0.08)
    w = max(stack.width + 0.5, 1.5)
    h = stack.height + 0.45
    glow = RoundedRectangle(
        width=w, height=h, corner_radius=0.14,
        stroke_color=color, stroke_width=12, stroke_opacity=0.12, fill_opacity=0.0,
    )
    box = RoundedRectangle(
        width=w, height=h, corner_radius=0.14,
        stroke_color=color, stroke_width=2.2,
        fill_color=color, fill_opacity=0.08,
    )
    stack.move_to(box.get_center())
    g = VGroup(glow, box, stack)
    g.node_color = color
    return g


class FamilyTree(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("The family tree", font=FONT, color=INK, weight="BOLD").scale(0.8)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)

        # Column x positions by decade-ish progression (left = older).
        cx = [-5.9, -3.3, -0.7, 1.9, 4.5]

        # --- Define nodes --------------------------------------------------
        # row y positions
        y_top = 2.2
        y_mid = 0.0
        y_low = -2.3

        unix = node("UNIX", 1969, TEAL).move_to([cx[0], y_mid, 0])
        bsd = node("BSD", 1977, TEAL).move_to([cx[1], y_top, 0])
        freebsd = node("FreeBSD", 1993, TEAL).move_to([cx[2], y_top, 0])
        darwin = node("Darwin", 2000, TEAL).move_to([cx[2], y_mid, 0])
        macos = node("macOS", 2001, SILVER).move_to([cx[3], y_mid, 0])
        ios = node("iOS", 2007, SILVER).move_to([cx[4], y_mid, 0])

        linux = node("Linux", 1991, GREEN).move_to([cx[1], y_low, 0])
        android = node("Android", 2008, AMBER).move_to([cx[2], y_low + 0.9, 0])
        chromeos = node("ChromeOS", 2011, AMBER).move_to([cx[3], y_low, 0])
        steamos = node("SteamOS", 2013, CORAL).move_to([cx[3], y_low - 1.3, 0])

        msdos = node("MS-DOS", 1981, VIOLET).move_to([cx[0], y_low - 0.6, 0])
        win = node("Windows", 1985, VIOLET).move_to([cx[1], y_low + 1.4, 0])
        winnt = node("Windows NT", 1993, VIOLET).move_to([cx[2], y_low + 2.0, 0])

        # Scale everything a touch so it fits with margins.
        all_nodes = VGroup(
            unix, bsd, freebsd, darwin, macos, ios,
            linux, android, chromeos, steamos,
            msdos, win, winnt,
        )

        # --- Edges (parent -> child, with a family color) -----------------
        edges = [
            (unix, bsd, TEAL),
            (bsd, freebsd, TEAL),
            (unix, darwin, TEAL),
            (darwin, macos, TEAL),
            (macos, ios, SILVER),
            (linux, android, GREEN),
            (linux, chromeos, GREEN),
            (linux, steamos, GREEN),
            (msdos, win, VIOLET),
            (win, winnt, VIOLET),
        ]

        edge_lines = []  # (line_mobject, color, start_pt, end_pt)
        for parent, child, color in edges:
            start = parent.get_edge_center(RIGHT) if parent.get_center()[0] <= child.get_center()[0] else parent.get_edge_center(LEFT)
            end = child.get_edge_center(LEFT) if child.get_center()[0] >= parent.get_center()[0] else child.get_edge_center(RIGHT)
            ln = Line(start, end, color=color, stroke_width=2.0, stroke_opacity=0.5)
            edge_lines.append((ln, color, start, end))

        # --- Build sequence: lineage by lineage ---------------------------
        def draw_group(nodes, lines):
            anims_nodes = [FadeIn(n, scale=0.85) for n in nodes]
            self.play(*anims_nodes, run_time=0.9)
            if lines:
                self.play(*[Create(l) for l in lines], run_time=0.7)

        unix_lines = [edge_lines[i][0] for i in (0, 1, 2, 3, 4)]
        linux_lines = [edge_lines[i][0] for i in (5, 6, 7)]
        ms_lines = [edge_lines[i][0] for i in (8, 9)]

        # UNIX / Apple branch (teal)
        self.play(FadeIn(unix, scale=0.85), run_time=0.6)
        draw_group([bsd, freebsd, darwin, macos, ios], unix_lines)
        # Linux branch (green)
        draw_group([linux, android, chromeos, steamos], linux_lines)
        # Microsoft branch (violet)
        draw_group([msdos, win, winnt], ms_lines)

        # --- Continuous light pulses down each branch ---------------------
        clock = ValueTracker(0.0)
        speed = 0.35  # fraction of branch per second

        def make_pulse(start, end, color, offset):
            def f():
                # position along the line based on clock, looping
                t = (clock.get_value() * speed + offset) % 1.0
                pt = start + (end - start) * t
                glow = Dot(pt, radius=0.13, color=color).set_opacity(0.2)
                core = Dot(pt, radius=0.06, color=color)
                return VGroup(glow, core)
            return f

        for i, (ln, color, s, e) in enumerate(edge_lines):
            offset = (i * 0.37) % 1.0
            self.add(always_redraw(make_pulse(s, e, color, offset)))

        # --- Breathing node glows -----------------------------------------
        for i, n in enumerate(all_nodes):
            glow = n[0]
            col = n.node_color
            phase = i * 0.5

            def breather(m, p=phase):
                t = clock.get_value()
                m.set_stroke(opacity=0.10 + 0.10 * (0.5 + 0.5 * math.sin(t * 1.6 + p)))

            glow.add_updater(breather)

        # Run the master clock for the remainder (~26s total).
        self.play(clock.animate.set_value(8.0), run_time=19.5, rate_func=rate_functions.linear)
        self.wait(0.3)

        # Clean final frame — stop updaters.
        for n in all_nodes:
            n[0].clear_updaters()
        self.wait(0.2)
