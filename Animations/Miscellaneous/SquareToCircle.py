# TITLE: Shape Transformations: Square to Circle
# DESCRIPTION: Basic shape animation demonstrating transformations between square, circle, and triangle with scaling and movement.
from manim import *


class SquareToCircle(Scene):
    def construct(self):
        square = Square(side_length=2, color=BLUE)
        circle = Circle(radius=1, color=RED)
        T = Triangle(color=YELLOW, fill_opacity=0.5)
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
