"""Scene: rolling updates — new pods up, old ones retired, zero downtime.

Class `Rollout` (~20s). A Deployment row of 4 pod hexes all at v1 (teal). A
rolling update proceeds pod-by-pod driven by t: a new v2 pod (violet) comes up
beside the row, shows a spinner then a green tick (healthy), then one v1 pod
fades out — repeat until all 4 are v2. A persistent GREEN "0 downtime" tag
stays lit. Near the end a coral rollback arrow sweeps and flips them back
toward v1 briefly, then the loop restarts.

Dark palette only, TEXT labels only, continuous motion. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    RegularPolygon,
    Text,
    VGroup,
    Arc,
    Arrow,
    ValueTracker,
    config,
    FadeIn,
    Create,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    PI,
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


def pod_hex(color=TEAL, scale=1.0):
    h = RegularPolygon(n=6, start_angle=PI / 6,
                       stroke_color=color, stroke_width=2.5,
                       fill_color="#0C1A18", fill_opacity=0.9)
    h.scale(0.55 * scale)
    return h


class Rollout(Scene):
    def construct(self):
        title = Text("Rolling update — new pods up, old ones retired",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        dep_lbl = Text("Deployment", font=MONO, color=SILVER).scale(0.3)
        dep_lbl.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(dep_lbl), run_time=0.3)

        # --- row of 4 v1 pods -------------------------------------------------
        N = 4
        pods = VGroup()
        ver_lbls = VGroup()
        for _ in range(N):
            h = pod_hex(TEAL)
            v = Text("v1", font=MONO, color=TEAL, weight="BOLD").scale(0.3)
            v.move_to(h.get_center())
            pods.add(h)
            ver_lbls.add(v)
        pods.arrange(RIGHT, buff=0.9)
        pods.move_to(DOWN * 0.3)
        for v, h in zip(ver_lbls, pods):
            v.move_to(h.get_center())
        self.play(*[FadeIn(h, scale=0.6) for h in pods],
                  *[FadeIn(v) for v in ver_lbls],
                  lag_ratio=0.08, run_time=0.9)

        # staging slot above the row for the incoming v2 pod
        stage_y = pods.get_center()[1] + 1.7

        # incoming v2 pod (reused each step), spinner, tick
        newpod = pod_hex(VIOLET)
        new_v = Text("v2", font=MONO, color=VIOLET, weight="BOLD").scale(0.3)
        spinner = Arc(radius=0.3, start_angle=0, angle=PI * 1.3,
                      stroke_color=AMBER, stroke_width=4)
        tick = Text("✓", font=MONO, color=GREEN, weight="BOLD").scale(0.4)
        self.add(newpod, new_v, spinner, tick)

        # --- 0 downtime tag ---------------------------------------------------
        tag = RoundedRectangle(corner_radius=0.1, width=2.4, height=0.6,
                               stroke_color=GREEN, stroke_width=2,
                               fill_color="#0A140F", fill_opacity=0.7)
        tag_txt = Text("0 downtime", font=MONO, color=GREEN,
                       weight="BOLD").scale(0.3)
        tag_txt.move_to(tag.get_center())
        tag_grp = VGroup(tag, tag_txt)
        tag_grp.to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.play(FadeIn(tag_grp), run_time=0.4)

        # rollback arrow (hidden until late)
        rb = Arrow(start=pods.get_right() + RIGHT * 0.5,
                   end=pods.get_left() + LEFT * 0.5,
                   color=CORAL, stroke_width=5, buff=0)
        rb.next_to(pods, DOWN, buff=0.5)
        rb_lbl = Text("rollback", font=MONO, color=CORAL,
                      weight="BOLD").scale(0.26)
        rb_lbl.next_to(rb, DOWN, buff=0.1)
        rb.set_opacity(0.0)
        rb_lbl.set_opacity(0.0)
        self.add(rb, rb_lbl)

        # --- caption ----------------------------------------------------------
        cap = Text("new pods up, old ones retired — a few at a time",
                   font=HEAD, color=VIOLET).scale(0.34)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        STEP = 3.0            # seconds to roll one pod
        ROLL = STEP * N       # full forward roll = 12s
        ROLLBACK = 3.5        # coral rollback sweep
        CYCLE = ROLL + ROLLBACK  # loops

        pod_centres = [p.get_center() for p in pods]

        def current_step(tt):
            """Index of the pod being rolled (0..N-1) during forward roll."""
            return int(min(tt // STEP, N - 1))

        def in_rollback(tt):
            return tt >= ROLL

        # version coloring of each row pod, flips to v2 after its step completes
        def make_pod_upd(idx):
            def _upd(m):
                tt = t.get_value() % CYCLE
                breath = 1.0 + 0.04 * np.sin(2.4 * t.get_value() + idx)
                m.scale_to_fit_height(0.95 * breath)
                m.move_to(pod_centres[idx])
                if in_rollback(tt):
                    # rollback sweep flips them back to v1 left-to-right
                    rb_f = (tt - ROLL) / ROLLBACK
                    flipped = rb_f * N
                    is_v1 = idx < flipped
                    col = TEAL if is_v1 else VIOLET
                else:
                    step = current_step(tt)
                    # pod becomes v2 once its step is done (step index passed it)
                    is_v2 = idx < step or (idx == step and
                                           (tt - idx * STEP) > STEP * 0.75)
                    col = VIOLET if is_v2 else TEAL
                m.set_stroke(color=col, width=2.5)
            return _upd

        for i, p in enumerate(pods):
            p.add_updater(make_pod_upd(i))

        def make_verlbl_upd(idx):
            def _upd(m):
                tt = t.get_value() % CYCLE
                m.move_to(pod_centres[idx])
                if in_rollback(tt):
                    rb_f = (tt - ROLL) / ROLLBACK
                    is_v1 = idx < rb_f * N
                    txt, col = ("v1", TEAL) if is_v1 else ("v2", VIOLET)
                else:
                    step = current_step(tt)
                    is_v2 = idx < step or (idx == step and
                                           (tt - idx * STEP) > STEP * 0.75)
                    txt, col = ("v2", VIOLET) if is_v2 else ("v1", TEAL)
                if getattr(m, "_txt", None) != txt:
                    m._txt = txt
                    new = Text(txt, font=MONO, color=col,
                               weight="BOLD").scale(0.3)
                    new.move_to(pod_centres[idx])
                    m.become(new)
            return _upd

        for i, v in enumerate(ver_lbls):
            v.add_updater(make_verlbl_upd(i))

        # incoming v2 pod: appears above the pod being rolled, spinner->tick,
        # then descends into place as that pod flips.
        def newpod_upd(m):
            tt = t.get_value() % CYCLE
            if in_rollback(tt):
                m.set_opacity(0.0)
                m.set_stroke(opacity=0.0)
                return
            step = current_step(tt)
            local = tt - step * STEP
            f = local / STEP
            target = pod_centres[step]
            stage = np.array([target[0], stage_y, 0])
            if f < 0.25:
                # grow in at the staging slot
                g = f / 0.25
                m.move_to(stage)
                m.set_opacity(0.9 * g)
                m.set_stroke(color=VIOLET, width=2.5, opacity=g)
                m.scale_to_fit_height(0.3 + 0.7 * g)
            elif f < 0.75:
                # healthy, waiting (spinner->tick handled separately)
                m.move_to(stage)
                m.set_opacity(0.9)
                m.set_stroke(color=VIOLET, width=2.5, opacity=1.0)
                m.scale_to_fit_height(1.0)
            else:
                # descend into the row slot
                g = (f - 0.75) / 0.25
                e = rate_functions.ease_in_out_quad(g)
                m.move_to(stage * (1 - e) + target * e)
                m.set_opacity(0.9 * (1 - e))  # hand off to the row pod
                m.set_stroke(opacity=1 - e)
        newpod.add_updater(newpod_upd)

        def new_v_upd(m):
            m.move_to(newpod.get_center())
            m.set_opacity(newpod.get_stroke_opacity())
        new_v.add_updater(new_v_upd)

        def spinner_upd(m):
            tt = t.get_value() % CYCLE
            if in_rollback(tt):
                m.set_opacity(0.0)
                return
            step = current_step(tt)
            f = (tt - step * STEP) / STEP
            if 0.25 <= f < 0.55:
                spin = (t.get_value() * 6.0) % (2 * PI)
                new = Arc(radius=0.3, start_angle=spin, angle=PI * 1.3,
                          stroke_color=AMBER, stroke_width=4)
                new.move_to(newpod.get_center())
                m.become(new)
                m.set_opacity(1.0)
            else:
                m.set_opacity(0.0)
        spinner.add_updater(spinner_upd)

        def tick_upd(m):
            tt = t.get_value() % CYCLE
            if in_rollback(tt):
                m.set_opacity(0.0)
                return
            step = current_step(tt)
            f = (tt - step * STEP) / STEP
            if 0.55 <= f < 0.78:
                m.move_to(newpod.get_center())
                pulse = 0.5 + 0.5 * np.sin(10 * t.get_value())
                m.set_opacity(0.6 + 0.4 * pulse)
            else:
                m.set_opacity(0.0)
        tick.add_updater(tick_upd)

        # rollback arrow sweeps during the rollback window
        def rb_upd(m):
            tt = t.get_value() % CYCLE
            if in_rollback(tt):
                rb_f = (tt - ROLL) / ROLLBACK
                m.set_opacity(0.4 + 0.6 * (0.5 + 0.5 *
                              np.sin(8 * t.get_value())))
                m.set_stroke(opacity=1.0)
            else:
                m.set_opacity(0.0)
                m.set_stroke(opacity=0.0)
        rb.add_updater(rb_upd)
        rb_lbl.add_updater(lambda m: m.set_opacity(rb.get_stroke_opacity()))

        # 0 downtime tag stays lit, gentle pulse
        def tag_upd(m):
            m.set_stroke(width=2.0 + 1.5 * (0.5 + 0.5 *
                         np.sin(t.get_value() * 2.5)))
        tag.add_updater(tag_upd)

        def cap_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 1.6)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(20.0), run_time=20.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
