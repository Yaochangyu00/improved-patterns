# 数据模型: 改进的 Python 设计模式项目

**特性**: 改进的 Python 设计模式项目
**日期**: 2025-11-20

## 概述

本文档定义了改进的 Python 设计模式项目中的核心数据实体和它们之间的关系。由于这是一个学习资源项目而非应用系统,数据模型相对简单,主要用于组织模式信息和支持 CLI 工具。

## 核心实体

### 1. PatternCategory (模式分类)

**描述**: 代表设计模式的分类

**属性**:
- `name` (str): 分类名称
  - 有效值: "creational", "structural", "behavioral", "other"
  - 必填,唯一
- `display_name_zh` (str): 中文显示名称
  - 示例: "创建型模式", "结构型模式", "行为型模式", "其他模式"
  - 必填
- `description_zh` (str): 中文描述
  - 说明该分类的特点和用途
  - 必填

**关系**:
- 一对多: 一个分类包含多个设计模式

**验证规则**:
- `name` 必须是预定义的四个分类之一
- `display_name_zh` 和 `description_zh` 必须是简体中文

**示例数据**:
```python
{
    "name": "creational",
    "display_name_zh": "创建型模式",
    "description_zh": "关注对象创建机制,通过控制创建过程来解决问题"
}
```

---

### 2. DesignPattern (设计模式)

**描述**: 代表一个具体的设计模式

**属性**:
- `id` (str): 模式唯一标识符
  - 格式: snake_case (例如: "singleton", "abstract_factory")
  - 必填,唯一,不可变
- `name_en` (str): 英文名称
  - 示例: "Singleton", "Abstract Factory"
  - 必填
- `name_zh` (str): 中文名称
  - 示例: "单例模式", "抽象工厂模式"
  - 必填
- `category` (str): 所属分类
  - 外键,关联到 PatternCategory.name
  - 必填
- `code_path` (str): 示例代码文件路径
  - 相对路径: `patterns/{category}/{id}.py`
  - 示例: "patterns/creational/singleton.py"
  - 必填,必须存在
- `doc_path` (str): 文档文件路径
  - 相对路径: `docs/{category}/{id}.md`
  - 示例: "docs/creational/singleton.md"
  - 必填,必须存在
- `test_path` (str): 测试文件路径
  - 相对路径: `tests/test_{category}/test_{id}.py`
  - 示例: "tests/test_creational/test_singleton.py"
  - 必填,必须存在
- `description_zh` (str): 简短中文描述
  - 1-2 句话概括模式意图
  - 必填
- `keywords_zh` (list[str]): 中文关键词
  - 用于搜索和索引
  - 可选
- `related_patterns` (list[str]): 相关模式ID列表
  - 用于模式对比(FR-008)
  - 可选

**关系**:
- 多对一: 多个模式属于一个分类
- 多对多: 模式之间的相关性(通过 `related_patterns`)

**验证规则**:
- `id` 必须匹配文件路径中的名称
- `category` 必须是有效的 PatternCategory.name
- 路径指向的文件必须存在
- `name_zh` 和 `description_zh` 必须是简体中文

**示例数据**:
```python
{
    "id": "singleton",
    "name_en": "Singleton",
    "name_zh": "单例模式",
    "category": "creational",
    "code_path": "patterns/creational/singleton.py",
    "doc_path": "docs/creational/singleton.md",
    "test_path": "tests/test_creational/test_singleton.py",
    "description_zh": "确保一个类只有一个实例,并提供全局访问点",
    "keywords_zh": ["单例", "全局", "唯一实例"],
    "related_patterns": ["borg", "factory"]
}
```

---

### 3. PatternExample (模式示例)

**描述**: 模式示例代码的元数据

**属性**:
- `pattern_id` (str): 关联的模式ID
  - 外键,关联到 DesignPattern.id
  - 必填
- `entry_function` (str): 示例入口函数名
  - 示例: "main", "run_example"
  - 用于 CLI 运行示例
  - 可选,默认 "main"
- `has_interactive` (bool): 是否包含交互式部分
  - 某些示例可能需要用户输入
  - 可选,默认 False
- `expected_output_pattern` (str): 预期输出模式(用于测试)
  - 正则表达式或关键词
  - 可选
- `dependencies` (list[str]): 额外依赖(超出标准库)
  - 通常为空,符合最小依赖原则
  - 可选,默认 []

**关系**:
- 一对一: 每个模式有一个示例

**示例数据**:
```python
{
    "pattern_id": "observer",
    "entry_function": "main",
    "has_interactive": False,
    "expected_output_pattern": "通知.*观察者",
    "dependencies": []
}
```

---

### 4. PatternDocumentation (模式文档)

**描述**: 模式文档的元数据和内容结构

**属性**:
- `pattern_id` (str): 关联的模式ID
  - 外键,关联到 DesignPattern.id
  - 必填
- `intent_zh` (str): 中文意图说明
  - 必填
- `use_cases_zh` (list[str]): 中文适用场景列表
  - 至少 3 个(SC-002)
  - 必填
- `pros_zh` (list[str]): 中文优点列表
  - 必填
- `cons_zh` (list[str]): 中文缺点列表
  - 必填
- `best_practices_zh` (list[str]): Python 特定最佳实践
  - 可选
- `real_world_examples` (list[str]): 真实世界应用案例
  - 可选

**关系**:
- 一对一: 每个模式有一个文档

**示例数据**:
```python
{
    "pattern_id": "decorator",
    "intent_zh": "动态地给对象添加额外的职责",
    "use_cases_zh": [
        "需要在不修改现有代码的情况下扩展功能",
        "需要动态组合多个功能",
        "继承导致类数量爆炸时的替代方案"
    ],
    "pros_zh": ["灵活性高", "遵循开闭原则", "可组合"],
    "cons_zh": ["可能产生大量小对象", "调试困难"],
    "best_practices_zh": [
        "使用 Python 的 @decorator 语法",
        "使用 functools.wraps 保留元数据"
    ],
    "real_world_examples": ["Django 的视图装饰器", "Flask 的路由装饰器"]
}
```

---

### 5. CLICommand (CLI 命令)

**描述**: CLI 工具支持的命令

**属性**:
- `command` (str): 命令名称
  - 示例: "run", "list", "docs", "test"
  - 必填,唯一
- `description_zh` (str): 中文描述
  - 必填
- `arguments` (list[dict]): 命令参数定义
  - 每个参数包含: name, type, required, help_zh
  - 可选
- `examples_zh` (list[str]): 中文使用示例
  - 必填

**示例数据**:
```python
{
    "command": "run",
    "description_zh": "运行指定设计模式的示例",
    "arguments": [
        {
            "name": "pattern",
            "type": "str",
            "required": True,
            "help_zh": "模式ID或名称"
        },
        {
            "name": "--verbose",
            "type": "bool",
            "required": False,
            "help_zh": "显示详细输出"
        }
    ],
    "examples_zh": [
        "patterns run singleton",
        "patterns run 观察者模式",
        "patterns run observer --verbose"
    ]
}
```

## 数据关系图

```
PatternCategory (1) ──< (N) DesignPattern
                              │
                              ├─── (1:1) PatternExample
                              └─── (1:1) PatternDocumentation

DesignPattern ><──> DesignPattern (related_patterns)

CLICommand (独立,无外键关系)
```

## 数据存储

### 存储方式

**选择**: JSON 配置文件 + 文件系统

**理由**:
- 符合"简洁设计"原则,无需数据库
- 便于版本控制
- 易于手动编辑和维护
- 支持离线使用

**文件结构**:
```
improved-patterns/
├── config/
│   ├── patterns.json     # DesignPattern 和 PatternExample 数据
│   ├── categories.json   # PatternCategory 数据
│   ├── cli_commands.json # CLICommand 数据
│   └── schema.json       # JSON Schema 验证规则
```

**示例 patterns.json**:
```json
{
  "patterns": [
    {
      "id": "singleton",
      "name_en": "Singleton",
      "name_zh": "单例模式",
      "category": "creational",
      "code_path": "patterns/creational/singleton.py",
      "doc_path": "docs/creational/singleton.md",
      "test_path": "tests/test_creational/test_singleton.py",
      "description_zh": "确保一个类只有一个实例",
      "keywords_zh": ["单例", "全局", "唯一实例"],
      "related_patterns": ["borg"],
      "example": {
        "entry_function": "main",
        "has_interactive": false,
        "dependencies": []
      }
    }
  ]
}
```

## 数据验证

### 验证规则

1. **路径验证**: 所有文件路径必须存在且可访问
2. **外键验证**: category 必须在 categories.json 中存在
3. **唯一性验证**: id 和 name 组合必须唯一
4. **语言验证**: 所有 *_zh 字段必须是简体中文
5. **计数验证**: use_cases_zh 至少 3 个(FR-005, SC-002)

### 验证时机

- **启动时**: CLI 加载配置时验证
- **测试时**: 集成测试验证数据完整性
- **CI/CD**: 自动化检查配置文件有效性

## 状态管理

### 无状态设计

项目采用无状态设计:
- 无用户会话
- 无持久化状态
- 每次运行独立

这符合宪章的"简洁设计"原则。

## 性能考虑

### 加载优化

1. **延迟加载**: 只在需要时加载模式模块
2. **缓存**: CLI 启动时缓存 patterns.json
3. **索引**: 构建模式ID到路径的快速查找表

**预期性能**:
- 配置加载: < 100ms
- 模式查找: O(1)
- 文档读取: < 50ms

## 扩展性

### 未来扩展

虽然当前版本保持简洁,但数据模型支持以下扩展:
1. 添加 `difficulty_level` (难度级别)
2. 添加 `learning_path` (学习路径推荐)
3. 添加 `code_variants` (不同实现变体)

这些扩展可在不破坏现有结构的情况下添加。
