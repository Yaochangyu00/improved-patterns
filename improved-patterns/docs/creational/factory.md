# 工厂模式 (Factory Pattern)

## 意图

定义创建对象的接口,让子类决定实例化哪个类。工厂方法将对象的实例化延迟到子类。

## 问题

在面向对象编程中,我们经常需要创建对象。但直接使用 `new` 或构造函数创建对象会导致:
- 代码与具体类紧密耦合
- 难以扩展新的类型
- 创建逻辑分散在代码各处,难以维护

## 解决方案

工厂模式通过引入工厂类来封装对象创建逻辑:
1. 定义一个创建对象的接口
2. 工厂根据参数决定创建哪种类型的对象
3. 客户端代码只与工厂和抽象接口交互,不直接依赖具体类

## 适用场景

1. **创建对象的类型在运行时决定**
   - 例如:根据用户输入创建不同类型的图形

2. **创建逻辑复杂,需要封装**
   - 例如:对象创建需要多个步骤或依赖其他对象

3. **需要对象创建过程的集中管理**
   - 例如:统计创建了多少个对象,或添加日志

4. **希望隐藏具体类的实现细节**
   - 例如:只暴露接口,不暴露具体类名

## 结构

```
┌────────────────┐
│    Factory     │
├────────────────┤
│ +create(type)  │─────┐
└────────────────┘     │ 创建
                       ↓
         ┌─────────────────────┐
         │   Product (抽象)    │
         └─────────────────────┘
                  △
                  │ 继承
        ┌─────────┴─────────┐
        │                   │
┌───────────────┐   ┌───────────────┐
│ ConcreteA     │   │ ConcreteB     │
└───────────────┘   └───────────────┘
```

## Python 实现

参见代码示例:`patterns/creational/factory.py`

### 关键点

1. **抽象基类**:使用 ABC 定义产品接口
2. **工厂类**:维护类型到类的映射
3. **可扩展性**:新增产品类型无需修改客户端代码

### 代码片段

```python
class ShapeFactory:
    _shapes = {
        "circle": Circle,
        "square": Square,
    }

    def create_shape(self, shape_type, **kwargs):
        shape_class = self._shapes.get(shape_type)
        if shape_class:
            return shape_class(**kwargs)
        raise ValueError(f"未知类型: {shape_type}")
```

## 优点

✓ **解耦**:客户端代码不依赖具体类,只依赖抽象接口
✓ **单一职责**:对象创建逻辑集中在工厂中
✓ **开闭原则**:新增产品类型时,只需扩展工厂,不修改客户端
✓ **灵活性**:可以轻松切换不同的产品实现

## 缺点

✗ **增加类数量**:需要为每种产品创建类
✗ **可能过度设计**:对于简单场景,直接创建对象可能更合适
✗ **工厂类可能变大**:随着产品类型增加,工厂类的职责增多

## 最佳实践

### Python 特定建议

1. **使用字典映射**
   ```python
   class Factory:
       _products = {}

       @classmethod
       def register(cls, key, product_class):
           cls._products[key] = product_class

       @classmethod
       def create(cls, key, **kwargs):
           return cls._products[key](**kwargs)
   ```

2. **使用 `**kwargs` 传递参数**
   - 保持工厂接口的灵��性

3. **结合类型提示**
   ```python
   from typing import Type, Dict

   class Factory:
       _products: Dict[str, Type[Product]] = {}
   ```

### 通用建议

- 只在需要时使用工厂模式,不要过度设计
- 工厂方法应该返回抽象接口,而非具体类
- 考虑使用依赖注入代替工厂模式
- 为工厂提供注册新产品的机制,提高扩展性

## 真实应用案例

1. **Django ORM**:
   - `Model.objects.create()` 方法

2. **SQLAlchemy**:
   - Session 工厂

3. **日志系统**:
   - `logging.getLogger()` 返回不同的日志记录器

4. **GUI 框架**:
   - 创建不同平台的 UI 组件

## 相关模式

- **抽象工厂模式**:创建相关对象族,而非单一对象
- **建造者模式**:逐步构建复杂对象
- **原型模式**:通过克隆创建对象
- **单例模式**:工厂可以返回单例对象

## 对比

| 特性 | 工厂模式 | 抽象工厂模式 |
|-----|---------|------------|
| 创建对象 | 单一产品 | 相关产品族 |
| 复杂度 | 简单 | 复杂 |
| 使用场景 | 创建一种类型的对象 | 创建多种相关对象 |
| 扩展性 | 易于添加新产品 | 添加新产品族较难 |

## 变体

### 简单工厂
最简单的形式,工厂类只有一个静态方法:
```python
class SimpleFactory:
    @staticmethod
    def create(type):
        if type == "A":
            return ProductA()
        elif type == "B":
            return ProductB()
```

### 工厂方法
每个产品类型有自己的创建方法:
```python
class Factory:
    def create_product_a(self):
        return ProductA()

    def create_product_b(self):
        return ProductB()
```

## 进一步学习

- 阅读源代码:`patterns/creational/factory.py`
- 运行示例:`patterns run factory`
- 运行测试:`patterns test factory`
- 对比学习:`patterns compare factory abstract_factory`
