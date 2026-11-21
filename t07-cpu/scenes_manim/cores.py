"""Primer scene: the hybrid CPU die — P-cores vs E-cores.

Class `Cores` (~24s). A CPU die outline holds TILES: a few LARGE "P-CORE"
tiles (performance), each showing two small queues inside (= hyperthreading,
two threads per core), and several SMALL "E-CORE" tiles (efficiency, one
thread). Tasks flow in continuously — big tasks route to P-cores, background
tasks to E-cores. Nothing ever freezes.

Silicon-dark palette (no pure blue, no white). IP-safe: TEXT labels only,
original diagram.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  amber #FFB020 (P)  teal #2DD4BF (E)  violet #B06BFF  coral #FF5C47
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Dot,
    Line,
    ValueTracker,
    config,
    FadeIn,
    GrowFromCenter,
    Create,
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
AMBER = "#FFB020"
TEAL = "#2DD4BF"
VIOLET = "#B06BFF"
CORAL = "#FF5C47"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"

config.background_color = BG


class Cores(Scene):
    def construct(self):
        # --- Title -----------------------------------------------------------
        title = Text("One die, two kinds of core", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.6)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- Die outline -----------------------------------------------------
        die = RoundedRectangle(
            corner_radius=0.18, width=9.6, height=5.4,
            stroke_color=SILVER, stroke_width=2.5,
            fill_color="#111114", fill_opacity=0.5,
        ).shift(DOWN * 0.3)
        die_glow = RoundedRectangle(
            corner_radius=0.18, width=9.6, height=5.4,
            stroke_color=SILVER, stroke_width=10, stroke_opacity=0.08,
            fill_opacity=0,
        ).move_to(die)
        die_label = Text("CPU die", font=MONO, color=SECOND).scale(0.3)
        die_label.next_to(die, UP, buff=0.1).align_to(die, LEFT).shift(RIGHT * 0.2)
        self.play(Create(die), FadeIn(die_glow), run_time=0.8)
        self.play(FadeIn(die_label), run_time=0.3)

        # --- P-core tiles (two per column, left side) ------------------------
        p_tiles = []
        p_queue_dots = []  # per tile: (dot_a, dot_b) that pulse = 2 threads

        def make_pcore():
            tile = RoundedRectangle(
                corner_radius=0.12, width=2.0, height=2.0,
                stroke_color=AMBER, stroke_width=2.5,
                fill_color="#1A160D", fill_opacity=0.9,
            )
            glow = RoundedRectangle(
                corner_radius=0.12, width=2.0, height=2.0,
                stroke_color=AMBER, stroke_width=10, stroke_opacity=0.12,
                fill_opacity=0,
            ).move_to(tile)
            lbl = Text("P-CORE", font=MONO, color=AMBER, weight="BOLD").scale(0.34)
            lbl.move_to(tile.get_top() + DOWN * 0.34)
            # Two thread queues inside = hyperthreading.
            q1 = RoundedRectangle(corner_radius=0.05, width=1.4, height=0.34,
                                  stroke_color=AMBER, stroke_width=1.5,
                                  fill_opacity=0)
            q2 = q1.copy()
            q1.move_to(tile.get_center() + DOWN * 0.05)
            q2.move_to(tile.get_center() + DOWN * 0.52)
            d1 = Dot(color=AMBER, radius=0.06).move_to(q1.get_left() + RIGHT * 0.2)
            d2 = Dot(color=AMBER, radius=0.06).move_to(q2.get_left() + RIGHT * 0.2)
            thr = Text("2 threads", font=MONO, color=SECOND).scale(0.22)
            thr.move_to(tile.get_center() + UP * 0.42)
            grp = VGroup(glow, tile, lbl, thr, q1, q2, d1, d2)
            grp.tile = tile
            grp.glow = glow
            grp.q1 = q1
            grp.q2 = q2
            grp.d1 = d1
            grp.d2 = d2
            return grp

        p_positions = [
            np.array([-3.1, 0.55, 0]),
            np.array([-3.1, -1.65, 0]),
        ]
        for pos in p_positions:
            pc = make_pcore()
            pc.move_to(pos)
            p_tiles.append(pc)
            p_queue_dots.append((pc.d1, pc.d2, pc.q1, pc.q2))

        # --- E-core tiles (small grid, right side) ---------------------------
        e_tiles = []

        def make_ecore():
            tile = RoundedRectangle(
                corner_radius=0.08, width=0.95, height=0.95,
                stroke_color=TEAL, stroke_width=2,
                fill_color="#0C1917", fill_opacity=0.9,
            )
            glow = RoundedRectangle(
                corner_radius=0.08, width=0.95, height=0.95,
                stroke_color=TEAL, stroke_width=8, stroke_opacity=0.12,
                fill_opacity=0,
            ).move_to(tile)
            lbl = Text("E", font=MONO, color=TEAL, weight="BOLD").scale(0.3)
            lbl.move_to(tile.get_center())
            d = Dot(color=TEAL, radius=0.05).move_to(tile.get_bottom() + UP * 0.2)
            grp = VGroup(glow, tile, lbl, d)
            grp.tile = tile
            grp.glow = glow
            grp.d = d
            return grp

        e_group = VGroup()
        for _ in range(8):
            e_group.add(make_ecore())
        e_group.arrange_in_grid(rows=2, cols=4, buff=0.22)
        e_group.move_to([1.7, -0.5, 0])
        for e in e_group:
            e_tiles.append(e)

        # Build tiles quickly.
        self.play(*[GrowFromCenter(p) for p in p_tiles],
                  lag_ratio=0.2, run_time=1.0)
        self.play(*[GrowFromCenter(e) for e in e_tiles],
                  lag_ratio=0.08, run_time=1.0)

        # --- Captions --------------------------------------------------------
        cap_p = Text("P-cores: big, fast, hyperthreaded", font=HEAD,
                     color=AMBER).scale(0.32)
        cap_e = Text("E-cores: small, efficient", font=HEAD,
                     color=TEAL).scale(0.32)
        cap_p.to_edge(DOWN, buff=0.55).shift(LEFT * 3.0)
        cap_e.to_edge(DOWN, buff=0.55).shift(RIGHT * 3.0)
        self.play(FadeIn(cap_p, shift=UP * 0.2), FadeIn(cap_e, shift=UP * 0.2),
                  run_time=0.6)
        # Core layout on screen (~6.5s in).

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # Tasks spawn at the top edge and fly into cores: big amber tasks go to
        # P-cores, small teal background tasks go to E-cores. Thread dots inside
        # P-cores slide along their two queues (hyperthreading). Glows breathe.
        # A master clock drives everything.
        # =====================================================================
        t = ValueTracker(0.0)

        # P-core thread dots sweep along their queues (two per core, offset).
        for i, (d1, d2, q1, q2) in enumerate(p_queue_dots):
            l1, r1 = q1.get_left()[0] + 0.18, q1.get_right()[0] - 0.18
            l2, r2 = q2.get_left()[0] + 0.18, q2.get_right()[0] - 0.18
            y1, y2 = q1.get_center()[1], q2.get_center()[1]
            ph = i * 0.9

            def make_thread(d, lo, hi, yy, phase, speed):
                def _upd(m):
                    frac = 0.5 - 0.5 * np.cos(t.get_value() * speed + phase)
                    m.move_to([lo + (hi - lo) * frac, yy, 0])
                return _upd
            d1.add_updater(make_thread(d1, l1, r1, y1, ph, 2.2))
            d2.add_updater(make_thread(d2, l2, r2, y2, ph + 1.3, 2.0))

        # Glow breathing on every tile.
        for i, g in enumerate(p_tiles + e_tiles):
            glow = g.glow

            def make_breath(gl, phase):
                def _upd(m):
                    tt = t.get_value()
                    gl.set_stroke(opacity=0.1 + 0.12 *
                                  (0.5 + 0.5 * np.sin(1.7 * tt + phase)))
                return _upd
            g.add_updater(make_breath(glow, i * 0.6))

        # E-core activity dots blink as background work lands.
        for i, e in enumerate(e_tiles):
            dot = e.d

            def make_blink(dd, phase):
                def _upd(m):
                    tt = t.get_value()
                    dd.set_opacity(0.3 + 0.7 *
                                   (0.5 + 0.5 * np.sin(2.8 * tt + phase)) ** 2)
                return _upd
            dot.add_updater(make_blink(dot, i * 0.8))

        # --- Flowing task packets -------------------------------------------
        # Spawn point along the top of the die.
        spawn_y = die.get_top()[1] - 0.15
        p_targets = [p.get_center() for p in p_tiles]
        e_targets = [e.get_center() for e in e_tiles]

        packets = VGroup()
        PACKET_N = 10
        packet_meta = []  # (period, offset, spawn_x, target, is_big)
        rng = np.random.default_rng(7)
        for k in range(PACKET_N):
            is_big = (k % 3 == 0)  # ~1/3 are big "foreground" tasks
            if is_big:
                target = p_targets[k % len(p_targets)]
                col = AMBER
                rad = 0.11
            else:
                target = e_targets[k % len(e_targets)]
                col = TEAL
                rad = 0.07
            dot = Dot(color=col, radius=rad)
            packets.add(dot)
            period = 2.4 + 0.5 * (k % 4)
            offset = rng.uniform(0, period)
            spawn_x = float(rng.uniform(die.get_left()[0] + 1.0,
                                        die.get_right()[0] - 1.0))
            packet_meta.append((period, offset, spawn_x, np.array(target),
                                is_big, col))

        def make_packet(dot, meta):
            period, offset, sx, target, is_big, col = meta
            start = np.array([sx, spawn_y, 0])

            def _upd(m):
                tt = (t.get_value() + offset) % period
                frac = tt / period
                eased = rate_functions.ease_in_out_quad(min(frac * 1.15, 1.0))
                pos = start * (1 - eased) + target * eased
                m.move_to(pos)
                # Fade out as it is absorbed by the core.
                m.set_opacity(np.clip(1.4 * (1 - frac) + 0.1, 0.0, 1.0))
            return _upd

        for dot, meta in zip(packets, packet_meta):
            dot.add_updater(make_packet(dot, meta))
        self.add(packets)

        # "big → P, bg → E" routing hint that pulses.
        hint = Text("big tasks → P   ·   background → E", font=MONO,
                    color=SECOND).scale(0.26)
        hint.next_to(title, DOWN, buff=0.12)

        def hint_upd(m):
            m.set_opacity(0.45 + 0.45 * (0.5 + 0.5 *
                                         np.sin(t.get_value() * 1.6)))
        hint.add_updater(hint_upd)
        self.add(hint)

        # Drive ~16.5s of unbroken flow.
        self.play(t.animate.set_value(16.5), run_time=16.5,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
