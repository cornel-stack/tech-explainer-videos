"""Scene: the resolution ladder — drawn to TRUE relative scale.

Class `Ladder` (~20s). Nested/stacked rectangles for 360p, 480p, 720p, 1080p,
1440p, 4K, 8K, each sized by its real pixel dimensions relative to 8K
(7680x4320) and sharing a common bottom-left corner so each bigger resolution
visibly contains the smaller ones — Russian dolls of rectangles. Each step is
labelled with its name and pixel count. A caption reinforces that each step
roughly doubles the pixels.

Continuous motion: a highlight sweep travels outward from the smallest to the
largest rectangle on a loop; the active rectangle's border brightens and its
label pulses; a "x pixels vs 1080p" readout updates as the sweep passes each
tier (1x -> 2x -> 4x -> 16x).

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Text,
    VGroup,
    ValueTracker,
    config,
    FadeIn,
    Create,
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


class Ladder(Scene):
    def construct(self):
        title = Text("The resolution ladder, to true scale",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the tiers: real pixel dims, ordered small -> large --------------
        # (name, width_px, height_px, color)
        tiers = [
            ("360p", 640, 360, SILVER),
            ("480p", 854, 480, TEAL),
            ("720p", 1280, 720, GREEN),
            ("1080p", 1920, 1080, AMBER),
            ("1440p", 2560, 1440, VIOLET),
            ("4K", 3840, 2160, CORAL),
            ("8K", 7680, 4320, GOLD),
        ]

        # Reference: 8K is the largest; scale everything so 8K fits the frame.
        ref_w, ref_h = 7680.0, 4320.0
        # On-screen footprint of the full 8K rectangle.
        BOX_W, BOX_H = 8.6, 4.84  # 16:9, leaves room for title + caption
        px_per_unit_x = ref_w / BOX_W
        px_per_unit_y = ref_h / BOX_H

        # Shared bottom-left anchor so each bigger box contains the smaller.
        anchor = np.array([-BOX_W / 2.0 - 1.0, -BOX_H / 2.0 - 0.35, 0.0])

        mp_1080 = 1920 * 1080  # pixel baseline for the "vs 1080p" readout

        rects = []
        name_labels = []
        px_labels = []
        tier_meta = []  # (name, color, w_units, h_units, megapixels, mult)

        for name, w_px, h_px, color in tiers:
            w_u = w_px / px_per_unit_x
            h_u = h_px / px_per_unit_y
            rect = Rectangle(
                width=w_u, height=h_u,
                stroke_color=color, stroke_width=2.2,
                fill_color=color, fill_opacity=0.04,
            )
            # Align bottom-left corner to the shared anchor.
            rect.move_to(anchor + np.array([w_u / 2.0, h_u / 2.0, 0.0]))
            rects.append(rect)

            mp = (w_px * h_px) / 1_000_000.0
            if mp >= 10:
                mp_txt = f"{mp:.0f} MP"
            else:
                mp_txt = f"{mp:.1f} MP"

            mult = (w_px * h_px) / mp_1080

            # Name label pinned to the top-right corner of each box.
            nm = Text(name, font=MONO, color=color,
                      weight="BOLD").scale(0.3)
            px = Text(mp_txt, font=MONO, color=color).scale(0.22)
            corner = rect.get_corner(UP + RIGHT)
            nm.next_to(corner, RIGHT, buff=0.12)
            px.next_to(nm, DOWN, buff=0.06).align_to(nm, LEFT)
            name_labels.append(nm)
            px_labels.append(px)

            tier_meta.append((name, color, w_u, h_u, mp, mult))

        rects_g = VGroup(*rects)

        # Draw largest-first so the small boxes land on top visually.
        self.play(*[Create(r) for r in reversed(rects)],
                  lag_ratio=0.12, run_time=1.6)
        self.play(*[FadeIn(n) for n in name_labels],
                  *[FadeIn(p) for p in px_labels],
                  lag_ratio=0.05, run_time=0.9)

        # --- caption ---------------------------------------------------------
        cap = Text("each step roughly doubles the pixels", font=HEAD,
                   color=SECOND).scale(0.34)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # --- "x pixels vs 1080p" readout, top-left -------------------------
        readout = Text("1x pixels vs 1080p", font=MONO,
                       color=INK).scale(0.4)
        readout.to_corner(UP + LEFT, buff=0.5).shift(DOWN * 0.1)
        self.add(readout)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        n_tiers = len(tiers)
        LOOP = 7.0  # seconds for one full outward sweep
        base_sw = 2.2
        base_nm_scale = 0.3

        # Capture starting label geometry as locals for the pulse updaters.
        nm_centers = [n.get_center() for n in name_labels]

        def active_index(tt):
            # Sweep progresses outward through the tiers on a loop.
            phase = (tt % LOOP) / LOOP
            return int(phase * n_tiers) % n_tiers

        # Border brightness: each rectangle brightens when it's the active one.
        for i, rect in enumerate(rects):
            color_i = tier_meta[i][1]

            def make_border(r, col, idx):
                def _upd(m):
                    act = active_index(t.get_value())
                    # Distance from active tier, wrapped; nearer => brighter.
                    d = (idx - act) % n_tiers
                    d = min(d, n_tiers - d)
                    glow = max(0.0, 1.0 - d / 2.0)
                    r.set_stroke(color=col, width=base_sw + 4.5 * glow)
                    r.set_fill(col, opacity=0.04 + 0.14 * glow)
                return _upd
            rect.add_updater(make_border(rect, color_i, i))

        # Label pulse: active tier's name label swells and brightens.
        for i, nm in enumerate(name_labels):
            def make_pulse(label, center, idx):
                def _upd(m):
                    act = active_index(t.get_value())
                    phase = (t.get_value() % LOOP) / LOOP
                    local = phase * n_tiers - act  # 0..1 within active slot
                    if idx == act:
                        s = 0.5 - 0.5 * np.cos(2.0 * np.pi * local)
                        label.scale_to_fit_height(
                            _H0[idx] * (1.0 + 0.35 * s))
                        label.move_to(center)
                        label.set_opacity(0.6 + 0.4 * s)
                    else:
                        label.scale_to_fit_height(_H0[idx])
                        label.move_to(center)
                        label.set_opacity(0.85)
                return _upd
            # defer attaching until _H0 captured below
            nm._pulse_factory = (make_pulse, nm_centers[i], i)

        # Capture original label heights for stable pulsing.
        _H0 = [n.height for n in name_labels]
        for nm in name_labels:
            factory, center, idx = nm._pulse_factory
            nm.add_updater(factory(nm, center, idx))

        # Readout updates as the sweep passes each tier.
        readout_pos = readout.get_center()

        def readout_upd(m):
            act = active_index(t.get_value())
            name, color, _w, _h, mp, mult = tier_meta[act]
            if mult >= 2:
                mtxt = f"{mult:.0f}x"
            else:
                mtxt = "1x"
            new = Text(f"{name}  ·  {mtxt} pixels vs 1080p",
                       font=MONO, color=color).scale(0.4)
            new.move_to(readout_pos, aligned_edge=LEFT)
            m.become(new)
        readout.become(
            Text("360p  ·  1x pixels vs 1080p", font=MONO,
                 color=SILVER).scale(0.4).move_to(readout_pos,
                                                  aligned_edge=LEFT))
        readout.add_updater(readout_upd)

        # Caption gentle breathe.
        def cap_upd(m):
            m.set_opacity(0.55 + 0.35 * (0.5 + 0.5 *
                                         np.sin(t.get_value() * 1.1)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
