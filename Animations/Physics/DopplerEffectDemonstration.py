from manim import *

class GenDynamics(Scene):
    #Create source and obsever
    def construct(self):
        A =Text("Both Approaching", font_size=50).to_edge(UP)
        A.set_color_by_gradient(RED, BLUE, YELLOW)
        Ul1=Underline(A,color=RED)


        B =Text("Both Receeding", font_size=50)
        B.set_color_by_gradient(RED, BLUE, YELLOW).shift(1.1*DOWN)
        Ul2=Underline(B,color=RED)


        source1= Text("Source", font_size=35).shift(6*LEFT +2*UP)
        source1.set_color_by_gradient(RED, PURPLE, LIGHT_BROWN)
        Arrow11=Arrow(start=3*LEFT,end=2*LEFT,buff=0.1,stroke_width=5,color=ORANGE).shift(4*LEFT+1.5*UP)

        observer1= Text("Oberver", font_size=35).shift(6*RIGHT+2*UP)
        observer1.set_color_by_gradient(GREEN,BLUE,LIGHT_BROWN)
        Arrow12=Arrow(start=3*RIGHT,end=2*RIGHT,buff=0.1,stroke_width=5,color=ORANGE).shift(4*RIGHT+1.5*UP)

        S1=SurroundingRectangle(source1)
        O1=SurroundingRectangle(observer1)

        source2= Text("Source", font_size=35).shift(LEFT+2*DOWN)
        source2.set_color_by_gradient(RED, PURPLE, LIGHT_BROWN)
        Arrow21=Arrow(end=3*LEFT,start=2*LEFT,buff=0.1,stroke_width=5, color=ORANGE).shift(0.3*LEFT+2.5*DOWN)

        observer2= Text("Oberver", font_size=35).shift(RIGHT +2*DOWN)
        observer2.set_color_by_gradient(GREEN,BLUE,LIGHT_BROWN)
        Arrow22=Arrow(end=3*RIGHT, start=2*RIGHT,buff=0.1,stroke_width=5,color=ORANGE).shift(0.3*RIGHT+2.5*DOWN)
        
        S2=SurroundingRectangle(source2)
        O2=SurroundingRectangle(observer2)

       
        self.play(Write(A), Create(Ul1),run_time=2)
        self.wait(1)
        self.play(Write(source1),Write(observer1),Create(Arrow11),Create(Arrow12),run_time=2)
        self.wait()
        self.play(source1.animate.shift(5*RIGHT),observer1.animate.shift(5*LEFT),Arrow11.animate.shift(5*RIGHT),Arrow12.animate.shift(5*LEFT),run_time=7)
        self.wait(2)


        self.play(Write(B),Create(Ul2), run_time=2)
        self.wait()
        self.play(Write(source2),Write(observer2),Create(Arrow21),Create(Arrow22),run_time=2)
        self.wait()
        self.play(source2.animate.shift(5*LEFT),observer2.animate.shift(5*RIGHT),Arrow21.animate.shift(5*LEFT),Arrow22.animate.shift(5*RIGHT),run_time=7)
        self.wait(6)