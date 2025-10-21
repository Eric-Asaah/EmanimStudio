from manim import *

class DopplerEffect(Scene):
    def construct(self):
        # Use compilable LaTeX fragments
        formula = MathTex(
            "f'", "=", "f", 
            r"\left(\frac{v \pm v_o}{v \pm v_s}\right)"
        )
        formula.shift(2*UP)
        formula.set_color_by_gradient(RED,BLUE,YELLOW)
        self.play(Write(formula))
        self.wait(1)
        
        # Target specific submobjects by index
        terms = [
            (0, r"\text{Apparent frequency } f'"),      # f' 
            (2, r"\text{Actual frequency } f_s"),       # f_s
            (3, r"\text{Fraction with speeds}")         # entire fraction
        ]
        
        for index, explanation_text in terms:
            target = formula[index]
            
            highlight = SurroundingRectangle(target, color=YELLOW, fill_opacity=0.2)
            explanation = MathTex(explanation_text, font_size=36).next_to(formula, DOWN, buff=1)
            arrow = Arrow(explanation.get_top(), target.get_bottom(), buff=0.15, color=YELLOW)
            
            self.play(Create(highlight), Write(explanation), Create(arrow))
            self.wait(1.5)
            self.play(FadeOut(highlight), FadeOut(explanation), FadeOut(arrow))
        
        # Create enlarged ratio
        Ratio = MathTex(
            r"\frac{v \pm v_o}{v \pm v_s}"
        ).next_to(formula, DOWN, buff=1).scale(2)  
        Ratio.set_color_by_gradient(RED,BLUE,YELLOW)
        self.play(ReplacementTransform(formula[3], Ratio), FadeOut(formula[0], formula[1], formula[2]))
        self.wait(2)    
        self.play(Ratio.animate.move_to(UP * 2))
        self.wait(1)
        
        # For individual speeds, create separate formulas
        v_formula = MathTex("v").move_to(ORIGIN)
        v_o_formula = MathTex("v_o").next_to(v_formula, RIGHT)
        v_s_formula = MathTex("v_s").next_to(v_o_formula, RIGHT)
        
        speed_group = VGroup(v_formula, v_o_formula, v_s_formula)
        speed_group.next_to(Ratio, DOWN, buff=2)
        
        explanations_speeds = [
            (v_formula, "Speed of sound"),
            (v_o_formula, "Speed of observer"),
            (v_s_formula, "Speed of source")
        ]
        
        for speed_obj, explanation_text in explanations_speeds:
            explanation = Text(explanation_text, font_size=24).next_to(speed_obj, DOWN)
            self.play(Write(speed_obj), Write(explanation))
            self.wait(1)
            self.play(FadeOut(speed_obj), FadeOut(explanation))
        
        self.play(FadeOut(Ratio))
        self.wait(2)