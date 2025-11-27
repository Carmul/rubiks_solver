from Cube import Cube

c = Cube()

c.pprint()

print(c.is_solved())

c.turn("R")

c.pprint()

print(c.is_solved())

print(c.stringify())

s = c.stringify()

Cube(s).pprint()

