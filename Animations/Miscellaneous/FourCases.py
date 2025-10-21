from manim import *
config.frame_width = 16
config.frame_height = 9
class FourCases(Scene):
    def construct(self):
        title = Text("Four Cases of Doppler Effect", font_size=80).to_edge(UP)
        title.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        Ul=Underline(title, color=RED)
        self.play(Write(title), Create(Ul), run_time=4)
        self.wait(1)
        Scenario_1=Text("1. Source follows observer: Source chasing", font_size=45).shift(UP*1.5)
        Scenario_1.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        Box=Rectangle(height=1, width=1, color=BLUE).shift(5*LEFT+DOWN*0.5)
        Box.set_fill(BLUE, opacity=5)
        self.play(Create(Box), run_time=0.2)
        self.play(Write(Scenario_1), Box.animate.shift(10*RIGHT), run_time=4)
        Circle1=Circle(radius=1, color=YELLOW)
        Circle1.set_fill(BLUE, opacity=3)
        self.play(ReplacementTransform(Box, Circle1), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(Circle1))
        