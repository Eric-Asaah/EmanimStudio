# TITLE: Euler's Identity: Derivation and Explanation
# DESCRIPTION: A single, coherent animation that first derives 
# Euler's Identity from Euler's Formula, and then explains 
# the five fundamental constants it contains.

from manim import *

class EulersIdentity(Scene):
    """
    A Manim scene that derives Euler's Identity from Euler's Formula
    and then explains the significance of its five components.
    """
    def construct(self):
        
        # --- PART 1: The Derivation ---

        # 1. Title
        title = Text("Deriving Euler's Identity", font_size=48)
        self.play(Write(title))
        self.wait(1.5)

        # 2. Start with Euler's Formula
        formula = MathTex(
            "e^{ix} = \\cos(x) + i\\sin(x)", 
            font_size=72
        )
        self.play(
            FadeOut(title, shift=UP),
            Write(formula)
        )
        self.wait(2)

        # 3. Substitute x = pi
        step_1_text = Text("Let's substitute x = \pi", font_size=36).to_edge(UP)
        substituted = MathTex(
            "e^{i\\pi} = \\cos(\\pi) + i\\sin(\\pi)", 
            font_size=72
        )
        self.play(Write(step_1_text))
        self.play(TransformMatchingTex(formula, substituted))
        self.wait(2)

        # 4. Evaluate the trigonometric functions
        step_2_text = Text("We know cos(\pi) = -1 and sin(\pi) = 0", font_size=36).to_edge(UP)
        evaluated = MathTex(
            "e^{i\\pi} = -1 + i(0)", 
            font_size=72
        )
        self.play(ReplacementTransform(step_1_text, step_2_text))
        self.play(TransformMatchingTex(substituted, evaluated))
        self.wait(2)

        # 5. Simplify the expression
        simplified = MathTex(
            "e^{i\\pi} = -1", 
            font_size=72
        )
        self.play(TransformMatchingTex(evaluated, simplified))
        self.wait(2)

        # 6. Rearrange to the final Identity
        step_3_text = Text("Rearranging gives...", font_size=36).to_edge(UP)
        final_identity = MathTex(
            "e^{i\\pi}", "+", "1", "=", "0", 
            font_size=96 # Make the final identity larger
        )
        self.play(ReplacementTransform(step_2_text, step_3_text))
        self.play(TransformMatchingTex(simplified, final_identity))
        self.wait(1)


        # --- PART 2: The Explanation ---

        # 1. Change title
        new_title = Text("Euler's Identity", font_size=48, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(step_3_text, new_title))
        self.wait(2)

        # 2. Narration and highlighting for each component
        # We can now refer to parts of `final_identity` by index
        
        # e, i, pi
        narration1 = Paragraph(
            "It connects 'e', Euler's number...",
            font_size=32, alignment="center"
        ).to_edge(DOWN)
        self.play(Write(narration1))
        # Use get_part_by_tex to be precise
        self.play(Indicate(final_identity.get_part_by_tex("e"), color=BLUE))
        self.wait(1.5)
        
        narration2 = Paragraph(
            "...the imaginary unit 'i'...",
            font_size=32, alignment="center"
        ).to_edge(DOWN)
        self.play(ReplacementTransform(narration1, narration2))
        self.play(Indicate(final_identity.get_part_by_tex("i"), color=GREEN))
        self.wait(1.5)

        narration3 = Paragraph(
            "...and 'π', the circle constant.",
            font_size=32, alignment="center"
        ).to_edge(DOWN)
        self.play(ReplacementTransform(narration2, narration3))
        self.play(Indicate(final_identity.get_part_by_tex("\\pi"), color=RED))
        self.wait(2)

        # 1
        narration4 = Paragraph(
            "It links them with '1', the multiplicative identity...",
            font_size=32, alignment="center"
        ).to_edge(DOWN)
        self.play(ReplacementTransform(narration3, narration4))
        self.play(
            Create(
                SurroundingRectangle(final_identity[2], color=PURPLE, buff=0.15)
            )
        )
        self.wait(2)

        # 0
        narration5 = Paragraph(
            "...and '0', the additive identity.",
            font_size=32, alignment="center"
        ).to_edge(DOWN)
        self.play(ReplacementTransform(narration4, narration5))
        self.play(
            Create(
                SurroundingRectangle(final_identity[4], color=ORANGE, buff=0.15)
            )
        )
        self.wait(2)

        # 3. Final summary
        self.play(FadeOut(VGroup(final_identity[1], final_identity[3]))) # Fade out + and =
        
        final_narration = Paragraph(
            "Five of math's most important numbers,",
            "united in one simple, elegant equation.",
            font_size=36, alignment="center"
        ).to_edge(DOWN)
        
        self.play(
            ReplacementTransform(narration5, final_narration),
            # Group the numbers and animate them
            VGroup(final_identity[0], final_identity[2], final_identity[4]).animate.arrange(RIGHT, buff=0.5)
        )
        self.wait(4)

        # Fade out everything
        self.play(
            FadeOut(new_title),
            FadeOut(final_narration),
            FadeOut(VGroup(final_identity[0], final_identity[2], final_identity[4]))
        )
        self.wait(1)
