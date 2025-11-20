"""
观察者模式测试

测试观察者模式的核心功能
"""
import pytest


def test_observer_registration():
    """测试观察者可以注册到主题"""
    from patterns.behavioral.observer import Subject, Observer

    subject = Subject()
    observer = Observer(name="Observer1")

    subject.attach(observer)
    assert observer in subject._observers, "观察者应该被成功注册"


def test_observer_notification():
    """测试观察者能够接收通知"""
    from patterns.behavioral.observer import Subject, Observer

    subject = Subject()
    observer = Observer(name="Observer1")

    subject.attach(observer)
    subject.state = "new_state"

    # 观察者应该收到了更新
    assert observer.state == "new_state", "观察者应该接收到状态更新"


def test_observer_detachment():
    """测试观察者可以取消注册"""
    from patterns.behavioral.observer import Subject, Observer

    subject = Subject()
    observer = Observer(name="Observer1")

    subject.attach(observer)
    subject.detach(observer)

    assert observer not in subject._observers, "观察者应该被成功移除"


def test_observer_multiple_observers():
    """测试多个观察者同时接收通知"""
    from patterns.behavioral.observer import Subject, Observer

    subject = Subject()
    observer1 = Observer(name="Observer1")
    observer2 = Observer(name="Observer2")
    observer3 = Observer(name="Observer3")

    subject.attach(observer1)
    subject.attach(observer2)
    subject.attach(observer3)

    subject.state = "shared_state"

    # 所有观察者都应该收到更新
    assert observer1.state == "shared_state", "观察者1应该接收到状态更新"
    assert observer2.state == "shared_state", "观察者2应该接收到状态更新"
    assert observer3.state == "shared_state", "观察者3应该接收到状态更新"


def test_observer_partial_notification():
    """测试部分观察者取消注册后的通知"""
    from patterns.behavioral.observer import Subject, Observer

    subject = Subject()
    observer1 = Observer(name="Observer1")
    observer2 = Observer(name="Observer2")

    subject.attach(observer1)
    subject.attach(observer2)

    subject.state = "first_state"
    assert observer1.state == "first_state"
    assert observer2.state == "first_state"

    # 移除 observer1
    subject.detach(observer1)

    subject.state = "second_state"
    assert observer1.state == "first_state", "observer1 不应该收到第二次更新"
    assert observer2.state == "second_state", "observer2 应该收到第二次更新"


def test_observer_main_function():
    """测试观察者模式的 main 函数可以正常运行"""
    from patterns.behavioral.observer import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
