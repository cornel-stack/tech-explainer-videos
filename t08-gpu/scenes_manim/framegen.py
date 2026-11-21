"""Scene: frame generation — inserted frames between real ones.

Class `Framegen` (~18s). A horizontal filmstrip of frames scrolls continuously
leftward. Real frames are solid teal ("REAL"); between each pair an inserted
frame is dashed violet ("AI FRAME"). Label "2 real -> 1 generated". A coral
latency arrow below grows with a "+latency" tag. Caption warns it is smoother
motion, not more real speed. Continuous scroll via a master ValueTracker.

Dark palette only, TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  red #FF5C47  teal #2DD4BF  violet #B06BFF  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Text,
    VGroup,
    Line,
    DashedVMobject,
    ValueTracker,
    config,
    FadeIn,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    rate_functions,
)

BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
GREEN = "#76D64A"
RED = "#FF5C47"
TEAL = "#2DD4BF"
VIOLET = "#B06BFF"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Framegen(Scene):
    def construct(self):
        title = Text("Frame generation", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        strip_y = 0.6
        FW, FH = 1.3, 1.7       # frame width/height
        GAP = 0.45
        PITCH = FW + GAP        # spacing between frame centers
        N = 12                  # frames alive in the strip
        SPAN_LEFT = -9.0
        SPAN_RIGHT = 9.0

        # Build frames. Every other frame (odd index) is an AI frame.
        frames = []
        for i in range(N):
            is_ai = (i % 2 == 1)
            if is_ai:
                base = Rectangle(width=FW, height=FH, stroke_color=VIOLET,
                                 stroke_width=2.5, fill_opacity=0)
                body = DashedVMobject(base, num_dashes=28, dashed_ratio=0.55)
                body.set_stroke(VIOLET, width=2.5)
                lbl = Text("AI FRAME", font=MONO, color=VIOLET).scale(0.24)
                fill = Rectangle(width=FW, height=FH, stroke_width=0,
                                 fill_color="#160F24", fill_opacity=0.55)
            else:
                body = Rectangle(width=FW, height=FH, stroke_color=TEAL,
                                 stroke_width=2.5, fill_color="#0C1917",
                                 fill_opacity=0.9)
                lbl = Text("REAL", font=MONO, color=TEAL,
                           weight="BOLD").scale(0.26)
                fill = None
            grp = VGroup()
            if fill is not None:
                grp.add(fill)
            grp.add(body)
            lbl.move_to([0, 0, 0])
            grp.add(lbl)
            grp.is_ai = is_ai
            grp.base_i = i
            frames.append(grp)
            self.add(grp)

        # Static labels / caption.
        ratio = Text("2 real -> 1 generated", font=HEAD,
                     color=SILVER).scale(0.36)
        ratio.next_to(title, DOWN, buff=0.2)

        cap = Text("smoother motion — not more real speed; "
                   "off for competitive.", font=HEAD, color=SECOND).scale(0.3)
        cap.to_edge(DOWN, buff=0.4)

        # Latency arrow (coral) below the strip with +latency tag.
        lat_base_y = -1.9
        lat_line = Line([SPAN_LEFT * 0.3, lat_base_y, 0],
                        [SPAN_LEFT * 0.3 + 0.1, lat_base_y, 0],
                        stroke_color=RED, stroke_width=5)
        lat_tag = Text("+latency", font=MONO, color=RED).scale(0.3)

        self.play(FadeIn(ratio), FadeIn(cap, shift=UP * 0.2), run_time=0.5)
        self.add(lat_line, lat_tag)

        # =====================================================================
        # CONTINUOUS SCROLL PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        SPEED = 1.6  # units/sec leftward

        for grp in frames:
            def make_scroll(g):
                i0 = g.base_i
                total_span = SPAN_RIGHT - SPAN_LEFT

                def _upd(m):
                    x0 = SPAN_RIGHT - i0 * PITCH
                    x = x0 - SPEED * t.get_value()
                    # Wrap so the strip loops forever.
                    x = SPAN_LEFT + ((x - SPAN_LEFT) % total_span)
                    g.move_to([x, strip_y, 0])
                    # Fade near the edges.
                    edge = min((x - SPAN_LEFT), (SPAN_RIGHT - x)) / 2.0
                    g.set_opacity(np.clip(edge, 0.0, 1.0))
                return _upd
            grp.add_updater(make_scroll(grp))

        # Latency arrow grows then holds (pulsing) to signal added lag.
        def lat_upd(m):
            tt = t.get_value()
            grow = min(tt / 4.0, 1.0)
            length = 0.1 + grow * 3.2
            pulse = 1.0 + 0.06 * np.sin(tt * 4.0)
            x0 = -2.4
            m.put_start_and_end_on([x0, lat_base_y, 0],
                                   [x0 + length * pulse, lat_base_y, 0])
        lat_line.add_updater(lat_upd)

        def tag_upd(m):
            m.next_to(lat_line.get_end(), RIGHT, buff=0.18)
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 3.0)))
        lat_tag.add_updater(tag_upd)

        self.play(t.animate.set_value(14.0), run_time=14.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
