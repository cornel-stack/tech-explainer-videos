"""Messenger scene for "What Is an API?".

Concept: an API is a messenger. Your App never touches the Server directly.
It hands a *request* to the API, the API carries it to the Server (whose
private data stays behind a locked padlock), and a *response* comes back.

Dark design system (shared with the Remotion video):
  bg      #0A0A0C
  ink     warm cream #EDE7DB   secondary #9A958C
  accents amber #FFC24B, magenta #FF3E7F, mint #3DE0B0,
          violet #B06BFF, coral #FF6B4A, gold #E8C24A
  (NO blue, NO pure white)

Rendered at 1920x1080. No external assets — everything is a Manim primitive.
The diagram builds over ~12s, then holds with looping request/response
packets. Approximate runtime: ~27 seconds.
"""

from manim import (
    Scene,
    RoundedRectangle,
    Rectangle,
    Text,
    VGroup,
    Dot,
    Line,
    Circle,
    Arc,
    MoveAlongPath,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    smooth,
    linear,
    there_and_back,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
)

# ---- Dark palette ------------------------------------------------------------
BG = "#0A0A0C"
INK = "#EDE7DB"
INK_SOFT = "#9A958C"

AMBER = "#FFC24B"
MAGENTA = "#FF3E7F"
MINT = "#3DE0B0"
VIOLET = "#B06BFF"
CORAL = "#FF6B4A"
GOLD = "#E8C24A"

FONT = "Inter"


def glow_rect(width, height, color, corner_radius=0.22, fill_opacity=0.06):
    """A rounded card with a simulated neon glow (a thicker low-opacity
    stroke layered behind the crisp main stroke). Returns a VGroup."""
    halo = RoundedRectangle(
        corner_radius=corner_radius,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=11,
        stroke_opacity=0.18,
        fill_opacity=0.0,
    )
    body = RoundedRectangle(
        corner_radius=corner_radius,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3.0,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    return VGroup(halo, body)


def labelled_card(label, width, height, color, font_size=30, sub=None):
    """Glowing card with a centred cream label (and optional sub-label)."""
    g = glow_rect(width, height, color)
    txt = Text(label, font=FONT, font_size=font_size, color=INK)
    if sub:
        sub_txt = Text(sub, font=FONT, font_size=20, color=INK_SOFT)
        stack = VGroup(txt, sub_txt).arrange(DOWN, buff=0.14)
        stack.move_to(g.get_center())
        return VGroup(g, stack)
    txt.move_to(g.get_center())
    return VGroup(g, txt)


def pill(label, color, width=2.3, height=1.0, font_size=30):
    """A fully-rounded accent pill (used for the central API node)."""
    g = glow_rect(width, height, color, corner_radius=height / 2.0,
                  fill_opacity=0.12)
    txt = Text(label, font=FONT, font_size=font_size, color=INK)
    txt.move_to(g.get_center())
    return VGroup(g, txt)


def padlock(color, scale=0.5):
    """A tiny closed padlock icon (body + shackle). Returns a VGroup."""
    body = RoundedRectangle(
        corner_radius=0.08,
        width=0.9 * scale,
        height=0.7 * scale,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.14,
    )
    shackle = Arc(
        radius=0.28 * scale,
        start_angle=0,
        angle=3.14159,
        stroke_color=color,
        stroke_width=2.5,
    )
    shackle.next_to(body, UP, buff=-0.02 * scale)
    keyhole = Dot(radius=0.05 * scale, color=color)
    keyhole.move_to(body.get_center())
    g = VGroup(body, shackle, keyhole)
    return g


class Messenger(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Nodes: Your App (left) / API (center) / Server (right) ---------
        app = labelled_card("Your App", 3.0, 1.5, AMBER, font_size=32,
                            sub="client")
        app.move_to(LEFT * 5.2)

        api = pill("API", MAGENTA, width=2.4, height=1.1, font_size=34)
        api.move_to(ORIGIN)

        server = labelled_card("Server", 3.0, 1.5, VIOLET, font_size=32,
                              sub="the back end")
        server.move_to(RIGHT * 5.2)

        # Locked private-data box tucked beside/behind the server.
        lock = padlock(MINT, scale=0.7)
        lock_label = Text("private data", font=FONT, font_size=18,
                          color=INK_SOFT)
        lock_group = VGroup(lock, lock_label).arrange(DOWN, buff=0.12)
        lock_group.next_to(server, DOWN, buff=0.45)

        # --- Build: nodes appear left -> center -> right --------------------
        self.play(FadeIn(app, shift=RIGHT * 0.3), run_time=0.9)
        self.play(GrowFromCenter(api), run_time=0.8)
        self.play(FadeIn(server, shift=LEFT * 0.3), run_time=0.9)
        self.play(FadeIn(lock_group, shift=UP * 0.2), run_time=0.8)

        # --- Connecting rails (App -> API -> Server) ------------------------
        left_rail = Line(
            app[0].get_right(), api[0].get_left(),
            stroke_color=INK_SOFT, stroke_width=2.0, stroke_opacity=0.35,
        )
        right_rail = Line(
            api[0].get_right(), server[0].get_left(),
            stroke_color=INK_SOFT, stroke_width=2.0, stroke_opacity=0.35,
        )
        self.play(Create(left_rail), Create(right_rail), run_time=0.8)

        # Full path points used by both packets.
        p_app = app[0].get_right()
        p_api = api[0].get_center()
        p_srv = server[0].get_left()

        # --- Packet helpers --------------------------------------------------
        def make_packet(label, color):
            halo = Circle(radius=0.34, stroke_width=0,
                          fill_color=color, fill_opacity=0.22)
            core = RoundedRectangle(
                corner_radius=0.16, width=1.5, height=0.55,
                stroke_color=color, stroke_width=2.5,
                fill_color=color, fill_opacity=0.22,
            )
            txt = Text(label, font=FONT, font_size=20, color=INK)
            txt.move_to(core.get_center())
            pkt = VGroup(halo, core, txt)
            return pkt

        def send(pkt, a, mid, b, color, run_time=1.0):
            """Move a packet a -> mid -> b along the rails."""
            pkt.move_to(a)
            path1 = Line(a, mid)
            path2 = Line(mid, b)
            self.play(MoveAlongPath(pkt, path1, rate_func=smooth),
                      run_time=run_time)
            self.play(MoveAlongPath(pkt, path2, rate_func=smooth),
                      run_time=run_time)

        # --- (1) First request App -> Server (through the API) --------------
        req = make_packet("request", AMBER)
        req.move_to(p_app)
        self.play(FadeIn(req, scale=0.6), run_time=0.4)
        # Light up the API as the packet passes through.
        send(req, p_app, p_api, p_srv, AMBER, run_time=0.9)
        # Padlock stays CLOSED — a brief shake to show access denied directly.
        self.play(lock.animate.scale(1.12), run_time=0.25)
        self.play(lock.animate.scale(1 / 1.12), run_time=0.25)
        self.play(FadeOut(req, scale=0.6), run_time=0.3)

        # --- (2) Response Server -> App -------------------------------------
        resp = make_packet("response", MINT)
        resp.move_to(p_srv)
        self.play(FadeIn(resp, scale=0.6), run_time=0.4)
        send(resp, p_srv, p_api, p_app, MINT, run_time=0.9)
        self.play(FadeOut(resp, scale=0.6), run_time=0.3)

        # --- HOLD: gently loop request/response + ambient glow pulses -------
        # Pulsing halos behind the three nodes keep the frame alive.
        def ambient_pulse(target, color):
            halo = Circle(radius=0.1, stroke_width=0,
                          fill_color=color, fill_opacity=0.0)
            halo.move_to(target[0].get_center())
            return halo

        app_glow = ambient_pulse(app, AMBER)
        api_glow = ambient_pulse(api, MAGENTA)
        srv_glow = ambient_pulse(server, VIOLET)
        self.add(app_glow, api_glow, srv_glow)

        # Loop several request/response cycles for the long stable hold.
        for i in range(4):
            req = make_packet("request", AMBER)
            req.move_to(p_app)
            self.add(req)
            # Fade packet in while the node glows softly.
            self.play(
                req.animate.set_opacity(1.0),
                api_glow.animate.scale(14).set_opacity(0.12),
                rate_func=there_and_back,
                run_time=0.6,
            )
            send(req, p_app, p_api, p_srv, AMBER, run_time=0.85)
            # Padlock gives a tiny reassuring bob (stays closed).
            self.play(lock.animate.shift(UP * 0.06), run_time=0.2)
            self.play(lock.animate.shift(DOWN * 0.06), run_time=0.2)
            self.remove(req)

            resp = make_packet("response", MINT)
            resp.move_to(p_srv)
            self.add(resp)
            self.play(
                resp.animate.set_opacity(1.0),
                app_glow.animate.scale(14).set_opacity(0.12),
                rate_func=there_and_back,
                run_time=0.6,
            )
            send(resp, p_srv, p_api, p_app, MINT, run_time=0.85)
            self.remove(resp)
            self.wait(0.3)

        self.wait(1.0)
