from manim import *

class GeometricConstruction(Scene):
    def construct(self):
        # TikZ coordinate system: x=0.75pt, y=0.75pt, yscale=-1
        # Convert TikZ coordinates to Manim (scale and flip y-axis)
        scale = 0.023  # Global scale to fit viewport
        
        def tikz_to_manim(x, y):
            """Convert TikZ coordinates to Manim coordinates"""
            # Apply TikZ scaling and flip y-axis
            mx = x * 0.75 * scale
            my = -y * 0.75 * scale  # Flip y-axis (yscale=-1 in TikZ)
            return np.array([mx, my, 0])
        
        # Main triangle vertices (exact TikZ coordinates)
        A = tikz_to_manim(51.33, 5.67)
        B = tikz_to_manim(591.33, 270.67)
        C = tikz_to_manim(51.33, 270.67)
        
        # Perpendicular intersections on hypotenuse (blue line endpoints)
        perp_tops = [
            tikz_to_manim(153.2, 54.97),   # R1
            tikz_to_manim(237.6, 98.49),   # R2
            tikz_to_manim(321.33, 138.17), # R3
            tikz_to_manim(379, 166.75),    # R4
            tikz_to_manim(420.33, 187),    # R5
            tikz_to_manim(454.97, 203.29), # R6
            tikz_to_manim(480.33, 215.67), # R7
            tikz_to_manim(500.33, 226),    # R8
            tikz_to_manim(521.33, 236.08), # R9
            tikz_to_manim(540.33, 246),    # R10
            tikz_to_manim(555.33, 253),    # R11
        ]
        
        # Base points (orange line endpoints on horizontal base)
        perp_bases = [
            tikz_to_manim(51.33, 270.67),   # Base of R1
            tikz_to_manim(153.33, 270.92),  # Base of R2
            tikz_to_manim(238, 270.92),     # Base of R3
            tikz_to_manim(320.33, 270.33),  # Base of R4
            tikz_to_manim(379.33, 271),     # Base of R5
            tikz_to_manim(420, 270.25),     # Base of R6
            tikz_to_manim(455.17, 270.92),  # Base of R7
            tikz_to_manim(481.33, 270.67),  # Base of R8
            tikz_to_manim(500.33, 271),     # Base of R9
            tikz_to_manim(521.33, 271),     # Base of R10
            tikz_to_manim(540.33, 271),     # Base of R11
            tikz_to_manim(555.33, 271),     # Base of R12
        ]
        
        # Green segment endpoints (horizontal segments on hypotenuse)
        green_segments = [
            (tikz_to_manim(51.81, 55.62), tikz_to_manim(153.2, 54.97)),
            (tikz_to_manim(153.03, 95.14), tikz_to_manim(237.6, 97.24)),
            (tikz_to_manim(238, 136.14), tikz_to_manim(321.33, 138.17)),
            (tikz_to_manim(321, 165.14), tikz_to_manim(379, 166.75)),
            (tikz_to_manim(379.33, 186.14), tikz_to_manim(420.33, 187)),
            (tikz_to_manim(420.33, 203.14), tikz_to_manim(454.97, 203.29)),
            (tikz_to_manim(455.33, 216.14), tikz_to_manim(480.33, 215.67)),
            (tikz_to_manim(480.33, 226.14), tikz_to_manim(500.33, 226)),
            (tikz_to_manim(500.33, 236.14), tikz_to_manim(521.33, 236.08)),
        ]
        
        # Center the figure
        all_points = [A, B, C] + perp_tops + perp_bases
        center = np.mean(all_points, axis=0)
        shift_vec = -center + DOWN * 0.3
        
        A += shift_vec
        B += shift_vec
        C += shift_vec
        perp_tops = [p + shift_vec for p in perp_tops]
        perp_bases = [p + shift_vec for p in perp_bases]
        green_segments = [(s + shift_vec, e + shift_vec) for s, e in green_segments]
        
        # STEP 1: Draw main triangle with right-angle marker
        triangle = Polygon(A, B, C, color=RED, stroke_width=2.5)
        right_angle_C = self.create_right_angle_marker(C, B, A, size=0.15)
        
        self.play(Create(triangle), run_time=2)
        self.play(FadeIn(right_angle_C), run_time=0.5)
        self.wait(0.5)
        
        # STEP 2: Draw perpendiculars alternating blue/orange with right-angle markers
        for i in range(9):  # Changed from 12 to 10 (removed last 2 segments)
            # Blue perpendicular (from base to hypotenuse)
            blue_line = Line(perp_bases[i], perp_tops[i], color=BLUE, stroke_width=2)
            blue_marker = self.create_right_angle_marker(
                perp_tops[i], 
                perp_bases[i],
                perp_tops[i] + (B - A) * 0.05,
                size=0.07
            )
            
            self.play(Create(blue_line), run_time=0.8)
            self.play(FadeIn(blue_marker), run_time=0.3)
            
            # Orange perpendicular (vertical drop from same point)
            if i < 9:  # Changed from 11 to 9
                orange_line = Line(perp_tops[i], perp_bases[i+1], color=ORANGE, stroke_width=2)
            else:
                orange_line = Line(perp_tops[i], B, color=ORANGE, stroke_width=2)
            
            orange_marker = self.create_right_angle_marker(
                perp_bases[i+1] if i < 9 else B,
                perp_tops[i],
                perp_bases[i+1] + LEFT * 0.1 if i < 9 else B + LEFT * 0.1,
                size=0.08
            )
            
            self.play(Create(orange_line), run_time=0.8)
            self.play(FadeIn(orange_marker), run_time=0.3)
            self.wait(0.2)
        
        # STEP 3: Draw green horizontal segments with right-angle markers
        for start, end in green_segments:
            green_line = Line(start, end, color=GREEN, stroke_width=2)
            green_marker = self.create_right_angle_marker(
                start,
                end,
                start + UP * 0.1,
                size=0.07
            )
            
            self.play(Create(green_line), FadeIn(green_marker), run_time=0.5)
        
        self.wait(0.5)
        
        # STEP 4: Fade in all labels
        labels = VGroup()
        
        # Main triangle vertices
        label_A = MathTex("A", color=WHITE).scale(0.9).next_to(A, UP+LEFT, buff=0.15)
        label_B = MathTex("B", color=WHITE).scale(0.9).next_to(B, 2.5*RIGHT, buff=0.3)
        label_C = MathTex("C", color=WHITE).scale(0.9).next_to(C, DOWN+LEFT, buff=0.15)
        
        # Side labels
        label_a = MathTex("a", color="#0C94CF").scale(0.8).next_to((A+C)/2, LEFT, buff=0.4)
        label_b = MathTex("b", color=RED).scale(0.8).next_to((C+B)/2, DOWN, buff=0.4)
        label_c = MathTex("c", color=RED).scale(0.8).next_to((A+B)/2, UP+RIGHT, buff=0.4)
        
        # r labels (perpendiculars) - reduced to r_8
        r_labels = []
        r_positions = [
            (perp_bases[0] + perp_tops[0])/2 + LEFT*0.3,
            (perp_bases[1] + perp_tops[1])/2 + LEFT*0.25,
            (perp_bases[2] + perp_tops[2])/2 + LEFT*0.25,
            (perp_bases[3] + perp_tops[3])/2 + LEFT*0.2,
            (perp_bases[4] + perp_tops[4])/2 + LEFT*0.2,
            (perp_bases[5] + perp_tops[5])/2 + LEFT*0.2,
            (perp_bases[6] + perp_tops[6])/2 + LEFT*0.15,
            (perp_bases[7] + perp_tops[7])/2 + LEFT*0.15,  # Last r_8 position
        ]
        
        for i in range(8):  # Changed from 10 to 8
            color = BLUE if i % 2 == 0 else ORANGE
            r_label = MathTex(f"r_{{{i+1}}}", color=color).scale(0.5).move_to(r_positions[i])
            r_labels.append(r_label)
        
        # Ellipsis and r_n
        r_dots = MathTex("...", color="#0DEFEF").scale(0.7).next_to(B, 0.5*DOWN, buff=0.15)
        r_n = MathTex("r_n", color="#0DEFEF").scale(0.6).next_to(r_dots, RIGHT, buff=0.15)
        
        # d labels (base segments)
        d_labels = []
        d_positions = [
            (perp_bases[0] + perp_bases[1])/2 + DOWN*0.15,
            (perp_bases[1] + perp_bases[2])/2 + DOWN*0.15,
            (perp_bases[2] + perp_bases[3])/2 + DOWN*0.15,
            (perp_bases[3] + perp_bases[4])/2 + DOWN*0.15,
            (perp_bases[4] + perp_bases[5])/2 + DOWN*0.15,
            (perp_bases[5] + perp_bases[6])/2 + DOWN*0.15,
            (perp_bases[6] + perp_bases[7])/2 + DOWN*0.15,
        ]
        
        for i in range(7):
            d_label = MathTex(f"d_{{{i+1}}}", color=RED).scale(0.5).move_to(d_positions[i])
            d_labels.append(d_label)
        
        d_dots = MathTex("...", color=RED).scale(0.9).next_to(perp_bases[9], DOWN, buff=0.1)
        d_n = MathTex("d_n", color=RED).scale(0.6).next_to(d_dots, RIGHT, buff=0.5)
        
        # x and y labels (on hypotenuse segments)
        x_labels = []
        y_labels = []
        
        for i in range(7):
            x_label = MathTex(f"x_{{{i+1}}}", color=RED).scale(0.5).next_to(
                green_segments[i][1], 1.6*UP+1.5*LEFT, buff=0.4
            )
            y_label = MathTex(f"y_{{{i+1}}}", color=ORANGE).scale(0.5).next_to(
                green_segments[i][0], 1.8*UP+LEFT, buff=0.05
            )
            x_labels.append(x_label)
            y_labels.append(y_label)
        
        x_dots = MathTex("...", color=RED).scale(0.9).next_to(perp_tops[8], UP+RIGHT, buff=0.1).rotate(-60)
        y_dots = MathTex("...", color=ORANGE).scale(0.7).next_to(B, 0.5*UP, buff=0.3)
        x_n = MathTex("x_n", color=RED).scale(0.6).next_to(x_dots, RIGHT+0.3*DOWN, buff=0.20)
        y_n = MathTex("y_n", color=ORANGE).scale(0.6).next_to(y_dots, 0.5*RIGHT, buff=0.15)
        
        # Combine all labels
        labels.add(
            label_A, label_B, label_C,
            label_a, label_b, label_c,
            *r_labels, r_dots, r_n,
            *d_labels, d_dots, d_n,
            *x_labels, *y_labels, x_dots, y_dots, x_n, y_n
        )
    

        # STEP 4: Animate labels in sequence
        
        # 1. First animate A, B, C labels
        vertex_labels = VGroup(label_A, label_B, label_C)
        self.play(Write(vertex_labels), run_time=1)
        self.wait(0.3)
        
        # 2. Then animate a, b, c labels
        side_labels = VGroup(label_a, label_b, label_c)
        self.play(Write(side_labels), run_time=1)
        self.wait(0.3)
        
        # 3. Animate r_i labels in sequence
        r_group = VGroup(*r_labels, r_dots, r_n)
        for label in r_group:
            self.play(Write(label), run_time=0.5)
        self.wait(0.3)
        
        # 4. Animate d_i labels in sequence
        d_group = VGroup(*d_labels, d_dots, d_n)
        for label in d_group:
            self.play(Write(label), run_time=0.5)
        self.wait(0.3)
        
        # 5. Animate y_i labels in sequence
        y_group = VGroup(*y_labels, y_dots, y_n)
        for label in y_group:
            self.play(Write(label), run_time=0.5)
        self.wait(0.3)
        
        # 6. Finally animate x_i labels in sequence
        x_group = VGroup(*x_labels, x_dots, x_n)
        for label in x_group:
            self.play(Write(label), run_time=0.5)
        
        self.wait(0.5)

# ...existing code...
    
    def create_right_angle_marker(self, vertex, point1, point2, size=0.15):
        """Create a right-angle square marker at vertex"""
        v1 = point1 - vertex
        v2 = point2 - vertex
        
        if np.linalg.norm(v1) > 0:
            v1 = v1 / np.linalg.norm(v1)
        if np.linalg.norm(v2) > 0:
            v2 = v2 / np.linalg.norm(v2)
        
        corner1 = vertex + v1 * size
        corner2 = corner1 + v2 * size
        corner3 = vertex + v2 * size
        
        square = Polygon(
            vertex, corner1, corner2, corner3,
            color=WHITE,
            stroke_width=1,
            fill_opacity=0
        )
        
        return square