import svgwrite
from svgwrite import cm, mm
import random
import math
import numpy as np



def main(name_ofSVG):

    canvus_height = 100                       # max height of the "paper"
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
grid = create_square_grid(grid_size=5, spacing=1.0)
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


def render_svg(lines, add_circles_to_points, svg_output_file):
    dwg = svgwrite.Drawing(filename=svg_output_file, debug=True)
    # Rendering goes here
    toCm = 35.43307  # https://github.com/mozman/svgwrite/blob/master/doc/overview.rst

    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'),
                     rx=None, ry=None, fill='rgb(0,0,5)'))

    
   #print("({},{}) ({},{})".format(first_x, first_y, last_x, last_y))
    # for points in lines:
    #     polyline = dwg.polyline(id='vline', stroke='blue',
    #                             fill_opacity=0, stroke_width=10)
    #     for point_index in range((len(points))):
    #         point = points[point_index]
    #         first_x = point[0]
    #         first_y = point[1]
    #         polyline.points.append((first_x*toCm, first_y*toCm))
    #     dwg.add(polyline)

    # if add_circles_to_points:
    #     for points in lines:
    #         for point_index in range((len(points))):
    #             point = points[point_index]
    #             first_x = point[0]
    #             first_y = point[1]
    #             circle = dwg.circle(center=(first_x*toCm, first_y*toCm),
                 circle = dwg.circle(center=(grid),
                                     r='0.5cm', stroke='blue', stroke_width=3, fill='blue')
                 circle['class'] = 'class1 class2'
                 dwg.add(circle)
                 circle = dwg.circle(center=(first_x*toCm, first_y*toCm),
                                     r='0.3cm', stroke='black', stroke_width=3, fill='black')
                 circle['class'] = 'class1 class2'
                 dwg.add(circle)

                for x, y in grid_points:
                    polyline.points.append((x * scale, y * scale))
                    dwg.add(polyline)
    dwg.save()

     dwg.save()


if __name__ == '__main__':
    main('shapes.svg')
