import numpy as np

from SimplexStep import SimplexStep


class SimplexSolver:
    def __init__(self, c, A, b, x=None, optimize=1):
        """
        initialize solver to solve a linear problem like:
        max/min c^T x
        s.t.    Ax = b
                x >= 0
        (m constraints, n variables, n>m)
        :param c: list of n numbers
        :param x: list of n string (variable names) (by default x1,x2,...,xn)
        :param A: m x n matrix of numbers
        :param b: list of m numbers
        :param optimize: 1 if maximize, -1 if minimize
        """
        self.A = np.array(A, dtype="float64")
        self.m, self.n = self.A.shape
        assert self.n > self.m, "You need more variables than constraints "
        assert optimize in [1, -1], "optimize must be 1 or -1"
        self.optimize = optimize
        self.c = np.array(c, dtype="float64")[np.newaxis].T
        self.b = np.array(b, dtype="float64")[np.newaxis].T

        if x is None:
            self.x = ["x{}".format(i) for i in range(1, self.n + 1)]
        else:
            assert len(x) == self.n, "Bad size for x parameter"
            self.x = x

        self.base = None
        self.sol = None
        self.obj = 0
        self.steps = []  # save of every steps

    def solve(self):
        self.find_init_base()

        is_opti = False
        while not is_opti:
            var_in, var_out = self.find_in_out_variables()

            self.steps.append(
                SimplexStep(self.A, self.x, self.c, self.base, self.obj, self.sol, var_in, var_out, self.optimize))
            """print("Obj: {}".format(self.obj))
            print("Current sol: {}".format(self.sol.T))
            print("Variable entrante: {}, Variable sortante: {}".format(var_in, var_out))
            print("c: {}".format(self.c.T))
            print("A: {}".format(self.A))
            print("Base: {}".format(self.base))
            print("")"""
            if var_in is None:
                is_opti = True
            else:
                line_index = self.base.index(var_out)
                self.base[line_index] = var_in

                # update A line for in_var
                a = self.A[line_index, var_in]
                self.A[line_index] /= a
                self.sol[line_index] /= a

                # update A and sol
                for m in range(self.m):
                    if m != line_index:
                        coef = self.A[m, var_in]
                        self.A[m] -= coef * self.A[line_index]
                        self.sol[m] -= coef * self.sol[line_index]

                coef = self.c[var_in, 0]
                self.c -= coef * self.A[line_index][np.newaxis].T
                self.obj -= coef * self.sol[line_index, 0]

    def find_in_out_variables(self):
        """
        find which variable must leave the base and which one must enter
        :return: (in variable index, out variable index) or None if none variable can go in base
        """
        in_variable = np.argmax(self.c)
        if self.c[in_variable] > 0:
            out_variable = -1
            current = float('inf')
            for m in range(self.m):
                a = self.A[m, in_variable]

                if a > 0 and self.sol[m, 0] / a < current:
                    current = self.sol[m, 0] / a
                    out_variable = self.base[m]

            if out_variable != -1:
                return in_variable, out_variable
        return None, None

    def find_init_base(self):
        var = 0
        self.base = []
        self.sol = []
        s = []
        while len(self.base) != self.m and var != self.n:
            col = self.A[:, var]  # get a column
            non_zero = np.flatnonzero(col)
            if len(non_zero) == 1:  # if only 1 no zero in column -> var can be in base
                constraint_index = non_zero[0]  # index of the constraints where the variable appear

                self.base.append(var)
                self.sol.append(self.b[constraint_index, 0] / self.A[constraint_index, var])
                s.append(self.sol[-1])
                self.A[constraint_index] /= self.A[constraint_index, var]
            else:  # variable not in base
                s.append(0)
            var += 1

        self.sol = np.array(self.sol)[np.newaxis].T
        self.obj = int(np.dot(self.c.T, s))

    def __str__(self):
        res = ""

        for i in range(len(self.steps)):
            step = self.steps[i]
            res += "# Iteration {}\n".format(i+1)
            res += str(step) + "\n"

        return res


if __name__ == "__main__":
    c = [5, 4, 0, 0, 0, 0]
    A = [
        [6, 4, 1, 0, 0, 0],
        [1, 2, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [-1, 1, 0, 0, 0, 1]
    ]
    b = [24, 6, 2, 1]

    simplex_solver = SimplexSolver(c, A, b, ["x1","x2","s1","s2","s3","s4"])

    # simplex_solver.find_init_base()
    # print(simplex_solver.base)
    # print(simplex_solver.obj)

    simplex_solver.solve()
    print(simplex_solver)
