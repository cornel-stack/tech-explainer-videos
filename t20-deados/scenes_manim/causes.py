"""Scene: What Killed Them — three causes of death for dead operating systems.

Class `Causes` (~18s). Three large labelled "cause of death" nodes across the
screen: TIMING (AMBER), MOMENTUM / users (VIOLET), APPS (GREEN). Small MONO
name-tags of the dead OSes drift inward and attach to the cause that killed
each one, with connecting lines lighting up as they settle. A recurring caption
cycles the through-line: "the best tech doesn't win" -> "the most users win" ->
"the most apps win". Continuous loop.

Dark palette only, TEXT labels only, continuous motion driven by a master
ValueTracker. No build-then-freeze.
  bg #0A0A0C  ink #E8E9EC  secondary #8C8E92
  green #35E08A  teal #2DD4BF  violet #B06BFF  amber #FFB020
  coral #FF5C47  gold #E8C24A  silver #C9CDD4
"""

import numpy as np

from manim import (
    Scene,
    Circle,
    Line,
    Text,
    VGroup,
    ValueTracker,
    ManimColor,
    config,
    FadeIn,
    Create,
    GrowFromCenter,
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


class Causes(Scene):
    def construct(self):
        # --- title -----------------------------------------------------------
        title = Text("WHAT KILLED THEM", font=HEAD, color=INK,
                     weight="SEMIBOLD").scale(0.62)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        # --- three cause nodes ----------------------------------------------
        # (key, title, subtitle, color, center)
        node_specs = [
            ("TIMING", "TIMING", "too early / too late", AMBER,
             np.array([-4.3, 0.2, 0])),
            ("MOMENTUM", "MOMENTUM", "lost the users", VIOLET,
             np.array([0.0, 0.2, 0])),
            ("APPS", "APPS", "no ecosystem", GREEN,
             np.array([4.3, 0.2, 0])),
        ]

        nodes = {}
        node_group = VGroup()
        for key, head, subtitle, color, center in node_specs:
            ring = Circle(radius=1.05, stroke_color=color, stroke_width=3.0,
                          fill_color="#131318", fill_opacity=0.9)
            ring.move_to(center)
            halo = Circle(radius=1.05, stroke_color=color, stroke_width=10,
                          stroke_opacity=0.0, fill_opacity=0.0).move_to(center)
            cap = Text(head, font=HEAD, color=color,
                       weight="BOLD").scale(0.42)
            cap.move_to(center + UP * 0.12)
            sub = Text(subtitle, font=MONO, color=SECOND).scale(0.2)
            sub.move_to(center + DOWN * 0.3)
            g = VGroup(halo, ring, cap, sub)
            node_group.add(g)
            nodes[key] = {"center": center, "color": color, "halo": halo,
                          "ring": ring}

        self.play(*[GrowFromCenter(g) for g in node_group],
                  lag_ratio=0.12, run_time=1.1)

        # --- dead OS name-tags with their assigned cause --------------------
        # (name, cause_key, start_angle_hint)
        assignments = [
            ("CP/M", "TIMING"),
            ("BeOS", "TIMING"),
            ("Palm OS", "TIMING"),
            ("Symbian", "TIMING"),
            ("OS/2", "MOMENTUM"),
            ("Classic Mac OS", "MOMENTUM"),
            ("MS-DOS", "MOMENTUM"),
            ("BlackBerry OS", "MOMENTUM"),
            ("webOS", "APPS"),
            ("Windows Phone", "APPS"),
        ]

        # How many tags attach to each cause (for slotting around the ring).
        per_cause = {"TIMING": 0, "MOMENTUM": 0, "APPS": 0}
        cause_counts = {"TIMING": 0, "MOMENTUM": 0, "APPS": 0}
        for _, c in assignments:
            cause_counts[c] += 1

        rng = np.random.default_rng(7)
        tags = []
        tag_group = VGroup()

        W_HALF = 7.3  # roughly half screen width for spawn positions

        for name, cause in assignments:
            color = nodes[cause]["color"]
            center = nodes[cause]["center"]

            # Slot index around this cause's ring.
            slot = per_cause[cause]
            per_cause[cause] += 1
            total = cause_counts[cause]

            # Distribute slots on an arc around the node, leaving room at top
            # for the big caption. Spread across a wide angular band.
            ang0 = -0.35 * np.pi
            ang1 = -1.65 * np.pi  # go the "long way" under the node
            frac = (slot + 0.5) / total
            ang = ang0 + (ang1 - ang0) * frac
            radius = 1.75
            settle = center + radius * np.array([np.cos(ang), np.sin(ang), 0])

            # Spawn far out at a random edge position.
            sx = float(rng.uniform(-W_HALF, W_HALF))
            sy = float(rng.uniform(-3.6, 3.6))
            # Push spawn to the outside so it drifts inward.
            spawn = np.array([sx, sy, 0])

            disp = name
            label = Text(disp, font=MONO, color=SILVER).scale(0.22)
            label.move_to(spawn)

            # Connecting line (drawn, lit when settled).
            link = Line(settle, center, stroke_color=color, stroke_width=1.6,
                        stroke_opacity=0.0)

            g = VGroup(link, label)
            tag_group.add(g)

            tags.append({
                "label": label,
                "link": link,
                "spawn": spawn,
                "settle": settle,
                "center": center,
                "color": color,
                "period": 7.0 + 1.5 * rng.random(),
                "offset": rng.uniform(0, 6.0),
            })

        self.add(tag_group)

        # --- through-line caption -------------------------------------------
        through = [
            "the best tech doesn't win",
            "the most users win",
            "the most apps win",
        ]

        # =====================================================================
        # CONTINUOUS MOTION PHASE
        # =====================================================================
        t = ValueTracker(0.0)

        LIT_INK = ManimColor(INK)
        GREY = ManimColor(SILVER)

        # --- node halos breathe in their cause colour -----------------------
        for key, info in nodes.items():
            halo = info["halo"]
            color = info["color"]
            phase = {"TIMING": 0.0, "MOMENTUM": 1.1, "APPS": 2.2}[key]

            def make_halo(halo, phase):
                def _upd(m):
                    tt = t.get_value()
                    s = 0.5 + 0.5 * np.sin(1.5 * tt + phase)
                    halo.set_stroke(opacity=0.1 + 0.3 * s)
                return _upd
            halo.add_updater(make_halo(halo, phase))

        # --- name-tags drift in, orbit, and settle on their cause -----------
        for tag in tags:
            label = tag["label"]
            link = tag["link"]
            spawn = tag["spawn"]
            settle = tag["settle"]
            center = tag["center"]
            color = ManimColor(tag["color"])
            period = tag["period"]
            offset = tag["offset"]

            def make_tag(label, link, spawn, settle, center, color,
                         period, offset):
                def _upd(m):
                    tt = (t.get_value() + offset) % period
                    frac = tt / period
                    # First 60%: drift inward from spawn to a settled slot.
                    # Last 40%: hold settled with a tiny orbital wobble, link lit.
                    if frac < 0.6:
                        a = frac / 0.6
                        eased = rate_functions.ease_in_out_quad(a)
                        pos = spawn * (1 - eased) + settle * eased
                        label.move_to(pos)
                        label.set_color(interpolate_color(GREY, color, eased))
                        label.set_opacity(0.35 + 0.65 * eased)
                        link.set_stroke(opacity=0.0)
                    else:
                        a = (frac - 0.6) / 0.4
                        # Gentle orbital wobble around the settled slot.
                        wob = 0.08 * np.sin(2.2 * t.get_value() + offset)
                        radial = settle - center
                        rn = radial / (np.linalg.norm(radial) + 1e-6)
                        pos = settle + rn * wob
                        label.move_to(pos)
                        label.set_color(color)
                        label.set_opacity(1.0)
                        # Link lights up then fades as the tag releases.
                        lit = np.sin(a * np.pi)  # 0 -> 1 -> 0
                        link.put_start_and_end_on(
                            label.get_center(), center)
                        link.set_stroke(opacity=0.5 * lit)
                return _upd

            label.add_updater(
                make_tag(label, link, spawn, settle, center, color,
                         period, offset))

        # --- big cycling through-line caption at the bottom ------------------
        caption = Text(through[0], font=HEAD, color=INK,
                       weight="MEDIUM").scale(0.5)
        caption.to_edge(DOWN, buff=0.55)
        caption._idx = -1

        cause_colors = [AMBER, VIOLET, GREEN]

        def caption_upd(m):
            idx = int(t.get_value() // 5.0) % len(through)
            if idx != m._idx:
                m._idx = idx
                new = Text(through[idx], font=HEAD,
                           color=ManimColor(cause_colors[idx]),
                           weight="MEDIUM").scale(0.5)
                new.to_edge(DOWN, buff=0.55)
                m.become(new)
        caption.add_updater(caption_upd)
        self.add(caption)

        self.play(t.animate.set_value(16.0), run_time=16.0,
                  rate_func=rate_functions.linear)

        for m in list(self.mobjects):
            m.clear_updaters()
        self.wait(0.3)
