from manim import *

class ValueTrackerScene(Scene):
    def construct(self):
        # Create a ValueTracker
        k = ValueTracker(5)

        # Create a DecimalNumber that updates with k's value
        num = always_redraw(
            lambda: DecimalNumber(
                k.get_value(), num_decimal_places=1
            ).scale(2).set_color(WHITE)
        )

        # Position the number at the center
        num.move_to(ORIGIN)

        # Add number to the scene
        self.play(FadeIn(num))
        self.wait(1)

        # Animate the value changing from 5 to 10
        self.play(k.animate.set_value(10), run_time=5, rate_func=linear)
        self.wait()
