from Package_Algorithm import UninformedSearch, InformedSearch, LocalSearch, NOOBS
from Package_Algorithm.NoOBS import find_start_beliefs, find_goal_beliefs

class AlgorithmManager:
    def __init__(self, map_model):
        self.map_model = map_model
        self.search = None
        self.visited_states = []
        self.path = []
        self.selected_alg = None

    # -------------------------------------------------------------
    def run_algorithm(self, name, start, goal):
        """Chạy thuật toán tương ứng và trả về (search, visited_states, path, info)."""
        self.selected_alg = name
        self.visited_states, self.path = [], []
        self.search = None

        if name in ["BFS", "DFS"]:
            self.search = UninformedSearch(self.map_model, start, goal)
            self.visited_states, self.path = getattr(self.search, name)()

        elif name in ["Greedy", "A*"]:
            self.search = InformedSearch(self.map_model, start, goal)
            self.visited_states, self.path = (
                self.search.Greedy() if name == "Greedy" else self.search.Astar()
            )

        elif name in ["Beam", "SA"]:
            self.search = LocalSearch(self.map_model, start, goal)
            self.visited_states, self.path = (
                self.search.BeamSearch() if name == "Beam" else self.search.SimulatedAnnealingSearch()
            )

        elif name == "NoOBS":
            matrix = self.map_model.collision_matrix
            starts = find_start_beliefs(matrix, 3)
            goals  = find_goal_beliefs(matrix, 3)
            self.search = NOOBS(matrix, starts, goals)
            belief_path = self.search.search()
            # visited_states là chuỗi belief (mỗi belief = tập toạ độ)
            self.visited_states = [list(b) for b in belief_path] if belief_path else []
            # NoOBS không trả về path đơn trị (rời rạc)
            self.path = []

        info = self.search.thong_so() if self.search else {}
        return self.search, self.visited_states, self.path, info

    # -------------------------------------------------------------
    def get_info(self):
        """Cho Information Panel mỗi frame."""
        if self.search:
            return self.search.thong_so()
        return {}
