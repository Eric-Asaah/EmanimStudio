from manim import *

class TextColour(Scene):
    def construct(self):
        A = Text("Hello...", font_size=200)
        B=Tex("And...Welcome", font_size=200)
        A.set_color_by_gradient(BLUE, GREEN, YELLOW)
        B.set_color_by_gradient(RED, ORANGE, PURPLE)
        self.play(Write(A), run_time=0.3 if A.text == "Hello" else 2)  
        self.wait(1)   
        self.play(ReplacementTransform(A, B), run_time=3)
        self.wait(2)
    
       # self.play(Write(B), run_time=3)
