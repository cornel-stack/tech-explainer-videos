"""Scene: ray tracing — light bounces, frames drop.

Class `Raytrace` (~20s). An amber light source (top-left) emits rays that
travel, bounce off a horizontal "surface" line (a puddle), and reach a
"pixel/camera" (right). The bounce node is labelled "RT core". Multiple rays
are in flight, phase-offset, bouncing forever. Three drawn FPS cost bars
(Standard 90 green, Ray tracing 44 amber, Path tracing 29 coral) encode the
numbers as height, each labelled. Caption: truer light, fewer frames. Bars
pulse; rays keep bouncing. Continuous motion, no freeze.

Dark palette only, TEXT labels only.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #76D64A  red #FF5C47  amber #FFB020  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Text,
    VGroup,
    Dot,
    Line,
    ValueTracker,
    config,
    FadeIn,
    Create,
    GrowFromEdge,
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
AMBER = "#FFB020"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Raytrace(Scene):
    def construct(self):
        title = Text("Ray tracing", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- Geometry --------------------------------------------------------
        src = np.array([-5.6, 2.3, 0])       # light source (top-left)
        bounce = np.array([-0.8, -1.0, 0])   # RT-core bounce point on surface
        cam = np.array([5.4, 1.6, 0])        # camera/pixel (right)
        surf_y = -1.0

        light = Dot(src, color=AMBER, radius=0.16)
        light_glow = Dot(src, color=AMBER, radius=0.32).set_opacity(0.3)
        light_lbl = Text("light", font=MONO, color=AMBER).scale(0.26)
        light_lbl.next_to(light, UP, buff=0.12)

        # Surface / puddle line.
        surface = Line([-6.2, surf_y, 0], [2.4, surf_y, 0],
                       stroke_color=SILVER, stroke_width=3)
        surf_lbl = Text("surface (puddle)", font=MONO, color=SECOND).scale(0.24)
        surf_lbl.next_to(surface, DOWN, buff=0.1).align_to(surface, LEFT)

        # RT core node at the bounce.
        rt_dot = Dot(bounce, color=GREEN, radius=0.1)
        rt_lbl = Text("RT core", font=MONO, color=GREEN,
                      weight="BOLD").scale(0.26)
        rt_lbl.next_to(rt_dot, DOWN, buff=0.12)

        # Camera / pixel.
        cam_box = Rectangle(width=0.5, height=0.5, stroke_color=INK,
                            stroke_width=2.5, fill_color="#16161A",
                            fill_opacity=0.9).move_to(cam)
        cam_lbl = Text("pixel / camera", font=MONO, color=INK).scale(0.24)
        cam_lbl.next_to(cam_box, UP, buff=0.12)

        self.play(FadeIn(light), FadeIn(light_glow), FadeIn(light_lbl),
                  Create(surface), FadeIn(surf_lbl), run_time=0.7)
        self.play(FadeIn(rt_dot), FadeIn(rt_lbl), Create(cam_box),
                  FadeIn(cam_lbl), run_time=0.6)

        # --- FPS cost bars (drawn, not screenshots) --------------------------
        bar_specs = [("Standard", 90, GREEN),
                     ("Ray tracing", 44, AMBER),
                     ("Path tracing", 29, RED)]
        base_y = -3.0
        H_PER = 0.032   # vertical units per fps
        bar_w = 0.8
        xs = [3.4, 4.6, 5.8]
        bars = []
        bar_groups = VGroup()
        for (name, fps, col), bx in zip(bar_specs, xs):
            h = fps * H_PER
            rect = Rectangle(width=bar_w, height=h, stroke_color=col,
                             stroke_width=2, fill_color=col, fill_opacity=0.35)
            rect.move_to([bx, base_y + h / 2, 0])
            num = Text(str(fps), font=MONO, color=col,
                       weight="BOLD").scale(0.3)
            num.next_to(rect, UP, buff=0.08)
            nm = Text(name, font=MONO, color=SECOND).scale(0.2)
            nm.next_to(rect, DOWN, buff=0.1)
            grp = VGroup(rect, num, nm)
            grp.rect = rect
            grp.full_h = h
            grp.col = col
            bar_groups.add(grp)
            bars.append(grp)
        self.play(*[GrowFromEdge(b.rect, DOWN) for b in bars],
                  *[FadeIn(b[1]) for b in bars],
                  *[FadeIn(b[2]) for b in bars], run_time=0.8)

        cap = Text("truer light, fewer frames.", font=HEAD,
                   color=SECOND).scale(0.34)
        cap.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Light glow breathing.
        def glow_upd(m):
            tt = t.get_value()
            m.set_opacity(0.2 + 0.2 * (0.5 + 0.5 * np.sin(2.5 * tt)))
        light_glow.add_updater(glow_upd)

        # RT-core node pulses on each bounce.
        def rt_upd(m):
            tt = t.get_value()
            m.set_opacity(0.5 + 0.5 * (0.5 + 0.5 *
                                       np.sin(2.0 * np.pi * tt / 2.0)) ** 2)
        rt_dot.add_updater(rt_upd)

        # Multiple rays in flight, phase-offset. Each ray is a short bright
        # segment travelling src->bounce then bounce->cam, forever.
        RAY_N = 4
        rays = VGroup()
        ray_meta = []
        for k in range(RAY_N):
            seg = Line(src, src + np.array([0.01, 0, 0]),
                       stroke_color=AMBER, stroke_width=4)
            rays.add(seg)
            period = 2.0
            offset = k * (period / RAY_N)
            ray_meta.append((period, offset))

        def point_on_path(frac):
            # frac in [0,1): first half src->bounce, second half bounce->cam.
            if frac < 0.5:
                f = frac / 0.5
                return src * (1 - f) + bounce * f
            f = (frac - 0.5) / 0.5
            return bounce * (1 - f) + cam * f

        def make_ray(mt):
            period, offset = mt

            def _upd(m):
                frac = ((t.get_value() + offset) % period) / period
                head = point_on_path(frac)
                tail_frac = max(frac - 0.06, 0.0)
                tail = point_on_path(tail_frac)
                m.put_start_and_end_on(tail, head)
                # Amber before bounce, greenish-amber after (energy carried).
                m.set_stroke(color=AMBER if frac < 0.5 else "#B8D64A")
                m.set_opacity(np.clip(1.2 - abs(frac - 0.5) * 1.2, 0.3, 1.0))
            return _upd

        for seg, mt in zip(rays, ray_meta):
            seg.add_updater(make_ray(mt))
        self.add(rays)

        # Bars pulse in height around their true value (number label stays).
        for i, b in enumerate(bars):
            def make_bar_pulse(bb, phase):
                base_h = bb.full_h

                def _upd(m):
                    tt = t.get_value()
                    scale = 1.0 + 0.05 * np.sin(2.5 * tt + phase)
                    new_h = base_h * scale
                    bb.rect.stretch_to_fit_height(new_h)
                    bb.rect.move_to([bb.rect.get_center()[0],
                                     base_y + new_h / 2, 0])
                    bb[1].next_to(bb.rect, UP, buff=0.08)
                return _upd
            b.add_updater(make_bar_pulse(b, i * 1.1))

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
