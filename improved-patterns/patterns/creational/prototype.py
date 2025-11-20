"""
原型模式 (Prototype Pattern)

意图:
    用原型实例指定创建对象的种类,并且通过复制这些原型创建新的对象

适用场景:
    - 需要在运行时创建对象,但直接创建成本太高
    - 避免创建与产品类层次平行的工厂类层次
    - 类的实例只能有几个不同状态组合中的一种时
    - 通过克隆创建对象比通过构造函数创建更方便

Python 实现说明:
    使用 copy 模块实现浅复制和深复制
    实现 __copy__ 和 __deepcopy__ 方法自定义复制行为
"""
import copy
from abc import ABC, abstractmethod
from typing import Dict, Any


# 原型接口
class Prototype(ABC):
    """原型抽象接口"""

    @abstractmethod
    def clone(self) -> 'Prototype':
        """克隆自身"""
        pass


# 具体原型 - 形状
class Shape(Prototype):
    """形状原型基类"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black"):
        """
        初始化形状

        Args:
            x: X 坐标
            y: Y 坐标
            color: 颜色
        """
        self.x = x
        self.y = y
        self.color = color

    def clone(self) -> 'Shape':
        """浅克隆"""
        return copy.copy(self)

    def deep_clone(self) -> 'Shape':
        """深克隆"""
        return copy.deepcopy(self)


class Rectangle(Shape):
    """矩形"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black",
                 width: int = 10, height: int = 10):
        """
        初始化矩形

        Args:
            width: 宽度
            height: 高度
        """
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return (f"矩形(位置=({self.x}, {self.y}), "
                f"颜色={self.color}, "
                f"大小={self.width}x{self.height})")


class Circle(Shape):
    """圆形"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black",
                 radius: int = 5):
        """
        初始化圆形

        Args:
            radius: 半径
        """
        super().__init__(x, y, color)
        self.radius = radius

    def __str__(self) -> str:
        return (f"圆形(位置=({self.x}, {self.y}), "
                f"颜色={self.color}, "
                f"半径={self.radius})")


# 包含引用类型的对象
class Document(Prototype):
    """文档类,包含嵌套对象"""

    def __init__(self, title: str, content: str):
        """
        初始化文档

        Args:
            title: 标题
            content: 内容
        """
        self.title = title
        self.content = content
        self.metadata: Dict[str, Any] = {
            "author": "未知",
            "tags": [],
            "created": "2024-01-01"
        }

    def clone(self) -> 'Document':
        """浅克隆 - 嵌套对象共享引用"""
        return copy.copy(self)

    def deep_clone(self) -> 'Document':
        """深克隆 - 嵌套对象也被复制"""
        return copy.deepcopy(self)

    def __str__(self) -> str:
        return f"文档(标题='{self.title}', 作者={self.metadata['author']}, 标签={self.metadata['tags']})"


# 原型注册表
class PrototypeRegistry:
    """原型注册表,管理预定义的原型"""

    def __init__(self):
        """初始化注册表"""
        self._prototypes: Dict[str, Prototype] = {}

    def register(self, name: str, prototype: Prototype) -> None:
        """
        注册原型

        Args:
            name: 原型名称
            prototype: 原型实例
        """
        self._prototypes[name] = prototype

    def unregister(self, name: str) -> None:
        """
        注销原型

        Args:
            name: 原型名称
        """
        del self._prototypes[name]

    def clone(self, name: str) -> Prototype:
        """
        克隆指定名称的原型

        Args:
            name: 原型名称

        Returns:
            克隆的实例
        """
        prototype = self._prototypes.get(name)
        if prototype is None:
            raise ValueError(f"未找到原型: {name}")
        return prototype.clone()


def main():
    """原型模式示例"""
    print("=" * 60)
    print("原型模式示例")
    print("=" * 60)

    # 示例 1: 基本克隆
    print("\n1. 基本克隆")
    print("-" * 60)
    original_rect = Rectangle(0, 0, "red", 100, 50)
    print(f"原始矩形: {original_rect}")

    cloned_rect = original_rect.clone()
    cloned_rect.x = 10
    cloned_rect.y = 20
    cloned_rect.color = "blue"
    print(f"克隆矩形: {cloned_rect}")
    print(f"原始矩形未变: {original_rect}")

    # 示例 2: 浅克隆 vs 深克隆
    print("\n2. 浅克隆 vs 深克隆")
    print("-" * 60)
    original_doc = Document("报告", "这是内容")
    original_doc.metadata["author"] = "张三"
    original_doc.metadata["tags"] = ["重要", "技术"]
    print(f"原始文档: {original_doc}")

    # 浅克隆 - 共享嵌套对象
    shallow_clone = original_doc.clone()
    shallow_clone.title = "报告副本"
    shallow_clone.metadata["tags"].append("副本")  # 这会影响原始对象!
    print(f"\n浅克隆文档: {shallow_clone}")
    print(f"原始文档(标签被改变了!): {original_doc}")

    # 深克隆 - 完全独立
    original_doc2 = Document("设计", "设计内容")
    original_doc2.metadata["tags"] = ["设计"]
    print(f"\n新原始文档: {original_doc2}")

    deep_clone = original_doc2.deep_clone()
    deep_clone.metadata["tags"].append("克隆")  # 不影响原始对象
    print(f"深克隆文档: {deep_clone}")
    print(f"原始文档(未被改变): {original_doc2}")

    # 示例 3: 使用原型注册表
    print("\n3. 使用原型注册表")
    print("-" * 60)
    registry = PrototypeRegistry()

    # 注册预定义原型
    registry.register("小圆", Circle(0, 0, "green", 5))
    registry.register("大圆", Circle(0, 0, "blue", 20))
    registry.register("标准矩形", Rectangle(0, 0, "gray", 100, 50))

    # 从注册表克隆
    circle1 = registry.clone("小圆")
    circle1.x = 100
    print(f"克隆的小圆: {circle1}")

    circle2 = registry.clone("大圆")
    circle2.color = "red"
    print(f"克隆的大圆: {circle2}")

    rect = registry.clone("标准矩形")
    rect.width = 200
    print(f"克隆的矩形: {rect}")

    print("\n" + "=" * 60)
    print("结论: 原型模式通过复制现有对象来创建新对象")
    print("=" * 60)


if __name__ == "__main__":
    main()
