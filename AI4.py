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
                                scale=40, num_lines=4,
                                diagonal_chance=0.5):
    """
    Draws wandering lines that move diagonally or straight down,
    without overlapping or crossing, on a black background.
    """
    width = scale * len(x_coords)
    height = scale * len(y_coords)
    dwg = svgwrite.Drawing(filename, size=(width, height))

    # Draw black background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='black'))

    # Draw grid points
    #for x, y in grid_points:
    #    dwg.add(dwg.circle(center=(x * scale, y * scale), r=2, fill='yellow'))

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

        while current_row < max_rows - 1:
            possible_moves = []

            # Straight down
            down_pos = (current_col, current_row + 1)
            down_edge = tuple(sorted([(current_col, current_row), down_pos]))
            if down_pos not in occupied_nodes and down_edge not in occupied_edges:
                possible_moves.append(('down', down_pos, down_edge))

            # Down-left
            if current_col > 0:
                dl_pos = (current_col - 1, current_row + 1)
                dl_edge = tuple(sorted([(current_col, current_row), dl_pos]))
                if dl_pos not in occupied_nodes and dl_edge not in occupied_edges:
                    possible_moves.append(('down_left', dl_pos, dl_edge))

            # Down-right
            if current_col < max_cols - 1:
                dr_pos = (current_col + 1, current_row + 1)
                dr_edge = tuple(sorted([(current_col, current_row), dr_pos]))
                if dr_pos not in occupied_nodes and dr_edge not in occupied_edges:
                    possible_moves.append(('down_right', dr_pos, dr_edge))

            if not possible_moves:
                break

            # Choose direction
            if random.random() < diagonal_chance:
                move_options = [m for m in possible_moves if m[0] in ('down_left', 'down_right')]
                if not move_options:
                    move_options = [m for m in possible_moves if m[0] == 'down']
            else:
                move_options = [m for m in possible_moves if m[0] == 'down']
                if not move_options:
                    move_options = [m for m in possible_moves if m[0] in ('down_left', 'down_right')]

            direction, next_pos, edge = random.choice(move_options)

            # Draw line
            x1 = x_coords[current_col] * scale
            y1 = y_coords[current_row] * scale
            x2 = x_coords[next_pos[0]] * scale
            y2 = y_coords[next_pos[1]] * scale
            dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke='yellow', stroke_width=2))

            # Update
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
                                diagonal_chance=0.3),


