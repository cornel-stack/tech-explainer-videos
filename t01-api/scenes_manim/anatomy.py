"""Anatomy scene for "What Is an API?".

Concept: take one API call apart. A REQUEST is built from an address + a
method; it points at a RESPONSE built from a status, headers, and a body.

Dark design system (shared with the Remotion video):
  bg      #0A0A0C
  ink     warm cream #EDE7DB   secondary #9A958C
  accents amber #FFC24B, magenta #FF3E7F, mint #3DE0B0,
          violet #B06BFF, coral #FF6B4A, gold #E8C24A
  (NO blue, NO pure white)

Rendered at 1920x1080. No external assets. The diagram assembles in sequence
over ~13s, then holds with a soft pulse on each chip. Runtime ~28 seconds.
"""

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Arrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    smooth,
    there_and_back,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

# ---- Dark palette ------------------------------------------------------------
BG = "#0A0A0C"
INK = "#EDE7DB"
INK_SOFT = "#9A958C"

AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

FONT = "Inter"


def glow_chip(label, color, width=3.6, height=0.9, font_size=26,
              font="mono"):
    """A rounded accent chip with a simulated glow and a centred label."""
    halo = RoundedRectangle(
        corner_radius=0.18, width=width, height=height,
        stroke_color=color, stroke_width=10, stroke_opacity=0.16,
        fill_opacity=0.0,
    )
    body = RoundedRectangle(
        corner_radius=0.18, width=width, height=height,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.10,
    )
    txt = Text(label, font=FONT, font_size=font_size, color=INK)
    txt.move_to(body.get_center())
    return VGroup(halo, body, txt)


def role_label(text):
    """Small secondary cream label describing a part's role."""
    return Text(text, font=FONT, font_size=18, color=INK_SOFT)


def section_title(text, color):
    return Text(text, font=FONT, font_size=30, color=color)


class Anatomy(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Column anchors --------------------------------------------------
        left_x = LEFT * 4.3
        right_x = RIGHT * 4.3

        # --- LEFT: REQUEST title --------------------------------------------
        req_title = section_title("REQUEST", AMBER)
        req_title.move_to(left_x + UP * 2.9)
        self.play(FadeIn(req_title, shift=DOWN * 0.2), run_time=0.7)

        # Two request chips fly in (address + method).
        addr = glow_chip("api.weather.gov/points", AMBER, width=4.3,
                         height=0.9, font_size=24)
        addr.move_to(left_x + UP * 1.4)
        addr_role = role_label("where you're asking")
        addr_role.next_to(addr, DOWN, buff=0.16)

        method = glow_chip("GET", AMBER, width=1.8, height=0.9, font_size=28)
        method.move_to(left_x + DOWN * 0.1 + LEFT * 1.25)
        method_role = role_label("what you want done")
        method_role.next_to(method, RIGHT, buff=0.4)

        self.play(FadeIn(addr, shift=RIGHT * 0.6), run_time=0.7)
        self.play(FadeIn(addr_role), run_time=0.4)
        self.play(FadeIn(method, shift=LEFT * 0.6), run_time=0.7)
        self.play(FadeIn(method_role), run_time=0.4)

        # --- The bold arrow REQUEST -> RESPONSE -----------------------------
        arrow = Arrow(
            start=left_x + RIGHT * 2.5 + DOWN * 0.3,
            end=right_x + LEFT * 2.9 + DOWN * 0.3,
            color=INK,
            stroke_width=6,
            buff=0.2,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(GrowArrow(arrow), run_time=0.9)

        # --- RIGHT: RESPONSE title ------------------------------------------
        resp_title = section_title("RESPONSE", MINT)
        resp_title.move_to(right_x + UP * 2.9)
        self.play(FadeIn(resp_title, shift=DOWN * 0.2), run_time=0.7)

        # Three stacked response chips assemble in sequence.
        status = glow_chip("200 OK", MINT, width=3.4, height=0.85,
                           font_size=26)
        headers = glow_chip("headers", GOLD, width=3.4, height=0.85,
                            font_size=26)
        body = glow_chip("{ body: JSON }", CORAL, width=3.4, height=0.85,
                         font_size=26)

        stack = VGroup(status, headers, body).arrange(DOWN, buff=0.4)
        stack.move_to(right_x + DOWN * 0.1)

        status_role = role_label("did it work?")
        status_role.next_to(status, RIGHT, buff=0.35)
        headers_role = role_label("about the answer")
        headers_role.next_to(headers, RIGHT, buff=0.35)
        body_role = role_label("the actual data")
        body_role.next_to(body, RIGHT, buff=0.35)

        self.play(FadeIn(status, shift=UP * 0.3),
                  FadeIn(status_role), run_time=0.7)
        self.play(FadeIn(headers, shift=UP * 0.3),
                  FadeIn(headers_role), run_time=0.7)
        self.play(FadeIn(body, shift=UP * 0.3),
                  FadeIn(body_role), run_time=0.7)

        self.wait(0.6)

        # --- HOLD: soft pulse sweeps across each chip, looping --------------
        all_chips = [addr, method, status, headers, body]

        for _ in range(3):
            for chip in all_chips:
                self.play(
                    chip[1].animate.set_fill(opacity=0.26),
                    rate_func=there_and_back,
                    run_time=0.45,
                )
            # Gentle breath on the connecting arrow between sweeps.
            self.play(
                arrow.animate.set_stroke(opacity=0.5),
                rate_func=there_and_back,
                run_time=0.8,
            )
            self.wait(0.4)

        self.wait(1.0)
