"""Scene: the worker node — where pods actually run.

Class `Worker` (~20s). A WORKER NODE box holds three agent chips on the left —
kubelet (keeps pods alive), container runtime (pulls & runs), kube-proxy
(routes traffic) — and 3 pods on the right with green health ticks driven by
kubelet. A user request (amber dot) arrives at kube-proxy and load-balances to
a healthy pod in round-robin; the chosen pod flashes. Requests keep arriving
and route to different pods in turn; health ticks pulse.

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


class Worker(Scene):
    def construct(self):
        title = Text("The worker node — where pods actually run",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- worker node box --------------------------------------------------
        node = RoundedRectangle(
            corner_radius=0.18, width=11.0, height=4.8,
            stroke_color=GREEN, stroke_width=2.2,
            fill_color="#0A140F", fill_opacity=0.35,
        ).shift(DOWN * 0.25)
        node_lbl = Text("WORKER NODE", font=MONO, color=GREEN,
                        weight="BOLD").scale(0.3)
        node_lbl.next_to(node, UP, buff=0.1).align_to(node, LEFT)
        self.play(Create(node), FadeIn(node_lbl), run_time=0.7)

        # --- three agent chips (left) ----------------------------------------
        def chip(name, desc, col):
            box = RoundedRectangle(
                corner_radius=0.1, width=3.4, height=1.05,
                stroke_color=col, stroke_width=2,
                fill_color="#101014", fill_opacity=0.9,
            )
            nm = Text(name, font=MONO, color=col, weight="BOLD").scale(0.24)
            nm.move_to(box.get_top() + DOWN * 0.26)
            ds = Text(desc, font=MONO, color=SECOND).scale(0.17)
            ds.next_to(nm, DOWN, buff=0.08)
            g = VGroup(box, nm, ds)
            g.body = box
            return g

        kubelet = chip("kubelet", "keeps pods alive", GREEN)
        runtime = chip("container runtime", "pulls & runs", AMBER)
        proxy = chip("kube-proxy", "routes traffic", TEAL)
        chips = VGroup(kubelet, runtime, proxy).arrange(DOWN, buff=0.3)
        chips.move_to(node.get_center() + LEFT * 3.3)
        self.play(*[Create(c.body) for c in chips],
                  *[FadeIn(c[1]) for c in chips],
                  *[FadeIn(c[2]) for c in chips], run_time=0.8)

        # --- three pods (right) with health ticks ----------------------------
        pods = VGroup()
        ticks = []
        for _ in range(3):
            pod = RoundedRectangle(
                corner_radius=0.16, width=1.6, height=1.15,
                stroke_color=TEAL, stroke_width=2.5,
                fill_color="#0C1A18", fill_opacity=0.9,
            )
            plbl = Text("pod", font=MONO, color=TEAL).scale(0.24)
            plbl.move_to(pod.get_center() + DOWN * 0.2)
            tick = Text("✓", font=MONO, color=GREEN,
                        weight="BOLD").scale(0.4)
            tick.move_to(pod.get_center() + UP * 0.2)
            g = VGroup(pod, plbl, tick)
            g.body = pod
            g.tick = tick
            pods.add(g)
            ticks.append(tick)
        pods.arrange(DOWN, buff=0.35)
        pods.move_to(node.get_center() + RIGHT * 3.3)
        self.play(*[FadeIn(p, scale=0.7) for p in pods], run_time=0.7)

        # --- caption ----------------------------------------------------------
        cap = Text("traffic always reaches a healthy pod",
                   font=HEAD, color=GREEN).scale(0.36)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        REQ_PERIOD = 2.2  # one request's travel time

        pod_centres = [p.body.get_center() for p in pods]
        proxy_out = proxy.body.get_right() + RIGHT * 0.1
        req_entry = np.array([node.get_left()[0] - 0.9,
                              proxy.body.get_center()[1], 0])

        # request dot + label
        req = Dot(color=AMBER, radius=0.12)
        req_lbl = Text("request", font=MONO, color=AMBER).scale(0.2)
        self.add(req, req_lbl)

        def req_upd(m):
            local = t.get_value() % REQ_PERIOD
            frac = local / REQ_PERIOD
            trip = int(t.get_value() // REQ_PERIOD)
            target = np.array(pod_centres[trip % 3])
            # leg 1: entry -> proxy (first 45%), leg 2: proxy -> chosen pod
            if frac < 0.45:
                f = frac / 0.45
                eased = rate_functions.ease_in_out_quad(f)
                pos = req_entry * (1 - eased) + proxy_out * eased
            else:
                f = (frac - 0.45) / 0.55
                eased = rate_functions.ease_in_out_quad(f)
                pos = proxy_out * (1 - eased) + target * eased
            m.move_to(pos)
            m.set_opacity(np.clip(1.4 * (1 - frac) + 0.25, 0.0, 1.0))
        req.add_updater(req_upd)
        req_lbl.add_updater(lambda m: m.next_to(req, UP, buff=0.08)
                            .set_opacity(req.get_fill_opacity()))

        # chosen pod flashes as the request arrives (frac > 0.85)
        def make_pod_glow(pod_g, idx):
            def _upd(m):
                local = t.get_value() % REQ_PERIOD
                frac = local / REQ_PERIOD
                trip = int(t.get_value() // REQ_PERIOD)
                chosen = (trip % 3) == idx
                breath = 1.0 + 0.03 * np.sin(2.5 * t.get_value() + idx)
                m.scale_to_fit_width(1.6 * breath)
                if chosen and frac > 0.82:
                    m.set_stroke(color=AMBER, width=4.5)
                else:
                    m.set_stroke(color=TEAL, width=2.5)
            return _upd

        for i, p in enumerate(pods):
            p.body.add_updater(make_pod_glow(p, i))

        # kubelet-driven health tick pulse
        def make_tick_upd(tk, idx):
            def _upd(m):
                pulse = 0.5 + 0.5 * np.sin(3.0 * t.get_value() + idx * 2.0)
                m.set_opacity(0.55 + 0.45 * pulse)
                m.scale_to_fit_height(0.3 + 0.08 * pulse)
            return _upd

        for i, tk in enumerate(ticks):
            tk.add_updater(make_tick_upd(tk, i))

        # kubelet chip glows in time with the health pulse
        def kubelet_upd(m):
            g = 0.5 + 0.5 * np.sin(3.0 * t.get_value())
            m.set_stroke(width=2.0 + 2.0 * g)
        kubelet.body.add_updater(kubelet_upd)

        # kube-proxy chip pulses when routing (request in leg 2)
        def proxy_upd(m):
            frac = (t.get_value() % REQ_PERIOD) / REQ_PERIOD
            m.set_stroke(width=4.0 if 0.4 <= frac < 0.6 else 2.0)
        proxy.body.add_updater(proxy_upd)

        def cap_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 1.7)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
