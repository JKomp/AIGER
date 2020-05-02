import random
import os
import tempfile
import subprocess
import aigsim

FILE = "./examples/input.txt"
print(FILE)

trials = 10000
input_length = 2
program = "aigsim"

runs = []
population = []


def create_random_stream(min_lines = 2, max_lines=50, len_input = input_length):
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

def delete_random_line(s, len_input):
    """Returns s with a random character deleted"""
    if s == "":
        return s

    for _ in range(0,5):
        pos = random.randint(0, len(s) - 1)
        if(pos < len(s) - len_input and s[pos-1]=="\n" and s[pos+len_input]=="\n"): 
            # print("Deleting", repr(s[pos]), "at", pos)
            return s[:pos] + s[pos + len_input + 1:]
    return s
        
def insert_random_line(s, len_input):
    """Returns s with a random character inserted"""
    out = ""
    for i in range(0, len_input):
        out += str(random.randint(0, 1))
    out += "\n"

    for _ in range(0,5):
        pos = random.randint(0, len(s) - 1)
        if(pos < len(s) - len_input and s[pos-1]=="\n" and s[pos+len_input]=="\n"):
            return s[:pos] + out + s[pos:]
    return s
    

def flip_random_line(s, len_input):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    new_c = "0"
    for _ in range(0,5):
        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        if(c == "0"):
            new_c = "1"
            return s[:pos] + new_c + s[pos + 1:]
        elif(c == "1"):
            new_c = "0"
            return s[:pos] + new_c + s[pos + 1:]
    return s    


def mutate(s, len_input):
    """Return s with a random mutation applied"""
    mutators = [
#         delete_random_line,
        insert_random_line,
        flip_random_line
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s, len_input)

class MutationFuzzer:
    def __init__(self, min_mutations=2, max_mutations=10):
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations

    def mutate(self, inp, len_input):
        return mutate(inp, len_input)        

    def create_candidate(self, len_input):
        candidate = random.choice(population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate, len_input)
        return candidate

    def fuzz(self, len_input = input_length):
        self.inp = self.create_candidate(len_input)
        return self.inp        

for i in range(trials):
    is_interesting = False

    if len(population) >= 1:
        rnd = random.random()
        if(rnd <= 0.5):
            MF = MutationFuzzer()
            data = MF.fuzz(input_length)
            with open(FILE, "w") as f:
                f.write(data)
        elif(rnd <= 0.8):
            ind = random.randrange(0,len(population))
            data = population[ind].replace(".","")
            data += create_random_stream(1,10)
            with open(FILE, "w") as f:
                f.write(data)        
        else:
            data = create_random_stream()
            with open(FILE, "w") as f:
                f.write(data)
    else:
        with open(FILE, "r") as f:
            data = f.read()
        population.append(data)                 

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
        population.append(data)

    runs.append((data, verbose, is_interesting))

for x in runs[-10:]:
    if(x[2]):
        print(x[0])
        print("---------")
        print(x[1])
        print("---------")
        print("++++++++++++++++++++++++")
