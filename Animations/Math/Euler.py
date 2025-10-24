from manim import *

class EulerIdentity(Scene):
    def construct(self):
        # Title
        title = Text("Euler's Identity", font_size=48, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # The full equation with explicit parts
        equation = MathTex("e^{i\\pi}", "+", "1", "=", "0", font_size=72)
        equation.move_to(ORIGIN)
        self.play(Write(equation))
        self.wait(2)

        # Narration 1: Exponential part
        narration1 = Paragraph(
            "Here we see the exponential function e raised",
            "to the power of i times pi.",
            font_size=28, alignment="center", line_spacing=0.6
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(narration1))
        self.wait(3)
        self.play(FadeOut(narration1))

        # Highlight e^(i pi)
        highlight1 = SurroundingRectangle(equation[0], color=BLUE, buff=0.2)
        self.play(Create(highlight1))
        self.wait(2)
        self.play(FadeOut(highlight1))

        # Narration 2: Imaginary unit
        narration2 = Paragraph(
            "The imaginary unit i represents the square root of -1.",
            font_size=28, alignment="center", line_spacing=0.6
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(narration2))
        self.wait(3)
        self.play(FadeOut(narration2))

        # Highlight i (inside the exponential term)
        i_symbol = MathTex("i", font_size=72).move_to(equation[0].get_center() + RIGHT*0.3)
        self.play(Indicate(equation[0], color=GREEN))
        self.wait(2)

        # Narration 3: Pi constant
        narration3 = Paragraph(
            "Pi is the fundamental circle constant, about 3.14159.",
            font_size=28, alignment="center", line_spacing=0.6
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(narration3))
        self.wait(3)
        self.play(FadeOut(narration3))

        # Highlight pi
        self.play(Indicate(equation[0], color=RED))
        self.wait(2)

        # Narration 4: Plus one
        narration4 = Paragraph(
            "Then we add the number 1.",
            font_size=28, alignment="center", line_spacing=0.6
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(narration4))
        self.wait(2)
        self.play(FadeOut(narration4))

        # Highlight +1
        highlight4 = SurroundingRectangle(equation[2], color=PURPLE, buff=0.2)
        self.play(Create(highlight4))
        self.wait(2)
        self.play(FadeOut(highlight4))

        # Narration 5: Equals zero
        narration5 = Paragraph(
            "And astonishingly, the result equals zero.",
            font_size=28, alignment="center", line_spacing=0.6
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(narration5))
        self.wait(3)
        self.play(FadeOut(narration5))

        # Highlight =0
        highlight5 = SurroundingRectangle(VGroup(equation[3], equation[4]), color=ORANGE, buff=0.2)
        self.play(Create(highlight5))
        self.wait(2)
        self.play(FadeOut(highlight5))

        # Final Narration
        final_text = Paragraph(
            "Euler's Identity unites five of the most fundamental numbers:",
            "e, i, π, 1, and 0 — in a single elegant equation.",
            font_size=28, alignment="center", line_spacing=0.6
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(final_text))
        self.wait(4)

        # Final emphasis
        self.play(Indicate(equation, color=YELLOW))
        self.wait(3)
