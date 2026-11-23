"""Scene: attention — each word reads its context.

Class `Attention` (~18s). A row of token pills; focus on the word "bank".
AMBER attention links light up from "bank" to context words ("river" vs
"savings") with varying thickness/weight; every token attends to every other
(a faint all-to-all mesh pulses). Caption: "attention: each word reads its
context".

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


class Attention(Scene):
    def construct(self):
        title = Text("Attention reads context", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- row of token pills ---------------------------------------------
        words = ["by", "the", "river", "bank", "near", "the", "savings"]
        focus_idx = 3  # "bank"
        strong_ctx = {2, 6}  # river, savings
        base_y = 1.2
        pills = []
        tmp = []
        total_w = 0
        for w in words:
            p = token_pill(w, TEAL)
            tmp.append(p)
            total_w += p.width + 0.2
        total_w -= 0.2
        x = -total_w / 2
        for i, p in enumerate(tmp):
            p.move_to([x + p.width / 2, base_y, 0])
            x += p.width + 0.2
            pills.append(p)
        self.play(*[FadeIn(p, shift=DOWN * 0.2) for p in pills],
                  lag_ratio=0.08, run_time=1.1)

        # highlight focus word "bank"
        focus = pills[focus_idx]
        focus_lbl = Text("focus", font=MONO, color=AMBER).scale(0.26)
        focus_lbl.next_to(focus, UP, buff=0.18)
        self.play(focus[0].animate.set_stroke(AMBER, width=3).set_fill(
            AMBER, opacity=0.14), focus[1].animate.set_color(AMBER),
            FadeIn(focus_lbl), run_time=0.7)

        centers = [p.get_center() for p in pills]

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # --- faint all-to-all mesh (every token attends to every other) ----
        mesh = VGroup()
        mesh_pairs = []
        n = len(pills)
        for i in range(n):
            for j in range(i + 1, n):
                ln = Line(centers[i] + DOWN * 0.32, centers[j] + DOWN * 0.32,
                          stroke_color=SECOND, stroke_width=1,
                          stroke_opacity=0.12)
                mesh.add(ln)
                mesh_pairs.append((i, j, ln))
        self.add(mesh)

        for k, (i, j, ln) in enumerate(mesh_pairs):
            def make_mesh(line, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(1.8 * t.get_value() + phase)
                    line.set_stroke(opacity=0.05 + 0.14 * s)
                return _upd
            ln.add_updater(make_mesh(ln, k * 0.35))

        mesh_lbl = Text("every token attends to every other", font=MONO,
                        color=SECOND).scale(0.26)
        mesh_lbl.move_to([0, -0.4, 0])
        mesh_lbl.add_updater(lambda m: m.set_opacity(
            0.4 + 0.4 * (0.5 + 0.5 * np.sin(1.8 * t.get_value()))))
        self.add(mesh_lbl)

        # --- AMBER attention links from "bank" to all context --------------
        # weight toward strong context words (river, savings)
        fc = centers[focus_idx]
        links = []
        for i in range(n):
            if i == focus_idx:
                continue
            base_weight = 0.9 if i in strong_ctx else 0.3
            ln = Line(fc, centers[i], stroke_color=AMBER,
                      stroke_width=2 + 6 * base_weight,
                      stroke_opacity=0.2)
            links.append((i, ln, base_weight))
            self.add(ln)

        # animate: weight pulses; strong links clearly thicker/brighter
        for idx, (i, ln, bw) in enumerate(links):
            end_pt = centers[i]

            def make_link(line, weight, target, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.4 * t.get_value() + phase)
                    w = 1.5 + (2 + 7 * weight) * (0.5 + 0.5 * s)
                    line.set_stroke(width=w)
                    line.set_stroke(opacity=0.15 + 0.7 * weight * (
                        0.4 + 0.6 * s))
                return _upd
            ln.add_updater(make_link(ln, bw, end_pt, idx * 0.5))

        # weight readout labels on strong context words
        weight_lbls = []
        for i in strong_ctx:
            wl = Text("high", font=MONO, color=AMBER).scale(0.24)
            wl.next_to(pills[i], DOWN, buff=0.5)
            wl.add_updater(lambda m: m.set_opacity(
                0.5 + 0.5 * (0.5 + 0.5 * np.sin(2.4 * t.get_value()))))
            weight_lbls.append(wl)
            self.add(wl)

        # focus pill breathes amber
        focus[0].add_updater(lambda m: m.set_stroke(
            AMBER,
            width=3 + 1.5 * (0.5 + 0.5 * np.sin(2.4 * t.get_value()))))
        focus_lbl.add_updater(lambda m: m.set_opacity(
            0.5 + 0.5 * (0.5 + 0.5 * np.sin(2.4 * t.get_value()))))

        # context pills gently pulse teal
        for i, p in enumerate(pills):
            if i == focus_idx:
                continue
            def make_ctx(box, phase, strong):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.0 * t.get_value() + phase)
                    col = AMBER if strong else TEAL
                    box.set_stroke(
                        interpolate_color(ManimColor(TEAL), ManimColor(AMBER),
                                          (0.6 * s) if strong else 0.0),
                        opacity=0.5 + 0.4 * s)
                return _upd
            p[0].add_updater(make_ctx(p[0], i * 0.7, i in strong_ctx))

        # caption
        cap = Text("attention: each word reads its context",
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
