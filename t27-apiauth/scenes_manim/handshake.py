"""Scene: PROVING WHO YOU ARE — a loop of API auth handshakes.

Class `Handshake` (~18s). A CLIENT box (TEAL, left) and a SERVER box
(VIOLET, right) with a request arrow between them. The scene cycles through
four representative auth methods, credentials riding the request arrow:
  (a) API KEY   — a key token rides to the server, server shows a green check.
  (b) BEARER    — client trades a password for a token, token rides along.
  (c) OAUTH     — three-party dance via an AUTH SERVER (GOLD): redirect,
                   consent, scoped token back.
  (d) mTLS      — both sides show certificate badges before the channel opens.
The active method's MONO label cycles up top. Caption:
  "every method: prove identity before data flows".

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze. Legible enough to sit behind the title.
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
    Line,
    Arrow,
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


class Handshake(Scene):
    def construct(self):
        title = Text("Proving who you are, before data flows",
                     font=HEAD, color=INK, weight="SEMIBOLD").scale(0.5)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- CLIENT (left) & SERVER (right) ----------------------------------
        client = RoundedRectangle(
            corner_radius=0.14, width=2.6, height=2.0,
            stroke_color=TEAL, stroke_width=2.5,
            fill_color="#07201D", fill_opacity=0.5,
        ).shift(LEFT * 4.3 + DOWN * 0.2)
        client_lbl = Text("CLIENT", font=MONO, color=TEAL,
                          weight="BOLD").scale(0.34)
        client_lbl.move_to(client.get_center())

        server = RoundedRectangle(
            corner_radius=0.14, width=2.6, height=2.0,
            stroke_color=VIOLET, stroke_width=2.5,
            fill_color="#160A24", fill_opacity=0.5,
        ).shift(RIGHT * 4.3 + DOWN * 0.2)
        server_lbl = Text("SERVER", font=MONO, color=VIOLET,
                          weight="BOLD").scale(0.34)
        server_lbl.move_to(server.get_center())

        self.play(Create(client), Create(server), run_time=0.7)
        self.play(FadeIn(client_lbl), FadeIn(server_lbl), run_time=0.3)

        # --- AUTH SERVER (top-centre, used only by OAUTH) --------------------
        auth = RoundedRectangle(
            corner_radius=0.12, width=2.4, height=1.1,
            stroke_color=GOLD, stroke_width=2.2,
            fill_color="#1E180A", fill_opacity=0.5,
        ).move_to(UP * 2.25)
        auth_lbl = Text("AUTH SERVER", font=MONO, color=GOLD).scale(0.26)
        auth_lbl.move_to(auth.get_center())
        auth_group = VGroup(auth, auth_lbl)
        self.add(auth_group)

        # --- request channel between client & server ------------------------
        chan_y = client.get_center()[1]
        left_x = client.get_right()[0] + 0.1
        right_x = server.get_left()[0] - 0.1
        channel = Line(
            np.array([left_x, chan_y, 0]),
            np.array([right_x, chan_y, 0]),
            stroke_color=SECOND, stroke_width=2, stroke_opacity=0.35,
        )
        req_arrow = Arrow(
            np.array([left_x, chan_y, 0]),
            np.array([right_x, chan_y, 0]),
            stroke_color=SILVER, stroke_width=3,
            buff=0.0, max_tip_length_to_length_ratio=0.05,
        )
        self.play(Create(channel), run_time=0.4)
        self.add(req_arrow)

        # --- top method label -----------------------------------------------
        method_lbl = Text("API KEY", font=MONO, color=GREEN,
                          weight="BOLD").scale(0.42)
        method_lbl.next_to(title, DOWN, buff=0.22)
        method_lbl._idx = -1
        self.add(method_lbl)

        # method step line (small, under the label)
        step_lbl = Text("key rides the request", font=MONO,
                        color=SECOND).scale(0.26)
        step_lbl.next_to(method_lbl, DOWN, buff=0.12)
        step_lbl._key = ""
        self.add(step_lbl)

        # caption bottom
        caption = Text("every method: prove identity before data flows",
                       font=HEAD, color=SILVER).scale(0.34)
        caption.to_edge(DOWN, buff=0.4)
        self.add(caption)

        # --- riding credential token (reused across methods) -----------------
        token = RoundedRectangle(
            corner_radius=0.06, width=0.9, height=0.42,
            stroke_width=2.0, fill_opacity=0.85,
        )
        token_lbl = Text("key", font=MONO, color=BG).scale(0.22)
        token_group = VGroup(token, token_lbl)
        token_group.set_opacity(0.0)
        self.add(token_group)

        # --- server check mark (text) ---------------------------------------
        check = Text("OK", font=MONO, color=GREEN, weight="BOLD").scale(0.4)
        check.move_to(server.get_center() + UP * 0.55)
        check.set_opacity(0.0)
        self.add(check)

        # --- certificate badges (mTLS) --------------------------------------
        cert_c = Text("[CERT]", font=MONO, color=TEAL).scale(0.26)
        cert_c.move_to(client.get_top() + UP * 0.25)
        cert_c.set_opacity(0.0)
        cert_s = Text("[CERT]", font=MONO, color=VIOLET).scale(0.26)
        cert_s.move_to(server.get_top() + UP * 0.25)
        cert_s.set_opacity(0.0)
        self.add(cert_c, cert_s)

        # --- OAUTH redirect paths (client -> auth -> client) -----------------
        path_up = Line(
            client.get_top(), auth.get_bottom() + LEFT * 0.6,
            stroke_color=GOLD, stroke_width=2, stroke_opacity=0.0,
        )
        path_down = Line(
            auth.get_bottom() + RIGHT * 0.6, client.get_top() + RIGHT * 0.2,
            stroke_color=GOLD, stroke_width=2, stroke_opacity=0.0,
        )
        self.add(path_up, path_down)

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        # Method cycle definition: label, color, step text, token face text.
        methods = [
            ("API KEY", GREEN, "key rides the request", "key"),
            ("BEARER TOKEN", TEAL, "trade password for token", "tok"),
            ("OAUTH 2.0", GOLD, "redirect -> consent -> scoped token", "scope"),
            ("mTLS", VIOLET, "both prove certificates first", "cert"),
        ]
        PHASE = 4.2  # seconds per method

        c_green = ManimColor(GREEN)
        c_teal = ManimColor(TEAL)
        c_gold = ManimColor(GOLD)
        c_violet = ManimColor(VIOLET)
        method_colors = [c_green, c_teal, c_gold, c_violet]

        def cur_idx():
            return int(t.get_value() // PHASE) % len(methods)

        def cur_frac():
            return (t.get_value() % PHASE) / PHASE

        # --- top method label updater ----------------------------------------
        def method_upd(m):
            idx = cur_idx()
            if idx != m._idx:
                m._idx = idx
                name, col, _step, _face = methods[idx]
                new = Text(name, font=MONO, color=col,
                           weight="BOLD").scale(0.42)
                new.move_to(m.get_center())
                m.become(new)
            # gentle pulse
            m.set_opacity(0.8 + 0.2 * (0.5 + 0.5 *
                                       np.sin(t.get_value() * 2.4)))
        method_lbl.add_updater(method_upd)

        def step_upd(m):
            idx = cur_idx()
            step = methods[idx][2]
            if step != m._key:
                m._key = step
                new = Text(step, font=MONO, color=SECOND).scale(0.26)
                new.move_to(np.array([title.get_center()[0],
                                      m.get_center()[1], 0]))
                m.become(new)
        step_lbl.add_updater(step_upd)

        # --- request arrow: steady travelling pulse (always alive) -----------
        def arrow_upd(m):
            # subtle breathing of stroke so channel reads "live"
            o = 0.4 + 0.5 * (0.5 + 0.5 * np.sin(t.get_value() * 3.0))
            m.set_stroke(opacity=o)
        req_arrow.add_updater(arrow_upd)

        # --- AUTH SERVER highlight (only lit during OAUTH) -------------------
        def auth_upd(m):
            on = 1.0 if cur_idx() == 2 else 0.22
            m[0].set_stroke(opacity=on)
            m[1].set_opacity(on)
        auth_group.add_updater(auth_upd)

        def path_upd_factory(line, active_sub):
            def _upd(m):
                on = 0.0
                if cur_idx() == 2:
                    f = cur_frac()
                    if active_sub == 0 and f < 0.5:
                        on = 0.8
                    elif active_sub == 1 and f >= 0.5:
                        on = 0.8
                m.set_stroke(opacity=on)
            return _upd
        path_up.add_updater(path_upd_factory(path_up, 0))
        path_down.add_updater(path_upd_factory(path_down, 1))

        # --- certificate badges (only during mTLS) --------------------------
        def cert_upd(m):
            if cur_idx() == 3:
                f = cur_frac()
                m.set_opacity(np.clip(f * 2.4, 0.0, 1.0))
            else:
                m.set_opacity(0.0)
        cert_c.add_updater(cert_upd)
        cert_s.add_updater(cert_upd)

        # --- server OK check -------------------------------------------------
        def check_upd(m):
            idx = cur_idx()
            f = cur_frac()
            # token lands around f ~ 0.7, flash the check after
            if idx in (0, 1) and f > 0.68:
                m.set_opacity(np.clip((f - 0.68) * 6.0, 0.0, 1.0))
            elif idx == 2 and f > 0.75:
                m.set_opacity(np.clip((f - 0.75) * 6.0, 0.0, 1.0))
            elif idx == 3 and f > 0.6:
                m.set_opacity(np.clip((f - 0.6) * 4.0, 0.0, 1.0))
            else:
                m.set_opacity(0.0)
        check.add_updater(check_upd)

        # --- riding credential token ----------------------------------------
        spawn = np.array([left_x + 0.15, chan_y, 0])
        land = np.array([right_x - 0.15, chan_y, 0])
        auth_pt = auth.get_center()
        client_top = client.get_top() + UP * 0.1

        def token_upd(m):
            idx = cur_idx()
            f = cur_frac()
            name, col, _step, face = methods[idx]
            rect, lbl = m[0], m[1]
            # relabel token face when needed
            if lbl.text != face:
                new = Text(face, font=MONO, color=BG).scale(0.22)
                new.move_to(rect.get_center())
                lbl.become(new)
            rect.set_stroke(color=col)
            rect.set_fill(color=col)

            if idx in (0, 1):
                # for BEARER, a short "trade" dwell near the client first
                if idx == 1 and f < 0.25:
                    m.move_to(spawn + LEFT * 0.0)
                    m.set_opacity(np.clip(f * 6.0, 0.0, 1.0))
                    return
                start_f = 0.25 if idx == 1 else 0.05
                travel = np.clip((f - start_f) / (0.72 - start_f), 0.0, 1.0)
                eased = rate_functions.ease_in_out_quad(travel)
                pos = spawn * (1 - eased) + land * eased
                m.move_to(pos)
                vis = 1.0 if f < 0.74 else np.clip(1.0 - (f - 0.74) * 8, 0, 1)
                m.set_opacity(np.clip(min(f * 6.0, 1.0), 0.0, 1.0) * vis)
            elif idx == 2:
                # OAUTH: client -> auth (0..0.45), auth -> client (0.45..0.6),
                # then scoped token client -> server (0.6..0.9)
                if f < 0.45:
                    tr = rate_functions.ease_in_out_quad(f / 0.45)
                    pos = client_top * (1 - tr) + auth_pt * tr
                    m.move_to(pos)
                    m.set_opacity(np.clip(f * 6.0, 0.0, 1.0))
                elif f < 0.6:
                    tr = rate_functions.ease_in_out_quad((f - 0.45) / 0.15)
                    pos = auth_pt * (1 - tr) + client_top * tr
                    m.move_to(pos)
                    m.set_opacity(1.0)
                else:
                    tr = rate_functions.ease_in_out_quad(
                        np.clip((f - 0.6) / 0.28, 0.0, 1.0))
                    pos = spawn * (1 - tr) + land * tr
                    m.move_to(pos)
                    vis = (1.0 if f < 0.9
                           else np.clip(1.0 - (f - 0.9) * 10, 0, 1))
                    m.set_opacity(vis)
            else:
                # mTLS: no single token rides; hide it, badges do the talking
                m.set_opacity(0.0)
        token_group.add_updater(token_upd)

        # --- a few generic data packets flowing after auth succeeds ----------
        data_packets = VGroup()
        rng = np.random.default_rng(7)
        for k in range(5):
            d = Dot(color=SILVER, radius=0.05)
            data_packets.add(d)
        self.add(data_packets)

        def data_factory(kk, ph):
            def _upd(m):
                f = cur_frac()
                col = method_colors[cur_idx()]
                m.set_color(col)
                # data only streams once auth has "landed" (late in phase)
                if f < 0.8:
                    m.set_opacity(0.0)
                    return
                local = ((t.get_value() * 1.6 + ph) % 1.0)
                pos = spawn * (1 - local) + land * local
                m.move_to(pos + UP * 0.0)
                m.set_opacity(0.6 * (1 - local))
            return _upd
        for kk, d in enumerate(data_packets):
            d.add_updater(data_factory(kk, kk * 0.2))

        self.play(t.animate.set_value(18.0), run_time=18.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
