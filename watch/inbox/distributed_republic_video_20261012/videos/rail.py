"""
THE DISTRIBUTED REPUBLIC - scene 1: THE RAIL (lane A, 2026-10-12)

The first buildable scene from the storyboard: the rail with five model
pulses, the noise-control discard, and the 85/10/5 payment particle split -
driven by the perimeter's REAL settle numbers (0.899132488 TON landed per
device wallet, SettlementMaster v2 testnet).

Run: .venv/Scripts/python.exe -m manim -qm videos.rail RailScene
Output: media/videos/rail/720p30/RailScene.mp4
"""
from manim import *


class RailScene(Scene):
    def construct(self):
        # ---- the rail -----------------------------------------------------
        title = Text("The rail does not care who you are.", font_size=30)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.2)

        rail = Line(LEFT * 5.5, RIGHT * 5.5, color=GREY_B, stroke_width=6)
        self.play(Create(rail), run_time=1.0)

        # ---- five model pulses answer the same task -----------------------
        task = Text("one task", font_size=24, color=WHITE)
        task.next_to(rail.get_start(), RIGHT * 0.5, DOWN)
        self.play(FadeIn(task), run_time=0.5)

        model_colors = [BLUE, TEAL, GREEN, ORANGE, PURPLE]
        pulses = VGroup()
        for i, color in enumerate(model_colors):
            p = Dot(color=color, radius=0.12)
            p.move_to(rail.get_start() + RIGHT * (1.0 + i * 0.15) + UP * 0.6)
            pulses.add(p)
        labels = VGroup()
        for i, p in enumerate(pulses):
            lab = Text(f"model {i+1}", font_size=16, color=p.color)
            lab.next_to(p, UP, buff=0.15)
            labels.add(lab)
        self.play(FadeIn(pulses), FadeIn(labels), run_time=0.8)

        # pulses travel the rail
        self.play(
            *[p.animate.move_to(rail.get_end() + UP * 0.6) for p in pulses],
            run_time=1.6, rate_func=linear,
        )

        # ---- the noise control: nonsense question gets discarded ----------
        noise_q = Text("nonsense question (control)", font_size=20, color=GREY)
        noise_q.next_to(rail, DOWN, buff=0.5)
        noise_mark = Text("all agree -> NOISE, discarded", font_size=20, color=RED)
        noise_mark.next_to(noise_q, DOWN, buff=0.2)
        self.play(FadeIn(noise_q), run_time=0.6)
        self.play(FadeIn(noise_mark), run_time=0.8)
        self.play(FadeOut(noise_q), FadeOut(noise_mark), run_time=0.6)

        # ---- verified work reaches the payment station --------------------
        station = RoundedRectangle(corner_radius=0.2, width=2.2, height=1.0)
        station.set_stroke(WHITE, 2).set_fill(DARK_GREY, 0.8)
        station.move_to(rail.get_end() + DOWN * 1.4)
        station_label = Text("SettlementMaster", font_size=20)
        station_label.move_to(station)
        self.play(Create(station), Write(station_label), run_time=1.0)

        # ---- the payment particle divides 85/10/5 -------------------------
        particle = Dot(color=YELLOW, radius=0.15)
        particle.move_to(station)
        pay_label = Text("0.899132488 TON", font_size=20, color=YELLOW)
        pay_label.next_to(station, DOWN, buff=0.3)
        self.play(FadeIn(particle), Write(pay_label), run_time=0.8)

        shares = [
            ("worker  85%", RIGHT * 2.4, YELLOW),
            ("treasury 10%", DOWN * 1.6, TEAL),
            ("protocol  5%", LEFT * 2.4, ORANGE),
        ]
        parts = VGroup()
        share_labels = VGroup()
        for text, direction, color in shares:
            d = Dot(color=color, radius=0.1)
            d.move_to(station.get_center() + direction)
            t = Text(text, font_size=16, color=color)
            t.next_to(d, DOWN, buff=0.1)
            parts.add(d)
            share_labels.add(t)
        self.play(
            particle.animate.scale(0.4).move_to(station.get_center()),
            run_time=0.4,
        )
        self.play(
            LaggedStart(
                *[GrowFromCenter(d) for d in parts], lag_ratio=0.25
            ),
            FadeIn(share_labels),
            FadeOut(particle),
            run_time=1.4,
        )

        # ---- the closing line ---------------------------------------------
        closing = Text(
            "The rail cares whether the numbers reconcile.",
            font_size=26,
        )
        closing.to_edge(DOWN)
        self.play(Write(closing), run_time=1.2)
        self.wait(2)
