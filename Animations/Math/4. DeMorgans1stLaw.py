from manim import *
import numpy as np

class DeMorgans1stLaw(Scene):
    def construct(self):
        # Colors
        color_A = "#3282B7"  # Blue
        color_B = "#676767"  # Green
        color_highlight = "#F4D03F"  # Yellow highlight
        background_color = "#1A1A1A"

        self.camera.background_color = background_color

        # Title
        main_title = Text("De Morgan's 1st Law", font_size=48, color=BLUE).set_color_by_gradient(RED, BLUE)
        underline = Line(
            main_title.get_left() + DOWN * 0.3,
            main_title.get_right() + DOWN * 0.3,
            color=color_highlight
        )
        title_group = VGroup(main_title, underline).to_edge(UP, buff=0.5)

        # Universal sets
        universal_left = RoundedRectangle(
            height=4, width=4, corner_radius=0.2,
            color=WHITE, stroke_width=2
        ).shift(LEFT * 3)
        
        universal_right = universal_left.copy().shift(RIGHT * 6)

        # Function to create labeled circles
        def create_circle_with_label(radius, color, position, label):
            circle = Circle(radius=radius, color=color, fill_opacity=0.2)
            text = MathTex(label, color=color, font_size=36)
            circle.move_to(position)
            text.move_to(circle.get_center())
            return VGroup(circle, text)

        # Left sets
        left_A = create_circle_with_label(1.2, color_A, LEFT*3.7, "A")
        left_B = create_circle_with_label(1.2, color_B, LEFT*2.2, "B")
        
        # Right sets
        right_A = create_circle_with_label(1.2, color_A, RIGHT*2.3, "A")
        right_B = create_circle_with_label(1.2, color_B, RIGHT*3.8, "B")

        # Labels
        left_title0 = MathTex("(A \\cup B)", font_size=40, color=color_highlight)

        left_title = MathTex("(A \\cup B)'", font_size=40, color=color_highlight)

        right_title0 = MathTex("A'", font_size=40, color=color_highlight)

        right_title1 = MathTex("B'", font_size=40, color=color_highlight)

        right_title = MathTex("A' \\cap B'", font_size=40, color=color_highlight)

        equals = MathTex("=", font_size=80, color=RED,).move_to(ORIGIN)

        left_title.next_to(universal_left, DOWN, buff=0.5)
        left_title0.next_to(universal_left, DOWN, buff=0.5)
        right_title.next_to(universal_right, DOWN, buff=0.5)
        right_title0.next_to(universal_right, DOWN, buff=0.5)
        right_title1.next_to(universal_right, DOWN, buff=0.5)   
        equals.move_to(DOWN * 2)

        # Show title
        self.play(Write(title_group), run_time=1.5)

        # Universal sets
        self.play(Create(universal_left), Create(universal_right), run_time=1.5)

        # Sets
        self.play(
            *[FadeIn(obj, scale=1.2) for obj in [left_A, left_B, right_A, right_B]],
            run_time=2
        )

        # --- Left side (Union then complement) ---
        union = Union(left_A[0], left_B[0], color=BLUE, fill_opacity=0.4)
        complement_union = Difference(
            universal_left, union,
            color=color_highlight, fill_opacity=0.8
        )

        # Show union first
        self.play(FadeIn(union), Write(left_title0))
        self.wait(3)  # pause on union

        # Then complement of union
        self.play(FadeIn(complement_union), FadeOut(union), FadeOut(left_title0))
        self.play(Write(left_title))
        self.wait(3)

        # --- Right side (Complements then intersection) ---
        A_complement = Difference(universal_right, right_A[0], color=RED, fill_opacity=0.8)
        B_complement = Difference(universal_right, right_B[0], color=BLUE, fill_opacity=0.8)

        # Show A'
        self.play(FadeIn(A_complement), Write(right_title0))
        self.wait(3)

        # Show B'
        self.play(FadeIn(B_complement),ReplacementTransform(right_title0, right_title1))
        self.wait(3)

        # Intersection of complements
        intersection_complements = Intersection(
            A_complement, B_complement,
            color=color_highlight, fill_opacity=1
        )
        self.play(FadeIn(intersection_complements), FadeOut(right_title1))
        self.play(Write(right_title), FadeOut(A_complement), FadeOut(B_complement))
        self.wait(2)

        # Equality
        self.play(Write(equals))
        self.wait(1)

        # Emphasis pulse
        self.play(
            *[
                UpdateFromAlphaFunc(
                    mob,
                    lambda m, a: m.set_fill(opacity=0.6 + np.sin(a * PI) * 0.3)
                ) for mob in [complement_union, intersection_complements]
            ],
            run_time=2
        )

        # Conclusion
        conclusion = Text(
            "De Morgan's 1st Law Verified!",
            font_size=36, color=color_highlight
        ).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(conclusion, shift=UP), run_time=1.5)
        self.wait(2)
