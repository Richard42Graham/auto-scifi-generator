import numpy as np
import svgwrite
import random

def create_square_grid(grid_size, spacing=1.0):
    x = np.arange(0, grid_size * spacing, spacing)
    y = np.arange(0, grid_size * spacing, spacing)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))
    return grid_points, x, y

def draw_wandering_vertical_lines(grid_points, x_coords, y_coords,
                                   filename="wandering_lines.svg",
                                   scale=40, num_lines=3, unique=True,
                                   step_chance=0.3):
    """
    Draws vertical lines that may wander left or right randomly as they descend.

    Parameters:
        step_chance: Probability (0–1) that a line moves left or right at each step.
    """
    dwg = svgwrite.Drawing(filename, size=(scale * len(x_coords), scale * len(y_coords)))

    # Draw base grid circles
  #  for x, y in grid_points:
  #      dwg.add(dwg.circle(center=(x * scale, y * scale), r=3, fill='black'))

    max_cols = len(x_coords)
    if unique:
        num_lines = min(num_lines, max_cols)
        col_indices = random.sample(range(max_cols), num_lines)
    else:
        col_indices = [random.randint(0, max_cols - 1) for _ in range(num_lines)]

    for col_idx in col_indices:
        current_col = col_idx

        for i in range(len(y_coords) - 1):
            y_start = y_coords[i]
            y_end = y_coords[i + 1]

            # Get current and next x positions
            x_start = x_coords[current_col]

            # Randomly decide to step left, right, or stay
            if random.random() < step_chance:
                step = random.choice([-1, 1])
                current_col = max(0, min(max_cols - 1, current_col + step))  # clamp to bounds

            x_end = x_coords[current_col]

            start = (x_start * scale, y_start * scale)
            end = (x_end * scale, y_end * scale)

            dwg.add(dwg.line(start=start, end=end, stroke='red', stroke_width=2))

    dwg.save()

# Example usage
if __name__ == "__main__":
    grid, x_vals, y_vals = create_square_grid(grid_size=70, spacing=1.0)
    draw_wandering_vertical_lines(grid, x_vals, y_vals,
                                  filename="wandering_lines_output.svg",
                                  num_lines=50,
                                  step_chance=0.4)
