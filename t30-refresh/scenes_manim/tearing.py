"""Scene: VRR — screen tearing vs fixed vs variable refresh.

Class `Tearing` (~18s). LEFT a "No Sync" monitor frame whose image is torn: a
vertical scan band whose top and bottom halves are horizontally offset, with the
tear line jumping around as a fixed refresh fights an out-of-phase GPU. RIGHT the
same scene under "VRR (G-Sync / FreeSync)": the GPU delivers frames at uneven
intervals and the monitor's refresh ticks snap to line up with each arrival, so
the image stays whole and smooth. Small readouts show fluctuating GPU fps and a
refresh Hz that tracks it. A caption cycles the story. Continuous loop.

Dark palette only, TEXT labels only, continuous motion from a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Line,
    Text,
    VGroup,
    Dot,
    ValueTracker,
    ManimColor,
    config,
    interpolate_color,
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


class Tearing(Scene):
    def construct(self):
        title = Text("VARIABLE REFRESH RATE", font=HEAD, color=INK,
                     weight="BOLD").scale(0.68)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- two monitor frames ----------------------------------------------
        mon_w, mon_h = 5.2, 3.6
        left_c = np.array([-3.5, -0.2, 0])
        right_c = np.array([3.5, -0.2, 0])

        left_frame = RoundedRectangle(
            corner_radius=0.12, width=mon_w, height=mon_h,
            stroke_color=CORAL, stroke_width=2.5,
            fill_color="#140B0A", fill_opacity=0.5,
        ).move_to(left_c)
        right_frame = RoundedRectangle(
            corner_radius=0.12, width=mon_w, height=mon_h,
            stroke_color=GREEN, stroke_width=2.5,
            fill_color="#0A140F", fill_opacity=0.5,
        ).move_to(right_c)

        left_lbl = Text("NO SYNC", font=MONO, color=CORAL,
                        weight="BOLD").scale(0.34)
        left_lbl.next_to(left_frame, UP, buff=0.14)
        right_lbl = Text("VRR  (G-Sync / FreeSync)", font=MONO, color=GREEN,
                         weight="BOLD").scale(0.34)
        right_lbl.next_to(right_frame, UP, buff=0.14)

        self.play(Create(left_frame), Create(right_frame), run_time=0.7)
        self.play(FadeIn(left_lbl), FadeIn(right_lbl), run_time=0.3)

        # --- content rows: horizontal stripes that scroll (the "image") ------
        N_ROWS = 14
        row_h = (mon_h - 0.3) / N_ROWS

        def build_rows(center, tint):
            rows = VGroup()
            top_y = center[1] + (mon_h - 0.3) / 2.0 - row_h / 2.0
            for i in range(N_ROWS):
                ry = top_y - i * row_h
                shade = interpolate_color(ManimColor("#101013"),
                                          ManimColor(tint), 0.18 + 0.5 *
                                          (0.5 + 0.5 * np.sin(i * 0.9)))
                r = Rectangle(width=mon_w - 0.3, height=row_h * 0.86,
                              stroke_width=0, fill_color=shade,
                              fill_opacity=0.9)
                r.move_to([center[0], ry, 0])
                rows.add(r)
            return rows, top_y

        left_rows, left_top = build_rows(left_c, TEAL)
        right_rows, right_top = build_rows(right_c, TEAL)
        self.play(FadeIn(left_rows), FadeIn(right_rows), run_time=0.5)

        # Tear line marker on the left monitor.
        tear_line = Line([left_c[0] - (mon_w - 0.3) / 2.0, 0, 0],
                         [left_c[0] + (mon_w - 0.3) / 2.0, 0, 0],
                         stroke_color=CORAL, stroke_width=3)
        self.add(tear_line)

        # --- GPU frame-arrival timeline under each monitor -------------------
        tl_y = left_c[1] - mon_h / 2.0 - 0.5
        left_tl = Line([left_c[0] - (mon_w - 0.3) / 2.0, tl_y, 0],
                       [left_c[0] + (mon_w - 0.3) / 2.0, tl_y, 0],
                       stroke_color=SECOND, stroke_width=1.5,
                       stroke_opacity=0.5)
        right_tl = Line([right_c[0] - (mon_w - 0.3) / 2.0, tl_y, 0],
                        [right_c[0] + (mon_w - 0.3) / 2.0, tl_y, 0],
                        stroke_color=SECOND, stroke_width=1.5,
                        stroke_opacity=0.5)
        left_tl_lbl = Text("fixed refresh ticks", font=MONO,
                           color=SECOND).scale(0.22)
        left_tl_lbl.next_to(left_tl, DOWN, buff=0.1)
        right_tl_lbl = Text("refresh snaps to GPU frames", font=MONO,
                            color=SECOND).scale(0.22)
        right_tl_lbl.next_to(right_tl, DOWN, buff=0.1)
        self.play(Create(left_tl), Create(right_tl),
                  FadeIn(left_tl_lbl), FadeIn(right_tl_lbl), run_time=0.5)

        # Readouts.
        left_read = Text("GPU 90 fps   refresh 60 Hz", font=MONO,
                         color=CORAL).scale(0.26)
        left_read.next_to(left_frame, DOWN, buff=0.14).shift(UP * 0.0)
        right_read = Text("GPU 90 fps   refresh 90 Hz", font=MONO,
                          color=GREEN).scale(0.26)
        right_read.next_to(right_frame, DOWN, buff=0.14)
        self.add(left_read, right_read)

        # Caption band.
        caption = Text("mismatch -> tearing", font=HEAD, color=INK).scale(0.4)
        caption.to_edge(DOWN, buff=0.3)
        caption._idx = -1
        self.add(caption)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        lw = mon_w - 0.3

        # --- LEFT: torn image. Rows below a jumping tear line shift sideways --
        def make_left_row(r, idx):
            base_y = r.get_y()
            frac = idx / (N_ROWS - 1)  # 0 top .. 1 bottom

            def _upd(m):
                tt = t.get_value()
                # Fixed 60Hz refresh phase, GPU frames out of phase -> tear.
                # Tear line position oscillates/jumps around mid screen.
                tear_frac = 0.5 + 0.28 * np.sin(tt * 2.3) \
                    + 0.12 * np.sign(np.sin(tt * 5.1))
                tear_frac = float(np.clip(tear_frac, 0.1, 0.9))
                # Rows below the tear are from an older frame -> offset.
                if frac > tear_frac:
                    off = 0.55 * np.sin(tt * 1.7) + 0.15
                else:
                    off = 0.1 * np.sin(tt * 1.7)
                m.move_to([left_c[0] + off, base_y, 0])
            return _upd

        for i, r in enumerate(left_rows):
            r.add_updater(make_left_row(r, i))

        def tear_line_upd(m):
            tt = t.get_value()
            tear_frac = 0.5 + 0.28 * np.sin(tt * 2.3) \
                + 0.12 * np.sign(np.sin(tt * 5.1))
            tear_frac = float(np.clip(tear_frac, 0.1, 0.9))
            top_edge = left_c[1] + (mon_h - 0.3) / 2.0
            y = top_edge - tear_frac * (mon_h - 0.3)
            m.put_start_and_end_on(
                [left_c[0] - lw / 2.0, y, 0],
                [left_c[0] + lw / 2.0, y, 0])
            m.set_opacity(0.5 + 0.5 * abs(np.sin(tt * 2.3)))
        tear_line.add_updater(tear_line_upd)

        # --- RIGHT: VRR — image stays whole, scrolls smoothly ----------------
        right_base_ys = [r.get_y() for r in right_rows]

        def make_right_row(r, idx):
            base_y = right_base_ys[idx]
            span = (mon_h - 0.3)

            def _upd(m):
                tt = t.get_value()
                # Smooth vertical scroll, wrapping within the screen -> whole.
                y = base_y - (tt * 0.6) % span
                if y < right_c[1] - span / 2.0:
                    y += span
                m.move_to([right_c[0], y, 0])
            return _upd

        for i, r in enumerate(right_rows):
            r.add_updater(make_right_row(r, i))

        # --- GPU frame arrivals: uneven ticks on both timelines --------------
        # Shared irregular cadence (seconds between GPU frames).
        rng = np.random.default_rng(7)
        intervals = rng.uniform(0.18, 0.5, size=60)
        arrival_times = np.cumsum(intervals)

        def arrivals_up_to(tt, window=lw):
            # Return list of (frac_x, age) for recent GPU frames.
            out = []
            recent = arrival_times[(arrival_times > tt - 2.2) &
                                   (arrival_times <= tt + 0.0)]
            for a in recent:
                age = tt - a
                fx = 1.0 - age / 2.2  # newest on the right
                out.append((fx, age))
            return out

        # GPU frame markers: green ticks drifting left on each timeline.
        gpu_ticks_left = VGroup(*[
            Line([0, tl_y - 0.14, 0], [0, tl_y + 0.14, 0],
                 stroke_color=AMBER, stroke_width=2) for _ in range(10)])
        gpu_ticks_right = VGroup(*[
            Line([0, tl_y - 0.14, 0], [0, tl_y + 0.14, 0],
                 stroke_color=GREEN, stroke_width=2) for _ in range(10)])
        self.add(gpu_ticks_left, gpu_ticks_right)

        def make_ticks_upd(group, center_x, col, snap):
            tick_list = list(group)

            def _upd(m):
                tt = t.get_value()
                arr = arrivals_up_to(tt)
                for j, tk in enumerate(tick_list):
                    if j < len(arr):
                        fx, age = arr[j]
                        x = center_x - lw / 2.0 + fx * lw
                        tk.set_opacity(float(np.clip(1.0 - age / 2.2, 0, 1)))
                        y0, y1 = tl_y - 0.14, tl_y + 0.14
                        tk.put_start_and_end_on([x, y0, 0], [x, y1, 0])
                        tk.set_stroke(col)
                    else:
                        tk.set_opacity(0.0)
            return _upd

        gpu_ticks_left.add_updater(
            make_ticks_upd(gpu_ticks_left, left_c[0], AMBER, False))
        gpu_ticks_right.add_updater(
            make_ticks_upd(gpu_ticks_right, right_c[0], GREEN, True))

        # Fixed refresh ticks on the LEFT timeline (evenly spaced, drifting).
        FIXED_PERIOD = 0.33  # ~ "60Hz" visual cadence
        fixed_ticks = VGroup(*[
            Line([0, tl_y - 0.1, 0], [0, tl_y + 0.1, 0],
                 stroke_color=SILVER, stroke_width=1.5) for _ in range(10)])
        self.add(fixed_ticks)

        def fixed_ticks_upd(m):
            tt = t.get_value()
            tick_list = list(fixed_ticks)
            phase = (tt % FIXED_PERIOD) / FIXED_PERIOD
            for j, tk in enumerate(tick_list):
                fx = 1.0 - ((j + phase) * FIXED_PERIOD) / 2.2
                if 0.0 <= fx <= 1.0:
                    x = left_c[0] - lw / 2.0 + fx * lw
                    tk.put_start_and_end_on([x, tl_y - 0.1, 0],
                                            [x, tl_y + 0.1, 0])
                    tk.set_opacity(0.45)
                else:
                    tk.set_opacity(0.0)
        fixed_ticks.add_updater(fixed_ticks_upd)

        # --- readouts: fluctuating GPU fps; refresh tracks on the right ------
        def make_fps(tt):
            return 90 + 22 * np.sin(tt * 1.3) + 8 * np.sin(tt * 3.7)

        def left_read_upd(m):
            fps = int(round(make_fps(t.get_value())))
            new = Text(f"GPU {fps} fps   refresh 60 Hz", font=MONO,
                       color=CORAL).scale(0.26)
            new.move_to(m.get_center())
            m.become(new)
        left_read.add_updater(left_read_upd)

        def right_read_upd(m):
            fps = int(round(make_fps(t.get_value())))
            new = Text(f"GPU {fps} fps   refresh {fps} Hz", font=MONO,
                       color=GREEN).scale(0.26)
            new.move_to(m.get_center())
            m.become(new)
        right_read.add_updater(right_read_upd)

        # --- caption cycles the story ----------------------------------------
        cap_chain = [
            ("mismatch -> tearing", CORAL),
            ("VRR flexes refresh to match the GPU", GREEN),
        ]

        def caption_upd(m):
            idx = int(t.get_value() // 4.0) % len(cap_chain)
            if idx != m._idx:
                m._idx = idx
                txt, col = cap_chain[idx]
                new = Text(txt, font=HEAD, color=col).scale(0.4)
                new.to_edge(DOWN, buff=0.3)
                new._idx = idx
                m.become(new)
                m._idx = idx
        caption.add_updater(caption_upd)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
