"""Scene: the problem Kubernetes solves — declare the end state, it keeps it true.

Class `Problem` (~22s). Start with ONE rounded container box ("your app"). At
"3am" it flashes CORAL and shows a crash mark, then a green restart arc heals
it. Then a "goes viral" surge multiplies it into ~10 small boxes across 3
server rows while amber traffic arrows rain in; at "night" it scales back to
~3. A persistent caption pulses the declarative promise. All motion driven by
a master ValueTracker on a repeating cycle.

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


class Problem(Scene):
    def construct(self):
        title = Text("You declare the end state — it keeps it true",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- three server rows (background lanes) ----------------------------
        rows = VGroup()
        row_ys = [1.4, 0.0, -1.4]
        for ry in row_ys:
            lane = RoundedRectangle(
                corner_radius=0.1, width=9.5, height=1.0,
                stroke_color=SECOND, stroke_width=1.2, stroke_opacity=0.5,
                fill_color="#101014", fill_opacity=0.4,
            ).shift(DOWN * 0.35 + UP * ry * 0.8)
            rows.add(lane)
        rows.move_to(DOWN * 0.3)
        row_labels = VGroup()
        for i, lane in enumerate(rows):
            rl = Text(f"server {i + 1}", font=MONO, color=SECOND).scale(0.22)
            rl.next_to(lane, LEFT, buff=0.15)
            row_labels.add(rl)

        # --- the one app box, centred -----------------------------------------
        app = RoundedRectangle(
            corner_radius=0.12, width=1.5, height=1.1,
            stroke_color=TEAL, stroke_width=2.5,
            fill_color="#0C1A18", fill_opacity=0.9,
        ).move_to(rows[1].get_center())
        app_lbl = Text("your app", font=MONO, color=TEAL).scale(0.3)
        app_lbl.move_to(app.get_center())
        one = VGroup(app, app_lbl)

        self.play(FadeIn(rows), FadeIn(row_labels), run_time=0.6)
        self.play(Create(app), FadeIn(app_lbl), run_time=0.6)

        # --- caption ----------------------------------------------------------
        cap = Text("you declare the end state — Kubernetes keeps it true",
                   font=HEAD, color=GREEN).scale(0.36)
        cap.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # phase marker label (3am / goes viral / night)
        phase = Text("3am", font=MONO, color=SILVER).scale(0.4)
        phase.next_to(title, DOWN, buff=0.2)
        phase._key = ""
        self.add(phase)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        CYCLE = 11.0  # seconds per full crash->restart->surge->shrink loop

        # crash mark (✕) + restart arc live near the app box
        crash = Text("✕", font=MONO, color=CORAL, weight="BOLD").scale(0.6)
        crash.move_to(app.get_center())
        crash.set_opacity(0.0)
        restart = Text("↻", font=MONO, color=GREEN, weight="BOLD").scale(0.7)
        restart.move_to(app.get_center())
        restart.set_opacity(0.0)
        self.add(crash, restart)

        # breathing + crash/restart of the primary app box
        def app_box_upd(m):
            tt = t.get_value() % CYCLE
            breath = 1.0 + 0.04 * np.sin(3.0 * t.get_value())
            m.scale_to_fit_width(1.5 * breath)
            # crash window 1.5..3.0 : flash coral
            if 1.5 <= tt < 3.0:
                m.set_stroke(color=CORAL, width=3.5)
                m.set_fill(color="#1A0C0A", opacity=0.9)
            else:
                m.set_stroke(color=TEAL, width=2.5)
                m.set_fill(color="#0C1A18", opacity=0.9)
            # during surge (3.5..8.5) hide the single box; fade back after
            if 3.6 <= tt < 8.8:
                m.set_opacity(np.clip((tt - 8.4) / 0.4, 0.0, 1.0))
            else:
                m.set_opacity(1.0)
        app.add_updater(app_box_upd)

        def app_lbl_upd(m):
            tt = t.get_value() % CYCLE
            m.move_to(app.get_center())
            m.set_opacity(0.0 if 3.6 <= tt < 8.8 else 1.0)
        app_lbl.add_updater(app_lbl_upd)

        def crash_upd(m):
            tt = t.get_value() % CYCLE
            m.move_to(app.get_center())
            if 1.5 <= tt < 3.0:
                m.set_opacity(0.4 + 0.6 * (0.5 + 0.5 * np.sin(14 * tt)))
            else:
                m.set_opacity(0.0)
        crash.add_updater(crash_upd)

        def restart_upd(m):
            tt = t.get_value() % CYCLE
            m.move_to(app.get_center())
            if 3.0 <= tt < 3.6:
                m.set_opacity(1.0)
                ang = (tt - 3.0) / 0.6 * 2 * np.pi
                m.scale_to_fit_width(0.6 + 0.1 * np.sin(ang))
            else:
                m.set_opacity(0.0)
        restart.add_updater(restart_upd)

        # --- surge replicas: ~10 small boxes spread across the 3 rows --------
        rng = np.random.default_rng(7)
        replicas = VGroup()
        rep_meta = []
        slot_x = np.linspace(-3.2, 3.2, 4)  # up to 4 per row
        slots = []
        for lane in rows:
            for sx in slot_x:
                slots.append(np.array([sx, lane.get_center()[1], 0]))
        for i in range(10):
            box = RoundedRectangle(
                corner_radius=0.08, width=0.78, height=0.62,
                stroke_color=TEAL, stroke_width=2,
                fill_color="#0C1A18", fill_opacity=0.95,
            )
            box.move_to(slots[i % len(slots)])
            box.set_opacity(0.0)
            replicas.add(box)
            # night keeps only first 3; appear order staggered
            rep_meta.append((slots[i % len(slots)], i))
        self.add(replicas)

        def make_rep_upd(target, idx):
            def _upd(m):
                tt = t.get_value() % CYCLE
                breath = 1.0 + 0.05 * np.sin(4.0 * t.get_value() + idx)
                m.move_to(target)
                m.scale_to_fit_width(0.78 * breath)
                # surge build 3.4..5.5 (staggered), hold, shrink at night 8.5..9.5
                appear_at = 3.4 + idx * 0.18
                if tt < appear_at:
                    vis = 0.0
                elif tt < 8.5:
                    vis = np.clip((tt - appear_at) / 0.3, 0.0, 1.0)
                else:
                    # night: keep only first 3 replicas
                    if idx < 3:
                        vis = np.clip(1.0 - (tt - 9.6) / 0.4, 0.0, 1.0) \
                            if tt > 9.6 else 1.0
                    else:
                        vis = np.clip(1.0 - (tt - 8.5) / 0.5, 0.0, 1.0)
                m.set_opacity(0.95 * vis)
                m.set_stroke(opacity=vis)
            return _upd

        for box, (target, idx) in zip(replicas, rep_meta):
            box.add_updater(make_rep_upd(target, idx))

        # --- traffic arrows (amber dots) rain in during the surge ------------
        traffic = VGroup()
        traf_meta = []
        for k in range(26):
            d = Dot(color=AMBER, radius=0.06)
            traffic.add(d)
            period = 1.0 + 0.8 * rng.random()
            offset = rng.uniform(0, period)
            tgt = slots[rng.integers(0, len(slots))] + np.array(
                [rng.uniform(-0.15, 0.15), rng.uniform(-0.1, 0.1), 0])
            sx = float(rng.uniform(-4.0, 4.0))
            traf_meta.append((period, offset, tgt, sx))
        self.add(traffic)

        def make_traf_upd(meta):
            period, offset, tgt, sx = meta
            start = np.array([sx, 3.0, 0])

            def _upd(m):
                tt = t.get_value() % CYCLE
                # traffic only flows during/around the surge window
                active = 2.8 < tt < 9.0
                if not active:
                    m.set_opacity(0.0)
                    return
                local = (t.get_value() + offset) % period
                frac = local / period
                eased = rate_functions.ease_in_quad(min(frac * 1.1, 1.0))
                pos = start * (1 - eased) + tgt * eased
                m.move_to(pos)
                m.set_opacity(np.clip(1.3 * (1 - frac) + 0.1, 0.0, 1.0))
            return _upd

        for d, meta in zip(traffic, traf_meta):
            d.add_updater(make_traf_upd(meta))

        # --- phase label cycles with the loop --------------------------------
        def phase_upd(m):
            tt = t.get_value() % CYCLE
            if tt < 3.0:
                key, col = "3am", CORAL
            elif tt < 8.5:
                key, col = "goes viral", AMBER
            else:
                key, col = "night", VIOLET
            if key != m._key:
                m._key = key
                new = Text(key, font=MONO, color=col, weight="BOLD").scale(0.4)
                new.next_to(title, DOWN, buff=0.2)
                m.become(new)
        phase.add_updater(phase_upd)

        # --- caption pulse ---------------------------------------------------
        def cap_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * np.sin(t.get_value() * 1.8)))
        cap.add_updater(cap_upd)

        self.play(t.animate.set_value(22.0), run_time=22.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
