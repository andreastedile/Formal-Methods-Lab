from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose3

map_var = IDPool()
cnf = CNF()


def dnf_list(l1, l2):
    for var1 in l1:
        for var2 in l2:
            clause = [map_var.id(var1), map_var.id(var2)]
            cnf.append(clause)


def negation(var):
    cnf.append([-map_var.id(var)])


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


def exactly_one(varlist):
    # AtLeastOne
    or_list(varlist)
    # AtMostOne
    at_most_one(varlist)


# Mapping
for i in range(0, 4):
    for j in ["c", "g", "s", "m", "A", "L", "S", "I"]:
        map_var.id("x{}{}".format(i, j))

# Clue 1
dnf_list(["x0A", "x2c"], ["x1A", "x3c"])

# Clue 2
negation("x0g")
negation("x3S")
neg_or_list(["x1g", "x2S"])

# Clue 3 and 4
dnf_list(["x0s", "x3L"], ["x0L", "x3s"])
dnf_list(["x0A", "x2I"], ["x1A", "x3I"])

for day in range(0, 4):
    list_company = list()
    for company in ["A", "L", "S", "I"]:
        list_company.append("x{}{}".format(day, company))
    exactly_one(list_company)
    list_jobs = list()
    for job in ["c", "g", "s", "m"]:
        list_jobs.append("x{}{}".format(day, job))
    exactly_one(list_jobs)

for company in ["A", "L", "S", "I"]:
    list_days = list()
    for day in range(0, 4):
        list_days.append("x{}{}".format(day, company))
    exactly_one(list_days)

for job in ["c", "g", "s", "m"]:
    list_days = list()
    for day in range(0, 4):
        list_days.append("x{}{}".format(day, job))
    exactly_one(list_days)

cnf.to_file('riddle.cnf')

g = Glucose3(bootstrap_with=cnf.clauses)
g.solve()
model = g.get_model()
print(model)
assert model == [-1, -2, 3, -4, 5, -6, -7, -8,
                 -9, -10, -11, 12, -13, -14, 15, -16,
                 17, -18, -19, -20, -21, -22, -23, 24,
                 -25, 26, -27, -28, -29, 30, -31, -32]
