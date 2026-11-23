"""Scene: symmetric vs asymmetric encryption.

Class `Twokeys` (~18s). LEFT: a single shared KEY that both locks and unlocks
a box, turning back and forth — "one shared key · fast". RIGHT: a key PAIR — a
PUBLIC key (AMBER) that locks the box and a PRIVATE key (GREEN) that unlocks it;
only the private opens what the public locked.

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Text,
    VGroup,
    Circle,
    Line,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    interpolate_color,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
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


def make_key(color):
    """A simple key: round bow + straight shaft + two teeth."""
    bow = Circle(radius=0.22, stroke_color=color, stroke_width=4,
                 fill_opacity=0)
    bow.move_to(LEFT * 0.55)
    shaft = Line(LEFT * 0.33, RIGHT * 0.6, stroke_color=color, stroke_width=4)
    tooth1 = Line(RIGHT * 0.45 + UP * 0.0, RIGHT * 0.45 + DOWN * 0.18,
                  stroke_color=color, stroke_width=4)
    tooth2 = Line(RIGHT * 0.6 + UP * 0.0, RIGHT * 0.6 + DOWN * 0.22,
                  stroke_color=color, stroke_width=4)
    return VGroup(bow, shaft, tooth1, tooth2)


class Twokeys(Scene):
    def construct(self):
        title = Text("Two ways to lock a box", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- LEFT: symmetric -------------------------------------------------
        L = LEFT * 3.6 + DOWN * 0.2
        head_sym = Text("SYMMETRIC", font=MONO, color=TEAL,
                        weight="BOLD").scale(0.34)
        head_sym.move_to(L + UP * 2.1)
        box_sym = RoundedRectangle(corner_radius=0.12, width=1.9, height=1.5,
                                   stroke_color=TEAL, stroke_width=3,
                                   fill_color="#0C1A18", fill_opacity=0.9)
        box_sym.move_to(L + DOWN * 0.1)
        shackle_sym = Circle(radius=0.3, stroke_color=TEAL, stroke_width=4,
                             fill_opacity=0)
        shackle_sym.move_to(box_sym.get_top() + UP * 0.12)
        key_sym = make_key(TEAL)
        key_sym.move_to(L + RIGHT * 0.1 + DOWN * 0.1)
        lbl_sym = Text("one shared key · fast", font=HEAD, color=TEAL).scale(0.32)
        lbl_sym.move_to(L + DOWN * 1.65)

        # --- RIGHT: asymmetric ----------------------------------------------
        R = RIGHT * 3.6 + DOWN * 0.2
        head_asym = Text("ASYMMETRIC", font=MONO, color=VIOLET,
                         weight="BOLD").scale(0.34)
        head_asym.move_to(R + UP * 2.1)
        box_asym = RoundedRectangle(corner_radius=0.12, width=1.9, height=1.5,
                                    stroke_color=VIOLET, stroke_width=3,
                                    fill_color="#140C1E", fill_opacity=0.9)
        box_asym.move_to(R + DOWN * 0.1)
        shackle_asym = Circle(radius=0.3, stroke_color=VIOLET, stroke_width=4,
                              fill_opacity=0)
        shackle_asym.move_to(box_asym.get_top() + UP * 0.12)
        pub_key = make_key(AMBER)
        pub_key.scale(0.8).move_to(R + LEFT * 1.55 + UP * 1.0)
        priv_key = make_key(GREEN)
        priv_key.scale(0.8).move_to(R + RIGHT * 1.55 + UP * 1.0)
        pub_lbl = Text("public\n(locks)", font=MONO, color=AMBER).scale(0.24)
        pub_lbl.next_to(pub_key, DOWN, buff=0.12)
        priv_lbl = Text("private\n(opens)", font=MONO, color=GREEN).scale(0.24)
        priv_lbl.next_to(priv_key, DOWN, buff=0.12)
        lbl_asym = Text("public locks · only the private opens", font=HEAD,
                        color=VIOLET).scale(0.28)
        lbl_asym.move_to(R + DOWN * 1.65)

        self.play(
            FadeIn(head_sym), FadeIn(head_asym),
            Create(box_sym), Create(box_asym),
            Create(shackle_sym), Create(shackle_asym),
            run_time=0.9,
        )
        self.play(
            FadeIn(key_sym), FadeIn(pub_key), FadeIn(priv_key),
            FadeIn(pub_lbl), FadeIn(priv_lbl),
            FadeIn(lbl_sym), FadeIn(lbl_asym),
            run_time=0.7,
        )

        caption = Text("public locks · only the private opens", font=HEAD,
                       color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # state words that change with lock/unlock
        state_sym = Text("", font=MONO, color=TEAL).scale(0.26)
        state_sym.move_to(box_sym.get_center())
        state_asym = Text("", font=MONO, color=VIOLET).scale(0.26)
        state_asym.move_to(box_asym.get_center())
        self.add(state_sym, state_asym)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 18.0
        key_sym_home = key_sym.get_center()
        pub_home = pub_key.get_center()
        priv_home = priv_key.get_center()

        # LEFT key turns back and forth; box locks/unlocks with it
        key_sym._ang = 0.0

        def sym_key_upd(m):
            tt = t.get_value()
            ang = 0.9 * np.sin(1.6 * tt)
            delta = ang - m._ang
            m.rotate(delta, about_point=key_sym_home + LEFT * 0.55)
            m._ang = ang
        key_sym.add_updater(sym_key_upd)

        def sym_box_upd(m):
            tt = t.get_value()
            locked = np.sin(1.6 * tt) >= 0  # same key does both
            col = TEAL
            m.set_stroke(col, width=3 + (1.5 if locked else 0))
            m.set_fill("#0C1A18",
                       opacity=0.95 if locked else 0.45)
        box_sym.add_updater(sym_box_upd)

        def sym_shackle_upd(m):
            tt = t.get_value()
            locked = np.sin(1.6 * tt) >= 0
            m.set_stroke(TEAL, opacity=1.0 if locked else 0.35)
        shackle_sym.add_updater(sym_shackle_upd)

        def sym_state_upd(m):
            tt = t.get_value()
            locked = np.sin(1.6 * tt) >= 0
            word = "LOCKED" if locked else "open"
            if m.text != word:
                new = Text(word, font=MONO, color=TEAL).scale(0.26)
                new.move_to(box_sym.get_center())
                m.become(new)
        state_sym.add_updater(sym_state_upd)

        # RIGHT: public key swings in to lock, then private swings in to open.
        # Phase cycle of period 6s: 0-2 public locks, 2-4 locked, 4-6 private opens
        R_period = 6.0

        def pub_upd(m):
            tt = t.get_value() % R_period
            frac = float(np.clip(tt / 2.0, 0.0, 1.0)) if tt < 2.0 else \
                float(np.clip(1.0 - (tt - 2.0) / 1.0, 0.0, 1.0)) if tt < 3.0 else 0.0
            target = box_asym.get_top() + UP * 0.12 + RIGHT * 0.1
            pos = pub_home + (target - pub_home) * frac
            m.move_to(pos)
            m.set_opacity(0.35 + 0.65 * frac)
        pub_key.add_updater(pub_upd)

        def priv_upd(m):
            tt = t.get_value() % R_period
            if tt < 4.0:
                frac = 0.0
            else:
                frac = float(np.clip((tt - 4.0) / 1.5, 0.0, 1.0))
            target = box_asym.get_top() + UP * 0.12 + RIGHT * 0.1
            pos = priv_home + (target - priv_home) * frac
            m.move_to(pos)
            m.set_opacity(0.35 + 0.65 * frac)
        priv_key.add_updater(priv_upd)

        def asym_box_upd(m):
            tt = t.get_value() % R_period
            # locked after public engages (t>=1) until private opens (t>=5)
            locked = 1.0 <= tt < 5.0
            m.set_stroke(VIOLET, width=3 + (1.5 if locked else 0))
            m.set_fill("#140C1E", opacity=0.95 if locked else 0.45)
        box_asym.add_updater(asym_box_upd)

        def asym_shackle_upd(m):
            tt = t.get_value() % R_period
            locked = 1.0 <= tt < 5.0
            col = interpolate_color(ManimColor(GREEN), ManimColor(AMBER),
                                    1.0 if locked else 0.0)
            m.set_stroke(col, opacity=1.0 if locked else 0.35)
        shackle_asym.add_updater(asym_shackle_upd)

        def asym_state_upd(m):
            tt = t.get_value() % R_period
            if 1.0 <= tt < 5.0:
                word, col = "LOCKED", AMBER
            else:
                word, col = "open", GREEN
            if m.text != word:
                new = Text(word, font=MONO, color=col).scale(0.26)
                new.move_to(box_asym.get_center())
                m.become(new)
        state_asym.add_updater(asym_state_upd)

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
