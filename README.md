# SBSSS
Step By Step Simplex Solver is an insane simplex solver that generates and shows all the algorithm steps. Yes it has already been done, but I'm actually bored. 

## Utilisation (flemme de faire en anglais)

Pour un problème:

min  30 x_1 + 40 x_2  
s.t.

* 1 x_1 + 2 x_2 - 1 s1 >= 8.0
* 2 x_1 + 2 x_2 - 1 s2 >= 11.0
* 1 x_1 + 1 s3 <= 5.0

```
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
print(simplex_solver)
```
* optimize: 1 si min, -1 si max (par défaut -1)
* equality: liste des signe des contraintes (>=, <=, =). Par défaut "=" pour toutes les contraintes
* x: nom des variables. Par défaut x1, x2, ...

## Fonctionnalités

* Ajoute des variables de slacks (de manière bête, une par contrainte) pour le moment
* Exécute le 2 phases si nécéssaire
