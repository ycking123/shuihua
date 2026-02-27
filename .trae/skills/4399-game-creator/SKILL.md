---
name: "4399-game-creator"
description: "创建4399风格的对战类格斗游戏，类似死神vs火影。支持角色系统、技能连招、人机对战和双人对战。当用户要求开发4399游戏、格斗游戏或对战游戏时调用此技能。"
---

# 4399游戏创建器 - 对战类格斗游戏开发指南

## 概述

本技能指导开发4399平台风格的横版对战格斗游戏，以《死神vs火影》为参考原型。包含完整的游戏开发流程，从角色设计、技能系统到对战逻辑和UI实现。

---

## 游戏核心特性

### 基础玩法
- **对战模式**：单人vs电脑、双人对战（本地）
- **角色选择**：多个可选角色，每个角色独特技能
- **连招系统**：普通攻击+技能组合
- **血条系统**：实时显示双方生命值
- **能量槽**：积累能量释放必杀技

### 技术规格
- **游戏引擎**：Phaser.js / Pixi.js / 原生HTML5 Canvas
- **分辨率**：800x600 或 1280x720（4399常用）
- **帧率**：60 FPS
- **兼容性**：PC浏览器（Chrome、Firefox、Edge）

---

## 开发准备

### 项目结构
```
4399-fighting-game/
├── index.html              # 游戏入口
├── css/
│   └── style.css          # 样式文件
├── js/
│   ├── main.js            # 游戏主逻辑
│   ├── game.js            # 游戏引擎初始化
│   ├── character.js       # 角色类
│   ├── input.js           # 输入处理
│   ├── combat.js          # 战斗逻辑
│   └── ui.js              # UI管理
├── assets/
│   ├── sprites/           # 角色精灵图
│   ├── backgrounds/       # 背景图
│   ├── effects/          # 特效图
│   └── sounds/           # 音效和BGM
└── data/
    ├── characters.json    # 角色配置
    └── skills.json       # 技能配置
```

### 必需依赖（Phaser.js版本）
```html
<!-- CDN引入 -->
<script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
```

---

## 角色系统设计

### 角色属性结构
```javascript
// data/characters.json
{
  "characters": [
    {
      "id": "character_1",
      "name": "角色名称",
      "health": 1000,
      "energy": 100,
      "speed": 5,
      "sprites": {
        "idle": "sprites/char1/idle.png",
        "walk": "sprites/char1/walk.png",
        "attack": "sprites/char1/attack.png",
        "skill1": "sprites/char1/skill1.png",
        "skill2": "sprites/char1/skill2.png",
        "ultimate": "sprites/char1/ultimate.png",
        "hit": "sprites/char1/hit.png",
        "die": "sprites/char1/die.png"
      },
      "animations": {
        "idle": { "frames": 8, "frameRate": 8 },
        "walk": { "frames": 6, "frameRate": 10 },
        "attack": { "frames": 12, "frameRate": 12 },
        "skill1": { "frames": 20, "frameRate": 15 },
        "skill2": { "frames": 18, "frameRate": 15 },
        "ultimate": { "frames": 30, "frameRate": 20 },
        "hit": { "frames": 3, "frameRate": 10 },
        "die": { "frames": 15, "frameRate": 8 }
      },
      "hitbox": {
        "width": 80,
        "height": 120
      }
    }
  ]
}
```

### 角色类实现
```javascript
// js/character.js
class Character extends Phaser.GameObjects.Container {
  constructor(scene, x, y, config) {
    super(scene, x, y);
    this.scene = scene;
    this.config = config;

    // 基础属性
    this.health = config.health;
    this.maxHealth = config.health;
    this.energy = 0;
    this.maxEnergy = 100;
    this.speed = config.speed;
    this.direction = 1; // 1=右, -1=左
    this.isAttacking = false;
    this.isHit = false;
    this.isDead = false;
    this.combo = 0;
    this.comboTimer = null;

    // 精灵对象
    this.sprite = this.scene.add.sprite(0, 0, config.sprites.idle);
    this.sprite.setScale(this.direction);
    this.add(this.sprite);

    // 碰撞箱
    this.hitbox = new Phaser.Geom.Rectangle(
      -config.hitbox.width/2,
      -config.hitbox.height/2,
      config.hitbox.width,
      config.hitbox.height
    );

    // 生命值条
    this.healthBar = new HealthBar(scene, x, y - 100, this.maxHealth);

    this.scene.add.existing(this);
  }

  update(time, delta, input) {
    if (this.isDead) return;

    // 状态更新
    this.handleInput(input);
    this.sprite.update(time, delta);
    this.healthBar.update(this.health);

    // 连招计时器
    if (this.comboTimer && time > this.comboTimer) {
      this.combo = 0;
      this.comboTimer = null;
    }
  }

  handleInput(input) {
    if (this.isAttacking || this.isHit) return;

    // 移动
    if (input.left) {
      this.x -= this.speed;
      this.direction = -1;
      this.sprite.setScale(this.direction);
      this.playAnimation('walk');
    } else if (input.right) {
      this.x += this.speed;
      this.direction = 1;
      this.sprite.setScale(this.direction);
      this.playAnimation('walk');
    } else {
      this.playAnimation('idle');
    }

    // 攻击
    if (input.attack) {
      this.performAttack('attack');
    }

    // 技能1
    if (input.skill1 && this.energy >= 20) {
      this.performAttack('skill1');
      this.energy -= 20;
    }

    // 技能2
    if (input.skill2 && this.energy >= 40) {
      this.performAttack('skill2');
      this.energy -= 40;
    }

    // 必杀技
    if (input.ultimate && this.energy >= 100) {
      this.performAttack('ultimate');
      this.energy = 0;
    }
  }

  playAnimation(key) {
    const anim = this.config.animations[key];
    if (this.sprite.anims.getName() !== key) {
      this.sprite.play(key);
    }
  }

  performAttack(type) {
    this.isAttacking = true;
    this.playAnimation(type);

    const animConfig = this.config.animations[type];
    const attackDuration = (anim.frames / anim.frameRate) * 1000;

    // 攻击判定延迟
    const hitDelay = attackDuration * 0.3;

    this.scene.time.delayedCall(hitDelay, () => {
      if (this.checkHit()) {
        this.onHitEnemy();
      }
    });

    // 攻击结束
    this.scene.time.delayedCall(attackDuration, () => {
      this.isAttacking = false;
    });
  }

  checkHit() {
    // 获取对手的碰撞箱
    const enemy = this.getEnemy();
    const enemyHitbox = enemy.getBounds();

    // 计算攻击范围
    const attackRange = new Phaser.Geom.Rectangle(
      this.x + (this.direction * 50),
      this.y - 60,
      100,
      120
    );

    return Phaser.Geom.Intersects.RectangleToRectangle(attackRange, enemyHitbox);
  }

  onHitEnemy() {
    const enemy = this.getEnemy();
    const damage = this.calculateDamage();

    enemy.takeDamage(damage);
    this.energy = Math.min(this.energy + 10, this.maxEnergy);

    // 连击加成
    this.combo++;
    this.comboTimer = this.scene.time.now + 1000;

    // 显示伤害数字
    this.showDamageNumber(enemy.x, enemy.y, damage);
  }

  calculateDamage() {
    let baseDamage = 50;
    let comboMultiplier = 1 + (this.combo * 0.1);
    return Math.floor(baseDamage * comboMultiplier);
  }

  takeDamage(damage) {
    if (this.isDead) return;

    this.health -= damage;
    this.isHit = true;
    this.playAnimation('hit');

    if (this.health <= 0) {
      this.health = 0;
      this.die();
    }

    // 受击硬直时间
    this.scene.time.delayedCall(500, () => {
      this.isHit = false;
    });
  }

  die() {
    this.isDead = true;
    this.playAnimation('die');
    this.scene.time.delayedCall(2000, () => {
      this.scene.gameOver();
    });
  }

  showDamageNumber(x, y, damage) {
    const text = this.scene.add.text(x, y - 50, `-${damage}`, {
      fontSize: '32px',
      fontStyle: 'bold',
      color: '#ff0000',
      stroke: '#000',
      strokeThickness: 4
    });

    this.scene.tweens.add({
      targets: text,
      y: y - 100,
      alpha: 0,
      duration: 1000,
      onComplete: () => text.destroy()
    });
  }
}
```

---

## 技能系统

### 技能配置
```javascript
// data/skills.json
{
  "skills": {
    "普通攻击": {
      "type": "attack",
      "damage": 50,
      "energyGain": 10,
      "cooldown": 0,
      "hitbox": { "width": 100, "height": 120 }
    },
    "技能1": {
      "type": "skill",
      "name": "火球术",
      "damage": 120,
      "energyCost": 20,
      "cooldown": 2000,
      "projectile": {
        "speed": 8,
        "sprite": "assets/effects/fireball.png"
      }
    },
    "技能2": {
      "type": "skill",
      "name": "突进斩",
      "damage": 200,
      "energyCost": 40,
      "cooldown": 5000,
      "dashDistance": 200
    },
    "必杀技": {
      "type": "ultimate",
      "name": "终极奥义",
      "damage": 500,
      "energyCost": 100,
      "cooldown": 0,
      "cameraShake": true,
      "screenFlash": true
    }
  }
}
```

---

## 输入系统

### 玩家1控制（键盘）
```javascript
// js/input.js
class InputHandler {
  constructor(scene) {
    this.scene = scene;
    this.keys = scene.input.keyboard.createCursorKeys();

    // WASD移动
    this.wKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
    this.aKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
    this.sKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
    this.dKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);

    // 攻击键
    this.jKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.J); // 普攻
    this.kKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.K); // 技能1
    this.lKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.L); // 技能2
    this.uKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.U); // 必杀技

    this.p1Input = {
      left: () => this.aKey.isDown,
      right: () => this.dKey.isDown,
      up: () => this.wKey.isDown,
      down: () => this.sKey.isDown,
      attack: () => this.justPressed(this.jKey),
      skill1: () => this.justPressed(this.kKey),
      skill2: () => this.justPressed(this.lKey),
      ultimate: () => this.justPressed(this.uKey)
    };
  }

  justPressed(key) {
    return Phaser.Input.Keyboard.JustDown(key);
  }

  getPlayer1Input() {
    return this.p1Input;
  }

  // 玩家2控制（方向键 + 数字键）
  getPlayer2Input() {
    return {
      left: () => this.keys.left.isDown,
      right: () => this.keys.right.isDown,
      up: () => this.keys.up.isDown,
      down: () => this.keys.down.isDown,
      attack: () => this.justPressed(Phaser.Input.Keyboard.KeyCodes.NUMPAD_1),
      skill1: () => this.justPressed(Phaser.Input.Keyboard.KeyCodes.NUMPAD_2),
      skill2: () => this.justPressed(Phaser.Input.Keyboard.KeyCodes.NUMPAD_3),
      ultimate: () => this.justPressed(Phaser.Input.Keyboard.KeyCodes.NUMPAD_0)
    };
  }
}
```

---

## 游戏主循环

```javascript
// js/main.js
class FightingGame extends Phaser.Scene {
  constructor() {
    super({ key: 'FightingGame' });
  }

  preload() {
    // 加载角色资源
    this.loadCharacters();
    // 加载背景
    this.loadBackground();
    // 加载UI资源
    this.loadUI();
  }

  loadCharacters() {
    const characters = this.cache.json.get('characters');
    characters.characters.forEach(char => {
      Object.values(char.sprites).forEach(spritePath => {
        this.load.image(spritePath, spritePath);
      });
    });
  }

  create() {
    // 创建背景
    this.createBackground();

    // 创建输入处理器
    this.inputHandler = new InputHandler(this);

    // 加载角色配置
    const charData = this.cache.json.get('characters');
    const char1Config = charData.characters[0];
    const char2Config = charData.characters[1];

    // 创建角色
    this.player1 = new Character(this, 200, 400, char1Config);
    this.player2 = new Character(this, 600, 400, char2Config);
    this.player2.direction = -1;
    this.player2.sprite.setScale(-1);

    // 创建UI
    this.createUI();

    // 游戏状态
    this.gameMode = 'pve'; // pve 或 pvp
    this.gameTime = 90; // 90秒倒计时
    this.timeEvent = this.time.addEvent({
      delay: 1000,
      callback: this.updateTimer,
      callbackScope: this,
      loop: true
    });
  }

  update(time, delta) {
    // 更新玩家1
    this.player1.update(time, delta, this.inputHandler.getPlayer1Input());

    // 根据模式更新玩家2
    if (this.gameMode === 'pvp') {
      this.player2.update(time, delta, this.inputHandler.getPlayer2Input());
    } else {
      this.updateAI(time, delta);
    }

    // 限制角色在场景内
    this.constrainPlayer(this.player1);
    this.constrainPlayer(this.player2);
  }

  updateAI(time, delta) {
    // 简单AI逻辑
    const p1 = this.player1;
    const p2 = this.player2;
    const distance = Phaser.Math.Distance.Between(p1.x, p1.y, p2.x, p2.y);

    const aiInput = {
      left: false,
      right: false,
      up: false,
      down: false,
      attack: false,
      skill1: false,
      skill2: false,
      ultimate: false
    };

    // AI决策
    if (distance > 300) {
      // 靠近玩家
      if (p1.x < p2.x) aiInput.left = true;
      else aiInput.right = true;
    } else if (distance < 150) {
      // 远离玩家
      if (p1.x < p2.x) aiInput.right = true;
      else aiInput.left = true;
    } else {
      // 攻击
      if (Math.random() < 0.05) aiInput.attack = true;
      if (p2.energy >= 20 && Math.random() < 0.03) aiInput.skill1 = true;
      if (p2.energy >= 100 && Math.random() < 0.01) aiInput.ultimate = true;
    }

    p2.update(time, delta, aiInput);
  }

  constrainPlayer(player) {
    const margin = 50;
    player.x = Phaser.Math.Clamp(
      player.x,
      margin,
      this.scale.width - margin
    );
  }

  updateTimer() {
    this.gameTime--;
    this.timerText.setText(this.gameTime);

    if (this.gameTime <= 0) {
      this.timeEnded();
    }
  }

  timeEnded() {
    this.timeEvent.remove();

    if (this.player1.health > this.player2.health) {
      this.gameOver('player1');
    } else if (this.player2.health > this.player1.health) {
      this.gameOver('player2');
    } else {
      this.gameOver('draw');
    }
  }

  gameOver(winner) {
    this.scene.pause();

    // 显示结果
    const resultText = winner === 'draw' ? '平局！' : `${winner === 'player1' ? '玩家1' : '玩家2'} 获胜！`;
    this.resultText = this.add.text(
      this.scale.width / 2,
      this.scale.height / 2,
      resultText,
      {
        fontSize: '64px',
        fontStyle: 'bold',
        color: '#ffff00',
        stroke: '#000',
        strokeThickness: 6
      }
    ).setOrigin(0.5);

    // 重来按钮
    const retryButton = this.add.text(
      this.scale.width / 2,
      this.scale.height / 2 + 80,
      '再来一局',
      {
        fontSize: '32px',
        backgroundColor: '#4CAF50',
        color: '#fff',
        padding: { x: 20, y: 10 }
      }
    ).setOrigin(0.5);

    retryButton.setInteractive();
    retryButton.on('pointerdown', () => {
      this.scene.restart();
    });
  }

  createUI() {
    // 玩家1血条
    this.p1HealthText = this.add.text(50, 30, '玩家1', {
      fontSize: '20px',
      color: '#fff'
    });

    this.p1HealthBar = this.add.graphics();
    this.updateHealthBar(this.p1HealthBar, 50, 60, 300, 20, '#4CAF50', this.player1.health, this.player1.maxHealth);

    // 玩家2血条
    this.p2HealthText = this.add.text(this.scale.width - 150, 30, '玩家2', {
      fontSize: '20px',
      color: '#fff'
    });

    this.p2HealthBar = this.add.graphics();
    this.updateHealthBar(this.p2HealthBar, this.scale.width - 450, 60, 300, 20, '#4CAF50', this.player2.health, this.player2.maxHealth);

    // 能量条
    this.p1EnergyBar = this.add.graphics();
    this.updateEnergyBar(this.p1EnergyBar, 50, 90, 200, 10, '#2196F3', this.player1.energy, this.player1.maxEnergy);

    this.p2EnergyBar = this.add.graphics();
    this.updateEnergyBar(this.p2EnergyBar, this.scale.width - 350, 90, 200, 10, '#2196F3', this.player2.energy, this.player2.maxEnergy);

    // 倒计时
    this.timerText = this.add.text(
      this.scale.width / 2,
      30,
      this.gameTime.toString(),
      {
        fontSize: '32px',
        fontStyle: 'bold',
        color: '#fff'
      }
    ).setOrigin(0.5);

    // 连击数
    this.comboText = this.add.text(100, 150, '', {
      fontSize: '24px',
      color: '#ff6600',
      fontStyle: 'bold'
    });
  }

  updateHealthBar(graphics, x, y, width, height, color, current, max) {
    graphics.clear();
    graphics.fillStyle(0x333333);
    graphics.fillRect(x, y, width, height);

    const currentWidth = (current / max) * width;
    graphics.fillStyle(parseInt(color.replace('#', '0x')));
    graphics.fillRect(x, y, currentWidth, height);
  }

  updateEnergyBar(graphics, x, y, width, height, color, current, max) {
    graphics.clear();
    graphics.fillStyle(0x333333);
    graphics.fillRect(x, y, width, height);

    const currentWidth = (current / max) * width;
    graphics.fillStyle(parseInt(color.replace('#', '0x')));
    graphics.fillRect(x, y, currentWidth, height);
  }

  createBackground() {
    this.bg = this.add.image(this.scale.width / 2, this.scale.height / 2, 'background');
    this.bg.setDisplaySize(this.scale.width, this.scale.height);
  }

  loadUI() {
    // UI资源加载...
  }

  loadBackground() {
    // 背景资源加载...
  }
}

// 游戏配置
const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#000000',
  scene: [MenuScene, CharacterSelectScene, FightingGame],
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 },
      debug: false
    }
  }
};

// 初始化游戏
const game = new Phaser.Game(config);
```

---

## 角色选择界面

```javascript
// js/character-select.js
class CharacterSelectScene extends Phaser.Scene {
  constructor() {
    super({ key: 'CharacterSelectScene' });
  }

  create() {
    // 背景和标题
    this.add.image(400, 300, 'select_bg');
    this.add.text(400, 50, '选择角色', {
      fontSize: '48px',
      fontStyle: 'bold',
      color: '#fff',
      stroke: '#000',
      strokeThickness: 4
    }).setOrigin(0.5);

    // 加载角色数据
    this.characters = this.cache.json.get('characters').characters;

    // 创建角色卡片
    this.createCharacterCards();

    // 玩家选择
    this.p1Selection = null;
    this.p2Selection = null;

    // 确认按钮
    this.createConfirmButton();
  }

  createCharacterCards() {
    const startX = 150;
    const startY = 200;
    const spacing = 200;

    this.characters.forEach((char, index) => {
      const x = startX + (index % 3) * spacing;
      const y = startY + Math.floor(index / 3) * 180;

      // 角色卡片容器
      const card = this.add.container(x, y);

      // 角色图片
      const sprite = this.add.sprite(0, 0, char.sprites.idle);
      sprite.setScale(1.5);
      card.add(sprite);

      // 角色名称
      const nameText = this.add.text(0, 70, char.name, {
        fontSize: '20px',
        color: '#fff',
        stroke: '#000',
        strokeThickness: 2
      }).setOrigin(0.5);
      card.add(nameText);

      // 选中框
      const selectFrame = this.add.graphics();
      selectFrame.lineStyle(4, 0xffff00);
      selectFrame.strokeRect(-60, -90, 120, 180);
      selectFrame.setVisible(false);
      card.add(selectFrame);

      // 交互
      sprite.setInteractive();
      sprite.on('pointerdown', () => {
        this.selectCharacter(index, selectFrame);
      });

      sprite.on('pointerover', () => {
        sprite.setTint(0xdddddd);
      });

      sprite.on('pointerout', () => {
        sprite.clearTint();
      });

      this.characterCards = this.characterCards || [];
      this.characterCards.push({ card, selectFrame, index });
    });
  }

  selectCharacter(index, frame) {
    // 简单实现：玩家1选择
    this.p1Selection = index;

    // 清除其他选中框
    this.characterCards.forEach(item => {
      item.selectFrame.setVisible(false);
    });

    // 显示当前选中框
    frame.setVisible(true);
  }

  createConfirmButton() {
    const button = this.add.text(400, 520, '开始战斗', {
      fontSize: '32px',
      backgroundColor: '#FF5722',
      color: '#fff',
      padding: { x: 40, y: 15 }
    }).setOrigin(0.5);

    button.setInteractive();

    button.on('pointerdown', () => {
      if (this.p1Selection !== null) {
        this.scene.start('FightingGame', {
          p1: this.p1Selection,
          p2: Math.floor(Math.random() * this.characters.length)
        });
      }
    });

    button.on('pointerover', () => {
      button.setStyle({ backgroundColor: '#FF7043' });
    });

    button.on('pointerout', () => {
      button.setStyle({ backgroundColor: '#FF5722' });
    });
  }
}
```

---

## 特效系统

### 必杀技特效
```javascript
class EffectManager {
  constructor(scene) {
    this.scene = scene;
    this.effects = [];
  }

  playUltimateEffect(character) {
    // 屏幕震动
    this.scene.cameras.main.shake(500, 0.02);

    // 屏幕闪光
    const flash = this.scene.add.rectangle(
      this.scene.scale.width / 2,
      this.scene.scale.height / 2,
      this.scene.scale.width,
      this.scene.scale.height,
      0xffffff
    ).setAlpha(0.8);

    this.scene.tweens.add({
      targets: flash,
      alpha: 0,
      duration: 500,
      onComplete: () => flash.destroy()
    });

    // 技能名称显示
    const skillName = this.scene.add.text(
      this.scene.scale.width / 2,
      this.scene.scale.height / 2 - 100,
      '终极奥义！',
      {
        fontSize: '64px',
        fontStyle: 'bold',
        color: '#ffff00',
        stroke: '#ff0000',
        strokeThickness: 8
      }
    ).setOrigin(0.5);

    this.scene.tweens.add({
      targets: skillName,
      alpha: 0,
      y: skillName.y - 50,
      duration: 1500,
      onComplete: () => skillName.destroy()
    });

    // 伤害数字
    for (let i = 0; i < 10; i++) {
      this.scene.time.delayedCall(i * 100, () => {
        this.showComboHit(character);
      });
    }
  }

  showComboHit(character) {
    const text = this.scene.add.text(
      character.x + Phaser.Math.Between(-50, 50),
      character.y - Phaser.Math.Between(50, 150),
      Math.floor(Phaser.Math.Between(40, 60)).toString(),
      {
        fontSize: '28px',
        fontStyle: 'bold',
        color: '#ff0000',
        stroke: '#fff',
        strokeThickness: 3
      }
    ).setOrigin(0.5);

    this.scene.tweens.add({
      targets: text,
      alpha: 0,
      y: text.y - 30,
      duration: 800,
      onComplete: () => text.destroy()
    });
  }
}
```

---

## 音效系统

```javascript
class AudioManager {
  constructor(scene) {
    this.scene = scene;
  }

  preload() {
    // 预加载音效
    this.scene.load.audio('bgm', 'assets/sounds/bgm.mp3');
    this.scene.load.audio('attack', 'assets/sounds/attack.mp3');
    this.scene.load.audio('skill', 'assets/sounds/skill.mp3');
    this.scene.load.audio('ultimate', 'assets/sounds/ultimate.mp3');
    this.scene.load.audio('hit', 'assets/sounds/hit.mp3');
    this.scene.load.audio('win', 'assets/sounds/win.mp3');
  }

  playBGM() {
    this.bgm = this.scene.sound.play('bgm', { loop: true, volume: 0.5 });
  }

  playAttack() {
    this.scene.sound.play('attack', { volume: 0.7 });
  }

  playSkill() {
    this.scene.sound.play('skill', { volume: 0.8 });
  }

  playUltimate() {
    this.scene.sound.play('ultimate', { volume: 1.0 });
  }

  playHit() {
    this.scene.sound.play('hit', { volume: 0.6 });
  }

  playWin() {
    this.scene.sound.play('win', { volume: 0.8 });
  }

  stopBGM() {
    if (this.bgm) {
      this.bgm.stop();
    }
  }
}
```

---

## 完整示例代码

### index.html
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4399格斗游戏</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
</head>
<body>
    <div id="game-container"></div>
    <script src="js/input.js"></script>
    <script src="js/character.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
```

### css/style.css
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Microsoft YaHei', Arial, sans-serif;
}

#game-container {
    position: relative;
    border: 4px solid #333;
    border-radius: 8px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    overflow: hidden;
}
```

---

## 开发步骤

### 第一步：创建基础项目结构
```bash
mkdir 4399-fighting-game
cd 4399-fighting-game
mkdir css js assets/sprites assets/backgrounds assets/effects assets/sounds data
```

### 第二步：准备素材资源
- 角色精灵图（idle, walk, attack, skill等动作）
- 游戏背景图
- 特效图片
- 音效文件（BGM、攻击、技能、胜利等）

### 第三步：编写核心代码
1. 实现角色类（Character.js）
2. 实现输入处理（Input.js）
3. 实现游戏主循环（Main.js）
4. 实现UI和特效

### 第四步：配置数据文件
1. 角色配置（characters.json）
2. 技能配置（skills.json）

### 第五步：测试和优化
- 测试角色移动和攻击
- 测试技能释放
- 测试AI对战
- 优化性能和流畅度

---

## 扩展功能

### 1. 更多角色
添加更多可选角色，每个角色有独特技能组合。

### 2. 在线对战
使用WebSocket实现在线多人对战功能。

### 3. 成就系统
- 首次胜利
- 连击达成
- 无伤通关
- 使用必杀技获胜

### 4. 排行榜
记录玩家胜率和连胜次数。

### 5. 装备系统
为角色添加装备，提升属性。

### 6. 关卡模式
添加剧情关卡和BOSS战。

---

## 技术要点

### 性能优化
- 使用对象池管理特效和伤害数字
- 精灵图合并减少draw calls
- 碰撞检测优化

### 兼容性
- 支持主流浏览器
- 响应式设计适配不同屏幕
- 移动端触控支持

### 调试技巧
- 使用Phaser的调试工具显示碰撞箱
- 添加FPS显示
- 日志输出关键事件

---

## 参考资料

- [Phaser.js 官方文档](https://photonstorm.github.io/phaser3-docs/)
- [4399小游戏平台](https://www.4399.com/)
- 游戏精灵素材网站
- 游戏音效资源库

---

## 注意事项

1. **资源管理**：所有游戏资源需要压缩优化，确保加载速度
2. **代码规范**：遵循一致的命名规范和代码风格
3. **测试覆盖**：测试各种边界情况和异常输入
4. **用户体验**：添加教程和操作说明
5. **版权注意**：使用的素材需要确认版权或使用免费资源
