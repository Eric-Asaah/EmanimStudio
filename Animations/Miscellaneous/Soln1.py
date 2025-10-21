from manim import *
class ExSoln2(Scene):
    def construct(self):

        # Use compilable LaTeX fragments
        formula1 = MathTex(
            "f'", "=", "280Hz", 
            r"\left(\frac{343 + 25}{343- 40}\right)"
        )
        formula1.scale(1.5)
        formula1.set_color_by_gradient(RED,BLUE,YELLOW)
        formula2= MathTex(
            "f'", "=", "280Hz", 
            r"\left(\frac{368}{303}\right)"
        )
        formula2.scale(1.5)
        formula2.set_color_by_gradient(RED,BLUE,YELLOW)
        formula3= MathTex(
            "f'", "=", "340.066Hz"
        )
        formula3.scale(2)
        formula3.set_color_by_gradient(RED,BLUE,YELLOW) 
        self.play(Write(formula1), run_time=3, fun_rate=smooth)
        self.wait(3)  
        self.play(ReplacementTransform(formula1,formula2), run_time=5, fun_rate=smooth)
        self.wait(2)
        self.play(ReplacementTransform(formula2,formula3), run_time=3, fun_rate=smooth)
        self.wait(5)

        