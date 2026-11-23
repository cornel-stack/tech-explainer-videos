"""Scene: HTTPS everywhere.

Class `Modern` (~18s). Two address bars contrast "Not secure — http://" (CORAL)
with "https://" (GREEN). Then a round-trip timeline shows TLS 1.2 taking two
round trips versus TLS 1.3 taking one (1.3 clearly faster). Finally the padlock
icon pulses then fades with "secure is now the default".

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


class Modern(Scene):
    def construct(self):
        title = Text("Secure is now the default", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- two address bars ------------------------------------------------
        bar_http = RoundedRectangle(corner_radius=0.2, width=5.0, height=0.8,
                                    stroke_color=CORAL, stroke_width=3,
                                    fill_color="#1A0F0C", fill_opacity=0.95)
        bar_http.move_to([-3.4, 2.0, 0])
        http_t = Text("⚠ Not secure — http://", font=MONO, color=CORAL).scale(0.32)
        http_t.move_to(bar_http.get_center())

        bar_https = RoundedRectangle(corner_radius=0.2, width=5.0, height=0.8,
                                     stroke_color=GREEN, stroke_width=3,
                                     fill_color="#0C1A12", fill_opacity=0.95)
        bar_https.move_to([3.4, 2.0, 0])
        https_t = Text("\U0001f512 https://", font=MONO, color=GREEN).scale(0.32)
        https_t.move_to(bar_https.get_center())

        self.play(FadeIn(bar_http), FadeIn(http_t),
                  FadeIn(bar_https), FadeIn(https_t), run_time=0.7)

        # --- round-trip timelines: TLS 1.2 (2 RTT) vs 1.3 (1 RTT) -----------
        # client lifeline left, server lifeline right, for each version
        def lifelines(y, label, col):
            xl, xr = -4.5, 4.5
            cl = Line([xl, y + 0.45, 0], [xl, y - 0.45, 0],
                      stroke_color=col, stroke_width=2, stroke_opacity=0.5)
            sr = Line([xr, y + 0.45, 0], [xr, y - 0.45, 0],
                      stroke_color=col, stroke_width=2, stroke_opacity=0.5)
            lab = Text(label, font=MONO, color=col, weight="BOLD").scale(0.3)
            lab.move_to([xl - 1.1, y, 0])
            cdot = Text("client", font=MONO, color=SECOND).scale(0.2)
            cdot.move_to([xl, y + 0.6, 0])
            sdot = Text("server", font=MONO, color=SECOND).scale(0.2)
            sdot.move_to([xr, y + 0.6, 0])
            return VGroup(cl, sr, lab, cdot, sdot), xl, xr

        g12, xl, xr = lifelines(0.5, "TLS 1.2", CORAL)
        g13, _, _ = lifelines(-1.8, "TLS 1.3", GREEN)
        self.play(FadeIn(g12), FadeIn(g13), run_time=0.6)

        rtt12 = Text("two round trips", font=HEAD, color=CORAL).scale(0.3)
        rtt12.move_to([0, 1.15, 0])
        rtt13 = Text("one round trip — faster", font=HEAD, color=GREEN).scale(0.3)
        rtt13.move_to([0, -1.15, 0])
        self.add(rtt12, rtt13)

        # travelling packets
        p12 = Dot(radius=0.1, color=CORAL)
        p13 = Dot(radius=0.1, color=GREEN)
        p12.set_opacity(0)
        p13.set_opacity(0)
        self.add(p12, p13)

        caption = Text("encryption protects the pipe — not your judgement",
                       font=HEAD, color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # final padlock
        padlock = Text("\U0001f512", color=GREEN).scale(1.4)
        padlock.move_to([0, -1.8, 0])
        padlock.set_opacity(0)
        self.add(padlock)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 18.0
        loop = 6.0
        y12, y13 = 0.5, -1.8

        # 1.2 takes 2 RTT -> packet bounces L->R->L->R across 2 cycles in `loop`
        def p12_upd(m):
            tt = t.get_value() % loop
            frac = tt / loop  # 0..1 over whole loop = 2 full round trips
            # 2 round trips => 4 legs
            leg = (frac * 4.0) % 4.0
            seg = int(leg)
            s = leg - seg
            if seg == 0:
                x = xl + (xr - xl) * s
            elif seg == 1:
                x = xr + (xl - xr) * s
            elif seg == 2:
                x = xl + (xr - xl) * s
            else:
                x = xr + (xl - xr) * s
            m.move_to([x, y12, 0])
            m.set_color(ManimColor(CORAL))
            m.set_opacity(1.0)
        p12.add_updater(p12_upd)

        # 1.3 takes 1 RTT -> one L->R->L in first half, then idle (done sooner)
        def p13_upd(m):
            tt = t.get_value() % loop
            frac = tt / loop
            if frac < 0.5:
                leg = (frac * 4.0)  # 0..2 => 2 legs in first half
                seg = int(leg)
                s = leg - seg
                if seg == 0:
                    x = xl + (xr - xl) * s
                else:
                    x = xr + (xl - xr) * s
                m.move_to([x, y13, 0])
                m.set_color(ManimColor(GREEN))
                m.set_opacity(1.0)
            else:
                # finished: sit at client, dim (secure chat already flowing)
                m.move_to([xl, y13, 0])
                m.set_opacity(0.3)
        p13.add_updater(p13_upd)

        # address bars pulse
        def http_pulse(m):
            tt = t.get_value()
            p = 0.5 + 0.5 * np.sin(2.5 * tt)
            m.set_stroke(CORAL, width=3 + 2 * p)
        bar_http.add_updater(http_pulse)

        def https_pulse(m):
            tt = t.get_value()
            p = 0.5 + 0.5 * np.sin(2.5 * tt + 1.0)
            m.set_stroke(GREEN, width=3 + 2 * p)
        bar_https.add_updater(https_pulse)

        # final padlock: pulses, fades out, returns (loop of `loop` seconds)
        def padlock_upd(m):
            tt = t.get_value() % loop
            # visible & pulsing first 4s, fade out 4-5, return 5-6
            if tt < 4.0:
                op = (0.75 + 0.25 * np.sin(5 * tt))
            elif tt < 5.0:
                op = 0.75 * (1 - (tt - 4.0))
            else:
                op = 0.75 * (tt - 5.0)
            m.set_opacity(float(np.clip(op, 0.0, 1.0)))
        padlock.add_updater(padlock_upd)

        # default note next to padlock
        default_note = Text("secure is now the default", font=MONO,
                            color=GREEN).scale(0.28)
        default_note.next_to(padlock, RIGHT, buff=0.3)
        self.add(default_note)

        def note_upd(m):
            tt = t.get_value() % loop
            if tt < 4.0:
                op = 0.9
            elif tt < 5.0:
                op = 0.9 * (1 - (tt - 4.0))
            else:
                op = 0.9 * (tt - 5.0)
            m.set_opacity(float(np.clip(op, 0.0, 1.0)))
        default_note.add_updater(note_upd)

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
