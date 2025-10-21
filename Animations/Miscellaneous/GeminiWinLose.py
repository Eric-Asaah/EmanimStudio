from manim import *
import numpy as np

class WinLose(MovingCameraScene):
    """
    A Manim scene that animates a branching "Try -> Win/Lose" diagram.
    It visualizes multiple attempts, showing the path to winning or losing,
    and the decision to try again after a loss.
    Includes functionality to highlight specific nodes with rectangles.
    """
    def construct(self):
        # --- Configuration Parameters ---
        x_space = 2.0  # Horizontal space between nodes
        y_space = 1.5  # Vertical space for branches (e.g., for WIN/LOSE separation)
        
        # Highlight rectangle properties
        HIGHLIGHT_COLOR = YELLOW
        HIGHLIGHT_STROKE_WIDTH = 4
        HIGHLIGHT_BUFFER = 0.15 # Space between rectangle and mobject

        # --- Define Diagram Structure (Data) ---
        points = {
            "TRY1": np.array([0, 0, 0]),
            "WIN1": np.array([x_space, y_space, 0]),
            "LOSE1": np.array([x_space, -y_space, 0]),
            "TRY2": np.array([2 * x_space, -y_space, 0]),
            "WIN2": np.array([3 * x_space, 0, 0]),
            "LOSE2": np.array([3 * x_space, -2 * y_space, 0]),
            "TRY3": np.array([4 * x_space, -2 * y_space, 0]),
            "WIN3": np.array([5 * x_space, -y_space, 0]),
            "LOSE3": np.array([5 * x_space, -3 * y_space, 0]),
            "TRY4": np.array([6 * x_space, -3 * y_space, 0]),
            "WIN4": np.array([7 * x_space, -2 * y_space, 0]),
            "LOSE4": np.array([7 * x_space, -4 * y_space, 0]),
            "TRY5": np.array([8 * x_space, -4 * y_space, 0]),
            "WIN5": np.array([9 * x_space, -3 * y_space, 0]),
            "LOSE5": np.array([9 * x_space, -5 * y_space, 0]),
        }

        edges = [
            ("TRY1", "WIN1"),
            ("TRY1", "LOSE1"),
            ("LOSE1", "TRY2"),
            ("TRY2", "WIN2"),
            ("TRY2", "LOSE2"),
            ("LOSE2", "TRY3"),
            ("TRY3", "WIN3"),
            ("TRY3", "LOSE3"),
            ("LOSE3", "TRY4"),
            ("TRY4", "WIN4"),
            ("TRY4", "LOSE4"),
            ("LOSE4", "TRY5"),
            ("TRY5", "WIN5"),
            ("TRY5", "LOSE5"),
        ]

        # --- Initial Camera Setup ---
        self.camera.frame.save_state()
        self.camera.frame.move_to(points["TRY1"])
        self.camera.frame.set(width=8)

        # --- Create Manim Objects (Mobjects) ---
        created_nodes = {}
        for name in points:
            created_nodes[name] = Dot(points[name], radius=0.06, color=RED)

        labels = {}
        for name in points:
            if "TRY" in name:
                num = "1"
                den = "1"
            elif "WIN" in name:
                num = "1"
                den = str(2 ** int(name[-1]))
            else:  # LOSE
                num = str(2 ** int(name[-1]) - 1)
                den = str(2 ** int(name[-1]))

            node_text = Text(name, font_size=20)
            fraction = MathTex(f"\\frac{{{num}}}{{{den}}}", font_size=16)
            label_group = VGroup(node_text, fraction).arrange(DOWN, buff=0.1)
            label_group.next_to(created_nodes[name], UP, buff=0.12)
            labels[name] = label_group

        # --- Helper Function for Animation Speed ---
        def get_speed_multiplier(node_name):
            if any(x in node_name for x in ["5", "6", "7", "8", "9"]):
                number = int(node_name[-1])
                return max(0.1, 1.0 / (number - 4))
            return 1.0

        # --- Helper Function for Highlighting ---
        def highlight_mobject(mobject_to_highlight, highlight_duration, color=HIGHLIGHT_COLOR, stroke_width=HIGHLIGHT_STROKE_WIDTH, buff=HIGHLIGHT_BUFFER):
            """
            Creates and animates a surrounding rectangle around the given mobject.
            """
            highlight_rect = SurroundingRectangle(
                mobject_to_highlight,
                color=color,
                stroke_width=stroke_width,
                buff=buff
            )
            # Animate the creation, hold, and uncreation of the highlight rectangle.
            self.play(Create(highlight_rect), run_time=0.5)
            self.wait(highlight_duration)
            self.play(Uncreate(highlight_rect), run_time=0.5)

        # --- Animation Sequence ---
        shown_nodes = set()
        arrows = []

        for frm, to in edges:
            speed = get_speed_multiplier(to)
            
            if frm not in shown_nodes:
                focus_point = points[frm]
                self.play(
                    self.camera.frame.animate.move_to(focus_point).set(width=8),
                    run_time=1 * speed
                )
                
                # Animate creation of the starting node and its label
                self.play(Create(created_nodes[frm]), run_time=1 * speed)
                self.wait(0.5 * speed) # Short wait before highlight
                
                # Highlight the TRY node when it first appears
                # We group the dot and its label for a single highlight
                highlight_mobject(VGroup(created_nodes[frm], labels[frm]), 1.5 * speed) # VOICEOVER: Describe the TRY situation
                
                self.play(FadeIn(labels[frm]), run_time=0.7 * speed)
                self.wait(1.5 * speed) # VOICEOVER: Explain what this attempt represents
                shown_nodes.add(frm)

            midpoint = np.array([(points[frm][0] + points[to][0])/2,
                                 (points[frm][1] + points[to][1])/2, 0])
            self.play(
                self.camera.frame.animate.move_to(midpoint).set(width=max(8, abs(points[to][0] - points[frm][0]) * 2)),
                run_time=0.8 * speed
            )

            # Animate creation of the destination node and its label
            self.play(Create(created_nodes[to]), run_time=1 * speed)
            self.wait(0.5 * speed) # Short wait before highlight

            # Highlight WIN/LOSE nodes when they appear
            highlight_mobject(VGroup(created_nodes[to], labels[to]), 1.5 * speed) # VOICEOVER: Introduce the possible outcome

            self.play(FadeIn(labels[to]), run_time=0.7 * speed)
            self.wait(1.5 * speed) # VOICEOVER: Explain this specific outcome

            # Draw the arrow
            arrow = Arrow(
                created_nodes[frm].get_center(),
                created_nodes[to].get_center(),
                buff=0.08,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.append(arrow)
            self.play(GrowArrow(arrow), run_time=1 * speed)
            self.wait(1 * speed)  # VOICEOVER: Explain the transition

            # Extra wait and highlight for LOSE to TRY transitions
            if "LOSE" in frm and "TRY" in to:
                # Highlight both the LOSE node and the new TRY node, and the connecting arrow
                # This shows the "decision to try again"
                self.wait(0.5 * speed)
                highlight_mobject(VGroup(created_nodes[frm], created_nodes[to], arrow), 2.0 * speed, color=BLUE) # Highlight transition
                self.wait(1.5 * speed)  # VOICEOVER: Explain trying again after failure
                
            # Extra wait for WIN outcomes
            if "WIN" in to:
                self.wait(1.5 * speed)  # VOICEOVER: Celebrate or explain success
            
            shown_nodes.add(to)

        # --- Final Display (for any potentially isolated nodes) ---
        for name in points:
            if name not in shown_nodes:
                self.play(Create(created_nodes[name]), run_time=0.7)
                self.play(FadeIn(labels[name]), run_time=0.7)
                self.wait(1)  # VOICEOVER: Explain any isolated points or final state.
