from manim import *

class RelativisticDEF(Scene):
    def construct(self):
        # Use compilable LaTeX fragments
        formula = MathTex(
            "f'", "=", "f", 
            r"\left(\frac{c \pm v_o}{c \pm v_s}\right)"
        )
        formula.set_color_by_gradient(RED,BLUE,YELLOW)
        self.play(Write(formula))
        self.wait(3)
        