"""Scene: Fix — move the signal closer, or run a wire.

Class `Fix` (~20s). The house floorplan again, fixed: a router placed central
and high ("central, in the open") plus 2 mesh nodes spread through the house;
signal now fills every room GREEN including the bedroom. A device hands off
(a marker hops from one node's coverage to the next as it moves). An ethernet
cable (straight line) runs to a desktop. A small crossed-out "router in a
cabinet" inset.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    Rectangle,
    Line,
    Circle,
    Text,
    VGroup,
    RoundedRectangle,
    Dot,
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


class Fix(Scene):
    def construct(self):
        title = Text("Move the signal closer - or run a wire",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- floorplan (same layout as walls) -------------------------------
        hw, hh = 10.0, 5.0
        cx, cy = 0.0, -0.5
        left = cx - hw / 2
        right = cx + hw / 2
        bottom = cy - hh / 2
        top = cy + hh / 2

        house = Rectangle(width=hw, height=hh, stroke_color=SILVER,
                          stroke_width=3.0, fill_color="#0C0D10",
                          fill_opacity=0.6).move_to([cx, cy, 0])

        midx = cx
        midy = cy
        vwall_top = Line([midx, top, 0], [midx, cy + 0.7, 0],
                         stroke_color=SILVER, stroke_width=6)
        vwall_bot = Line([midx, cy - 0.7, 0], [midx, bottom, 0],
                         stroke_color=SILVER, stroke_width=6)
        hwall_l = Line([midx, midy, 0], [midx - 2.3, midy, 0],
                       stroke_color=SILVER, stroke_width=6)
        hwall_r = Line([right, midy, 0], [midx + 1.0, midy, 0],
                       stroke_color=SILVER, stroke_width=6)
        walls = VGroup(vwall_top, vwall_bot, hwall_l, hwall_r)

        living_lbl = Text("Living room", font=MONO, color=SILVER).scale(0.28)
        living_lbl.move_to([left + 2.4, top - 0.4, 0])
        hall_lbl = Text("Hall", font=MONO, color=SILVER).scale(0.28)
        hall_lbl.move_to([left + 2.4, bottom + 0.4, 0])
        kitchen_lbl = Text("Kitchen", font=MONO, color=SILVER).scale(0.28)
        kitchen_lbl.move_to([right - 2.3, top - 0.4, 0])
        bedroom_lbl = Text("Bedroom", font=MONO, color=GREEN).scale(0.28)
        bedroom_lbl.move_to([right - 2.3, bottom + 0.4, 0])

        self.play(Create(house), Create(walls), run_time=0.9)
        self.play(FadeIn(living_lbl), FadeIn(hall_lbl),
                  FadeIn(kitchen_lbl), FadeIn(bedroom_lbl), run_time=0.4)

        # --- central router + 2 mesh nodes ----------------------------------
        router_pos = np.array([cx - 0.5, cy + 0.9, 0.0])
        mesh1_pos = np.array([left + 1.8, bottom + 0.9, 0.0])
        mesh2_pos = np.array([right - 1.8, bottom + 0.9, 0.0])
        nodes = [router_pos, mesh1_pos, mesh2_pos]

        r_body = RoundedRectangle(
            corner_radius=0.06, width=0.5, height=0.34,
            stroke_color=GREEN, stroke_width=2.2,
            fill_color="#0A1711", fill_opacity=1.0,
        ).move_to(router_pos)
        r_lbl = Text("central, in the open", font=MONO, color=GREEN).scale(0.24)
        r_lbl.next_to(r_body, UP, buff=0.12)

        mesh_bodies = VGroup()
        for mp in (mesh1_pos, mesh2_pos):
            mb = RoundedRectangle(
                corner_radius=0.05, width=0.36, height=0.26,
                stroke_color=TEAL, stroke_width=2.0,
                fill_color="#0A1716", fill_opacity=1.0,
            ).move_to(mp)
            mesh_bodies.add(mb)
        mesh_lbl = Text("mesh node", font=MONO, color=TEAL).scale(0.22)
        mesh_lbl.next_to(mesh_bodies[1], DOWN, buff=0.1)

        self.play(Create(r_body), FadeIn(r_lbl),
                  *[Create(m) for m in mesh_bodies], FadeIn(mesh_lbl),
                  run_time=0.6)

        # --- ethernet cable to a desktop ------------------------------------
        desktop = RoundedRectangle(
            corner_radius=0.05, width=0.55, height=0.4,
            stroke_color=GOLD, stroke_width=2.0,
            fill_color="#17140A", fill_opacity=1.0,
        ).move_to([left + 1.6, top - 1.3, 0])
        cable = Line(router_pos, desktop.get_center(),
                     stroke_color=GOLD, stroke_width=2.5)
        eth_lbl = Text("ethernet", font=MONO, color=GOLD).scale(0.22)
        eth_lbl.next_to(cable.get_center(), UP, buff=0.08)
        self.play(Create(cable), Create(desktop), FadeIn(eth_lbl),
                  run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # green coverage rings pulsing from each node (fills every room)
        for ni, np_pos in enumerate(nodes):
            for k in range(3):
                col = GREEN if ni == 0 else TEAL
                ring = Circle(radius=0.3, stroke_color=col, stroke_width=2.5,
                              fill_opacity=0).move_to(np_pos)

                def make_ring(origin, colour, phase):
                    def _upd(m):
                        period = 2.6
                        tt = (t.get_value() + phase) % period
                        frac = tt / period
                        m.set(width=0.5 + frac * 4.2)
                        m.move_to(origin)
                        m.set_stroke(colour,
                                     opacity=np.clip((1 - frac) * 0.6,
                                                     0.04, 0.6))
                    return _upd
                ring.add_updater(make_ring(np_pos, col, ni * 0.5 + k * 0.86))
                self.add(ring)

        # soft green tint fill over the whole house (now covered)
        glow = Rectangle(width=hw - 0.1, height=hh - 0.1, stroke_width=0,
                         fill_color=GREEN, fill_opacity=0.05).move_to([cx, cy, 0])

        def glow_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 1.8)
            m.set_fill(GREEN, opacity=0.04 + 0.05 * s)
        glow.add_updater(glow_upd)
        self.add(glow)

        # handoff marker: a device hops between node coverages as it moves
        waypoints = [router_pos, mesh2_pos,
                     np.array([right - 2.3, bottom + 0.9, 0.0]),
                     mesh1_pos]
        marker = Dot(radius=0.11, color=AMBER)
        marker_ring = Circle(radius=0.22, stroke_color=AMBER, stroke_width=2.0,
                             fill_opacity=0)

        def marker_pos(tt):
            period = 8.0
            frac = (tt % period) / period
            n = len(waypoints)
            seg = frac * n
            i0 = int(seg) % n
            i1 = (i0 + 1) % n
            local = seg - int(seg)
            smooth = 0.5 - 0.5 * np.cos(np.pi * local)
            return waypoints[i0] * (1 - smooth) + waypoints[i1] * smooth

        def marker_upd(m):
            m.move_to(marker_pos(t.get_value()))
        marker.add_updater(marker_upd)

        def marker_ring_upd(m):
            m.move_to(marker_pos(t.get_value()))
            s = 0.5 + 0.5 * np.sin(t.get_value() * 5.0)
            m.set(width=0.35 + 0.15 * s)
            m.set_stroke(AMBER, opacity=0.4 + 0.4 * s)
        marker_ring.add_updater(marker_ring_upd)
        self.add(marker_ring, marker)

        dev_lbl = Text("device", font=MONO, color=AMBER).scale(0.2)

        def dev_lbl_upd(m):
            m.move_to(marker_pos(t.get_value()) + DOWN * 0.3)
        dev_lbl.add_updater(dev_lbl_upd)
        self.add(dev_lbl)

        # router glow
        def router_glow(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 4.0)
            m.set_stroke(GREEN, opacity=0.6 + 0.4 * s)
        r_body.add_updater(router_glow)

        # --- "bad: router in a cabinet" crossed-out inset -------------------
        inset = RoundedRectangle(
            corner_radius=0.08, width=2.2, height=1.0,
            stroke_color=CORAL, stroke_width=1.5,
            fill_color="#17090A", fill_opacity=0.5,
        ).move_to([right - 1.3, top + 1.0, 0])
        inset_lbl = Text("bad: in a cabinet", font=MONO,
                         color=CORAL).scale(0.22)
        inset_lbl.move_to(inset.get_center())
        x1 = Line(inset.get_corner(UP + LEFT), inset.get_corner(DOWN + RIGHT),
                  stroke_color=CORAL, stroke_width=2.0)
        x2 = Line(inset.get_corner(UP + RIGHT), inset.get_corner(DOWN + LEFT),
                  stroke_color=CORAL, stroke_width=2.0)
        self.add(inset, inset_lbl, x1, x2)

        cap = Text("every room green - including the bedroom", font=MONO,
                   color=GREEN).scale(0.3)
        cap.to_edge(DOWN, buff=0.35)

        def cap_upd(m):
            s = 0.5 + 0.5 * np.sin(t.get_value() * 2.2)
            m.set_opacity(0.6 + 0.4 * s)
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
