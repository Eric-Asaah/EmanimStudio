# TITLE: Professional Intro
# DESCRIPTION: Elegant text animation with fade effects

from manim import *

class IntroAnimation(Scene):
    def construct(self):
        # Create title
        title = Text("Welcome to EmanimStudio", font_size=48)
        title.set_color_by_gradient(BLUE, PURPLE)
        
        # Create subtitle
        subtitle = Text("Portable Animation System", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.5)
        subtitle.set_color(GRAY)
        
        # Animate title
        self.play(Write(title), run_time=2)
        self.wait(0.5)
        
        # Animate subtitle
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(subtitle, shift=DOWN)
        )
        self.wait(0.5)