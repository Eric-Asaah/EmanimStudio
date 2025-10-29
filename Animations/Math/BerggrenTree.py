from manim import *
import numpy as np

class PythagoreanTreeRevised(Scene):
    def construct(self):
        """
        Animates the generation of the tree of primitive Pythagorean triples
        using the 3 Berggren (or Barning's) matrices.
        Revised to fit all elements on screen with proper spacing.
        """
        
        # Define the three Berggren matrices
        M1 = np.array([[ 1, -2,  2],
                       [ 2, -1,  2],
                       [ 2, -2,  3]])

        M2 = np.array([[ 1,  2,  2],
                       [ 2,  1,  2],
                       [ 2,  2,  3]])

        M3 = np.array([[-1,  2,  2],
                       [-2,  1,  2],
                       [-2,  2,  3]])
        
        matrices = [M1, M2, M3]

        # --- Configuration ---
        # Adjusted spacing and font size for each level to fit on screen better
        x_spacing = [3.5, 4.0, 4.5] # Horizontal distance between levels
        y_spacing = [2.7, 0.85, 0.25] # Vertical spread for new children
                                    # Increased significantly for level 1 and 2
        font_sizes = [40, 32, 26, 20] # Font size for levels 0, 1, 2, 3
                                      # Slightly reduced overall
        
        # Starting position for the root node - moved further left
        root_pos = LEFT * 6.5
        
        # Helper function to create a text node for a triple
        def create_triple_node(triple, position, font_size):
            triple_int = triple.astype(int)
            triple_str = f"({triple_int[0]},{triple_int[1]},{triple_int[2]})"
            return MathTex(triple_str, font_size=font_size).move_to(position)

        # --- Level 0 (Root) ---
        root_triple = np.array([3, 4, 5])
        root_node = create_triple_node(root_triple, root_pos, font_size=font_sizes[0])
        
        self.play(Write(root_node))
        self.wait(0.5)

        # Keep track of nodes and lines to group them later
        all_nodes = [root_node]
        all_lines = []
        
        # List of (triple_vector, node_mobject) for the current level
        current_level_nodes = [(root_triple, root_node)]

        # --- Generate Levels 1, 2, and 3 ---
        for level in range(3): # This loop generates 3 new levels (total 4 levels: 0, 1, 2, 3)
            next_level_nodes = []
            level_animations = []
            
            # Get config for the new level we are creating
            dx = x_spacing[level]
            dy = y_spacing[level]
            font_size = font_sizes[level + 1]
            
            # To manage vertical position for children
            # We need to know the 'midpoint' of the parent's children for vertical centering
            # The structure is fixed (M1=top, M2=middle, M3=bottom for each parent)
            
            # We will calculate the target Y position for each child based on the parent's Y
            # and the total spread for that parent's children
            
            
            # Iterate through parent nodes of the current level
            for parent_triple, parent_node in current_level_nodes:
                parent_center = parent_node.get_center()
                
                # Calculate the Y offsets for the three children from the parent's Y position
                # This ensures consistent spacing for each set of children
                y_offset_top = dy
                y_offset_mid = 0
                y_offset_bottom = -dy
                
                children_relative_y_offsets = [y_offset_top, y_offset_mid, y_offset_bottom]
                
                for i in range(3):
                    # Calculate the new triple using matrix multiplication
                    child_triple = matrices[i] @ parent_triple
                    
                    # Determine the child's position
                    child_x = parent_center[0] + dx
                    child_y = parent_center[1] + children_relative_y_offsets[i]
                    child_position = np.array([child_x, child_y, 0])
                    
                    # Create the new node and the line connecting it
                    child_node = create_triple_node(child_triple, child_position, font_size)
                    
                    # Adjust line endpoints slightly to meet the edge of the text Mobjects
                    line = Line(
                        parent_node.get_right(), 
                        child_node.get_left(), 
                        stroke_width=1.5, # Slightly thinner lines
                        color=GRAY
                    )
                    
                    # Add objects to lists for animation and tracking
                    level_animations.extend([Create(line), Write(child_node)])
                    next_level_nodes.append((child_triple, child_node))
                    all_nodes.append(child_node)
                    all_lines.append(line)

            # Animate the creation of this entire level at once
            self.play(*level_animations, run_time= max(1.0, 2.0 - level * 0.5) )
            self.wait(0.5)
            
            # The newly created level becomes the parent level for the next iteration
            current_level_nodes = next_level_nodes
        
        # --- Final Polish ---
        # Group all mobjects and scale/position them to fit nicely on screen
        all_mobjects = VGroup(*all_nodes, *all_lines)
        
        # Animate the final adjustment to fit everything neatly on screen
        # We need to ensure the entire group scales down and centers properly
        # Calculate the bounding box and scale to fit
        self.play(
            all_mobjects.animate.scale(0.65).move_to(ORIGIN) # More aggressive scaling
        )
        self.wait(2)