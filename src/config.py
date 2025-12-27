# 游戏配置

# 网格默认配置
DEFAULT_GRID_WIDTH = 200
DEFAULT_GRID_HEIGHT = 200
MIN_GRID_SIZE = 100
MAX_GRID_SIZE = 500

# 细胞默认配置
DEFAULT_CELL_SIZE = 4  # 像素
MIN_CELL_SIZE = 2
MAX_CELL_SIZE = 10

# 颜色配置
COLORS = {
    'background': (255, 255, 255),  # 白色背景
    'cell': (0, 0, 0),  # 黑色细胞
    'grid_line': (200, 200, 200),  # 灰色网格线
    'species_stage': [
        (0, 0, 0),        # 阶段1：黑色
        (255, 0, 0),      # 阶段2：红色
        (0, 255, 0),      # 阶段3：绿色
        (0, 0, 255),      # 阶段4：蓝色
        (255, 255, 0),    # 阶段5：黄色
        (255, 0, 255),    # 阶段6：紫色
        (0, 255, 255),    # 阶段7：青色
        (128, 0, 128),    # 阶段8：深紫色
    ],
    'ui_text': (0, 0, 0),  # 黑色文本
    'ui_background': (240, 240, 240),  # 浅灰色UI背景
    'button': (180, 180, 180),  # 按钮颜色
    'button_hover': (200, 200, 200),  # 按钮悬停颜色
}

# 演化配置
DEFAULT_GAME_SPEED = 100  # ms per iteration
MIN_GAME_SPEED = 10
MAX_GAME_SPEED = 1000

DEFAULT_EVOLUTION_SPEED = 1.0  # game time multiplier
MIN_EVOLUTION_SPEED = 0.1
MAX_EVOLUTION_SPEED = 10.0

# 物种演化配置
SPECIES_STAGES = {
    1: {'size': 1, 'time_requirement': 0, 'color': COLORS['species_stage'][0]},
    2: {'size': 2, 'time_requirement': 3, 'color': COLORS['species_stage'][1]},  # 3 minutes
    3: {'size': 4, 'time_requirement': 6, 'color': COLORS['species_stage'][2]},  # 6 minutes
    4: {'size': 8, 'time_requirement': 12, 'color': COLORS['species_stage'][3]},  # 12 minutes
    5: {'size': 16, 'time_requirement': 24, 'color': COLORS['species_stage'][4]},  # 24 minutes
    6: {'size': 32, 'time_requirement': 48, 'color': COLORS['species_stage'][5]},  # 48 minutes
    7: {'size': 64, 'time_requirement': 96, 'color': COLORS['species_stage'][6]},  # 96 minutes
    8: {'size': 128, 'time_requirement': 192, 'color': COLORS['species_stage'][7]},  # 192 minutes
}

# 边界类型
BOUNDARY_TYPES = {
    'fixed': 'fixed',
    'periodic': 'periodic'
}

DEFAULT_BOUNDARY_TYPE = BOUNDARY_TYPES['periodic']
