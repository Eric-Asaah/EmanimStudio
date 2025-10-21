from manim import *
config.frame_width = 16
config_frame_height = 9
class WriteDopplerEffect(Scene):
    def construct(self):
        title = Text("Doppler Effect", font_size=100).to_edge(UP)
        title.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        Ul=Underline(title, color=RED)
        self.play(Write(title), Create(Ul), run_time=3)
        self.wait(2)
        Definition=[Text("The change in frequency or wavelength of a wave in relation", font_size=38).shift(UP*1.5),     
        Text("to an observer who is moving relative to the wave source.", font_size=38).shift(UP*0.5)]
        for i in Definition:
            i.set_color_by_gradient(GREEN, BLUE, PURPLE)
            self.play(Write(i))
        self.wait(1)
       