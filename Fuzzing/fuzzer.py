import random
import os
import tempfile
import subprocess
import aigsim

FILE = "./examples/input.txt"
print(FILE)

def fuzzer(min_lines = 2, max_lines=50, len_input = 2):
    """A string of up to `max_lines` lines, each line binary of lengh `len_input`"""
    string_length = random.randrange(min_lines, max_lines + 1)
    out = ""
    for j in range(0, string_length):
        for i in range(0, len_input):
            out += str(random.randint(0, 1))
        if j < string_length - 1:
            out += "\n"
        else:
            out += "\n."
    return out

trials = 10000
program = "aigsim"

runs = []
datas = []

for i in range(trials):
    is_interesting = False

    if len(datas) >= 1:
        if(random.random() <= 0.8):
            ind = random.randrange(0,len(datas))
            data = datas[ind].replace(".","")
            data += fuzzer(1,10)
            with open(FILE, "w") as f:
                f.write(data)
        else:
            data = fuzzer()
            with open(FILE, "w") as f:
                f.write(data)
    else:
        data = fuzzer()
        with open(FILE, "w") as f:
            f.write(data)

    verbose = aigsim.main("./examples/aigTestSMV2.aag.txt",FILE)

    ver_lines = verbose.split("\n")
    count_1 = 0
    count_all = 0
    for ver_line in ver_lines:
        if(ver_line == ""):
            continue
        args = ver_line.split(" ")
        output = args[2]
        if output == "1":
            count_1 += 1
        count_all += 1
    if(float(count_1/count_all) <= 0.05):
        is_interesting = True
        datas.append(data)

    runs.append((data, verbose, is_interesting))

for x in runs[-10:]:
    if(x[2]):
        print(x[0])
        print("---------")
        print(x[1])
        print("---------")
        print("++++++++++++++++++++++++")
