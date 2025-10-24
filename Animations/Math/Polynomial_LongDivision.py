from manim import *

class PolynomialLongDivision(Scene):
    def construct(self):
        # ---- Title ----
        title = Tex("Polynomial Long Division", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---- Original Expression ----
        expr = MathTex(r"\frac{x^3 + 2x^2 - 5x + 6}{x - 2}").next_to(title, DOWN, buff=0.5)
        self.play(Write(expr))
        self.wait(0.5)

        # ---- Setup Division Structure ----
        # Divisor
        divisor = MathTex("x - 2").scale(0.9)
        divisor.move_to([-3.5, 0.5, 0])
        
        # Division symbol (like long division bracket)
        # Vertical line
        vline = Line(
            start=divisor.get_right() + RIGHT * 0.3,
            end=divisor.get_right() + RIGHT * 0.3 + DOWN * 4,
            stroke_width=3
        )
        
        # Horizontal line on top
        hline_top = Line(
            start=divisor.get_right() + RIGHT * 0.3,
            end=divisor.get_right() + RIGHT * 5.5,
            stroke_width=3
        )
        
        # Dividend (polynomial being divided)
        dividend = MathTex("x^3 + 2x^2 - 5x + 6").scale(0.9)
        dividend.next_to(hline_top, DOWN, buff=0.3, aligned_edge=LEFT)
        dividend.shift(RIGHT * 0.3)
        
        self.play(Write(divisor), Create(vline), Create(hline_top))
        self.play(Write(dividend))
        self.wait(0.5)

        # ---- Step 1: x³ ÷ x = x² ----
        quotient1 = MathTex("x^2").scale(0.9)
        quotient1.next_to(hline_top, UP, buff=0.2, aligned_edge=LEFT)
        quotient1.shift(RIGHT * 0.3)
        
        # Curved arrow from x³ to x² 
        arc1 = CurvedArrow(
            start_point=dividend[0][0:2].get_top(),
            end_point=quotient1.get_bottom(),
            angle=-TAU/6,
            color=YELLOW
        )
        
        self.play(ShowPassingFlash(arc1, time_width=0.5), run_time=1)
        self.play(Write(quotient1))
        self.wait(0.5)

        # ---- Step 2: Multiply x² by (x - 2) = x³ - 2x² ----
        product1 = MathTex("x^3 - 2x^2").scale(0.9)
        product1.next_to(dividend, DOWN, buff=0.5, aligned_edge=LEFT)
        
        # Curved arrows showing multiplication
        arc2a = CurvedArrow(
            start_point=divisor.get_right() + RIGHT * 0.1,
            end_point=quotient1.get_left() + LEFT * 0.1,
            angle=-TAU/6,
            color=BLUE
        )
        arc2b = CurvedArrow(
            start_point=quotient1.get_left() + DOWN * 0.3,
            end_point=product1.get_left() + LEFT * 0.1,
            angle=-TAU/6,
            color=BLUE
        )
        
        self.play(ShowPassingFlash(arc2a, time_width=0.4), run_time=1)
        self.play(ShowPassingFlash(arc2b, time_width=0.4), run_time=1)
        self.play(Write(product1))
        self.wait(0.5)

        # ---- Step 3: Subtract to get remainder ----
        underline1 = Line(
            start=product1.get_left() + LEFT * 0.2,
            end=product1.get_right() + RIGHT * 0.2,
            stroke_width=2,
            color=RED
        )
        self.play(Create(underline1))
        self.wait(0.3)
        
        remainder1 = MathTex("4x^2 - 5x").scale(0.9)
        remainder1.next_to(underline1, DOWN, buff=0.3, aligned_edge=LEFT)
        remainder1.shift(RIGHT * 0.5)
        
        self.play(Write(remainder1))
        self.wait(0.5)

        # ---- Step 4: Bring down +6 ----
        bring_down = MathTex("+ 6").scale(0.9).set_color(GREEN)
        bring_down.next_to(remainder1, RIGHT, buff=0.1)
        
        arc3 = CurvedArrow(
            start_point=dividend[0][-1].get_center() + DOWN * 0.2,
            end_point=bring_down.get_top() + UP * 0.1,
            angle=TAU/6,
            color=GREEN
        )
        
        self.play(ShowPassingFlash(arc3, time_width=0.5), run_time=1)
        self.play(Write(bring_down))
        self.wait(0.5)
        
        # Combine remainder
        remainder1_full = MathTex("4x^2 - 5x + 6").scale(0.9)
        remainder1_full.move_to(remainder1.get_center()).shift(RIGHT * 0.3)
        self.play(Transform(VGroup(remainder1, bring_down), remainder1_full))
        self.wait(0.5)

        # ---- Step 5: 4x² ÷ x = 4x ----
        quotient2 = MathTex("+ 4x").scale(0.9)
        quotient2.next_to(quotient1, RIGHT, buff=0.1)
        
        arc4 = CurvedArrow(
            start_point=remainder1_full[0][0:3].get_top(),
            end_point=quotient2.get_bottom(),
            angle=-TAU/6,
            color=YELLOW
        )
        
        self.play(ShowPassingFlash(arc4, time_width=0.5), run_time=1)
        self.play(Write(quotient2))
        self.wait(0.5)

        # ---- Step 6: Multiply 4x by (x - 2) = 4x² - 8x ----
        product2 = MathTex("4x^2 - 8x").scale(0.9)
        product2.next_to(remainder1_full, DOWN, buff=0.5, aligned_edge=LEFT)
        product2.shift(RIGHT * 0.5)
        
        arc5a = CurvedArrow(
            start_point=divisor.get_right() + DOWN * 0.5,
            end_point=quotient2.get_left() + LEFT * 0.1,
            angle=-TAU/8,
            color=BLUE
        )
        arc5b = CurvedArrow(
            start_point=quotient2.get_left() + DOWN * 0.3,
            end_point=product2.get_left() + LEFT * 0.1,
            angle=-TAU/6,
            color=BLUE
        )
        
        self.play(ShowPassingFlash(arc5a, time_width=0.4), run_time=1)
        self.play(ShowPassingFlash(arc5b, time_width=0.4), run_time=1)
        self.play(Write(product2))
        self.wait(0.5)

        # ---- Step 7: Subtract ----
        underline2 = Line(
            start=product2.get_left() + LEFT * 0.2,
            end=product2.get_right() + RIGHT * 0.2,
            stroke_width=2,
            color=RED
        )
        self.play(Create(underline2))
        self.wait(0.3)
        
        remainder2 = MathTex("3x + 6").scale(0.9)
        remainder2.next_to(underline2, DOWN, buff=0.3, aligned_edge=LEFT)
        remainder2.shift(RIGHT * 0.5)
        
        self.play(Write(remainder2))
        self.wait(0.5)

        # ---- Step 8: 3x ÷ x = 3 ----
        quotient3 = MathTex("+ 3").scale(0.9)
        quotient3.next_to(quotient2, RIGHT, buff=0.1)
        
        arc6 = CurvedArrow(
            start_point=remainder2[0][0:2].get_top(),
            end_point=quotient3.get_bottom(),
            angle=-TAU/6,
            color=YELLOW
        )
        
        self.play(ShowPassingFlash(arc6, time_width=0.5), run_time=1)
        self.play(Write(quotient3))
        self.wait(0.5)

        # ---- Step 9: Multiply 3 by (x - 2) = 3x - 6 ----
        product3 = MathTex("3x - 6").scale(0.9)
        product3.next_to(remainder2, DOWN, buff=0.5, aligned_edge=LEFT)
        product3.shift(RIGHT * 0.5)
        
        arc7a = CurvedArrow(
            start_point=divisor.get_right() + DOWN * 1.5,
            end_point=quotient3.get_left() + LEFT * 0.1,
            angle=-TAU/10,
            color=BLUE
        )
        arc7b = CurvedArrow(
            start_point=quotient3.get_left() + DOWN * 0.3,
            end_point=product3.get_left() + LEFT * 0.1,
            angle=-TAU/6,
            color=BLUE
        )
        
        self.play(ShowPassingFlash(arc7a, time_width=0.4), run_time=1)
        self.play(ShowPassingFlash(arc7b, time_width=0.4), run_time=1)
        self.play(Write(product3))
        self.wait(0.5)

        # ---- Step 10: Final subtraction ----
        underline3 = Line(
            start=product3.get_left() + LEFT * 0.2,
            end=product3.get_right() + RIGHT * 0.2,
            stroke_width=2,
            color=RED
        )
        self.play(Create(underline3))
        self.wait(0.3)
        
        final_remainder = MathTex("12", color=GREEN).scale(0.9)
        final_remainder.next_to(underline3, DOWN, buff=0.3, aligned_edge=LEFT)
        final_remainder.shift(RIGHT * 1.5)
        
        self.play(Write(final_remainder))
        self.wait(0.8)

        # ---- Final Answer ----
        answer_label = Tex("Quotient:", color=YELLOW).scale(0.8)
        answer_quotient = MathTex("x^2 + 4x + 3", color=YELLOW).scale(0.9)
        remainder_label = Tex("Remainder:", color=GREEN).scale(0.8)
        answer_remainder = MathTex("12", color=GREEN).scale(0.9)
        
        answer_group = VGroup(
            answer_label, answer_quotient,
            remainder_label, answer_remainder
        ).arrange(RIGHT, buff=0.3)
        answer_group.next_to(final_remainder, DOWN, buff=0.8)
        
        self.play(Write(answer_group))
        self.wait(0.8)

        # ---- Complete Expression ----
        final_expr = MathTex(
            r"\frac{x^3 + 2x^2 - 5x + 6}{x - 2} = x^2 + 4x + 3 + \frac{12}{x - 2}"
        ).scale(0.85)
        final_expr.next_to(answer_group, DOWN, buff=0.6)
        
        self.play(Write(final_expr))
        self.wait(1)

        # ---- Fade everything except final expression ----
        fade_group = [
            title, expr, divisor, vline, hline_top, dividend,
            quotient1, quotient2, quotient3,
            product1, product2, product3,
            underline1, underline2, underline3,
            remainder1_full, remainder2, final_remainder,
            answer_group
        ]
        
        self.play(
            *[FadeOut(obj) for obj in fade_group],
            final_expr.animate.move_to(ORIGIN).scale(1.2)
        )
        self.wait(0.5)

        # ---- Highlight final answer ----
        box = SurroundingRectangle(final_expr, color=BLUE, buff=0.2)
        self.play(Create(box))
        self.play(final_expr.animate.set_color(YELLOW))
        self.wait(2)