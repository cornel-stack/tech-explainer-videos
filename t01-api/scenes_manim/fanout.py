"""FanOut scene for "What Is an API?".

Concept: a flight-search "fan-out". One client (Flight Search) asks many
airline APIs the same question at once, each answers, and the answers are
merged into a single results list.

Dark design system (shared with the Remotion video):
  bg      #0A0A0C
  ink     warm cream #EDE7DB   secondary #9A958C
  accents amber #FFC24B, magenta #FF3E7F, mint #3DE0B0,
          violet #B06BFF, coral #FF6B4A, gold #E8C24A
  (NO blue, NO pure white)

Rendered at 1920x1080. No external assets — everything is a Manim primitive.
Builds over ~12s then holds with looping fan-out pulses. Runtime ~27 seconds.
"""

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    Line,
    Circle,
    MoveAlongPath,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Flash,
    Transform,
    Polygon,
    rate_functions,
    linear,
    smooth,
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
PAPER = "#141418"   # card fill: a touch lighter than the background
LINE = "#2A2A30"

AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

# Aliases so the original animation code reads unchanged.
BLUE = MAGENTA   # the client / results accent (was blue)
GREEN = MINT     # "available" result chips
PINK = CORAL
SKY = GOLD
RED = CORAL      # "sold out" chips

FONT = "Inter"


def card(label, width=2.9, height=1.0, fill=PAPER, stroke=LINE,
         stroke_w=2.0, text_color=INK, font_size=28):
    """A flat rounded card with centred label. Returns a VGroup(rect, text)."""
    rect = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=stroke_w,
    )
    txt = Text(label, font=FONT, font_size=font_size, color=text_color)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)


def chip(label, fill, text_color=PAPER, font_size=24):
    """A small pill-shaped result chip."""
    rect = RoundedRectangle(
        corner_radius=0.22,
        width=1.5,
        height=0.6,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_width=0,
    )
    txt = Text(label, font=FONT, font_size=font_size, color=text_color)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)


class FanOut(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- (a) The client card appears on the left ------------------------
        client = card("Flight Search", width=3.2, height=1.2,
                      stroke=BLUE, stroke_w=3.0, text_color=INK, font_size=30)
        client.move_to(LEFT * 5.0)

        self.play(FadeIn(client, shift=UP * 0.3), run_time=0.7)

        # --- (b) A question bubble pops above the client --------------------
        bubble = RoundedRectangle(
            corner_radius=0.25,
            width=3.9,
            height=0.9,
            fill_color=BLUE,
            fill_opacity=1.0,
            stroke_width=0,
        )
        q_text = Text("any seats to Lagos?", font=FONT, font_size=26,
                      color=PAPER)
        q_text.move_to(bubble.get_center())
        bubble_group = VGroup(bubble, q_text)
        bubble_group.next_to(client, UP, buff=0.5)

        # Little tail pointing down toward the client.
        tail = Polygon(
            bubble.get_bottom() + LEFT * 0.2,
            bubble.get_bottom() + RIGHT * 0.2,
            bubble.get_bottom() + DOWN * 0.3,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=1.0,
            stroke_width=0,
        )

        self.play(
            GrowFromCenter(bubble_group),
            FadeIn(tail),
            run_time=0.6,
        )
        self.wait(0.3)
        self.play(FadeOut(bubble_group), FadeOut(tail), run_time=0.4)

        # --- The five airline API cards, stacked on the center-right --------
        airline_names = ["Airline A", "Airline B", "Airline C",
                         "Airline D", "Airline E"]
        airline_colors = [AMBER, VIOLET, GREEN, PINK, SKY]

        airlines = VGroup()
        for name, col in zip(airline_names, airline_colors):
            c = card(name, width=2.9, height=0.95, stroke=col, stroke_w=2.5,
                     text_color=INK, font_size=28)
            airlines.add(c)
        airlines.arrange(DOWN, buff=0.35)
        airlines.move_to(RIGHT * 3.6)

        self.play(
            FadeIn(airlines, shift=RIGHT * 0.3, lag_ratio=0.12),
            run_time=0.9,
        )

        # --- (c) Five arrows fan OUT, each with a glowing travelling dot -----
        client_anchor = client[0].get_right()
        arrow_lines = VGroup()
        for air, col in zip(airlines, airline_colors):
            target = air[0].get_left()
            seg = Line(client_anchor, target, stroke_color=col,
                       stroke_width=2.5, stroke_opacity=0.35)
            arrow_lines.add(seg)

        # Draw the faint connection lines quickly.
        self.play(
            *[Create(seg) for seg in arrow_lines],
            run_time=0.5,
        )

        # Request pulses: a glowing dot runs along each line in succession.
        for seg, col in zip(arrow_lines, airline_colors):
            glow = Dot(seg.get_start(), radius=0.12, color=col)
            glow.set_fill(col, opacity=1.0)
            halo = Circle(radius=0.22, color=col, stroke_width=0,
                          fill_color=col, fill_opacity=0.25)
            halo.move_to(seg.get_start())
            pulse = VGroup(halo, glow)
            self.play(
                MoveAlongPath(pulse, seg, rate_func=smooth),
                run_time=0.34,
            )
            self.remove(pulse)

        # --- (d) Each airline flashes and emits a result chip back ----------
        results = ["$420", "$510", "sold out", "$390", "$455"]
        result_cols = [GREEN, GREEN, RED, GREEN, GREEN]

        # Where the merged list will live (far left, below the client).
        merge_center = LEFT * 5.0 + DOWN * 0.3

        emitted_chips = []  # keep final chips for the merge step
        for air, seg, label, rcol in zip(
            airlines, arrow_lines, results, result_cols
        ):
            # Flash the airline card to show it "answered".
            self.play(
                Flash(air[0].get_center(), color=air[0].get_stroke_color(),
                      line_length=0.18, num_lines=10, flash_radius=0.9),
                run_time=0.22,
            )

            # Spawn a chip at the airline and send it back along the line.
            ch = chip(label, fill=rcol)
            ch.move_to(air[0].get_left())
            back_path = Line(seg.get_end(), seg.get_start())
            self.play(
                FadeIn(ch, scale=0.6),
                run_time=0.12,
            )
            self.play(
                MoveAlongPath(ch, back_path, rate_func=smooth),
                run_time=0.38,
            )
            emitted_chips.append((ch, label, rcol))

        # Fade the connection lines so the merge reads cleanly.
        self.play(FadeOut(arrow_lines), run_time=0.4)

        # --- (e) The chips stack into one merged "Results" list card --------
        # Build the destination results card.
        results_card = RoundedRectangle(
            corner_radius=0.2,
            width=3.4,
            height=3.6,
            fill_color=PAPER,
            fill_opacity=1.0,
            stroke_color=BLUE,
            stroke_width=3.0,
        )
        results_card.move_to(merge_center)
        results_title = Text("Results", font=FONT, font_size=30, color=INK)
        results_title.next_to(results_card.get_top(), DOWN, buff=0.28)

        self.play(
            FadeIn(results_card),
            FadeIn(results_title),
            run_time=0.5,
        )

        # Compute target slots inside the card for each chip.
        n = len(emitted_chips)
        top_y = results_card.get_top()[1] - 0.95
        step = 0.56
        animations = []
        for i, (ch, label, rcol) in enumerate(emitted_chips):
            target = results_card.get_center().copy()
            target[1] = top_y - i * step
            animations.append(ch.animate.move_to(target).scale(0.92))

        self.play(*animations, lag_ratio=0.08, run_time=1.0)

        # Settle beat.
        self.wait(1.0)

        # --- HOLD: loop the fan-out pulses so the frame never goes still ----
        # Rebuild the faint connection lines for the ambient loop.
        hold_lines = VGroup()
        for air, col in zip(airlines, airline_colors):
            seg = Line(client[0].get_right(), air[0].get_left(),
                       stroke_color=col, stroke_width=2.0,
                       stroke_opacity=0.25)
            hold_lines.add(seg)
        self.play(FadeIn(hold_lines), run_time=0.6)

        for _ in range(3):
            # Outbound request pulses fan out together.
            out_pulses = []
            out_moves = []
            for seg, col in zip(hold_lines, airline_colors):
                glow = Dot(seg.get_start(), radius=0.09, color=col)
                glow.set_fill(col, opacity=1.0)
                halo = Circle(radius=0.17, stroke_width=0,
                              fill_color=col, fill_opacity=0.22)
                halo.move_to(seg.get_start())
                p = VGroup(halo, glow)
                out_pulses.append(p)
                out_moves.append(MoveAlongPath(p, seg, rate_func=linear))
            self.play(*out_moves, run_time=0.9)
            for p in out_pulses:
                self.remove(p)

            # Inbound responses pulse back, with the results card breathing.
            in_pulses = []
            in_moves = []
            for seg, col in zip(hold_lines, airline_colors):
                back = Line(seg.get_end(), seg.get_start())
                glow = Dot(back.get_start(), radius=0.09, color=GREEN)
                glow.set_fill(GREEN, opacity=1.0)
                halo = Circle(radius=0.17, stroke_width=0,
                              fill_color=GREEN, fill_opacity=0.22)
                halo.move_to(back.get_start())
                p = VGroup(halo, glow)
                in_pulses.append(p)
                in_moves.append(MoveAlongPath(p, back, rate_func=linear))
            self.play(
                *in_moves,
                results_card.animate.set_stroke(width=4.5, opacity=0.9),
                rate_func=linear,
                run_time=0.9,
            )
            self.play(results_card.animate.set_stroke(width=3.0, opacity=1.0),
                      run_time=0.3)
            for p in in_pulses:
                self.remove(p)
            self.wait(0.5)

        self.wait(1.0)
