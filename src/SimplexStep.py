import numpy as np
from fractions import Fraction


class SimplexStep:
    def __init__(self, A, x, c, base, obj, sol, in_variable, out_variable, optimize):
        self.A = np.copy(A)
        self.x = np.copy(x)
        self.c = np.copy(c)
        self.base = np.copy(base)
        self.obj = obj
        self.sol = np.copy(sol)
        self.in_variable = in_variable
        self.out_variable = out_variable
        self.optimize = optimize

    def __str__(self):
        labels = ["Var. en base", "z"] + list(self.x.T) + ["Solution"]
        head = " | ".join([":--:"]*(3+len(list(self.x.T))))
        z = ["z", -self.optimize] + list(self.c.T[0]) + [self.obj]
        z = list(map(create_fraction, z))

        matrix = [list(map(create_fraction,[self.x[self.base[i]], 0] + list(self.A[i]) + [self.sol[i,0]])) for i in range(self.A.shape[0])]

        if self.out_variable is not None:
            index = list(self.base).index(self.out_variable)
            matrix[index][self.in_variable + 2] = "**" + matrix[index][self.in_variable + 2] + "**"

        res = "| " + " | ".join(labels) + " |" + "\n"
        res += head + "\n"
        res += "| " + " | ".join(z) + " |" + "\n"
        for line in matrix:
            res += "| " + " | ".join(line) + "| " + "\n"

        return res

def create_fraction(n):
    if type(n) in [float,int, np.float64]:
        return str(Fraction(n).limit_denominator())
    return n

