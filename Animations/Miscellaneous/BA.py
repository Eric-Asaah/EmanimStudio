from manim import *
class BothApproaching(Scene):
    def construct(self):
        # Use compilable LaTeX fragments
        formula = MathTex(
            "f'", "=", "f", 
            r"\left(\frac{v + v_o}{v - v_s}\right)"
        )
        formula.scale(2)
        formula.set_color_by_gradient(RED,BLUE,YELLOW)
        self.play(Write(formula), run_time=5, fun_rate=smooth)
        self.wait(50)