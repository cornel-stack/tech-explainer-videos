"""Signature scene: decode an Intel CPU product name into its parts.

Class `Decoder` (~26s). A chip NAME is broken into coloured segments; each
segment is highlighted in sequence while its meaning appears below it. Two
naming schemes are decoded the same way — the new "Core Ultra 7 265KF" and
the older "Core i7-14700K" — with a small suffix legend. After the first
pass, a highlight keeps sweeping continuously across the segments.

Silicon-dark palette (no pure blue, no white). IP-safe: TEXT labels only,
no Intel logo/badge, all diagrams original.
  bg      #0A0A0C   ink #E8E9EC   secondary #8C8E92
  accents teal #2DD4BF  green #35E08A  amber #FFB020  coral #FF5C47
          violet #B06BFF  silver #C9CDD4  gold #E8C24A
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Line,
    ValueTracker,
    config,
    FadeIn,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    rate_functions,
)

# --- palette -----------------------------------------------------------------
BG = "#0A0A0C"
INK = "#E8E9EC"
SECOND = "#8C8E92"
TEAL = "#2DD4BF"
GREEN = "#35E08A"
AMBER = "#FFB020"
CORAL = "#FF5C47"
VIOLET = "#B06BFF"
SILVER = "#C9CDD4"
GOLD = "#E8C24A"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


def segment(text, accent, width, height=0.95):
    """A mono-labelled rounded tile with a soft glow behind a crisp stroke."""
    txt = Text(text, font=MONO, color=INK, weight="BOLD").scale(0.62)
    if txt.width > width - 0.3:
        txt.scale((width - 0.3) / txt.width)
    body = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=height,
        stroke_color=accent,
        stroke_width=2.5,
        fill_color="#141417",
        fill_opacity=0.92,
    )
    glow = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=height,
        stroke_color=accent,
        stroke_width=11,
        stroke_opacity=0.14,
        fill_opacity=0,
    )
    g = VGroup(glow, body, txt)
    g.glow = glow
    g.body = body
    g.accent = accent
    return g


class Decoder(Scene):
    def construct(self):
        # --- Title -----------------------------------------------------------
        title = Text("Reading a CPU name", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.62)
        title.to_edge(UP, buff=0.45)
        sub = Text("every part means something", font=HEAD, color=SECOND).scale(0.34)
        sub.next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)

        # --- Scheme definitions ---------------------------------------------
        # Each entry: (segment text, accent, meaning label).
        new_scheme = [
            ("Core Ultra", VIOLET, "BRAND"),
            ("7", AMBER, "TIER"),
            ("2", TEAL, "SERIES / gen"),
            ("65", SILVER, "SKU"),
            ("KF", CORAL, "SUFFIX"),
        ]
        old_scheme = [
            ("Core i7", VIOLET, "BRAND"),
            ("i7", AMBER, "TIER"),
            ("14", TEAL, "GEN"),
            ("700", SILVER, "SKU"),
            ("K", CORAL, "SUFFIX"),
        ]

        def build_row(scheme, y, name_tag):
            """Lay out segments left→right, return (group, segs, meanings)."""
            tag = Text(name_tag, font=HEAD, color=SECOND).scale(0.3)
            widths = []
            for text, _, _ in scheme:
                w = max(0.95, 0.42 * len(text) + 0.55)
                widths.append(w)
            segs = VGroup()
            x = -sum(widths) / 2 - 0.15 * (len(widths) - 1) / 2
            seg_objs = []
            for (text, accent, _), w in zip(scheme, widths):
                s = segment(text, accent, w)
                s.move_to([x + w / 2, y, 0])
                x += w + 0.15
                segs.add(s)
                seg_objs.append(s)
            # Meaning labels below each segment.
            meanings = []
            for (_, accent, meaning), s in zip(scheme, seg_objs):
                m = Text(meaning, font=MONO, color=accent).scale(0.3)
                m.next_to(s, DOWN, buff=0.16)
                meanings.append(m)
            tag.next_to(segs, UP, buff=0.18).align_to(segs, LEFT)
            return segs, seg_objs, meanings, tag

        # New scheme (upper), older scheme (lower).
        new_segs, new_objs, new_means, new_tag = build_row(
            new_scheme, 1.35, "Core Ultra 7 265KF  (new, 2024+)")
        old_segs, old_objs, old_means, old_tag = build_row(
            old_scheme, -1.35, "Core i7-14700K  (older scheme)")

        # --- Build the new-scheme row quickly, decoding in sequence ----------
        self.play(FadeIn(new_tag), run_time=0.3)
        self.play(*[GrowFromCenter(s) for s in new_objs],
                  lag_ratio=0.14, run_time=1.1)

        # Decode each segment: flash its stroke + drop its meaning label.
        for s, m in zip(new_objs, new_means):
            self.play(
                s.body.animate.set_stroke(width=5),
                FadeIn(m, shift=UP * 0.15),
                run_time=0.34,
            )
            self.play(s.body.animate.set_stroke(width=2.5), run_time=0.18)

        # --- Build the older-scheme row the same way -------------------------
        self.play(FadeIn(old_tag), run_time=0.3)
        self.play(*[GrowFromCenter(s) for s in old_objs],
                  lag_ratio=0.14, run_time=0.9)
        for s, m in zip(old_objs, old_means):
            self.play(
                s.body.animate.set_stroke(width=5),
                FadeIn(m, shift=UP * 0.15),
                run_time=0.26,
            )
            self.play(s.body.animate.set_stroke(width=2.5), run_time=0.14)

        # --- Suffix legend ---------------------------------------------------
        legend_lines = [
            ("K", "unlocked"),
            ("F", "no iGPU"),
            ("T", "low-power"),
            ("H / HX", "high-perf mobile"),
            ("U", "ultra-low-power"),
        ]
        legend = VGroup()
        for code, meaning in legend_lines:
            c = Text(code, font=MONO, color=CORAL, weight="BOLD").scale(0.3)
            eq = Text("= " + meaning, font=MONO, color=SECOND).scale(0.3)
            eq.next_to(c, RIGHT, buff=0.14)
            legend.add(VGroup(c, eq))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        legend.to_edge(DOWN, buff=0.4)
        # Divider cue so the legend reads as a side note.
        legend_title = Text("suffix key", font=HEAD, color=SECOND).scale(0.28)
        legend_title.next_to(legend, UP, buff=0.12).align_to(legend, LEFT)
        self.play(FadeIn(legend_title), FadeIn(legend, shift=UP * 0.2),
                  run_time=0.6)
        # Core content fully on screen (~7s in).

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # A master clock drives: a highlight ring sweeping across the new-row
        # segments, a mirrored sweep across the old-row segments, segment glow
        # breathing, and the matching meaning label pulsing as the sweep lands.
        # =====================================================================
        t = ValueTracker(0.0)

        def row_centers(objs):
            return [o.get_center() for o in objs]

        new_centers = row_centers(new_objs)
        old_centers = row_centers(old_objs)
        n = len(new_objs)

        # Sweep highlighter for the new row.
        sweep_new = RoundedRectangle(
            corner_radius=0.14, width=1.0, height=1.12,
            stroke_color=INK, stroke_width=3.5, stroke_opacity=0.0,
            fill_opacity=0,
        )
        sweep_old = RoundedRectangle(
            corner_radius=0.14, width=1.0, height=1.12,
            stroke_color=INK, stroke_width=3.5, stroke_opacity=0.0,
            fill_opacity=0,
        )

        seg_dwell = 0.9  # seconds hovering per segment

        def make_sweep(centers, objs, offset=0.0):
            def _upd(m):
                tt = t.get_value() + offset
                pos = (tt / seg_dwell)
                idx = int(pos) % n
                nxt = (idx + 1) % n
                local = pos % 1.0
                eased = rate_functions.ease_in_out_sine(local)
                c = np.array(centers[idx]) * (1 - eased) + \
                    np.array(centers[nxt]) * eased
                m.move_to(c)
                # Match width to the segment it is currently closest to.
                target = objs[idx] if local < 0.5 else objs[nxt]
                m.stretch_to_fit_width(target.body.width + 0.22)
                m.set_stroke(color=target.accent,
                             opacity=0.3 + 0.45 * np.sin(np.pi * local) ** 2)
            return _upd

        sweep_new.add_updater(make_sweep(new_centers, new_objs, 0.0))
        sweep_old.add_updater(make_sweep(old_centers, old_objs, seg_dwell * 0.5))
        self.add(sweep_new, sweep_old)

        # Segment glow breathing — each tile pulses its glow on its own phase.
        for i, s in enumerate(new_objs + old_objs):
            phase = i * 0.55
            glow = s.glow

            def make_breath(g, ph):
                def _upd(m):
                    tt = t.get_value()
                    g.set_stroke(
                        opacity=0.12 + 0.14 * (0.5 + 0.5 * np.sin(1.8 * tt + ph))
                    )
                return _upd
            s.add_updater(make_breath(glow, phase))

        # Meaning labels brighten as the sweep passes over their segment.
        def make_label_pulse(label, index, offset):
            base = label.get_fill_color()

            def _upd(m):
                tt = t.get_value() + offset
                pos = (tt / seg_dwell)
                active = int(pos) % n
                local = pos % 1.0
                near = (active == index and local > 0.25) or \
                       ((active + 1) % n == index and local > 0.75)
                m.set_opacity(0.95 if near else 0.5)
            return _upd

        for i, m in enumerate(new_means):
            m.add_updater(make_label_pulse(m, i, 0.0))
        for i, m in enumerate(old_means):
            m.add_updater(make_label_pulse(m, i, seg_dwell * 0.5))

        # Legend codes flicker softly so even the side note keeps moving.
        for i, grp in enumerate(legend):
            code = grp[0]

            def make_flick(c, ph):
                def _upd(m):
                    tt = t.get_value()
                    c.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                                               np.sin(2.4 * tt + ph)))
                return _upd
            code.add_updater(make_flick(code, i * 0.8))

        # Drive ~18s of unbroken motion (several full sweeps of both rows).
        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        # Clean stop so the final frame isn't mid-pulse.
        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
