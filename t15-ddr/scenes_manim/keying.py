"""Scene: the NOTCH is a physical key — RAM sticks seated or rejected.

Class `Keying` (~22s). A long thin motherboard SLOT (rounded-rect outline)
has a small KEY TAB sticking up at a fixed x-position. RAM sticks slide in
from the right; each stick is a rounded rect with a NOTCH (a gap) at some
x-position. On a loop driven by t:
  (i)  a DDR3 stick, notch at the WRONG x -> hits the key tab, STOPS,
       flashes CORAL, "x WON'T FIT", retreats.
  (ii) a DDR4 stick, also wrong notch -> blocked, coral x.
  (iii)a DDR5 stick, notch LINES UP with the slot key -> slides all the way
       in and CLICKS, flashing GREEN with "SEATED".
Then the loop restarts. A bright marker sits on both the stick notch and the
slot key to emphasise alignment.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
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
    Dot,
    Line,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    rate_functions,
    interpolate_color,
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


class Keying(Scene):
    def construct(self):
        title = Text("The notch is a physical key", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- SLOT geometry ---------------------------------------------------
        slot_w, slot_h = 8.4, 0.9
        slot_cy = -0.4
        slot_left = -slot_w / 2.0
        slot_right = slot_w / 2.0

        slot = RoundedRectangle(
            corner_radius=0.1, width=slot_w, height=slot_h,
            stroke_color=SILVER, stroke_width=2.5,
            fill_color="#111114", fill_opacity=0.8,
        ).move_to(np.array([0, slot_cy, 0]))

        # Key tab sticks UP from the slot floor at a fixed x (the slot's key).
        # fraction along slot where the real DDR5 key lives.
        key_frac = 0.62
        key_x = slot_left + key_frac * slot_w
        key_tab = Rectangle(
            width=0.14, height=slot_h * 0.7,
            stroke_width=0, fill_color=GREEN, fill_opacity=0.95,
        )
        key_tab.move_to(np.array([key_x, slot_cy - slot_h * 0.12, 0]))

        key_mark = Dot(color=GREEN, radius=0.08)
        key_mark.move_to(np.array([key_x, slot_cy + slot_h * 0.5 + 0.18, 0]))

        slot_lbl = Text("MOTHERBOARD SLOT", font=MONO, color=SILVER).scale(0.26)
        slot_lbl.next_to(slot, DOWN, buff=0.28)

        key_lbl = Text("key", font=MONO, color=GREEN).scale(0.2)
        key_lbl.next_to(key_mark, UP, buff=0.08)

        self.play(Create(slot), run_time=0.7)
        self.play(FadeIn(key_tab), FadeIn(key_mark), FadeIn(key_lbl),
                  FadeIn(slot_lbl), run_time=0.5)

        # The slot floor y where sticks ride.
        stick_h = slot_h - 0.22
        seated_y = slot_cy
        resting_y = slot_cy + 2.1   # hover line before insertion

        # --- stick factory ---------------------------------------------------
        # notch_frac: where the gap sits along the stick (0..1 left->right).
        # A stick seats only if its notch_frac matches key_frac closely.
        def make_stick(name, notch_frac, accent):
            stick_w = slot_w - 0.3
            body = RoundedRectangle(
                corner_radius=0.08, width=stick_w, height=stick_h,
                stroke_color=accent, stroke_width=2.5,
                fill_color=BG, fill_opacity=0.92,
            )
            # Pin rows (text-only decoration): little tick marks along bottom.
            pins = VGroup()
            n_pins = 34
            for p in range(n_pins):
                px = -stick_w / 2.0 + 0.2 + p * (stick_w - 0.4) / (n_pins - 1)
                pin = Line(
                    np.array([px, -stick_h / 2.0 + 0.02, 0]),
                    np.array([px, -stick_h / 2.0 + 0.12, 0]),
                    stroke_color=GOLD, stroke_width=2, stroke_opacity=0.8,
                )
                pins.add(pin)

            # NOTCH = a gap carved into the bottom edge at notch_frac.
            notch_x_local = -stick_w / 2.0 + notch_frac * stick_w
            notch = Rectangle(
                width=0.18, height=stick_h * 0.55,
                stroke_width=0, fill_color=BG, fill_opacity=1.0,
            )
            notch.move_to(np.array([notch_x_local,
                                    -stick_h / 2.0 + stick_h * 0.275, 0]))
            notch_edge = Rectangle(
                width=0.18, height=stick_h * 0.55,
                stroke_color=accent, stroke_width=1.5,
                fill_opacity=0,
            ).move_to(notch)

            name_lbl = Text(name, font=MONO, color=accent,
                            weight="BOLD").scale(0.3)
            name_lbl.move_to(np.array([-stick_w / 2.0 + 0.9, 0.0, 0]))

            notch_mark = Dot(color=accent, radius=0.07)
            notch_mark.move_to(np.array([notch_x_local,
                                         stick_h / 2.0 + 0.16, 0]))

            g = VGroup(body, pins, notch, notch_edge, name_lbl, notch_mark)
            g.width_val = stick_w
            g.notch_x_local = notch_x_local
            g.accent = accent
            return g

        # Three sticks: DDR3 and DDR4 have wrong notches; DDR5 aligns.
        stick_defs = [
            ("DDR3", 0.30, AMBER, False),
            ("DDR4", 0.44, GOLD, False),
            ("DDR5", key_frac, GREEN, True),
        ]
        sticks = []
        for name, nf, accent, ok in stick_defs:
            s = make_stick(name, nf, accent)
            s.ok = ok
            s.set_opacity(0.0)
            sticks.append(s)
            self.add(s)

        # Off-screen spawn (far right), hover/approach positions.
        spawn_x = slot_right + slot_w * 0.9

        caption = Text(
            "the notch moves every generation — a deliberate physical lock",
            font=HEAD, color=SECOND).scale(0.32)
        caption.to_edge(DOWN, buff=0.72)
        caption2 = Text(
            "(so you can't fry a stick at the wrong voltage)",
            font=MONO, color=SECOND).scale(0.26)
        caption2.next_to(caption, DOWN, buff=0.12)
        self.play(FadeIn(caption), FadeIn(caption2), run_time=0.5)

        # Verdict label (reused, becomes per cycle).
        verdict = Text("", font=HEAD, color=CORAL, weight="BOLD").scale(0.5)
        verdict.move_to(np.array([0, slot_cy + 2.7, 0]))
        self.add(verdict)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        CYCLE = 6.0                 # seconds per stick attempt
        LOOP = CYCLE * len(sticks)  # full loop over all three

        # how far right the body's notch reaches toward the key when centred
        # relative to the slot. The stick is blocked when its notch doesn't sit
        # over the key: the solid body between notch and the matching slot key
        # collides. We model the stop distance geometrically.
        def stop_offset(stick):
            """Horizontal stop position (x of stick centre) when blocked.

            If the notch aligns with the key, the stick centres at 0 (seated).
            Otherwise the stick jams: its body edge meets the key tab, so it
            stops short by the notch<->key misalignment.
            """
            if stick.ok:
                return 0.0
            # misalignment in scene units; the farther the notch is from key,
            # the sooner it jams (stops further right).
            mis = abs((stick.notch_x_local) - (key_x))
            return min(2.4, 0.9 + mis * 1.4)

        def cycle_state():
            tt = t.get_value() % LOOP
            idx = int(tt // CYCLE)
            idx = min(idx, len(sticks) - 1)
            local = (tt - idx * CYCLE) / CYCLE   # 0..1 within this attempt
            return idx, local

        # Per-stick motion updater.
        for si, stick in enumerate(sticks):
            def make_stick_upd(s, idx):
                stop_x = stop_offset(s)

                def _upd(m):
                    cur, local = cycle_state()
                    if cur != idx:
                        m.set_opacity(0.0)
                        m.move_to(np.array([spawn_x, resting_y, 0]))
                        return
                    m.set_opacity(1.0)
                    # phases within an attempt:
                    #   0.00-0.45 : slide in from spawn toward target
                    #   0.45-0.70 : hold (blocked jiggle, or seated settle)
                    #   0.70-1.00 : retreat (blocked) or stay (seated)
                    target_x = 0.0 if s.ok else stop_x
                    if local < 0.45:
                        f = rate_functions.ease_in_out_quad(local / 0.45)
                        x = spawn_x * (1 - f) + target_x * f
                        y = resting_y * (1 - f) + seated_y * f
                    elif local < 0.70:
                        x = target_x
                        y = seated_y
                        if not s.ok:
                            # jam jiggle
                            x += 0.05 * np.sin((local - 0.45) * 60.0)
                    else:
                        if s.ok:
                            x = 0.0
                            y = seated_y
                        else:
                            f = rate_functions.ease_in_quad(
                                (local - 0.70) / 0.30)
                            x = target_x * (1 - f) + spawn_x * f
                            y = seated_y * (1 - f) + resting_y * f
                    m.move_to(np.array([x, y, 0]))
                return _upd
            stick.add_updater(make_stick_upd(stick, si))

        # Body colour flash: coral when blocked-hold, green when seated.
        for si, stick in enumerate(sticks):
            body = stick[0]
            accent_c = ManimColor(stick.accent)
            good_c = ManimColor(GREEN)
            bad_c = ManimColor(CORAL)

            def make_flash_upd(s, bd, ac, gc, bc, idx):
                def _upd(m):
                    cur, local = cycle_state()
                    if cur != idx:
                        m.set_stroke(color=ac)
                        return
                    if 0.45 <= local < 0.90:
                        pulse = 0.5 + 0.5 * np.sin(t.get_value() * 8.0)
                        if s.ok:
                            col = interpolate_color(ac, gc, 0.5 + 0.5 * pulse)
                        else:
                            col = interpolate_color(ac, bc, 0.5 + 0.5 * pulse)
                        m.set_stroke(color=col)
                    else:
                        m.set_stroke(color=ac)
                return _upd
            body.add_updater(make_flash_upd(stick, body, accent_c, good_c,
                                            bad_c, si))

        # Key tab pulses; glows GREEN brighter while the matching stick seats.
        base_key_green = ManimColor(GREEN)

        def key_upd(m):
            cur, local = cycle_state()
            seating = (sticks[cur].ok and local >= 0.45)
            pulse = 0.5 + 0.5 * np.sin(t.get_value() * 5.0)
            if seating:
                m.set_opacity(0.85 + 0.15 * pulse)
                m.scale_to_fit_height(slot_h * (0.7 + 0.05 * pulse))
            else:
                m.set_opacity(0.6 + 0.3 * pulse)
        key_tab.add_updater(key_upd)

        def key_mark_upd(m):
            pulse = 0.5 + 0.5 * np.sin(t.get_value() * 5.0)
            m.set_opacity(0.6 + 0.4 * pulse)
        key_mark.add_updater(key_mark_upd)

        # Verdict text: becomes per cycle with the right colour + glyph.
        verdict._key = (-1, False)

        def verdict_upd(m):
            cur, local = cycle_state()
            show = local >= 0.45
            key = (cur, show)
            if key != m._key:
                m._key = key
                if not show:
                    new = Text("", font=HEAD).scale(0.5)
                    new.move_to(np.array([0, slot_cy + 2.7, 0]))
                    m.become(new)
                    return
                s = sticks[cur]
                if s.ok:
                    new = Text("✓ SEATED", font=HEAD, color=GREEN,
                               weight="BOLD").scale(0.5)
                else:
                    name = stick_defs[cur][0]
                    new = Text(f"✗ WON'T FIT  ·  {name}", font=HEAD,
                               color=CORAL, weight="BOLD").scale(0.5)
                new.move_to(np.array([0, slot_cy + 2.7, 0]))
                m.become(new)
            # opacity breathe while shown
            if show:
                pulse = 0.5 + 0.5 * np.sin(t.get_value() * 6.0)
                m.set_opacity(0.7 + 0.3 * pulse)
        verdict.add_updater(verdict_upd)

        # Alignment read-out under the title: notch vs key.
        readout = Text("DDR3 notch vs key", font=MONO, color=SECOND).scale(0.28)
        readout.next_to(title, DOWN, buff=0.14)
        readout._idx = -1

        def readout_upd(m):
            cur, _ = cycle_state()
            if cur != m._idx:
                m._idx = cur
                name, nf, accent, ok = stick_defs[cur]
                if ok:
                    txt = f"{name}: notch lines up with the key -> seats"
                    col = GREEN
                else:
                    txt = f"{name}: notch in the wrong place -> blocked"
                    col = CORAL
                new = Text(txt, font=MONO, color=col).scale(0.28)
                new.move_to(m.get_center())
                m.become(new)
        readout.add_updater(readout_upd)
        self.add(readout)

        self.play(t.animate.set_value(LOOP * 1.2222), run_time=22.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
