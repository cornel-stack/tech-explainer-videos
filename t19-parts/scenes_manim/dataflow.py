"""Scene: how the parts cooperate on one task — opening a photo.

Class `Dataflow` (~18s). Labelled part nodes laid in a path:
MOUSE -> CPU -> STORAGE -> RAM -> CPU -> GPU -> MONITOR, with a PSU node at
the bottom feeding power lines up to all parts and FANS cooling. A single
glowing PACKET travels the path in order on a loop: click at the mouse, to
CPU, CPU asks storage, file goes to RAM, CPU processes, hands to GPU, GPU
draws, image appears on the monitor. Each node lights as the packet passes;
the PSU power lines pulse throughout.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92  green #35E08A  teal #2DD4BF
  violet #B06BFF  amber #FFB020  coral #FF5C47  gold #E8C24A  silver #C9CDD4
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
    interpolate_color,
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


class Dataflow(Scene):
    def construct(self):
        title = Text("One click to an image — the parts cooperate",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.5)
        title.to_edge(UP, buff=0.38)
        self.play(FadeIn(title, shift=DOWN * 0.25), run_time=0.6)

        # --- Node layout -----------------------------------------------------
        # name : (x, y), colour
        NODE_SPEC = [
            ("MOUSE",   (-6.0,  1.6), SILVER),
            ("CPU",     (-3.0,  1.6), AMBER),
            ("STORAGE", (-3.0, -1.0), GOLD),
            ("RAM",     (0.3,   1.6), CORAL),
            ("GPU",     (3.2,   1.6), GREEN),
            ("MONITOR", (6.0,   1.6), TEAL),
        ]

        nodes = {}
        for name, (x, y), col in NODE_SPEC:
            body = RoundedRectangle(
                corner_radius=0.1, width=1.9, height=1.0,
                stroke_color=col, stroke_width=2.2,
                fill_color="#101014", fill_opacity=0.92,
            ).move_to(np.array([x, y, 0]))
            glow = RoundedRectangle(
                corner_radius=0.1, width=1.9, height=1.0,
                stroke_color=col, stroke_width=9, stroke_opacity=0.0,
                fill_opacity=0,
            ).move_to(body)
            lbl = Text(name, font=MONO, color=col).scale(0.26)
            lbl.move_to(body)
            nodes[name] = {
                "grp": VGroup(glow, body, lbl), "glow": glow,
                "body": body, "col": col, "center": body.get_center(),
            }

        # --- The ordered path (CPU and STORAGE appear twice) -----------------
        PATH = ["MOUSE", "CPU", "STORAGE", "RAM", "CPU", "GPU", "MONITOR"]
        path_pts = [nodes[n]["center"] for n in PATH]

        # Flow lines connecting consecutive path stops.
        flow_lines = VGroup()
        for a, b in zip(path_pts[:-1], path_pts[1:]):
            ln = Line(a, b, stroke_color=SECOND, stroke_width=1.6,
                      stroke_opacity=0.4)
            flow_lines.add(ln)

        # --- PSU at bottom + power lines up to every physical part ----------
        psu_body = RoundedRectangle(
            corner_radius=0.1, width=2.4, height=1.0,
            stroke_color=SILVER, stroke_width=2.2,
            fill_color="#101014", fill_opacity=0.92,
        ).move_to(np.array([-1.3, -3.0, 0]))
        psu_lbl = Text("PSU", font=MONO, color=SILVER).scale(0.26)
        psu_lbl.move_to(psu_body)
        psu = {"grp": VGroup(psu_body, psu_lbl), "body": psu_body,
               "center": psu_body.get_center()}

        powered = ["CPU", "STORAGE", "RAM", "GPU", "MONITOR"]
        power_lines = VGroup()
        for nm in powered:
            ln = Line(psu_body.get_top(), nodes[nm]["body"].get_bottom(),
                      stroke_color=GREEN, stroke_width=1.6,
                      stroke_opacity=0.25)
            power_lines.add(ln)

        # --- FANS node cooling (bottom-right) --------------------------------
        fans_body = RoundedRectangle(
            corner_radius=0.1, width=1.9, height=1.0,
            stroke_color=VIOLET, stroke_width=2.2,
            fill_color="#101014", fill_opacity=0.92,
        ).move_to(np.array([3.2, -3.0, 0]))
        fans_lbl = Text("FANS", font=MONO, color=VIOLET).scale(0.26)
        fans_lbl.move_to(fans_body)
        fan_blades = VGroup()
        fc = fans_body.get_center()
        for k in range(3):
            ang0 = k * (2 * np.pi / 3)
            blade = Line(fc, fc + np.array([0.3, 0, 0]),
                         stroke_color=VIOLET, stroke_width=3)
            blade._ang0 = ang0
            fan_blades.add(blade)
        fans = {"grp": VGroup(fans_body, fans_lbl), "center": fc}

        # Reveal.
        self.play(Create(flow_lines), Create(power_lines), run_time=0.8)
        self.play(*[FadeIn(nodes[n]["grp"]) for n in nodes],
                  FadeIn(psu["grp"]), FadeIn(fans["grp"]),
                  lag_ratio=0.05, run_time=1.0)
        self.add(fan_blades)

        caption = Text("from a click to an image — "
                       "every part playing its position",
                       font=HEAD, color=SECOND).scale(0.3)
        caption.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.5)

        # Step labels that sit along the path describing the handoff.
        STEP_TXT = [
            "click", "read request", "load file",
            "process", "render", "display",
        ]

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        n_seg = len(path_pts) - 1          # 6 segments
        LOOP = 12.0                        # full journey + pause.
        TRAVEL = 9.6                       # time spent moving.
        seg_dur = TRAVEL / n_seg

        GREEN_C = ManimColor(GREEN)

        # Helper: current segment index and frac along it (0 if paused).
        def path_state(tt):
            cyc = tt % LOOP
            if cyc >= TRAVEL:
                return n_seg, 1.0          # parked at monitor during pause.
            seg = int(cyc // seg_dur)
            frac = (cyc - seg * seg_dur) / seg_dur
            return seg, frac

        def packet_pos(tt):
            seg, frac = path_state(tt)
            if seg >= n_seg:
                return path_pts[-1]
            a = path_pts[seg]
            b = path_pts[seg + 1]
            e = rate_functions.ease_in_out_quad(frac)
            return a * (1 - e) + b * e

        # Glowing packet (core dot + halo).
        halo = Dot(color=GREEN, radius=0.22, fill_opacity=0.28)
        core = Dot(color=INK, radius=0.09)
        packet = VGroup(halo, core)

        def packet_upd(m):
            tt = t.get_value()
            m.move_to(packet_pos(tt))
            halo.set_opacity(0.2 + 0.2 * (0.5 + 0.5 * np.sin(6.0 * tt)))
        packet.add_updater(packet_upd)
        self.add(packet)

        # Light each node when the packet is on/arriving at it.
        def make_node_updater(nm, col):
            base = ManimColor(col)
            node = nodes[nm]
            glow = node["glow"]
            body = node["body"]
            # which path indices correspond to this node
            idxs = [i for i, p in enumerate(PATH) if p == nm]

            def _upd(m):
                tt = t.get_value()
                seg, frac = path_state(tt)
                # progress measured in path-index space (0..n_seg)
                prog = seg + frac
                # proximity to any visit of this node
                lit = 0.0
                for idx in idxs:
                    d = abs(prog - idx)
                    lit = max(lit, np.clip(1.0 - d / 0.55, 0.0, 1.0))
                glow.set_stroke(opacity=0.08 + 0.55 * lit)
                body.set_stroke(color=interpolate_color(base, GREEN_C, lit))
            return _upd

        for name, _, col in NODE_SPEC:
            nodes[name]["grp"].add_updater(make_node_updater(name, col))

        # Flow lines: the active segment glows green and flows.
        def make_line_updater(seg_i, ln):
            def _upd(m):
                tt = t.get_value()
                seg, frac = path_state(tt)
                active = 1.0 if seg == seg_i else 0.0
                ln.set_stroke(
                    color=interpolate_color(ManimColor(SECOND), GREEN_C,
                                            active),
                    opacity=0.3 + 0.6 * active)
            return _upd

        for i, ln in enumerate(flow_lines):
            ln.add_updater(make_line_updater(i, ln))

        # PSU power lines pulse throughout (travelling brightness).
        for i, ln in enumerate(power_lines):
            def make_pwr(idx, line):
                def _upd(m):
                    tt = t.get_value()
                    pulse = 0.5 + 0.5 * np.sin(3.5 * tt - idx * 0.9)
                    line.set_stroke(opacity=0.2 + 0.5 * pulse)
                return _upd
            ln.add_updater(make_pwr(i, ln))

        def psu_upd(m):
            tt = t.get_value()
            m.set_stroke(opacity=0.7 + 0.3 * (0.5 + 0.5 * np.sin(3.5 * tt)))
        psu_body.add_updater(psu_upd)

        # Fan blades spin continuously.
        for blade in fan_blades:
            def make_spin(bl):
                a0 = bl._ang0
                center = fc

                def _upd(m):
                    tt = t.get_value()
                    ang = a0 + 4.0 * tt
                    end = center + 0.34 * np.array(
                        [np.cos(ang), np.sin(ang), 0])
                    bl.put_start_and_end_on(center + 0.001 * np.array(
                        [np.cos(ang), np.sin(ang), 0]), end)
                return _upd
            blade.add_updater(make_spin(blade))

        # Step caption cycles with the packet's current segment.
        step = Text(STEP_TXT[0], font=MONO, color=GREEN).scale(0.3)
        step.next_to(title, DOWN, buff=0.12)
        step._idx = -1

        def step_upd(m):
            seg, frac = path_state(t.get_value())
            idx = min(seg, len(STEP_TXT) - 1)
            if idx != m._idx:
                m._idx = idx
                new = Text(STEP_TXT[idx], font=MONO, color=GREEN).scale(0.3)
                new.move_to(m)
                m.become(new)
        step.add_updater(step_upd)
        self.add(step)

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
