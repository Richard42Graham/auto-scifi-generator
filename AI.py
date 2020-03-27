import svgwrite
from svgwrite import cm, mm
import random
import math


def main(name_ofSVG):

    canvus_height = 100              # max height of the "paper"

    lines = list()
    lines.append(generate_points(0, 0, 20, canvus_height, 2, 10, 2, 5))
    lines.append(generate_points(10, 0, 20, canvus_height, 2, 10, 2, 5))
    lines.append(generate_points(20, 0, 20, canvus_height, 2, 10, 2, 10))
    lines.append(generate_points(30, 0, 20, canvus_height, 2, 10, 2, 10))
    lines.append(generate_points(40, 0, 20, canvus_height, 2, 10, 2, 10))
    render_svg(lines, name_ofSVG)


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
    x_new = random.randint(line_boundry_startX,
                           (line_boundry_startX + line_boundry_width))
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


def render_svg(lines, svg_output_file):
    dwg = svgwrite.Drawing(filename=svg_output_file, debug=True)
    # Rendering goes here

    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'),
                     rx=None, ry=None, fill='rgb(0,0,5)'))

    vlines = dwg.add(dwg.g(id='vline', stroke='blue', stroke_width=20))

    for points in lines:
        for point_index in range((len(points) - 1)):
            point = points[point_index]
            first_x = point[0]
            first_y = point[1]

            point = points[point_index + 1]
            last_x = point[0]
            last_y = point[1]

            print("({},{}) ({},{})".format(first_x, first_y, last_x, last_y))

            # Polyline.points.append( point )

            vlines.add(dwg.line(start=(first_x*cm, first_y*cm),
                                end=(last_x*cm, last_y*cm)))
            #circle =dwg.circle(center=(first_x*cm, first_y*cm), r='0.5cm', stroke='blue', stroke_width=3,fill='blue')
            #circle['class'] = 'class1 class2'
            #dwg.add(circle)

            #circle =dwg.circle(center=(first_x*cm, first_y*cm), r='0.4cm', stroke='black', stroke_width=3,fill='black')
            #circle['class'] = 'class1 class2'
            #dwg.add(circle)

    dwg.save()


if __name__ == '__main__':
    main('shapes.svg')
