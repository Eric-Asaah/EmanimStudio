# TITLE: Euler's Identity: e^(iπ) + 1 = 0
# DESCRIPTION: Step-by-step derivation of Euler's famous identity showing the mathematical beauty connecting five fundamental constants.
from manim import *


class EulersIdentityReveal(Scene):
    def construct(self):
        # 1. Intro Text
        title = Text("Let's explore Euler's Identity", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # 2. Euler's Formula
        formula = MathTex("e^{ix} = \\cos(x) + i\\sin(x)").scale(1.4)
        self.play(Write(formula))
        self.wait(2)

        # 3. Plug in x = π
        substituted = MathTex(
            "e^{i\\pi} = \\cos(\\pi) + i\\sin(\\pi)").scale(1.4)
        self.play(Transform(formula, substituted))
        self.wait(2)

        # 4. Evaluate cos(π) and sin(π)
        simplified = MathTex("e^{i\\pi} = -1 + i \\cdot 0").scale(1.4)
        self.play(Transform(formula, simplified))
        self.wait(1.5)

        # 5. Final Step: Euler's Identity
        final_identity = MathTex("e^{i\\pi} + 1 = 0").scale(1.8)
        final_identity.set_color_by_tex("e^{i\\pi}", BLUE)
        final_identity.set_color_by_tex("1", YELLOW)
        final_identity.set_color_by_tex("0", GREEN)

        # Dramatic reveal with scale
        self.play(Transform(formula, final_identity), run_time=1.5)
        self.wait(2)

        # Optional Mic-Drop Fade
        self.play(FadeOut(formula, scale=1.5), run_time=0.5)
        self.wait()
