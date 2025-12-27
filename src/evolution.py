# 细胞演化模块
from typing import List, Tuple, Set, Dict
from src.grid import Grid
from src.group_detection import GroupDetection
from src.species_manager import SpeciesManager

class Evolution:
    def __init__(self, grid: Grid):
        """初始化演化模块"""
        self.grid = grid
        self.group_detector = GroupDetection(grid)
        self.species_manager = SpeciesManager(grid)
    
    def evolve(self, delta_time: float = 0.1) -> None:
        """执行一次演化循环"""
        # 1. 检测当前群体
        groups = self.group_detector.detect_groups()
        
        # 2. 更新物种生存时间
        self.species_manager.update(groups, delta_time)
        
        # 3. 处理物种演化
        self.species_manager.process_evolution()
        
        # 4. 创建新网格用于存储下一状态
        new_grid = [[0 for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        
        # 5. 应用基础演化规则更新每个细胞
        for x in range(self.grid.height):
            for y in range(self.grid.width):
                current_state = self.grid.grid[x][y]
                live_neighbors = self.grid.count_live_neighbors(x, y)
                
                # 应用康威生命游戏规则
                if current_state == 1:
                    # 存活细胞
                    if live_neighbors in [2, 3]:
                        new_grid[x][y] = 1  # 继续存活
                    else:
                        new_grid[x][y] = 0  # 死亡
                else:
                    # 死亡细胞
                    if live_neighbors == 3:
                        new_grid[x][y] = 1  # 出生
                    else:
                        new_grid[x][y] = 0  # 保持死亡
        
        # 6. 更新网格状态
        self._update_grid_state(new_grid)
    
    def _update_grid_state(self, new_grid: List[List[int]]) -> None:
        """更新网格状态"""
        # 清空现有状态
        self.grid.live_cells.clear()
        
        # 更新网格和存活细胞集合
        for x in range(self.grid.height):
            for y in range(self.grid.width):
                self.grid.grid[x][y] = new_grid[x][y]
                if new_grid[x][y] == 1:
                    self.grid.live_cells.add((x, y))
    
    def get_species_manager(self) -> SpeciesManager:
        """获取物种管理器"""
        return self.species_manager
    
    def get_group_detector(self) -> GroupDetection:
        """获取群体检测器"""
        return self.group_detector
