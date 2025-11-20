"""
抽象工厂模式 (Abstract Factory Pattern)

意图:
    提供一个创建一系列相关或相互依赖对象的接口,而无需指定它们具体的类

适用场景:
    - 系统需要独立于产品的创建、组合和表示
    - 系统需要由多个产品系列中的一个来配置
    - 需要强调一系列相关产品对象的设计以便进行联合使用
    - 提供一个产品类库,只想显示接口而不是实现

Python 实现说明:
    定义抽象工厂接口和抽象产品接口
    具体工厂创建具体产品,确保产品族的一致性
"""
from abc import ABC, abstractmethod


# 抽象产品 - 按钮
class Button(ABC):
    """按钮抽象接口"""

    @abstractmethod
    def paint(self) -> str:
        """绘制按钮"""
        pass


# 抽象产品 - 复选框
class Checkbox(ABC):
    """复选框抽象接口"""

    @abstractmethod
    def paint(self) -> str:
        """绘制复选框"""
        pass


# 具体产品 - Windows 按钮
class WindowsButton(Button):
    """Windows 风格按钮"""

    def paint(self) -> str:
        result = "渲染 Windows 风格按钮"
        print(result)
        return result


# 具体产品 - Windows 复选框
class WindowsCheckbox(Checkbox):
    """Windows 风格复选框"""

    def paint(self) -> str:
        result = "渲染 Windows 风格复选框"
        print(result)
        return result


# 具体产品 - Mac 按钮
class MacButton(Button):
    """Mac 风��按钮"""

    def paint(self) -> str:
        result = "渲染 Mac 风格按钮"
        print(result)
        return result


# 具体产品 - Mac 复选框
class MacCheckbox(Checkbox):
    """Mac 风格复选框"""

    def paint(self) -> str:
        result = "渲染 Mac 风格复选框"
        print(result)
        return result


# 抽象工厂
class GUIFactory(ABC):
    """GUI 工厂抽象接口"""

    @abstractmethod
    def create_button(self) -> Button:
        """创建按钮"""
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """创建复选框"""
        pass


# 具体工厂 - Windows
class WindowsFactory(GUIFactory):
    """Windows GUI 工厂"""

    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


# 具体工厂 - Mac
class MacFactory(GUIFactory):
    """Mac GUI 工厂"""

    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


# 客户端代码
class Application:
    """使用 GUI 工厂的应用程序"""

    def __init__(self, factory: GUIFactory):
        """
        初始化应用程序

        Args:
            factory: GUI 工厂实例
        """
        self.factory = factory
        self.button = None
        self.checkbox = None

    def create_ui(self) -> None:
        """创建 UI 组件"""
        self.button = self.factory.create_button()
        self.checkbox = self.factory.create_checkbox()

    def paint(self) -> None:
        """渲染 UI"""
        self.button.paint()
        self.checkbox.paint()


def main():
    """抽象工厂模式示例"""
    print("=" * 60)
    print("抽象工厂模式示例")
    print("=" * 60)

    # 使用 Windows 工厂
    print("\n1. 使用 Windows 工厂创建 UI")
    print("-" * 60)
    windows_factory = WindowsFactory()
    app1 = Application(windows_factory)
    app1.create_ui()
    app1.paint()

    # 使用 Mac 工厂
    print("\n2. 使用 Mac 工厂创建 UI")
    print("-" * 60)
    mac_factory = MacFactory()
    app2 = Application(mac_factory)
    app2.create_ui()
    app2.paint()

    # 动态切换工厂
    print("\n3. 动态切换工厂")
    print("-" * 60)
    import platform
    system = platform.system()
    print(f"检测到操作系统: {system}")

    if system == "Windows":
        factory = WindowsFactory()
    elif system == "Darwin":  # macOS
        factory = MacFactory()
    else:
        factory = WindowsFactory()  # 默认

    app3 = Application(factory)
    app3.create_ui()
    print("使用适配当前系统的 UI:")
    app3.paint()

    print("\n" + "=" * 60)
    print("结论: 抽象工厂确保产品族的一致性")
    print("=" * 60)


if __name__ == "__main__":
    main()
