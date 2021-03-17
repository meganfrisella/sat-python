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
            assert(assignment[var] != -1)
            # NOTE: converted `var` to bool (represented as ints in our assignment)
            result += " " + ("" if bool(assignment[var]) else "-") + str(var)

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")


def unitClauseElim(varAssignment, formula):
    '''
    for each unit clause {+/-x} in formula
    	remove all non-unit clauses containing +/-x
    	remove all instances of -/+x in every clause // flipped sign!
    	assign x consistent with its sign in unit clause
    '''
    for clause in formula:
        if (len(clause.literalSet) == 1):
            literal = clause.literalSet[0]
            opliteral = Literal(literal.name, not(literal.sign))
            formula = list(filter(lambda c: not(literal in c.literalSet), formula))
            formula = list(map(lambda c: Clause(c.id, list(filter(lambda l: not(opliteral == l), c.literalSet))), formula))
            varAssignment[literal.name] = int(literal.sign)
    return varAssignment, formula


def pureLiteralElim(varAssignment, formula):
    '''
    for each variable x
        if +/-x is pure in formula
            remove all clauses containing +/-x
            assign x consistent with its sign
    '''
    if len(formula) == 0:
        return varAssignment, formula

    sign_dict = dict()
    var_set = set(k for k in varAssignment.keys() if varAssignment[k] == -1)

    for clause in formula:
        literals = clause.literalSet
        for lit in literals:
            if (lit.name in sign_dict) and (lit.name in var_set):
                if sign_dict[lit.name] != lit.sign:
                    var_set.remove(lit.name)
            else:
                sign_dict[lit.name] = lit.sign

    # TODO: are these similar loops to simplify?
    # Clause(c.id, list(filter(lambda l: not(l.name in var_set), c.literalSet)))
    formula = list(filter(lambda c: all(list(lit.name not in var_set for lit in c.literalSet)), formula))
    for name in var_set:
        varAssignment[name] = int(sign_dict[name])

    return varAssignment, formula


def solve(varAssignment, formula):
    '''
	do unit clause elim and pure literal elim on the formula
	unitClauseElim(formula)
	pureLiteralElim(formula)

	if formula has empty clause
		return unsat
	if formula has no clauses
		sat -> return current varAssignment

	x := pickVar(formula) // do anything reasonable here
	if solve(varAssignment + {+x}, formula) is sat
		return result of solving with x assigned to true
	else
		return solve(varAssignment + {-x}, formula)
    '''

    # print("______________________________________")
    # print(f"BEGINNING:\n{varAssignment.items()},\n{formula}")

    varAssignment, formula = unitClauseElim(varAssignment, formula)
    # print("______________________________________")
    # print(f"AFTER UNIT ELIM:\n{varAssignment.items()},\n{formula}")

    varAssignment, formula = pureLiteralElim(varAssignment, formula)
    # print("______________________________________")
    # print(f"AFTER PURE ELIM:\n{varAssignment.items()},\n{formula}")

    if len(formula) == 0:
        for name in varAssignment.keys():
            if varAssignment[name] == -1:
                varAssignment[name] = 1
        return varAssignment

    for clause in formula:
        if len(clause.literalSet) == 0:
            return None

    # get num. occurrences of each variable in formula
    lit2freq = dict()
    for clause in formula:
        for lit in clause.literalSet:
            if lit.name in lit2freq:
                lit2freq[lit.name] += 1
            else:
                lit2freq[lit.name] = 1
    # find the most frequent variable
    sort_keys = list(k for k, v in sorted(lit2freq.items(), key=lambda item: item[1]))
    most_freq = sort_keys[0]

    # print(f"SORTED UNASSIGNED KEYS: {sort_keys}\n")

    # create a new unit clause with this variable (positive)
    new_id = max(list(map(lambda c: c.id, formula))) + 1
    new_literal = Literal(most_freq, True)
    new_assigment = solve(varAssignment, [Clause(new_id, [new_literal])] + formula)

    if not(new_assigment is None):
        return new_assigment
    else:
        # create a new unit clause with this variable (negative)
        new_literal = Literal(most_freq, False)
        new_assigment = solve(varAssignment, [Clause(new_id, [new_literal])] + formula)
        return new_assigment

if __name__ == "__main__":
    inputFile = sys.argv[1]
    varset, clauseSet = readInput(inputFile)

    # dictionary mapping variable name to int (-1=unassigned, 0=False, 1=True)
    varAssignment = dict.fromkeys(varset, -1)
    varAssignment = solve(varAssignment, clauseSet)

    printOutput(varAssignment)
