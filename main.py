import re
import time
from typing import List


class Parser:

    DEFAULT_FILEPATH = "Power.log"
    DEFAULT_OUTPUT = "output.log"

    def __init__(self, filepath: str = ""):
        self.filepath = filepath or Parser.DEFAULT_FILEPATH
        self.output_path = Parser.DEFAULT_OUTPUT

    def remove_duplicates(self):
        """
        Remove line duplicates
        :return:
        """
        results = []
        lines_seen = []
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                l = " ".join(line.split()[4:])
                # print(i)
                # if l not in lines_seen[max(0, i-5000):]:
                #     results.append(line)
                lines_seen.append(l)
        self.write_lines(results)

    def get_duplicates(self):
        """
        Output the line present 2 times
        :return:
        """
        results = []
        lines_seen = []
        with open(self.filepath, "r") as file:
            for i, line in enumerate(file):
                if i < 50000:
                    l = " ".join(line.split()[4:])
                    if l not in lines_seen[max(0, i - 10000):]:
                        lines_seen.append(l)
                    else:
                        results.append(line)
                else:
                    break
        self.write_lines(results)

    def write_lines(self, lines: List[str]):
        with open(self.output_path, "w") as file:
            file.writelines(lines)


p = Parser()
p.remove_duplicates()
print("end.")
