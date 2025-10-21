from manim import *

class TextColour(Scene):
    def construct(self):
        A = Text("1. Answer more than 100 mcqs in 60 minutes", font_size=45)
        B=Text("2. Say wow, I didn't think it was that easy", font_size=45)
        C=Text("OBJECTIVES", font_size=70)
        C.set_color_by_gradient(BLUE, GREEN, YELLOW)
        C.to_edge(UP)
        D=Underline(C, color=RED)

        A.set_color_by_gradient(BLUE, GREEN, YELLOW)
        B.set_color_by_gradient(BLUE, GREEN, YELLOW)
        self.play(Write(C), Create(D) ,run_time=3)
        self.wait(3)
        self.play(Write(A), run_time=5 if A.text == "1. Answer more than 100 mcqs in" else 8)  
        self.wait(5)  
        self.play(A.animate.shift(UP * 2), run_time=1)
        self.play(Write(B), run_time=6)
        self.play(B.animate.shift(UP * 1), run_time=2)
        self.wait(10)

    
