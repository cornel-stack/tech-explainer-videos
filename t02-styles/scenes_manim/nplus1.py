"""Interlude scene: REST N+1 vs GraphQL single round-trip.

Class `NPlusOne` — LEFT shows REST making three sequential round-trips;
RIGHT shows GraphQL making one. Both sides LOOP FOREVER, staggered, so the
contrast keeps replaying and the frame is never still. ~25s.

Dark design system (no blue, no white).
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

BG = "#0A0A0C"
INK = "#EDE7DB"
SECOND = "#9A958C"
AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

config.background_color = BG


def card(label, accent, w=2.4, h=1.1):
    """A rounded card with glow + crisp stroke and a centred label."""
    glow = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        stroke_color=accent, stroke_width=12, stroke_opacity=0.16,
        fill_opacity=0,
    )
    body = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        stroke_color=accent, stroke_width=3,
        fill_color=BG, fill_opacity=0.92,
    )
    txt = Text(label, font="Inter", color=INK, weight="SEMIBOLD").scale(0.38)
    txt.move_to(body.get_center())
    g = VGroup(glow, body, txt)
    g.glow = glow
    return g


class NPlusOne(Scene):
    def construct(self):
        title = Text("One query, or many?",
                     font="Inter", color=INK, weight="SEMIBOLD").scale(0.52)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.7)

        # Divider between the two halves.
        divider = Line([0, -3.2, 0], [0, 2.4, 0],
                       color=SECOND, stroke_width=1, stroke_opacity=0.25)
        self.play(FadeIn(divider), run_time=0.4)

        # ---------- LEFT: REST ----------------------------------------------
        lx = -3.6
        rest_client = card("REST\nclient", AMBER, w=2.1, h=1.2)
        rest_client.move_to([lx, 1.3, 0])
        rest_server = card("server", AMBER, w=2.1, h=1.2)
        rest_server.move_to([lx, -2.2, 0])

        rest_head = Text("REST", font="Inter", color=AMBER,
                         weight="BOLD").scale(0.4)
        rest_head.move_to([lx, 2.2, 0])

        # ---------- RIGHT: GraphQL ------------------------------------------
        rx = 3.6
        gql_client = card("GraphQL\nclient", MINT, w=2.1, h=1.2)
        gql_client.move_to([rx, 1.3, 0])
        gql_server = card("server", MINT, w=2.1, h=1.2)
        gql_server.move_to([rx, -2.2, 0])

        gql_head = Text("GraphQL", font="Inter", color=MINT,
                        weight="BOLD").scale(0.4)
        gql_head.move_to([rx, 2.2, 0])

        # Build fast: everything on screen in one snappy beat (~1.0s).
        self.play(
            FadeIn(rest_head), FadeIn(gql_head),
            GrowFromCenter(rest_client), GrowFromCenter(gql_client),
            GrowFromCenter(rest_server), GrowFromCenter(gql_server),
            run_time=1.0,
        )

        # Endpoints for travelling pulses (client bottom -> server top).
        rest_top = np.array([lx, 0.7, 0])
        rest_bot = np.array([lx, -1.6, 0])
        gql_top = np.array([rx, 0.7, 0])
        gql_bot = np.array([rx, -1.6, 0])

        # Cost labels (shown once, then they pulse within the loop phase).
        rest_cost = Text("3 round-trips  (N+1)", font="Inter",
                         color=CORAL, weight="SEMIBOLD").scale(0.36)
        rest_cost.move_to([lx, -3.1, 0])
        gql_cost = Text("1 round-trip", font="Inter",
                        color=MINT, weight="SEMIBOLD").scale(0.36)
        gql_cost.move_to([rx, -3.1, 0])

        # Request labels (static text; the motion is the travelling pulse).
        rest_lbl = Text("GET /books • /authors ...", font="Inter",
                        color=AMBER).scale(0.24)
        rest_lbl.move_to([lx + 1.35, -0.45, 0])
        gql_lbl = Text("{ book { title author } }", font="Inter",
                       color=MINT).scale(0.24)
        gql_lbl.move_to([rx + 1.45, -0.45, 0])

        self.play(
            FadeIn(rest_cost, shift=UP * 0.2),
            FadeIn(gql_cost, shift=UP * 0.2),
            FadeIn(rest_lbl), FadeIn(gql_lbl),
            run_time=0.6,
        )
        # Core diagram on screen by ~3s.

        # =====================================================================
        # CONTINUOUS LOOP PHASE
        # A master clock drives both sides forever. REST fires three staggered
        # down-and-back pulses per cycle; GraphQL fires one. The cycles overlap
        # so there is always a pulse in flight on at least one side.
        # =====================================================================
        t = ValueTracker(0.0)

        def leg(center_pt_a, center_pt_b, frac):
            """Interpolate a->b for frac in [0,1]."""
            return center_pt_a * (1 - frac) + center_pt_b * frac

        # --- REST: three sequential round-trips, repeating -----------------
        # Cycle length 4.0s: trips at local offsets 0, 1.1, 2.2 (each ~0.9s
        # out + back). A dot goes down (request) then a response dot comes up.
        rest_cycle = 4.0
        rest_offsets = [0.0, 1.1, 2.2]
        rest_dots = VGroup()
        for off in rest_offsets:
            req_dot = Dot(color=AMBER, radius=0.09)
            resp_dot = Dot(color=CORAL, radius=0.085)

            def make_rest(off=off, req_dot=req_dot, resp_dot=resp_dot):
                def _upd(_m):
                    local = (t.get_value() - off) % rest_cycle
                    # request leg: 0..0.9 going down
                    if 0 <= local < 0.9:
                        f = rate_functions.ease_in_out_sine(local / 0.9)
                        req_dot.move_to(leg(rest_top, rest_bot, f))
                        req_dot.set_opacity(np.sin(np.pi * (local / 0.9)) ** 0.4)
                        resp_dot.set_opacity(0)
                    # response leg: 0.9..1.8 coming back up
                    elif 0.9 <= local < 1.8:
                        f = rate_functions.ease_in_out_sine((local - 0.9) / 0.9)
                        resp_dot.move_to(leg(rest_bot, rest_top, f))
                        resp_dot.set_opacity(
                            np.sin(np.pi * ((local - 0.9) / 0.9)) ** 0.4)
                        req_dot.set_opacity(0)
                    else:
                        req_dot.set_opacity(0)
                        resp_dot.set_opacity(0)
                return _upd

            # Attach updater to a lightweight carrier (the group itself).
            grp = VGroup(req_dot, resp_dot)
            grp.add_updater(make_rest())
            rest_dots.add(grp)
        self.add(rest_dots)

        # --- GraphQL: one round-trip, repeating -----------------------------
        # Cycle length 2.2s so it fires roughly twice per REST burst, staggered.
        gql_cycle = 2.2
        gql_req = Dot(color=MINT, radius=0.1)
        gql_resp = Dot(color=MINT, radius=0.095)
        gql_pair = VGroup(gql_req, gql_resp)

        def gql_upd(_m):
            local = (t.get_value() + 0.5) % gql_cycle
            if 0 <= local < 0.85:
                f = rate_functions.ease_in_out_sine(local / 0.85)
                gql_req.move_to(leg(gql_top, gql_bot, f))
                gql_req.set_opacity(np.sin(np.pi * (local / 0.85)) ** 0.4)
                gql_resp.set_opacity(0)
            elif 0.85 <= local < 1.7:
                f = rate_functions.ease_in_out_sine((local - 0.85) / 0.85)
                gql_resp.move_to(leg(gql_bot, gql_top, f))
                gql_resp.set_opacity(np.sin(np.pi * ((local - 0.85) / 0.85)) ** 0.4)
                gql_req.set_opacity(0)
            else:
                gql_req.set_opacity(0)
                gql_resp.set_opacity(0)
        gql_pair.add_updater(gql_upd)
        self.add(gql_pair)

        # --- Glows breathe + cost labels flare on each burst ----------------
        glows = [rest_client.glow, rest_server.glow,
                 gql_client.glow, gql_server.glow]

        def glow_upd(m, ph=0.0):
            m.set_stroke(opacity=0.16 + 0.22 *
                         (0.5 + 0.5 * np.sin(2.0 * t.get_value() + ph)))
        for i, g in enumerate(glows):
            g.add_updater(lambda m, i=i: glow_upd(m, ph=i * 1.3))

        def rest_cost_upd(m):
            m.set_opacity(0.6 + 0.4 *
                          (0.5 + 0.5 * np.sin(2 * np.pi * t.get_value() / rest_cycle)))
        rest_cost.add_updater(rest_cost_upd)

        def gql_cost_upd(m):
            m.set_opacity(0.6 + 0.4 *
                          (0.5 + 0.5 * np.sin(2 * np.pi * t.get_value() / gql_cycle)))
        gql_cost.add_updater(gql_cost_upd)

        # Drive ~19s of unbroken looping motion.
        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
