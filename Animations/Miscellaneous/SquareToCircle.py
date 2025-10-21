from manim import *

class SquareToCircle(Scene):
    def construct(self):
        square = Square(side_length=2, color=BLUE)
        circle = Circle(radius=1, color=RED)
        T=Triangle(color=YELLOW, fill_opacity=0.5)    
        self.play(Create(square))
        self.wait(1)
        self.play(square.animate.shift(RIGHT*3))
        self.play(ReplacementTransform(square.copy(), circle))
        self.wait(1)
        self.play(circle.animate.shift(LEFT*3))
        self.play(circle.animate.scale(0.5))
        self.play(DrawBorderThenFill(T))
        self.play(FadeOut(circle))
        self.wait(1)
        
from manim.utils.unit import Percent, Pixels
class Concentric(Scene):
    def construct(self):
        for i in range(5, 51, 5):
            circle = Circle(radius=Percent(i), color=BLUE, fill_opacity=0.1)
            self.play(Create(circle), run_time=0.5)