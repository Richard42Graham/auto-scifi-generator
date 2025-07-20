import svgwrite
from svgwrite import cm, mm
import random
import math
import numpy as np



def main(name_ofSVG):

    canvus_height = 10                       # max height of the "paper"
    Numbers_of_Lines = 30                     # 10
    add_circles_to_points =  True #False
    lines = list()
    I = 0                                     # lines start at X = 0
    while I < Numbers_of_Lines:
        #lines.append(generate_points(    0, 0, 20, canvus_height, 2, 10, 2, 5))
        lines.append(generate_points((I*10), 0, 20, canvus_height, 2, 10, 2, 5))
        I += 1

    render_svg(lines, add_circles_to_points, name_ofSVG)

def create_square_grid(grid_size, spacing=1.0):
    """
    Create an array of points in a square grid.

    Parameters:
        grid_size (int): Number of points along one axis (grid_size x grid_size total points)
        spacing (float): Distance between adjacent points

    Returns:
        numpy.ndarray: Array of shape (grid_size**2, 2) with (x, y) coordinates
    """
    x = np.arange(0, grid_size * spacing, spacing)
    y = np.arange(0, grid_size * spacing, spacing)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))
    return grid_points

# Example usage:
grid = create_square_grid(grid_size=50, spacing=1.0)
print(grid)




def generate_points(
        line_boundry_startX,
        line_boundry_starty,
        line_boundry_width,
        line_boundry_height,
        min_line_lenght,
        max_line_lenght,
        min_straight_line_lenght,
        max_straight_line_lenght):

    points = list()                 # array to store line points.
    # end of segment could start at any point in bound
    x_new = int(random.randint(int(line_boundry_startX), int((line_boundry_startX + line_boundry_width))))
    y_new = line_boundry_starty

    x_current = 0
    y_current = 0

    # while the line height is not the hight of the "paper" contineu drawing the line
    while(y_new <= line_boundry_starty + line_boundry_height):

        x_current = x_new
        y_current = y_new

        points.append([x_new, y_new])

        if len(points) % 2 != 0:

            x_new = get_next_x(min_line_lenght, max_line_lenght, x_current)
            while x_new < line_boundry_startX or x_new > line_boundry_startX + line_boundry_width:
                x_new = get_next_x(min_line_lenght, max_line_lenght, x_current)

            y_new = y_current + abs(x_current - x_new)
        else:
            x_new = x_current
            y_new = y_current + random.randint(min_straight_line_lenght,
                                               max_straight_line_lenght)

    return points


def get_next_x(min_line_lenght, max_line_lenght, x_current):
    line_lenght = random.randint(min_line_lenght, max_line_lenght)
    xy_lenght = math.sqrt((line_lenght*line_lenght) / 2)

    if random.randint(0, 1) == 1:
        x_new = x_current + xy_lenght
    else:
        x_new = x_current - xy_lenght
    return x_new


def draw_svg_grid(grid_points, filename="grid.svg", scale=20, circle_radius=3):
    """
    Draws an SVG with a circle at each grid point.

    Parameters:
        grid_points (ndarray): Array of shape (N, 2) with (x, y) coordinates.
        filename (str): Output SVG file name.
        scale (int): Multiplier to scale grid points into pixels.
        circle_radius (int): Radius of each circle in pixels.
    """
    # Determine canvas size based on max coordinates
    max_x = np.max(grid_points[:, 0]) * scale + scale
    max_y = np.max(grid_points[:, 1]) * scale + scale
    dwg = svgwrite.Drawing(filename, size=(max_x, max_y))

    for point in grid_points:
        px = point[0] * scale
        py = point[1] * scale
        dwg.add(dwg.circle(center=(px, py), r=circle_radius, fill='black'))

# Draw polyline connecting points in order
    polyline = dwg.polyline(fill='none', stroke='blue', stroke_width=2)

    for x, y in grid_points:
        polyline.points.append((x * scale, y * scale))

    dwg.add(polyline)
    dwg.save()


if __name__ == '__main__':
    grid_points = create_square_grid(grid_size=60, spacing=1.0)
    draw_svg_grid(grid_points, filename="grid_circles.svg", scale=30, circle_radius=4)
