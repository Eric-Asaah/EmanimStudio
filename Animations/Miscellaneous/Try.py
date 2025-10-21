from manim import *

class DopplerEffect(Scene):
    def construct(self):
        # Moving source
        source = Dot(color=RED).move_to(LEFT * 5)
        label = Text("Source", font_size=24).next_to(source, DOWN)
        destination= Dot(color=GREEN).move_to(RIGHT * 5)
        label_destination = Text("Observer", font_size=24).next_to(destination, DOWN)

        self.add(source, label, destination, label_destination)

        # Emit expanding waves
        def make_wave(center):
            return Circle(radius=2, color=BLUE).move_to(center).set_stroke(width=2)

        waves = VGroup()
        self.add(waves)

        # Animate source moving and emitting waves
        def emit_waves(mob, dt):
            new_wave = make_wave(source.get_center())
            waves.add(new_wave)
            for w in waves:
                w.set_radius(w.radius + dt * 2)  # expand
                w.set_stroke(opacity=max(0, 1 - w.radius / 6))  # fade out
            # remove old waves
            if waves and waves[0].radius > 6:
                waves.remove(waves[0])

        waves.add_updater(emit_waves)


        TITLE_FONT_SIZE = 56
        SUBTITLE_FONT_SIZE = 48
        BODY_FONT_SIZE = 36
        SMALL_FONT_SIZE = 24
        FOOTNOTE_FONT_SIZE = 18

        equation = MathTex(
            "f'", "=", "f", r"\left( \frac{V \pm V_o}{V \pm V_s} \right)",
            font_size=BODY_FONT_SIZE,
            color=ManimColor.from_hex("#ffffff")
        )
        equation.set_color_by_gradient(RED, BLUE)
        equation.scale(1.5)
        equation.to_edge(UP)
 # Move the source to the right
        self.play(Write(equation), source.animate.shift(RIGHT * 10), rate_func=linear, run_time=6) 
        self.wait(1)