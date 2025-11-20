"""
抽象工厂模式测试
"""
import pytest


def test_abstract_factory_creates_product_family():
    """测试抽象工厂创建产品族"""
    from patterns.creational.abstract_factory import WindowsFactory, Application

    factory = WindowsFactory()
    app = Application(factory)
    app.create_ui()

    assert app.button is not None
    assert app.checkbox is not None
    assert "Windows" in app.button.paint()
    assert "Windows" in app.checkbox.paint()


def test_different_factories_create_different_products():
    """测试不同工厂创建不同产品"""
    from patterns.creational.abstract_factory import WindowsFactory, MacFactory

    windows_factory = WindowsFactory()
    mac_factory = MacFactory()

    windows_button = windows_factory.create_button()
    mac_button = mac_factory.create_button()

    assert type(windows_button).__name__ == "WindowsButton"
    assert type(mac_button).__name__ == "MacButton"


def test_product_family_consistency():
    """测试产品族的一致性"""
    from patterns.creational.abstract_factory import MacFactory, Application

    factory = MacFactory()
    app = Application(factory)
    app.create_ui()

    # Mac 工厂创建的所有组件都应该是 Mac 风格
    button_result = app.button.paint()
    checkbox_result = app.checkbox.paint()

    assert "Mac" in button_result
    assert "Mac" in checkbox_result


def test_application_can_switch_factories():
    """测试应用可以切换工厂"""
    from patterns.creational.abstract_factory import (
        WindowsFactory, MacFactory, Application
    )

    # 创建 Windows 应用
    app = Application(WindowsFactory())
    app.create_ui()
    assert "Windows" in app.button.paint()

    # 切换到 Mac 工厂
    app.factory = MacFactory()
    app.create_ui()
    assert "Mac" in app.button.paint()


def test_main_function():
    """测试 main 函数正常运行"""
    from patterns.creational.abstract_factory import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
