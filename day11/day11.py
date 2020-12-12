from functools import reduce

puzzle_input = [list(line) for line in open("input.txt").read().splitlines()]


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x:{self.x},y:{self.y})"


class Solver:
    EMPTY_SEAT = "L"
    FLOOR = "."
    OCCUPIED_SEAT = "#"
    ADJACENT_POSITIONS_OFFSET = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if (0, 0) != (x, y)]
    __rule_function = None
    __min_occupied_seats = None

    def __init__(self, initial_seats_states, debug=False):
        self.seats_states = initial_seats_states
        self.width = len(initial_seats_states[0])
        self.height = len(initial_seats_states)
        self.debug = debug
        self.debug and self.print_seats()

    def print_seats(self):
        [print("".join(line)) for line in self.seats_states]
        print()

    def find_end_up_adjacent_occupied_seats(self):
        self.__min_occupied_seats = 4
        self.__rule_function = self.adjacent_occupied_seats
        return self.find_end_up_occupied_seats()

    def find_end_up_visible_occupied_seats(self):
        self.__min_occupied_seats = 5
        self.__rule_function = self.visible_occupied_seats
        return self.find_end_up_occupied_seats()

    def find_end_up_occupied_seats(self):
        while self.launch_round():
            self.debug and self.print_seats()
        if self.debug:
            self.print_seats()
        return reduce(lambda acc, row: acc + row.count(self.OCCUPIED_SEAT), self.seats_states, 0)

    def launch_round(self):
        new_seats_states = []
        states_has_change = False
        for y, row in enumerate(self.seats_states):
            row_states = []
            for x in range(len(row)):
                p = Position(x, y)
                new_seat_state = self.new_seat_state(p)
                row_states.append(new_seat_state)
                states_has_change = states_has_change or new_seat_state != self.get_seat(p)
            new_seats_states.append(row_states)
        self.seats_states = new_seats_states
        return states_has_change

    def new_seat_state(self, p):
        if self.get_seat(p) == self.EMPTY_SEAT and self.__rule_function(p) == 0:
            return self.OCCUPIED_SEAT
        elif self.get_seat(p) == self.OCCUPIED_SEAT and self.__rule_function(p) >= self.__min_occupied_seats:
            return self.EMPTY_SEAT
        return self.get_seat(p)

    def get_seat(self, p):
        return self.seats_states[p.y][p.x]

    def adjacent_occupied_seats(self, p):
        return len([adj for adj in self.immediate_adjacent_positions(p) if self.get_seat(adj) == self.OCCUPIED_SEAT])

    def immediate_adjacent_positions(self, p):
        return [Position(p.x + offx, p.y + offy) for (offx, offy) in self.ADJACENT_POSITIONS_OFFSET if
                (self.is_valid_position(Position(p.x + offx, p.y + offy)))]

    def visible_occupied_seats(self, p):
        visible_occupied_seats = 0
        for offx, offy in self.ADJACENT_POSITIONS_OFFSET:
            if self.is_an_occupied_seat_visible(p, offx, offy):
                visible_occupied_seats += 1
        return visible_occupied_seats

    def is_an_occupied_seat_visible(self, p, offx, offy):
        current_position = Position(p.x + offx, p.y + offy)
        if self.is_valid_position(current_position):
            current_state = self.get_seat(current_position)
            if current_state == self.OCCUPIED_SEAT:
                return True
            elif current_state == self.EMPTY_SEAT:
                return False
            else:
                return self.is_an_occupied_seat_visible(current_position, offx, offy)
        else:
            return False

    def is_valid_position(self, p):
        return 0 <= p.x < self.width and 0 <= p.y < self.height


def main():
    result_part_one = Solver(puzzle_input, False).find_end_up_adjacent_occupied_seats()
    print(f"Part one : there are {result_part_one} occupied seats")
    result_part_two = Solver(puzzle_input, False).find_end_up_visible_occupied_seats()
    print(f"Part two : there are {result_part_two} occupied seats")


main()
