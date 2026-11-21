"""Primer — "What an OS actually does."

A premium-dark layered diagram: HARDWARE at the bottom, the KERNEL (RING 0)
above it, a SYSTEM CALLS divider, and USER SPACE / APPS at the top. A request
continuously flows down from an app through a system call into the kernel, to
the hardware, and a response travels back up — looping forever.
"""

from manim import (
    VGroup,
    Scene,
    RoundedRectangle,
    Rectangle,
    Line,
    DashedLine,
    Dot,
    Text,
    ValueTracker,
    Create,
    FadeIn,
    always_redraw,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

# --- Premium-dark palette -----------------------------------------------------
BG = "#09090C"
INK = "#E9E8E4"
INK2 = "#90908C"
TEAL = "#2DD4BF"      # kernel / UNIX family
GREEN = "#35FF9E"     # linux family
VIOLET = "#9B8CFF"    # microsoft
AMBER = "#FFB020"     # google
SILVER = "#C9CDD4"    # apple
CORAL = "#FF6B4A"     # accent

FONT = "Inter"
MONO = "DejaVu Sans Mono"


def soft_panel(width, height, color, fill_opacity=0.06):
    """A crisp rounded rect with a soft glow ring behind it."""
    glow = RoundedRectangle(
        width=width, height=height, corner_radius=0.18,
        stroke_color=color, stroke_width=14, stroke_opacity=0.12,
        fill_opacity=0.0,
    )
    crisp = RoundedRectangle(
        width=width, height=height, corner_radius=0.18,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=fill_opacity,
    )
    return VGroup(glow, crisp)


class Primer(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Title ---------------------------------------------------------
        title = Text("What an OS actually does", font=FONT, color=INK, weight="BOLD")
        title.scale(0.8).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.9)

        # --- Layer geometry ------------------------------------------------
        lw = 9.8           # layer width
        lh = 1.35          # layer height
        gap = 0.55
        # y positions bottom -> top
        y_hw = -3.0
        y_kernel = y_hw + lh + gap
        y_user = y_kernel + lh + gap + 0.5  # extra room for divider

        # HARDWARE (bottom) -------------------------------------------------
        hw = soft_panel(lw, lh, INK2, fill_opacity=0.05).move_to([0, y_hw, 0])
        hw_label = Text("HARDWARE", font=FONT, color=INK, weight="BOLD").scale(0.5)
        hw_label.move_to(hw.get_center() + LEFT * (lw / 2 - 1.5))
        # small chips: CPU / RAM / DISK
        chips = VGroup()
        for i, name in enumerate(("CPU", "RAM", "DISK")):
            chip = RoundedRectangle(
                width=1.55, height=0.72, corner_radius=0.1,
                stroke_color=INK2, stroke_width=2,
                fill_color=INK2, fill_opacity=0.10,
            )
            txt = Text(name, font=MONO, color=INK2).scale(0.38)
            txt.move_to(chip.get_center())
            chips.add(VGroup(chip, txt))
        chips.arrange(RIGHT, buff=0.4)
        chips.move_to(hw.get_center() + RIGHT * 1.6)

        # KERNEL · RING 0 ---------------------------------------------------
        kernel = soft_panel(lw, lh, TEAL, fill_opacity=0.08).move_to([0, y_kernel, 0])
        kernel_label = Text("KERNEL · RING 0", font=FONT, color=TEAL, weight="BOLD").scale(0.5)
        kernel_label.move_to(kernel.get_center() + LEFT * (lw / 2 - 2.0))
        kernel_sub = Text("schedules · memory · drivers", font=MONO, color=INK2).scale(0.34)
        kernel_sub.move_to(kernel.get_center() + RIGHT * 2.3)

        # SYSTEM CALLS divider (between kernel and user) --------------------
        y_div = (y_kernel + lh / 2 + y_user - lh / 2) / 2
        divider = DashedLine(
            [-lw / 2, y_div, 0], [lw / 2, y_div, 0],
            color=CORAL, stroke_width=2.5, dash_length=0.14,
        )
        div_label = Text("SYSTEM CALLS", font=MONO, color=CORAL, weight="BOLD").scale(0.36)
        div_label.next_to(divider, RIGHT, buff=-1.9).shift(UP * 0.0)
        div_label.move_to([lw / 2 - 1.4, y_div, 0])
        div_bg = Rectangle(
            width=div_label.width + 0.3, height=div_label.height + 0.14,
            stroke_opacity=0, fill_color=BG, fill_opacity=1.0,
        ).move_to(div_label)
        div_group = VGroup(divider, div_bg, div_label)

        # USER SPACE · APPS (top) ------------------------------------------
        user = soft_panel(lw, lh, SILVER, fill_opacity=0.05).move_to([0, y_user, 0])
        user_label = Text("USER SPACE · APPS", font=FONT, color=INK, weight="BOLD").scale(0.5)
        user_label.move_to(user.get_center() + LEFT * (lw / 2 - 2.2))
        apps = VGroup()
        for name in ("Browser", "Editor", "Media"):
            a = RoundedRectangle(
                width=1.7, height=0.72, corner_radius=0.12,
                stroke_color=SILVER, stroke_width=2,
                fill_color=SILVER, fill_opacity=0.08,
            )
            t = Text(name, font=FONT, color=INK).scale(0.36)
            t.move_to(a.get_center())
            apps.add(VGroup(a, t))
        apps.arrange(RIGHT, buff=0.4)
        apps.move_to(user.get_center() + RIGHT * 1.9)

        # --- Build sequence (first ~5s) -----------------------------------
        self.play(FadeIn(hw, shift=UP * 0.2), FadeIn(hw_label), run_time=0.7)
        self.play(*[FadeIn(c, shift=UP * 0.15) for c in chips], run_time=0.6)
        self.play(FadeIn(kernel, shift=UP * 0.2), FadeIn(kernel_label), FadeIn(kernel_sub), run_time=0.7)
        self.play(Create(divider), FadeIn(div_label), run_time=0.7)
        self.add(div_bg)
        div_bg.z_index = -1
        self.play(FadeIn(user, shift=DOWN * 0.2), FadeIn(user_label), run_time=0.7)
        self.play(*[FadeIn(a, shift=DOWN * 0.15) for a in apps], run_time=0.6)

        # Connector spine (the request channel) ----------------------------
        x_ch = -lw / 2 + 0.9
        top_y = user.get_center()[1]
        bot_y = hw.get_center()[1]
        spine = Line([x_ch, top_y, 0], [x_ch, bot_y, 0], color=INK2, stroke_width=1.5, stroke_opacity=0.4)
        self.play(Create(spine), run_time=0.5)

        # --- Continuous request/response loop -----------------------------
        clock = ValueTracker(0.0)

        # The packet travels: top -> bottom (request), then bottom -> top
        # (response), over a period. We map phase in [0,1): 0..0.5 request
        # going down, 0.5..1 response going up.
        period = 3.6  # seconds per full round-trip
        travel = top_y - bot_y

        def packet_y(phase):
            if phase < 0.5:
                f = phase / 0.5          # 0 -> 1 going down
                return top_y - travel * rate_functions.ease_in_out_sine(f)
            else:
                f = (phase - 0.5) / 0.5  # 0 -> 1 going up
                return bot_y + travel * rate_functions.ease_in_out_sine(f)

        def current_phase():
            return (clock.get_value() / period) % 1.0

        # Request packet (coral going down, teal going up).
        def make_packet():
            phase = current_phase()
            y = packet_y(phase)
            color = AMBER if phase < 0.5 else TEAL
            glow = Dot([x_ch, y, 0], radius=0.22, color=color).set_opacity(0.18)
            core = Dot([x_ch, y, 0], radius=0.10, color=color)
            return VGroup(glow, core)

        packet = always_redraw(make_packet)
        self.add(packet)

        # A trailing comet tail of fading dots.
        def make_tail():
            grp = VGroup()
            phase = current_phase()
            for k in range(1, 7):
                p2 = (phase - 0.012 * k) % 1.0
                y = packet_y(p2)
                color = AMBER if p2 < 0.5 else TEAL
                d = Dot([x_ch, y, 0], radius=0.06, color=color)
                d.set_opacity(max(0.0, 0.5 - 0.08 * k))
                grp.add(d)
            return grp

        tail = always_redraw(make_tail)
        self.add(tail)

        # Breathing kernel glow (the ring) + sweeping highlight label.
        kernel_glow = kernel[0]

        def breathe_kernel(m):
            t = clock.get_value()
            m.set_stroke(opacity=0.12 + 0.10 * (0.5 + 0.5 * __import__("math").sin(t * 2.0)))

        kernel_glow.add_updater(breathe_kernel)

        # Phase caption that flips between REQUEST and RESPONSE.
        caption = Text("", font=MONO, color=INK2).scale(0.4)
        caption.move_to([x_ch + 0.0, (top_y + bot_y) / 2, 0]).shift(RIGHT * 0.0)

        def update_caption(m):
            phase = current_phase()
            if phase < 0.5:
                label, col = "request  ↓", AMBER
            else:
                label, col = "response  ↑", TEAL
            new = Text(label, font=MONO, color=col).scale(0.4)
            new.move_to([x_ch + 1.9, (top_y + bot_y) / 2, 0])
            m.become(new)

        caption.add_updater(update_caption)
        self.add(caption)

        # Pulsing chip under the hardware when the packet reaches bottom.
        def pulse_hw(m):
            phase = current_phase()
            near = min(abs(phase - 0.5), 1 - abs(phase - 0.5))
            amt = max(0.0, 0.5 - near * 4.0)
            m.set_stroke(opacity=0.12 + amt)

        hw_glow = hw[0]
        hw_glow.add_updater(pulse_hw)

        # --- Run the clock for the rest of the scene ----------------------
        # ~5.5s build above; animate the clock ~20s for a ~26s total.
        self.play(clock.animate.set_value(period * 5.6), run_time=20.0, rate_func=rate_functions.linear)
        self.wait(0.3)

        # Clean final frame.
        kernel_glow.clear_updaters()
        hw_glow.clear_updaters()
        caption.clear_updaters()
        packet.clear_updaters()
        tail.clear_updaters()
        self.wait(0.2)
