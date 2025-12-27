# 群体检测模块
from typing import List, Tuple, Set, Dict
from src.grid import Grid

class GroupDetection:
    def __init__(self, grid: Grid):
        """初始化群体检测模块"""
        self.grid = grid
        self.height, self.width = grid.get_size()
    
    def detect_groups(self) -> List[Set[Tuple[int, int]]]:
        """检测所有相连的细胞群体"""
        visited = set()
        groups = []
        
        # 遍历所有存活细胞
        for (x, y) in self.grid.get_live_cells():
            if (x, y) not in visited:
                # 使用深度优先搜索检测群体
                group = self._dfs(x, y, visited)
                groups.append(group)
        
        return groups
    
    def _dfs(self, x: int, y: int, visited: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """深度优先搜索检测单个群体"""
        stack = [(x, y)]
        visited.add((x, y))
        group = set()
        
        while stack:
            current_x, current_y = stack.pop()
            group.add((current_x, current_y))
            
            # 检查8个邻居
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    neighbor_x, neighbor_y = current_x + dx, current_y + dy
                    neighbor_state = self.grid.get_cell(neighbor_x, neighbor_y)
                    
                    if neighbor_state == 1 and (neighbor_x, neighbor_y) not in visited:
                        stack.append((neighbor_x, neighbor_y))
                        visited.add((neighbor_x, neighbor_y))
        
        return group
    
    def get_group_id(self, x: int, y: int, groups: List[Set[Tuple[int, int]]]) -> int:
        """获取细胞所属的群体ID"""
        for i, group in enumerate(groups):
            if (x, y) in group:
                return i
        return -1  # 不属于任何群体
    
    def calculate_group_center(self, group: Set[Tuple[int, int]]) -> Tuple[float, float]:
        """计算群体的中心坐标"""
        if not group:
            return (0, 0)
        
        total_x = sum(x for x, y in group)
        total_y = sum(y for x, y in group)
        count = len(group)
        
        return (total_x / count, total_y / count)
