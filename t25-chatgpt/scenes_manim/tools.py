"""Scene: The model as the centre of a tool-using system.

Class `Tools` (~19s). The VIOLET model sits at the centre, calling TOOLS
arranged around it: "browse web", "run code", "retrieve docs". A request
goes out to one tool and a real result comes back into the answer; a CORAL
"guardrails" filter layer sits on the output. Caption: "tools (browse/code/
retrieval) + guardrails = a full system".

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
    Dot,
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


class Tools(Scene):
    def construct(self):
        title = Text("A full system — tools & guardrails", font=HEAD,
                     color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the VIOLET model at the centre ---------------------------------
        model_c = np.array([-1.2, 0.0, 0.0])
        box = RoundedRectangle(corner_radius=0.22, width=2.6, height=2.0,
                               stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.08)
        box.move_to(model_c)
        m_lbl = Text("MODEL", font=MONO, color=VIOLET,
                     weight="BOLD").scale(0.4)
        m_lbl.move_to(model_c)
        self.play(Create(box), FadeIn(m_lbl), run_time=0.8)

        # --- the tools arranged around it -----------------------------------
        tool_specs = [
            ("browse web", np.array([-4.6, 1.8, 0.0]), TEAL),
            ("run code", np.array([-4.8, -0.2, 0.0]), GREEN),
            ("retrieve docs", np.array([-4.6, -2.0, 0.0]), GOLD),
        ]
        tools = []
        for name, pos, col in tool_specs:
            tb = RoundedRectangle(corner_radius=0.12, width=2.1, height=0.8,
                                  stroke_color=col, stroke_width=2.2,
                                  fill_color=col, fill_opacity=0.07)
            tb.move_to(pos)
            tl = Text(name, font=MONO, color=col).scale(0.3)
            tl.move_to(pos)
            # two-way link to the model
            link = Line(tb.get_right(), box.get_left(), stroke_color=col,
                        stroke_width=2, stroke_opacity=0.4)
            tools.append((tb, tl, link, col, pos))
        self.play(*[FadeIn(tb) for tb, _, _, _, _ in tools],
                  *[FadeIn(tl) for _, tl, _, _, _ in tools],
                  *[Create(lk) for _, _, lk, _, _ in tools],
                  lag_ratio=0.1, run_time=1.2)

        tools_lbl = Text("TOOLS", font=MONO, color=SECOND,
                         weight="BOLD").scale(0.3)
        tools_lbl.move_to([-4.7, 2.6, 0])
        self.play(FadeIn(tools_lbl), run_time=0.4)

        # --- CORAL guardrails filter layer on the output -------------------
        guard = RoundedRectangle(corner_radius=0.14, width=0.55, height=3.0,
                                 stroke_color=CORAL, stroke_width=2.5,
                                 fill_color=CORAL, fill_opacity=0.1)
        guard.move_to([1.5, 0.0, 0])
        g_lbl = Text("guardrails", font=MONO, color=CORAL,
                     weight="BOLD").scale(0.28)
        g_lbl.rotate(np.pi / 2)
        g_lbl.move_to(guard.get_center())
        out_arrow_in = Arrow(box.get_right() + RIGHT * 0.02,
                             guard.get_left() + LEFT * 0.02, color=VIOLET,
                             stroke_width=3, buff=0.08,
                             max_tip_length_to_length_ratio=0.2)
        # answer bubble on the far right (the clean output)
        ans = RoundedRectangle(corner_radius=0.12, width=2.4, height=1.1,
                               stroke_color=GREEN, stroke_width=2.2,
                               fill_color=GREEN, fill_opacity=0.07)
        ans.move_to([4.5, 0.0, 0])
        ans_lbl = Text("assistant:\nanswer", font=MONO, color=GREEN).scale(0.28)
        ans_lbl.move_to(ans.get_center())
        out_arrow_out = Arrow(guard.get_right() + RIGHT * 0.02,
                              ans.get_left() + LEFT * 0.02, color=CORAL,
                              stroke_width=3, buff=0.08,
                              max_tip_length_to_length_ratio=0.2)
        self.play(Create(out_arrow_in), Create(guard), FadeIn(g_lbl),
                  Create(out_arrow_out), FadeIn(ans), FadeIn(ans_lbl),
                  run_time=1.0)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        v_base = ManimColor(VIOLET)
        v_hi = ManimColor(INK)

        def box_upd(m):
            s = 0.5 + 0.5 * np.sin(2.4 * t.get_value())
            m.set_stroke(color=interpolate_color(v_base, v_hi, 0.2 * s))
            m.set_fill(VIOLET, opacity=0.06 + 0.08 * s)
        box.add_updater(box_upd)

        # request/result packets travel out to the ACTIVE tool and back.
        # One tool is "active" at a time, cycling through the three.
        packets = VGroup()
        for i in range(3):
            p = Dot(radius=0.07, color=INK)
            packets.add(p)
        self.add(packets)

        tool_centers = [tb.get_center() for tb, _, _, _, _ in tools]
        model_edge = box.get_left()
        n_tools = len(tools)

        def make_packet_upd(idx):
            def _upd(m):
                tt = t.get_value()
                # full cycle 0..1 ; which tool is active
                cyc = (tt * 0.35 + idx / 3.0)
                active = int(cyc) % n_tools
                phase = cyc % 1.0
                tc = tool_centers[active]
                col = tool_specs[active][2]
                # 0..0.5 request out (model->tool), 0.5..1 result back
                if phase < 0.5:
                    a = phase / 0.5
                    p = model_edge + (tc - model_edge) * a
                    m.set_color(VIOLET)
                else:
                    a = (phase - 0.5) / 0.5
                    p = tc + (model_edge - tc) * a
                    m.set_color(ManimColor(col))
                m.move_to(p)
                m.set_opacity(0.3 + 0.7 * np.sin(np.pi * phase))
            return _upd
        for i, p in enumerate(packets):
            p.add_updater(make_packet_upd(i))

        # the active tool box glows
        for i, (tb, tl, link, col, pos) in enumerate(tools):
            def make_tool_upd(idx, color):
                base = ManimColor(color)
                hi = ManimColor(INK)

                def _upd(m):
                    tt = t.get_value()
                    cyc = tt * 0.35
                    active = int(cyc) % n_tools
                    if active == idx:
                        pulse = 0.5 + 0.5 * np.sin(8.0 * tt)
                        m.set_stroke(color=interpolate_color(base, hi,
                                     0.35 * pulse))
                        m.set_fill(color, opacity=0.08 + 0.14 * pulse)
                    else:
                        m.set_stroke(color=base)
                        m.set_fill(color, opacity=0.05)
                return _upd
            tb.add_updater(make_tool_upd(i, col))

        # guardrails layer scans (a shimmer)
        c_base = ManimColor(CORAL)
        c_hi = ManimColor(INK)

        def guard_upd(m):
            s = 0.5 + 0.5 * np.sin(4.0 * t.get_value())
            m.set_stroke(color=interpolate_color(c_base, c_hi, 0.25 * s))
            m.set_fill(CORAL, opacity=0.08 + 0.1 * s)
        guard.add_updater(guard_upd)

        def out_upd(m):
            s = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_opacity(0.5 + 0.5 * s)
        out_arrow_in.add_updater(out_upd)
        out_arrow_out.add_updater(out_upd)

        # caption
        cap = Text("tools (browse/code/retrieval) + guardrails = a full system",
                   font=HEAD, color=SECOND).scale(0.34)
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
