from manim import *
import numpy as np
# Run with command line: manim -pql mtnr1b_curve.py SceneName


from manim import *
import numpy as np


class ConfidenceFan(Scene):
    def construct(self):
        # ─── Replace these with your real data ─────────────────────────────
        data_x = np.array(
            [13.00, 9.00, 9.25, 9.50, 9.75, 10.00, 10.25, 10.50, 10.75, 11.00, 11.25,
             11.50, 11.75, 12.00, 12.25, 12.50, 12.75, 13.00, 13.25, 13.50,
             13.75, 14.00, 14.25, 14.50, 14.75, 15.00, 15.25, 15.50, 15.75,
             16.00, 16.25, 16.50, 16.75, 17.00, 17.25, 17.50, 17.75, 18.00,
             18.25, 18.50, 18.75, 19.00])    # your Xs
        data_y = np.array(
            [0, 0.007532740,  0.007382330,  0.008385310,  0.007386740,  0.006971780,
             0.007102110,  0.005825820,  0.005740130,  0.004448370,  0.003889780,
             0.003205570,  0.002342840,  0.002019450,  0.001446530,  0.001295140,
             0.000936986,  0.000597256, -0.000674283, -0.002176760, -0.001389860,
             -0.001679700, -0.002162340, -0.001850210, -0.003004550, -0.003108660,
             -0.002774170, -0.002829320, -0.003684980, -0.003926910, -0.003650060,
             -0.004783910, -0.004914630, -0.005609160, -0.005955670, -0.006494470,
             -0.007023340, -0.007628500, -0.007901860, -0.007126980, -0.006813000,
             -0.006541320])                   # your Ys
        standard_errs = np.array(
            [0.001, 0.002000370, 0.001735900, 0.001541250, 0.001380610, 0.001257170, 0.001165630,
             0.001094580, 0.001041960, 0.000994493, 0.000960708, 0.000933328, 0.000908012,
             0.000899905, 0.000893030, 0.000896142, 0.000898872, 0.000906281, 0.000912904,
             0.000923668, 0.000932713, 0.000945135, 0.000960848, 0.000972872, 0.000983258,
             0.000983494, 0.000980678, 0.000978036, 0.000973340, 0.000962176, 0.000952870,
             0.000943379, 0.000932186, 0.000924118, 0.000920206, 0.000908932, 0.000902919,
             0.000901835, 0.000915743, 0.000937548, 0.000982268, 0.001049480])

        data_ci_lower = data_y - standard_errs
        data_ci_upper = data_y + standard_errs
        initial_index = 0                                  # which point to show first
        # ────────────────────────────────────────────────────────────────────

        # 1) Axes
        x_min, x_max = float(data_x.min()), float(data_x.max())
        y_min = float(data_ci_lower.min()) - 0.01  # a little padding
        y_max = float(data_ci_upper.max()) + 0.01

        print(x_min)
        print(x_max)

        axes = Axes(
            x_range=[x_min, x_max, (x_max - x_min) / 5],  # tick every ~1/5th of the span
            y_range=[y_min, y_max, (y_max - y_min) / 5],  # likewise
            x_length=10,
            y_length=6,
            axis_config={"include_ticks": True},
        )

        self.play(Create(axes))

        # 2) Initial point + its CI bar
        x0 = data_x[initial_index]
        y0 = data_y[initial_index]
        ci0_lo = data_ci_lower[initial_index]
        ci0_hi = data_ci_upper[initial_index]
        pt = Dot(axes.coords_to_point(x0, y0), color=RED)
        err = Line(
            axes.coords_to_point(x0, ci0_lo),
            axes.coords_to_point(x0, ci0_hi),
            color=RED
        )
        self.play(FadeIn(err), FadeIn(pt))
        self.wait(1)

        # 3) Prepare all the final dots and their CI bars
        fan_dots = VGroup(*[
            Dot(axes.coords_to_point(x, y), color=BLUE)
            for x, y in zip(data_x, data_y)
        ])
        fan_bars = VGroup(*[
            Line(
                axes.coords_to_point(x, lo),
                axes.coords_to_point(x, hi),
                color=BLUE
            )
            for x, lo, hi in zip(data_x, data_ci_lower, data_ci_upper)
        ])

        # 4) Animate the fan-out: each dot + its error bar
        #    transform from the initial pt and err
        animations = []
        for d, b in zip(fan_dots, fan_bars):
            animations.append(TransformFromCopy(pt, d))
            animations.append(TransformFromCopy(err, b))

        self.play(
            FadeOut(err),
            LaggedStart(*animations, lag_ratio=0.05),
            FadeOut(pt),
            run_time=3
        )
        self.wait(2)
