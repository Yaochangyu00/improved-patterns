"""
惰性求值模式 (Lazy Evaluation Pattern)

意图:
    延迟计算直到真正需要结果时,避免不必要的计算和资源消耗

适用场景:
    - 计算成本很高但结果可能不需要
    - 需要处理大数据集但只使用部分数据
    - 初始化开销大的对象
    - 需要支持无限序列或惰性数据流

Python 实现说明:
    使用属性(property)实现延迟初始化
    使用生成器(generator)实现惰性序列
    使用装饰器封装惰性行为
"""
import time
from typing import Callable, Any, Iterator, Optional
from functools import wraps


# 惰性属性装饰器
class LazyProperty:
    """惰性属性装饰器"""

    def __init__(self, func: Callable):
        """
        初始化惰性属性

        Args:
            func: 计算属性值的函数
        """
        self.func = func
        self.attr_name = f"_{func.__name__}"

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """获取属性值,首次访问时计算"""
        if obj is None:
            return self

        # 检查是否已缓存
        if not hasattr(obj, self.attr_name):
            # 首次访问,计算并缓存
            value = self.func(obj)
            setattr(obj, self.attr_name, value)

        return getattr(obj, self.attr_name)


# 示例类 - 数据报告
class DataReport:
    """数据报告类,使用惰性属性"""

    def __init__(self, data: list):
        """
        初始化报告

        Args:
            data: 原始数据
        """
        self.data = data
        print(f"报告初始化,数据量: {len(data)}")

    @LazyProperty
    def summary(self) -> dict:
        """计算统计摘要(惰性)"""
        print("  计算统计摘要...")
        time.sleep(0.5)  # 模拟耗时计算

        return {
            "total": len(self.data),
            "sum": sum(self.data),
            "avg": sum(self.data) / len(self.data) if self.data else 0,
            "max": max(self.data) if self.data else 0,
            "min": min(self.data) if self.data else 0,
        }

    @LazyProperty
    def visualization(self) -> str:
        """生成可视化(惰性)"""
        print("  生成可视化...")
        time.sleep(0.3)  # 模拟耗时操作

        # 简单的条形图
        max_val = max(self.data) if self.data else 1
        chart = []
        for i, val in enumerate(self.data[:10]):  # 只显示前10个
            bar = "█" * int((val / max_val) * 20)
            chart.append(f"{i:2d}: {bar} ({val})")

        return "\n".join(chart)


# 惰性序列生成器
class LazySequence:
    """惰性序列类"""

    @staticmethod
    def fibonacci() -> Iterator[int]:
        """生成斐波那契数列(惰性,无限)"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    @staticmethod
    def range_with_transform(start: int, end: int, transform: Callable) -> Iterator[Any]:
        """
        生成转换后的范围(惰性)

        Args:
            start: 起始值
            end: 结束值
            transform: 转换函数
        """
        for i in range(start, end):
            yield transform(i)

    @staticmethod
    def lazy_filter(iterable: Iterator, predicate: Callable) -> Iterator:
        """
        惰性过滤

        Args:
            iterable: 可迭代对象
            predicate: 过滤条件函数
        """
        for item in iterable:
            if predicate(item):
                yield item


# 延迟初始化的资源类
class HeavyResource:
    """重量级资源类"""

    _instance: Optional['HeavyResource'] = None

    def __init__(self):
        """初始化(延迟)"""
        print("  初始化重量级资源...")
        time.sleep(0.5)  # 模拟耗时初始化
        self.data = "重要数据"

    @classmethod
    def get_instance(cls) -> 'HeavyResource':
        """获取实例(延迟初始化)"""
        if cls._instance is None:
            print("首次访问,创建实例")
            cls._instance = cls()
        else:
            print("复用已存在的实例")
        return cls._instance


def main():
    """惰性求值模式示例"""
    print("=" * 60)
    print("惰性求值模式示例")
    print("=" * 60)

    # 示例 1: 惰性属性
    print("\n1. 惰性属性 - 延迟计算")
    print("-" * 60)
    report = DataReport([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    print("报告对象已创建,但统计和可视化尚未计算\n")

    time.sleep(0.5)
    print("现在访问 summary 属性:")
    print(report.summary)
    print("\n再次访问 summary (从缓存读取):")
    print(report.summary)

    print("\n现在访问 visualization 属性:")
    print(report.visualization)

    # 示例 2: 惰性序列 - 无限序列
    print("\n2. 惰性序列 - 斐波那契数列(无限)")
    print("-" * 60)
    fib = LazySequence.fibonacci()
    print("前 10 个斐波那契数:")
    for i, num in enumerate(fib):
        if i >= 10:
            break
        print(f"  {i}: {num}")

    # 示例 3: 惰性转换
    print("\n3. 惰性转换 - 只在需要时计算")
    print("-" * 60)
    print("创建惰性转换序列(平方运算)")
    lazy_squares = LazySequence.range_with_transform(1, 1000000, lambda x: x ** 2)
    print("序列已创建,但尚未计算任何值")

    print("\n获取前 5 个值:")
    for i, square in enumerate(lazy_squares):
        if i >= 5:
            break
        print(f"  {i+1}² = {square}")
    print("(注意: 百万个值中只计算了 5 个)")

    # 示例 4: 惰性过滤
    print("\n4. 惰性过滤 - 按需过滤")
    print("-" * 60)
    numbers = LazySequence.fibonacci()
    even_fib = LazySequence.lazy_filter(numbers, lambda x: x % 2 == 0)
    print("前 5 个偶数斐波那契数:")
    for i, num in enumerate(even_fib):
        if i >= 5:
            break
        print(f"  {i}: {num}")

    # 示例 5: 延迟初始化
    print("\n5. 延迟初始化 - 重量级资源")
    print("-" * 60)
    print("程序启动,尚未创建资源")
    time.sleep(0.3)

    print("\n第一次使用资源:")
    resource1 = HeavyResource.get_instance()
    print(f"资源数据: {resource1.data}")

    print("\n第二次使用资源:")
    resource2 = HeavyResource.get_instance()
    print(f"是同一个实例: {resource1 is resource2}")

    print("\n" + "=" * 60)
    print("结论: 惰性求值延迟计算,提高性能和资源利用率")
    print("=" * 60)


if __name__ == "__main__":
    main()
