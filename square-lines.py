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
                                scale=40, num_lines=4, step_chance=0.4,
                                horizontal_chance=0.5):
    """
    Draws wandering vertical lines that do not touch or cross each other,
    and can move horizontally more than once.
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
    occupied_nodes = set()
    occupied_edges = set()

    start_columns = list(range(max_cols))
    random.shuffle(start_columns)

    line_count = 0

    for col_idx in start_columns:
        if line_count >= num_lines:
            break

        if (col_idx, 0) in occupied_nodes:
            continue

        current_col = col_idx
        current_row = 0
        occupied_nodes.add((current_col, current_row))

        steps = 0
        max_steps = max_rows * 2  # Allow some wandering

        while current_row < max_rows - 1 and steps < max_steps:
            steps += 1

            possible_moves = []

            # Always consider moving down
            down_pos = (current_col, current_row + 1)
            down_edge = tuple(sorted([(current_col, current_row), down_pos]))
            if down_pos not in occupied_nodes and down_edge not in occupied_edges:
                possible_moves.append(('down', down_pos, down_edge))

            # Consider moving left
            if current_col > 0:
                left_pos = (current_col - 1, current_row)
                left_edge = tuple(sorted([(current_col, current_row), left_pos]))
                if left_pos not in occupied_nodes and left_edge not in occupied_edges:
                    possible_moves.append(('left', left_pos, left_edge))

            # Consider moving right
            if current_col < max_cols - 1:
                right_pos = (current_col + 1, current_row)
                right_edge = tuple(sorted([(current_col, current_row), right_pos]))
                if right_pos not in occupied_nodes and right_edge not in occupied_edges:
                    possible_moves.append(('right', right_pos, right_edge))

            if not possible_moves:
                break  # No way to go

            # Decide direction
            if random.random() < horizontal_chance:
                move_options = [m for m in possible_moves if m[0] in ('left', 'right')]
                if not move_options:
                    move_options = [m for m in possible_moves if m[0] == 'down']
            else:
                move_options = [m for m in possible_moves if m[0] == 'down']
                if not move_options:
                    move_options = [m for m in possible_moves if m[0] in ('left', 'right')]

            direction, next_pos, edge = random.choice(move_options)

            # Draw the segment
            x1 = x_coords[current_col] * scale
            y1 = y_coords[current_row] * scale
            x2 = x_coords[next_pos[0]] * scale
            y2 = y_coords[next_pos[1]] * scale
            dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke='blue', stroke_width=2))

            # Update positions and occupancy
            occupied_nodes.add(next_pos)
            occupied_edges.add(edge)

            current_col, current_row = next_pos

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
