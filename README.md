# Desert Labyrinth With AI (MazeGame)

Trò chơi mô phỏng **AI Search Algorithms** trong mê cung bằng **Pygame**, giúp trực quan hóa quá trình tìm đường của các thuật toán AI

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cài đặt môi trường](#cài-đặt-môi-trường)
- [Hướng dẫn chơi](#hướng-dẫn-chơi)
  - [Màn hình Menu](#màn-hình-menu)
  - [Màn hình Options](#màn-hình-options)
  - [Màn hình Game](#màn-hình-game)
- [Các thuật toán hỗ trợ](#các-thuật-toán-hỗ-trợ)

## Giới thiệu

**Desert Labyrinth With AI** cho phép quan sát từng bước hoạt động của các thuật toán tìm đường trong mê cung (maze):
- Hiển thị *visited*, *path*, và *goal*.
- Có thể chọn *bản đồ*, *nhân vật*, *môi trường*, và *hiệu ứng* khác nhau.
- So sánh *thời gian chạy*, *số trạng thái đã sinh/đã duyệt*, và *độ dài đường đi* qua biểu đồ và bảng thống kê.

## Cấu trúc thư mục
```
Desert-Labyrinth-With-AI/
│
├── main.py # Chạy toàn bộ game (vòng lặp chính)
├── settings.py # Cấu hình kích thước, TILE_SIZE, độ phân giải
├── ui.py # Hệ thống UI (panel, button, text,…)
│
├── map_model.py # Quản lý các map (.tmx)
├── player.py
├── tile.py 
│
├── Package_Core/ # Logic điều phối chính
│ ├── algorithm_manager.py # Quản lý gọi thuật toán và thống kê
│ ├── game_renderer.py # Hiển thị bản đồ, visited, path, goal
│ └── ...
│
├── Package_Algorithm/ # Các thuật toán AI
│ ├── UninformedSearch.py
│ ├── InformedSearch.py
│ ├── LocalSearch.py
│ ├── NoOBS.py
│ ├── AndOrSearch.py
│ ├── Backtracking.py
│ ├── ForwardChecking.py
│ └── ...
│
├── Package_Panel/
│ ├── panel_history.py # Lịch sử chạy thuật toán
│ ├── panel_pathview.py # Chi tiết đường đi
│ ├── panel_chart.py # Biểu đồ so sánh hiệu năng
│ └── ...
│
├── Package_Menu/ # Menu và Options
│ ├── menu.py
│ ├── options.py
│ ├── panel_bg.py # Chọn background
│ ├── panel_map.py # Chọn map
│ ├── panel_player.py # Chọn nhân vật
│ ├── panel_effects.py # Chọn hiệu ứng môi trường
│ └── ...
│
├── Package_Animation/
│ ├── animation.py
│ ├── particle.py
│ ├── transition.py
│ └── ...
├── Resources/ 
```

## Cài đặt môi trường
Yêu cầu Python ≥ **3.9** và thư viện sau:
```bash
pip install pygame numpy pytmx matplotlib
```

## Hướng dẫn chơi

### Màn hình Menu

- **START GAME** → bắt đầu trò chơi.  
- **OPTIONS** → chọn nhân vật, bản đồ, hiệu ứng, nền.  
- **QUIT** → thoát chương trình.  

### Màn hình Options

Tại đây bạn có thể tùy chỉnh:

| Thành phần | Mô tả |
|-------------|-------|
| **Background** | Chọn môi trường: Desert, Snow, Forest, Jungle, Cave,… |
| **Map** | Chọn bản đồ mê cung (Map1–Map5) |
| **Player** | Nhân vật hoạt hình: Torchman, Blue, Yellow, Red |
| **Effect** | Hiệu ứng môi trường: Sandstorm, Snow, Rain, Leaves, Fireflies |

> Nhấn **Back** để lưu cấu hình và quay lại Menu chính.

### Màn hình Game

- Bên phải là **Information Panel** hiển thị thông tin thuật toán.  
- Chọn thuật toán trong khung **Algorithm Panel**.  
- Nhấn **Detail** để xem chi tiết đường đi.  
- Nhấn **History** để xem lịch sử các lần chạy.  
- Nhấn **Chart** để xem biểu đồ so sánh hiệu năng.  

## Các thuật toán hỗ trợ
| Nhóm | Thuật toán | Ghi chú |
|------|-------------|---------|
| **Uninformed Search** | BFS, DFS | Không dùng heuristic |
| **Informed Search** | Greedy, A* | Dựa vào heuristic Manhattan |
| **Local Search** | Beam Search, Simulated Annealing | Không duyệt toàn bộ cây |
| **NoOBS** | Nondeterministic Search with Belief States | Tìm đường với quan sát không đầy đủ |
| **CSP** | Backtracking, Forward Checking | Giải ràng buộc trên mê cung |
| **And-Or Search** |  | Áp dụng cho không gian AND/OR |
| **Adversarial Search** | *(đang phát triển)* | Người chơi vs kẻ địch |
