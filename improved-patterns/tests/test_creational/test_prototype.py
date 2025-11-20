"""
原型模式测试
"""
import pytest


def test_prototype_clone_creates_copy():
    """测试原型克隆创建副本"""
    from patterns.creational.prototype import Rectangle

    original = Rectangle(10, 20, "red", 100, 50)
    clone = original.clone()

    assert clone.x == original.x
    assert clone.y == original.y
    assert clone.color == original.color
    assert clone is not original


def test_clone_modifications_are_independent():
    """测试克隆修改不影响原始对象"""
    from patterns.creational.prototype import Circle

    original = Circle(0, 0, "blue", 10)
    clone = original.clone()

    clone.x = 100
    clone.color = "red"

    assert original.x == 0
    assert original.color == "blue"


def test_shallow_clone_shares_nested_objects():
    """测试浅克隆共享嵌套对象"""
    from patterns.creational.prototype import Document

    original = Document("Title", "Content")
    original.metadata["tags"] = ["tag1"]

    shallow = original.clone()
    shallow.metadata["tags"].append("tag2")

    # 浅克隆共享嵌套对象
    assert "tag2" in original.metadata["tags"]


def test_deep_clone_copies_nested_objects():
    """测试深克隆复制嵌套对象"""
    from patterns.creational.prototype import Document

    original = Document("Title", "Content")
    original.metadata["tags"] = ["tag1"]

    deep = original.deep_clone()
    deep.metadata["tags"].append("tag2")

    # 深克隆不影响原始对象
    assert "tag2" not in original.metadata["tags"]


def test_prototype_registry():
    """测试原型注册表"""
    from patterns.creational.prototype import PrototypeRegistry, Circle

    registry = PrototypeRegistry()
    registry.register("circle", Circle(0, 0, "green", 5))

    clone = registry.clone("circle")

    assert isinstance(clone, Circle)
    assert clone.color == "green"
    assert clone.radius == 5


def test_registry_clone_invalid_name():
    """测试注册表克隆无效名称抛出异常"""
    from patterns.creational.prototype import PrototypeRegistry

    registry = PrototypeRegistry()

    with pytest.raises(ValueError):
        registry.clone("nonexistent")


def test_main_function():
    """测试 main 函数正常运行"""
    from patterns.creational.prototype import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
