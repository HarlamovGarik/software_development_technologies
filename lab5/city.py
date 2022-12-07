from case import Case


class City:
    MAX_LENGTH = 1000
    MAX_COFFEE_SHOPS = 105
    MAX_QUERIES = 20
    MAX_DISTANCE = 106

    def __init__(self):
        self.grid = []
        self.marks_grid = []
        self.cases = []
        self.errors = []
        self.coffee_shops = []
        self.coffee_shops_amount = 0
        self.distances_amount = 0
        self.case_num = 0
        self.width = 0
        self.length = 0
        self.case_started = False
        self.current_case = None

    def parse(self, name):
        file = open(name, 'r')
        line_num = 0
        coffee_shop_num = 1
        distance_num = 1

        while True:
            line = file.readline()

            if self.end_of_file(line):
                break

            if not line.strip():
                continue

            line = line.split()
            line_num += 1

            if self.case_started:
                if coffee_shop_num <= self.coffee_shops_amount:
                    coffee_shop_num += 1
                    if self.current_case.status and self.line_is_correct(line, 2, line_num):
                        self.add_coffee_shop(line, line_num)

                elif distance_num <= self.distances_amount:
                    distance_num += 1
                    if self.current_case.status and self.line_is_correct(line, 1, line_num):
                            optimal_position = self.get_optimal_position(line)
                            self.current_case.add_optimal_position(optimal_position)

                    if distance_num > self.distances_amount:
                        self.clear_variables()
                        coffee_shop_num = 1
                        distance_num = 1
            else:
                if self.line_is_correct(line, 4, line_num):
                        self.start_case(line)
                elif self.is_end(line):
                    break

    def start_case(self, line):
        self.width = int(line[0])
        self.length = int(line[1])
        self.coffee_shops_amount = int(line[2])
        self.distances_amount = int(line[3])
        self.fill_grid(self.grid)
        self.fill_grid(self.marks_grid)
        self.case_started = True
        self.case_num += 1
        self.current_case = Case(self.case_num)
        self.cases.append(self.current_case)

    def fill_grid(self, grid):
        del grid[:]
        for _ in range(0, self.length + 1):
            locations = []
            for _ in range(0, self.width + 1):
                locations.append(0)
            grid.append(locations)

    def line_is_correct(self, line, args_amount, line_num):
        if len(line) == args_amount:
            for arg in line:
                if not arg.isdigit():
                    self.errors.append('Error. All arguments must be Integer type. Line %d' % line_num)
                    return False
            return self.args_are_correct(line, line_num)
        else:
            self.errors.append('Error. City line must contain %d arguments. Line %d' % (args_amount, line_num))
            return False

    def args_are_correct(self, line, line_num):
        if len(line) == 4 and not self.is_end(line):
            if not 0 < int(line[0]) < self.MAX_LENGTH or not 0 < int(line[1]) < self.MAX_LENGTH:
                self.errors.append('Error. Coordinates (x, y) of the City must be > 0 and < %d. Line %d'
                                   % (self.MAX_LENGTH, line_num))
                return False
            elif not 0 < int(line[2]) < self.MAX_COFFEE_SHOPS:
                self.errors.append('Error. Number of Coffee shops must be > 0 and < %d. Line %d'
                                   % (self.MAX_COFFEE_SHOPS, line_num))
                return False
            elif not 0 < int(line[3]) < self.MAX_QUERIES:
                self.errors.append('Error. Number of Queries must be > 0 and < %d. Line %d'
                                   % (self.MAX_QUERIES, line_num))
                return False
            else:
                return True

        elif len(line) == 2:
            if not 0 < int(line[0]) <= len(self.grid[0]) or not 0 < int(line[1]) <= len(self.grid):
                self.errors.append('Wrong Coffee shop coordinates. Line %d' % line_num)
                self.current_case.status = False
                return False
            else:
                return True

        elif len(line) == 1:
            if not 0 < int(line[0]) < self.MAX_DISTANCE:
                self.errors.append('Error. Distance must be > 0 and < %d' % (self.MAX_DISTANCE, line_num))
                self.current_case.status = False
                return False
            else:
                return True

    def is_end(self, line):
        for arg in line:
            # print(arg, end=' ')
            if arg != '0':
                return False
        return True

    def add_coffee_shop(self, line, line_num):
        x = int(line[0])
        y = int(line[1])

        if self.grid[y][x] != -1:
            self.grid[y][x] = -1
            self.coffee_shops.append({'x': x, 'y': y})
        else:
            self.current_case.add_error('Error. Coffee shops can not have same coordinates. Line %d' % line_num)
            self.current_case.status = False

    def get_optimal_position(self, line):
        distance = int(line[0])
        self.mark_reachable_locations(distance)

        optimal_position = None
        max_reached = 0

        for i in range(1, self.length + 1):
            for j in range(1, self.width + 1):
                if self.marks_grid[i][j] > max_reached:
                    max_reached = self.marks_grid[i][j]
                    optimal_position = {'amount': max_reached, 'x': j, 'y': i}
                elif self.marks_grid[i][j] == max_reached != 0:
                    if j < optimal_position['x'] and i <= optimal_position['y']:
                        optimal_position = {'amount': max_reached, 'x': j, 'y': i}

        self.fill_grid(self.marks_grid)
        return optimal_position

    def mark_reachable_locations(self, distance):
        for coffee_shop in self.coffee_shops:
            x = coffee_shop['x']
            y = coffee_shop['y']

            for i in range(-distance, distance + 1):
                for j in range(abs(i) - distance, distance - abs(i) + 1):
                    try:
                        if self.grid[y + i][x + j] != -1:
                            if y + i > 0 and x + j > 0:
                                self.marks_grid[y + i][x + j] += 1
                            else:
                                raise IndexError
                    except IndexError:
                        pass

    def clear_variables(self):
        self.grid = []
        self.coffee_shops = []
        self.coffee_shops_amount = 0
        self.distances_amount = 0
        self.width = 0
        self.length = 0
        self.case_started = False
        self.current_case = None

    def end_of_file(self, line):
        if "" == line:
            if self.case_started:
                self.current_case.add_error('Error. Unexpected EOF')
            return True
        return False

    def print_result(self):
        for case in self.cases:
            case.print()

        for error in self.errors:
            print(error)