from FlotMaxStep import *


class FlotMax:
    def __init__(self, vertex_name, edges):
        """
        Solve a Flot Max problem
        :param edges: list of tuple (vertex source, vertex destination, capacity of the edge, current value of the edge (optional))
        :param vertex_name: list of name for the vertex (the first oone is the source abd the last one the destination)
        """

        n_edges = len(edges)
        n_vertex = len(vertex_name)

        # n_edges + 1 variables, first one is v
        n_var = n_edges + 1
        c = [0 for _ in range(n_var)]
        c[0] = 1

        self.capacity = np.zeros((n_vertex, n_vertex))
        self.solution = np.zeros((n_vertex, n_vertex))
        self.obj = 0
        self.mark = []
        self.n_vertex = n_vertex
        self.vertex_name = vertex_name
        self.edges = edges
        self.steps = []

        for edge in edges:
            i = vertex_name.index(edge[0])
            j = vertex_name.index(edge[1])
            self.capacity[i, j] = edge[2]
            if len(edge) == 4:
                self.solution[i,j] = edge[3]

    def solve(self):
        while self.mark_vertex():
            current = self.vertex_name[-1]
            val = self.mark[current][1]
            increasing_path = []
            while current is not None:
                increasing_path = [current] + increasing_path
                self.increase_solution(current, val)
                current = self.mark[current][0]

            self.save_step(increasing_path, val)
        self.save_step([], 0)

    def increase_solution(self, name, value):
        m = self.mark[name]

        if m[0] is None:
            return
        i = self.vertex_name.index(m[0])
        j = self.vertex_name.index(name)

        if m[2]:
            self.solution[i, j] += value
        else:
            self.solution[j, i] -= value

    def mark_vertex(self):
        self.mark = {}
        L = []
        self.mark[self.vertex_name[0]] = (None, np.Inf, 1)
        L.append(0)
        while len(L) and self.vertex_name[-1] not in self.mark:
            vertex = L.pop(0)
            current_val = self.mark[self.vertex_name[vertex]][1]
            for j in range(self.n_vertex):
                if self.vertex_name[j] not in self.mark:
                    if self.solution[vertex, j] < self.capacity[vertex, j]:
                        val = min(current_val, self.capacity[vertex, j] - self.solution[vertex, j])
                        self.mark[self.vertex_name[j]] = (self.vertex_name[vertex], val, 1)
                        L.append(j)
                    elif self.capacity[j, vertex] and self.solution[j, vertex] > 0:
                        val = min(current_val, self.solution[j, vertex])
                        self.mark[self.vertex_name[j]] = (self.vertex_name[vertex], val, 0)
                        L.append(j)

        return self.vertex_name[-1] in self.mark

    def save_step(self, increasing_path, augmentation):
        obj = sum(self.solution[:, 0])
        self.steps.append(
            FlotMaxStep(self.capacity, self.solution, increasing_path, augmentation, obj, self.vertex_name, self.edges))

    def __str__(self):
        res = ""
        for i, step in enumerate(self.steps):
            res += "# Iteration {}\n\n".format(i + 1)
            res += str(step)

        return res


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
    print(maxFlot)
