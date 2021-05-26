from SimplexSolver import *


class TransportProblem(SimplexSolver):
    def __init__(self, costs, request, offer):
        """
        Solve Transport Problem
        :param costs: matrix of costs
        :param request: list of requests for each center
        :param offer: list of offer for each center
        """

        self.n_offer = len(offer)
        self.n_request = len(request)

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

    def find_solution_admissiblesss(self):
        self.base = []
        self.var_base_value = []

        i, j = 0, 0
        current_offer = self.offer[:]
        current_request = self.request[:]
        while sum(self.var_base_value) != sum(self.offer):
            var_index = i * self.n_request + j
            self.base.append(var_index)
            request_possible = current_request[j]
            offer_possible = current_offer[i]
            value = min(request_possible, offer_possible)
            self.var_base_value.append(value)

            current_request[j] -= value
            current_offer[i] -= value

            if current_request[j] == 0:
                j += 1
            else:
                i += 1


        self.put_solution_in_base()
        return True

    def save_step(self, var_in, var_out):
        super().save_step(var_in, var_out)


if __name__ == "__main__":
    # exemple 1
    offer = [1000, 1500, 1200]
    request = [2300, 1400]
    costs = [
        [80, 215],
        [100, 108],
        [102, 68]
    ]
    #transport = TransportProblem(costs, request, offer)


    # exemple 2
    offer = [15, 25, 10]
    request = [5, 15, 15, 15]
    costs = [
        [10, 2, 20, 11],
        [12, 7, 9, 20],
        [4, 14, 16, 18]
    ]
    transport = TransportProblem(costs, request, offer)
    transport.solve()
    print(transport._solution_str())
