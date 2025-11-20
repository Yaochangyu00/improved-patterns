"""
单例模式 (Singleton Pattern)

意图:
    确保一个类只有一个实例,并提供全局访问点

适用场景:
    - 需要严格控制全局状态访问时
    - 系统中某个类只应该有一个实例(如配置管理器)
    - 需要延迟初始化的全局对象

Python 实现说明:
    在 Python 中,使用 __new__ 方法实现单例模式
"""
import threading


class Singleton:
    """
    单例类实现

    使用 __new__ 方法确保只创建一个实例
    使用锁保证线程安全
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        重写 __new__ 方法实现单例

        使用双重检查锁定模式确保线程安全
        """
        if cls._instance is None:
            with cls._lock:
                # 双重检查锁定
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化实例(只会执行一次)"""
        if not hasattr(self, '_initialized'):
            self.value = None
            self._initialized = True


def main():
    """单例模式示例"""
    print("=" * 50)
    print("单例模式示例")
    print("=" * 50)

    # 创建第一个实例
    print("\n创建第一个实例...")
    singleton1 = Singleton()
    singleton1.value = "第一次赋值"
    print(f"singleton1.value = {singleton1.value}")
    print(f"singleton1 的内存地址: {id(singleton1)}")

    # 创建第二个实例
    print("\n创建第二个实例...")
    singleton2 = Singleton()
    print(f"singleton2.value = {singleton2.value}")
    print(f"singleton2 的内存地址: {id(singleton2)}")

    # 验证是同一个实例
    print(f"\nsingleton1 和 singleton2 是同一个对象: {singleton1 is singleton2}")

    # 修改 singleton2 的值
    print("\n修改 singleton2.value...")
    singleton2.value = "第二次赋值"
    print(f"singleton1.value = {singleton1.value}")
    print(f"singleton2.value = {singleton2.value}")

    print("\n" + "=" * 50)
    print("结论: 单例模式确保了全局只有一个实例")
    print("=" * 50)


if __name__ == "__main__":
    main()
