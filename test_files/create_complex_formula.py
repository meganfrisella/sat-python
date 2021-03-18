import random

FILENAME = "random_complex_clause.txt"

all_vars = list(range(1, 26))
# varAssignment = dict.fromkeys(all_vars, -1)
write_str = "c  simple.cnf\nc\np cnf 25 40\n"

for i in range(40):
    n = random.sample(all_vars, 1)[0]
    sampled_clause = random.sample(all_vars, n)
    sampled_clause = [str(i) for i in sampled_clause]
    line = " ".join(sampled_clause) + " 0\n"
    print(line)
    write_str += line

with open(FILENAME, 'w') as fp:
    fp.write(write_str)
