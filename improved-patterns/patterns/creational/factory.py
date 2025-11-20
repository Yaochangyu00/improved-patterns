"""
工厂模式 (Factory Pattern)

意图:
    定义创建对象的接口,让子类决定实例化哪个类

适用场景:
    - 创建对象的类型在运行时决定
    - 创建逻辑复杂,需要封装
    - 需要对象创建过程的集中管理

Python 实现说明:
    使用工厂方法根据参数返回不同类型的对象
"""
from abc import ABC, abstractmethod
from typing import Dict, Type


class Shape(ABC):
    """形状抽象基类"""

    @abstractmethod
    def draw(self) -> str:
        """绘制形状"""
        pass


class Circle(Shape):
    """圆形类"""

    def __init__(self, radius: float = 1.0):
        """
        初始化圆形

        Args:
            radius: 圆的半径
        """
        self.radius = radius

    def draw(self) -> str:
        """绘制圆形"""
        result = f"绘制圆形,半径为 {self.radius}"
        print(result)
        return result


class Square(Shape):
    """正方形类"""

    def __init__(self, side: float = 1.0):
        """
        初始化正方形

        Args:
            side: 正方形的边长
        """
        self.side = side

    def draw(self) -> str:
        """绘制正方形"""
        result = f"绘制正方形,边长为 {self.side}"
        print(result)
        return result


class Triangle(Shape):
    """三角形类"""

    def __init__(self, base: float = 1.0, height: float = 1.0):
        """
        初始化三角形

        Args:
            base: 三角形的底边
            height: 三角形的高
        """
        self.base = base
        self.height = height

    def draw(self) -> str:
        """绘制三角形"""
        result = f"绘制三角形,底边为 {self.base},高为 {self.height}"
        print(result)
        return result


class ShapeFactory:
    """形状工厂类"""

    # 注册可用的形状类型
    _shapes: Dict[str, Type[Shape]] = {
        "circle": Circle,
        "square": Square,
        "triangle": Triangle,
    }

    def create_shape(self, shape_type: str, **kwargs) -> Shape:
        """
        根据类型创建形状对象

        Args:
            shape_type: 形状类型('circle', 'square', 'triangle')
            **kwargs: 传递给形状构造函数的参数

        Returns:
            Shape 实例

        Raises:
            ValueError: 如果形状类型无效
        """
        shape_type = shape_type.lower()

        if shape_type not in self._shapes:
            raise ValueError(
                f"无效的形状类型: {shape_type}. "
                f"有效类型: {', '.join(self._shapes.keys())}"
            )

        shape_class = self._shapes[shape_type]
        return shape_class(**kwargs)

    @classmethod
    def register_shape(cls, name: str, shape_class: Type[Shape]) -> None:
        """
        注册新的形状类型

        Args:
            name: 形状名称
            shape_class: 形状类
        """
        cls._shapes[name.lower()] = shape_class


def main():
    """工厂模式示例"""
    print("=" * 50)
    print("工厂模式示例")
    print("=" * 50)

    factory = ShapeFactory()

    # 创建不同类型的形状
    print("\n使用工厂创建不同类型的形状:")
    print("-" * 50)

    circle = factory.create_shape("circle", radius=5)
    circle.draw()

    square = factory.create_shape("square", side=10)
    square.draw()

    triangle = factory.create_shape("triangle", base=8, height=6)
    triangle.draw()

    # 演示多态性
    print("\n" + "-" * 50)
    print("演示多态性 - 统一接口处理不同对象:")
    print("-" * 50)

    shapes = [
        factory.create_shape("circle", radius=3),
        factory.create_shape("square", side=5),
        factory.create_shape("triangle", base=4, height=3),
    ]

    for i, shape in enumerate(shapes, 1):
        print(f"{i}. {shape.__class__.__name__}: ", end="")
        shape.draw()

    # 演示错误处理
    print("\n" + "-" * 50)
    print("演示错误处理:")
    print("-" * 50)

    try:
        invalid_shape = factory.create_shape("pentagon")
    except ValueError as e:
        print(f"捕获到异常: {e}")

    print("\n" + "=" * 50)
    print("结论: 工厂模式封装了对象创建逻辑")
    print("=" * 50)


if __name__ == "__main__":
    main()
