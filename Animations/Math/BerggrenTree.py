from manim import *

class FullBeeLineage(MovingCameraScene):
    def construct(self):
        # ----------------------------------------------------
        # 1. Define Styles and Constants
        # ----------------------------------------------------
        MALE_COLOR = BLUE_B # Drones (Haploid)
        FEMALE_COLOR = RED_B # Queens/Workers (Diploid)
        TEXT_COLOR = WHITE
        RADIUS = 0.1
        V_SPACING = 0.8  # Vertical spacing between generations
        H_SPACING = 0.5  # Horizontal spacing for nodes

        # ----------------------------------------------------
        # 2. Helper function to create a bee circle with a gender label
        # ----------------------------------------------------
        def create_bee(gender, position):
            color = MALE_COLOR if gender == 'M' else FEMALE_COLOR
            label = Text(gender, font_size=18, color=TEXT_COLOR).move_to(position)
            circle = Circle(radius=RADIUS, color=color, fill_opacity=1).move_to(position)
            # The Text object is the second sub-mobject in the VGroup
            return VGroup(circle, label)

        # ----------------------------------------------------
        # 3. Setup the Central "Current Generation" (CG)
        # ----------------------------------------------------
        
        # Current Generation: A Female who is the Mother/Queen (F_CG)
        cg_pos = [0, 0, 0]
        f_cg = create_bee('F', cg_pos)
        cg_label = Text("Current Generation (F)", font_size=24, color=YELLOW).next_to(f_cg, LEFT * 0.5 + UP * 0.5)
        
        self.add(f_cg, cg_label)
        
        prev_nodes_up = [f_cg]
        prev_nodes_down = [f_cg]
        
        # ----------------------------------------------------
        # 4. ANCESTRAL LINEAGE (Tracing UPWARDS)
        # ----------------------------------------------------
        ancestral_structure = [
            (1, ['M', 'F']),
            (2, ['F', 'F', 'M']),
            (3, ['F', 'M', 'F', 'M', 'F']),
            (4, ['F', 'F', 'M', 'F', 'F', 'M', 'F', 'M']),
            (5, ['F', 'F', 'M', 'F', 'F', 'M', 'F', 'M', 'F', 'F', 'M', 'F', 'F', 'M', 'F', 'M'])
        ]
        
        self.play(self.camera.frame.animate.shift(UP * V_SPACING * 3).set(height=10), run_time=1)
        
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

            lines = []
            curr_idx = 0 
            
            for parent in prev_nodes_up:
                parent_pos = parent.get_center()
                
                # FIX: Access the Text sub-mobject at index 1 of the VGroup
                if parent[1].get_text() == 'F':
                    ancestor_1 = curr_nodes[curr_idx]
                    ancestor_2 = curr_nodes[curr_idx + 1]
                    lines.append(Arrow(ancestor_1.get_center(), parent_pos, buff=RADIUS, color=GRAY, max_tip_length_to_length_ratio=0.1))
                    lines.append(Arrow(ancestor_2.get_center(), parent_pos, buff=RADIUS, color=GRAY, max_tip_length_to_length_ratio=0.1))
                    curr_idx += 2
                    
                # FIX: Access the Text sub-mobject at index 1 of the VGroup
                elif parent[1].get_text() == 'M':
                    ancestor = curr_nodes[curr_idx]
                    lines.append(Arrow(ancestor.get_center(), parent_pos, buff=RADIUS, color=GRAY, max_tip_length_to_length_ratio=0.1))
                    curr_idx += 1
            
            self.add(*lines)
            fib_num = len(genders)
            label_text = f"Ancestors (Fib: {fib_num})"
            gen_label = Text(label_text, font_size=20, color=BLUE_A).next_to(curr_nodes[-1], RIGHT * 0.7)
            self.add(gen_label)

            prev_nodes_up = curr_nodes

        # ----------------------------------------------------
        # 5. OFFSPRING GENERATION (Tracing DOWNWARDS)
        # ----------------------------------------------------
        offspring_structure = [
            (1, ['M']),
            (2, ['M', 'F']),
            (3, ['M', 'F', 'M']),
            (4, ['M', 'F', 'M', 'F', 'M']),
            (5, ['M', 'F', 'M', 'M', 'F', 'M', 'F','M'])
        ]

        self.play(self.camera.frame.animate.move_to(ORIGIN).set(height=12), run_time=1)
        self.wait(1)

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

            lines = []
            
            if gen_num == 1:
                # FIX: Add the Arrow creation to the lines list
                for child in curr_nodes:
                    lines.append(Arrow(prev_nodes_down[0].get_center(), child.get_center(), buff=RADIUS, color=GRAY, max_tip_length_to_length_ratio=0.1))
            else:
                # FIX: Access the Text sub-mobject at index 1 of the VGroup
                f_indices_prev = [i for i, node in enumerate(prev_nodes_down) if node[1].get_text() == 'F']
                
                node_chunks = [curr_nodes[i:i + 2] for i in range(0, len(curr_nodes), 2)]
                
                current_chunk_index = 0
                for parent_index in f_indices_prev:
                    if current_chunk_index < len(node_chunks):
                        parent_node = prev_nodes_down[parent_index]
                        for child in node_chunks[current_chunk_index]:
                            lines.append(Arrow(parent_node.get_center(), child.get_center(), buff=RADIUS, color=GRAY, max_tip_length_to_length_ratio=0.1))
                        current_chunk_index += 1

            # FIX: Only call self.play if there are animations
            if lines:
                self.play(*[Create(line) for line in lines], run_time=0.5)

            fib_num = len(genders)
            label_text = f"Offspring (Fib: {fib_num})"
            gen_label = Text(label_text, font_size=20, color=RED_A).next_to(curr_nodes[-1], RIGHT * 0.7)
            self.play(FadeIn(gen_label))
            
            prev_nodes_down = curr_nodes
            
        self.wait(3)

