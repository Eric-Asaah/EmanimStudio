from manim import *

class WinLose(MovingCameraScene):
	def construct(self):
		import numpy as np
		# Parameters for horizontal spacing
		x_space = 2.0  # horizontal space between nodes
		y_space = 1.5  # vertical space for branches

		# Define points for TRY->WIN/LOSE pattern
		points = {
			"TRY1": np.array([0, 0, 0]),
			"WIN1": np.array([x_space, y_space, 0]),      # upper branch (success)
			"LOSE1": np.array([x_space, -y_space, 0]),    # lower branch (failure)
			"TRY2": np.array([2 * x_space, -y_space, 0]), # next try after losing
			"WIN2": np.array([3 * x_space, 0, 0]),        # upper branch from second try
			"LOSE2": np.array([3 * x_space, -2 * y_space, 0]),  # lower branch from second try
			"TRY3": np.array([4 * x_space, -2 * y_space, 0]),   # third try
			"WIN3": np.array([5 * x_space, -y_space, 0]),       # win from third try
			"LOSE3": np.array([5 * x_space, -3 * y_space, 0]),  # lose from third try
			"TRY4": np.array([6 * x_space, -3 * y_space, 0]),   # fourth try
			"WIN4": np.array([7 * x_space, -2 * y_space, 0]),   # win from fourth try
			"LOSE4": np.array([7 * x_space, -4 * y_space, 0]),  # lose from fourth try
			"TRY5": np.array([8 * x_space, -4 * y_space, 0]),   # fifth try
			"WIN5": np.array([9 * x_space, -3 * y_space, 0]),   # win from fifth try
			"LOSE5": np.array([9 * x_space, -5 * y_space, 0]),  # lose from fifth try
		}
		# Define the branching pattern
		edges = [
			("TRY1", "WIN1"),   # First try can lead to win
			("TRY1", "LOSE1"),  # First try can lead to lose
			("LOSE1", "TRY2"),  # After losing, try again
			("TRY2", "WIN2"),   # Second try can lead to win
			("TRY2", "LOSE2"),  # Second try can lead to lose
			("LOSE2", "TRY3"),  # After losing again, try third time
			("TRY3", "WIN3"),   # Third try can lead to win
			("TRY3", "LOSE3"),  # Third try can lead to lose
			("LOSE3", "TRY4"),  # After losing third time, try fourth time
            ("TRY4", "WIN4"),   # Fourth try can lead to win
            ("TRY4", "LOSE4"),  # Fourth try can lead to lose
            ("LOSE4", "TRY5"),  # After losing fourth time, try fifth time
            ("TRY5", "WIN5"),   # Fifth try can lead to win
            ("TRY5", "LOSE5"),  # Fifth try can lead to lose
		]

		# Set initial camera
		self.camera.frame.save_state()
		self.camera.frame.move_to(points["TRY1"])
		self.camera.frame.set(width=8)  # Start zoomed in

		# Keep track of created dots for connecting
		created = {}
		# Create and animate the root point
		for name in points:
			created[name] = Dot(points[name], radius=0.06, color=RED)  # Smaller dots

		# Add labels with fractions
		labels = {}
		for name in points:
			if "TRY" in name:
				num = "1"
				den = "1"
			elif "WIN" in name:
				num = "1"
				den = str(2 ** int(name[-1]))  # 1/2, 1/4, 1/8, etc.
			else:  # LOSE
				num = str(2 ** int(name[-1]) - 1)
				den = str(2 ** int(name[-1]))

			node_text = Text(name, font_size=20)
			fraction = MathTex(f"\\frac{{{num}}}{{{den}}}", font_size=16)
			label_group = VGroup(node_text, fraction).arrange(DOWN, buff=0.1)
			label_group.next_to(created[name], UP, buff=0.12)
			labels[name] = label_group

		# Function to determine animation speed based on node number
		def get_speed_multiplier(node_name):
			if any(x in node_name for x in ["5", "6", "7", "8", "9"]):
				number = int(node_name[-1])
				return max(0.1, 1.0 / (number - 4))  # Gradually speeds up
			return 1.0

		# Animate creation and branching with customizable waits for voiceover
		shown = set()
		arrows = []  # Store arrows for later
		
		for frm, to in edges:
			# Calculate speed multiplier based on node numbers
			speed = get_speed_multiplier(to)
			
			if frm not in shown:
				# Move camera to focus on the current action area
				focus_point = points[frm]
				self.play(
					self.camera.frame.animate.move_to(focus_point).set(width=8),
					run_time=1 * speed
				)
				
				# Create the starting point (TRY node)
				self.play(Create(created[frm]), run_time=1 * speed)
				self.wait(2 * speed)  # VOICEOVER: Describe the TRY situation
				self.play(FadeIn(labels[frm]), run_time=0.7 * speed)
				self.wait(1.5 * speed)  # VOICEOVER: Explain what this attempt represents
				shown.add(frm)

			# Move camera to include both current and next point
			midpoint = np.array([(points[frm][0] + points[to][0])/2,
							   (points[frm][1] + points[to][1])/2, 0])
			self.play(
				self.camera.frame.animate.move_to(midpoint).set(width=max(8, abs(points[to][0] - points[frm][0]) * 2)),
				run_time=0.8 * speed
			)

			# Create the destination point (WIN or LOSE node)
			self.play(Create(created[to]), run_time=1 * speed)
			self.wait(1 * speed)  # VOICEOVER: Introduce the possible outcome
			self.play(FadeIn(labels[to]), run_time=0.7 * speed)
			self.wait(1.5 * speed)  # VOICEOVER: Explain this outcome

			# Draw the arrow showing the progression
			arrow = Arrow(
				created[frm].get_center(),
				created[to].get_center(),
				buff=0.08,
				stroke_width=3,
				max_tip_length_to_length_ratio=0.15
			)
			arrows.append(arrow)
			self.play(GrowArrow(arrow), run_time=1 * speed)
			self.wait(1 * speed)  # VOICEOVER: Explain the transition

			# Extra wait for LOSE to TRY transitions
			if "LOSE" in frm and "TRY" in to:
				self.wait(1.5 * speed)  # VOICEOVER: Explain trying again after failure
			
			# Extra wait for WIN outcomes
			if "WIN" in to:
				self.wait(1.5 * speed)  # VOICEOVER: Celebrate or explain success
			
			shown.add(to)

		# Show any isolated points (not in edges)
		for name in points:
			if name not in shown:
				self.play(Create(created[name]), run_time=0.7)
				self.play(FadeIn(labels[name]), run_time=0.7)
				self.wait(1)  # VOICEOVER: Explain any isolated points