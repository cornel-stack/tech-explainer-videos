"""Scene: the building blocks — container -> pod -> node -> cluster.

Class `Blocks` (~20s). Build the nesting outward and keep it alive. A small
container rect sits inside a POD (teal rounded box). 2-3 pods sit on a NODE
box; 2 node boxes sit inside a big dashed CLUSTER box. Pods breathe and every
few seconds a new pod spawns onto a node via an updater-driven scale/opacity,
showing the cluster is live. Three left-aligned legend lines explain each tier.

Dark palette only, TEXT labels only, continuous motion. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
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


def make_pod(scale=1.0):
    """A pod: rounded teal box with a tiny container inside + sublabel."""
    pod = RoundedRectangle(
        corner_radius=0.18, width=1.5 * scale, height=1.25 * scale,
        stroke_color=TEAL, stroke_width=2.5,
        fill_color="#0C1A18", fill_opacity=0.85,
    )
    inner = RoundedRectangle(
        corner_radius=0.05, width=0.8 * scale, height=0.5 * scale,
        stroke_color=SILVER, stroke_width=1.6,
        fill_color="#141418", fill_opacity=0.9,
    ).move_to(pod.get_center() + UP * 0.12 * scale)
    lbl = Text("pod", font=MONO, color=TEAL).scale(0.26 * scale)
    lbl.move_to(pod.get_center() + DOWN * 0.3 * scale)
    sub = Text("shared net + storage", font=MONO, color=SECOND)
    sub.scale(0.14 * scale)
    sub.move_to(pod.get_center() + DOWN * 0.48 * scale)
    g = VGroup(pod, inner, lbl, sub)
    g.body = pod
    return g


class Blocks(Scene):
    def construct(self):
        title = Text("Container -> Pod -> Node -> Cluster",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- cluster box (dashed green) --------------------------------------
        cluster = RoundedRectangle(
            corner_radius=0.2, width=11.0, height=5.4,
            stroke_color=GREEN, stroke_width=2.5,
            fill_color="#0A140F", fill_opacity=0.35,
        ).shift(DOWN * 0.3 + RIGHT * 1.4)
        # dashed appearance via overlaid dashes is heavy; use stroke + label.
        cluster_dash = RoundedRectangle(
            corner_radius=0.2, width=11.0, height=5.4,
            stroke_color=GREEN, stroke_width=1.2, stroke_opacity=0.4,
            fill_opacity=0.0,
        ).move_to(cluster)
        cluster_lbl = Text("cluster · one pool", font=MONO, color=GREEN,
                           weight="BOLD").scale(0.3)
        cluster_lbl.next_to(cluster, UP, buff=0.1).align_to(cluster, LEFT)

        # --- two node boxes inside the cluster -------------------------------
        nodes = VGroup()
        node_centres = [cluster.get_center() + LEFT * 2.6,
                        cluster.get_center() + RIGHT * 2.6]
        for i, c in enumerate(node_centres):
            node = RoundedRectangle(
                corner_radius=0.12, width=4.6, height=4.2,
                stroke_color=AMBER, stroke_width=2,
                fill_color="#141008", fill_opacity=0.5,
            ).move_to(c)
            nlbl = Text("node · a machine", font=MONO, color=AMBER).scale(0.26)
            nlbl.next_to(node, UP, buff=0.08)
            g = VGroup(node, nlbl)
            g.body = node
            nodes.add(g)

        self.play(Create(cluster), Create(cluster_dash), run_time=0.7)
        self.play(FadeIn(cluster_lbl), run_time=0.3)
        self.play(*[Create(n.body) for n in nodes],
                  *[FadeIn(n[1]) for n in nodes], run_time=0.7)

        # --- starter pods: 2 on node0, 1 on node1 (room for spawns) ----------
        pod_slots = []  # (node_index, position)
        for ni, c in enumerate(node_centres):
            node = nodes[ni].body
            cols = np.linspace(node.get_left()[0] + 1.0,
                               node.get_right()[0] - 1.0, 2)
            rows_y = [node.get_center()[1] + 0.8,
                      node.get_center()[1] - 0.9]
            for ry in rows_y:
                for cx in cols:
                    pod_slots.append(np.array([cx, ry, 0]))

        pods = VGroup()
        self.pod_scale = 0.78
        # 3 starter pods appear immediately
        starter_n = 3
        for i in range(starter_n):
            g = make_pod(self.pod_scale)
            g.move_to(pod_slots[i])
            pods.add(g)
        self.play(*[FadeIn(p, scale=0.6) for p in pods], run_time=0.8)

        # --- legend ----------------------------------------------------------
        legend = VGroup(
            Text("pod   — one or more containers, shared net + storage",
                 font=MONO, color=TEAL).scale(0.24),
            Text("node  — a machine that runs pods",
                 font=MONO, color=AMBER).scale(0.24),
            Text("cluster — many nodes, one pool of capacity",
                 font=MONO, color=GREEN).scale(0.24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        legend.to_edge(LEFT, buff=0.4).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(legend, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # breathing of all starter pods
        for i, p in enumerate(pods):
            def make_breath(pod_g, phase):
                base = self.pod_scale

                def _upd(m):
                    s = base * (1.0 + 0.03 * np.sin(2.2 * t.get_value() + phase))
                    m.set_width(1.5 * s, stretch=False)
                return _upd
            p.add_updater(make_breath(p, i * 0.8))

        # --- live spawns: new pods appear onto remaining free slots ----------
        spawn_slots = pod_slots[starter_n:starter_n + 4]
        spawn_pods = VGroup()
        for slot in spawn_slots:
            g = make_pod(self.pod_scale)
            g.move_to(slot)
            g.set_opacity(0.0)
            spawn_pods.add(g)
        self.add(spawn_pods)

        SPAWN_GAP = 3.5  # a new pod every few seconds, looping

        def make_spawn_upd(idx):
            appear_at = 1.5 + idx * SPAWN_GAP

            def _upd(m):
                cycle_len = SPAWN_GAP * len(spawn_slots)
                tt = t.get_value() % cycle_len
                local = tt - (appear_at % cycle_len)
                # grow-from-center window ~0.6s, then live breathing, then
                # at end of cycle fade so the loop can replay
                if local < 0:
                    vis, s = 0.0, 0.3
                elif local < 0.6:
                    f = local / 0.6
                    vis = f
                    s = 0.3 + 0.7 * rate_functions.ease_out_back(f)
                else:
                    vis = 1.0
                    s = 1.0 + 0.03 * np.sin(2.4 * t.get_value() + idx)
                m.set_opacity(vis)
                m.body.set_stroke(opacity=vis)
                m.set_width(1.5 * self.pod_scale * max(s, 0.05), stretch=False)
            return _upd

        for i, g in enumerate(spawn_pods):
            g.add_updater(make_spawn_upd(i))

        # --- cluster dash shimmer (keeps it feeling alive) -------------------
        def dash_upd(m):
            m.set_stroke(opacity=0.25 + 0.3 * (0.5 + 0.5 *
                         np.sin(t.get_value() * 1.6)))
        cluster_dash.add_updater(dash_upd)

        # --- "live" indicator --------------------------------------------------
        live = Text("cluster live · pods scheduling", font=MONO,
                    color=GREEN).scale(0.26)
        live.next_to(title, DOWN, buff=0.18)
        live.add_updater(lambda m: m.set_opacity(
            0.5 + 0.5 * (0.5 + 0.5 * np.sin(t.get_value() * 3.0))))
        self.add(live)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
