from SimplexSolver import *


class FlotMax(SimplexSolver):
    def __init__(self, vertex_name, edges):
        """
        Solve a Flot Max problem
        :param edges: list of tuple (vertex source, vertex destination, capacity of the edge)
        :param vertex_name: list of name for the vertex (the first oone is the source abd the last one the destination)
        """

        n_edges = len(edges)
        n_vertex = len(vertex_name)

        # n_edges + 1 variables, first one is v
        n_var = n_edges + 1
        c = [0 for i in range(n_var)]
        c[0] = 1

        A = []
        b = []
        equality = []
        for i in range(n_vertex):
            flux_conservation_constraint = [0 for _ in range(n_var)]
            name = vertex_name[i]
            for j, edge in enumerate(edges):
                if name == edge[0]:  # vertex is a source of this edge
                    flux_conservation_constraint[j + 1] = 1
                elif name == edge[1]:  # vertex is a destination of this edge
                    flux_conservation_constraint[j + 1] = -1

            if i == 0:  # source
                flux_conservation_constraint[0] = -1
            elif i == n_vertex - 1:  # destination
                flux_conservation_constraint[0] = 1

            A.append(flux_conservation_constraint)
            b.append(0)
            equality.append("=")

        for i in range(n_edges):
            flux_limit = [0 for _ in range(n_var)]
            flux_limit[i + 1] = 1
            A.append(flux_limit)
            b.append(edges[i][2])
            equality.append("<=")

        super(FlotMax, self).__init__(c, A, b, optimize=-1, equality=equality)


if __name__ == "__main__":
    vertex_name = ["s", "A", "B", "t"]
    edges = [
        ("s", "A", 1),
        ("s", "B", 2),
        ("B", "A", 3),
        ("A", "t", 4),
        ("B", "t", 5)
    ]

    maxFlot = FlotMax(vertex_name, edges)
    maxFlot.solve()
    print(maxFlot.obj)
