from manim import *

class Box(Scene):
    def construct(self):
        # Create simpler number plane with less detail
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_opacity": 0.4
            }
        )
        self.add(plane)

        # Create the box with enhanced styling
        box = Rectangle(
            stroke_color=GREEN_C,
            stroke_opacity=0.7, 
            fill_color=RED_B,
            fill_opacity=0.5, 
            width=1,
            height=1
        ).move_to(ORIGIN)

        # Create a simpler triangle
        triangle = Triangle(
            stroke_color=BLUE_C,
            stroke_opacity=0.8,
            fill_color=YELLOW_B,
            fill_opacity=0.6
        ).scale(1.2)

        # Simplified animations
        self.play(Create(box))
        self.wait(0.5)
        
        # Box animations with shorter duration
        self.play(box.animate.shift(RIGHT*2), run_time=1)
        self.play(box.animate.shift(UP*2), run_time=1)
        
        # Transform box to triangle
        self.play(Transform(box.copy(), triangle), run_time=1.5)
        
        self.wait(1)
