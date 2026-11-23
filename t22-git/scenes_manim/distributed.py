"""Scene: distributed — same hashes everywhere, sync only what's new.

Class `Distributed` (~18s). Two object databases ("local" and "remote")
side by side, sharing some objects (by identical hash) and syncing only the
NEW objects across a link (push/pull). Clone = full copy of the graph.
Caption: "same hashes everywhere -> sync only what's new".

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
    Text,
    VGroup,
    Line,
    Arrow,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowArrow,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    DOWN,
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


def obj_node(hash_str, color, center, scale=1.0):
    box = RoundedRectangle(corner_radius=0.07, width=1.25 * scale,
                           height=0.55 * scale, stroke_color=color,
                           stroke_width=2.2, fill_color=color,
                           fill_opacity=0.1)
    box.move_to(center)
    hsh = Text(hash_str, font=MONO, color=INK).scale(0.22 * scale)
    hsh.move_to(center)
    return VGroup(box, hsh), box


class Distributed(Scene):
    def construct(self):
        title = Text("Every clone is the whole graph", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- two object databases side by side ------------------------------
        local_c = np.array([-3.7, -0.2, 0.0])
        remote_c = np.array([3.7, -0.2, 0.0])
        db_w, db_h = 3.6, 3.6

        local_db = RoundedRectangle(corner_radius=0.14, width=db_w, height=db_h,
                                    stroke_color=TEAL, stroke_width=2.5,
                                    fill_color=TEAL, fill_opacity=0.03)
        local_db.move_to(local_c)
        remote_db = RoundedRectangle(corner_radius=0.14, width=db_w, height=db_h,
                                     stroke_color=VIOLET, stroke_width=2.5,
                                     fill_color=VIOLET, fill_opacity=0.03)
        remote_db.move_to(remote_c)

        local_lbl = Text("local  .git", font=MONO, color=TEAL).scale(0.3)
        local_lbl.next_to(local_db, UP, buff=0.15)
        remote_lbl = Text("remote  origin", font=MONO, color=VIOLET).scale(0.3)
        remote_lbl.next_to(remote_db, UP, buff=0.15)

        self.play(Create(local_db), Create(remote_db), FadeIn(local_lbl),
                  FadeIn(remote_lbl), run_time=0.8)

        # --- SHARED objects (identical hash in both DBs) --------------------
        shared_hashes = ["1a2b3c", "4d5e6f", "9fb2a0"]
        shared_cols = [AMBER, AMBER, TEAL]
        # relative offsets inside a db box
        offs = [np.array([0, 1.0, 0]), np.array([0, 0.25, 0]),
                np.array([0, -0.5, 0])]

        local_shared = []
        remote_shared = []
        link_dashes = []
        for i, (h, col) in enumerate(zip(shared_hashes, shared_cols)):
            lg, lb = obj_node(h, col, local_c + offs[i])
            rg, rb = obj_node(h, col, remote_c + offs[i])
            local_shared.append((lg, lb))
            remote_shared.append((rg, rb))
            self.play(FadeIn(lg), FadeIn(rg), run_time=0.3)
            # thin green "identical hash" link between the matching pair
            dl = Line(lb.get_right(), rb.get_left(), stroke_color=GREEN,
                      stroke_width=1.5, stroke_opacity=0.35)
            link_dashes.append(dl)
            self.add(dl)

        same_lbl = Text("same hash = same object", font=MONO,
                        color=GREEN).scale(0.24)
        same_lbl.move_to([0, 1.5, 0])
        self.play(FadeIn(same_lbl), run_time=0.4)

        # --- a NEW object only in local, pushed across the link -------------
        new_off = np.array([0, -1.25, 0])
        new_g, new_b = obj_node("5e6f7a", AMBER, local_c + new_off)
        new_lbl = Text("new commit", font=MONO, color=AMBER).scale(0.2)
        new_lbl.next_to(new_b, DOWN, buff=0.08)
        self.play(GrowFromCenter(new_g), FadeIn(new_lbl), run_time=0.5)

        # push arrow local -> remote
        push_arr = Arrow(local_db.get_right(), remote_db.get_left(),
                         color=GREEN, stroke_width=4, buff=0.1,
                         max_tip_length_to_length_ratio=0.1)
        push_lbl = Text("push: send only the NEW object", font=MONO,
                        color=GREEN).scale(0.24)
        push_lbl.move_to([0, -2.6, 0])
        self.play(GrowArrow(push_arr), FadeIn(push_lbl), run_time=0.6)

        # the new object now also exists on remote
        rnew_g, rnew_b = obj_node("5e6f7a", AMBER, remote_c + new_off)
        self.play(FadeIn(rnew_g), run_time=0.4)

        clone_lbl = Text("clone = copy the whole graph", font=MONO,
                         color=SILVER).scale(0.24)
        clone_lbl.move_to([0, 0.4, 0])
        self.play(FadeIn(clone_lbl), run_time=0.4)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # databases breathe
        def ldb_upd(m):
            s = 0.5 + 0.5 * np.sin(1.3 * t.get_value())
            m.set_stroke(opacity=0.5 + 0.4 * s)
        local_db.add_updater(ldb_upd)

        def rdb_upd(m):
            s = 0.5 + 0.5 * np.sin(1.3 * t.get_value() + 1.0)
            m.set_stroke(opacity=0.5 + 0.4 * s)
        remote_db.add_updater(rdb_upd)

        # shared-object links pulse green (sync heartbeat)
        for i, dl in enumerate(link_dashes):
            def make_link(line, phase):
                def _upd(m):
                    s = 0.5 + 0.5 * np.sin(2.2 * t.get_value() + phase)
                    m.set_stroke(opacity=0.2 + 0.4 * s)
                return _upd
            dl.add_updater(make_link(dl, i * 0.8))

        # matching shared objects glow identically (same hash -> same glow)
        for i in range(len(shared_hashes)):
            def make_pair(lb, rb, col, phase):
                base = ManimColor(col)
                hot = ManimColor(GREEN)

                def _upd_l(m):
                    s = 0.5 + 0.5 * np.sin(2.2 * t.get_value() + phase)
                    m.set_stroke(color=interpolate_color(base, hot, 0.35 * s),
                                 opacity=0.6 + 0.4 * s)

                def _upd_r(m):
                    s = 0.5 + 0.5 * np.sin(2.2 * t.get_value() + phase)
                    m.set_stroke(color=interpolate_color(base, hot, 0.35 * s),
                                 opacity=0.6 + 0.4 * s)
                return _upd_l, _upd_r
            lu, ru = make_pair(local_shared[i][1], remote_shared[i][1],
                               shared_cols[i], i * 0.9)
            local_shared[i][1].add_updater(lu)
            remote_shared[i][1].add_updater(ru)

        # push arrow carries a travelling packet (dot sweeping left->right)
        packet = Dot(local_c + new_off, color=GOLD, radius=0.08)
        a_pt = local_db.get_right()
        b_pt = remote_db.get_left()

        def packet_upd(m):
            s = (t.get_value() * 0.6) % 1.0
            p = a_pt * (1 - s) + b_pt * s
            m.move_to(p)
            m.set_opacity(0.4 + 0.6 * np.sin(np.pi * s))
        packet.add_updater(packet_upd)
        self.add(packet)

        # the two "new" objects throb amber (freshly synced)
        def newl_upd(m):
            s = 0.5 + 0.5 * np.sin(2.6 * t.get_value())
            m.set_stroke(opacity=0.6 + 0.4 * s)
        new_b.add_updater(newl_upd)

        def newr_upd(m):
            s = 0.5 + 0.5 * np.sin(2.6 * t.get_value() + 1.3)
            m.set_stroke(opacity=0.6 + 0.4 * s)
        rnew_b.add_updater(newr_upd)

        # same-hash label pulses
        def same_upd(m):
            m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 *
                          np.sin(2.0 * t.get_value())))
        same_lbl.add_updater(same_upd)

        # caption
        cap = Text("same hashes everywhere -> sync only what's new",
                   font=HEAD, color=SECOND).scale(0.36)
        cap.to_edge(DOWN, buff=0.22)

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
