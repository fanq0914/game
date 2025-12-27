# 演化模块测试
import unittest
from src.grid import Grid
from src.evolution import Evolution
from src.group_detection import GroupDetection
from src.species_manager import SpeciesManager

class TestEvolution(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.grid = Grid(width=10, height=10)
        self.evolution = Evolution(self.grid)
    
    def test_initialization(self):
        """测试演化模块初始化"""
        self.assertIsNotNone(self.evolution)
        self.assertIsNotNone(self.evolution.get_group_detector())
        self.assertIsNotNone(self.evolution.get_species_manager())
    
    def test_glider_pattern(self):
        """测试滑翔机模式演化"""
        # 滑翔机初始模式
        glider = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        self.grid.load_pattern(glider)
        
        # 执行多次演化，检查滑翔机是否移动
        initial_live_cells = self.grid.get_live_cells()
        for _ in range(4):  # 滑翔机每4步回到相似形状
            self.evolution.evolve()
        
        final_live_cells = self.grid.get_live_cells()
        self.assertNotEqual(initial_live_cells, final_live_cells, "滑翔机应该移动")
    
    def test_group_detection(self):
        """测试群体检测功能"""
        # 创建两个独立的群体
        self.grid.set_cell(1, 1, 1)
        self.grid.set_cell(1, 2, 1)
        self.grid.set_cell(2, 1, 1)
        
        self.grid.set_cell(5, 5, 1)
        self.grid.set_cell(5, 6, 1)
        self.grid.set_cell(6, 5, 1)
        
        group_detector = GroupDetection(self.grid)
        groups = group_detector.detect_groups()
        
        self.assertEqual(len(groups), 2, "应该检测到2个群体")
        self.assertEqual(len(groups[0]), 3, "第一个群体应该有3个细胞")
        self.assertEqual(len(groups[1]), 3, "第二个群体应该有3个细胞")
    
    def test_species_evolution(self):
        """测试物种演化功能"""
        # 创建一个稳定的群体（方块模式）
        block = [(1, 1), (1, 2), (2, 1), (2, 2)]
        self.grid.load_pattern(block)
        
        species_manager = SpeciesManager(self.grid)
        group_detector = GroupDetection(self.grid)
        
        # 模拟长时间生存，检查物种演化
        for _ in range(100):  # 模拟10分钟生存时间
            groups = group_detector.detect_groups()
            species_manager.update(groups, 0.1)  # 每次更新0.1分钟
            species_manager.process_evolution()
        
        species_list = species_manager.get_species_list()
        self.assertEqual(len(species_list), 1, "应该只有1个物种")
        
        # 方块群体应该演化到至少阶段2
        self.assertGreaterEqual(species_list[0].stage, 2, "物种应该演化到至少阶段2")
    
    def test_species_devolution(self):
        """测试物种退化功能"""
        # 创建一个大群体
        for i in range(3):
            for j in range(3):
                self.grid.set_cell(i, j, 1)
        
        species_manager = SpeciesManager(self.grid)
        group_detector = GroupDetection(self.grid)
        
        # 模拟长时间生存，让物种演化到高级阶段
        for _ in range(200):
            groups = group_detector.detect_groups()
            species_manager.update(groups, 0.1)
            species_manager.process_evolution()
        
        # 破坏群体，减少细胞数量
        self.grid.set_cell(0, 0, 0)
        self.grid.set_cell(0, 1, 0)
        self.grid.set_cell(0, 2, 0)
        
        # 更新物种状态，检查是否退化
        groups = group_detector.detect_groups()
        species_manager.update(groups, 0.1)
        species_manager.process_evolution()
        
        species_list = species_manager.get_species_list()
        self.assertEqual(len(species_list), 1, "应该只有1个物种")
        
        # 群体缩小后应该退化
        self.assertLessEqual(species_list[0].stage, 3, "物种应该退化到阶段3或更低")
    
    def test_empty_grid_evolution(self):
        """测试空网格演化"""
        # 确保空网格演化后仍然是空的
        for _ in range(5):
            self.evolution.evolve()
        
        self.assertEqual(len(self.grid.get_live_cells()), 0, "空网格演化后应该仍然是空的")
    
    def test_full_grid_evolution(self):
        """测试满网格演化"""
        # 填充整个网格
        for i in range(10):
            for j in range(10):
                self.grid.set_cell(i, j, 1)
        
        # 执行演化，满网格应该大部分细胞死亡
        self.evolution.evolve()
        live_cells_count = len(self.grid.get_live_cells())
        
        # 满网格演化后应该只有少数细胞存活（根据康威规则）
        self.assertLess(live_cells_count, 50, "满网格演化后应该只有少数细胞存活")

if __name__ == '__main__':
    unittest.main()
