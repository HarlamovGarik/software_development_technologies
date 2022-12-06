from __MetricCounter__ import Init_MetricCounter
from __ClassStats__ import class_stats_to_row
import tabulate
import pytest

if __name__ == '__main__':
    package_counter = Init_MetricCounter('pytest', False)
    table_headers = ["Name", "Inheritance Depth", "N-Children", "N-Inherited Methods", "N-Overridden Methods",
                     "N-Visible Methods", "N-Private Methods"]
    print(tabulate.tabulate(
        [class_stats_to_row(example_class, stats) for example_class, stats in package_counter.classes_stats.items()],
        headers=table_headers))

    lib_factors = {"Closed Methods Factor": [package_counter.get_closed_methods_factor()],
                   "Method Inheritance Factor": [package_counter.get_method_inheritance_factor()],
                   "Polymorphism Factor": [package_counter.get_polymorphism_factor()]}
    lib_factors_headers = ["Closed Methods Factor", "Method Inheritance Factor", "Polymorphism Factor"]
    print(tabulate.tabulate(lib_factors, headers="keys"))
