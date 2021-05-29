from SimplexSolver import *
from TransportProblemStep import TransportProblemStep


class TransportProblem(SimplexSolver):
    def __init__(self, costs, request, offer, init_base_method="NO"):
        """
        Solve Transport Problem
        :param costs: matrix of costs
        :param request: list of requests for each center
        :param init_base_method: pour choisir la méthode pour la solution initiale: soit "NO" pourd nord ouest,
            "MC" pour moindre coût, ou directewment une solution avec un format [var en base 1, var en base 2, ...]
        :param offer: list of offer for each center
        """

        self.n_offer = len(offer)
        self.n_request = len(request)
        self.costs = costs
        self.init_base_method = init_base_method

        costs = np.array(costs)
        assert self.n_offer == costs.shape[0] and self.n_request == costs.shape[1], "Bad size"
        assert sum(offer) == sum(request), "Offer must be same as request"

        c = costs.flatten()
        b = [0] * (self.n_offer + self.n_request)
        A = np.zeros((self.n_offer + self.n_request, self.n_offer * self.n_request))

        for i in range(self.n_offer):
            b[i] = offer[i]
            for j in range(self.n_request):
                A[i, j + i * self.n_request] = 1
                A[self.n_offer + j, j + i * self.n_request] = 1
                b[self.n_offer + j] = request[j]

        self.offer = offer
        self.request = request

        super(TransportProblem, self).__init__(c, A, b, optimize=1)

    def find_solution_admissible(self):
        self.two_phase_find_init_base()
        self.var_base_value = []
        temp_costs = np.array(self.costs, dtype="float64")
        var_base_value = []

        new_base = []

        if self.init_base_method in ["NO", "MC"]:
            i, j = 0, 0
            current_offer = self.offer[:]
            current_request = self.request[:]
            while sum(var_base_value) != sum(self.offer):
                if self.init_base_method == "MC":
                    i, j = np.unravel_index(temp_costs.argmin(), temp_costs.shape)
                    temp_costs[i, j] = np.Inf

                var_index = i * self.n_request + j
                request_possible = current_request[j]
                offer_possible = current_offer[i]
                value = min(request_possible, offer_possible)


                new_base.append(var_index)
                var_base_value.append(value)

                current_request[j] -= value
                current_offer[i] -= value

                if self.init_base_method == "NO":
                    if current_request[j] == 0:
                        j += 1
                    else:
                        i += 1
                else:
                    if current_request[j] == 0:
                        temp_costs[:,j] += np.Inf
                    if current_offer[i] == 0:
                        temp_costs[i,:] += np.Inf
        else:
            new_base = self.init_base_method

        if self.init_base_method == "MC":
            var = 0
            while len(new_base) != self.n_offer + self.n_request - 1 and var != self.n_offer * self.n_request:
                if var not in new_base:
                    new_base.append(var)
                var += 1

        self.set_base(new_base)
        return True

    def save_step(self, var_in, var_out):
        v = []
        for i in range(self.n_request):
            v.append(self.costs[0][i] + self.c[i, 0])
        u = [0]
        for i in range(1, self.n_offer):
            u.append(self.costs[i][0] - v[0] + self.c[i * self.n_request, 0])
        self.steps.append(
            TransportProblemStep(self.costs, self.c, self.n_offer, self.n_request, self.base, self.var_base_value,
                                 var_in,
                                 var_out, u, v))

    def __str__(self):
        self.two_phase_simplex = None  # pour ne pas print les infos du 2 phases
        return super(TransportProblem, self).__str__()


if __name__ == "__main__":
    # exemple 1
    offer = [1000, 1500, 1200]
    request = [2300, 1400]
    costs = [
        [80, 215],
        [100, 108],
        [102, 68]
    ]
    # transport = TransportProblem(costs, request, offer)

    # exemple 2
    offer = [15, 25, 10]
    request = [5, 15, 15, 15]
    costs = [
        [10, 2, 20, 11],
        [12, 7, 9, 20],
        [4, 14, 16, 18]
    ]
    # transport = TransportProblem(costs, request, offer, init_base_method=[1,5,6,7,8,11])
    transport = TransportProblem(costs, request, offer, init_base_method=[1,6,7,8,9,11])

    transport.solve()
    print(transport)
