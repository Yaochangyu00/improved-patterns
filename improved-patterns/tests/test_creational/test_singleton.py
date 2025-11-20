"""
单例模式测试

测试单例模式的核心功能
"""
import pytest


def test_singleton_single_instance():
    """测试单例模式确保只有一个实例"""
    from patterns.creational.singleton import Singleton

    instance1 = Singleton()
    instance2 = Singleton()

    assert instance1 is instance2, "两个实例应该是同一个对象"


def test_singleton_state_sharing():
    """测试单例实例之间共享状态"""
    from patterns.creational.singleton import Singleton

    instance1 = Singleton()
    instance1.value = "test_value"

    instance2 = Singleton()
    assert instance2.value == "test_value", "实例之间应该共享状态"


def test_singleton_thread_safety():
    """测试单例模式的线程安全性"""
    from patterns.creational.singleton import Singleton
    import threading

    instances = []

    def create_instance():
        instances.append(Singleton())

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # 所有实例应该是同一个对象
    assert all(inst is instances[0] for inst in instances), "在多线程环境中应该只有一个实例"


def test_singleton_main_function():
    """测试单例模式的 main 函数可以正常运行"""
    from patterns.creational.singleton import main

    # main 函数应该能够正常执行而不抛出异常
    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
