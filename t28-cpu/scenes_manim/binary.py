"""Scene 2: it only understands 1s and 0s.

Class `Binary` (~18s). A row of bits flips, groups into a number, and that
number becomes a letter / a pixel / a sound wave. Also shows "program =
numbers in memory too" (von Neumann) with code and data side by side as
number cells. Caption: "it only understands 1s and 0s".

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
    Square,
    Dot,
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

DIM = "#1C2A22"


class Binary(Scene):
    def construct(self):
        title = Text("Everything is 1s and 0s", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- a row of 8 bits ------------------------------------------------
        n_bits = 8
        bit_cells = []
        row = VGroup()
        start_x = -3.4
        for i in range(n_bits):
            box = Square(side_length=0.62, stroke_color=SECOND,
                         stroke_width=2, fill_color="#111318",
                         fill_opacity=0.9)
            box.move_to([start_x + i * 0.72, 2.0, 0])
            txt = Text("0", font=MONO, color=SECOND).scale(0.42)
            txt.move_to(box.get_center())
            row.add(box, txt)
            bit_cells.append((box, txt, i))
        self.play(FadeIn(row), run_time=0.8)

        bits_lbl = Text("8 bits = 1 byte", font=MONO, color=SECOND).scale(0.3)
        bits_lbl.next_to(row, LEFT, buff=0.3).shift(UP * 0.0)
        bits_lbl.move_to([start_x - 1.2, 2.0, 0])
        self.play(FadeIn(bits_lbl), run_time=0.4)

        # --- the grouped number display -------------------------------------
        num_box = RoundedRectangle(corner_radius=0.1, width=1.9, height=0.8,
                                   stroke_color=INK, stroke_width=2,
                                   fill_color="#111318", fill_opacity=0.9)
        num_box.move_to([0.0, 0.7, 0])
        num_txt = Text("= 0", font=MONO, color=INK).scale(0.5)
        num_txt.move_to(num_box.get_center())
        self.play(Create(num_box), FadeIn(num_txt), run_time=0.6)

        # --- three interpretations: letter / pixel / sound ------------------
        letter_box = RoundedRectangle(corner_radius=0.1, width=1.3, height=1.0,
                                      stroke_color=TEAL, stroke_width=2,
                                      fill_color="#111318", fill_opacity=0.9)
        letter_box.move_to([-3.4, -1.3, 0])
        letter_txt = Text("A", font=HEAD, color=TEAL).scale(0.8)
        letter_txt.move_to(letter_box.get_center())
        letter_lbl = Text("a letter", font=MONO, color=SECOND).scale(0.26)
        letter_lbl.next_to(letter_box, DOWN, buff=0.15)

        pixel_box = RoundedRectangle(corner_radius=0.1, width=1.3, height=1.0,
                                     stroke_color=VIOLET, stroke_width=2,
                                     fill_color="#111318", fill_opacity=0.9)
        pixel_box.move_to([0.0, -1.3, 0])
        pixel = Square(side_length=0.42, stroke_width=0,
                       fill_color=VIOLET, fill_opacity=0.9)
        pixel.move_to(pixel_box.get_center())
        pixel_lbl = Text("a pixel", font=MONO, color=SECOND).scale(0.26)
        pixel_lbl.next_to(pixel_box, DOWN, buff=0.15)

        sound_box = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.0,
                                     stroke_color=AMBER, stroke_width=2,
                                     fill_color="#111318", fill_opacity=0.9)
        sound_box.move_to([3.4, -1.3, 0])
        sound_lbl = Text("a sound", font=MONO, color=SECOND).scale(0.26)
        sound_lbl.next_to(sound_box, DOWN, buff=0.15)
        wave = Line(sound_box.get_left() + RIGHT * 0.15,
                    sound_box.get_right() + LEFT * 0.15,
                    stroke_color=AMBER, stroke_width=2.5)

        interp = VGroup(letter_box, letter_txt, letter_lbl,
                        pixel_box, pixel, pixel_lbl,
                        sound_box, sound_lbl, wave)
        self.play(FadeIn(interp), run_time=0.9)

        # --- von Neumann: code & data side by side --------------------------
        vn_lbl = Text("program = numbers in memory too",
                      font=MONO, color=SECOND).scale(0.3)
        vn_lbl.move_to([0.0, -3.0, 0])

        def cell_strip(center, label, color):
            strip = VGroup()
            head = Text(label, font=MONO, color=color).scale(0.26)
            head.move_to(center + UP * 0.5)
            cells = []
            for i in range(4):
                c = Square(side_length=0.38, stroke_color=color,
                           stroke_width=1.8, fill_color="#111318",
                           fill_opacity=0.9)
                c.move_to(center + RIGHT * ((i - 1.5) * 0.44))
                tx = Text("00", font=MONO, color=color).scale(0.22)
                tx.move_to(c.get_center())
                strip.add(c, tx)
                cells.append(tx)
            strip.add(head)
            return strip, cells

        code_strip, code_cells = cell_strip(
            np.array([-2.4, -2.3, 0.0]), "CODE", GREEN)
        data_strip, data_cells = cell_strip(
            np.array([2.4, -2.3, 0.0]), "DATA", TEAL)
        self.play(FadeIn(code_strip), FadeIn(data_strip), FadeIn(vn_lbl),
                  run_time=0.8)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        c_on = ManimColor(GREEN)
        c_off = ManimColor(SECOND)

        def bit_value(i, tt):
            # each bit flips at its own rate -> a counting-like pattern
            return 1 if np.sin((0.5 + i * 0.18) * tt + i) > 0 else 0

        def current_number(tt):
            v = 0
            for b in range(n_bits):
                v = v * 2 + bit_value(n_bits - 1 - b, tt)
            return v

        def make_bit(txt_m, idx):
            def _upd(m):
                val = bit_value(idx, t.get_value())
                col = ManimColor(GREEN) if val else ManimColor(SECOND)
                new = Text(str(val), font=MONO, color=col).scale(0.42)
                new.move_to(m.get_center())
                m.become(new)
            return _upd
        for box, txt, i in bit_cells:
            txt.add_updater(make_bit(txt, i))

        def make_box(box_m, idx):
            def _upd(m):
                val = bit_value(idx, t.get_value())
                m.set_stroke(GREEN if val else SECOND,
                             width=2.5 if val else 2)
                m.set_fill("#13261C" if val else "#111318", opacity=0.9)
            return _upd
        for box, txt, i in bit_cells:
            box.add_updater(make_box(box, i))

        def num_upd(m):
            v = current_number(t.get_value())
            new = Text("= " + str(v), font=MONO, color=INK).scale(0.5)
            new.move_to(num_box.get_center())
            m.become(new)
        num_txt.add_updater(num_upd)

        # letter interpretation (A..Z cycling with the low byte)
        def letter_upd(m):
            v = current_number(t.get_value())
            ch = chr(65 + (v % 26))
            new = Text(ch, font=HEAD, color=TEAL).scale(0.8)
            new.move_to(letter_box.get_center())
            m.become(new)
        letter_txt.add_updater(letter_upd)

        # pixel brightness interpretation
        cp_a = ManimColor("#2A1540")
        cp_b = ManimColor(VIOLET)

        def pixel_upd(m):
            v = current_number(t.get_value()) / 255.0
            m.set_fill(interpolate_color(cp_a, cp_b, v), opacity=0.95)
        pixel.add_updater(pixel_upd)

        # sound wave interpretation (amplitude/freq from value)
        wx0 = sound_box.get_left()[0] + 0.15
        wx1 = sound_box.get_right()[0] - 0.15
        wy = sound_box.get_center()[1]

        def wave_upd(m):
            v = current_number(t.get_value())
            freq = 2.0 + (v / 255.0) * 10.0
            amp = 0.12 + (v / 255.0) * 0.28
            pts = []
            steps = 48
            for k in range(steps + 1):
                fx = k / steps
                x = wx0 + (wx1 - wx0) * fx
                y = wy + amp * np.sin(freq * fx * 2 * np.pi
                                      + 3.0 * t.get_value())
                pts.append([x, y, 0])
            m.set_points_as_corners(pts)
        wave.add_updater(wave_upd)

        # von Neumann cells shuffle numbers (both are just numbers)
        def make_cell(tx_m, seed):
            def _upd(m):
                v = int((np.sin(0.7 * t.get_value() + seed) * 0.5 + 0.5)
                        * 255)
                new = Text(f"{v:02X}", font=MONO,
                           color=m.get_color()).scale(0.22)
                new.move_to(m.get_center())
                m.become(new)
            return _upd
        for j, tx in enumerate(code_cells):
            tx.set_color(GREEN)
            tx.add_updater(make_cell(tx, j * 1.3))
        for j, tx in enumerate(data_cells):
            tx.set_color(TEAL)
            tx.add_updater(make_cell(tx, j * 1.3 + 5.0))

        def vn_upd(m):
            m.set_opacity(0.45 + 0.4 * (0.5 + 0.5 *
                          np.sin(1.4 * t.get_value())))
        vn_lbl.add_updater(vn_upd)

        # caption
        cap = Text("it only understands 1s and 0s",
                   font=HEAD, color=SECOND).scale(0.4)
        cap.to_edge(DOWN, buff=0.22)

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
