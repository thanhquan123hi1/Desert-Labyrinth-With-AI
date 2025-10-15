from Package_Algorithm import UninformedSearch, InformedSearch, LocalSearch, NOOBS, AndOrSearch, Backtracking, ForwardChecking, AdversarialSearch
from Package_Algorithm.NoOBS import find_start_beliefs, find_goal_beliefs



class AlgorithmManager:
    def __init__(self, map_model):
        self.map_model = map_model
        self.search = None
        self.visited_states = []
        self.path = []
        self.selected_alg = None

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

            belief_path = self.search.search()

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
            
        #  Adversarial 
        elif name in ["Minimax", "AlphaBeta"]:
            mat = self.map_model.collision_matrix
            enemy_pos = None
            for r in range(mat.shape[0]):
                for c in range(mat.shape[1]):
                    if mat[r, c] == 3:
                        enemy_pos = (r, c)
                        break
                if enemy_pos:
                    break
            if not enemy_pos:
                enemy_pos = (18, 28)

            # Khởi tạo thuật toán rượt đuổi cơ bản
            self.search = AdversarialSearch(
                map_model=self.map_model,
                start=start,
                enemy_start=enemy_pos,
                goals=[goal],
                max_depth=4,
                step_limit=200
            )


            if name == "Minimax":
                player_path, enemy_path = self.search.run_minimax()
            else:
                player_path, enemy_path = self.search.run_alphabeta()

            self.visited_states = []
            self.path = player_path
            self.search.duong_di_player = player_path
            self.search.duong_di_enemy = enemy_path

            info = self.search.thong_so()
            return self.search, self.visited_states, self.path, info




        # Trả kết quả thống kê
        if self.search:
            info = self.search.thong_so()
        else:
            info = {}


        return self.search, self.visited_states, self.path, info



    # -------------------------------------------------------------
    def get_info(self):
        """Lấy thông tin hiện tại của thuật toán để hiển thị trên Information Panel."""
        if not self.search:
            return {}

        # Nếu là AdversarialSearch -> cần truyền player_path và enemy_path
        if hasattr(self.search, "duong_di_player") and hasattr(self.search, "duong_di_enemy"):
            return self.search.thong_so()


        # Các thuật toán khác (BFS, A*, NoOBS, v.v.)
        return self.search.thong_so()

