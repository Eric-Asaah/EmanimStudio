from manim import *

class VennDiagramAB(Scene):
    def construct(self):
        # Define colors
        color_A = BLUE
        color_B = GREEN

        # Create circles for sets A and B
        circle_A = Circle(radius=1.5, color=color_A, fill_opacity=0.5).shift(LEFT * 1.2)
        circle_B = Circle(radius=1.5, color=color_B, fill_opacity=0.5).shift(RIGHT * 1.2)

        # Labels for the sets
        label_A = Text("A", color=color_A).next_to(circle_A, LEFT)
        label_B = Text("B", color=color_B).next_to(circle_B, RIGHT)

        # Animate the creation of the sets
        self.play(Create(circle_A), Write(label_A))
        self.play(Create(circle_B), Write(label_B))

        # Highlight intersection
        intersection_AB = Intersection(circle_A, circle_B, color=YELLOW, fill_opacity=0.5)
        self.play(FadeIn(intersection_AB))

        # Label the regions
        label_A_only = Text("1", color=BLACK).move_to(circle_A.get_center() + LEFT * 0.5)
        label_B_only = Text("2", color=BLACK).move_to(circle_B.get_center() + RIGHT * 0.5)
        label_AB = Text("3", color=BLACK).move_to(intersection_AB.get_center())

        self.play(Write(label_A_only), Write(label_B_only), Write(label_AB))

        # Create and label the universal set
        universal_set = Rectangle(width=8, height=6, color=WHITE).move_to(ORIGIN)
        label_U = Text("U", color=WHITE).next_to(universal_set, UP + RIGHT)

        self.play(Create(universal_set), Write(label_U))

        # Hold the final frame
        self.wait(3)
