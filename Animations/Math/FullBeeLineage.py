# TITLE: Full Bee Lineage: Ancestry and Offspring
# DESCRIPTION: Visualizes the Fibonacci-based lineage of a honeybee, showing ancestral generations above and offspring below the current queen, with gender-based reproduction rules.
from manim import *

# Use config to set the background color to white
config.background_color = WHITE

class FullBeeLineage(MovingCameraScene):
    def construct(self):
        # ----------------------------------------------------
        # 1. Define Styles and Constants
        # ----------------------------------------------------
        # Invert colors for white background
        MALE_COLOR = BLUE_E  # Use a darker color for a white background
        FEMALE_COLOR = RED_E # Use a darker color for a white background
        TEXT_COLOR = BLACK
        RADIUS = 0.18
        V_SPACING = 0.8  # Vertical spacing between generations
        H_SPACING = 0.5  # Horizontal spacing for nodes

        # ----------------------------------------------------
        # 2. Helper function to create a bee circle with a gender label
        # ----------------------------------------------------
        def create_bee(gender, position):
            color = MALE_COLOR if gender == 'M' else FEMALE_COLOR
            label = Text(gender, font_size=18, color=TEXT_COLOR).move_to(position)
            circle = Circle(radius=RADIUS, color=color, fill_opacity=1).move_to(position)
            return VGroup(circle, label)

        # ----------------------------------------------------
        # 3. Setup the Central "Current Generation" (CG)
        # ----------------------------------------------------
        
        # Current Generation: A Female who is the Mother/Queen (F_CG)
        cg_pos = [0, 0, 0]
        f_cg = create_bee('F', cg_pos)
        cg_label = Text("Current Generation: 1", font_size=20, color=BLACK).next_to(f_cg, RIGHT * 0.5)
        CM_num = Tex("0", font_size=20, color=BLUE_E)
        CF_num = Tex("1", font_size=20, color=RED_E)
        ratio_text = Text("M:F = ", font_size=20, color=BLACK)
        ratio = VGroup(ratio_text, CM_num, Text(":", font_size=20, color=BLACK), CF_num).arrange(RIGHT, buff=0.1)   
        ratio.next_to(cg_label, 1.5*RIGHT, aligned_edge=UP)

        self.add(f_cg, cg_label, ratio)
        
        prev_nodes_up = [f_cg]
        prev_nodes_down = [f_cg]
        
        # Create a VGroup to collect all mobjects
        all_mobjects = VGroup(f_cg, cg_label)
        
        # ----------------------------------------------------
        # 4. ANCESTRAL LINEAGE (Tracing UPWARDS)
        # ----------------------------------------------------
        
        ancestral_structure = [
            (1, ['M', 'F']),
            (2, ['F', 'F', 'M']),
            (3, ['F', 'M', 'F', 'M', 'F']),
            (4, ['F', 'F', 'M', 'F', 'F', 'M', 'F', 'M'])
        ]
        
        self.play(self.camera.frame.animate.move_to([0, V_SPACING * 2, 0]).set(height=12))
        
        for gen_num, genders in ancestral_structure:
            curr_nodes = []
            y_pos = V_SPACING * gen_num
            total_width = (len(genders) - 1) * H_SPACING
            start_x = -total_width / 2

            for i, gender in enumerate(genders):
                x_pos = start_x + i * H_SPACING
                node = create_bee(gender, [x_pos, y_pos, 0])
                curr_nodes.append(node)
                self.add(node)
            
            all_mobjects.add(*curr_nodes)

            lines = []
            curr_idx = 0 
            
            for parent in prev_nodes_up:
                parent_pos = parent.get_center()
                
                # Get the gender from the second submobject (Text) in VGroup
                parent_gender = parent[1].text
                
                if parent_gender == 'F':
                    ancestor_1 = curr_nodes[curr_idx]
                    ancestor_2 = curr_nodes[curr_idx + 1]
                    lines.append(Arrow(ancestor_1.get_center(), parent_pos, buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
                    lines.append(Arrow(ancestor_2.get_center(), parent_pos, buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
                    curr_idx += 2
                elif parent_gender == 'M':
                    ancestor = curr_nodes[curr_idx]
                    lines.append(Arrow(ancestor.get_center(), parent_pos, buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
                    curr_idx += 1
            
            if lines:
                self.add(*lines)
                all_mobjects.add(*lines)

            fib_num = len(genders)
            M_num = len([g for g in genders if g == 'M'])
            F_num = len([g for g in genders if g == 'F'])
            
            gen_label = Text(f"Ancestors: {fib_num}", font_size=20, color=BLACK)
            
            # Create separate texts for better color control
            m_count = Text(str(M_num), font_size=20, color=BLUE_E)
            f_count = Text(str(F_num), font_size=20, color=RED_E)
            ratio_parts = VGroup(
                Text("M:F = ", font_size=20, color=BLACK),
                m_count,
                Text(":", font_size=20, color=BLACK),
                f_count
            ).arrange(RIGHT, buff=0.1)
            
            label_group = VGroup(gen_label, ratio_parts).arrange(RIGHT, buff=0.5)
            label_group.next_to(curr_nodes[-1], RIGHT * 0.7)
            self.add(label_group)
            all_mobjects.add(label_group)


            prev_nodes_up = curr_nodes

                # ----------------------------------------------------
        # 5. OFFSPRING GENERATION (Tracing DOWNWARDS) - Corrected Logic
        # ----------------------------------------------------
        
        # NOTE: This structure is now used with the new connection logic.
        offspring_structure = [
            (1, ['M']),
            (2, ['M', 'F']),
            (3, ['M', 'F', 'M']),
            (4, ['M', 'F', 'M', 'F', 'M']),
            (5, ['M', 'F', 'M', 'M', 'F', 'M', 'F', 'M'])
        ]

        self.play(self.camera.frame.animate.move_to([0, V_SPACING * -1, 0]).set(height=12))
        
        for gen_num, genders in offspring_structure:
            curr_nodes = []
            y_pos = -V_SPACING * gen_num
            total_width = (len(genders) - 1) * H_SPACING
            start_x = -total_width / 2

            for i, gender in enumerate(genders):
                x_pos = start_x + i * H_SPACING
                node = create_bee(gender, [x_pos, y_pos, 0])
                curr_nodes.append(node)
                self.play(FadeIn(node), run_time=0.2)
            
            all_mobjects.add(*curr_nodes)

            lines = []
            
            if gen_num == 1:
                # Gen 1 is produced by the central female (F_CG)
                for child in curr_nodes:
                    lines.append(Arrow(prev_nodes_down[0].get_center(), child.get_center(), buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
            else:
                child_idx = 0
                for parent in prev_nodes_down:
                    parent_pos = parent.get_center()
                    
                    # Get the gender from the second submobject (Text) in VGroup
                    parent_gender = parent[1].text
                    
                    # Male parent branches into two offspring (F and M)
                    if parent_gender == 'M':
                        if child_idx + 1 < len(curr_nodes):
                            child_m = curr_nodes[child_idx]
                            child_f = curr_nodes[child_idx + 1]
                            lines.append(Arrow(parent_pos, child_m.get_center(), buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
                            lines.append(Arrow(parent_pos, child_f.get_center(), buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
                            child_idx += 2
                    
                    # Female parent only connects to a male
                    elif parent_gender == 'F':
                        if child_idx < len(curr_nodes):
                            child_m = curr_nodes[child_idx]
                            lines.append(Arrow(parent_pos, child_m.get_center(), buff=RADIUS, color=BLACK, max_tip_length_to_length_ratio=0.1))
                            child_idx += 1
            
            if lines:
                self.play(*[Create(line) for line in lines], run_time=0.5)
                all_mobjects.add(*lines)
            
            # --- START: Updated labeling logic for offspring ---
            fib_num = len(genders)
            M_num = len([g for g in genders if g == 'M'])
            F_num = len([g for g in genders if g == 'F'])

            gen_label = Text(f"Offspring: {fib_num}", font_size=20, color=BLACK)
            
            # Create separate texts for better color control
            m_count = Text(str(M_num), font_size=20, color=BLUE_E)
            f_count = Text(str(F_num), font_size=20, color=RED_E)
            ratio_parts = VGroup(
                Text("M:F = ", font_size=20, color=BLACK),
                m_count,
                Text(":", font_size=20, color=BLACK),
                f_count
            ).arrange(RIGHT, buff=0.1)
            
            label_group = VGroup(gen_label, ratio_parts).arrange(RIGHT, buff=0.5)
            label_group.next_to(curr_nodes[-1], RIGHT * 0.7)
            
            self.play(FadeIn(label_group))
            all_mobjects.add(label_group)
            # --- END: Updated labeling logic ---
            
            prev_nodes_down = curr_nodes

        # ----------------------------------------------------
        # 6. Final Camera Fit using auto_zoom
        # ----------------------------------------------------
        self.play(self.camera.auto_zoom(all_mobjects, margin=1))
        self.wait(3)