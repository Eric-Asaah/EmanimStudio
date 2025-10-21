# TITLE: Amazing Logo Animation
# DESCRIPTION: This animation demonstrates a beautiful logo reveal with smooth transitions and particle effects
from manim import *
import math

class AMPLogo(Scene):
    def construct(self):
        self.camera.background_color = "#00000000"  # Black background

        # Parametric curve a (smaller)
        curve_a = ParametricFunction(
            lambda t: [np.cos(10 * t) + np.cos(23 * t), np.sin(10 * t) - np.sin(23 * t), 0], t_range=[-5, 5, 0.01],
            stroke_width=2)
        curve_a.set_color(GREEN)
        curve_a.set_stroke_width(1)



        # Parametric curve b (larger)
        curve_b = ParametricFunction(
            lambda t: [2.3 * np.cos(10 * t) + np.cos(23 * t), 2.3 * np.sin(10 * t) - np.sin(23 * t), 0], t_range=[-5, 5, 0.01],
            stroke_width=2)
        curve_b.set_color(BLUE)
        curve_b.scale(0.7)
        curve_b.set_stroke_width(5)



        # Circle
        circle = Circle(radius=2.30, color=RED_E)
        circle.set_stroke_width(5)



        # Large "AMP" text
        emp= MathTex(r"\text{EMP}", font_size=35, color=RED+BLUE+GREEN)


        #Name of brand with logo
        Name = Text("EMAPHY", font="Futura", font_size=60)
        Name.set_color_by_gradient(RED,BLUE,GREEN)
        Name.shift(1.35*DOWN+0.02*RIGHT)
        #Background Rectangle for Name



        rect=BackgroundRectangle(Name, color=BLACK, fill_opacity=1)

        # Group all elements
        logo= VGroup(curve_a, curve_b, circle, emp, rect, Name)
        logo.shift(UP)

       # self.add(logo)
       
        self.play(Create(curve_a, run_time=1, func_rate=linear))
        self.play(Create(curve_b,  run_time=1, func_rate=linear))
        self.play(Write(emp),  run_time=0.5, func_rate=linear)
        self.play(Create(rect),  run_time=0.5, func_rate=linear)
        self.play(Write(Name, run_time=2, func_rate=linear))
        self.play(Create(circle))