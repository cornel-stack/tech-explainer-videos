"""Scene: HTTP is a postcard, HTTPS is a sealed envelope.

Class `Problem` (~18s). A message travels left->right along a path of hops
(router, Wi-Fi, ISP). As plain HTTP it is a POSTCARD with readable text
("password: ...") — every eye reads it and it flashes CORAL. Then HTTPS turns
the same message into a SEALED ENVELOPE with a padlock; now each eye sees only
scrambled characters (GREEN lock).

Dark palette only, TEXT labels only, continuous motion via a master
ValueTracker. No build-then-freeze.
"""

import numpy as np

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Dot,
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

_GLYPHS = "@#$%&*+=?/\\<>{}[]~^"


class Problem(Scene):
    def construct(self):
        title = Text("Your data crosses many hands on the way",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.55)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- the path of hops ------------------------------------------------
        path_y = 0.6
        x_start, x_end = -6.0, 6.0
        line = Line([x_start, path_y, 0], [x_end, path_y, 0],
                    stroke_color=SECOND, stroke_width=2)

        hop_names = ["router", "Wi-Fi", "ISP", "backbone"]
        hop_xs = np.linspace(x_start + 1.6, x_end - 1.6, len(hop_names))
        hops = VGroup()
        eyes = []
        for name, hx in zip(hop_names, hop_xs):
            box = RoundedRectangle(
                corner_radius=0.08, width=1.2, height=0.8,
                stroke_color=SILVER, stroke_width=2,
                fill_color="#14141A", fill_opacity=0.9,
            ).move_to([hx, path_y, 0])
            lbl = Text(name, font=MONO, color=SILVER).scale(0.26)
            lbl.move_to(box.get_center())
            # eye above the hop
            eye = Circle(radius=0.16, stroke_color=SECOND, stroke_width=2,
                         fill_opacity=0).move_to([hx, path_y + 0.95, 0])
            pupil = Dot(radius=0.06, color=SECOND).move_to(eye.get_center())
            eye_g = VGroup(eye, pupil)
            eyes.append((eye_g, hx))
            hops.add(VGroup(box, lbl, eye_g))

        self.play(Create(line), run_time=0.5)
        self.play(*[FadeIn(h) for h in hops], run_time=0.6)

        # endpoint labels
        sender = Text("you", font=MONO, color=INK).scale(0.3)
        sender.move_to([x_start - 0.2, path_y - 0.55, 0])
        receiver = Text("server", font=MONO, color=INK).scale(0.3)
        receiver.move_to([x_end + 0.2, path_y - 0.55, 0])
        self.play(FadeIn(sender), FadeIn(receiver), run_time=0.4)

        caption = Text("HTTP = postcard  ·  HTTPS = sealed envelope",
                       font=HEAD, color=SECOND).scale(0.4)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # mode label (HTTP first half, HTTPS second half)
        mode = Text("HTTP  —  readable by anyone", font=MONO, color=CORAL).scale(0.34)
        mode.next_to(title, DOWN, buff=0.2)
        mode._http = True
        self.add(mode)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)
        N = 18.0
        rng = np.random.default_rng(7)

        def is_https(tt):
            # First ~8s HTTP (postcard), then HTTPS (envelope); loops at 16.
            return (tt % 16.0) >= 8.0

        def mode_upd(m):
            https = is_https(t.get_value())
            if https and m._http:
                m._http = False
                new = Text("HTTPS  —  sealed & scrambled", font=MONO,
                           color=GREEN).scale(0.34)
                new.move_to(m)
                m.become(new)
            elif (not https) and (not m._http):
                m._http = True
                new = Text("HTTP  —  readable by anyone", font=MONO,
                           color=CORAL).scale(0.34)
                new.move_to(m)
                m.become(new)
        mode.add_updater(mode_upd)

        # --- travelling messages (postcards / envelopes) --------------------
        n_cards = 3
        period = 8.0
        cards = VGroup()
        for k in range(n_cards):
            # card face
            face = RoundedRectangle(corner_radius=0.06, width=1.5, height=0.95,
                                    stroke_color=GOLD, stroke_width=2,
                                    fill_color="#1A1708", fill_opacity=0.95)
            txt = Text("password:\nhunter2", font=MONO, color=INK).scale(0.22)
            txt.move_to(face.get_center())
            # padlock marker (shown only in HTTPS)
            lock = Text("LOCK", font=MONO, color=GREEN, weight="BOLD").scale(0.18)
            lock.move_to(face.get_corner(UP + RIGHT) + LEFT * 0.28 + DOWN * 0.18)
            g = VGroup(face, txt, lock)
            g.set_opacity(0)
            cards.add(g)
        self.add(cards)

        def make_card(card, kk):
            face, txt, lock = card
            offset = kk * (period / n_cards)

            def _upd(m):
                tt_global = t.get_value()
                https = is_https(tt_global)
                local = (tt_global + offset) % period
                frac = local / period
                x = x_start + (x_end - x_start) * frac
                m.move_to([x, path_y, 0])

                # fade in/out at the ends
                edge = min(frac, 1 - frac) * 4.0
                base_op = float(np.clip(edge, 0.0, 1.0))

                # proximity to any eye => "being read" flash
                near = 0.0
                for _, hx in eyes:
                    d = abs(x - hx)
                    near = max(near, float(np.clip(1.0 - d / 0.7, 0.0, 1.0)))

                if https:
                    # ENVELOPE: teal sealed, scrambled text, lock visible
                    face.set_stroke(GREEN)
                    face.set_fill("#0C1A12", opacity=base_op * 0.95)
                    # scramble the visible text when near an eye
                    seed = int(tt_global * 3) + kk
                    rr = np.random.default_rng(seed)
                    scrambled = "".join(_GLYPHS[rr.integers(0, len(_GLYPHS))]
                                        for _ in range(7))
                    new_txt = Text(scrambled, font=MONO, color=GREEN).scale(0.22)
                    new_txt.move_to(face.get_center())
                    txt.become(new_txt)
                    lock.set_opacity(base_op)
                else:
                    # POSTCARD: coral when being read, gold otherwise
                    col = interpolate_color(ManimColor(GOLD), ManimColor(CORAL),
                                            near)
                    face.set_stroke(col)
                    face.set_fill("#1A1708", opacity=base_op * 0.95)
                    txt.set_opacity(base_op)
                    txt.set_color(interpolate_color(ManimColor(INK),
                                                    ManimColor(CORAL), near))
                    lock.set_opacity(0)
            return _upd

        for kk, card in enumerate(cards):
            card.add_updater(make_card(card, kk))

        # --- eyes react: flash coral (HTTP) or stay calm green (HTTPS) ------
        def make_eye(eye_g, hx):
            eye, pupil = eye_g

            def _upd(m):
                tt = t.get_value()
                https = is_https(tt)
                # is a card right now near this hop?
                near = 0.0
                for k in range(n_cards):
                    local = (tt + k * (period / n_cards)) % period
                    x = x_start + (x_end - x_start) * (local / period)
                    near = max(near, float(np.clip(1.0 - abs(x - hx) / 0.6,
                                                   0.0, 1.0)))
                if https:
                    col = interpolate_color(ManimColor(SECOND),
                                            ManimColor(GREEN), near)
                else:
                    col = interpolate_color(ManimColor(SECOND),
                                            ManimColor(CORAL), near)
                eye.set_stroke(col, width=2 + 2 * near)
                pupil.set_color(col)
            return _upd

        for eye_g, hx in eyes:
            eye_g.add_updater(make_eye(eye_g, hx))

        self.play(t.animate.set_value(N), run_time=N,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
