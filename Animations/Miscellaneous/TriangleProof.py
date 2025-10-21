from manim import *

class TriangleAltitudes(Scene):
    def construct(self):
        # Scaling factor to fit Manim's coordinate system
        scale = 0.01  # Divide TikZ coordinates by 100
        # Shift to center the diagram in Manim's frame
        shift_x = -3.5  # Approximate center of x-range (51.33 to 591.33)
        shift_y = -1.5  # Approximate center of y-range (5.67 to 270.67)

        # Define vertices of the right triangle
        A = [scale * 51.33 + shift_x, -scale * 5.67 + shift_y, 0]  # Top vertex
        B = [scale * 591.33 + shift_x, -scale * 270.67 + shift_y, 0]  # Right vertex
        C = [scale * 51.33 + shift_x, -scale * 270.67 + shift_y, 0]  # Bottom-left vertex

        # Create the triangle
        triangle = Polygon(A, B, C, color=WHITE, stroke_width=3)
        self.play(Create(triangle), run_time=2)
        self.wait(1)

        # Right angle marker at C (51.33, 270.67) using two Lines
        ra_C_1_start = [scale * 51.33 + shift_x, -scale * 262.67 + shift_y, 0]
        ra_C_1_end = [scale * 61.33 + shift_x, -scale * 262.67 + shift_y, 0]
        ra_C_2_start = [scale * 61.33 + shift_x, -scale * 262.67 + shift_y, 0]
        ra_C_2_end = [scale * 61.33 + shift_x, -scale * 270.67 + shift_y, 0]
        right_angle_C_1 = Line(ra_C_1_start, ra_C_1_end, color=WHITE, stroke_width=3)
        right_angle_C_2 = Line(ra_C_2_start, ra_C_2_end, color=WHITE, stroke_width=3)
        right_angle_C_group = VGroup(right_angle_C_1, right_angle_C_2)
        self.play(Create(right_angle_C_group), run_time=1)
        self.wait(0.5)

        # First altitude from (153.33, 54.67) to (51.33, 270.67)
        alt1_start = [scale * 153.33 + shift_x, -scale * 54.67 + shift_y, 0]
        alt1_end = [scale * 51.33 + shift_x, -scale * 270.67 + shift_y, 0]
        altitude1 = Line(alt1_start, alt1_end, color=WHITE, stroke_width=3)
        self.play(Create(altitude1), run_time=1.5)
        self.wait(0.5)

        # Right angle marker for first altitude at (153.33, 54.67) using two Lines
        ra_alt1_1_start = [scale * 149.97 + shift_x, -scale * 62.06 + shift_y, 0]
        ra_alt1_1_end = [scale * 140.33 + shift_x, -scale * 57.67 + shift_y, 0]
        ra_alt1_2_start = [scale * 140.33 + shift_x, -scale * 57.67 + shift_y, 0]
        ra_alt1_2_end = [scale * 143.7 + shift_x, -scale * 50.28 + shift_y, 0]
        right_angle_alt1_1 = Line(ra_alt1_1_start, ra_alt1_1_end, color=WHITE, stroke_width=3)
        right_angle_alt1_2 = Line(ra_alt1_2_start, ra_alt1_2_end, color=WHITE, stroke_width=3)
        right_angle_alt1_group = VGroup(right_angle_alt1_1, right_angle_alt1_2)
        self.play(Create(right_angle_alt1_group), run_time=1)
        self.wait(0.5)

        # Second altitude from (153.33, 54.67) to (153.33, 269.67)
        alt2_start = [scale * 153.33 + shift_x, -scale * 54.67 + shift_y, 0]
        alt2_end = [scale * 153.33 + shift_x, -scale * 269.67 + shift_y, 0]
        altitude2 = Line(alt2_start, alt2_end, color=WHITE, stroke_width=3)
        self.play(Create(altitude2), run_time=1.5)
        self.wait(0.5)

        # Right angle marker for second altitude at (153.33, 269.67) using two Lines
        ra_alt2_1_start = [scale * 153.33 + shift_x, -scale * 264.67 + shift_y, 0]
        ra_alt2_1_end = [scale * 160.33 + shift_x, -scale * 264.67 + shift_y, 0]
        ra_alt2_2_start = [scale * 160.33 + shift_x, -scale * 264.67 + shift_y, 0]
        ra_alt2_2_end = [scale * 160.33 + shift_x, -scale * 269.67 + shift_y, 0]
        right_angle_alt2_1 = Line(ra_alt2_1_start, ra_alt2_1_end, color=WHITE, stroke_width=3)
        right_angle_alt2_2 = Line(ra_alt2_2_start, ra_alt2_2_end, color=WHITE, stroke_width=3)
        right_angle_alt2_group = VGroup(right_angle_alt2_1, right_angle_alt2_2)
        self.play(Create(right_angle_alt2_group), run_time=1)
        self.wait(0.5)

        # Third altitude from (238.33, 95.67) to (153.33, 269.67)
        alt3_start = [scale * 238.33 + shift_x, -scale * 95.67 + shift_y, 0]
        alt3_end = [scale * 153.33 + shift_x, -scale * 269.67 + shift_y, 0]
        altitude3 = Line(alt3_start, alt3_end, color=WHITE, stroke_width=3)
        self.play(Create(altitude3), run_time=1.5)
        self.wait(0.5)

        # Extension of third altitude to (240.33, 271.67)
        alt3_ext_end = [scale * 240.33 + shift_x, -scale * 271.67 + shift_y, 0]
        altitude3_ext = Line(alt3_start, alt3_ext_end, color=WHITE, stroke_width=3)
        self.play(Create(altitude3_ext), run_time=1)
        self.wait(0.5)

        # Right angle marker for third altitude at (238.33, 95.67) using two Lines
        ra_alt3_1_start = [scale * 235.72 + shift_x, -scale * 106.06 + shift_y, 0]
        ra_alt3_1_end = [scale * 227.33 + shift_x, -scale * 101.67 + shift_y, 0]
        ra_alt3_2_start = [scale * 227.33 + shift_x, -scale * 101.67 + shift_y, 0]
        ra_alt3_2_end = [scale * 231.76 + shift_x, -scale * 93.22 + shift_y, 0]
        right_angle_alt3_1 = Line(ra_alt3_1_start, ra_alt3_1_end, color=WHITE, stroke_width=3)
        right_angle_alt3_2 = Line(ra_alt3_2_start, ra_alt3_2_end, color=WHITE, stroke_width=3)
        right_angle_alt3_group = VGroup(right_angle_alt3_1, right_angle_alt3_2)
        self.play(Create(right_angle_alt3_group), run_time=1)
        self.wait(0.5)

        # Line from (50.33, 58.33) to (153.33, 54.67)
        line1_start = [scale * 50.33 + shift_x, -scale * 58.33 + shift_y, 0]
        line1_end = [scale * 153.33 + shift_x, -scale * 54.67 + shift_y, 0]
        line1 = Line(line1_start, line1_end, color=WHITE, stroke_width=3)
        self.play(Create(line1), run_time=1)
        self.wait(0.5)

        # Line from (153.33, 91.67) to (240.14, 97.62)
        line2_start = [scale * 153.33 + shift_x, -scale * 91.67 + shift_y, 0]
        line2_end = [scale * 240.14 + shift_x, -scale * 97.62 + shift_y, 0]
        line2 = Line(line2_start, line2_end, color=WHITE, stroke_width=3)
        self.play(Create(line2), run_time=1)
        self.wait(0.5)

        self.wait(2)