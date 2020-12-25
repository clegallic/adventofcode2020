import re
import math
import numpy
from functools import reduce

puzzle_input = open("input.txt").read()
sea_monster = [line for line in open("sea_monster.txt").read().splitlines()]


def main():
    result_part_one = multiply_corner_tiles(puzzle_input)
    print(f"Part one : I get {result_part_one} if I multiply together the IDs of the four corner tiles")
    result_part_two = find_monster(puzzle_input)
    print(f"Part two : {result_part_two} '#' are not part of a sea monster")


def multiply_corner_tiles(p_input):
    tiles_matches = find_tiles_matches(p_input)
    return math.prod([tile_number for tile_number, matches in tiles_matches.items() if len(matches) == 2])


def find_monster(p_input):
    tiles = build_tiles(p_input)
    tiles_borders = build_tiles_borders(tiles)
    final_image = build_image(tiles, tiles_borders)
    count_monsters_in_image(final_image)
    for flip in ["FLIP_V", "FLIP_H", "NO_FLIP"]:
        for rot in ["ROT_CW", "ROT_CCW", "NO_ROT"]:
            nb_monsters = count_monsters_in_image(flip_rot_tile(final_image, flip, rot))
            if nb_monsters > 0:
                nb_sharp_in_image = reduce(lambda acc, line: acc + line.count("#"), final_image, 0)
                nb_sharp_in_monster = reduce(lambda acc, line: acc + line.count("#"), sea_monster, 0)
                return nb_sharp_in_image - nb_monsters * nb_sharp_in_monster


def find_tiles_matches(p_input):
    tiles = build_tiles(p_input)
    tiles_borders = build_tiles_borders(tiles)
    tiles_matches = dict()
    for tile_number, tile_borders in tiles_borders.items():
        tiles_matches[tile_number] = find_matching_tiles(tile_number, tile_borders, tiles_borders)
    return tiles_matches


def build_tiles(p_input):
    tiles = dict()
    for definition in p_input.split("\n\n"):
        tiles[int(re.match(r"Tile (\d+):", definition.splitlines()[0]).group(1))] = definition.splitlines()[1:]
    return tiles


def build_tiles_borders(tiles):
    tiles_borders = dict()
    for tile_number, pixels_lines in tiles.items():
        tiles_borders[tile_number] = build_tile_borders(pixels_lines)
    return tiles_borders


def build_tile_borders(pixels_lines):
    left, right = reduce(lambda acc, pixel_line: (acc[0] + pixel_line[0], acc[1] + pixel_line[-1]), pixels_lines,
                         ("", ""))
    return pixels_lines[0], right, pixels_lines[-1], left


def find_matching_tiles(tile_number, borders, tiles_borders):
    matching_tiles = list()
    for other_tile_number, other_tile_borders in tiles_borders.items():
        if tile_number != other_tile_number:
            for other_border_pos, other_tile_border in enumerate(other_tile_borders):
                flipped = False
                border_pos = borders.index(other_tile_border) if other_tile_border in borders else None
                if border_pos is None:
                    flipped = True
                    border_pos = borders.index(other_tile_border[::-1]) if other_tile_border[::-1] in borders else None
                if border_pos is not None:
                    matching_tiles.append((border_pos, other_border_pos, flipped, other_tile_number))
                    break
    return matching_tiles


def translate_loc(loc, x, y):
    if loc == "TOP":
        return x, y - 1
    elif loc == "BOTTOM":
        return x, y + 1
    elif loc == "RIGHT":
        return x + 1, y
    else:
        return x - 1, y


other_loc_flip_rot = {
    (0, 0): ("TOP", "FLIP_V", "NO_ROT"),
    (0, 1): ("TOP", "FLIP_H", "ROT_CCW"),
    (0, 2): ("TOP", "NO_FLIP", "NO_ROT"),
    (0, 3): ("TOP", "NO_FLIP", "ROT_CCW"),

    (1, 0): ("RIGHT", "FLIP_V", "ROT_CW"),
    (1, 1): ("RIGHT", "FLIP_H", "NO_ROT"),
    (1, 2): ("RIGHT", "NO_FLIP", "ROT_CW"),
    (1, 3): ("RIGHT", "NO_FLIP", "NO_ROT"),

    (2, 0): ("BOTTOM", "NO_FLIP", "NO_ROT"),
    (2, 1): ("BOTTOM", "NO_FLIP", "ROT_CCW"),
    (2, 2): ("BOTTOM", "FLIP_V", "NO_ROT"),
    (2, 3): ("BOTTOM", "FLIP_H", "ROT_CCW"),

    (3, 0): ("LEFT", "NO_FLIP", "ROT_CW"),
    (3, 1): ("LEFT", "NO_FLIP", "NO_ROT"),
    (3, 2): ("LEFT", "FLIP_V", "ROT_CW"),
    (3, 3): ("LEFT", "FLIP_H", "NO_ROT"),
}


def build_image(all_tiles, all_tiles_borders):
    image_data = dict()
    remaining_tiles_borders = all_tiles_borders.copy()
    first_tile_number, _ = remaining_tiles_borders.popitem()
    image_data[(0, 0)] = (first_tile_number, "NO_FLIP", "NO_ROT", all_tiles[first_tile_number])
    build_adjacents(0, 0, first_tile_number, all_tiles[first_tile_number], image_data, remaining_tiles_borders,
                    all_tiles_borders, all_tiles)
    return build_final_image(image_data)


def build_adjacents(x, y, tile_number, tile_data, image_data, remaining_tiles_borders, all_tiles_borders, all_tiles):
    adjacent_tiles = find_matching_tiles(tile_number, build_tile_borders(tile_data), remaining_tiles_borders)
    for border_pos, adj_tile_border_pos, adj_flipped, adj_tile_number in adjacent_tiles:
        if adj_tile_number in remaining_tiles_borders:
            # Remove the adjacent tile from remaining tiles
            remaining_tiles_borders.pop(adj_tile_number)
            # Get the adjacent tile location, flip and rotation
            loc, flip, rot = other_loc_flip_rot[(border_pos, abs(adj_tile_border_pos))]
            # Get adjacent tile location
            adj_tile_x, adj_tile_y = translate_loc(loc, x, y)
            adj_tile_data = all_tiles[adj_tile_number] if not adj_flipped \
                else flip_rot_tile(all_tiles[adj_tile_number], "FLIP_V", "NO_ROT") if adj_tile_border_pos in (3, 1) \
                else flip_rot_tile(all_tiles[adj_tile_number], "FLIP_H", "NO_ROT")
            # Modifiy adjacent tile data base on flip and rotation
            adj_tile_data = flip_rot_tile(adj_tile_data, flip, rot)
            image_data[(adj_tile_x, adj_tile_y)] = (adj_tile_number, flip, rot, adj_tile_data)  # Set image data
            build_adjacents(adj_tile_x, adj_tile_y, adj_tile_number, adj_tile_data, image_data, remaining_tiles_borders,
                            all_tiles_borders, all_tiles)


def flip_rot_tile(tile_data, flip, rot):
    new_tile_data = tile_data
    if flip == "FLIP_V":
        new_tile_data = list(reversed(tile_data))
    elif flip == "FLIP_H":
        new_tile_data = ["".join(list(reversed(tile_line))) for tile_line in tile_data]
    if rot == "ROT_CW":
        new_tile_data = ["".join(line) for line in numpy.rot90([list(line) for line in new_tile_data], -1)]
    elif rot == "ROT_CCW":
        new_tile_data = ["".join(line) for line in numpy.rot90([list(line) for line in new_tile_data])]
    return new_tile_data


def build_final_image(image_data):
    upper_left_coord = reduce(lambda acc, coord:
                              (acc[0] if acc[0] < coord[0] else coord[0], acc[1] if acc[1] < coord[1] else coord[1]),
                              image_data.keys())
    bottom_right_coord = reduce(lambda acc, coord:
                                (acc[0] if acc[0] > coord[0] else coord[0], acc[1] if acc[1] > coord[1] else coord[1]),
                                image_data.keys())
    final_image = list()
    for y in range(upper_left_coord[1], bottom_right_coord[1] + 1):
        for h in range(1, len(image_data[(upper_left_coord[0], y)][3]) - 1):
            line = ""
            for x in range(upper_left_coord[0], bottom_right_coord[0] + 1):
                line += image_data[(x, y)][3][h][1:-1]
            final_image.append(line)
    return final_image


def count_monsters_in_image(image):
    num_monsters_found = 0
    for top_y in range(0, len(image) - len(sea_monster)):
        for top_x in range(0, len(image[0]) - len(sea_monster[0])):
            monster_found = True
            for y in range(len(sea_monster)):
                for x in range(len(sea_monster[0])):
                    if sea_monster[y][x] == "#" and image[top_y + y][top_x + x] != "#":
                        monster_found = False
                        break
                if not monster_found:
                    break
            if monster_found:
                num_monsters_found += 1
    return num_monsters_found


main()
