"""Scene: SHAPE vs CAPABILITY — the core USB-C insight.

Class `Chaos` (~18s). Centre: a single TEAL USB-C connector outline (the only
shape there will ever be). Fanned out around it, a ring of labelled capability
tags shows the SAME plug can be many different things: USB 2.0, USB 3.2, USB4,
Thunderbolt, Power Delivery, or charge-only. Driven by a master ValueTracker
the tags orbit and light up one at a time while the plug's shape never changes.
Two column headers read SHAPE (1) vs CAPABILITY (many); the caption cycles
"the plug tells you nothing" -> "check the spec, not the shape".

Dark palette only, TEXT labels only, continuous motion. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Line,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
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


class Chaos(Scene):
    def construct(self):
        title = Text("ONE SHAPE, MANY CAPABILITIES",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- column headers --------------------------------------------------
        head_shape = Text("SHAPE (1)", font=MONO, color=TEAL).scale(0.4)
        head_cap = Text("CAPABILITY (many)", font=MONO, color=AMBER).scale(0.4)
        head_shape.next_to(title, DOWN, buff=0.2).shift(LEFT * 4.2)
        head_cap.next_to(title, DOWN, buff=0.2).shift(RIGHT * 3.6)
        self.play(FadeIn(head_shape), FadeIn(head_cap), run_time=0.5)

        center = ORIGIN + DOWN * 0.3

        # --- the single USB-C connector outline (centre) --------------------
        c_body = RoundedRectangle(corner_radius=0.5, width=2.2, height=1.0,
                                  stroke_color=TEAL, stroke_width=4,
                                  fill_color="#07201D", fill_opacity=0.6)
        c_tongue = RoundedRectangle(corner_radius=0.14, width=1.5, height=0.3,
                                    stroke_color=TEAL, stroke_width=2.5,
                                    fill_opacity=0)
        plug = VGroup(c_body, c_tongue).move_to(center)
        c_tongue.move_to(c_body)
        plug_lbl = Text("USB-C", font=MONO, color=TEAL).scale(0.34)
        plug_lbl.next_to(plug, DOWN, buff=0.22)

        self.play(Create(c_body), run_time=0.7)
        self.play(Create(c_tongue), FadeIn(plug_lbl), run_time=0.5)

        # --- capability tags fanned around the plug -------------------------
        tags_spec = [
            ("USB 2.0 . 480 Mbps", SILVER),
            ("USB 3.2 . 20 Gbps", GREEN),
            ("USB4 . 40 Gbps", TEAL),
            ("Thunderbolt . 80 Gbps", VIOLET),
            ("PD . 240W", AMBER),
            ("charge only", CORAL),
        ]
        n = len(tags_spec)
        radius = 3.0

        tags = []   # list of dicts
        for i, (txt, col) in enumerate(tags_spec):
            label = Text(txt, font=MONO, color=col).scale(0.34)
            box = RoundedRectangle(
                corner_radius=0.12,
                width=label.width + 0.4, height=label.height + 0.3,
                stroke_color=col, stroke_width=2,
                fill_color=BG, fill_opacity=0.9,
            )
            label.move_to(box)
            tag = VGroup(box, label)
            # connector line from plug centre to tag (grows during motion)
            link = Line(center, center, stroke_color=col, stroke_width=2)
            tags.append({
                "group": tag, "box": box, "label": label,
                "link": link, "col": col, "phase": i,
            })

        tag_groups = VGroup(*[tg["group"] for tg in tags])
        links = VGroup(*[tg["link"] for tg in tags])
        self.add(links)
        self.play(*[GrowFromCenter(tg["group"]) for tg in tags],
                  lag_ratio=0.08, run_time=1.0)

        # --- caption ---------------------------------------------------------
        caption = Text("the plug tells you nothing",
                       font=HEAD, color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.4)
        caption._idx = -1
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        TOTAL = 18.0
        omega = 0.42          # orbit angular speed
        highlight_rate = 1.5  # seconds each tag stays "active"

        TEAL_C = ManimColor(TEAL)

        # orbit + light-up updater for each tag
        for i, tg in enumerate(tags):
            def make_orbit(entry, idx):
                group = entry["group"]
                box = entry["box"]
                label = entry["label"]
                link = entry["link"]
                base = ManimColor(entry["col"])
                hot = ManimColor(INK)

                def _upd(m):
                    tt = t.get_value()
                    ang = omega * tt + idx * (2 * np.pi / n) + np.pi / 2
                    pos = center + radius * np.array(
                        [np.cos(ang), np.sin(ang) * 0.62, 0])
                    group.move_to(pos)
                    # which tag is active right now (cycles through indices)
                    active = int(tt / highlight_rate) % n
                    on = 1.0 if active == idx else 0.0
                    # smooth the on/off a touch via sub-phase
                    sub = (tt / highlight_rate) % 1.0
                    glow = on * (0.5 + 0.5 * np.sin(np.pi * sub))
                    col = interpolate_color(base, hot, 0.5 * glow)
                    box.set_stroke(color=col, width=2 + 2.5 * glow)
                    box.set_fill(opacity=0.9)
                    label.set_color(col)
                    group.set_opacity(0.45 + 0.55 * (0.4 + 0.6 * glow))
                    # link from plug edge to tag, brightens with glow
                    edge = center + 1.15 * (pos - center) / (
                        np.linalg.norm(pos - center) + 1e-6)
                    link.put_start_and_end_on(edge, pos)
                    link.set_stroke(
                        color=interpolate_color(ManimColor(SECOND), base, glow),
                        width=1.5 + 2.0 * glow,
                        opacity=0.3 + 0.6 * glow)
                return _upd
            tg["group"].add_updater(make_orbit(tg, i))

        # the central plug stays the exact same shape but pulses teal to show
        # it is the active conduit — shape never changes.
        def plug_pulse(m):
            tt = t.get_value()
            g = 0.5 + 0.5 * np.sin(tt * 2.2)
            col = interpolate_color(TEAL_C, ManimColor(INK), 0.25 * g)
            c_body.set_stroke(color=col, width=4 + 1.5 * g)
            c_tongue.set_stroke(color=col)
        plug.add_updater(plug_pulse)
        self.add(plug)

        # subtitle reminding shape is fixed
        fixed_note = Text("shape never changes", font=MONO, color=TEAL).scale(0.28)
        fixed_note.next_to(plug_lbl, DOWN, buff=0.18)

        def note_upd(m):
            tt = t.get_value()
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 * np.sin(tt * 1.8)))
        fixed_note.add_updater(note_upd)
        self.add(fixed_note)

        # caption cycles between the two lines
        cap_lines = ["the plug tells you nothing",
                     "check the spec, not the shape"]

        def caption_upd(m):
            idx = int(t.get_value() / 4.5) % len(cap_lines)
            if idx != m._idx:
                m._idx = idx
                col = SECOND if idx == 0 else AMBER
                new = Text(cap_lines[idx], font=HEAD, color=col).scale(0.4)
                new.to_edge(DOWN, buff=0.4)
                new._idx = idx
                m.become(new)
        caption.add_updater(caption_upd)
        self.add(caption)

        self.play(t.animate.set_value(TOTAL), run_time=TOTAL,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
