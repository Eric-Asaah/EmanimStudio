from manim import *

class TwinPrimesHighlight(Scene):
    def construct(self):
        # Generate primes up to 500
        primes = self.get_primes(500)

        # Table dimensions
        cols = 9
        rows = (len(primes) + cols - 1) // cols

        # Build a grid of strings (not MathTex objects yet!)
        entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                idx = i * cols + j
                if idx < len(primes):
                    row_entries.append(str(primes[idx]))
                else:
                    row_entries.append("")  # empty cell if no prime
            entries.append(row_entries)

        # Create table with LaTeX entries and borders
        table = Table(
            entries,
            include_outer_lines=True,
            h_buff=1.0,
            v_buff=0.6,
            element_to_mobject=MathTex,  # convert strings → MathTex
        )

        table.scale(0.8)
        self.play(Create(table), run_time=3)

        # Find twin primes
        twin_primes = [(a, b) for a, b in zip(primes, primes[1:]) if b - a == 2]

        # Create one rectangle and reuse it
        first_a, first_b = twin_primes[0]
        a_mob = self.get_entry_mob(table, str(first_a))
        b_mob = self.get_entry_mob(table, str(first_b))
        highlight_rect = SurroundingRectangle(VGroup(a_mob, b_mob), color=YELLOW, buff=0.15)
        self.play(Create(highlight_rect))

        # Move rectangle around to next twin primes
        for a, b in twin_primes:
            a_mob = self.get_entry_mob(table, str(a))
            b_mob = self.get_entry_mob(table, str(b))

            # Background highlight rectangles for the twin primes
            a_bg = SurroundingRectangle(a_mob, color=WHITE, fill_opacity=1, buff=0.1)
            b_bg = SurroundingRectangle(b_mob, color=WHITE, fill_opacity=1, buff=0.1)
            a_color=a_mob.set_color(RED)
            b_color=b_mob.set_color(BLUE)

            # Change text color too
            self.play(
                Transform(highlight_rect, SurroundingRectangle(VGroup(a_mob, b_mob), color=YELLOW, buff=0.15)),
                 ReplacementTransform(a_mob, a_color), ReplacementTransform(b_mob, b_color),
                run_time=2
            )
            self.wait(1)

    def get_entry_mob(self, table, text):
        """Finds the MathTex mob in the table by its string content."""
        for mob in table.get_entries_without_labels():
            if mob.tex_string == text:
                return mob
        return None

    def get_primes(self, n):
        """Sieve of Eratosthenes"""
        sieve = [True] * (n+1)
        sieve[0:2] = [False, False]
        for i in range(2, int(n**0.5)+1):
            if sieve[i]:
                sieve[i*i:n+1:i] = [False] * len(range(i*i, n+1, i))
        return [x for x in range(2, n+1) if sieve[x]]
