from manim import *

class IntegrateX2SinX(Scene):
    def construct(self):
        # === 1. Heading ===
        title = MathTex(r"\int x^2 \sin x \, dx").scale(1.2).set_color(RED).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # === 2. Define u and dv close to title ===
        u_tex = MathTex(r"u = x^2").next_to(title, DOWN, buff=0.5).shift(1.5*LEFT)
        dv_tex = MathTex(r"dv = \sin x\,dx").next_to(title, DOWN, buff=0.5).shift(1.5*RIGHT)
        self.play(Write(u_tex))
        self.play(Write(dv_tex))
        self.wait(0.5)

        # === 3. Build columns (D and I) further down for clarity ===
        d_color = BLUE
        i_color = GREEN

        D_label = MathTex("D", color=d_color).scale(1.2)
        I_label = MathTex("I", color=i_color).scale(1.2)

        D_label.next_to(u_tex, DOWN, buff=0.2)
        I_label.next_to(D_label, RIGHT, buff=3.5)

        self.play(Write(D_label), Write(I_label))
        self.wait(0.3)

        # === 4. Animate differentiation (left column) ===
        d_exprs = [MathTex(r"x^2", color=d_color),
                   MathTex(r"2x", color=d_color),
                   MathTex(r"2", color=d_color),
                   MathTex(r"0", color=d_color)]
        d_exprs[0].next_to(D_label, DOWN, buff=0.5)
        self.play(Write(d_exprs[0]))
        self.wait(0.3)

        d_arrows = []
        for i in range(1, len(d_exprs)):
            arrow = Arrow(d_exprs[i-1].get_bottom(), d_exprs[i-1].get_bottom() + DOWN*0.5, buff=0.1, color=d_color)
            d_arrows.append(arrow)
            self.play(GrowArrow(arrow))
            self.play(Write(d_exprs[i].next_to(d_exprs[i-1], DOWN, buff=0.5)))
            self.wait(0.3)
        self.wait(0.5)

        # === 5. Animate integration (right column) ===
        i_exprs = [MathTex(r"\sin x", color=i_color),
                   MathTex(r"-\cos x", color=i_color),
                   MathTex(r"-\sin x", color=i_color),
                   MathTex(r"\cos x", color=i_color)]
        i_exprs[0].next_to(I_label, DOWN, buff=0.5)
        self.play(Write(i_exprs[0]))
        self.wait(0.3)

        i_arrows = []
        for i in range(1, len(i_exprs)):
            arrow = Arrow(i_exprs[i-1].get_bottom(), i_exprs[i-1].get_bottom() + DOWN*0.5, buff=0.1, color=i_color)
            i_arrows.append(arrow)
            self.play(GrowArrow(arrow))
            self.play(Write(i_exprs[i].next_to(i_exprs[i-1], DOWN, buff=0.5)))
            self.wait(0.3)
        self.wait(0.8)

        # === 6. Animate DI diagonals and show resulting terms ===
        diag_terms = []
        term_texts = [r"-x^2\cos x", r"+\,2x\sin x", r"+\,2\cos x"]
        term_expressions = []

        for i in range(3):
            diag = Arrow(
                d_exprs[i].get_right(),
                i_exprs[i+1].get_left(),
                color=YELLOW,
                buff=0.1,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.08
            )
            diag_terms.append(diag)
            self.play(Create(diag))
            self.play(Indicate(d_exprs[i]), Indicate(i_exprs[i+1]))
            term = MathTex("=", term_texts[i]).next_to(i_exprs[i+1], RIGHT, buff=0.8)
            self.play(FadeIn(term, shift=RIGHT))
            self.wait(0.4)
            term_expressions.append(term)

        self.wait(0.8)

        # === 7. Group everything and shift upward ===
        di_group = VGroup(
            D_label, I_label,
            *d_exprs, *i_exprs,
            *d_arrows, *i_arrows,
            *diag_terms, *term_expressions
        )

        self.play(FadeOut(u_tex,dv_tex,title),di_group.animate.to_edge(UP, buff=0.8))
        self.wait(0.5)

        # === 8. Write final integration result step-by-step ===
        equal_sign = MathTex("=").next_to(di_group, DOWN + LEFT*0.7, buff=1.2)
        Question = MathTex(r"\int x^2 \sin x \, dx").scale(1).set_color(RED).next_to(equal_sign, LEFT, buff=0.5)
        self.play(Write(Question))
        self.wait(0.5)
        self.play(Write(equal_sign))
        self.wait(0.5)

        # Move first term left for spacing
        term1 = MathTex(r"-x^2\cos x", color=BLUE).next_to(equal_sign, RIGHT, buff=0.3)
        self.play(Transform(term_expressions[0][1], term1))
        self.wait(1)

        term2 = MathTex(r"+\,2x\sin x",color=BLUE).next_to(term1, RIGHT, buff=0.3)
        self.play(Transform(term_expressions[1][1], term2))
        self.wait(1)

        term3 = MathTex(r"+\,2\cos x", color=BLUE).next_to(term2, RIGHT, buff=0.3)
        self.play(Transform(term_expressions[2][1], term3))
        self.wait(1)

        term4 = MathTex(r"+" "C", color=BLUE).next_to(term3, RIGHT, buff=0.3)
        self.play(Write(term4))
        self.wait(1)


        # === 9. Fade out DI table, keep only the final expression ===
        self.play(FadeOut(di_group, equal_sign))
        self.wait(0.5)

        final_expr = VGroup(Question, equal_sign, term1, term2, term3, term4)
        self.play(final_expr.animate.to_edge(UP, buff=1))
        self.wait(0.5)

        # === 10. Highlight the final result ===
        box = SurroundingRectangle(final_expr, color=BLUE, buff=0.3)
        self.play(Create(box))
        self.wait(1.5)
