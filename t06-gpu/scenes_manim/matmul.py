"""MatMul — matrix multiplication, the heart of AI. THE payoff scene.

A x B = C as grids. Output cells computed as dot-products of a row and a
column, with MANY output tiles highlighted/computed in parallel. Lands on:
"a neural-network layer IS a matrix multiply - and a GPU is a matrix-multiply
machine." Then reveals TENSOR CORES as a distinct unit. ~26s. violet/green.
"""

import math

from manim import (
    Scene,
    VGroup,
    RoundedRectangle,
    Rectangle,
    Text,
    Line,
    ValueTracker,
    Write,
    FadeIn,
    Create,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

BG = "#07090A"
INK = "#E9EAE6"
SUB = "#8A8C88"
GREEN = "#39FF88"
VIOLET = "#B06BFF"
TEAL = "#2DD4BF"

MONO = "JetBrains Mono"
HEAD = "Inter"


def _grid(rows, cols, cell, col, center, fill=0.06):
    """Build a VGroup grid of rounded cells centred at `center`."""
    g = VGroup()
    gap = cell * 0.14
    w = cols * cell + (cols - 1) * gap
    h = rows * cell + (rows - 1) * gap
    x0 = center[0] - w / 2 + cell / 2
    y0 = center[1] + h / 2 - cell / 2
    for r in range(rows):
        row_cells = VGroup()
        for c in range(cols):
            sq = RoundedRectangle(width=cell, height=cell, corner_radius=cell * 0.14,
                                  stroke_color=col, stroke_width=1.4,
                                  fill_color=col, fill_opacity=fill)
            sq.move_to([x0 + c * (cell + gap), y0 - r * (cell + gap), 0])
            row_cells.add(sq)
        g.add(row_cells)
    return g


class MatMul(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("The heart of AI: a matrix multiply", font=HEAD,
                     color=INK, weight="BOLD").scale(0.75).to_edge(UP, buff=0.4)
        self.play(Write(title, run_time=0.8))

        N = 5  # square matrices N x N
        cell = 0.52

        A = _grid(N, N, cell, VIOLET, [-4.6, 0.3, 0])
        B = _grid(N, N, cell, TEAL, [-0.6, 0.3, 0])
        C = _grid(N, N, cell, GREEN, [3.6, 0.3, 0])

        la = Text("A", font=MONO, color=VIOLET, weight="BOLD").scale(0.55)
        lb = Text("B", font=MONO, color=TEAL, weight="BOLD").scale(0.55)
        lc = Text("C", font=MONO, color=GREEN, weight="BOLD").scale(0.55)
        la.next_to(A, UP, buff=0.2)
        lb.next_to(B, UP, buff=0.2)
        lc.next_to(C, UP, buff=0.2)

        times = Text("x", font=MONO, color=SUB).scale(0.7).move_to([-2.6, 0.3, 0])
        eq = Text("=", font=MONO, color=SUB).scale(0.7).move_to([1.5, 0.3, 0])

        self.play(Create(A, run_time=0.7), Create(B, run_time=0.7),
                  Create(C, run_time=0.7))
        self.play(FadeIn(VGroup(la, lb, lc, times, eq), run_time=0.5))

        caption = Text(
            "a neural-network layer IS a matrix multiply - "
            "and a GPU is a matrix-multiply machine",
            font=MONO, color=SUB).scale(0.38)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, run_time=0.6))

        # ---------------- Master clock: parallel dot-product loop ---------
        clock = ValueTracker(0.0)
        period = 4.0

        def row_of(cell_idx):
            return cell_idx // N

        def col_of(cell_idx):
            return cell_idx % N

        def A_updater(m):
            t = clock.get_value()
            # which output cells are "active" this phase (several at once)
            step = int((t % period) / period * N) % N  # highlighted output row
            for r in range(N):
                for c in range(N):
                    sq = m[r][c]
                    on = (r == step)  # the row feeding current output tiles
                    sq.set_fill(VIOLET, opacity=0.6 if on else 0.06)
                    sq.set_stroke(VIOLET, opacity=1.0 if on else 0.5,
                                  width=2.4 if on else 1.4)

        def B_updater(m):
            t = clock.get_value()
            # columns pulse together (all cols feed in parallel)
            pulse = 0.5 + 0.5 * math.sin(t * 3.0)
            for r in range(N):
                for c in range(N):
                    sq = m[r][c]
                    sq.set_fill(TEAL, opacity=0.1 + 0.4 * pulse)
                    sq.set_stroke(TEAL, opacity=0.5 + 0.4 * pulse,
                                  width=1.4 + 1.0 * pulse)

        def C_updater(m):
            t = clock.get_value()
            step = int((t % period) / period * N) % N  # the output row being filled
            frac = ((t % period) / period * N) - step
            for r in range(N):
                for c in range(N):
                    sq = m[r][c]
                    if r < step or (r == step):
                        # computed (or computing) tiles: MANY at once in a row
                        glow = 0.5 + 0.5 * math.sin(t * 5.0 + c)
                        active = (r == step)
                        sq.set_fill(GREEN, opacity=(0.3 + 0.5 * glow) if active
                                    else 0.5)
                        sq.set_stroke(GREEN,
                                      opacity=1.0 if active else 0.8,
                                      width=(2.0 + 2.0 * glow) if active else 2.0)
                    else:
                        sq.set_fill(GREEN, opacity=0.06)
                        sq.set_stroke(GREEN, opacity=0.4, width=1.4)

        A.add_updater(A_updater)
        B.add_updater(B_updater)
        C.add_updater(C_updater)

        # run the compute loop for a while before revealing tensor cores
        self.play(clock.animate.set_value(8.0), run_time=8.0,
                  rate_func=rate_functions.linear)

        # ---------------- TENSOR CORES: matrix specialists ----------------
        tc_glow = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.14,
                                   stroke_color=VIOLET, stroke_width=14,
                                   fill_opacity=0.0).set_stroke(opacity=0.22)
        tc = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.12,
                              stroke_color=VIOLET, stroke_width=2.5,
                              fill_color=VIOLET, fill_opacity=0.12)
        tc_t1 = Text("TENSOR CORES", font=MONO, color=INK,
                     weight="BOLD").scale(0.46)
        tc_t2 = Text("matrix specialists", font=MONO, color=VIOLET).scale(0.36)
        tc_t1.shift(UP * 0.22)
        tc_t2.next_to(tc_t1, DOWN, buff=0.12)
        tensor = VGroup(tc_glow, tc, tc_t1, tc_t2).move_to([-0.6, -2.35, 0])
        self.play(FadeIn(tensor, run_time=0.7))

        def tensor_updater(m):
            t = clock.get_value()
            pulse = 0.5 + 0.5 * math.sin(t * 4.0)
            glow, box = m[0], m[1]
            glow.set_stroke(VIOLET, opacity=0.18 + 0.4 * pulse)
            box.set_stroke(VIOLET, width=2.5 + 1.5 * pulse)
            box.set_fill(VIOLET, opacity=0.1 + 0.1 * pulse)

        tensor.add_updater(tensor_updater)

        self.play(clock.animate.set_value(18.0), run_time=10.0,
                  rate_func=rate_functions.linear)

        # Clean final frame.
        A.clear_updaters()
        B.clear_updaters()
        C.clear_updaters()
        tensor.clear_updaters()
        for r in range(N):
            for c in range(N):
                C[r][c].set_fill(GREEN, opacity=0.55)
                C[r][c].set_stroke(GREEN, opacity=0.9, width=2.0)
        self.wait(0.3)
