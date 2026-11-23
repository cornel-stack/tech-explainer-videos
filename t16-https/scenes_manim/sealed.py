"""Scene: the encrypted tunnel.

Class `Sealed` (~18s). Browser (left) <-> Server (right) joined by a pipe.
Before the session key, readable text flows. After a "session key" marker the
text in the pipe becomes scrambled gibberish. An eavesdropper on café Wi-Fi taps
the pipe but sees only noise (CORAL "???"). A tamper attempt flips a bit and an
integrity check ✗ rejects it (CORAL flash).

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
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

_GLYPHS = "@#$%&*+=?/\\<>{}[]~^0123456789abcdef"
_WORDS = ["GET /login", "user=amal", "balance", "transfer $50", "cookie=ab12"]


class Sealed(Scene):
    def construct(self):
        title = Text("Inside the encrypted tunnel", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- endpoints + pipe ------------------------------------------------
        yp = 0.3
        bx = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.3,
                              stroke_color=TEAL, stroke_width=2.5,
                              fill_color="#0C1A18", fill_opacity=0.9)
        bx.move_to([-5.2, yp, 0])
        b_lbl = Text("Browser", font=MONO, color=TEAL).scale(0.3)
        b_lbl.move_to(bx.get_center())
        sx = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.3,
                              stroke_color=AMBER, stroke_width=2.5,
                              fill_color="#1A1708", fill_opacity=0.9)
        sx.move_to([5.2, yp, 0])
        s_lbl = Text("Server", font=MONO, color=AMBER).scale(0.3)
        s_lbl.move_to(sx.get_center())

        pipe_l, pipe_r = -4.1, 4.1
        pipe_top = Line([pipe_l, yp + 0.5, 0], [pipe_r, yp + 0.5, 0],
                        stroke_color=SECOND, stroke_width=2, stroke_opacity=0.5)
        pipe_bot = Line([pipe_l, yp - 0.5, 0], [pipe_r, yp - 0.5, 0],
                        stroke_color=SECOND, stroke_width=2, stroke_opacity=0.5)

        self.play(Create(bx), Create(sx), FadeIn(b_lbl), FadeIn(s_lbl),
                  Create(pipe_top), Create(pipe_bot), run_time=0.8)

        # --- session key marker ---------------------------------------------
        key_marker = Text("\U0001f512 session key", font=MONO, color=GREEN).scale(0.3)
        key_marker.move_to([0, yp + 1.15, 0])
        self.add(key_marker)

        # --- eavesdropper (café Wi-Fi) --------------------------------------
        eve = RoundedRectangle(corner_radius=0.1, width=2.1, height=0.9,
                               stroke_color=CORAL, stroke_width=2,
                               fill_color="#1A0F0C", fill_opacity=0.9)
        eve.move_to([0, -2.3, 0])
        eve_lbl = Text("café Wi-Fi\neavesdropper", font=MONO, color=CORAL).scale(0.24)
        eve_lbl.move_to(eve.get_center())
        tap = Line([0, yp - 0.5, 0], eve.get_top(), stroke_color=CORAL,
                   stroke_width=2, stroke_opacity=0.5)
        eve_sees = Text("???", font=MONO, color=CORAL, weight="BOLD").scale(0.4)
        eve_sees.next_to(eve, DOWN, buff=0.15)
        self.add(eve, eve_lbl, tap, eve_sees)

        caption = Text("private + tamper-evident", font=HEAD,
                       color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # mode banner
        banner = Text("", font=MONO, color=GREEN).scale(0.3)
        banner.next_to(title, DOWN, buff=0.18)
        self.add(banner)

        # --- flowing text packets inside the pipe ---------------------------
        n_pk = 5
        period = 4.0
        packets = []
        for k in range(n_pk):
            txt = Text("GET /login", font=MONO, color=INK).scale(0.26)
            txt.move_to([0, yp, 0])
            packets.append(txt)
            self.add(txt)

        # tamper indicator
        tamper = Text("integrity check ✗", font=MONO, color=CORAL,
                      weight="BOLD").scale(0.32)
        tamper.move_to([0, yp + 1.15, 0])
        tamper.set_opacity(0)
        self.add(tamper)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 18.0
        # phases within a 9s loop: 0-3 readable, 3-6 encrypted, 6-9 tamper rejected
        loop = 9.0

        def phase_of(tt):
            p = tt % loop
            if p < 3.0:
                return "readable"
            elif p < 6.0:
                return "encrypted"
            else:
                return "tamper"

        def banner_upd(m):
            ph = phase_of(t.get_value())
            if ph == "readable":
                word, col = "before the key — readable", CORAL
            elif ph == "encrypted":
                word, col = "after the key — scrambled", GREEN
            else:
                word, col = "tamper attempt — rejected", CORAL
            if m.text != word:
                new = Text(word, font=MONO, color=col).scale(0.3)
                new.move_to(m)
                m.become(new)
        banner.add_updater(banner_upd)

        def make_packet(txt, kk):
            offset = kk * (period / n_pk)

            def _upd(m):
                tt = t.get_value()
                ph = phase_of(tt)
                local = (tt + offset) % period
                frac = local / period
                x = pipe_l + (pipe_r - pipe_l) * frac
                m.move_to([x, yp, 0])
                edge = min(frac, 1 - frac) * 5.0
                op = float(np.clip(edge, 0.0, 1.0))

                if ph == "readable":
                    content = _WORDS[kk % len(_WORDS)]
                    col = INK
                else:
                    # scrambled gibberish, reshuffled over time
                    seed = int(tt * 4) + kk
                    rr = np.random.default_rng(seed)
                    content = "".join(_GLYPHS[rr.integers(0, len(_GLYPHS))]
                                      for _ in range(8))
                    col = GREEN
                new = Text(content, font=MONO, color=col).scale(0.26)
                new.move_to([x, yp, 0])
                new.set_opacity(op)
                m.become(new)
            return _upd

        for kk, txt in enumerate(packets):
            txt.add_updater(make_packet(txt, kk))

        # eavesdropper tap + "???" only ever shows noise
        def tap_upd(m):
            tt = t.get_value()
            p = 0.5 + 0.5 * np.sin(3 * tt)
            m.set_stroke(CORAL, opacity=0.3 + 0.4 * p)
        tap.add_updater(tap_upd)

        def eve_sees_upd(m):
            tt = t.get_value()
            seed = int(tt * 5)
            rr = np.random.default_rng(seed)
            content = "".join(_GLYPHS[rr.integers(0, len(_GLYPHS))]
                              for _ in range(4))
            if m.text != content:
                new = Text(content, font=MONO, color=CORAL,
                           weight="BOLD").scale(0.34)
                new.next_to(eve, DOWN, buff=0.15)
                m.become(new)
        eve_sees.add_updater(eve_sees_upd)

        # key marker glows green during encrypted phase
        def key_upd(m):
            ph = phase_of(t.get_value())
            if ph in ("encrypted", "tamper"):
                m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(4 * t.get_value())))
            else:
                m.set_opacity(0.25)
        key_marker.add_updater(key_upd)

        # tamper rejection flash during tamper phase
        def tamper_upd(m):
            tt = t.get_value()
            if phase_of(tt) == "tamper":
                local = tt % loop - 6.0  # 0..3
                flash = abs(np.sin(3 * local))
                m.set_opacity(flash)
            else:
                m.set_opacity(0)
        tamper.add_updater(tamper_upd)

        def eve_box_upd(m):
            tt = t.get_value()
            m.set_stroke(CORAL, width=2 + 1.5 * (0.5 + 0.5 * np.sin(2.5 * tt)))
        eve.add_updater(eve_box_upd)

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
