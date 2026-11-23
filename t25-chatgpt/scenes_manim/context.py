"""Scene: Runtime — system prompt + a finite context window.

Class `Context` (~19s). A hidden SILVER "system prompt" slab placed before
a TEAL user message, the whole transcript fed into the VIOLET model each
turn, and a finite "context window" frame; old messages at the top slide
OUT of the window ("forgotten") as new ones arrive. Caption: "hidden
system prompt + a finite context window = its only memory".

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
    Arrow,
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


class Context(Scene):
    def construct(self):
        title = Text("Runtime — the context window", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.54)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the finite context-window frame on the left -------------------
        win_c = np.array([-3.4, -0.2, 0.0])
        win_w, win_h = 4.4, 4.1
        window = RoundedRectangle(corner_radius=0.14, width=win_w, height=win_h,
                                  stroke_color=SILVER, stroke_width=2,
                                  stroke_opacity=0.5, fill_opacity=0.0)
        window.move_to(win_c)
        win_lbl = Text("context window", font=MONO, color=SILVER).scale(0.3)
        win_lbl.move_to([win_c[0], win_c[1] + win_h / 2 + 0.25, 0])
        self.play(Create(window), FadeIn(win_lbl), run_time=0.8)

        win_top = win_c[1] + win_h / 2 - 0.1
        win_bot = win_c[1] - win_h / 2 + 0.1
        row_h = 0.72

        # --- the VIOLET model on the right, fed the whole transcript --------
        model_c = np.array([3.2, -0.2, 0.0])
        box = RoundedRectangle(corner_radius=0.2, width=2.6, height=2.0,
                               stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.08)
        box.move_to(model_c)
        m_lbl = Text("MODEL", font=MONO, color=VIOLET,
                     weight="BOLD").scale(0.4)
        m_lbl.move_to(model_c + UP * 0.2)
        m_sub = Text("reads it all\neach turn", font=MONO, color=SECOND).scale(0.28)
        m_sub.move_to(model_c + DOWN * 0.4)
        feed = Arrow([win_c[0] + win_w / 2 + 0.05, win_c[1], 0],
                     box.get_left() + LEFT * 0.05, color=TEAL, stroke_width=3,
                     buff=0.1, max_tip_length_to_length_ratio=0.12)
        self.play(Create(box), FadeIn(m_lbl), FadeIn(m_sub), Create(feed),
                  run_time=0.9)

        # --- the hidden system prompt slab (pinned at top of window) --------
        sys = RoundedRectangle(corner_radius=0.1, width=win_w - 0.5,
                               height=row_h - 0.14, stroke_color=SILVER,
                               stroke_width=2, fill_color=SILVER,
                               fill_opacity=0.08)
        sys.move_to([win_c[0], win_top - row_h / 2, 0])
        sys_txt = Text("system prompt  (hidden)", font=MONO,
                       color=SILVER).scale(0.28)
        sys_txt.move_to(sys.get_center())
        sys_g = VGroup(sys, sys_txt)
        self.play(FadeIn(sys_g, shift=DOWN * 0.15), run_time=0.6)
        self.add(sys_g)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # scrolling conversation rows below the pinned system slab.
        # Rows are created once; an updater scrolls them up and fades the ones
        # that slide out the TOP of the window ("forgotten").
        n_rows = 7
        scroll_top = win_top - row_h   # first chat row sits just below sys slab
        visible_span = (scroll_top - win_bot)  # usable height for chat rows
        n_visible = 4

        rows = []
        row_group = VGroup()
        for i in range(n_rows):
            is_user = (i % 2 == 0)
            col = TEAL if is_user else GREEN
            role = "user:" if is_user else "assistant:"
            r = RoundedRectangle(corner_radius=0.1, width=win_w - 0.5,
                                 height=row_h - 0.16, stroke_color=col,
                                 stroke_width=2, fill_color=col,
                                 fill_opacity=0.07)
            tx = Text(role + " message " + str(i + 1), font=MONO,
                      color=col).scale(0.26)
            tx.move_to(r.get_center())
            g = VGroup(r, tx)
            row_group.add(g)
            rows.append((g, col))
        self.add(row_group)

        def make_row_upd(idx):
            col = ManimColor(rows[idx][1])

            def _upd(m):
                tt = t.get_value()
                # each row's slot decreases over time as new rows arrive
                slot = (idx + 0.5) - (tt * 0.45)
                y = scroll_top - slot * row_h
                m.move_to([win_c[0], y, 0])
                # opacity: full inside window, fades as it passes above top
                if y > win_top + 0.1:
                    a = 0.0
                elif y > scroll_top:
                    a = np.clip((win_top + 0.1 - y) / (win_top + 0.1 - scroll_top),
                                0.0, 1.0)
                elif y < win_bot:
                    a = 0.0
                else:
                    a = 1.0
                m.set_opacity(a)
            return _upd
        for i, (g, _) in enumerate(rows):
            g.add_updater(make_row_upd(i))

        # a "forgotten" tag drifts up and out above the window top
        forget = Text("forgotten", font=MONO, color=SECOND).scale(0.28)
        self.add(forget)

        def forget_upd(m):
            tt = t.get_value()
            drift = (tt * 0.45) % 2.0
            y = win_top + 0.35 + drift * 0.3
            m.move_to([win_c[0], y, 0])
            m.set_opacity(0.6 * np.clip(1.0 - drift / 2.0, 0.0, 1.0))
        forget.add_updater(forget_upd)

        # system slab stays pinned and glows (it never scrolls out)
        def sys_upd(m):
            s = 0.5 + 0.5 * np.sin(2.0 * t.get_value())
            m[0].set_fill(SILVER, opacity=0.05 + 0.08 * s)
            m[0].set_stroke(opacity=0.5 + 0.4 * s)
        sys_g.add_updater(sys_upd)

        v_base = ManimColor(VIOLET)
        v_hi = ManimColor(INK)

        def box_upd(m):
            s = 0.5 + 0.5 * np.sin(2.3 * t.get_value())
            m.set_stroke(color=interpolate_color(v_base, v_hi, 0.2 * s))
            m.set_fill(VIOLET, opacity=0.06 + 0.08 * s)
        box.add_updater(box_upd)

        def feed_upd(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_opacity(0.5 + 0.5 * s)
        feed.add_updater(feed_upd)

        # keep the pinned system slab on top of scrolling rows
        sys_g.set_z_index(5)
        window.set_z_index(6)

        # caption
        cap = Text("hidden system prompt + a finite context window = its only memory",
                   font=HEAD, color=SECOND).scale(0.33)
        cap.to_edge(DOWN, buff=0.25)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
