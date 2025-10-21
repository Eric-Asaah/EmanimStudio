from manim import *
class ExSoln2(Scene):
    def construct(self):

        # Use compilable LaTeX fragments
        formula = MathTex(
            "f'", "=", "280Hz", 
            r"\left(\frac{343 + 25}{343- 40}\right)"
        )
        formula.scale(1.5)
        formula.set_color_by_gradient(RED,BLUE,YELLOW)
        self.add(formula)
        self.wait(5)
        #self.play(Write(formula), run_time=5, fun_rate=smooth)
        #self.wait(3)