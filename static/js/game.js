// 康威生命游戏前端逻辑

class GameOfLife {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.cellSize = 4; // 每个细胞的像素大小
        this.isRunning = false;
        this.animationId = null;
        this.evolutionSpeed = 1000; // ms per evolution (1秒)
        this.autoRefreshId = null; // 自动刷新的定时器ID
        this.refreshInterval = 2500; // 刷新间隔，2.5秒
        
        // 物种阶段基础颜色（浅色）
        this.baseStageColors = [
            '#cccccc',  // 阶段1: 浅灰色
            '#ffcccc',  // 阶段2: 浅红色
            '#ccffcc',  // 阶段3: 浅绿色
            '#ccccff',  // 阶段4: 浅蓝色
            '#ffffcc',  // 阶段5: 浅黄色
            '#ffccff',  // 阶段6: 浅紫色
            '#ccffff',  // 阶段7: 浅青色
            '#e6ccff'   // 阶段8: 浅粉紫色
        ];
        
        // 物种阶段目标颜色（深色）
        this.targetStageColors = [
            '#000000',  // 阶段1: 黑色
            '#ff0000',  // 阶段2: 红色
            '#00ff00',  // 阶段3: 绿色
            '#0000ff',  // 阶段4: 蓝色
            '#ffff00',  // 阶段5: 黄色
            '#ff00ff',  // 阶段6: 紫色
            '#00ffff',  // 阶段7: 青色
            '#800080'   // 阶段8: 深紫色
        ];
        
        this.init();
        // 绑定所有事件
        this.bindEvents();
        this.bindCellSizeEvent();
        this.bindSpeedEvent();
        this.update();
    }
    
    init() {
        // 设置画布大小
        this.gridWidth = 200;
        this.gridHeight = 200;
        this.canvas.width = this.gridWidth * this.cellSize;
        this.canvas.height = this.gridHeight * this.cellSize;
        
        // 初始化游戏状态
        this.grid = [];
        this.species = [];
        this.generation = 0;
        this.liveCells = 0;
        this.speciesCount = 0;
        this.evolutionTime = 0; // 演化时间（秒）
        this.cellCount = 8000; // 初始细胞数量
        this.cellDensity = 0.2; // 初始细胞密度
    }
    
    bindEvents() {
        // 按钮事件
        document.getElementById('run-btn').addEventListener('click', () => this.toggleRun());
        document.getElementById('step-btn').addEventListener('click', () => this.step());
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());
        document.getElementById('random-btn').addEventListener('click', () => this.randomize());
        
        // 细胞数量滑块事件
        const cellCountSlider = document.getElementById('cell-count');
        const cellCountValue = document.getElementById('cell-count-value');
        cellCountSlider.addEventListener('input', (e) => {
            this.cellCount = parseInt(e.target.value);
            cellCountValue.textContent = this.cellCount;
            // 根据细胞数量更新密度
            const totalCells = this.gridWidth * this.gridHeight;
            this.cellDensity = this.cellCount / totalCells;
            document.getElementById('density-slider').value = this.cellDensity;
            document.getElementById('density-value').textContent = `密度: ${Math.round(this.cellDensity * 100)}%`;
        });
        
        // 密度滑块事件
        const densitySlider = document.getElementById('density-slider');
        const densityValue = document.getElementById('density-value');
        densitySlider.addEventListener('input', (e) => {
            this.cellDensity = parseFloat(e.target.value);
            densityValue.textContent = `密度: ${Math.round(this.cellDensity * 100)}%`;
            // 根据密度更新细胞数量
            const totalCells = this.gridWidth * this.gridHeight;
            this.cellCount = Math.round(this.cellDensity * totalCells);
            document.getElementById('cell-count').value = this.cellCount;
            document.getElementById('cell-count-value').textContent = this.cellCount;
        });
        
        // 画布事件
        this.canvas.addEventListener('click', (e) => this.toggleCell(e));
        this.canvas.addEventListener('mousedown', (e) => {
            this.isDrawing = true;
            this.toggleCell(e);
        });
        this.canvas.addEventListener('mouseup', () => {
            this.isDrawing = false;
        });
        this.canvas.addEventListener('mousemove', (e) => {
            if (this.isDrawing) {
                this.toggleCell(e);
            }
        });
    }
    
    bindCellSizeEvent() {
        // 细胞大小滑块事件
        const cellSizeSlider = document.getElementById('cell-size');
        const cellSizeValue = document.getElementById('cell-size-value');
        
        // 设置初始值
        cellSizeValue.textContent = `${this.cellSize}px`;
        
        cellSizeSlider.addEventListener('input', (e) => {
            const newCellSize = parseInt(e.target.value);
            cellSizeValue.textContent = `${newCellSize}px`;
            this.setCellSize(newCellSize);
        });
    }
    
    bindSpeedEvent() {
        // 速度滑块事件
        const speedSlider = document.getElementById('speed-slider');
        const speedValue = document.getElementById('speed-value');
        
        // 设置初始值
        speedValue.textContent = `${(this.evolutionSpeed / 1000).toFixed(1)}秒`;
        
        speedSlider.addEventListener('input', (e) => {
            const newSpeed = parseInt(e.target.value);
            this.evolutionSpeed = newSpeed;
            speedValue.textContent = `${(newSpeed / 1000).toFixed(1)}秒`;
        });
    }
    
    setCellSize(newSize) {
        // 更新细胞大小
        this.cellSize = newSize;
        
        // 重新计算画布大小
        this.canvas.width = this.gridWidth * this.cellSize;
        this.canvas.height = this.gridHeight * this.cellSize;
        
        // 重新渲染画布
        this.render();
    }
    
    startAutoRefresh() {
        // 开始自动刷新画板，每隔2.5秒刷新一次
        if (!this.autoRefreshId) {
            this.autoRefreshId = setInterval(async () => {
                await this.update();
            }, this.refreshInterval);
        }
    }
    
    stopAutoRefresh() {
        // 停止自动刷新画板
        if (this.autoRefreshId) {
            clearInterval(this.autoRefreshId);
            this.autoRefreshId = null;
        }
    }
    
    async toggleRun() {
        this.isRunning = !this.isRunning;
        const btn = document.getElementById('run-btn');
        btn.textContent = this.isRunning ? '暂停' : '开始';
        
        // 更新游戏状态显示
        const statusElement = document.getElementById('game-status');
        statusElement.textContent = this.isRunning ? '进行中' : '暂停';
        
        if (this.isRunning) {
            // 检查是否有细胞，如果没有则从中间生成初始细胞，使用用户设置的细胞数
            if (this.liveCells === 0) {
                await this.generateCenterCells(this.cellCount);
            }
            await this.evolveLoop();
            // 开始实时刷新画板
            this.startAutoRefresh();
        } else {
            // 停止实时刷新画板
            this.stopAutoRefresh();
        }
    }
    
    async generateCenterCells(count) {
        // 重置网格
        await this.reset();
        
        // 计算画布中心点
        const centerX = Math.floor(this.gridWidth / 2);
        const centerY = Math.floor(this.gridHeight / 2);
        
        // 生成指定数量的细胞，分布在中心点周围
        const response = await fetch('/api/generate_center', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                count: count,
                centerX: centerX,
                centerY: centerY
            })
        });
        
        const data = await response.json();
        if (data.success) {
            await this.update();
        }
    }
    
    async evolveLoop() {
        while (this.isRunning) {
            await this.evolve();
            await this.sleep(this.evolutionSpeed);
        }
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    async step() {
        await this.evolve();
    }
    
    async reset() {
        this.isRunning = false;
        document.getElementById('run-btn').textContent = '开始';
        this.evolutionTime = 0; // 重置演化时间
        
        // 更新游戏状态显示
        const statusElement = document.getElementById('game-status');
        statusElement.textContent = '暂停';
        
        // 停止自动刷新画板
        this.stopAutoRefresh();
        
        const response = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        if (data.success) {
            this.update();
        }
    }
    
    async randomize() {
        // 使用细胞数量来生成初始网格
        const response = await fetch('/api/randomize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ density: this.cellDensity })
        });
        
        const data = await response.json();
        if (data.success) {
            this.update();
        }
    }
    
    async evolve() {
        const response = await fetch('/api/evolve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        if (data.success) {
            this.evolutionTime += 1; // 每次演化增加1秒
            this.update();
        }
    }
    
    async toggleCell(event) {
        // 计算点击的细胞坐标
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / this.cellSize);
        const y = Math.floor((event.clientY - rect.top) / this.cellSize);
        
        if (x >= 0 && x < this.gridWidth && y >= 0 && y < this.gridHeight) {
            const response = await fetch('/api/toggle_cell', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ x: x, y: y })
            });
            
            const data = await response.json();
            if (data.success) {
                this.update();
            }
        }
    }
    
    async update() {
        // 更新网格数据
        await this.updateGrid();
        // 更新物种数据
        await this.updateSpecies();
        // 更新界面显示
        this.render();
        this.updateUI();
    }
    
    async updateGrid() {
        const response = await fetch('/api/grid');
        const data = await response.json();
        
        this.grid = data.grid;
        this.generation = data.generation;
        this.liveCells = data.live_cells.length;
    }
    
    async updateSpecies() {
        const response = await fetch('/api/species');
        const data = await response.json();
        
        this.species = data.species;
        this.speciesCount = data.species_count;
    }
    
    render() {
        // 清空画布
        this.ctx.fillStyle = '#fafafa';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制网格线
        this.ctx.strokeStyle = '#e0e0e0';
        this.ctx.lineWidth = 0.5;
        
        for (let x = 0; x <= this.gridWidth; x++) {
            this.ctx.beginPath();
            this.ctx.moveTo(x * this.cellSize, 0);
            this.ctx.lineTo(x * this.cellSize, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.gridHeight; y++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y * this.cellSize);
            this.ctx.lineTo(this.canvas.width, y * this.cellSize);
            this.ctx.stroke();
        }
        
        // 绘制存活细胞和物种
        this.renderSpecies();
    }
    
    // 颜色插值函数：从浅色到深色的渐变
    interpolateColor(baseColor, targetColor, progress) {
        // 将十六进制颜色转换为RGB
        const parseHex = (hex) => {
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            return { r, g, b };
        };
        
        const base = parseHex(baseColor);
        const target = parseHex(targetColor);
        
        // 计算插值后的RGB值
        const r = Math.round(base.r + (target.r - base.r) * progress);
        const g = Math.round(base.g + (target.g - base.g) * progress);
        const b = Math.round(base.b + (target.b - base.b) * progress);
        
        // 转换回十六进制
        return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
    }
    
    renderSpecies() {
        // 计算颜色渐变进度（基于世代数，每100代完成从浅色到深色的过渡）
        const colorProgress = Math.min(1.0, this.generation / 100);
        
        // 绘制存活细胞
        for (let i = 0; i < this.gridHeight; i++) {
            for (let j = 0; j < this.gridWidth; j++) {
                if (this.grid[i][j] === 1) {
                    this.ctx.fillStyle = '#f0f0f0'; // 默认浅灰色，物种会覆盖这个颜色
                    this.ctx.fillRect(j * this.cellSize, i * this.cellSize, this.cellSize - 1, this.cellSize - 1);
                }
            }
        }
        
        // 绘制物种，按阶段从低到高绘制，高级物种覆盖低级物种
        this.species.forEach(species => {
            const stage = species.stage - 1; // 索引从0开始
            
            // 根据世代数计算当前阶段的颜色（从浅色到深色渐变）
            const baseColor = this.baseStageColors[stage % this.baseStageColors.length];
            const targetColor = this.targetStageColors[stage % this.targetStageColors.length];
            const color = this.interpolateColor(baseColor, targetColor, colorProgress);
            
            // 绘制物种的每个细胞
            species.group.forEach(([x, y]) => {
                this.ctx.fillStyle = color;
                this.ctx.fillRect(y * this.cellSize, x * this.cellSize, this.cellSize - 1, this.cellSize - 1);
                
                // 为高级物种添加边框（边框颜色也随世代加深）
                if (stage >= 1) {
                    const borderColor = this.interpolateColor('#e0e0e0', '#333333', colorProgress);
                    this.ctx.strokeStyle = borderColor;
                    this.ctx.lineWidth = 1;
                    this.ctx.strokeRect(y * this.cellSize, x * this.cellSize, this.cellSize - 1, this.cellSize - 1);
                }
            });
        });
    }
    
    updateUI() {
        // 更新游戏信息
        document.getElementById('generation').textContent = this.generation;
        document.getElementById('live-cells').textContent = this.liveCells;
        document.getElementById('species-count').textContent = this.speciesCount;
        document.getElementById('evolution-time').textContent = `${this.evolutionTime}秒`;
        
        // 更新物种统计
        this.updateSpeciesStats();
        // 更新物种阶段分布
        this.updateStageDistribution();
    }
    
    updateSpeciesStats() {
        const statsDiv = document.getElementById('species-stats');
        
        // 计算阶段分布
        const stageCounts = new Array(8).fill(0);
        this.species.forEach(species => {
            const stage = species.stage - 1;
            if (stage >= 0 && stage < 8) {
                stageCounts[stage]++;
            }
        });
        
        let html = '';
        html += `<div class="species-stat-item">阶段1: ${stageCounts[0]} 个</div>`;
        html += `<div class="species-stat-item">阶段2: ${stageCounts[1]} 个</div>`;
        html += `<div class="species-stat-item">阶段3: ${stageCounts[2]} 个</div>`;
        html += `<div class="species-stat-item">阶段4: ${stageCounts[3]} 个</div>`;
        html += `<div class="species-stat-item">阶段5: ${stageCounts[4]} 个</div>`;
        html += `<div class="species-stat-item">阶段6: ${stageCounts[5]} 个</div>`;
        html += `<div class="species-stat-item">阶段7: ${stageCounts[6]} 个</div>`;
        html += `<div class="species-stat-item">阶段8: ${stageCounts[7]} 个</div>`;
        
        statsDiv.innerHTML = html;
    }
    
    updateStageDistribution() {
        const distributionDiv = document.getElementById('stage-distribution');
        
        // 计算阶段分布
        const stageCounts = new Array(8).fill(0);
        this.species.forEach(species => {
            const stage = species.stage - 1;
            if (stage >= 0 && stage < 8) {
                stageCounts[stage]++;
            }
        });
        
        // 为每个阶段定义对应的图标
        const stageIcons = [
            '<i class="fas fa-microscope"></i>',  // 阶段1：细胞
            '<i class="fas fa-dna"></i>',        // 阶段2：DNA/简单生物
            '<i class="fas fa-seedling"></i>',    // 阶段3：植物
            '<i class="fas fa-bug"></i>',         // 阶段4：昆虫
            '<i class="fas fa-fish"></i>',        // 阶段5：鱼类
            '<i class="fas fa-dragon"></i>',      // 阶段6：爬行动物
            '<i class="fas fa-dog"></i>',         // 阶段7：哺乳动物
            '<i class="fas fa-user"></i>'         // 阶段8：人类
        ];
        
        let html = '';
        for (let i = 0; i < 8; i++) {
            if (stageCounts[i] > 0) {
                html += `
                    <div class="stage-item">
                        <div class="stage-icon">${stageIcons[i]}</div>
                        <div class="stage-color" style="background-color: ${this.baseStageColors[i]}"></div>
                        <div class="stage-info">
                            <div>阶段${i + 1}</div>
                        </div>
                        <div class="stage-count">${stageCounts[i]}</div>
                    </div>
                `;
            }
        }
        
        distributionDiv.innerHTML = html;
    }
}

// 初始化游戏
window.addEventListener('DOMContentLoaded', () => {
    new GameOfLife();
});
