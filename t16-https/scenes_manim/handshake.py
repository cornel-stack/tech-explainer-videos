"""Scene: the TLS handshake as a sequence diagram.

Class `Handshake` (~20s). Two vertical lifelines — "Browser" (left) and
"Server" (right) — with time flowing downward. Messages travel between them in
order and loop: ClientHello, Certificate (public key), key exchange, both
derive one session key, then GREEN encrypted data flowing both ways. Each arrow
lights as it fires.

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    Text,
    VGroup,
    Line,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
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


class Handshake(Scene):
    def construct(self):
        title = Text("The TLS handshake, step by step", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- lifelines -------------------------------------------------------
        x_left, x_right = -4.2, 4.2
        y_top, y_bot = 2.4, -3.0
        head_b = Text("Browser", font=MONO, color=TEAL, weight="BOLD").scale(0.38)
        head_b.move_to([x_left, y_top + 0.35, 0])
        head_s = Text("Server", font=MONO, color=AMBER, weight="BOLD").scale(0.38)
        head_s.move_to([x_right, y_top + 0.35, 0])
        life_b = Line([x_left, y_top, 0], [x_left, y_bot, 0],
                      stroke_color=TEAL, stroke_width=2, stroke_opacity=0.5)
        life_s = Line([x_right, y_top, 0], [x_right, y_bot, 0],
                      stroke_color=AMBER, stroke_width=2, stroke_opacity=0.5)

        self.play(FadeIn(head_b), FadeIn(head_s),
                  Create(life_b), Create(life_s), run_time=0.8)

        # --- the ordered steps ----------------------------------------------
        # (y, direction, label, color)  direction +1 = left->right
        steps = [
            (1.8, +1, "ClientHello →", TEAL),
            (0.9, -1, "← Certificate (public key)", AMBER),
            (0.0, +1, "⇄ key exchange", VIOLET),
            (-0.9, 0, "✓ both derive one session key", GREEN),
            (-1.9, 2, "\U0001f512 encrypted data ⇄", GREEN),
        ]

        rows = []
        for y, _dir, label, col in steps:
            arrow = Line([x_left, y, 0], [x_right, y, 0],
                         stroke_color=SECOND, stroke_width=2, stroke_opacity=0.25)
            lbl = Text(label, font=MONO, color=SECOND).scale(0.3)
            lbl.move_to([0, y + 0.3, 0])
            self.add(arrow, lbl)
            rows.append((y, _dir, col, arrow, lbl))

        # travelling packet dots (reused per fire)
        packet = Dot(radius=0.11, color=TEAL)
        packet.set_opacity(0)
        packet2 = Dot(radius=0.11, color=GREEN)
        packet2.set_opacity(0)
        self.add(packet, packet2)

        caption = Text("slow secure setup, then fast secure chat", font=HEAD,
                       color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 20.0
        n_steps = len(steps)
        step_dur = 2.0            # each step occupies 2s
        cycle = n_steps * step_dur  # 10s full sequence, loops twice

        def active_step(tt):
            local = tt % cycle
            return int(local // step_dur), (local % step_dur) / step_dur

        # arrows light when their step is active, fade once passed
        def make_row(idx, y, col, arrow, lbl):
            def _upd_arrow(m):
                tt = t.get_value()
                ai, frac = active_step(tt)
                if ai == idx:
                    glow = 0.3 + 0.7 * np.sin(np.pi * frac)
                    c = interpolate_color(ManimColor(SECOND), ManimColor(col),
                                          glow)
                    m.set_stroke(c, width=2 + 3 * glow, opacity=0.4 + 0.6 * glow)
                elif ai > idx:
                    m.set_stroke(ManimColor(col), width=2, opacity=0.5)
                else:
                    m.set_stroke(ManimColor(SECOND), width=2, opacity=0.2)

            def _upd_lbl(m):
                tt = t.get_value()
                ai, frac = active_step(tt)
                if ai == idx:
                    g = 0.4 + 0.6 * np.sin(np.pi * frac)
                    m.set_color(interpolate_color(ManimColor(SECOND),
                                                  ManimColor(col), g))
                    m.set_opacity(0.6 + 0.4 * g)
                elif ai > idx:
                    m.set_color(ManimColor(col))
                    m.set_opacity(0.85)
                else:
                    m.set_color(ManimColor(SECOND))
                    m.set_opacity(0.3)
            return _upd_arrow, _upd_lbl

        for i, (y, _dir, col, arrow, lbl) in enumerate(rows):
            ua, ul = make_row(i, y, col, arrow, lbl)
            arrow.add_updater(ua)
            lbl.add_updater(ul)

        # packet motion along the active arrow
        def packet_upd(m):
            tt = t.get_value()
            ai, frac = active_step(tt)
            y, _dir, col, _arrow, _lbl = rows[ai]
            if _dir in (+1, 2):
                x = x_left + (x_right - x_left) * frac
            elif _dir == -1:
                x = x_right + (x_left - x_right) * frac
            else:  # 0 => shuttle both ways (key exchange / derive)
                x = x_left + (x_right - x_left) * (0.5 - 0.5 * np.cos(2 * np.pi * frac))
            m.move_to([x, y, 0])
            m.set_color(ManimColor(col))
            m.set_opacity(np.sin(np.pi * frac))
        packet.add_updater(packet_upd)

        # second packet: only for the final encrypted-both-ways row
        def packet2_upd(m):
            tt = t.get_value()
            ai, frac = active_step(tt)
            y, _dir, col, _arrow, _lbl = rows[ai]
            if _dir == 2:  # encrypted data both ways -> second dot goes R->L
                x = x_right + (x_left - x_right) * frac
                m.move_to([x, y, 0])
                m.set_color(ManimColor(GREEN))
                m.set_opacity(np.sin(np.pi * frac))
            else:
                m.set_opacity(0)
        packet2.add_updater(packet2_upd)

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
