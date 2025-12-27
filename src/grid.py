# 网格管理模块
from typing import List, Tuple, Set, Dict
import random
from src.config import (
    DEFAULT_GRID_WIDTH, DEFAULT_GRID_HEIGHT,
    DEFAULT_BOUNDARY_TYPE, BOUNDARY_TYPES
)

class Grid:
    def __init__(self, width: int = DEFAULT_GRID_WIDTH, height: int = DEFAULT_GRID_HEIGHT, 
                 boundary_type: str = DEFAULT_BOUNDARY_TYPE):
        """初始化网格"""
        self.width = width
        self.height = height
        self.boundary_type = boundary_type
        # 使用二维列表存储网格状态，0表示死亡，1表示存活
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        # 使用集合存储存活细胞的坐标，提高查询效率
        self.live_cells = set()
    
    def reset(self) -> None:
        """重置网格"""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.live_cells.clear()
    
    def randomize(self, density: float = 0.3) -> None:
        """随机初始化网格"""
        self.reset()
        for i in range(self.height):
            for j in range(self.width):
                if random.random() < density:
                    self.set_cell(i, j, 1)
    
    def set_cell(self, x: int, y: int, state: int) -> None:
        """设置单个细胞状态"""
        if 0 <= x < self.height and 0 <= y < self.width:
            self.grid[x][y] = state
            if state == 1:
                self.live_cells.add((x, y))
            else:
                self.live_cells.discard((x, y))
    
    def get_cell(self, x: int, y: int) -> int:
        """获取单个细胞状态，处理边界条件"""
        if self.boundary_type == BOUNDARY_TYPES['periodic']:
            # 周期性边界处理
            x = x % self.height
            y = y % self.width
            return self.grid[x][y]
        else:
            # 固定边界处理
            if 0 <= x < self.height and 0 <= y < self.width:
                return self.grid[x][y]
            else:
                return 0
    
    def count_live_neighbors(self, x: int, y: int) -> int:
        """计算单个细胞的存活邻居数量"""
        count = 0
        # 检查8个邻居
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor_x, neighbor_y = x + dx, y + dy
                count += self.get_cell(neighbor_x, neighbor_y)
        return count
    
    def get_size(self) -> Tuple[int, int]:
        """获取网格大小"""
        return (self.height, self.width)
    
    def get_live_cells(self) -> Set[Tuple[int, int]]:
        """获取所有存活细胞"""
        return self.live_cells.copy()
    
    def load_pattern(self, pattern: List[Tuple[int, int]]) -> None:
        """加载预设模式"""
        self.reset()
        for (x, y) in pattern:
            if 0 <= x < self.height and 0 <= y < self.width:
                self.set_cell(x, y, 1)
    
    def clear_area(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """清空指定区域"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.set_cell(x, y, 0)
    
    def copy(self) -> 'Grid':
        """创建网格副本"""
        new_grid = Grid(self.width, self.height, self.boundary_type)
        new_grid.grid = [row.copy() for row in self.grid]
        new_grid.live_cells = self.live_cells.copy()
        return new_grid
