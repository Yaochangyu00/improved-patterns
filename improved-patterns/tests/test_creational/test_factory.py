"""
工厂模式测试

测试工厂模式的核心功能
"""
import pytest


def test_factory_creates_correct_types():
    """测试工厂方法创建正确的对象类型"""
    from patterns.creational.factory import ShapeFactory, Circle, Square

    factory = ShapeFactory()

    circle = factory.create_shape("circle")
    assert isinstance(circle, Circle), "应该创建 Circle 实例"

    square = factory.create_shape("square")
    assert isinstance(square, Square), "应该创建 Square 实例"


def test_factory_invalid_type():
    """测试工厂方法处理无效类型"""
    from patterns.creational.factory import ShapeFactory

    factory = ShapeFactory()

    with pytest.raises(ValueError):
        factory.create_shape("invalid_shape")


def test_factory_polymorphism():
    """测试工厂创建的对象具有多态性"""
    from patterns.creational.factory import ShapeFactory

    factory = ShapeFactory()

    shapes = [
        factory.create_shape("circle"),
        factory.create_shape("square"),
    ]

    # 所有形状都应该有 draw 方法
    for shape in shapes:
        assert hasattr(shape, "draw"), "所有形状都应该有 draw 方法"
        # draw 方法应该能够正常调用
        try:
            result = shape.draw()
            assert isinstance(result, str), "draw 方法应该返回字符串"
        except Exception as e:
            pytest.fail(f"draw 方法调用失败: {e}")


def test_factory_circle_properties():
    """测试圆形对象的属性"""
    from patterns.creational.factory import ShapeFactory

    factory = ShapeFactory()
    circle = factory.create_shape("circle", radius=5)

    assert hasattr(circle, "radius"), "圆形应该有 radius 属性"
    assert circle.radius == 5, "圆形的 radius 应该是 5"


def test_factory_square_properties():
    """测试正方形对象的属性"""
    from patterns.creational.factory import ShapeFactory

    factory = ShapeFactory()
    square = factory.create_shape("square", side=10)

    assert hasattr(square, "side"), "正方形应该有 side 属性"
    assert square.side == 10, "正方形的 side 应该是 10"


def test_factory_main_function():
    """测试工厂模式的 main 函数可以正常运行"""
    from patterns.creational.factory import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
