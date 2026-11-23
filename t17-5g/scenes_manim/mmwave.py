"""Scene: mmWave — a fast beam blocked by almost everything.

Class `Mmwave` (~18s). A tower fires a mmWave BEAM reaching only a small
radius. Obstacles block it: a WALL, a TREE/leaf, RAIN, a HAND — each flashes
CORAL "x blocked" when the beam hits. A phone behind a wall gets nothing
(CORAL "no signal"); a phone in clear line-of-sight nearby gets GREEN
"2 Gbps". Caption: "barely a block — blocked by walls, rain, leaves, your
hand".

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92  green #35E08A
  teal #2DD4BF  violet #B06BFF  amber #FFB020  coral #FF5C47
  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Line,
    Circle,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    PI,
    interpolate_color,
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


class Mmwave(Scene):
    def construct(self):
        title = Text("mmWave: huge speed, tiny reach", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- tower on the left ----------------------------------------------
        tower_base = np.array([-5.4, -1.8, 0.0])
        mast = Line(tower_base, tower_base + UP * 2.2,
                    stroke_color=AMBER, stroke_width=4)
        emit = np.array([tower_base[0], tower_base[1] + 2.2, 0.0])
        tower_lbl = Text("mmWave cell", font=MONO, color=AMBER).scale(0.3)
        tower_lbl.next_to(mast, DOWN, buff=0.15)
        self.play(Create(mast), FadeIn(tower_lbl), run_time=0.6)

        # beam reach radius (small)
        reach = 3.2
        reach_ring = Circle(radius=reach, stroke_color=AMBER, stroke_width=1.5,
                            stroke_opacity=0.35, fill_opacity=0.0).move_to(emit)
        self.play(Create(reach_ring), run_time=0.5)

        # --- obstacles at various angles/positions along the beam -----------
        # each: (label, position, color)
        obstacles = [
            ("WALL", emit + np.array([2.4, 0.2, 0]), SILVER),
            ("TREE", emit + np.array([1.7, -1.6, 0]), GREEN),
            ("RAIN", emit + np.array([2.9, 1.1, 0]), TEAL),
            ("HAND", emit + np.array([1.2, 1.5, 0]), GOLD),
        ]
        obs_group = VGroup()
        obs_items = []
        for name, pos, col in obstacles:
            box = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.6,
                                   stroke_color=col, stroke_width=2,
                                   fill_color="#111318", fill_opacity=0.9)
            box.move_to(pos)
            lbl = Text(name, font=MONO, color=col).scale(0.24).move_to(box)
            blocked = Text("x blocked", font=MONO, color=CORAL,
                           weight="BOLD").scale(0.22)
            blocked.next_to(box, UP, buff=0.08)
            blocked.set_opacity(0.0)
            g = VGroup(box, lbl, blocked)
            obs_group.add(g)
            obs_items.append((pos, blocked, name))
        self.play(*[FadeIn(g) for g in obs_group], lag_ratio=0.1, run_time=0.9)

        # --- phones ----------------------------------------------------------
        # phone behind wall -> no signal
        phone_blocked_pos = emit + np.array([3.6, 0.2, 0])
        phone_b = RoundedRectangle(corner_radius=0.1, width=0.7, height=1.3,
                                   stroke_color=CORAL, stroke_width=2.5,
                                   fill_color="#15100F",
                                   fill_opacity=0.9).move_to(phone_blocked_pos)
        phone_b_lbl = Text("no signal", font=MONO, color=CORAL,
                           weight="BOLD").scale(0.26)
        phone_b_lbl.next_to(phone_b, DOWN, buff=0.12)

        # phone in clear line of sight -> 2 Gbps
        phone_ok_pos = emit + np.array([1.3, -0.1, 0])
        phone_ok = RoundedRectangle(corner_radius=0.1, width=0.7, height=1.3,
                                    stroke_color=GREEN, stroke_width=2.5,
                                    fill_color="#0D170F",
                                    fill_opacity=0.9).move_to(phone_ok_pos)
        phone_ok_lbl = Text("2 Gbps", font=MONO, color=GREEN,
                            weight="BOLD").scale(0.28)
        phone_ok_lbl.next_to(phone_ok, DOWN, buff=0.12)

        self.play(FadeIn(phone_b), FadeIn(phone_b_lbl),
                  FadeIn(phone_ok), FadeIn(phone_ok_lbl), run_time=0.7)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # The beam: a sweeping sector that fires on a loop, trying to reach,
        # getting blocked. We animate a growing wedge pulse from emitter.
        beam = Line(emit, emit + RIGHT * 0.1, stroke_color=AMBER,
                    stroke_width=10)

        # direction toward the clear phone (line of sight)
        los_dir = (phone_ok_pos - emit)
        los_dir = los_dir / np.linalg.norm(los_dir)
        # direction toward blocked phone (hits wall)
        blk_dir = (phone_blocked_pos - emit)
        blk_dir = blk_dir / np.linalg.norm(blk_dir)
        wall_dist = np.linalg.norm(obstacles[0][1] - emit)

        def beam_upd(m):
            tt = t.get_value()
            # alternate between two aim directions over time
            phase = (tt % 3.0) / 3.0
            aim_blocked = (int(tt // 3.0) % 2 == 0)
            direc = blk_dir if aim_blocked else los_dir
            maxlen = wall_dist if aim_blocked else reach * 0.42
            # pulse grows then resets within each aim window
            grow = (tt * 2.4) % 1.0
            length = 0.2 + grow * maxlen
            col = CORAL if aim_blocked else GREEN
            m.put_start_and_end_on(emit, emit + direc * length)
            m.set_stroke(color=col, opacity=0.4 + 0.6 * (1 - grow))
        beam.add_updater(beam_upd)
        self.add(beam)

        # Obstacle "x blocked" flashes cycle round the obstacles.
        def make_obs_flash(blocked_lbl, idx):
            def _upd(m):
                active = int(t.get_value() // 1.3) % len(obs_items)
                if active == idx:
                    s = 0.5 + 0.5 * np.sin(8.0 * t.get_value())
                    m.set_opacity(0.4 + 0.6 * s)
                else:
                    m.set_opacity(0.0)
            return _upd
        for idx, (pos, blk_lbl, name) in enumerate(obs_items):
            blk_lbl.add_updater(make_obs_flash(blk_lbl, idx))

        # reach ring breathes
        def ring_upd(m):
            s = 0.5 + 0.5 * np.sin(1.6 * t.get_value())
            m.set_stroke(opacity=0.2 + 0.3 * s)
        reach_ring.add_updater(ring_upd)

        # good phone pulses green, blocked phone flickers coral
        def ok_upd(m):
            s = 0.5 + 0.5 * np.sin(2.4 * t.get_value())
            m.set_stroke(width=2.0 + 2.0 * s, opacity=0.7 + 0.3 * s)
        phone_ok.add_updater(ok_upd)

        def blk_phone_upd(m):
            s = 0.5 + 0.5 * np.sin(5.0 * t.get_value())
            m.set_stroke(opacity=0.35 + 0.4 * s)
        phone_b.add_updater(blk_phone_upd)

        # caption
        cap = Text("barely a block — blocked by walls, rain, leaves, your hand",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.3)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
