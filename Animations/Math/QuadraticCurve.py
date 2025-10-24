from manim import *

class Parabola(Scene):
    def construct(self):
        # 1. Define your axes/plane
        X_MIN = -10
        X_MAX = 10
        X_STEP = 1
        Y_MIN = -5
        Y_MAX = 5 # Adjusted Y_MAX to better show the parabola
        Y_STEP = 1 # Adjusted Y_STEP for a finer grid

        plane = NumberPlane(
            x_range=(X_MIN, X_MAX, X_STEP),
            y_range=(Y_MIN, Y_MAX, Y_STEP)
        )
        self.play(Create(plane)) # Animate the creation of the plane

        # 2. Define the function for your parabola
        def func(x):
            return x**5/50

        # 3. Get the graph Mobject from the plane and set its color
        parabola_graph = plane.plot(func, color=RED)

        # 4. Create a label for the parabola function
        graph_label = MathTex("y = x^2").next_to(parabola_graph, UP + RIGHT)

        # 5. Animate the plotting of the parabola and its label
        self.play(Create(parabola_graph), Write(graph_label))

        # 6. Keep the graph on screen for a moment
        self.wait(2)