import os
import re


def analyze_lib(path):
    total_lines = 0
    empty_lines = 0
    comment_lines = 0
    for root, directories, file in os.walk(path):
        for file in file:
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as python_file:
                    lines = python_file.readlines()
                    total_lines += len(lines)
                    for line in lines:
                        if line.strip():
                            empty_lines += 1
                            continue
                        if re.findall(r'( [^!].*)|( :\"\"\"(.|\ n*)*?\"\"\")|( :\'\'\'(.|\n*)*?\'\'\')', line):
                            comment_lines += 1
    if empty_lines / total_lines > 0.25:
        empty_lines = total_lines * 0.25
    return total_lines, empty_lines, comment_lines, comment_lines / total_lines


lib_statistic = analyze_lib("../../dsml-privat")
print(f'Physical SLOC:\n\ttotal lines {lib_statistic[0]}\n\tempty lines {lib_statistic[1]}\n\tcomment lines {lib_statistic[2]}\n\tcomment_ratio {lib_statistic[3]}\n')
