from manim import *
import numpy as np
# Run with command line: manim -pql mtnr1b_curve.py SceneName


from manim import *
import numpy as np


class ConfidenceFan(Scene):
    def construct(self):
        # Make sure background is white
        self.camera.background_color = WHITE

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

        # Data minus initial point
        rem_x = data_x[initial_index + 1:]
        rem_y = data_y[initial_index + 1:]
        rem_lo = data_ci_lower[initial_index + 1:]
        rem_hi = data_ci_upper[initial_index + 1:]

        # ────────────────────────────────────────────────────────────────────

        # 1) Axes
        x_min, x_max = float(data_x.min()), float(data_x.max())
        y_min = float(data_ci_lower.min()) - 0.001  # a little padding
        y_max = float(data_ci_upper.max()) + 0.001

        axes = Axes(
            x_range=[x_min, x_max, (x_max - x_min) / 5],  # tick every ~1/5th of the span
            y_range=[y_min, y_max, (y_max - y_min) / 5],  # likewise
            x_length=10,
            y_length=6,
            axis_config={
                "color": BLACK,
                "include_ticks": True,
                "tick_size": 0.05,
            },
        ).to_edge(DOWN)

        # Compute data-space mid-X and mid-Y for each band
        x_mid = (x_min + x_max) / 2
        y_mid_pos = (0 + y_max) / 2  # center of the red band
        y_mid_neg = (0 + y_min) / 2  # center of the blue band

        # Convert those to scene coordinates
        center_pos = axes.coords_to_point(x_mid, y_mid_pos)
        center_neg = axes.coords_to_point(x_mid, y_mid_neg)

        # Band sizes in scene units:
        band_width = axes.x_length
        band_height_pos = axes.y_length * (y_max - 0) / (y_max - y_min)
        band_height_neg = axes.y_length * (0 - y_min) / (y_max - y_min)

        # Now build the rectangles at origin, then move them
        red_band = Rectangle(
            width=band_width,
            height=band_height_pos,
            fill_color=RED,
            fill_opacity=0.2,
            stroke_opacity=0,
        )
        red_band.move_to(center_pos)

        blue_band = Rectangle(
            width=band_width,
            height=band_height_neg,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_opacity=0,
        )
        blue_band.move_to(center_neg)

        self.play(
            Create(red_band),
            Create(blue_band),
            Create(axes),
            run_time=1
        )

        self.wait(3)

        # 2) Build but hide x-axis labels
        #    a) Get the tick values
        x_start, x_end, x_delta = axes.x_range
        tick_values = np.arange(x_start, x_end + 1e-8, x_delta)

        #    b) Create a Text label for each
        bottom_y = axes.get_bottom()[1]
        x_labels = VGroup()
        for val in tick_values:
            lbl = Text(f"{val:.2f}", font_size=24, color=BLACK)
            # Position at the same x, but below the axes box
            screen_pt = axes.coords_to_point(val, y_min)
            lbl.move_to([screen_pt[0], bottom_y - 0.3, 0])
            x_labels.add(lbl)

        x_labels.set_opacity(0)  # start invisible
        self.add(x_labels)

        # 2) Initial point + its CI bar
        x0 = data_x[initial_index]
        y0 = data_y[initial_index]
        ci0_lo = data_ci_lower[initial_index]
        ci0_hi = data_ci_upper[initial_index]

        # first point & bar in red:
        pt = Dot(axes.coords_to_point(x0, y0), color=RED)
        err = Line(
            axes.coords_to_point(x0, ci0_lo),
            axes.coords_to_point(x0, ci0_hi),
            color=RED
        )
        self.add(pt, err)
        self.wait(10)

        # 3) Build all blue dots & bars at the red point’s location:
        initial_pt = axes.coords_to_point(x0, y0)
        initial_lo = axes.coords_to_point(x0, ci0_lo)
        initial_hi = axes.coords_to_point(x0, ci0_hi)

        fan_dots = VGroup(*[
            Dot(initial_pt, color=BLACK)
            for _ in data_x[initial_index+1:]
        ])
        fan_bars = VGroup(*[
            Line(initial_lo, initial_hi, color=BLACK)
            for _ in data_x[initial_index+1:]
        ])

        # Add them behind the red ones
        self.add(fan_dots, fan_bars)

        # 4) Animate: fade out the red, move all blue into place simultaneously
        animations = []
        for dot, x, y in zip(fan_dots, rem_x, rem_y):
            animations.append(
                dot.animate.move_to(axes.coords_to_point(x, y))
            )
        for bar, x, lo, hi in zip(fan_bars, rem_x, rem_lo, rem_hi):
            animations.append(
                bar.animate.put_start_and_end_on(
                    axes.coords_to_point(x, lo),
                    axes.coords_to_point(x, hi),
                )
            )
        # at the same time, fade out the original red dot & bar
        animations.append(FadeOut(pt))
        animations.append(FadeOut(err))

        self.play(
            *animations,
            x_labels.animate.set_opacity(1),
            run_time=5
        )
        self.wait(50)
