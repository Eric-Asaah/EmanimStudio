# TITLE: Twin Primes Visualization
# DESCRIPTION: Animated highlighting of twin prime pairs in a prime number grid showing consecutive primes with difference of 2.
from manim import *


class TwinPrimesHighlight(Scene):
    def construct(self):
        # Generate primes up to 1000
        primes = self.get_primes(250)

        # Table dimensions
        cols = 8
        cell_size = 1

        # Make grid of primes
        table = VGroup()
        for i, p in enumerate(primes):
            row = i // cols
            col = i % cols
            num = Text(str(p), font_size=28)
            num.move_to([col * cell_size, -row * cell_size, 0])
            table.add(num)
        table.move_to(ORIGIN)
        self.play(Create(table))

        # Find twin primes
        twin_primes = [(a, b)
                       for a, b in zip(primes, primes[1:]) if b - a == 2]

        # Highlight twin primes one after another
        for a, b in twin_primes:
            a_mob = [m for m in table if m.text == str(a)][0]
            b_mob = [m for m in table if m.text == str(b)][0]
            HighlightedTwinPrimes = VGroup(a_mob, b_mob)

            self.play(SurroundingRectangle(HighlightedTwinPrimes, color=YELLOW, buff=0.1).animate.set_stroke(width=4),
                      run_time=2
                      )
            self.wait(0.3)

    def get_primes(self, n):
        """Sieve of Eratosthenes"""
        sieve = [True] * (n+1)
        sieve[0:2] = [False, False]
        for i in range(2, int(n**0.5)+1):
            if sieve[i]:
                sieve[i*i:n+1:i] = [False] * len(range(i*i, n+1, i))
        return [x for x in range(2, n+1) if sieve[x]]
