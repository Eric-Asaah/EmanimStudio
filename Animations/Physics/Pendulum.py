from manim import *
import numpy as np

class Pendulum(Scene):
    def construct(self):
        # Parameters
        length = 4
        max_angle = PI / 3  # 60 degrees
        num_cycles = 5

        # Pendulum parts
        pivot = UP * 2.5
        bob = Dot().shift(pivot + length * DOWN)
        rod = Line(pivot, bob.get_center())
        pendulum = VGroup(rod, bob)

        # --- Support bar at pivot ---
        support_bar = Line(pivot + LEFT*0.5, pivot + RIGHT*0.5, stroke_width=6, color=WHITE)

        # hatch marks (like optics mirrors shading)
        hatches = VGroup()
        for x in np.linspace(-0.45, 0.45, 9):  # 9 short diagonal lines
            hatch = Line(
                pivot + np.array([x, 0.05, 0]),  # top point
                pivot + np.array([x+0.1, 0.25, 0]),  # bottom point, shifted right
                stroke_width=2,
                color=GRAY
            )
            hatches.add(hatch)

        support = VGroup(support_bar, hatches)
        self.add(support)


        # Equilibrium line
        equilibrium = DashedLine(pivot, pivot + length * DOWN, dash_length=0.1, color=GRAY)
        self.add(equilibrium, pendulum)

        # Custom arc for θ (acute)
        def arc_between_lines():
            v1 = np.array([0, -1, 0])  # vertical down
            v2 = normalize(bob.get_center() - pivot)  # rod direction
            angle = np.arccos(np.clip(np.dot(v1, v2), -1, 1))
            if angle < 1e-3:
                return VGroup()
            return Arc(
                start_angle=-PI/2,
                angle=angle * np.sign(v2[0]),
                radius=0.5,
                arc_center=pivot,
                color=RED
            )

        angle_arc = always_redraw(arc_between_lines)
        self.add(angle_arc)


            # θ label that follows the arc
        def theta_label_func():
            arc = arc_between_lines()
            if isinstance(arc, VGroup) and len(arc) == 0:
                return VGroup()  # nothing when arc disappears
            return MathTex(r"\theta", color=RED).scale(0.5).move_to(
                arc.point_from_proportion(0.5)
                + 0.2 * normalize(arc.point_from_proportion(0.5) - pivot)
            )

        theta_label = always_redraw(theta_label_func)

        self.add(angle_arc, theta_label)


        # Force arrows --------------------
        # Weight W
        weight_arrow = always_redraw(
            lambda: Arrow(bob.get_center(), bob.get_center() + 1.0 * DOWN, buff=0, color=BLUE)
        )
        weight_label = always_redraw(
            lambda: MathTex("W", color=BLUE).scale(0.4).next_to(weight_arrow, DOWN, buff=0.1)
        )

        # Tension T (along rod)
        tension_arrow = always_redraw(
            lambda: Arrow(
                bob.get_center(),
                bob.get_center() + normalize(pivot - bob.get_center()) * 1.2,
                buff=0, color=GREEN
            )
        )
        tension_label = always_redraw(
            lambda: MathTex("T", color=GREEN).scale(0.4).next_to(tension_arrow, UP, buff=0.1)
        )

        # Components of T (final version only)
        def components():
            v_rod = normalize(pivot - bob.get_center())
            theta = np.arctan2(v_rod[0], v_rod[1])  # angle from vertical
            # Vertical component ∝ cosθ (upward)
            v_cos = UP * np.cos(theta)
            # Horizontal component ∝ |sinθ| (always inward)
            inward_dir = np.array([pivot[0] - bob.get_center()[0], 0, 0])
            inward_dir = normalize(inward_dir)
            v_sin = inward_dir * abs(np.sin(theta))  # always inward
            return v_cos, v_sin, theta

        # Tcosθ arrow (vertical)
        tcos_arrow = always_redraw(
            lambda: Arrow(
                bob.get_center(),
                bob.get_center() + components()[0] * 1.2,
                buff=0, color=ORANGE
            )
        )
        tcos_label = always_redraw(
            lambda: MathTex(r"T\cos\theta", color=ORANGE).scale(0.4).next_to(tcos_arrow, UP, buff=0.1)
        )

        # Tsinθ arrow (horizontal inward)
        tsin_arrow = always_redraw(
            lambda: Arrow(
                bob.get_center(),
                bob.get_center() + components()[1] * 1.2,
                buff=0, color=PURPLE
            )
        )
        tsin_label = always_redraw(
            lambda: MathTex(r"T\sin\theta", color=PURPLE).scale(0.4).next_to(tsin_arrow, RIGHT, buff=0.1)
        )

        self.add(weight_arrow, weight_label,
                 tension_arrow, tension_label,
                 tcos_arrow, tcos_label,
                 tsin_arrow, tsin_label)
        

        # --- Trace path of the bob ---
        trace = TracedPath(
            bob.get_center,
            stroke_color=DARK_BLUE,
            stroke_width=2
        )

        # make the trace fade out gradually
        def fade_trace(mob, dt):
            mob.set_stroke(opacity=0.6)  # fixed opacity trail
        trace.add_updater(fade_trace)

        self.add(trace)



                # --- Dashed path and labels (dynamic) ---
        base_arc = Arc(
            start_angle=-PI/2 - max_angle,
            angle=2 * max_angle,
            radius=length,
            arc_center=pivot,
            color=GRAY,
            stroke_width=2
        )
        path_arc = DashedVMobject(base_arc, num_dashes=40)  # no dash_length here

        left_end = base_arc.get_start()
        right_end = base_arc.get_end()
        mid_point = base_arc.point_from_proportion(0.5)

        label_left = MathTex(r"V=0, \; x=A").scale(0.5).next_to(left_end, LEFT+DOWN, buff=0.1)
        label_right = MathTex(r"V=0, \; x=-A").scale(0.5).next_to(right_end, RIGHT+DOWN, buff=0.1)
        label_mid = MathTex(r"V_{\max}, \; x=0").scale(0.5).next_to(mid_point, DOWN, buff=0.1)

        guide_group = VGroup(path_arc, label_left, label_right, label_mid)

        # Opacity updater: fades out as bob leaves
        def fade_with_position(mob):
            # normalized horizontal displacement
            x_disp = abs(bob.get_center()[0] - pivot[0]) / (length * np.sin(max_angle))
            alpha = np.clip(x_disp, 0, 1)  # extremes=1, center=0
            mob.set_opacity(alpha)

        guide_group.add_updater(fade_with_position)
        self.add(guide_group)

        


               # Pendulum motion
        def update_pendulum(mob, alpha):
            angle = max_angle * np.cos(TAU * alpha * num_cycles)  # multiply alpha by num_cycles
            new_bob_pos = pivot + length * np.array([np.sin(angle), -np.cos(angle), 0])
            bob.move_to(new_bob_pos)
            rod.put_start_and_end_on(pivot, new_bob_pos)

        # Animate continuously over num_cycles
        self.play(
            UpdateFromAlphaFunc(pendulum, update_pendulum),
            run_time=3 * num_cycles,
            rate_func=linear
        )
