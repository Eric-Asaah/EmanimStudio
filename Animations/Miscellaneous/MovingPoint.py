# Title: Point Motion on Circle and Line
# Description: Demonstrates a dot moving along a circle, transforming position, and rotating around a fixed point, with a static line for reference. From Manim Community Examples.
from manim import *


class PointMovingOnShapes(Scene):
    def construct(self):
        # Create a blue circle and a dot
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)

        # Add initial dot and a reference line
        self.add(dot)
        line = Line(start=[3, 0, 0], end=[5, 0, 0])
        self.add(line)

        # Animate the circle and dot transformations
        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()
