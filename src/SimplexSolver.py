from fractions import Fraction

import numpy as np

from SimplexStep import SimplexStep


class SimplexSolver:
    def __init__(self, c, A, b, x=None, optimize=-1, two_phase=False, equality=None):
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
        :param equality: list of constraints sign ("=","<=",">=") or None if only "="
        """
        self.A = np.array(A, dtype="float64")
        self.m, self.n = self.A.shape

        if x is None:
            self.x = ["x{}".format(i) for i in range(1, self.n + 1)]
        else:
            assert len(x) == self.n, "Bad size for x parameter"
            self.x = x

        self.equality = equality
        if equality is not None:
            for i in range(len(equality)):
                s = equality[i]
                if s in ["<=", ">="]:
                    tmp = np.zeros((self.m, self.n + 1))
                    tmp[:, :-1] = self.A
                    self.A = tmp  # add a column of 0
                    self.n += 1

                    c.append(0)

                    if s == ">=":
                        self.A[i, -1] = -1
                    elif s == "<=":
                        self.A[i, -1] = 1

                    self.x.append("s{}".format(i + 1))
        self.Ab = None
        self.An = None
        self.init_A = np.copy(self.A)
        assert self.n >= self.m, "You need more variables than constraints "
        assert optimize in [1, -1], "optimize must be 1 or -1"
        self.optimize = optimize
        self.c = np.array(c, dtype="float64")[np.newaxis].T
        self.cb = None
        self.cn = None
        self.init_c = np.copy(self.c)
        self.b = np.array(b, dtype="float64")[np.newaxis].T
        self.init_b = np.copy(self.b)

        self.base = None
        self.var_base_value = None
        self.obj = 0
        self.steps = []  # save of every steps

        self.two_phase = two_phase
        self.two_phase_simplex = None

    def solve(self):
        solution_found = self.find_solution_admissible()
        if not solution_found:
            return None

        is_opti = False
        while not is_opti:
            var_in, var_out = self.find_in_out_variables()

            self.save_step(var_in, var_out)

            if var_in is None:
                is_opti = True
            else:
                line_index = self.base.index(var_out)
                self.base[line_index] = var_in

                # update A line for in_var
                a = self.A[line_index, var_in]
                self.A[line_index] /= a
                self.var_base_value[line_index] /= a

                # update A and sol
                for m in range(self.m):
                    if m != line_index:
                        coef = self.A[m, var_in]
                        self.A[m] -= coef * self.A[line_index]
                        self.var_base_value[m] -= coef * self.var_base_value[line_index]

                coef = self.c[var_in, 0]
                self.c -= coef * self.A[line_index][np.newaxis].T
                self.obj -= coef * self.var_base_value[line_index, 0]

    def save_step(self, var_in, var_out):
        self.steps.append(
            SimplexStep(self.A, self.x, self.c, self.base, self.obj, self.var_base_value, var_in, var_out,
                        self.optimize))

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
                if a > 0 and self.var_base_value[m, 0] / a < current:
                    current = self.var_base_value[m, 0] / a
                    out_variable = self.base[m]

            if out_variable != -1:
                return in_variable, out_variable
        return None, None

    def find_solution_admissible(self):
        var = 0
        self.base = []
        self.var_base_value = []
        sol = []
        cols = []  # keep the number column that correspond with the base variable

        while len(self.base) != self.m and var != self.n:
            col = self.A[:, var]  # get a column
            non_zero = np.flatnonzero(col)
            constraint_index = non_zero[0]  # index of the constraints where the variable appear
            if len(non_zero) == 1 and self.A[
                constraint_index, var] > 0:  # if only 1 no zero in column -> var can be in base

                cols.append(constraint_index)
                self.base.append(var)
                self.var_base_value.append(self.b[constraint_index, 0] / self.A[constraint_index, var])

                sol.append(self.var_base_value[-1])
                self.A[constraint_index] /= self.A[constraint_index, var]
            else:  # variable not in base
                sol.append(0)
            var += 1

        if len(self.base) != self.m and not self.two_phase:  # no initial solution found
            self.two_phase_find_init_base(cols)

        if len(self.base) != self.m:  # "Initial base not found"
            return False

        if self.two_phase:
            tmp = sorted(zip(cols, self.base))
            self.base = [b for c, b in tmp]

        self.put_solution_in_base()

        return True

    def put_solution_in_base(self):
        """
        Adapt the problem with the new base
        :return:
        """
        var_not_base = list(set(range(self.n)) - set(self.base))

        print(self.two_phase)
        print(self.base)
        print(self.A)

        self.Ab = self.A[:, self.base]
        self.An = self.A[:, var_not_base]
        self.cb = np.array(self.c[self.base, :], dtype="float64")
        self.cn = np.array(self.c[var_not_base, :], dtype="float64")
        tmp_c = self.cn.T - np.dot(np.dot(self.cb.T, np.linalg.inv(self.Ab)), self.An)
        self.c *= 0
        pos = 0
        for i in var_not_base:
            self.c[i, 0] = tmp_c[0, pos]
            pos += 1
        self.c *= -self.optimize
        self.var_base_value = np.dot(np.linalg.inv(self.Ab), self.b)
        self.obj = self.optimize * np.dot(self.cb.T, self.var_base_value)[0, 0]

    def two_phase_find_init_base(self, list_column=[]):
        """
        Make the two phases to find an initial solution
        :param list_column: list of the position of line that correspond with the variable in base
        :return: value of two phase
        """
        A = np.append(self.A, np.eye(self.m), axis=1)
        x = self.x[:] + ["R{}".format(i) for i in range(self.m - len(self.base))]
        c = [0] * self.n + [1] * self.m

        count = 0
        for i in list_column:
            col_index = self.n - count + i
            A = np.delete(A, col_index, 1)
            c = c[:col_index] + c[col_index + 1:]
            count += 1

        b = self.b[:, 0]

        two_phase_simplex = SimplexSolver(c, A, b, x, 1, True)
        two_phase_simplex.solve()
        if round(two_phase_simplex.obj, 10) == 0:
            self.A = two_phase_simplex.A[:, :self.n]
            self.b = two_phase_simplex.var_base_value
            self.base = two_phase_simplex.base
            self.var_base_value = two_phase_simplex.var_base_value

            all_constraints = list(range(self.m))
            i = 0
            while i < len(self.base): # retire les ligne si des variables artificielles encore en base (si = 0)
                if self.base[i] >= self.n:
                    self.base.pop(i)
                    self.A = np.delete(self.A, i, 0)
                    self.b = np.delete(self.b, i, 0)
                    self.m -= 1
                else:
                    i += 1


        self.two_phase_simplex = two_phase_simplex

        return two_phase_simplex.obj

    def __str__(self):
        if not self.two_phase:
            res = "# Formulation\n" + self._formulation_str()
        else:
            res = "## Formulation 2 phase\n" + self._formulation_str()

        if self.two_phase_simplex is not None:
            res += str(self.two_phase_simplex)
        if len(self.steps):
            res += "#" * self.two_phase + "# Resolution\n" + self._resolution_str()
        res += "#" * self.two_phase + "# Optimal Solution\n" + self._solution_str()

        return res

    def _resolution_str(self):
        res = ""
        for i in range(len(self.steps)):
            step = self.steps[i]
            res += "#" * self.two_phase + "## Iteration {}\n".format(i + 1)
            res += str(step) + "\n"

        return res

    def _formulation_str(self):
        res = ""
        res += "max  " if self.optimize == -1 else "min  "
        addition = []
        for i in range(self.n):
            if self.init_c[i, 0] != 0:
                addition.append("{} {}".format(Fraction(self.init_c[i, 0]).limit_denominator(), self.x[i]))

        res += " + ".join(addition) + "  \n"
        res += "s.t.\n\n"

        for i in range(self.m):
            addition = []
            for j in range(self.n):
                if self.init_A[i, j] != 0:
                    addition.append("{} {}".format(Fraction(self.init_A[i, j]).limit_denominator(), self.x[j]))
            signe = "="
            if self.equality is not None:
                signe = self.equality[i]
            constraint = "* " + " + ".join(addition) + " {} {}\n".format(signe, self.init_b[i, 0])
            constraint = constraint.replace("+ -", "- ")
            res += constraint

        return res

    def _solution_str(self):
        if len(self.steps):
            current_sol = []
            for i in range(self.n):
                if i in self.base:
                    val = Fraction(self.var_base_value[self.base.index(i)][0]).limit_denominator()
                    current_sol.append(val)
                else:
                    current_sol.append(0)

            res = "\n* ({}) = ({})\n".format(", ".join(map(str, self.x)), ", ".join(map(str, current_sol)))
            sol = self.optimize * self.obj
            res += "* obj = {} = {}\n".format(Fraction(sol).limit_denominator(), sol)
        else:
            res = "no admissible solution found\n"
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

    # simplex_solver = SimplexSolver(c, A, b, ["x1", "x2", "s1", "s2", "s3", "s4"])

    c = [30, 40, 0, 0, 0]
    A = [
        [1, 2, -1, 0, 0],
        [2, 2, 0, -1, 0],
        [1, 0, 0, 0, 1]
    ]
    b = [8, 11, 5]
    x = ["x_1", "x_2", "s_1", "s_2", "s_3"]

    # simplex_solver = SimplexSolver(c, A, b, x, 1)
    # simplex_solver.solve()

    c = [30, 40]
    A = [
        [1, 2],
        [2, 2],
        [1, 0]
    ]
    b = [8, 11, 5]
    x = ["x_1", "x_2"]

    # simplex_solver = SimplexSolver(c, A, b, x, 1, equality=[">=", ">=", "<="])

    # simplex_solver.find_init_base()
    # print(simplex_solver.base)
    # print(simplex_solver.obj)

    c = [4, 1]

    A = [
        [3, 1],
        [4, 3],
        [1, 2]
    ]

    simplex_solver = SimplexSolver(c, A, b, x, 1, equality=["=", ">=", "<="])

    simplex_solver.solve()
    print(simplex_solver)
