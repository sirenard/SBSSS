import numpy as np


class FlotMaxStep:
    def __init__(self, capacity, sol, increasing_path, augmentation, obj, vertex_name, edges):
        self.capacyty = np.copy(capacity)
        self.sol = np.copy(sol)
        self.increasing_path = list(map(str, increasing_path[:]))
        self.augmentation = augmentation
        self.obj = obj
        self.vertex_name = vertex_name
        self.edges = edges

    def __str__(self):
        res = ""

        res += "* Flot actuel: {}\n".format(self.obj)
        res += "* Chemin augmentant: " + ", ".join(self.increasing_path) + "\n"
        res += "* Flot sur le chemin a augmenté de {} \n".format(self.augmentation)
        res += "* Solution actuelle:\n"

        for edge in self.edges:
            i = self.vertex_name.index(edge[0])
            j = self.vertex_name.index(edge[1])

            res += "\t* {}->{}: {}/{}\n".format(edge[0], edge[1], self.sol[i, j], edge[2])

        return res + "\n"