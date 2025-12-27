#!/usr/bin/env python3
# 康威生命游戏主程序

import sys
import time
from src.grid import Grid
from src.evolution import Evolution
from src.config import DEFAULT_GRID_WIDTH, DEFAULT_GRID_HEIGHT

def main():
    """主程序入口"""
    print("康威生命游戏 - 物种演化版")
    print("=" * 50)
    
    # 创建网格
    grid = Grid(width=DEFAULT_GRID_WIDTH, height=DEFAULT_GRID_HEIGHT)
    evolution = Evolution(grid)
    
    # 随机初始化网格
    grid.randomize(density=0.2)
    
    # 执行演化演示
    print(f"初始网格大小: {grid.get_size()}")
    print(f"初始存活细胞数量: {len(grid.get_live_cells())}")
    
    # 运行演化循环
    for generation in range(100):
        # 执行一次演化
        evolution.evolve(delta_time=0.1)
        
        # 每10代打印一次状态
        if generation % 10 == 0:
            live_cells = len(grid.get_live_cells())
            species_list = evolution.get_species_manager().get_species_list()
            print(f"\n第 {generation+1} 代:")
            print(f"  存活细胞数量: {live_cells}")
            print(f"  物种数量: {len(species_list)}")
            
            # 打印物种阶段分布
            stage_counts = {}
            for species in species_list:
                stage_counts[species.stage] = stage_counts.get(species.stage, 0) + 1
            
            if stage_counts:
                print("  物种阶段分布:", end=" ")
                for stage in sorted(stage_counts.keys()):
                    print(f"阶段{stage}: {stage_counts[stage]}", end=" ")
                print()
    
    print("\n" + "=" * 50)
    print("演化演示完成")
    print(f"最终存活细胞数量: {len(grid.get_live_cells())}")
    print(f"最终物种数量: {len(evolution.get_species_manager().get_species_list())}")

if __name__ == "__main__":
    main()
