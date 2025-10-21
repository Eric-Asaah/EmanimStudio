from manim import *

class CollatzConjecture(Scene):
    def construct(self):
        # Utility function for blocks
        def process_block(current, operation_tex, result_tex):
            """
            Takes current MathTex, operation string, and result string.
            Places them nicely and returns the new result at 2*UP.
            """
            # Operation below current
            operation = MathTex(operation_tex).next_to(current, DOWN, buff=1).set_color_by_gradient(RED, YELLOW).scale(2)
            self.play(Write(operation))
            self.wait(1)

            # Result below operation
            result = MathTex(result_tex, color=BLUE).next_to(operation, DOWN, buff=1).scale(2)
            self.play(TransformFromCopy(operation, result))
            self.wait(1)

            # Fade out old stuff, shift result back to top
            self.play(FadeOut(current, operation))
            self.play(result.animate.move_to(2*UP))
            return result

        # --- Opening text ---
        opening = Tex("Pick any number you want").scale(1.2).set_color_by_gradient(RED, BLUE, GREEN)
        even = Tex("Even: Divide it by 2").scale(1.2).set_color_by_gradient(RED, BLUE, GREEN)
        odd = Tex("Odd: Multiply by 3 and add 1").scale(1.2).set_color_by_gradient(RED, BLUE, GREEN)
        check = Tex("Repeat this for the results").scale(1.2).set_color_by_gradient(RED, BLUE, GREEN)

        self.play(Write(opening)); self.wait(2)
        self.play(ReplacementTransform(opening, even)); self.wait(2)
        self.play(ReplacementTransform(even, odd)); self.wait(2)
        self.play(ReplacementTransform(odd, check)); self.wait(2)
        self.play(FadeOut(check))


        three = MathTex("3", color=BLUE).scale(2.5).move_to(2*UP)
        self.play(Write(three))
        self.wait(1)

        # Step 1: Odd → 3n + 1 
        mult0 = MathTex("3", "(", "3", ")", "+", "1", color=RED).next_to(three, DOWN, buff=1).scale(2.2)
        self.play(Write(mult0[0]), Write(mult0[1]), Write(mult0[3]), Write(mult0[4]), Write(mult0[5])) 
        self.play(TransformFromCopy(three, mult0[2]))
        result0=MathTex("10", color=BLUE).scale(2).next_to(mult0, DOWN, buff=1)
        self.play(TransformFromCopy(mult0,result0))
        self.wait(1.5)
        self.play(FadeOut(three, mult0))
        self.play(result0.animate.move_to(2*UP))
        result_1 = process_block(result0, r"\frac{10}{2}", "5")


        # --- Collatz sequence starting from 5 ---
        five = MathTex("5", color=BLUE).scale(2.5).move_to(2*UP)
        self.play(ReplacementTransform(result_1,five)); self.wait(1)

        # Step 1: Odd → 3n + 1 
        mult1 = MathTex("3", "(", "5", ")", "+", "1", color=RED).next_to(five, DOWN, buff=1).scale(2.2)
        self.play(Write(mult1[0]), Write(mult1[1]), Write(mult1[3]), Write(mult1[4]), Write(mult1[5])) 
        self.play(TransformFromCopy(five, mult1[2]))
        result1=MathTex("16", color=BLUE).scale(2).next_to(mult1, DOWN, buff=1)
        self.play(TransformFromCopy(mult1,result1))
        self.wait(1.5)
        self.play(FadeOut(five, mult1))
        self.play(result1.animate.move_to(2*UP))

        # Step 2: 16 → 8
        result2 = process_block(result1, r"\frac{16}{2}", "8")

        # Step 3: 8 → 4
        result3 = process_block(result2, r"\frac{8}{2}", "4")

        # Step 4: 4 → 2
        result4 = process_block(result3, r"\frac{4}{2}", "2")

        # Step 5: 2 → 1
        result5 = process_block(result4, r"\frac{2}{2}", "1")

        # --- Closing statement ---
        closing = Tex("No matter where you start, you always end at 1...").scale(0.9).set_color_by_gradient(BLUE, GREEN)
        closing.next_to(result5, DOWN, buff=1)
        self.play(Write(closing))
        self.wait(3)
