"""
建造者模式 (Builder Pattern)

意图:
    将一个复杂对象的构建与它的表示分离,使得同样的构建过程可以创建不同的表示

适用场景:
    - 需要创建的对象有复杂的内部结构
    - 需要生成的对象内部属性相互依赖
    - 对象的创建过程独立于创建该对象的类
    - 隔离复杂对象的创建和使用,相同的创建过程可以创建不同的产品

Python 实现说明:
    定义 Builder 接口和具体 Builder
    使用 Director 控制构建过程
    支持链式调用提高可读性
"""
from abc import ABC, abstractmethod
from typing import List


# 产品类
class Computer:
    """计算机产品类"""

    def __init__(self):
        """初始化计算机"""
        self.cpu: str = ""
        self.ram: str = ""
        self.storage: str = ""
        self.gpu: str = ""
        self.os: str = ""

    def __str__(self) -> str:
        """返回计算机配置的字符串表示"""
        parts = [
            f"CPU: {self.cpu}",
            f"RAM: {self.ram}",
            f"存储: {self.storage}",
        ]
        if self.gpu:
            parts.append(f"GPU: {self.gpu}")
        if self.os:
            parts.append(f"操作系统: {self.os}")

        return "计算机配置:\n  " + "\n  ".join(parts)


# 抽象建造者
class ComputerBuilder(ABC):
    """计算机建造者抽象接口"""

    def __init__(self):
        """初始化建造者"""
        self.computer = Computer()

    @abstractmethod
    def build_cpu(self) -> 'ComputerBuilder':
        """构建 CPU"""
        pass

    @abstractmethod
    def build_ram(self) -> 'ComputerBuilder':
        """构建内存"""
        pass

    @abstractmethod
    def build_storage(self) -> 'ComputerBuilder':
        """构建存储"""
        pass

    def build_gpu(self) -> 'ComputerBuilder':
        """构建 GPU (可选)"""
        return self

    def build_os(self) -> 'ComputerBuilder':
        """构建操作系统 (可选)"""
        return self

    def get_computer(self) -> Computer:
        """获取构建好的计算机"""
        return self.computer


# 具体建造者 - 办公电脑
class OfficeComputerBuilder(ComputerBuilder):
    """办公电脑建造者"""

    def build_cpu(self) -> 'OfficeComputerBuilder':
        self.computer.cpu = "Intel Core i5"
        return self

    def build_ram(self) -> 'OfficeComputerBuilder':
        self.computer.ram = "8GB DDR4"
        return self

    def build_storage(self) -> 'OfficeComputerBuilder':
        self.computer.storage = "256GB SSD"
        return self

    def build_os(self) -> 'OfficeComputerBuilder':
        self.computer.os = "Windows 11 Pro"
        return self


# 具体建造者 - 游戏电脑
class GamingComputerBuilder(ComputerBuilder):
    """游戏电脑建造者"""

    def build_cpu(self) -> 'GamingComputerBuilder':
        self.computer.cpu = "Intel Core i9"
        return self

    def build_ram(self) -> 'GamingComputerBuilder':
        self.computer.ram = "32GB DDR5"
        return self

    def build_storage(self) -> 'GamingComputerBuilder':
        self.computer.storage = "2TB NVMe SSD"
        return self

    def build_gpu(self) -> 'GamingComputerBuilder':
        self.computer.gpu = "NVIDIA RTX 4090"
        return self

    def build_os(self) -> 'GamingComputerBuilder':
        self.computer.os = "Windows 11 Home"
        return self


# 具体建造者 - 服务器
class ServerBuilder(ComputerBuilder):
    """服务器建造者"""

    def build_cpu(self) -> 'ServerBuilder':
        self.computer.cpu = "AMD EPYC 64-Core"
        return self

    def build_ram(self) -> 'ServerBuilder':
        self.computer.ram = "128GB ECC"
        return self

    def build_storage(self) -> 'ServerBuilder':
        self.computer.storage = "10TB SSD RAID"
        return self

    def build_os(self) -> 'ServerBuilder':
        self.computer.os = "Ubuntu Server 22.04 LTS"
        return self


# 指挥者
class ComputerDirector:
    """计算机构建指挥者"""

    def __init__(self, builder: ComputerBuilder):
        """
        初始化指挥者

        Args:
            builder: 建造者实例
        """
        self.builder = builder

    def construct_minimal_computer(self) -> Computer:
        """构建最小配置计算机"""
        return (self.builder
                .build_cpu()
                .build_ram()
                .build_storage()
                .get_computer())

    def construct_full_computer(self) -> Computer:
        """构建完整配置计算机"""
        return (self.builder
                .build_cpu()
                .build_ram()
                .build_storage()
                .build_gpu()
                .build_os()
                .get_computer())


def main():
    """建造者模式示例"""
    print("=" * 60)
    print("建造者模式示例")
    print("=" * 60)

    # 方式 1: 使用指挥者构建
    print("\n1. 使用指挥者构建办公电脑")
    print("-" * 60)
    office_builder = OfficeComputerBuilder()
    director = ComputerDirector(office_builder)
    office_computer = director.construct_full_computer()
    print(office_computer)

    # 方式 2: 直接使用建造者(链式调用)
    print("\n2. 直接构建游戏电脑(链式调用)")
    print("-" * 60)
    gaming_computer = (GamingComputerBuilder()
                       .build_cpu()
                       .build_ram()
                       .build_storage()
                       .build_gpu()
                       .build_os()
                       .get_computer())
    print(gaming_computer)

    # 方式 3: 构建最小配置
    print("\n3. 构建最小配置服务器")
    print("-" * 60)
    server_builder = ServerBuilder()
    director2 = ComputerDirector(server_builder)
    minimal_server = director2.construct_minimal_computer()
    print(minimal_server)

    # 方式 4: 自定义构建过程
    print("\n4. 自定义构建过程")
    print("-" * 60)
    custom_computer = (OfficeComputerBuilder()
                       .build_cpu()
                       .build_ram()
                       .build_storage()
                       # 跳过 GPU
                       # 跳过 OS
                       .get_computer())
    print(custom_computer)

    print("\n" + "=" * 60)
    print("结论: 建造者模式分离了对象的构建和表示")
    print("=" * 60)


if __name__ == "__main__":
    main()
