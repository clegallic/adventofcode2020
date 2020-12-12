from functools import reduce

puzzle_input = [(line[:1], int(line[1:])) for line in open("input.txt").read().splitlines()]

TURN_L = lambda dir_x, dir_y: (dir_y, -dir_x) if abs(dir_x) == 1 else (dir_y, dir_x)
TURN_R = lambda dir_x, dir_y: (dir_y, dir_x) if abs(dir_x) == 1 else (-dir_y, dir_x)
ACTIONS = {"N": lambda dir_x, dir_y, value: ((dir_x, dir_y), (0, -value)),
           "S": lambda dir_x, dir_y, value: ((dir_x, dir_y), (0, value)),
           "E": lambda dir_x, dir_y, value: ((dir_x, dir_y), (value, 0)),
           "W": lambda dir_x, dir_y, value: ((dir_x, dir_y), (-value, 0)),
           "L": lambda dir_x, dir_y, value: (
               reduce(lambda acc, d: TURN_L(acc[0], acc[1]), list(range(value // 90)), (dir_x, dir_y)), (0, 0)),
           "R": lambda dir_x, dir_y, value: (
               reduce(lambda acc, d: TURN_R(acc[0], acc[1]), list(range(value // 90)), (dir_x, dir_y)), (0, 0)),
           "F": lambda dir_x, dir_y, value: ((dir_x, dir_y), (dir_x * value, dir_y * value))
           }
EAST_DIRECTION = (1, 0)
WAYPOINT_INITIAL_POSITION = (10, -1)


def main():
    result_part_one = find_manhattan_distance_part_one(puzzle_input)
    print(f"Part one : the Manhattan distance with ship's starting position is {result_part_one}")
    result_part_two = find_manhattan_distance_part_two(puzzle_input)
    print(f"Part two : the Manhattan distance with ship's starting position is {result_part_two}")


def apply_offset(position, offset):
    return position[0] + offset[0], position[1] + offset[1]


def find_manhattan_distance_part_one(instructions):
    ship_direction = EAST_DIRECTION
    ship_position = (0, 0)
    for instruction in instructions:
        action_result = ACTIONS[instruction[0]](ship_direction[0], ship_direction[1], instruction[1])
        ship_direction = action_result[0]
        ship_position = ship_position[0] + action_result[1][0], ship_position[1] + action_result[1][1]
    return abs(ship_position[0]) + abs(ship_position[1])


def find_manhattan_distance_part_two(instructions):
    ship_direction = EAST_DIRECTION
    waypoint_position = WAYPOINT_INITIAL_POSITION
    ship_position = (0, 0)
    for instruction in instructions:
        action = instruction[0]
        given_value = instruction[1]
        if action == "F":
            ship_to_waypoint_offset = waypoint_position[0] - ship_position[0], waypoint_position[1] - ship_position[1]
            ship_position = apply_offset(ship_position, [offset * given_value for offset in ship_to_waypoint_offset])
            waypoint_position = apply_offset(ship_position, ship_to_waypoint_offset)
        elif action in ["N", "S", "E", "W"]:
            action_result = ACTIONS[instruction[0]](ship_direction[0], ship_direction[1], instruction[1])
            waypoint_position = apply_offset(waypoint_position, action_result[1])
        else:
            for turn in list(range(given_value // 90)):
                ship_to_waypoint_offset = waypoint_position[0] - ship_position[0], waypoint_position[1] - ship_position[1]
                if action == "L":
                    waypoint_position = ship_position[0] + ship_to_waypoint_offset[1], ship_position[1] - ship_to_waypoint_offset[0]
                else:
                    waypoint_position = ship_position[0] - ship_to_waypoint_offset[1], ship_position[1] + ship_to_waypoint_offset[0]
    return abs(ship_position[0]) + abs(ship_position[1])


main()
