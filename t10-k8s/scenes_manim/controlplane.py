"""Scene: the control plane — the brain that decides.

Class `Controlplane` (~22s). A titled CONTROL PLANE container holds four
labelled sub-boxes: API server (front door), etcd (key/value state, with a few
tiny key:value rows), scheduler (places pods), controller manager (fixes
drift). Command packets (amber dots) flow in from the left into API server ->
etcd (a row updates) -> scheduler, which points at a node box below. The flow
loops; etcd rows blink as they update.

Dark palette only, TEXT labels only, continuous motion. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Dot,
    Arrow,
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


class Controlplane(Scene):
    def construct(self):
        title = Text("The control plane — the brain that decides",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- control plane container -----------------------------------------
        plane = RoundedRectangle(
            corner_radius=0.18, width=11.0, height=4.4,
            stroke_color=VIOLET, stroke_width=2.2,
            fill_color="#120A1A", fill_opacity=0.4,
        ).shift(UP * 0.55)
        plane_lbl = Text("CONTROL PLANE", font=MONO, color=VIOLET,
                         weight="BOLD").scale(0.3)
        plane_lbl.next_to(plane, UP, buff=0.1).align_to(plane, LEFT)

        self.play(Create(plane), FadeIn(plane_lbl), run_time=0.7)

        # --- four sub-boxes ---------------------------------------------------
        def subbox(title_txt, sub_txt, col, w=2.3, h=2.0):
            box = RoundedRectangle(
                corner_radius=0.1, width=w, height=h,
                stroke_color=col, stroke_width=2,
                fill_color="#101014", fill_opacity=0.85,
            )
            name = Text(title_txt, font=MONO, color=col,
                        weight="BOLD").scale(0.24)
            name.move_to(box.get_top() + DOWN * 0.3)
            desc = Text(sub_txt, font=MONO, color=SECOND).scale(0.17)
            desc.next_to(name, DOWN, buff=0.1)
            g = VGroup(box, name, desc)
            g.body = box
            g.name = name
            return g

        api = subbox("API server", "front door", VIOLET)
        etcd = subbox("etcd", "key/value state", SILVER)
        sched = subbox("scheduler", "places pods", AMBER)
        ctrl = subbox("controller mgr", "fixes drift", TEAL)

        grp = VGroup(api, etcd, sched, ctrl).arrange(RIGHT, buff=0.35)
        grp.move_to(plane.get_center())

        # etcd key:value rows
        kv_rows = VGroup()
        kv_pairs = [("replicas", "10"), ("image", "v1"), ("node", "n2")]
        for k, v in kv_pairs:
            row = Text(f"{k}: {v}", font=MONO, color=SILVER).scale(0.15)
            kv_rows.add(row)
        kv_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        kv_rows.move_to(etcd.body.get_center() + DOWN * 0.1)

        self.play(*[Create(b.body) for b in (api, etcd, sched, ctrl)],
                  run_time=0.8)
        self.play(*[FadeIn(b.name) for b in (api, etcd, sched, ctrl)],
                  *[FadeIn(b[2]) for b in (api, etcd, sched, ctrl)],
                  run_time=0.4)
        self.play(FadeIn(kv_rows), run_time=0.4)

        # --- node box at bottom ----------------------------------------------
        node = RoundedRectangle(
            corner_radius=0.12, width=3.0, height=1.3,
            stroke_color=GREEN, stroke_width=2,
            fill_color="#0A140F", fill_opacity=0.6,
        ).to_edge(DOWN, buff=1.1)
        node_lbl = Text("-> picks a node", font=MONO, color=GREEN).scale(0.26)
        node_lbl.move_to(node.get_center())
        self.play(Create(node), FadeIn(node_lbl), run_time=0.5)

        # --- caption ----------------------------------------------------------
        cap = Text("the brain decides — it never runs your containers",
                   font=HEAD, color=VIOLET).scale(0.34)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        CYCLE = 5.0  # one command's journey

        # waypoints: left entry -> api -> etcd -> scheduler -> node
        wp_entry = np.array([plane.get_left()[0] - 0.8,
                             api.body.get_center()[1], 0])
        wp_api = api.body.get_center()
        wp_etcd = etcd.body.get_center()
        wp_sched = sched.body.get_center()
        wp_node = node.get_top() + UP * 0.1

        legs = [wp_entry, wp_api, wp_etcd, wp_sched, wp_node]

        # command packets — a few in flight, staggered
        packets = VGroup()
        pk_offsets = [0.0, CYCLE / 3.0, 2 * CYCLE / 3.0]
        for _ in pk_offsets:
            d = Dot(color=AMBER, radius=0.11)
            packets.add(d)
        self.add(packets)

        def make_packet_upd(offset):
            def _upd(m):
                local = (t.get_value() + offset) % CYCLE
                frac = local / CYCLE
                # 4 legs over the cycle
                seg_f = frac * 4.0
                seg = int(min(seg_f, 3.999))
                sub = seg_f - seg
                eased = rate_functions.ease_in_out_quad(sub)
                a = np.array(legs[seg])
                b = np.array(legs[seg + 1])
                m.move_to(a * (1 - eased) + b * eased)
                m.set_opacity(1.0)
            return _upd

        for d, off in zip(packets, pk_offsets):
            d.add_updater(make_packet_upd(off))

        # etcd rows blink when a packet passes through etcd (frac ~0.25..0.5)
        def make_kv_upd(row, idx):
            def _upd(m):
                near = False
                for off in pk_offsets:
                    frac = ((t.get_value() + off) % CYCLE) / CYCLE
                    if 0.25 <= frac < 0.5:
                        near = True
                blink = 0.5 + 0.5 * np.sin(8.0 * t.get_value() + idx * 1.3)
                if near and idx == int(t.get_value() // 1.4) % len(kv_pairs):
                    m.set_color(GREEN)
                    m.set_opacity(0.6 + 0.4 * blink)
                else:
                    m.set_color(SILVER)
                    m.set_opacity(0.8)
            return _upd

        for i, row in enumerate(kv_rows):
            row.add_updater(make_kv_upd(row, i))

        # highlight the active sub-box as the packet reaches it
        boxes_order = [api, etcd, sched]
        box_fracs = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75)]

        def make_box_glow(bx, lo, hi):
            base_col = bx.body.get_stroke_color()

            def _upd(m):
                active = False
                for off in pk_offsets:
                    frac = ((t.get_value() + off) % CYCLE) / CYCLE
                    if lo <= frac < hi:
                        active = True
                m.set_stroke(width=4.0 if active else 2.0)
            return _upd

        for bx, (lo, hi) in zip(boxes_order, box_fracs):
            bx.body.add_updater(make_box_glow(bx.body, lo, hi))

        # scheduler -> node highlight on the last leg
        def node_upd(m):
            active = any(0.75 <= ((t.get_value() + off) % CYCLE) / CYCLE
                         for off in pk_offsets)
            m.set_stroke(width=3.0 if active else 2.0)
        node.add_updater(node_upd)

        def cap_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 1.7)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(22.0), run_time=22.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
