# 物种管理模块
from typing import List, Tuple, Set, Dict
from src.grid import Grid
from src.config import SPECIES_STAGES

class Species:
    def __init__(self, group: Set[Tuple[int, int]], stage: int = 1):
        """初始化物种"""
        self.group = group
        self.stage = stage
        self.survival_time = 0.0  # 分钟
        self.evolution_progress = 0.0  # 0.0 到 1.0
    
    def update_survival_time(self, delta_time: float) -> None:
        """更新生存时间"""
        self.survival_time += delta_time
        # 更新演化进度
        current_requirement = SPECIES_STAGES[self.stage]['time_requirement']
        next_stage = self.stage + 1
        if next_stage in SPECIES_STAGES:
            next_requirement = SPECIES_STAGES[next_stage]['time_requirement']
            if current_requirement < next_requirement:
                self.evolution_progress = min(1.0, 
                    (self.survival_time - current_requirement) / 
                    (next_requirement - current_requirement))
            else:
                self.evolution_progress = 1.0
        else:
            self.evolution_progress = 1.0
    
    def can_evolve(self) -> bool:
        """检查是否可以演化到下一阶段"""
        next_stage = self.stage + 1
        if next_stage not in SPECIES_STAGES:
            return False  # 已经是最高阶段
        
        next_requirement = SPECIES_STAGES[next_stage]['time_requirement']
        return self.survival_time >= next_requirement
    
    def evolve(self) -> bool:
        """演化到下一阶段"""
        if self.can_evolve():
            self.stage += 1
            self.evolution_progress = 0.0
            return True
        return False
    
    def can_devolve(self) -> bool:
        """检查是否需要退化到下一阶段"""
        return self.stage > 1
    
    def devolve(self) -> bool:
        """退化到下一阶段"""
        if self.can_devolve():
            self.stage -= 1
            self.survival_time = 0.0  # 重置生存时间
            self.evolution_progress = 0.0
            return True
        return False
    
    def get_size_requirement(self) -> int:
        """获取当前阶段的大小要求"""
        return SPECIES_STAGES[self.stage]['size']
    
    def get_color(self) -> Tuple[int, int, int]:
        """获取当前阶段的颜色"""
        return SPECIES_STAGES[self.stage]['color']

class SpeciesManager:
    def __init__(self, grid: Grid):
        """初始化物种管理器"""
        self.grid = grid
        self.species_list: List[Species] = []
    
    def update(self, groups: List[Set[Tuple[int, int]]], delta_time: float) -> None:
        """更新所有物种状态"""
        # 简单实现：重新检测物种
        self.species_list.clear()
        
        for group in groups:
            # 基于群体大小和生存时间确定初始阶段
            stage = self._determine_initial_stage(len(group))
            species = Species(group, stage)
            self.species_list.append(species)
            # 更新生存时间
            species.update_survival_time(delta_time)
    
    def _determine_initial_stage(self, group_size: int) -> int:
        """基于群体大小确定初始阶段"""
        for stage in sorted(SPECIES_STAGES.keys(), reverse=True):
            if group_size >= SPECIES_STAGES[stage]['size']:
                return stage
        return 1
    
    def process_evolution(self) -> None:
        """处理所有物种的演化"""
        for species in self.species_list:
            # 检查是否可以演化
            if species.can_evolve():
                # 检查是否有足够的空间演化
                if self._has_enough_space(species):
                    species.evolve()
            
            # 检查是否需要退化
            if len(species.group) < species.get_size_requirement():
                species.devolve()
    
    def _has_enough_space(self, species: Species) -> bool:
        """检查物种是否有足够的空间演化到下一阶段"""
        next_stage = species.stage + 1
        if next_stage not in SPECIES_STAGES:
            return False
        
        next_size = SPECIES_STAGES[next_stage]['size']
        # 检查群体大小是否满足下一阶段的大小要求
        return len(species.group) >= next_size
    
    def get_species_at(self, x: int, y: int) -> Species:
        """获取指定位置的物种"""
        for species in self.species_list:
            if (x, y) in species.group:
                return species
        return None
    
    def get_species_list(self) -> List[Species]:
        """获取所有物种列表"""
        return self.species_list.copy()
