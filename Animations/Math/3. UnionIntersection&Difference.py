# TITLE: Set Operations: Union, Intersection & Difference
# DESCRIPTION: Visual demonstration of fundamental set operations including union, intersection, and both difference operations between two sets.
from manim import *


class UnionIntersectionDifference(Scene):
    def construct(self):
        # Colors
        color_A = BLUE
        color_B = GREEN
        color_intersection = YELLOW

        # Circles for sets A and B
        circle_A = Circle(radius=1.5, color=color_A,
                          fill_opacity=0.3).shift(LEFT)
        circle_B = Circle(radius=1.5, color=color_B,
                          fill_opacity=0.3).shift(RIGHT)

        # Labels for sets
        label_A = Text("A", color=color_A).next_to(circle_A, LEFT)
        label_B = Text("B", color=color_B).next_to(circle_B, RIGHT)

        # Animate creation
        self.play(Create(circle_A), Write(label_A))
        self.play(Create(circle_B), Write(label_B))
        self.wait(1)

        # --- UNION A ∪ B ---
        union_region = Union(circle_A, circle_B,
                             color=PURPLE, fill_opacity=0.7)
        union_label = MathTex("A \\cup B", font_size=42,
                              color=PURPLE).to_edge(DOWN, buff=0.5)
        union_title = Text("Union", font_size=44,
                           color=PURPLE).to_edge(UP, buff=0.5)

        self.play(Write(union_title))
        self.play(FadeIn(union_region, scale=1.1))
        self.play(Write(union_label))
        self.play(Indicate(union_region, color=PURPLE, scale_factor=1.1))
        self.wait(3)
        self.play(FadeOut(union_region), FadeOut(
            union_label), FadeOut(union_title))

        # --- INTERSECTION A ∩ B ---
        intersection_region = Intersection(
            circle_A, circle_B, color=color_intersection, fill_opacity=0.85)
        intersection_label = MathTex(
            "A \\cap B", font_size=42, color=color_intersection).to_edge(DOWN, buff=0.5)
        intersection_title = Text(
            "Intersection", font_size=44, color=color_intersection).to_edge(UP, buff=0.5)

        self.play(Write(intersection_title))
        self.play(FadeIn(intersection_region, scale=1.1))
        self.play(Write(intersection_label))
        self.play(Indicate(intersection_region,
                  color=color_intersection, scale_factor=1.2))
        self.wait(3)
        self.play(FadeOut(intersection_region), FadeOut(
            intersection_label), FadeOut(intersection_title))

        # --- DIFFERENCE A - B ---
        difference_region = Difference(
            circle_A, circle_B, color=color_A, fill_opacity=0.8)
        difference_label = MathTex(
            "A - B", font_size=42, color=color_A).to_edge(DOWN, buff=0.5)
        difference_title = Text(
            "Difference (A - B)", font_size=44, color=color_A).to_edge(UP, buff=0.5)

        self.play(Write(difference_title))
        self.play(FadeIn(difference_region, scale=1.1))
        self.play(Write(difference_label))
        self.play(Indicate(difference_region, color=color_A, scale_factor=1.2))
        self.wait(3)
        self.play(FadeOut(difference_region), FadeOut(
            difference_label), FadeOut(difference_title))

        # --- DIFFERENCE B - A ---
        difference_region2 = Difference(
            circle_B, circle_A, color=color_B, fill_opacity=0.8)
        difference_label2 = MathTex(
            "B - A", font_size=42, color=color_B).to_edge(DOWN, buff=0.5)
        difference_title2 = Text(
            "Difference (B - A)", font_size=44, color=color_B).to_edge(UP, buff=0.5)

        self.play(Write(difference_title2))
        self.play(FadeIn(difference_region2, scale=1.1))
        self.play(Write(difference_label2))
        self.play(Indicate(difference_region2, color=color_B, scale_factor=1.2))
        self.wait(3)
        self.play(FadeOut(difference_region2), FadeOut(
            difference_label2), FadeOut(difference_title2))

        # Hold final frame
        self.wait(3)
