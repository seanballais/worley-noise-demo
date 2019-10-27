from random import randint
import math
import sys

from PIL import Image
import numpy as np


len_prev_printed_line:int = 0


def main():
    img_width, img_height, num_points, output_file = _get_args()
    img_grid = _create_img_grid(img_width, img_height)
    rand_points = _select_random_points(img_width, img_height, num_points)
    is_verbose = '--verbose' in sys.argv[1:]
    is_one_line_output = '--one-line-output' in sys.argv[1:]
    show_starting_points =  '--show-starting-points' in sys.argv[1:]

    for y in range(img_height):
        for x in range(img_width):
            bw_colour = _map_to_bw_colour(
                            _get_normalized_distance_from_nearest_point(
                                x, y, img_width, img_height, rand_points))
            # NOTE: Colour is in RGBA.
            img_grid[y][x] = tuple(([ round(bw_colour) ] * 3) + [ 255 ])

            if is_verbose:
                output = f'({x}, {y}): {img_grid[y][x]}'
                if is_one_line_output:
                    _one_line_print(output)
                else:
                    print(output)

    if is_one_line_output:
        _clear_line_printed()

    if show_starting_points:
        print('Random Points')
        print('-------------')
        for x, y in rand_points:
            print(f'({x},\t{y})')
            img_grid[y][x] = tuple([ 255, 0, 0, 255 ])

    Image.fromarray(np.array(img_grid).astype('uint8')).save(output_file)


def _get_args():
    img_width = int(sys.argv[1])
    img_height = int(sys.argv[2])
    num_points = int(sys.argv[3])
    output_file = sys.argv[4]

    return img_width, img_height, num_points, output_file


def _create_img_grid(img_width: int, img_height: int):
    grid = list()
    for _ in range(img_height):
        grid_row = list()
        for _ in range(img_width):
            grid_row.append(None)

        grid.append(grid_row)

    return grid


def _select_random_points(img_width: int, img_height: int, num_points: int):
    max_width = img_width - 1
    max_height = img_height - 1
    random_points = list()
    for _ in range(num_points):
        random_points.append(
            tuple([ randint(0, max_width), randint(0, max_height) ])
        )

    return random_points


def _get_normalized_distance_from_nearest_point(pixel_x: int,
                                                pixel_y: int,
                                                img_width: int,
                                                img_height: int,
                                                random_points: list):
    shortest_norm_dist = 1
    for point_x, point_y in random_points:
        x_dist = (pixel_x - point_x) / (img_width / 4)
        y_dist = (pixel_y - point_y) / (img_height / 4)
        norm_dist = math.sqrt(x_dist ** 2 + y_dist ** 2)

        shortest_norm_dist = min(norm_dist, shortest_norm_dist)

    return shortest_norm_dist


def _map_to_bw_colour(colour_val: float):
    # We should return this as inverted so that pixels nearer to a selected
    # point is closer to a white colour.
    return (1 - colour_val) * 255


def _one_line_print(text: str):
    global len_prev_printed_line
    _clear_line_printed()
    print(f'{text}', end='', flush=True)

    len_prev_printed_line = len(text)


def _clear_line_printed():
    global len_prev_printed_line
    print(f'\r{" " * len_prev_printed_line}\r', end='', flush=True)


if __name__ == '__main__':
    main()
