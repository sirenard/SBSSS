import numpy as np


class TransportProblemStep:
    def __init__(self, costs,c, n_offer, n_request, var_base, var_base_value, in_variable, out_variable, u, v):
        self.costs = costs
        self.c = np.copy(c)
        self.n_offer = n_offer
        self.n_request = n_request
        self.var_base = var_base[:]
        self.var_base_value = np.copy(var_base_value)
        self.in_variable = in_variable
        self.out_variable = out_variable
        self.u = u
        self.v = v

    def __str__(self):
        res = ""

        res += "* u_i: " + ", ".join(list(map(str, self.u))) + "\n"
        res += "* v_j: " + ", ".join(list(map(str, self.v))) + "\n\n"

        m = [[" "] * 2 * self.n_request for j in range(2 * self.n_offer)]

        for i in range(self.n_offer):
            for j in range(self.n_request):
                m[2 * i][2 * j] = str(self.costs[i][j])

                var = self.n_request * i + j
                if var in self.var_base:
                    var_index = self.var_base.index(var)
                    m[2 * i + 1][2 * j] = "**"+str(self.var_base_value[var_index, 0])+"**"
                else:
                    cr = "*"+str(self.c[var,0])+"*"
                    if var == self.in_variable:
                        cr = "<u>{}</u>".format(cr)
                    m[2*i+1][2*j+1] = cr
        head = []
        for i in range(self.n_request):
            head += ["Request", str(i)]

        res += "| |" + " | ".join(head) +"|\n"
        res += "|" + " | ".join([":--:"] * (2 * self.n_request + 1)) + "|\n"

        count = 0
        for line in m:
            t = ""
            if count%2==0:
                t = "Offer {}".format(count//2)
            res += "| {}  |".format(t) + " | ".join(line) + "\n"
            count += 1

        return res
