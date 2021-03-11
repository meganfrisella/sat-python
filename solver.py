#!/bin/python3
import sys
from copy import copy, deepcopy
import random

# Feel free to change the provided types and parsing code to match
# your preferred representation of formulas, clauses, and literals.

class Literal:
    def __init__(self, name, sign):
        self.name = name  # integer
        self.sign = sign  # boolean

    def __repr__(self):
        return ("-" if not self.sign else "") + self.name

    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
      return hash((self.name, self.sign))


class Clause:
    def __init__(self, id, literalSet):
        self.id = id
        self.literalSet = literalSet

    def __repr__(self):
        return f"{self.id}: {str(self.literalSet)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.id == other.id


# Read and parse a cnf file, returning the variable set and clause set
def readInput(cnfFile):
    variableSet = []
    clauseSet = []
    nextCID = 0
    with open(cnfFile, "r") as f:
        for line in f.readlines():
            tokens = line.strip().split()
            if tokens and tokens[0] != "p" and tokens[0] != "c":
                literalSet = []
                for lit in tokens[:-1]:
                    sign = lit[0] != "-"
                    variable = lit.strip("-")

                    literalSet.append(Literal(variable, sign))
                    if variable not in variableSet:
                        variableSet.append(variable)

                clauseSet.append(Clause(nextCID, literalSet))
                nextCID += 1

    return variableSet, clauseSet

# Print the result in DIMACS format
def printOutput(assignment):
    result = ""
    isSat = (assignment is not None)
    if isSat:
        for var in assignment:
            result += " " + ("" if assignment[bool(var)] else "-") + str(var)

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")


def unitClauseElim(varAssignment: dict[Literal, int], formula: list[Clause]):
    # for each unit clause {+/-x} in formula
    # 	remove all non-unit clauses containing +/-x
    # 	remove all instances of -/+x in every clause // flipped sign!
    # 	assign x consistent with its sign in unit clause
    for clause in formula:
        if (len(clause.literalSet) == 1):
            literal = clause.literalSet[0]
            opliteral = Literal(literal.name, not(literal.sign))
            formula = list(filter(lambda c: not((len(c.literalSet) != 1) and literal in c.literalSet), formula))
            formula = list(map(lambda c: filter(lambda l: not(opliteral == l), c.literalSet), formula))
            varAssignment[literal] = int(literal.sign)
    return varAssignment, formula


def pureLiteralElim(varAssignment: dict[Literal, int], formula: list[Clause]):
    # for each variable x
    #     if +/-x is pure in formula
    #         remove all clauses containing +/-x
    #         assign x consistent with its sign
    sign_dict = dict()
    var_set = set(k for k in varAssignment.keys() if varAssignment[k] == -1)

    for clause in formula:
        literals = clause.literalSet
        for lit in literals:
            if lit in sign_dict:
                if sign_dict[lit] != lit.sign:
                    var_set.remove(lit)
            else:
                sign_dict[lit] = lit.sign

    # TODO: are these similar loops to simplify?
    formula = list(map(lambda c: filter(lambda l: not(l in var_set), c.literalSet), formula))
    for lit in var_set:
        varAssignment[lit] = int(lit.sign)

    return varAssignment, formula


def solve(varAssignment: dict[Literal, int], formula: list[Clause]):
	# // do unit clause elim and pure literal elim on the formula
	# unitClauseElim(formula)
	# pureLiteralElim(formula)
    #
	# if formula has empty clause
	# 	return unsat
	# if formula has no clauses
	# 	sat -> return current varAssignment
    #
	# x := pickVar(formula) // do anything reasonable here
	# if solve(varAssignment + {+x}, formula) is sat
	# 	return result of solving with x assigned to true
	# else
	# 	return solve(varAssignment + {-x}, formula)

    varAssignment, formula = unitClauseElim(varAssignment, formula)
    varAssignment, formula = pureLiteralElim(varAssignment, formula)

    if len(formula) == 0:
        return varAssignment

    for clause in formula:
        if len(clause.literalSet) == 0:
            return None

    lit2freq = dict()
    for clause in formula:
        for lit in clause.literalSet:
            if lit in lit2freq:
                lit2freq[lit] += 1
            else:
                lit2freq[lit] = 1

    # TODO: will this forever recur on the same literal? what's the logic?
    sort_keys = list(k for k, v in sorted(lit2freq.items(), key=lambda item: item[1]))
    most_freq = sort_keys[-1]
    varAssignment[most_freq] = 1

    new_assigment = solve(varAssignment, formula)
    if not(new_assigment is None):
        return new_assigment
    else:
        varAssignment[most_freq] = 0
        new_assigment = solve(varAssignment, formula)
        return new_assigment

if __name__ == "__main__":
    inputFile = sys.argv[1]
    varset, clauseSet = readInput(inputFile)
    varAssignment = dict.fromKeys(varset, -1)
    varAssignment = solve(varAssignment, clauseSet)

    # TODO: find a satisfying instance (or return unsat) and print it out
    if varAssignment is None:
        printOutput("unsat")
    else:
        printOutput(varAssignment)
