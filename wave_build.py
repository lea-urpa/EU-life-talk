from manim import *
import numpy as np

# Run with command line: manim -pql wave_build.py SceneName
# High quality: manim -pqh wave_build.py WaveBuildComposite


class WaveDecomposition(Scene):
    def construct(self):
        # 1) Frequencies: fundamental + four harmonics
        freqs = [1, 2, 4, 8, 16]

        # 2) Main axes & combined waveform
        axes_main = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=3,
            axis_config={"color": WHITE},
        ).to_edge(UP)
        combined = axes_main.plot(
            lambda x: sum(np.sin(f * x) for f in freqs),
            color=YELLOW
        )

        self.play(Create(axes_main), Create(combined))
        self.wait(1)

        # 3) Small axes & individual component curves (all stacked at center)
        small_axes = VGroup(*[
            Axes(
                x_range=[0, 2 * PI, PI / 2],
                y_range=[-1.5, 1.5, 0.5],
                x_length=2,
                y_length=2,
                tips=False,
                axis_config={"color": BLUE},
            ).move_to(axes_main.get_center())
            for _ in freqs
        ])
        small_curves = VGroup(*[
            axes.plot(lambda x, f=f: np.sin(f * x), color=BLUE).move_to(axes_main.get_center())
            for axes, f in zip(small_axes, freqs)
        ])

        self.add(small_axes, small_curves)

        # 4) Compute final positions for each small axes
        #    (arrange them in a row at the bottom)
        small_axes.arrange(RIGHT, buff=0.5).to_edge(DOWN)
        target_positions = [ax.get_center() for ax in small_axes]

        # 5) Animate: fade out the big plot, move each small axes + curve
        animations = []
        for ax, curve, pos in zip(small_axes, small_curves, target_positions):
            animations.append(ax.animate.move_to(pos))
            animations.append(curve.animate.move_to(pos))

        self.play(
            FadeOut(axes_main),
            FadeOut(combined),
            *animations,
            run_time=3
        )
        self.wait(2)


class WaveBuildComposite(Scene):
    def construct(self):
        # 1) Frequencies: fundamental + first four “doubling” harmonics
        freqs = [1, 2, 4, 8]

        # 2) Top row: small axes (no arrowheads)
        top_axes = VGroup(*[
            Axes(
                x_range=[0, 2 * PI, PI/2],
                y_range=[-1.5, 1.5, 0.5],
                x_length=2,
                y_length=2,
                tips=False,
                axis_config={"color": BLUE},
            )
            for _ in freqs
        ])
        top_axes.arrange(RIGHT, buff=0.5).to_edge(UP)

        # Pause before anything appears
        self.wait(1)

        # Show the axes
        self.play(Create(top_axes), run_time=1)

        # Pause after axes
        self.wait(8)

        # 3) Draw each component one by one
        curves = []
        #for ax, f in zip(top_axes, freqs):
        #    curve = ax.plot(lambda x, f=f: np.sin(f * x), color=BLUE)
        #    curves.append(curve)
        #    self.play(Create(curve), run_time=1)
        #    self.wait(1)

        for i, (ax, f) in enumerate(zip(top_axes, freqs)):
            curve = ax.plot(lambda x, f=f: np.sin(f * x), color=BLUE)
            self.play(Create(curve), run_time=1)
            # longer pause after the first, shorter after the others
            self.wait(7 if i == 0 else 1.5)

        self.wait(1)

        # 4) Bottom: combined-wave axes
        axes_bottom = Axes(
            x_range=[0, 2 * PI, PI/2],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=3,
            tips=True,  # arrowheads on bottom plot
            axis_config={"color": WHITE},
        ).to_edge(DOWN)
        combined = axes_bottom.plot(
            lambda x: sum(np.sin(f * x) for f in freqs),
            color=YELLOW
        )

        # 5) Reveal combined plot
        self.play(Create(axes_bottom), run_time=3)
        self.play(Create(combined), run_time=2)
        self.wait(30)