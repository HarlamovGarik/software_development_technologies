import inspect
import sys
from __ClassStats__ import ClassStats


class MetricCounter:
    def __init__(self, __print=False):
        self.__cached_inheritance_depths: dict[type, int] = {}
        self.classes_stats: dict[type, ClassStats] = {}
        self.__print = __print

    def vprint(self, *args):
        if self.__print:
            print(*args)

    def count_class(self, example_class: type) -> ClassStats:
        class_metrics = ClassStats()
        class_metrics.child_count = len(example_class.__subclasses__())
        class_metrics.inheritance_depth = self.count_class_inheritance_depth(example_class)
        self.count_props(example_class, class_metrics)
        self.classes_stats[example_class] = class_metrics
        return class_metrics

    def count_class_inheritance_depth(self, example_class: type) -> int:
        if example_class.__base__ == object:
            inheritance_depth = 0
        else:
            inheritance_depth = self.count_class_inheritance_depth(example_class.__base__) + 1
        return inheritance_depth

    def count_props(self, example_class: type, out_stats: ClassStats):
        inherited_methods = 0
        overridden_methods = 0
        visible_methods = 0
        private_methods = 0
        for _name, member in inspect.getmembers(example_class):
            if inspect.isroutine(member):
                if _name not in example_class.__dict__:
                    inherited_methods += 1
                    self.vprint(f'{_name} inherited')
                elif any(_name in super_class.__dict__ for super_class in example_class.mro()[1:]):
                    overridden_methods += 1
                    self.vprint(f'{_name} overridden')

                if _name.startswith(f'_{example_class.__name__}') and not _name.endswith("__"):
                    private_methods += 1
                    self.vprint(f'{_name} private')
                else:
                    visible_methods += 1
                    self.vprint(f'{_name} visible')

        out_stats.set_statistic([inherited_methods, overridden_methods, visible_methods, private_methods])

    def get_polymorphism_factor(self) -> float:
        total_overriden_count = 0
        total_child_count = 0
        for example_class, stats in self.classes_stats.items():
            total_overriden_count += stats.overridden_methods_count
            total_child_count += stats.child_count
        return 0 if total_overriden_count == 0 or total_child_count == 0 else total_overriden_count / total_child_count

    def get_method_inheritance_factor(self) -> float:
        inherited_methods = 0
        all_methods = 0
        for example_class, stats in self.classes_stats.items():
            inherited_methods += stats.overridden_methods_count
            all_methods += stats.inherited_methods_count + stats.overridden_methods_count
        return 0 if inherited_methods == 0 or all_methods == 0 else inherited_methods / all_methods

    def get_closed_methods_factor(self) -> float:
        private_methods = 0
        all_methods = 0
        for example_class, stats in self.classes_stats.items():
            private_methods += stats.private_methods_count
            all_methods += stats.visible_methods_count + stats.private_methods_count
        return 0 if private_methods == 0 or all_methods == 0 else private_methods / all_methods


def Init_MetricCounter(module: str, __print: bool) -> MetricCounter:
    module_stats = MetricCounter(__print)
    for name, obj in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(obj):
            module_stats.count_class(obj)
    return module_stats
