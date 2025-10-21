from manim import *

class VennDiagramABC(Scene):
    def construct(self):
        # Define colors
        color_A = BLUE
        color_B = GREEN
        color_C = RED

        # Create circles for sets A, B, and C
        circle_A = Circle(radius=1.5, color=color_A, fill_opacity=0.5).shift(LEFT)
        circle_B = Circle(radius=1.5, color=color_B, fill_opacity=0.5).shift(RIGHT)
        circle_C = Circle(radius=1.5, color=color_C, fill_opacity=0.5).shift(DOWN * 1.5)
        Sets=VGroup(circle_A, circle_B, circle_C)
        Sets.shift(UP*0.90)

        # Labels for the sets
        label_A = Text("A", color=color_A).next_to(circle_A, LEFT)
        label_B = Text("B", color=color_B).next_to(circle_B, RIGHT)
        label_C = Text("C", color=color_C).next_to(circle_C, DOWN)

        # Animate the creation of the sets
        self.play(Create(circle_A), Write(label_A))
        self.play(Create(circle_B), Write(label_B))
        self.play(Create(circle_C), Write(label_C))

        # Highlight intersections
        intersection_AB = Intersection(circle_A, circle_B, color=YELLOW, fill_opacity=0.5)
        intersection_BC = Intersection(circle_B, circle_C, color=YELLOW, fill_opacity=0.5)
        intersection_CA = Intersection(circle_C, circle_A, color=YELLOW, fill_opacity=0.5)
        intersection_ABC = Intersection(intersection_AB, circle_C, color=ORANGE, fill_opacity=0.5)

        # Animate intersections
        self.play(FadeIn(intersection_AB))
        self.play(FadeIn(intersection_BC))
        self.play(FadeIn(intersection_CA))
        self.play(FadeIn(intersection_ABC))

        # Label all regions
        label_A_only = Text("1", color=BLACK).move_to(circle_A.get_center() + LEFT * 0.5)

        label_B_only = Text("2", color=BLACK).move_to(circle_B.get_center() + RIGHT * 0.5)

        label_C_only = Text("3", color=BLACK).move_to(circle_C.get_center() + DOWN * 0.5)
        label_AB = Text("4", color=BLACK).move_to(intersection_AB.get_center()+ UP * 0.5)
        label_BC = Text("5", color=BLACK).move_to(intersection_BC.get_center() + DOWN * 0.2+ RIGHT * 0.2)

        label_CA = Text("6", color=BLACK).move_to(intersection_CA.get_center() + DOWN * 0.2 + LEFT * 0.2)

        label_ABC = Text("7", color=BLACK).move_to(intersection_ABC.get_center()+ UP * 0.1)

        self.play(
            Write(label_A_only), 
            Write(label_B_only), 
            Write(label_C_only)
        )
        self.play(
            Write(label_AB), 
            Write(label_BC), 
            Write(label_CA), 
            Write(label_ABC)
        )

        # Create and label the universal set
        universal_set = Rectangle(width=8, height=6, color=WHITE).move_to(ORIGIN)
        label_U = Text("U", color=WHITE).next_to(universal_set, UP+RIGHT)

        self.play(Create(universal_set), Write(label_U))

        # Hold the final frame
        self.wait(3)
