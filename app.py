#!/usr/bin/env python3
# 康威生命游戏Web应用

from flask import Flask, render_template, jsonify, request
from src.grid import Grid
from src.evolution import Evolution
from src.config import DEFAULT_GRID_WIDTH, DEFAULT_GRID_HEIGHT

app = Flask(__name__)

# 全局游戏状态
class GameState:
    def __init__(self):
        self.grid = Grid(width=DEFAULT_GRID_WIDTH, height=DEFAULT_GRID_HEIGHT)
        self.evolution = Evolution(self.grid)
        self.generation = 0
        self.is_running = False

# 创建游戏实例
game = GameState()

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html', 
                         width=game.grid.width, 
                         height=game.grid.height,
                         generation=game.generation)

@app.route('/api/grid')
def get_grid():
    """获取当前网格状态"""
    return jsonify({
        'grid': game.grid.grid,
        'live_cells': list(game.grid.get_live_cells()),
        'generation': game.generation
    })

@app.route('/api/species')
def get_species():
    """获取当前物种状态"""
    species_list = game.evolution.get_species_manager().get_species_list()
    species_data = []
    
    for species in species_list:
        species_data.append({
            'group': list(species.group),
            'stage': species.stage,
            'survival_time': species.survival_time,
            'evolution_progress': species.evolution_progress
        })
    
    return jsonify({
        'species': species_data,
        'species_count': len(species_data)
    })

@app.route('/api/evolve', methods=['POST'])
def evolve():
    """执行一次演化"""
    game.evolution.evolve(delta_time=0.1)
    game.generation += 1
    
    return jsonify({
        'success': True,
        'generation': game.generation,
        'live_cells': len(game.grid.get_live_cells())
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    """重置游戏"""
    game.grid.reset()
    game.generation = 0
    game.is_running = False
    # 重置物种管理器，确保清空物种列表
    game.evolution = Evolution(game.grid)
    
    return jsonify({
        'success': True,
        'generation': game.generation,
        'live_cells': 0
    })

@app.route('/api/randomize', methods=['POST'])
def randomize():
    """随机初始化网格"""
    density = request.json.get('density', 0.3)
    game.grid.randomize(density=density)
    game.generation = 0
    game.is_running = False
    
    return jsonify({
        'success': True,
        'generation': game.generation,
        'live_cells': len(game.grid.get_live_cells())
    })

@app.route('/api/toggle_cell', methods=['POST'])
def toggle_cell():
    """切换单个细胞状态"""
    x = request.json.get('x')
    y = request.json.get('y')
    
    if x is not None and y is not None:
        current_state = game.grid.grid[x][y]
        new_state = 1 - current_state
        game.grid.set_cell(x, y, new_state)
        
        return jsonify({
            'success': True,
            'x': x,
            'y': y,
            'state': new_state
        })
    
    return jsonify({'success': False})

@app.route('/api/generate_center', methods=['POST'])
def generate_center():
    """从画布中间生成指定数量的细胞"""
    count = request.json.get('count', 100)
    centerX = request.json.get('centerX', game.grid.width // 2)
    centerY = request.json.get('centerY', game.grid.height // 2)
    
    # 重置网格
    game.grid.reset()
    game.generation = 0
    game.is_running = False
    
    # 生成指定数量的细胞，分布在中心点周围
    import random
    radius = min(game.grid.width, game.grid.height) // 4
    cells_generated = 0
    
    while cells_generated < count:
        # 在中心点周围随机生成坐标
        dx = random.randint(-radius, radius)
        dy = random.randint(-radius, radius)
        x = centerY + dy  # 注意x和y的对应关系
        y = centerX + dx
        
        # 检查坐标是否在网格范围内
        if 0 <= x < game.grid.height and 0 <= y < game.grid.width:
            # 设置细胞为存活状态
            game.grid.set_cell(x, y, 1)
            cells_generated += 1
    
    return jsonify({
        'success': True,
        'generation': game.generation,
        'live_cells': cells_generated
    })

@app.route('/api/toggle_run', methods=['POST'])
def toggle_run():
    """切换游戏运行状态"""
    game.is_running = not game.is_running
    return jsonify({
        'success': True,
        'is_running': game.is_running
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
