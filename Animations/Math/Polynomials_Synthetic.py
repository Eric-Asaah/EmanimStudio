from manim import *

class SyntheticDivisionClean(Scene):
    def construct(self):
        # ---- Parameters ----
        x_spacing = 1.3
        top_y = 1.0
        mid_y = 0.3
        bottom_y = -0.5

        # ---- Title ----
        title = Tex("Synthetic Division", font_size=48).to_edge(UP)

        title.set_color(BLUE)
        Uline=Underline(title, color=RED)
        self.play(Write(title), Create(Uline))
        self.wait(0.5)

        # ---- Expression ----
        expr = MathTex(r"\frac{2x^3 + 3x^2 - 5x + 6}{x - 2}").next_to(title, DOWN, buff=0.5)
        expr.set_color_by_gradient(BLUE,GREEN)
        self.play(Write(expr))
        self.wait(0.5)

        # ---- Coefficients ----
        coeff_vals = [2, 3, -5, 6]
        coeffs = VGroup(*[MathTex(str(v)) for v in coeff_vals]).arrange(RIGHT, buff=x_spacing)
        coeffs.move_to([0, top_y, 0])
        for c in coeffs:
            c.set_color(BLUE)
        self.play(Write(coeffs))
        self.wait(0.5)

        # ---- Divisor and divider lines ----
        divisor = MathTex("2", color=GREEN).next_to(coeffs, LEFT, buff=1)
        vline = Line(divisor.get_right() + RIGHT*0.25, divisor.get_right() + RIGHT*0.25 + DOWN*1.8, stroke_width=3, color=RED)
        
        hline = Line(coeffs[0].get_left() + LEFT*0.2, coeffs[-1].get_right() + RIGHT*0.2, stroke_width=3, color=RED)
        hline.move_to([0, bottom_y + 0.25, 0])
        self.play(Write(divisor), Create(vline), Create(hline))
        self.wait(0.4)

        # ---- Step 1: zero under first coeff ----
        zero = MathTex("0").move_to([coeffs[0].get_center()[0], mid_y, 0])
        self.play(Write(zero))
        self.wait(0.3)

        # ---- Step 2: 2 + 0 = 2 ----
        bottom1 = MathTex("2",color=RED).move_to([coeffs[0].get_center()[0], bottom_y, 0])
        self.play(TransformFromCopy(coeffs[0], bottom1))
        self.wait(0.5)

        # ---- Step 3: Multiply (2 * 2 = 4) ----
        product1 = MathTex("4").move_to([coeffs[1].get_center()[0], mid_y, 0])
        arc1a = ArcBetweenPoints(divisor.get_right(), bottom1.get_left(),color=YELLOW, angle=PI/3)

        arc1b = ArcBetweenPoints(bottom1.get_right(), product1.get_left(),color=YELLOW, angle=PI/3)

        self.play(ShowPassingFlash(arc1a, time_width=0.4), run_time=1.5)
        self.play(ShowPassingFlash(arc1b, time_width=0.4), run_time=1.5)
        self.play(Write(product1))
        self.wait(0.3)

        # ---- Step 4: 3 + 4 = 7 ----
        bottom2 = MathTex("7",color=RED).move_to([coeffs[1].get_center()[0], bottom_y, 0])
        self.play(Write(bottom2))
        self.wait(0.4)

        # ---- Step 5: Multiply (2 * 7 = 14) ----
        product2 = MathTex("14").move_to([coeffs[2].get_center()[0], mid_y, 0])
        arc2a = ArcBetweenPoints(divisor.get_right(), bottom2.get_left(),color=YELLOW, angle=PI/3)

        arc2b = ArcBetweenPoints(bottom2.get_right(), product2.get_left(), color=YELLOW, angle=PI/3)

        self.play(ShowPassingFlash(arc2a, time_width=0.3), run_time=1.5)
        self.play(ShowPassingFlash(arc2b, time_width=0.3), run_time=1.5)
        self.play(Write(product2))
        self.wait(0.3)

        # ---- Step 6: -5 + 14 = 9 ----
        bottom3 = MathTex("9",color=RED).move_to([coeffs[2].get_center()[0], bottom_y, 0])
        self.play(Write(bottom3))
        self.wait(0.4)

        # ---- Step 7: Multiply (2 * 9 = 18) ----
        product3 = MathTex("18",color=RED).move_to([coeffs[3].get_center()[0], mid_y, 0])
        arc3a = ArcBetweenPoints(divisor.get_right(), bottom3.get_left(),color=YELLOW, angle=PI/3)

        arc3b = ArcBetweenPoints(bottom3.get_right(), product3.get_left(),color=YELLOW, angle=-PI/3)

        self.play(ShowPassingFlash(arc3a, time_width=0.3), run_time=1.5)
        self.play(ShowPassingFlash(arc3b, time_width=0.3), run_time=1.5)
        self.play(Write(product3))
        self.wait(0.3)

        # ---- Step 8: 6 + 18 = 24 ----
        bottom4 = MathTex("24",color=BLUE).move_to([coeffs[3].get_center()[0], bottom_y, 0])
        self.play(Write(bottom4))
        self.wait(2)

        # ---- Quotient & remainder ----
        quotient = MathTex(r"2x^2 + 7x + 9", color=RED).next_to(hline, DOWN, buff=1.0).shift(LEFT*1)
        remainder = MathTex(r"R = 24", color=BLUE).next_to(quotient, RIGHT, buff=1.0)
        self.play(Write(quotient), Write(remainder), run_time=2)
        self.wait(1.0)

        # ---- Final Expression ----
        final = MathTex(
            r"\frac{2x^3 + 3x^2 - 5x + 6}{x - 2} = 2x^2 + 7x + 9 + \frac{24}{x - 2}"
        ).scale(0.9).next_to(quotient, DOWN, buff=0.7)
        self.play(Write(final))
        self.wait(1)

        # ---- Fade all except final ----
        fade_out_group = [Uline,coeffs, divisor, vline, hline, zero,
                          product1, product2, product3,
                          bottom1, bottom2, bottom3, bottom4,
                          quotient, remainder, title, expr]
        self.play(*[FadeOut(m) for m in fade_out_group],
                  final.animate.move_to(ORIGIN))
        self.wait(0.5)

        # ---- Highlight final answer ----
        box = SurroundingRectangle(final, color=RED, buff=0.2)
        self.play(Create(box))
        self.play(final.animate.set_color(BLUE))
        self.wait(2)
