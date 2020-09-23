import csv
import re
import time
import hashlib
import pandas as pd
from typing import List


class Parser:

    DEFAULT_FILEPATH = "Power.log"
    DEFAULT_OUTPUT = "output.log"

    def __init__(self, filepath: str = ""):
        self.filepath = filepath or Parser.DEFAULT_FILEPATH
        self.output_path = Parser.DEFAULT_OUTPUT

    def remove_duplicates(self, method="BASIC"):
        """
        Remove line duplicates
        :return:
        """
        if method == "BASIC":
            results = []
            lines_seen = []
            with open(self.filepath, "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    l = " ".join(line.split()[4:])
                    if l not in lines_seen[max(0, i-5000):]:
                        results.append(line)
                    lines_seen.append(l)
            self.write_lines(results)

        elif method=="HASH":
            results = []
            hash_seen = []
            with open(self.filepath, "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    l = " ".join(line.split()[4:])
                    hashval = int(hashlib.sha1(l.encode()).hexdigest(), 16)
                    if hashval not in hash_seen[max(0, i - 5000):]:
                        results.append(line)
                    hash_seen.append(hashval)
            self.write_lines(results)

        elif method=="PANDAS":
            with open(self.filepath, "r") as file:
                lines = file.readlines()
                df = pd.DataFrame(data={"lines":lines, "splitted": [" ".join(line.split()[4:]) for line in lines]})
                df.drop_duplicates(subset=["splitted"], inplace=True)
                self.write_lines(df["lines"])
                # df.to_csv("output.log", header=False, index=False, columns=["lines"], quoting=csv.QUOTE_NONE, escapechar='')

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

start = time.time()
p.remove_duplicates(method="PANDAS")
print("PANDAS method took : ", time.time()-start, "s")

# start = time.time()
# p.remove_duplicates(method="BASIC")
# print("BASIC method took : ", time.time()-start, "s")
#
# start = time.time()
# p.remove_duplicates(method="HASH")
# print("HASH method took : ", time.time()-start, "s")

print("end.")
