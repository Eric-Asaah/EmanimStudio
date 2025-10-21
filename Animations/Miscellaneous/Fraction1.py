from manim import *
config.frame_width = 16
config.frame_height = 9

class Numerator(Scene):
    def construct(self):
        TITLE_FONT_SIZE = 80
        SUBTITLE_FONT_SIZE = 48
        BODY_FONT_SIZE = 100
        SMALL_FONT_SIZE = 24
        FOOTNOTE_FONT_SIZE = 18

        # Initial fraction and value
        numerator = 1
        denominator = 2
        value = numerator / denominator

        fraction_tex = MathTex(f"\\frac{{{numerator}}}{{{denominator}}} = {value:.2f}", font_size=BODY_FONT_SIZE)
        fraction_tex.set_color_by_gradient(RED, BLUE)
        self.play(Write(fraction_tex))
        self.wait(9)

        # Gradually increase numerator
        for num in range(2, 10):
            new_value = num / denominator
            new_tex = MathTex(f"\\frac{{{num}}}{{{denominator}}} = {new_value:.2f}", font_size=BODY_FONT_SIZE)
            self.play(ReplacementTransform(fraction_tex, new_tex), run_time=0.2 if num < 7 else 0.5)
            fraction_tex = new_tex
            self.wait(1.5)

                # Gradually decrease numerator
        for num in range(10, 0, -1):
            new_value = num / denominator
            new_tex = MathTex(f"\\frac{{{num}}}{{{denominator}}} = {new_value:.2f}", font_size=BODY_FONT_SIZE)
            self.play(ReplacementTransform(fraction_tex, new_tex), run_time=0.2 if num > 5 else 0.4)
            fraction_tex = new_tex
        self.wait(1)
        self.play(FadeOut(fraction_tex))