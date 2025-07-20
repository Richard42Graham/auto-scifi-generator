import numpy as np
import svgwrite
import random

def create_square_grid(grid_size, spacing=1.0):
    x = np.arange(0, grid_size * spacing, spacing)
    y = np.arange(0, grid_size * spacing, spacing)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))
    return grid_points, x, y

def draw_non_overlapping_lines(grid_points, x_coords, y_coords,
                                filename="non_overlapping_lines.svg",
                                scale=40, num_lines=4, step_chance=0.4):
    """
    Draws wandering vertical lines that do not touch each other.
    """
    width = scale * len(x_coords)
    height = scale * len(y_coords)
    dwg = svgwrite.Drawing(filename, size=(width, height))

    # Draw black background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='black'))

    # Draw all grid points as small yellow circles
    for x, y in grid_points:
        dwg.add(dwg.circle(center=(x * scale, y * scale), r=2, fill='yellow'))

    max_cols = len(x_coords)
    max_rows = len(y_coords)
    occupied = set()  # Store (col_idx, row_idx)

    start_columns = list(range(max_cols))
    random.shuffle(start_columns)

    line_count = 0

    for col_idx in start_columns:
        if line_count >= num_lines:
            break

        if (col_idx, 0) in occupied:
            continue

        current_col = col_idx
        current_row = 0
        occupied.add((current_col, current_row))

        path = [(x_coords[current_col] * scale, y_coords[current_row] * scale)]

        for row_idx in range(1, max_rows):
            candidates = [current_col]
            if current_col > 0:
                candidates.append(current_col - 1)
            if current_col < max_cols - 1:
                candidates.append(current_col + 1)

            valid_moves = [c for c in candidates if (c, row_idx) not in occupied]

            if not valid_moves:
                break

            if random.random() < step_chance and len(valid_moves) > 1:
                next_col = random.choice([c for c in valid_moves if c != current_col])
            else:
                next_col = current_col if current_col in valid_moves else random.choice(valid_moves)

            start = (x_coords[current_col] * scale, y_coords[row_idx - 1] * scale)
            end = (x_coords[next_col] * scale, y_coords[row_idx] * scale)
            dwg.add(dwg.line(start=start, end=end, stroke='blue', stroke_width=2))

            occupied.add((next_col, row_idx))
            current_col = next_col
            current_row = row_idx

        line_count += 1

    dwg.save()

# Example usage
if __name__ == "__main__":
    grid_size = 70
    spacing = 1.0

    grid, x_vals, y_vals = create_square_grid(grid_size, spacing)
    draw_non_overlapping_lines(grid, x_vals, y_vals,
                                filename="no_touch_lines.svg",
                                num_lines=int(0.1 * grid_size ** 2),
                                step_chance=0.5)
