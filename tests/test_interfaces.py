# 接口测试用例
import unittest
from src.grid import Grid
from src.group_detection import GroupDetection
from src.species_manager import SpeciesManager, Species
from src.evolution import Evolution

class TestGridInterface(unittest.TestCase):
    """测试网格管理模块接口"""
    
    def setUp(self):
        """设置测试环境"""
        self.grid = Grid(width=10, height=10)
    
    def test_set_and_get_cell(self):
        """测试设置和获取细胞状态"""
        # 设置细胞状态
        self.grid.set_cell(0, 0, 1)
        self.grid.set_cell(0, 1, 0)
        
        # 验证细胞状态
        self.assertEqual(self.grid.get_cell(0, 0), 1)
        self.assertEqual(self.grid.get_cell(0, 1), 0)
    
    def test_count_live_neighbors(self):
        """测试计算存活邻居数量"""
        # 创建一个3x3的存活细胞块
        for i in range(3):
            for j in range(3):
                self.grid.set_cell(i, j, 1)
        
        # 中心细胞应该有8个存活邻居
        self.assertEqual(self.grid.count_live_neighbors(1, 1), 8)
        
        # 边缘细胞应该有5个存活邻居
        self.assertEqual(self.grid.count_live_neighbors(0, 0), 3)
    
    def test_get_live_cells(self):
        """测试获取存活细胞"""
        # 设置一些存活细胞
        self.grid.set_cell(0, 0, 1)
        self.grid.set_cell(0, 1, 1)
        self.grid.set_cell(1, 0, 1)
        
        live_cells = self.grid.get_live_cells()
        expected = {(0, 0), (0, 1), (1, 0)}
        self.assertEqual(live_cells, expected)
    
    def test_reset(self):
        """测试重置网格"""
        # 设置一些存活细胞
        self.grid.set_cell(0, 0, 1)
        self.grid.set_cell(0, 1, 1)
        
        # 重置网格
        self.grid.reset()
        
        # 验证网格为空
        self.assertEqual(len(self.grid.get_live_cells()), 0)
    
    def test_randomize(self):
        """测试随机初始化网格"""
        # 随机初始化网格
        self.grid.randomize(density=0.5)
        
        # 验证网格中有存活细胞
        live_cells = len(self.grid.get_live_cells())
        self.assertGreater(live_cells, 0)
        self.assertLess(live_cells, 100)  # 10x10网格，密度0.5，应该有50左右的存活细胞

class TestGroupDetectionInterface(unittest.TestCase):
    """测试群体检测模块接口"""
    
    def setUp(self):
        """设置测试环境"""
        self.grid = Grid(width=10, height=10)
        self.group_detector = GroupDetection(self.grid)
    
    def test_detect_single_group(self):
        """测试检测单个群体"""
        # 创建一个3x3的存活细胞块
        for i in range(3):
            for j in range(3):
                self.grid.set_cell(i, j, 1)
        
        groups = self.group_detector.detect_groups()
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 9)
    
    def test_detect_multiple_groups(self):
        """测试检测多个独立群体"""
        # 创建两个独立的群体
        # 第一个群体
        for i in range(2):
            for j in range(2):
                self.grid.set_cell(i, j, 1)
        
        # 第二个群体
        for i in range(6, 8):
            for j in range(6, 8):
                self.grid.set_cell(i, j, 1)
        
        groups = self.group_detector.detect_groups()
        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0]), 4)
        self.assertEqual(len(groups[1]), 4)
    
    def test_get_group_id(self):
        """测试获取细胞所属的群体ID"""
        # 创建两个独立的群体
        self.grid.set_cell(0, 0, 1)
        self.grid.set_cell(0, 1, 1)
        self.grid.set_cell(6, 6, 1)
        self.grid.set_cell(6, 7, 1)
        
        groups = self.group_detector.detect_groups()
        
        # 第一个群体的细胞应该属于群体0
        self.assertEqual(self.group_detector.get_group_id(0, 0, groups), 0)
        self.assertEqual(self.group_detector.get_group_id(0, 1, groups), 0)
        
        # 第二个群体的细胞应该属于群体1
        self.assertEqual(self.group_detector.get_group_id(6, 6, groups), 1)
        self.assertEqual(self.group_detector.get_group_id(6, 7, groups), 1)
        
        # 死亡细胞应该不属于任何群体
        self.assertEqual(self.group_detector.get_group_id(3, 3, groups), -1)
    
    def test_calculate_group_center(self):
        """测试计算群体中心"""
        # 创建一个2x2的存活细胞块
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        center = self.group_detector.calculate_group_center(group)
        
        # 2x2群体的中心应该是(0.5, 0.5)
        self.assertEqual(center, (0.5, 0.5))
        
        # 创建一个1x3的存活细胞块
        group = {(0, 0), (0, 1), (0, 2)}
        center = self.group_detector.calculate_group_center(group)
        
        # 1x3群体的中心应该是(0, 1)
        self.assertEqual(center, (0, 1))

class TestSpeciesInterface(unittest.TestCase):
    """测试物种模块接口"""
    
    def setUp(self):
        """设置测试环境"""
        self.grid = Grid(width=10, height=10)
        self.species_manager = SpeciesManager(self.grid)
    
    def test_species_initialization(self):
        """测试物种初始化"""
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        species = Species(group)
        
        self.assertEqual(species.stage, 1)
        self.assertEqual(species.survival_time, 0.0)
        self.assertEqual(species.evolution_progress, 0.0)
    
    def test_update_survival_time(self):
        """测试更新生存时间"""
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        species = Species(group)
        
        # 更新生存时间
        species.update_survival_time(1.0)  # 1分钟
        self.assertEqual(species.survival_time, 1.0)
        
        species.update_survival_time(2.0)  # 再2分钟
        self.assertEqual(species.survival_time, 3.0)
    
    def test_can_evolve(self):
        """测试是否可以演化"""
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        species = Species(group)
        
        # 初始阶段，生存时间为0，不应该可以演化
        self.assertFalse(species.can_evolve())
        
        # 更新生存时间到3分钟，应该可以演化到阶段2
        species.survival_time = 3.0
        self.assertTrue(species.can_evolve())
    
    def test_evolve(self):
        """测试演化功能"""
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        species = Species(group)
        species.survival_time = 3.0
        
        # 演化到阶段2
        result = species.evolve()
        self.assertTrue(result)
        self.assertEqual(species.stage, 2)
        self.assertEqual(species.evolution_progress, 0.0)
    
    def test_devolve(self):
        """测试退化功能"""
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        species = Species(group, stage=2)
        species.survival_time = 1.0
        
        # 退化到阶段1
        result = species.devolve()
        self.assertTrue(result)
        self.assertEqual(species.stage, 1)
        self.assertEqual(species.survival_time, 0.0)
        self.assertEqual(species.evolution_progress, 0.0)
    
    def test_get_size_requirement(self):
        """测试获取大小要求"""
        group = {(0, 0)}
        species = Species(group)
        
        self.assertEqual(species.get_size_requirement(), 1)  # 阶段1
        
        species.stage = 2
        self.assertEqual(species.get_size_requirement(), 2)  # 阶段2
        
        species.stage = 3
        self.assertEqual(species.get_size_requirement(), 4)  # 阶段3

class TestSpeciesManagerInterface(unittest.TestCase):
    """测试物种管理器接口"""
    
    def setUp(self):
        """设置测试环境"""
        self.grid = Grid(width=10, height=10)
        self.species_manager = SpeciesManager(self.grid)
    
    def test_update_species(self):
        """测试更新物种"""
        # 创建一个群体
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.grid.set_cell(0, 0, 1)
        self.grid.set_cell(0, 1, 1)
        self.grid.set_cell(1, 0, 1)
        self.grid.set_cell(1, 1, 1)
        
        # 更新物种
        self.species_manager.update([group], 1.0)
        
        # 应该有一个物种
        species_list = self.species_manager.get_species_list()
        self.assertEqual(len(species_list), 1)
        
        # 物种生存时间应该是1.0
        self.assertEqual(species_list[0].survival_time, 1.0)
    
    def test_determine_initial_stage(self):
        """测试确定初始阶段"""
        # 小群体应该是阶段1
        stage = self.species_manager._determine_initial_stage(1)
        self.assertEqual(stage, 1)
        
        # 中等群体应该是阶段2
        stage = self.species_manager._determine_initial_stage(2)
        self.assertEqual(stage, 2)
        
        # 大群体应该是阶段3
        stage = self.species_manager._determine_initial_stage(5)
        self.assertEqual(stage, 3)
    
    def test_process_evolution(self):
        """测试处理演化"""
        # 创建一个足够大的群体（8个细胞，满足阶段4的大小要求）
        group = {(0, 0), (0, 1), (0, 2), (0, 3),
                 (1, 0), (1, 1), (1, 2), (1, 3)}  # 8个细胞
        for cell in group:
            self.grid.set_cell(cell[0], cell[1], 1)
        
        # 创建一个物种，设置生存时间为12分钟，应该可以演化到阶段4
        species = Species(group, stage=3)  # 手动设置为阶段3
        species.survival_time = 12.0
        
        # 添加到物种管理器
        self.species_manager.species_list.append(species)
        
        # 处理演化
        self.species_manager.process_evolution()
        
        # 物种应该演化到阶段4
        self.assertEqual(species.stage, 4)
    
    def test_get_species_at(self):
        """测试获取指定位置的物种"""
        # 创建一个群体
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.grid.set_cell(0, 0, 1)
        self.grid.set_cell(0, 1, 1)
        self.grid.set_cell(1, 0, 1)
        self.grid.set_cell(1, 1, 1)
        
        # 更新物种
        self.species_manager.update([group], 1.0)
        
        # 获取物种
        species = self.species_manager.get_species_at(0, 0)
        self.assertIsNotNone(species)
        
        # 获取不存在的物种
        species = self.species_manager.get_species_at(5, 5)
        self.assertIsNone(species)

class TestEvolutionInterface(unittest.TestCase):
    """测试演化模块接口"""
    
    def setUp(self):
        """设置测试环境"""
        self.grid = Grid(width=10, height=10)
        self.evolution = Evolution(self.grid)
    
    def test_evolution_initialization(self):
        """测试演化模块初始化"""
        self.assertIsNotNone(self.evolution)
        self.assertIsNotNone(self.evolution.get_group_detector())
        self.assertIsNotNone(self.evolution.get_species_manager())
    
    def test_evolve_once(self):
        """测试执行一次演化"""
        # 创建一个简单的初始模式
        self.grid.set_cell(0, 1, 1)
        self.grid.set_cell(1, 2, 1)
        self.grid.set_cell(2, 0, 1)
        self.grid.set_cell(2, 1, 1)
        self.grid.set_cell(2, 2, 1)
        
        initial_live_cells = self.grid.get_live_cells()
        
        # 执行一次演化
        self.evolution.evolve()
        
        final_live_cells = self.grid.get_live_cells()
        self.assertNotEqual(initial_live_cells, final_live_cells)
    
    def test_evolve_multiple_times(self):
        """测试执行多次演化"""
        # 创建一个稳定的初始模式（方块）
        self.grid.set_cell(1, 1, 1)
        self.grid.set_cell(1, 2, 1)
        self.grid.set_cell(2, 1, 1)
        self.grid.set_cell(2, 2, 1)
        
        initial_live_cells = self.grid.get_live_cells()
        
        # 执行多次演化，稳定模式应该保持不变
        for _ in range(5):
            self.evolution.evolve()
        
        final_live_cells = self.grid.get_live_cells()
        self.assertEqual(initial_live_cells, final_live_cells, "稳定模式应该保持不变")
    
    def test_evolution_with_species(self):
        """测试带有物种的演化"""
        # 创建一个稳定的初始模式（方块）
        self.grid.set_cell(1, 1, 1)
        self.grid.set_cell(1, 2, 1)
        self.grid.set_cell(2, 1, 1)
        self.grid.set_cell(2, 2, 1)
        
        # 执行多次演化，让物种演化
        for _ in range(50):  # 50次演化，每次0.1分钟，共5分钟
            self.evolution.evolve(delta_time=0.1)
        
        # 获取物种列表
        species_list = self.evolution.get_species_manager().get_species_list()
        self.assertEqual(len(species_list), 1)
        
        # 物种应该演化到阶段2
        self.assertGreaterEqual(species_list[0].stage, 2)

if __name__ == '__main__':
    unittest.main()
