from manim import *

class GoldbachWalkthrough(Scene):
    def construct(self):
        # STEP 2: Prompt - "Take an even number..."
        prompt = Text("Take an even number...", font_size=36).shift(UP*2.8).set_color_by_gradient(BLUE, GREEN)
        self.play(Write(prompt))
        self.wait(2)
        Realization=Text("This pattern continues even with larger integers...", font_size=36).shift(UP*2.8).set_color_by_gradient(BLUE, GREEN)

        # STEP 3: Show 4 = 2 + 2
        ex1 = MathTex("4", "=", "2", "+", "2").scale(1.2).shift(UP*0.5)
        self.play(Write(ex1))
        self.wait(2)

        # STEP 4: Show 6 = 3 + 3
        ex2 = MathTex("6", "=", "3", "+", "3").scale(1.2).next_to(ex1, DOWN, buff=0.7)
        self.play(Write(ex2))
        self.wait(2)

        # STEP 5: Show 8 = 5 + 3
        ex3 = MathTex("8", "=", "5", "+", "3").scale(1.2).next_to(ex2, DOWN, buff=0.7)
        self.play(Write(ex3))
        self.wait(2)

        self.play(FadeOut(ex1, ex2, ex3, prompt))
        self.play(Write(Realization))
        self.wait(1)


        # STEP 6: More examples together
        examples_group = VGroup(
            MathTex("10", "=", "5", "+", "5"),
            MathTex("12", "=", "7", "+", "5"),
            MathTex("14", "=", "7", "+", "7"),
            MathTex("16", "=", "13", "+", "3"),
            MathTex("18", "=", "13", "+", "5"),
        ).arrange(DOWN, buff=0.8)

        self.play(LaggedStart(*[Write(eq) for eq in examples_group], lag_ratio=0.6))
        self.wait(5)
        self.play(FadeOut(examples_group, Realization))

        # STEP 7: Ask the big question
        question = Text("Can EVERY even number > 2 be written this way?", 
                        font_size=36, color=YELLOW)
        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question))
        Question = Text("We believe so!", 
                        font_size=36, color=YELLOW)
        self.play(Write(Question))
        self.wait(2)
        self.play(FadeOut(Question))

        Question1 = Text("Because no one has found a counterexample yet...", 
                        font_size=36, color=YELLOW)
        self.play(Write(Question1))
        self.wait(2)
        self.play(FadeOut(Question1))
        

        goldbach = Text("The Goldbach Conjecture", font_size=46, weight=BOLD).to_edge(UP, buff=0.7).set_color_by_gradient(BLUE,GREEN)

        underline = Line(goldbach.get_left(), goldbach.get_right()).next_to(goldbach, DOWN, buff=0.1)
        self.play(Write(goldbach), Create(underline))
        self.wait(3)

        # STEP 10: Statement of the conjecture
        statement = Text(
            "Every even integer greater than 2\nis the sum of two primes.",
            font_size=34
        ).next_to(goldbach, DOWN, buff=1)
        self.play(Write(statement))
        self.wait(4)
