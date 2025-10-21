from manim import *
config.frame_width = 16
config.frame_height = 9

class Denominator(Scene):
    def construct(self):
        BODY_FONT_SIZE = 100
        fraction = MathTex(r"\frac{1}{2} = 0.5", font_size=BODY_FONT_SIZE).set_color_by_gradient(RED, BLUE)
        self.play(Write(fraction))
        self.wait(10)
        # Gradually increase denominator
        for d in range(3, 50, 5):
            new_fraction = MathTex(rf"\frac{{1}}{{{d}}} = {1/d:.3f}", font_size=BODY_FONT_SIZE).set_color_by_gradient(RED, BLUE)
            self.play(ReplacementTransform(fraction, new_fraction), run_time=0.2 if d < 40 else 0.5)
            fraction = new_fraction
            self.wait(1.5)

        # Gradually decrease denominator
        for d in range(50, 2, -5):
            new_fraction = MathTex(rf"\frac{{1}}{{{d}}} = {1/d:.3f}", font_size=BODY_FONT_SIZE).set_color_by_gradient(RED, BLUE)
            self.play(ReplacementTransform(fraction, new_fraction), run_time=0.2 if d > 10 else 0.4)
            fraction = new_fraction
            self.wait(2)