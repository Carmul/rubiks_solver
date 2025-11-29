from Cube import Cube
import Solver

c = Cube()
c.turn("R L U D F D B'")

c.show()

heuristics_db = Solver.build_heuristics(Cube().stringify(), Solver.all_actions, max_moves=4)

my_solver = Solver.Solver(heuristics_db)

moves = my_solver.run(c.stringify())

for m in moves:
    print(m, "")



