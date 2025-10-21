from manim import *

class FractionPattern(Scene):
    def construct(self):
        title = Text("The Beauty of 1 / (99²)", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Step 1: Show the fraction
        frac = MathTex(r"\frac{1}{99^2} = \frac{1}{9801}", font_size=48)
        self.play(Write(frac))
        self.wait(1)

        # Step 2: Show the decimal expansion beginning
        dec_text = Text("Look at the decimal:", font_size=36).next_to(frac, DOWN, buff=1)
        self.play(Write(dec_text))

        decimal = Text("0.0001020304050607...", font_size=36).next_to(dec_text, DOWN)
        self.play(Write(decimal))
        self.wait(1)

        # Step 3: Highlight the counting
        count_text = Text("It's counting two-digit numbers!", font_size=36).next_to(decimal, DOWN, buff=1)
        self.play(FadeIn(count_text))
        self.wait(2)

        # Step 4: Animate the pattern
        count_numbers = VGroup()
        for i in range(1, 10):
            num = Text(f"{i:02}", font_size=32)
            num.shift(RIGHT * (i - 5) * 0.9 + DOWN * 2.5)
            count_numbers.add(num)

        self.play(*[FadeIn(n) for n in count_numbers], run_time=2)
        self.wait(2)

        # Step 5: Outro
        outro = Text("The magic inside a simple fraction...", font_size=40).set_slant(ITALIC).to_edge(DOWN)
        self.play(FadeIn(outro))
        self.wait(3)

        # Fade out all elements for a clean ending
        self.play(*[FadeOut(mob) for mob in self.mobjects])
