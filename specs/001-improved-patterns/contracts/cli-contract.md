# CLI 契约: 改进的 Python 设计模式项目

**特性**: 改进的 Python 设计模式项目
**日期**: 2025-11-20
**版本**: 1.0.0

## 概述

本文档定义了 `patterns` CLI 工具的命令行接口契约。CLI 提供统一的方式来运行示例、查看文档和执行测试。

## 全局选项

所有命令支持以下全局选项:

```bash
--help, -h          显示帮助信息
--version, -v       显示版本信息
--verbose           显示详细输出
--quiet, -q         静默模式,仅显示错误
```

## 命令

### 1. run - 运行模式示例

**用途**: 运行指定设计模式的示例代码

**语法**:
```bash
patterns run <pattern> [选项]
```

**参数**:
- `<pattern>`: 必填,模式标识符
  - 类型: 字符串
  - 格式:
    - 英文ID (例如: "singleton", "observer")
    - 中文名称 (例如: "单例模式", "观察者模式")
  - 大小写不敏感

**选项**:
- `--interactive, -i`: 交互模式(适用于需要用户输入的示例)
- `--timing`: 显示执行时间

**输出**:
- **成功** (退出码 0):
  ```
  === 运行模式: 单例模式 (Singleton) ===

  [示例输出]

  ✓ 示例执行成功 (耗时: 0.023s)
  ```

- **失败** (退出码 1):
  ```
  ✗ 错误: 未找到模式 'xxx'

  建议:
  - 使用 'patterns list' 查看所有可用模式
  - 检查拼写是否正确
  ```

**示例**:
```bash
# 运行单例模式
patterns run singleton

# 运行观察者模式(中文名称)
patterns run 观察者模式

# 交互模式运行
patterns run command --interactive

# 显示执行时间
patterns run decorator --timing
```

**性能要求**:
- 响应时间: < 500ms
- 示例执行: < 1s (SC-001 的部分要求)

---

### 2. list - 列出模式

**用途**: 列出所有或指定分类的设计模式

**语法**:
```bash
patterns list [分类] [选项]
```

**参数**:
- `[分类]`: 可选,模式分类
  - 有效值: "creational", "structural", "behavioral", "other"
  - 中文值: "创建型", "结构型", "行为型", "其他"
  - 省略则显示所有分类

**选项**:
- `--format, -f`: 输出格式
  - 有效值: "table" (默认), "json", "simple"
- `--search, -s <关键词>`: 按关键词搜索

**输出**:
- **table 格式** (默认):
  ```
  创建型模式 (Creational Patterns)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ID                  中文名称    描述
  ──────────────────────────────────────────
  singleton           单例模式    确保一个类只有一个实例
  factory             工厂模式    定义创建对象的接口
  ...

  共 7 个模式
  ```

- **json 格式**:
  ```json
  {
    "category": "creational",
    "patterns": [
      {
        "id": "singleton",
        "name_zh": "单例模式",
        "description_zh": "确保一个类只有一个实例"
      }
    ]
  }
  ```

- **simple 格式**:
  ```
  singleton (单例模式)
  factory (工厂模式)
  ...
  ```

**示例**:
```bash
# 列出所有模式
patterns list

# 列出创建型模式
patterns list creational

# JSON 格式输出
patterns list --format json

# 搜索包含"工厂"的模式
patterns list --search 工厂
```

**性能要求**:
- 响应时间: < 200ms

---

### 3. docs - 查看文档

**用途**: 查看指定模式的文档

**语法**:
```bash
patterns docs <pattern> [选项]
```

**参数**:
- `<pattern>`: 必填,模式标识符(同 run 命令)

**选项**:
- `--section, -s <章节>`: 仅显示特定章节
  - 有效值: "intent", "use_cases", "pros_cons", "examples", "best_practices"
- `--browser, -b`: 在浏览器中打开(如果支持)
- `--export <路径>`: 导出文档到文件

**输出**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
单例模式 (Singleton Pattern)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【意图】
确保一个类只有一个实例,并提供全局访问点。

【适用场景】
1. 需要严格控制全局状态访问时
2. 系统中某个类只应该有一个实例(如配置管理器)
3. 需要延迟初始化的全局对象

【优点】
✓ 控制实例数量
✓ 全局访问点
✓ 延迟初始化

【缺点】
✗ 违反单一职责原则
✗ 难以单元测试
✗ 在多线程环境下需要特殊处理

【示例代码】
见: patterns/creational/singleton.py

【最佳实践】
• 在 Python 中,使用模块级变量通常比单例模式更简单
• 如果需要单例,使用 __new__ 方法
• 考虑使用 Borg 模式作为替代

【相关模式】
• Borg - 共享状态而非单例实例
• Factory - 可以返回单例实例

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**示例**:
```bash
# 查看单例模式文档
patterns docs singleton

# 仅查看适用场景
patterns docs singleton --section use_cases

# 导出文档
patterns docs observer --export observer_doc.md
```

**性能要求**:
- 文档加载: < 100ms

---

### 4. test - 运行测试

**用途**: 运行模式示例的测试

**语法**:
```bash
patterns test [pattern] [选项]
```

**参数**:
- `[pattern]`: 可选,特定模式标识符
  - 省略则运行所有测试

**选项**:
- `--coverage`: 显示测试覆盖率
- `--verbose, -v`: 详细输出
- `--failfast, -x`: 首次失败后停止
- `--parallel, -n <数量>`: 并行测试数量

**输出**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
运行测试: 单例模式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

test_singleton.py::test_single_instance ✓
test_singleton.py::test_global_access ✓
test_singleton.py::test_thread_safety ✓

3 个测试通过 (耗时: 0.152s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
测试摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计: 87 个测试
通过: 87 ✓
失败: 0 ✗
跳过: 0 ⊘

覆盖率: 92% (目标: 90%)
总耗时: 12.3s
```

**示例**:
```bash
# 运行所有测试
patterns test

# 测试单例模式
patterns test singleton

# 运行测试并显示覆盖率
patterns test --coverage

# 并行运行测试
patterns test --parallel 4
```

**性能要求**:
- 完整测试套件: < 30s (SC-007)

---

### 5. compare - 对比模式

**用途**: 对比两个或多个设计模式

**语法**:
```bash
patterns compare <pattern1> <pattern2> [pattern3...] [选项]
```

**参数**:
- `<pattern1> <pattern2>...`: 必填,要对比的模式标识符

**选项**:
- `--aspects, -a <方面>`: 对比特定方面
  - 有效值: "use_cases", "complexity", "performance"
- `--table`: 表格形式显示对比

**输出**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模式对比: 工厂模式 vs 抽象工厂模式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【主要区别】
• 工厂模式创建单一类型的对象
• 抽象工厂模式创建相关对象族

【使用场景对比】
工厂模式:
- 创建对象的类型在运行时决定
- 创建逻辑复杂,需要封装

抽象工厂模式:
- 需要创建一系列相关对象
- 需要确保对象之间的兼容性

【复杂度对比】
工厂模式: ★★☆☆☆ (简单)
抽象工厂模式: ★★★★☆ (复杂)

【选择建议】
→ 如果只需要创建单一产品,使用工厂模式
→ 如果需要创建产品族,使用抽象工厂模式
```

**示例**:
```bash
# 对比工厂模式和抽象工厂模式
patterns compare factory abstract_factory

# 对比三个模式
patterns compare observer mediator pubsub

# 表格形式对比
patterns compare singleton borg --table
```

---

### 6. search - 搜索模式

**用途**: 按关键词或场景搜索设计模式

**语法**:
```bash
patterns search <关键词> [选项]
```

**参数**:
- `<关键词>`: 必填,搜索关键词

**选项**:
- `--in <范围>`: 搜索范围
  - 有效值: "name", "description", "use_cases", "all" (默认)
- `--category <分类>`: 限定分类

**输出**:
```
搜索 "缓存" 的结果 (找到 3 个匹配):

1. 单例模式 (Singleton)
   匹配: 适用场景 - "需要缓存的全局对象"
   相关度: ★★★★☆

2. 享元模式 (Flyweight)
   匹配: 描述 - "通过共享缓存来减少内存使用"
   相关度: ★★★★★

3. 代理模式 (Proxy)
   匹配: 适用场景 - "实现缓存代理"
   相关度: ★★★☆☆
```

**示例**:
```bash
# 搜索包含"缓存"的模式
patterns search 缓存

# 仅在适用场景中搜索
patterns search 缓存 --in use_cases

# 在创建型模式中搜索
patterns search 对象创建 --category creational
```

---

## 退出码

| 退出码 | 含义 |
|-------|------|
| 0 | 成功 |
| 1 | 一般错误(如找不到模式) |
| 2 | 参数错误 |
| 3 | 配置错误 |
| 10 | 示例运行失败 |
| 11 | 测试失败 |

## 环境变量

| 变量 | 描述 | 默认值 |
|-----|------|-------|
| PATTERNS_CONFIG | 配置文件路径 | `./config/patterns.json` |
| PATTERNS_VERBOSE | 详细输出 | `false` |
| PATTERNS_COLOR | 彩色输出 | `auto` (支持则启用) |

## 配置文件

CLI 支持可选的配置文件 `~/.patterns/config.yaml`:

```yaml
# 默认输出格式
default_format: table

# 是否启用彩色输出
color: true

# 默认测试并行数
test_parallel: 4

# 自定义别名
aliases:
  单例: singleton
  观察者: observer
```

## 错误处理

所有错误消息使用以下格式:

```
✗ 错误: [错误类型] [错误描述]

详情:
[详细错误信息]

建议:
• [解决建议 1]
• [解决建议 2]
```

## 国际化

虽然当前版本仅支持简体中文,但 CLI 设计支持未来国际化:

```bash
# 未来可能支持
LANG=en_US patterns list
```

## 性能保证

| 操作 | 性能目标 |
|-----|---------|
| CLI 启动 | < 200ms |
| 命令响应 | < 500ms |
| 文档加载 | < 100ms |
| 示例运行 | < 1s |
| 完整测试 | < 30s |

## 版本兼容性

- 初始版本: 1.0.0
- 遵循语义化版本规则
- 主版本更新可能包含破坏性变更
- 次版本和修订版本保证向后兼容
