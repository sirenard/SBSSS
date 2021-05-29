# SBSSS

Step By Step Simplex Solver is an insane simplex solver that generates and shows all the algorithm steps. Yes it has
already been done, but I'm actually bored.

## Utilisation (flemme de faire en anglais)

Tous les print sont au format markdown.

### Simplexe

Pour un problème:

min 30 x_1 + 40 x_2  
s.t.

* 1 x_1 + 2 x_2 - 1 s1 >= 8.0
* 2 x_1 + 2 x_2 - 1 s2 >= 11.0
* 1 x_1 + 1 s3 <= 5.0

```python
from src.SimplexSolver import *

c = [30, 40]
A = [
  [1, 2],
  [2, 2],
  [1, 0]
]
b = [8, 11, 5]
x = ["x_1", "x_2"]

simplex_solver = SimplexSolver(c, A, b, x, optimize=1, equality=[">=", ">=", "<="])
simplex_solver.solve()
print(simplex_solver)  # texte au format markdown
```

* optimize: 1 si min, -1 si max (par défaut -1)
* equality: liste des signe des contraintes (>=, <=, =). Par défaut "=" pour toutes les contraintes
* x: nom des variables. Par défaut x1, x2, ...

#### Fonctionnalités

* Ajoute des variables de slacks (de manière bête, une par contrainte) pour le moment
* Exécute le 2 phases si nécéssaire

### Problème de transport

| | 1 | 2 | 3| Offre |
|:--: | :--: | :--: | :--: | :--: |
| 1 |10 | 2 | 20 | 11 | 15 |
| 2 |12 | 7 | 9 | 20 | 25 | | 3
|4 |14 | 16 | 18 | 10 |
| Demande | 5 | 15 | 15 | 15 | |

```python
from src.TransportProblem import *

offer = [15, 25, 10]
request = [5, 15, 15, 15]
costs = [
  [10, 2, 20, 11],
  [12, 7, 9, 20],
  [4, 14, 16, 18]
]
transport = TransportProblem(costs, request, offer)
transport.solve()
print(transport)  # format markdown
```

#### Note

* On peut modifier la méthode pour choisir la base initiale en modifiant le paramètre init_base_method à la
  construction:
  * "NO" pour nord ouest (fonctionne bien) (par défaut)
  * "MC" pour les moindre coûts (peu tester, n'a pas l'air de fonctionner si une var en base est nulle)
  * liste d'indice de variable pour définir la base manuellement

## Problème de flot max

Exemple:

```python
from src.FlotMax import FlotMax

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
```

### Note

* Il est possible de donner une solution initiale en ajoutant une valeur aux tuples des arrêtes concernée. Par
  exemple: `("s", "B", 2, 1)` pour une arrête avec une capacité de 2 et un flot initial de 2.
    * Le solver ne vérifie pas que la solution initiale est valide
