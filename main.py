import csv
import re
import time
from datetime import datetime
import pandas as pd
from typing import List


class Parser:

    DEFAULT_FILEPATH = "Power.log"
    DEFAULT_OUTPUT = "output.log"

    def __init__(self, filepath: str = ""):
        self.filepath = filepath or Parser.DEFAULT_FILEPATH
        self.output_path = Parser.DEFAULT_OUTPUT

    def get_date(self, date):
        return datetime.strptime(date, "%H:%M:%S.%f")

    def remove_duplicates(self, filepath=""):
        """
        Remove line duplicates
        :return:
        """
        filepath = filepath or self.filepath
        with open(filepath, "r") as file:
            lines = file.readlines()
            df = pd.DataFrame(data={"lines": lines, "splitted": [" ".join(line.split()[4:]) for line in lines]})
            df.drop_duplicates(subset=["splitted"], inplace=True)
            self.write_lines(df["lines"])

    def reset_time(self, filepath=""):
        filepath = filepath or self.filepath
        with open(filepath, "r") as file:
            lines = file.readlines()
            df = pd.DataFrame(data={"lines": lines})
            begin = datetime.strptime(lines[0].split()[1][:-1], "%H:%M:%S.%f")

            def set_time(line):
                line = line.split()
                date = self.get_date(line[1][:-1])
                line[1] = str(date - begin)
                return " ".join(line)

            df["lines"] = df["lines"].apply(set_time)
            df["lines"] = df["lines"] + "\n"
            self.write_lines(df["lines"])

    def get_entity(self, entity_id, filepath=""):
        filepath = filepath or "output.log"
        with open(filepath, "r") as file:
            lines = file.readlines()
            results = []
            creation = "FULL_ENTITY - Creating ID={}".format(entity_id)
            starting = 0
            for i, line in enumerate(lines):
                if creation in line:
                    starting = i
                    results.append(line)
                if starting:
                    if "Entity={}".format(entity_id) in line:
                        results.append(line)
                    if "id={}".format(entity_id) in line:
                        results.append(line)
                    if i - starting > 1000:
                        break
        with open("entity_{}.log".format(entity_id), "w") as file:
            file.writelines(results)
        return results

    def write_lines(self, lines: List[str]):
        with open(self.output_path, "w") as file:
            file.writelines(lines)


p = Parser()

start = time.time()
p.remove_duplicates()
# p.reset_time("output.log")
print("PANDAS method took : ", time.time()-start, "s")


