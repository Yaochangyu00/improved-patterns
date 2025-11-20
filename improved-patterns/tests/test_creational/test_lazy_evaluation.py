"""
惰性求值模式测试
"""
import pytest


def test_lazy_property_computes_once():
    """测试惰性属性只计算一次"""
    from patterns.creational.lazy_evaluation import DataReport

    report = DataReport([1, 2, 3, 4, 5])

    # 首次访问
    summary1 = report.summary
    # 再次访问(应从缓存读取)
    summary2 = report.summary

    assert summary1 is summary2
    assert summary1["total"] == 5
    assert summary1["sum"] == 15


def test_lazy_property_correct_values():
    """测试惰性属性计算正确值"""
    from patterns.creational.lazy_evaluation import DataReport

    report = DataReport([10, 20, 30])
    summary = report.summary

    assert summary["total"] == 3
    assert summary["sum"] == 60
    assert summary["avg"] == 20
    assert summary["max"] == 30
    assert summary["min"] == 10


def test_fibonacci_generator():
    """测试斐波那契生成器"""
    from patterns.creational.lazy_evaluation import LazySequence

    fib = LazySequence.fibonacci()
    first_ten = [next(fib) for _ in range(10)]

    assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_lazy_transform():
    """测试惰性转换"""
    from patterns.creational.lazy_evaluation import LazySequence

    squares = LazySequence.range_with_transform(1, 6, lambda x: x ** 2)
    result = list(squares)

    assert result == [1, 4, 9, 16, 25]


def test_lazy_filter():
    """测试惰性过滤"""
    from patterns.creational.lazy_evaluation import LazySequence

    numbers = iter(range(10))
    evens = LazySequence.lazy_filter(numbers, lambda x: x % 2 == 0)
    result = list(evens)

    assert result == [0, 2, 4, 6, 8]


def test_heavy_resource_lazy_init():
    """测试重量级资源延迟初始化"""
    from patterns.creational.lazy_evaluation import HeavyResource

    # 重置单例
    HeavyResource._instance = None

    # 首次获取
    resource1 = HeavyResource.get_instance()
    # 再次获取
    resource2 = HeavyResource.get_instance()

    assert resource1 is resource2
    assert resource1.data == "重要数据"


def test_main_function():
    """测试 main 函数正常运行"""
    from patterns.creational.lazy_evaluation import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
