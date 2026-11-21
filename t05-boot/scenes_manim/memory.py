"""Memory — virtual memory via the MMU (~24s).

LEFT   = VIRTUAL ADDRESS SPACE (per-app, tidy 4 KB page boxes).
MIDDLE = PAGE TABLE / MMU translator block.
RIGHT  = PHYSICAL RAM (scattered frames).
BOTTOM = DISK box (for page faults).

A virtual page is looked up in the page table and mapped to a scattered
physical frame continuously; occasionally a PAGE FAULT fetches a page from
disk. Teal/green, translations flowing on a loop.
"""

from manim import (
    VGroup,
    RoundedRectangle,
    Rectangle,
    Line,
    Dot,
    Text,
    Scene,
    ValueTracker,
    Create,
    FadeIn,
    rate_functions,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)
import numpy as np

BG = "#08080B"
INK = "#EDECE6"
INK2 = "#8E8E8A"
AMBER = "#FFB020"
TEAL = "#2DD4BF"
GREEN = "#35FF9E"
VIOLET = "#9B8CFF"
CORAL = "#FF6B4A"
SILVER = "#C9CDD4"

MONO = "JetBrains Mono"
HEAD = "Inter"


def mono(txt, size=22, color=INK):
    try:
        return Text(txt, font=MONO, font_size=size, color=color)
    except Exception:
        return Text(txt, font="Courier New", font_size=size, color=color)


def head(txt, size=34, color=INK, weight="BOLD"):
    try:
        return Text(txt, font=HEAD, font_size=size, color=color, weight=weight)
    except Exception:
        return Text(txt, font_size=size, color=color, weight=weight)


class Memory(Scene):
    def construct(self):
        self.camera.background_color = BG
        clock = ValueTracker(0.0)

        title = head("VIRTUAL MEMORY & THE MMU", size=34, color=INK)
        title.to_edge(UP, buff=0.45)
        sub = mono("// every app thinks it owns all of RAM", size=19, color=INK2)
        sub.next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(sub), run_time=0.4)

        # ---------------- LEFT: virtual address space ----------------
        v_x = -5.1
        v_top = 1.9
        n_pages = 6
        v_pages = []
        v_group = VGroup()
        v_hdr = mono("VIRTUAL\nADDRESS SPACE", size=18, color=TEAL)
        v_hdr.move_to([v_x, v_top + 1.0, 0])
        for i in range(n_pages):
            y = v_top - i * 0.62
            box = RoundedRectangle(
                width=1.9, height=0.5, corner_radius=0.07,
                stroke_color=TEAL, stroke_width=1.8,
                fill_color=TEAL, fill_opacity=0.05,
            ).move_to([v_x, y, 0])
            lbl = mono(f"page {i}  4KB", size=13, color=INK).move_to(box.get_center())
            v_pages.append(box)
            v_group.add(box, lbl)

        # ---------------- MIDDLE: page table / MMU ----------------
        m_x = -1.4
        mmu = RoundedRectangle(
            width=2.5, height=4.4, corner_radius=0.14,
            stroke_color=GREEN, stroke_width=2.4,
            fill_color=GREEN, fill_opacity=0.05,
        ).move_to([m_x, -0.1, 0])
        mmu_glow = RoundedRectangle(
            width=2.62, height=4.52, corner_radius=0.16,
            stroke_color=GREEN, stroke_width=9, stroke_opacity=0.16,
            fill_opacity=0.0,
        ).move_to([m_x, -0.1, 0])
        mmu_hdr = mono("PAGE TABLE\n/ MMU", size=18, color=GREEN)
        mmu_hdr.move_to([m_x, 1.75, 0])
        # a few translation rows
        rows = VGroup()
        row_boxes = []
        for i in range(4):
            ry = 0.95 - i * 0.7
            rb = RoundedRectangle(
                width=2.1, height=0.5, corner_radius=0.06,
                stroke_color=INK2, stroke_width=1.3,
                fill_color=GREEN, fill_opacity=0.0,
            ).move_to([m_x, ry, 0])
            rt = mono(f"V{i} -> F?", size=14, color=INK2).move_to(rb.get_center())
            rows.add(rb, rt)
            row_boxes.append((rb, rt, i))

        # ---------------- RIGHT: physical RAM (scattered) ----------------
        r_x = 3.1
        ram_hdr = mono("PHYSICAL RAM", size=18, color=SILVER)
        ram_hdr.move_to([r_x + 1.0, v_top + 1.0, 0])
        # Scattered frame grid (3 cols x 4 rows) with a few highlighted.
        frame_positions = []
        frames = []
        f_group = VGroup()
        cols = 3
        rows_n = 4
        for i in range(cols * rows_n):
            cx = r_x + (i % cols) * 1.15
            cy = v_top - (i // cols) * 0.82
            # scatter jitter for "scattered" feel
            jig = ((i * 37) % 7 - 3) * 0.03
            box = RoundedRectangle(
                width=0.95, height=0.6, corner_radius=0.07,
                stroke_color=INK2, stroke_width=1.5,
                fill_color=SILVER, fill_opacity=0.04,
            ).move_to([cx + jig, cy, 0])
            fl = mono(f"F{i:02d}", size=11, color=INK2).move_to(box.get_center())
            frame_positions.append(box.get_center())
            frames.append(box)
            f_group.add(box, fl)

        # ---------------- BOTTOM: disk ----------------
        disk = RoundedRectangle(
            width=2.6, height=0.9, corner_radius=0.12,
            stroke_color=AMBER, stroke_width=2.0,
            fill_color=AMBER, fill_opacity=0.05,
        ).move_to([m_x, -2.95, 0])
        disk_lbl = mono("DISK (swap)", size=17, color=AMBER).move_to(disk.get_center())

        # Build everything in.
        self.play(FadeIn(v_hdr), FadeIn(ram_hdr), run_time=0.4)
        self.play(
            *[Create(b) for b in v_pages],
            run_time=0.7,
        )
        self.add(v_group)
        self.play(FadeIn(mmu_glow), Create(mmu), FadeIn(mmu_hdr), run_time=0.6)
        self.play(FadeIn(rows), run_time=0.4)
        self.play(*[Create(f) for f in frames], run_time=0.8)
        self.add(f_group)
        self.play(Create(disk), FadeIn(disk_lbl), run_time=0.45)

        # Which virtual page maps to which physical frame (looping sequence).
        # Occasionally a PAGE FAULT: fetch from disk first.
        mapping = [
            (0, 7, False),
            (2, 2, False),
            (4, 10, True),   # page fault
            (1, 5, False),
            (3, 9, True),    # page fault
            (5, 1, False),
        ]
        period = 2.4  # seconds per translation

        # ===================== CONTINUOUS MOTION =====================
        packet = Dot(radius=0.11, color=TEAL).set_z_index(6)
        fault = mono("PAGE FAULT", size=20, color=CORAL).set_z_index(7)
        fault.move_to([m_x, -1.75, 0])
        fault.set_opacity(0.0)

        mmu_entry = np.array([m_x - 1.25, -0.1, 0])
        mmu_exit = np.array([m_x + 1.25, -0.1, 0])
        disk_top = disk.get_top()

        def packet_up(m):
            t = clock.get_value()
            idx = int(t // period) % len(mapping)
            ph = (t % period) / period  # 0..1
            vp, fr, is_fault = mapping[idx]
            v_pos = v_pages[vp].get_right()
            f_pos = frame_positions[fr]

            if not is_fault:
                # VA box -> MMU -> physical frame
                if ph < 0.4:
                    a = rate_functions.ease_in_out_sine(ph / 0.4)
                    p = v_pos + (mmu_entry - v_pos) * a
                    m.set_color(TEAL)
                elif ph < 0.6:
                    a = (ph - 0.4) / 0.2
                    p = mmu_entry + (mmu_exit - mmu_entry) * a
                    m.set_color(GREEN)
                else:
                    a = rate_functions.ease_in_out_sine((ph - 0.6) / 0.4)
                    p = mmu_exit + (f_pos - mmu_exit) * a
                    m.set_color(GREEN)
            else:
                # VA -> MMU -> (fault) down to disk -> back to MMU -> frame
                if ph < 0.25:
                    a = rate_functions.ease_in_out_sine(ph / 0.25)
                    p = v_pos + (mmu_entry - v_pos) * a
                    m.set_color(TEAL)
                elif ph < 0.5:
                    a = rate_functions.ease_in_out_sine((ph - 0.25) / 0.25)
                    mc = np.array([m_x, -0.1, 0])
                    p = mc + (disk_top - mc) * a
                    m.set_color(CORAL)
                elif ph < 0.7:
                    a = rate_functions.ease_in_out_sine((ph - 0.5) / 0.2)
                    mc = np.array([m_x, -0.1, 0])
                    p = disk_top + (mc - disk_top) * a
                    m.set_color(AMBER)
                else:
                    a = rate_functions.ease_in_out_sine((ph - 0.7) / 0.3)
                    p = mmu_exit + (f_pos - mmu_exit) * a
                    m.set_color(GREEN)
            m.move_to(p)
        packet.add_updater(packet_up)

        def fault_up(m):
            t = clock.get_value()
            idx = int(t // period) % len(mapping)
            ph = (t % period) / period
            _, _, is_fault = mapping[idx]
            if is_fault and 0.25 <= ph < 0.7:
                m.set_opacity(0.6 + 0.4 * np.sin(ph * 30))
            else:
                m.set_opacity(0.0)
        fault.add_updater(fault_up)

        # Active MMU row lights up + shows the resolved frame.
        def rows_up(m):
            t = clock.get_value()
            idx = int(t // period) % len(mapping)
            vp, fr, is_fault = mapping[idx]
            active_row = idx % len(row_boxes)
            for rb, rt, i in row_boxes:
                if i == active_row:
                    rb.set_fill(GREEN, opacity=0.18)
                    rb.set_stroke(GREEN, width=2)
                    new = mono(f"V{vp} -> F{fr:02d}", size=14, color=GREEN)
                    new.move_to(rb.get_center())
                    rt.become(new)
                else:
                    rb.set_fill(GREEN, opacity=0.0)
                    rb.set_stroke(INK2, width=1.3)
        rows.add_updater(rows_up)

        # Highlight the active virtual page + target frame.
        def hl_up(m):
            t = clock.get_value()
            idx = int(t // period) % len(mapping)
            vp, fr, _ = mapping[idx]
            for j, b in enumerate(v_pages):
                if j == vp:
                    b.set_fill(TEAL, opacity=0.22).set_stroke(width=2.6)
                else:
                    b.set_fill(TEAL, opacity=0.05).set_stroke(width=1.8)
            for j, b in enumerate(frames):
                if j == fr:
                    b.set_fill(GREEN, opacity=0.25).set_stroke(GREEN, width=2.4)
                else:
                    b.set_fill(SILVER, opacity=0.04).set_stroke(INK2, width=1.5)
        # Attach to an invisible proxy dot so it ticks every frame.
        proxy = Dot(radius=0.001).set_opacity(0.0)
        proxy.add_updater(hl_up)

        # MMU glow breathing.
        def glow_up(m):
            t = clock.get_value()
            m.set_stroke(width=9 + 6 * (0.5 + 0.5 * np.sin(t * 2.2)))
        mmu_glow.add_updater(glow_up)

        # HUD counter: translations/sec feel.
        counter = mono("TLB lookups: 0", size=18, color=TEAL)
        counter.to_corner(DOWN + LEFT, buff=0.5)

        def counter_up(m):
            t = clock.get_value()
            val = int(t * 137)
            new = mono(f"TLB lookups: {val}", size=18, color=TEAL)
            new.move_to(m, aligned_edge=LEFT)
            m.become(new)
        counter.add_updater(counter_up)

        self.add(packet, fault, proxy, counter)

        self.play(clock.animate.set_value(14.4),
                  run_time=14.4, rate_func=rate_functions.linear)

        # Clean final frame.
        for m in (packet, fault, proxy, rows, mmu_glow, counter):
            m.clear_updaters()
        packet.set_opacity(0.0)
        fault.set_opacity(0.0)
        self.wait(0.3)
