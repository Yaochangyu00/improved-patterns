# 观察者模式 (Observer Pattern)

## 意图

定义对象间的一对多依赖关系,当一个对象状态改变时,所有依赖它的对象都会收到通知并自动更新。

## 别名

- 发布-订阅模式 (Publish-Subscribe)
- 依赖模式 (Dependents)
- 事件订阅者模式 (Event-Subscriber)

## 问题

在软件系统中,对象之间经常存在依赖关系:
- 当一个对象改变时,其他对象也需要相应改变
- 但我们不希望对象之间紧密耦合
- 需要一种机制让对象在不知道彼此细节的情况下相互通信

## 解决方案

观察者模式通过以下方式解决问题:
1. 定义主题(Subject)和观察者(Observer)接口
2. 主题维护观察者列表
3. 主题状态改变时,自动通知所有观察者
4. 观察者收到通知后自行决定如何响应

## 适用场景

1. **当一个对象的改变需要同时改变其他对象**
   - 例如:Excel 中数据改变时,图表自动更新

2. **不希望对象间形成紧耦合**
   - 例如:事件系统,发布者不需要知道订阅者的具体类型

3. **需要创建触发链**
   - 例如:对象 A 的改变影响 B,B 的改变又影响 C

4. **需要实时通知多个对象**
   - 例如:股票价格变化通知多个显示器

## 结构

```
┌──────────────────┐                    ┌──────────────────┐
│     Subject      │◆───────────────────│    Observer      │
├──────────────────┤                    ├──────────────────┤
│ +attach()        │                    │ +update()        │
│ +detach()        │                    └──────────────────┘
│ +notify()        │                           △
└──────────────────┘                           │
        △                                      │
        │                                      │
        │                              ┌───────┴────────┐
┌───────┴─────────┐                    │                │
│ ConcreteSubject │            ┌───────────────┐ ┌─────────────┐
├─────────────────┤            │ ObserverA     │ │ ObserverB   │
│ -state          │            └───────────────┘ └─────────────┘
│ +getState()     │
│ +setState()     │
└─────────────────┘
```

## Python 实现

参见代码示例:`patterns/behavioral/observer.py`

### 关键点

1. **主题接口**:定义注册、移除和通知观察者的方法
2. **观察者接口**:定义更��方法
3. **松耦合**:主题和观察者通过接口交互

### 代码片段

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Observer:
    def update(self, subject):
        # 响应主题的变化
        pass
```

## 优点

✓ **开闭原则**:可以在不修改主题的情况下添加新观察者
✓ **松耦合**:主题和观察者相互独立,可以独立变化
✓ **支持广播通信**:主题可以同时通知多个观察者
✓ **动态关系**:可以在运行时建立和移除依赖关系

## 缺点

✗ **可能导致意外更新**:观察者不知道其他观察者的存在,可能导致循环依赖
✗ **性能开销**:大量观察者时,通知可能很慢
✗ **调试困难**:难以追踪通知链和更新顺序
✗ **内存泄漏风险**:忘记移除观察者可能导致内存泄漏

## 最佳实践

### Python 特定建议

1. **使用弱引用避免内存泄漏**
   ```python
   import weakref

   class Subject:
       def __init__(self):
           self._observers = weakref.WeakSet()
   ```

2. **使用装饰器简化观察者注册**
   ```python
   class Subject:
       def __init__(self):
           self._observers = []

       def observer(self, func):
           self._observers.append(func)
           return func

   subject = Subject()

   @subject.observer
   def on_change(subject):
       print("Changed!")
   ```

3. **使用 Python 的信号库**
   - `blinker` 库提供了完善的信号机制
   - Django 的信号系统

### 通用建议

- 考虑通知的顺序和优先级
- 为观察者提供过滤机制,只接收感兴趣的通知
- 避免在更��方法中进行耗时操作
- 使用异步通知避免阻塞
- 明确文档化通知的时机和内容

## 真实应用案例

1. **GUI 框架**:
   - MVC 模式中,Model 是主题,View 是观察者
   - Qt 的信号-槽机制
   - Tkinter 的事件绑定

2. **Django 框架**:
   - Django Signals (pre_save, post_save 等)

3. **响应式编程**:
   - RxPY (Reactive Extensions for Python)
   - ReactiveX

4. **事件系统**:
   - JavaScript 的事件监听
   - Node.js 的 EventEmitter

## 相关模式

- **发布-订阅模式**:观察者模式的变体,引入事件通道解耦主题和观察者
- **中介者模式**:通过中介者管理对象间的通信
- **单例模式**:主题可能是单例

## 对比

| 特性 | 观察者模式 | 发布-订阅模式 |
|-----|----------|-------------|
| 耦合度 | 主题知道观察者 | 发布者不知道订阅者 |
| 通信方式 | 直接通知 | 通过事件通道 |
| 复杂度 | 简单 | 较复杂 |
| 使用场景 | 一对多依赖 | 多对多消息分发 |

| 特性 | 观察者模式 | 中介者模式 |
|-----|----------|----------|
| 通信方式 | 一对多 | 多对多 |
| 职责 | 主题广播通知 | 中介者协调通信 |
| 适用场景 | 一个对象影响多个对象 | 多个对象相互影响 |

## 实现变体

### 推模型 (Push Model)
主题主动推送详细信息给观察者:
```python
class Subject:
    def notify(self):
        for observer in self._observers:
            observer.update(self.state, self.data)
```

### 拉模型 (Pull Model)
主题只通知观察者,观察者主动拉取需要的信息:
```python
class Subject:
    def notify(self):
        for observer in self._observers:
            observer.update(self)  # 观察者自己获取需要的数据
```

推荐使用拉模型,因为它更灵活,观察者可以选择需要的信息。

## 注意事项

1. **避免循环依赖**:观察者的更新不应该触发主题的改变
2. **注意更新顺序**:如果顺序重要,需要明确定义
3. **处理异常**:一个观察者的异常不应影响其他观察者
4. **线程安全**:多线程环境下需要同步

## 进一步学习

- 阅读源代码:`patterns/behavioral/observer.py`
- 运行示例:`patterns run observer`
- 运行测试:`patterns test observer`
- 对比学习:`patterns compare observer pubsub mediator`
