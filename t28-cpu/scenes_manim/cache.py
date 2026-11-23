"""Scene 6: cache + pipeline + cores = fast.

Class `Cache` (~19s). Three speed tricks:
 (a) a memory hierarchy ladder REGISTERS -> L1 -> L2 -> L3 -> RAM, each bigger
     but slower/further; data mostly served from fast cache.
 (b) a PIPELINE as an assembly line where instructions I1,I2,I3 overlap across
     fetch/decode/execute stages.
 (c) MULTIPLE CORES as several small CPU blocks each running their own loop.
Caption: "cache + pipeline + cores = fast".

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
    Square,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
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


class Cache(Scene):
    def construct(self):
        title = Text("Three speed tricks", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.58)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # ===== (a) memory hierarchy ladder (left column) ====================
        hier = [("REG", 0.6, TEAL), ("L1", 0.8, GREEN), ("L2", 1.05, GREEN),
                ("L3", 1.35, TEAL), ("RAM", 1.75, SECOND)]
        ladder = VGroup()
        ladder_boxes = []
        base_x = -5.1
        for i, (nm, w, col) in enumerate(hier):
            y = 1.7 - i * 0.68
            box = RoundedRectangle(corner_radius=0.06, width=w, height=0.52,
                                   stroke_color=col, stroke_width=2,
                                   fill_color="#111318", fill_opacity=0.9)
            box.move_to([base_x + w / 2 - 0.3, y, 0])
            lbl = Text(nm, font=MONO, color=col).scale(0.24)
            lbl.move_to(box.get_center())
            ladder.add(box, lbl)
            ladder_boxes.append(box.get_center())
        hd = Text("hierarchy", font=MONO, color=SECOND).scale(0.26)
        hd.move_to([base_x + 0.3, 2.3, 0])
        fast = Text("fast", font=MONO, color=GREEN).scale(0.22)
        fast.move_to([base_x - 0.55, 1.7, 0])
        slow = Text("slow", font=MONO, color=SECOND).scale(0.22)
        slow.move_to([base_x - 0.55, -1.0, 0])
        self.play(FadeIn(ladder), FadeIn(hd), FadeIn(fast), FadeIn(slow),
                  run_time=1.0)

        # data token served mostly from the fast cache levels
        data_tok = Dot(ladder_boxes[1], color=AMBER, radius=0.1)
        self.add(data_tok)

        # ===== (b) pipeline / assembly line (centre-top) ====================
        stages = ["F", "D", "E"]
        stage_cols = {"F": GREEN, "D": VIOLET, "E": AMBER}
        pipe_x0 = -1.6
        pipe_y = 1.5
        slot_w = 1.1
        pipe_grp = VGroup()
        slot_centers = []
        for j, st in enumerate(stages):
            cx = pipe_x0 + j * slot_w
            slot = Square(side_length=0.9, stroke_color=SECOND,
                          stroke_width=1.5, fill_color="#111318",
                          fill_opacity=0.9).move_to([cx, pipe_y, 0])
            hdr = Text(st, font=MONO, color=SECOND).scale(0.26)
            hdr.move_to([cx, pipe_y + 0.75, 0])
            pipe_grp.add(slot, hdr)
            slot_centers.append(np.array([cx, pipe_y, 0]))
        pipe_lbl = Text("pipeline", font=MONO, color=INK).scale(0.28)
        pipe_lbl.move_to([pipe_x0 + slot_w, pipe_y - 0.85, 0])
        pipe_grp.add(pipe_lbl)
        self.play(FadeIn(pipe_grp), run_time=0.8)

        # three instruction tokens overlapping across stages
        instr_toks = []
        for k in range(3):
            tok = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.5,
                                   stroke_color=INK, stroke_width=2,
                                   fill_color="#1A1A20", fill_opacity=1.0)
            tx = Text(f"I{k + 1}", font=MONO, color=INK).scale(0.24)
            instr_toks.append((tok, tx))
            self.add(tok, tx)

        # ===== (c) multiple cores (right column) ============================
        core_centers = [np.array([3.9, 1.6, 0]), np.array([5.2, 1.6, 0]),
                        np.array([3.9, 0.3, 0]), np.array([5.2, 0.3, 0])]
        cores = []
        core_grp = VGroup()
        for i, cc in enumerate(core_centers):
            box = RoundedRectangle(corner_radius=0.1, width=1.0, height=1.0,
                                   stroke_color=GREEN, stroke_width=2,
                                   fill_color="#0E1A14", fill_opacity=0.9)
            box.move_to(cc)
            lbl = Text(f"core {i}", font=MONO, color=SECOND).scale(0.2)
            lbl.move_to(cc + DOWN * 0.3)
            ring = Dot(cc + UP * 0.12, color=GREEN, radius=0.07)
            core_grp.add(box, lbl, ring)
            cores.append((box, ring, cc))
        cores_lbl = Text("cores", font=MONO, color=GREEN).scale(0.28)
        cores_lbl.move_to([4.55, 2.3, 0])
        core_grp.add(cores_lbl)
        self.play(FadeIn(core_grp), run_time=0.9)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # (a) data token bounces mostly among the fast cache levels
        def data_upd(m):
            ph = (t.get_value() * 0.8) % 1.0
            # mostly stays in levels 0-2 (REG/L1/L2), occasional dip to RAM
            cycle = int(t.get_value() * 0.8) % 5
            seq = [0, 1, 0, 2, 1]  # mostly-fast access pattern
            idx = seq[cycle]
            nxt = seq[(cycle + 1) % 5]
            p0 = ladder_boxes[idx]
            p1 = ladder_boxes[nxt]
            m.move_to(p0 + (p1 - p0) * ph)
        data_tok.add_updater(data_upd)

        # highlight whichever cache level is serving
        c_dim = ManimColor("#2A2A30")

        def make_ladder(idx, col):
            c_hot = ManimColor(col)

            def _upd(m):
                dpos = data_tok.get_center()
                dist = np.linalg.norm(dpos - ladder_boxes[idx])
                hot = dist < 0.35
                m.set_stroke(interpolate_color(c_dim, c_hot,
                             1.0 if hot else 0.4),
                             width=2.8 if hot else 2.0)
            return _upd
        for i, (nm, w, col) in enumerate(hier):
            ladder[2 * i].add_updater(make_ladder(i, col))

        # (b) pipeline: three instructions overlap, each shifted by one stage
        PSTEP = 1.0  # seconds per stage advance

        def instr_pos(k, tt):
            # instruction k enters one stage later than k-1
            prog = tt / PSTEP - k
            if prog < 0:
                return None  # not yet entered
            stage_idx = prog % 4  # 0..3, with 3 = exited
            if stage_idx >= 3:
                return None  # exited the pipeline
            s = int(stage_idx)
            f = stage_idx - s
            if s >= 2:
                a = slot_centers[2]
                b = slot_centers[2] + RIGHT * slot_w
                return a + (b - a) * f, 2
            a = slot_centers[s]
            b = slot_centers[s + 1]
            return a + (b - a) * f, s

        def make_instr(k, tok_m, tx_m):
            def _upd_tok(m):
                res = instr_pos(k, t.get_value())
                if res is None:
                    m.set_opacity(0.0)
                    return
                pos, _ = res
                m.set_opacity(1.0)
                m.move_to(pos)
            return _upd_tok

        def make_instr_tx(k, tok_m):
            def _upd(m):
                res = instr_pos(k, t.get_value())
                if res is None:
                    m.set_opacity(0.0)
                    return
                pos, _ = res
                m.set_opacity(1.0)
                m.move_to(pos)
            return _upd
        for k, (tok, tx) in enumerate(instr_toks):
            tok.add_updater(make_instr(k, tok, tx))
            tx.add_updater(make_instr_tx(k, tok))

        # pipeline slots light under whichever instruction occupies them
        def make_slot(j):
            def _upd(m):
                occupied = False
                for k in range(3):
                    res = instr_pos(k, t.get_value())
                    if res is not None and res[1] == j:
                        occupied = True
                        break
                col = ManimColor(stage_cols[stages[j]])
                m.set_stroke(interpolate_color(c_dim, col,
                             0.9 if occupied else 0.35),
                             width=2.5 if occupied else 1.5)
            return _upd
        for j in range(3):
            pipe_grp[2 * j].add_updater(make_slot(j))

        # (c) cores each run their own loop pulse at different phases
        c_core_dim = ManimColor("#163024")
        c_core_hot = ManimColor(GREEN)
        for i, (box, ring, cc) in enumerate(cores):
            def make_core(bx, rg, center, phase):
                def _upd_box(m):
                    s = 0.5 + 0.5 * np.sin(3.0 * t.get_value() + phase)
                    m.set_stroke(interpolate_color(c_core_dim, c_core_hot,
                                 0.4 + 0.6 * s), width=2 + 1.5 * s)
                return _upd_box

            def make_ring(center, phase):
                def _upd(m):
                    ang = 2.0 * t.get_value() + phase
                    m.move_to(center + 0.22 * np.array(
                        [np.cos(ang), np.sin(ang), 0]))
                return _upd
            box.add_updater(make_core(box, ring, cc, i * 1.3))
            ring.add_updater(make_ring(cc, i * 1.3))

        # caption
        cap = Text("cache + pipeline + cores = fast",
                   font=HEAD, color=SECOND).scale(0.4)
        cap.to_edge(DOWN, buff=0.3)

        def cap_upd(m):
            m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 *
                          np.sin(1.3 * t.get_value())))
        cap.add_updater(cap_upd)
        self.add(cap)

        self.play(t.animate.set_value(19.0), run_time=19.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
