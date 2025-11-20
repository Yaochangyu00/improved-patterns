# 惰性求值模式 (Lazy Evaluation Pattern)

## 意图

延迟计算直到真正需要结果时,避免不必要的计算和资源消耗。

## 问题

立即计算面临的问题:
- 计算成本很高但结果可能不需要
- 需要处理大数据集但只使用部分数据
- 初始化开销大的对象可能从未使用
- 无法处理无限序列

## 解决方案

惰性求值延迟计算到实际需要时:
1. 使用属性延迟初始化
2. 使用生成器实现惰性序列
3. 缓存计算结果避免重复计算
4. 按需加载数据

## 适用场景

1. **计算成本很高但结果可能不需要**
   - 例如:复杂报表中用户可能不查看的部分

2. **需要处理大数据集但只使用部分**
   - 例如:分页加载、流式处理

3. **初始化开销大的对象**
   - 例如:大型配置、外部资源

4. **需要支持无限序列**
   - 例如:斐波那契数列、素数序列

## 结构

```
    Client
       |
       ↓
  LazyObject
  +_value (cached)
  +getValue() → 首次计算并缓存
```

## Python 实现

参见代码: `patterns/creational/lazy_evaluation.py`

### 关键点
- 使用 `@property` 实现延迟初始化
- 使用生成器 `yield` 实现惰性序列
- 使用描述符实现惰性属性装饰器
- 缓存结果避免重复计算

### 代码示例

**惰性属性**:
```python
class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value

class Report:
    @LazyProperty
    def summary(self):
        # 耗时计算,首次访问时执行
        return calculate_summary(self.data)
```

**惰性序列**:
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 只计算需要的部分
for i, num in zip(range(10), fibonacci()):
    print(num)
```

## 优点

✓ **提高性能**: 避免不必要的计算
✓ **节省内存**: 只在需要时创建对象
✓ **支持无限数据**: 可以处理无限序列
✓ **更快的启动**: 延迟初始化加速启动

## 缺点

✗ **首次访问延迟**: 第一次访问时的延迟
✗ **增加复杂度**: 需要处理缓存和状态
✗ **调试困难**: 计算时机不确定
✗ **可能内存泄漏**: 缓存可能导致内存问题

## 最佳实践

### Python 特定建议
- 使用 `@functools.cached_property` (Python 3.8+)
- 使用生成器表达式代替列表推导
- 考虑使用 `itertools` 模块

### 通用建议
- 只对确实昂贵的计算使用惰性求值
- 考虑缓存策略(LRU、TTL等)
- 文档化惰性行为

## Python 内置支持

```python
from functools import cached_property

class MyClass:
    @cached_property
    def expensive(self):
        return compute()  # 只计算一次
```

## 真实应用案例

1. **生成器**: Python 的生成器和迭代器
2. **Django ORM**: QuerySet 惰性求值
3. **pandas**: 延迟计算的 DataFrame 操作
4. **Spark**: 延迟计算的分布式数据处理

## 相关模式

- **代理模式**: 代理可以实现惰性加载
- **单例模式**: 惰性初始化的单例
- **虚拟代理**: 惰性加载重量级对象

## 变体

### 惰性初始化
延迟创建对象:
```python
if self._instance is None:
    self._instance = create()
return self._instance
```

### 惰性序列
使用生成器实现:
```python
def lazy_range(n):
    i = 0
    while i < n:
        yield i
        i += 1
```

### 记忆化
缓存函数调用结果:
```python
@functools.lru_cache
def expensive_func(n):
    return compute(n)
```

## 注意事项

1. **线程安全**: 多线程环境需要同步
2. **缓存失效**: 考虑何时需要重新计算
3. **内存管理**: 控制缓存大小

## 进一步学习

- 运行示例: `patterns run lazy_evaluation`
- 查看代码: `patterns/creational/lazy_evaluation.py`
- 运行测试: `patterns test lazy_evaluation`
