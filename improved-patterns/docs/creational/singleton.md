# 单例模式 (Singleton Pattern)

## 意图

确保一个类只有一个实例,并提供全局访问点。

## 问题

在某些情况下,我们需要确保一个类只有一个实例,例如:
- 配置管理器:全局配置应该只有一份
- 数据库连接池:避免创建多个连接池浪费资源
- 日志记录器:统一的日志输出管理

如果不限制实例数量,可能导致资源浪费、状态不一致等问题。

## 解决方案

单例模式通过以下方式确保唯一实例:
1. 将构造函数设为私有,防止外部直接创建实例
2. 提供一个静态方法获取唯一实例
3. 在首次调用时创建实例,后续调用返回同一实例

## 适用场景

1. **需要严格控制全局状态访问时**
   - 例如:应用程序配置管理器

2. **系统中某个类只应该有一个实例**
   - 例如:线程池、缓存管理器、窗口管理器

3. **需要延迟初始化的全局对象**
   - 例如:数据库连接在首次使用时才建立

4. **需要控制资源使用**
   - 例如:打印机管理器,确保打印任务有序执行

## 结构

```
┌─────────────────┐
│   Singleton     │
├─────────────────┤
│ -instance       │ ← 静态私有实例
├─────────────────┤
│ +getInstance()  │ ← 公共静态方法
│ -Singleton()    │ ← 私有构造函数
└─────────────────┘
```

## Python 实现

参见代码示例:`patterns/creational/singleton.py`

### 关键点

1. **使用 `__new__` 方法**:在 Python 中,重写 `__new__` 方法来控制实例创建
2. **线程安全**:使用锁(Lock)确保多线程环境下的安全性
3. **双重检查锁定**:先检查实例是否存在,再加锁,提高性能

### 代码片段

```python
class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

## 优点

✓ **控制实例数量**:确保全局只有一个实例
✓ **全局访问点**:提供统一的访问接口
✓ **延迟初始化**:实例在首次使用时才创建,节省资源
✓ **避免资源冲突**:多个部分访问同一资源时保持一致性

## 缺点

✗ **违反单一职责原则**:类既要管理自身业务逻辑,又要管理实例唯一性
✗ **难以单元测试**:全局状态使得测试间可能相互影响
✗ **多线程问题**:需要额外处理线程安全
✗ **隐藏依赖**:使用全局实例可能导致代码依赖关系不明确

## 最佳实践

### Python 特定建议

1. **优先使用模块级变量**
   ```python
   # 在 Python 中,模块本身就是单例
   # config.py
   class Config:
       pass

   config = Config()  # 模块级单例
   ```

2. **使用装饰器实现单例**
   ```python
   def singleton(cls):
       instances = {}
       def get_instance(*args, **kwargs):
           if cls not in instances:
               instances[cls] = cls(*args, **kwargs)
           return instances[cls]
       return get_instance

   @singleton
   class MyClass:
       pass
   ```

3. **考虑使用 Borg 模式**
   - Borg 模式允许多个实例,但共享状态
   - 比单例模式更灵活

### 通用建议

- 仔细考虑是否真的需要单例,过度使用会导致代码耦合
- 如果需要单例,明确文档化原因
- 为测试提供重置实例的方法
- 注意多线程环境下的线程安全

## 真实应用案例

1. **Python 标准库**:
   - `None`:Python 中 `None` 就是单例

2. **Django 框架**:
   - Settings 配置对象

3. **日志系统**:
   - Python 的 `logging` 模块使用单例管理日志器

4. **数据库连接池**:
   - SQLAlchemy 的 Engine 通常作为单例使用

## 相关模式

- **Borg 模式**:共享状态而非单例实例,更灵活
- **工厂模式**:工厂可以返回单例实例
- **抽象工厂模式**:可以用来创建单例对象

## 对比

| 特性 | 单例模式 | Borg 模式 |
|-----|---------|----------|
| 实例数量 | 唯一实例 | 多个实例 |
| 状态共享 | 通过同一实例 | 通过共享字典 |
| 实现复杂度 | 中等 | 简单 |
| 使用场景 | 需要唯一实例 | 只需共享状态 |

## 进一步学习

- 阅读源代码:`patterns/creational/singleton.py`
- 运行示例:`patterns run singleton`
- 运行测试:`patterns test singleton`
