"""
观察者模式 (Observer Pattern)

意图:
    定义对象间的一对多依赖关系,当一个对象状态改变时,所有依赖它的对象都会收到通知并自动更新

适用场景:
    - 当一个对象的改变需要同时改变其他对象,但不知道具体有多少对象需要改变时
    - 当一个对象必须通知其他对象,但又不希望与被通知的对象形成紧耦合时
    - 需要创建一个触发链,使得对象A的行为影响对象B,对象B又影响对象C

Python 实现说明:
    实现 Subject(主题)和 Observer(观察者)接口
    主题维护观察者列表,状态改变时通知所有观察者
"""
from abc import ABC, abstractmethod
from typing import List


class ObserverInterface(ABC):
    """观察者接口"""

    @abstractmethod
    def update(self, subject: 'SubjectInterface') -> None:
        """
        接收主题的更新通知

        Args:
            subject: 发生变化的主题对象
        """
        pass


class SubjectInterface(ABC):
    """主题接口"""

    @abstractmethod
    def attach(self, observer: ObserverInterface) -> None:
        """添加观察者"""
        pass

    @abstractmethod
    def detach(self, observer: ObserverInterface) -> None:
        """移除观察者"""
        pass

    @abstractmethod
    def notify(self) -> None:
        """通知所有观察者"""
        pass


class Subject(SubjectInterface):
    """
    具体主题类

    维护观察者列表,状态改变时通知所有观察者
    """

    def __init__(self):
        """初始化主题"""
        self._observers: List[ObserverInterface] = []
        self._state: str = ""

    @property
    def state(self) -> str:
        """获取主题状态"""
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        """
        设置主题状态并通知观察者

        Args:
            value: 新的状态值
        """
        print(f"\n主题状态改变: {self._state} -> {value}")
        self._state = value
        self.notify()

    def attach(self, observer: ObserverInterface) -> None:
        """
        添加观察者

        Args:
            observer: 要添加的观察者
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"观察者已添加: {observer}")

    def detach(self, observer: ObserverInterface) -> None:
        """
        移除观察者

        Args:
            observer: 要移除的观察者
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"观察者已移除: {observer}")

    def notify(self) -> None:
        """通知所有观察者"""
        print(f"正在通知 {len(self._observers)} 个观察者...")
        for observer in self._observers:
            observer.update(self)


class Observer(ObserverInterface):
    """
    具体观察者类

    接收主题的更新通知并做出响应
    """

    def __init__(self, name: str):
        """
        初始化观察者

        Args:
            name: 观察者名称
        """
        self.name = name
        self.state: str = ""

    def update(self, subject: SubjectInterface) -> None:
        """
        接收主题的更新通知

        Args:
            subject: 发生变化的主题对象
        """
        self.state = subject.state
        print(f"  → {self.name} 收到更新,新状态: {self.state}")

    def __str__(self) -> str:
        """返回观察者的字符串表示"""
        return f"Observer({self.name})"


def main():
    """观察者模式示例"""
    print("=" * 60)
    print("观察者模式示例")
    print("=" * 60)

    # 创建主题
    subject = Subject()

    # 创建观察者
    observer1 = Observer("观察者1")
    observer2 = Observer("观察者2")
    observer3 = Observer("观察者3")

    print("\n1. 添加观察者")
    print("-" * 60)
    subject.attach(observer1)
    subject.attach(observer2)
    subject.attach(observer3)

    # 改变主题状态 - 所有观察者都会收到通知
    print("\n2. 改变主题状态 - 所有观察者收到通知")
    print("-" * 60)
    subject.state = "状态A"

    # 改变主题状态 - 再次通知所有观察者
    print("\n3. 再次改变主题状态")
    print("-" * 60)
    subject.state = "状态B"

    # 移除一个观察者
    print("\n4. 移除观察者2")
    print("-" * 60)
    subject.detach(observer2)

    # 改变主题状态 - 只有剩余的观察者收到通知
    print("\n5. 改变主题状态 - 只有观察者1和3收到通知")
    print("-" * 60)
    subject.state = "状态C"

    # 验证观察者状态
    print("\n6. 验证观察者状态")
    print("-" * 60)
    print(f"{observer1.name} 的状态: {observer1.state}")
    print(f"{observer2.name} 的状态: {observer2.state} (未收到最后一次更新)")
    print(f"{observer3.name} 的状态: {observer3.state}")

    print("\n" + "=" * 60)
    print("结论: 观察者模式实现了一对多的依赖关系")
    print("=" * 60)


if __name__ == "__main__":
    main()
