from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose3

map_var = IDPool()
cnf = CNF()


def or_list(varlist):
    clause = [map_var.id(var) for var in varlist]
    cnf.append(clause)


def neg_or_list(varlist):
    clause = [-map_var.id(var) for var in varlist]
    cnf.append(clause)


def at_most_one(varlist):
    for i in range(0, len(varlist)):
        for j in range(i + 1, len(varlist)):
            clause = [-map_var.id(varlist[i]), -map_var.id(varlist[j])]
            cnf.append(clause)


def and_list(varlist):
    for var in varlist:
        clause = [map_var.id(var)]
        cnf.append(clause)


def exactly_one(varlist):
    # AtLeastOne
    or_list(varlist)
    # AtMostOne
    at_most_one(varlist)


for i in range(1, 10):
    for j in range(1, 10):
        for k in range(1, 10):
            map_var.id("x{}{}{}".format(i, j, k))

# Each row
for i in range(1, 10):
    for k in range(1, 10):
        varlist = list()
        for j in range(1, 10):
            varlist.append("x{}{}{}".format(i, j, k))
        exactly_one(varlist)

# Each columns
for j in range(1, 10):
    for k in range(1, 10):
        varlist = list()
        for i in range(1, 10):
            varlist.append("x{}{}{}".format(i, j, k))
        exactly_one(varlist)

for k in range(1, 10):
    for i in range(1, 10, 3):
        for j in range(1, 10, 3):
            varlist = list()
            varlist.append("x{}{}{}".format(i, j, k))
            varlist.append("x{}{}{}".format(i, j + 1, k))
            varlist.append("x{}{}{}".format(i, j + 2, k))
            varlist.append("x{}{}{}".format(i + 1, j, k))
            varlist.append("x{}{}{}".format(i + 2, j, k))
            varlist.append("x{}{}{}".format(i + 1, j + 1, k))
            varlist.append("x{}{}{}".format(i + 1, j + 2, k))
            varlist.append("x{}{}{}".format(i + 2, j + 1, k))
            varlist.append("x{}{}{}".format(i + 2, j + 2, k))
            exactly_one(varlist)

and_list(["x149", "x171",
          "x283", "x295",
          "x338", "x357",
          "x455", "x479",
          "x511", "x534", "x543", "x572",
          "x627", "x669", "x693",
          "x735", "x752", "x767",
          "x824", "x839", "x878",
          "x917", "x941", "x982"])

cnf.to_file('sudoku.cnf')

g = Glucose3(bootstrap_with=cnf.clauses)
g.solve()
model = g.get_model()
print(model)
