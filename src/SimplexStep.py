from fractions import Fraction

import numpy as np


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
        labels = ["base", "z"] + list(self.x.T) + ["Solution"]
        head = " | ".join([":--:"] * (3 + len(list(self.x.T))))
        z = ["z", self.optimize] + list(self.c.T[0]) + [self.obj]

        print(" Je print le print")

        z = list(map(create_fraction, z))
        matrix = [list(map(create_fraction, [self.x[self.base[i]], 0] + list(self.A[i]) + [self.sol[i, 0]])) for i in
                  range(self.A.shape[0])]

        if self.out_variable is not None:
            index = list(self.base).index(self.out_variable)
            matrix[index][self.in_variable + 2] = "*" + matrix[index][self.in_variable + 2] + "*"



        res2=""
        for label in labels :
            nbr_espace = 8 - len(label)
            if nbr_espace%2==0:
                espace = " "* (nbr_espace//2) + "|"+" "* (nbr_espace//2)
            else :
                espace = " " * (nbr_espace //2 ) + "|" + " " * (nbr_espace // 2  +1)
            res2 += label + espace
        res2 +="\n"

        for z_val in z :

            nbr_espace = 8 - len(z_val)
            if nbr_espace%2==0:
                espace = " "* (nbr_espace//2) + "|"+" "* (nbr_espace//2)
            else :
                espace = " " * (nbr_espace //2 ) + "|" + " " * (nbr_espace // 2  +1)
            if (z_val=="z"):
                res2 += ""+z_val +" "+ espace
            else:
                res2 +=  z_val + espace
        res2 += "\n"

        for line in matrix:
            i = 0
            for element in line:
                nbr_espace = 8 - len(element)
                if nbr_espace % 2 == 0:
                    espace = " " * (nbr_espace // 2) + "|" + " " * (nbr_espace // 2)
                else:
                    espace = " " * (nbr_espace // 2) + "|" + " " * (nbr_espace // 2 + 1)
                if (i==0):
                    res2 += " "+element + espace
                else:
                    res2 +=  element + espace
                i+=1
            res2 += "\n"

        return res2


def create_fraction(n):
    if type(n) in [float, int, np.float64]:
        return str(Fraction(n).limit_denominator())
    return n
