class Case:
    def __init__(self, case_num):
        self.optimal_positions = []
        self.errors = []
        self.status = True
        self.case_num = case_num

    def add_optimal_position(self, optimal_position):
        self.optimal_positions.append(optimal_position)

    def add_error(self, error):
        self.errors.append(error)
        self.status = False

    def print(self):
        print('CASE %d:' % self.case_num)

        if self.status:
            for optimal_position in self.optimal_positions:
                print('%d (%d, %d)' % (optimal_position['amount'], optimal_position['x'], optimal_position['y']))
        else:
            for error in self.errors:
                print(error)

        print()