# Title: Sierpinski Triangle Zoom Animation
# Description: A recursive zoom into the Sierpinski triangle using scaled copies and camera framing to highlight fractal depth.
from manim import *


class SierpinskiZoom(Scene):
    def construct(self):
        bblue = "#0072B2"

        # Define triangle vertices
        points = [100 * np.array([
            np.cos(2 * PI * i / 3 - PI / 6),
            np.sin(2 * PI * i / 3 - PI / 6),
            0
        ]) for i in range(3)]

        base_triangle = Polygon(*points, color=bblue,
                                fill_opacity=1, stroke_width=1)
        base_triangle.move_to(ORIGIN)

        self.camera.frame.set_height(base_triangle.height)
        self.camera.frame.move_to(base_triangle.get_center())

        num_levels = 9
        levels = []

        for j in range(num_levels):
            group = VGroup()
            for i in range(3):
                if j == 0:
                    temp = base_triangle.copy().scale(0.5)
                else:
                    temp = levels[j - 1].copy().scale(0.5)
                group.add(temp)

            group[:2].arrange(RIGHT, buff=0.01)
            group[:2].next_to(group[2], DOWN, buff=0.01)

            if j == 0:
                group.move_to(base_triangle.get_center())
            else:
                group.move_to(levels[j - 1].get_center())

            levels.append(group)

        self.add(levels[-1])

        self.play(
            self.camera.frame.animate.set_height(
                levels[2][2].height).move_to(levels[2][2]),
            run_time=10,
            rate_func=linear
        )
