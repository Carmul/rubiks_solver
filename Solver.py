from Cube import Cube
from tqdm import tqdm
import random

all_actions = ("R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'")


def build_heuristics(state: str, actions, max_moves = 20, heuristic = None):
    if heuristic is None:
        heuristic = {state: 0}
    que = [(state, 0)]
    node_count = sum([len(actions) ** (x + 1) for x in range(max_moves)])
    with tqdm(total=node_count, desc='Heuristic DB') as pbar:
        while True:
            if not que:
                break
            s, d = que.pop(0)
            for a in actions:
                cube = Cube(s)
                cube.turn(a)
                a_str = cube.stringify()
                if a_str not in heuristic or heuristic[a_str] > d + 1:
                    heuristic[a_str] = d + 1
                if d+1 < max_moves:
                    que.append((a_str, d+1))
                pbar.update(1)
    return heuristic


class Solver():

    def __init__(self, heuristic, max_depth = 20):
        
        self.max_depth = max_depth
        self.threshold = max_depth
        self.min_threshold = None
        self.heuristic = heuristic
        self.moves = []
        
    def h(self, state):
        """Return heuristic for state (fallback to max_depth if unknown)."""
        return self.heuristic.get(state, self.max_depth)


    def search(self, state, g_score):
            """
            Input: state - string representing the current state of the cube
                g_score - integer representing the cost to reach the current node
            Description: search the game tree using the IDA* algorithm
            Output: boolean representing if the cube has been solved
            """
            cube = Cube(state=state)
            if cube.is_solved():
                return True
            elif len(self.moves) >= self.threshold:
                return False
            min_val = float('inf')
            best_action = None
            for a in all_actions:
                cube = Cube(state=state)
                cube.turn(a)
                if cube.is_solved():
                    self.moves.append(a)
                    return True
                cube_str = cube.stringify()
                h_score = self.heuristic[cube_str] if cube_str in self.heuristic else self.max_depth
                f_score = g_score + h_score
                if f_score < min_val:
                    min_val = f_score
                    best_action = [(cube_str, a)]
                elif f_score == min_val:
                    if best_action is None:
                        best_action = [(cube_str, a)]
                    else:
                        best_action.append((cube_str, a))
            if best_action is not None:
                if self.min_threshold is None or min_val < self.min_threshold:
                    self.min_threshold = min_val
                next_action = random.choice(best_action)
                self.moves.append(next_action[1])
                status = self.search(next_action[0], g_score + 1)
                if status: return status
            return False
        
        
    def run(self, state):
        """
        Input: state - string representing the current state of the cube
        Description: solve the rubix cube
        Output: list containing the moves taken to solve the cube
        """
        while True:
            status = self.search(state, 1)
            if status: return self.moves
            self.moves = []
            self.threshold = self.min_threshold
        