class ClassStats:
    def __init__(self):
        self.inheritance_depth = 0
        self.child_count = 0
        self.inherited_methods_count = 0
        self.overridden_methods_count = 0
        self.visible_methods_count = 0
        self.private_methods_count = 0

    def set_statistic(self, args: []):
        self.inherited_methods_count, self.overridden_methods_count, self.visible_methods_count, self.private_methods_count = args

    def get_statistic(self):
        return [self.inheritance_depth, self.child_count, self.inherited_methods_count, self.overridden_methods_count,
                self.visible_methods_count, self.private_methods_count]


def class_stats_to_row(example_class: type, stats: ClassStats):
    _name = example_class.__name__
    values = stats.get_statistic()
    values.insert(0, _name)
    return [str(value) for value in values]