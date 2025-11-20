# 改进的 Python 设计模式项目

一个全面的 Python 设计模式学习资源,提供交互式示例、完整中文文档和自动化测试。

## 特性

- 📚 **29+ 设计模式**: 覆盖创建型、结构型、行为型和其他模式
- 🎯 **交互式示例**: 每个模式都有可运行的示例代码
- 📖 **完整中文文档**: 包含意图、适用场景、优缺点和最佳实践
- ✅ **自动化测试**: 90%+ 测试覆盖率,确保代码质量
- 🚀 **命令行工具**: 统一的 CLI 界面,轻松运行示例和查看文档

## 安装

### 前置要求

- Python 3.8 或更高版本
- pip

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/your-username/improved-patterns.git
cd improved-patterns

# 创建虚拟环境(推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装项目
pip install -e .

# 安装开发依赖(可选)
pip install -e ".[dev]"
```

## 快速开始

### 列出所有模式

```bash
patterns list
```

### 运行示例

```bash
# 运行单例模式示例
patterns run singleton

# 运行观察者模式示例
patterns run observer
```

### 查看文档

```bash
# 查看单例模式文档
patterns docs singleton

# 查看工厂模式文档
patterns docs factory
```

### 运行测试

```bash
# 运行所有测试
patterns test

# 运行特定模式的测试
patterns test singleton

# 运行测试并显示覆盖率
patterns test --coverage
```

## 包含的设计模式

### 创建型模式 (7)
- Singleton (单例)
- Factory (工厂)
- Abstract Factory (抽象工厂)
- Builder (建造者)
- Prototype (原型)
- Object Pool (对象池)
- Lazy Evaluation (惰性求值)

### 结构型模式 (9)
- Adapter (适配器)
- Bridge (桥接)
- Composite (组合)
- Decorator (装饰器)
- Facade (外观)
- Flyweight (享元)
- Proxy (代理)
- MVC (模型-视图-控制器)
- 3-Tier (三层)

### 行为型模式 (11)
- Chain of Responsibility (责任链)
- Command (命令)
- Iterator (迭代器)
- Mediator (中介者)
- Memento (备忘录)
- Observer (观察者)
- State (状态)
- Strategy (策略)
- Template Method (模板方法)
- Visitor (访问者)
- Publish-Subscribe (发布-订阅)

### 其他模式 (2)
- Dependency Injection (依赖注入)
- Blackboard (黑板)

## 项目结构

```
improved-patterns/
├── patterns/       # 设计模式示例代码
├── docs/           # 中文文档
├── cli/            # 命令行工具
├── tests/          # 测试套件
├── config/         # 配置文件
└── README.md       # 本文件
```

## CLI 命令参考

- `patterns list [category]` - 列出所有或指定分类的模式
- `patterns run <pattern>` - 运行指定模式的示例
- `patterns docs <pattern>` - 查看指定模式的文档
- `patterns test [pattern]` - 运行测试
- `patterns compare <pattern1> <pattern2>` - 对比模式(未来版本)
- `patterns search <keyword>` - 搜索模式(未来版本)

## 开发

### 运行测试

```bash
pytest
```

### 运行测试并生成覆盖率报告

```bash
pytest --cov=patterns --cov=cli --cov-report=html
```

### 代码格式化

```bash
black .
```

### 代码检查

```bash
flake8
```

## 贡献

欢迎贡献!请查看贡献指南了解详情。

## 许可证

MIT License

## 致谢

本项目受 [python-patterns](https://github.com/faif/python-patterns) 启发,旨在提供更完整的学习体验。
