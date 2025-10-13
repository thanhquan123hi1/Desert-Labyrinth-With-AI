from Package_Algorithm import UninformedSearch, InformedSearch, LocalSearch, NOOBS, AndOrSearch, Backtracking, ForwardChecking
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

        # Uninformed Search 
        if name in ["BFS", "DFS"]:
            self.search = UninformedSearch(self.map_model, start, goal)
            self.visited_states, self.path = getattr(self.search, name)()

        # Informed Search
        elif name in ["Greedy", "A*"]:
            self.search = InformedSearch(self.map_model, start, goal)
            self.visited_states, self.path = (
                self.search.Greedy() if name == "Greedy" else self.search.Astar()
            )

        # Local Search 
        elif name in ["Beam", "SA"]:
            self.search = LocalSearch(self.map_model, start, goal)
            self.visited_states, self.path = (
                self.search.BeamSearch() if name == "Beam" else self.search.SimulatedAnnealingSearch()
            )

        #  NoOBS 
        elif name == "NoOBS":
            matrix = self.map_model.collision_matrix
            starts = find_start_beliefs(matrix, 3)
            goals = find_goal_beliefs(matrix, 3)

            # Khởi tạo thuật toán NoOBS
            self.search = NOOBS(matrix, starts, goals)

            # Chạy và nhận kết quả: chuỗi belief (mỗi belief = tập toạ độ)
            belief_path = self.search.search()

            # 🔹 visited_states & path = cùng là chuỗi belief
            self.visited_states = belief_path if belief_path else []
            self.path = belief_path if belief_path else []

            # Gán lại start/goal để panel Detail hiển thị đúng
            self.search.starts = starts
            self.search.goals = goals

            print(f"[NoOBS] Độ dài đường đi belief: {len(self.path)}")
            
        #  And-Or Search 
        elif name == "AndOrS":
            self.search = AndOrSearch(self.map_model, start, goal)
            self.visited_states, self.path = self.search.AndOrSearch()
        
        #  Backtracking (CSP) 
        elif name == "Backtrack":
            self.search = Backtracking(self.map_model, start, goal)
            self.visited_states, self.path = self.search.run()

        #  Forward Checking (CSP)
        elif name == "Forward":
            self.search = ForwardChecking(self.map_model, start, goal)
            self.visited_states, self.path = self.search.run()

        # Trả kết quả thống kê
        info = self.search.thong_so() if self.search else {}
        return self.search, self.visited_states, self.path, info

    # -------------------------------------------------------------
    def get_info(self):
        """Lấy thông tin hiện tại của thuật toán để hiển thị trên Information Panel."""
        if self.search:
            return self.search.thong_so()
        return {}
