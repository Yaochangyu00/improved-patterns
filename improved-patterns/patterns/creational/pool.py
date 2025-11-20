"""
对象池模式 (Object Pool Pattern)

意图:
    运用共享技术有效地支持大量细粒度的对象,通过对象复用避免频繁创建和销毁的开销

适用场景:
    - 对象创建成本很高(如数据库连接、线程)
    - 需要频繁创建和销毁相似对象
    - 对象数量有限但需要控制
    - 需要提高性能和资源利用率

Python 实现说明:
    使用队列管理可用对象
    提供获取(acquire)和释放(release)方法
    支持自动扩展和收缩
"""
import queue
import threading
import time
from typing import Any, Callable, Optional
from abc import ABC, abstractmethod


# 可池化对象接口
class PoolableObject(ABC):
    """可池化对象的抽象接口"""

    @abstractmethod
    def reset(self) -> None:
        """重置对象状态,准备被复用"""
        pass


# 具体的可池化对象 - 数据库连接
class DatabaseConnection(PoolableObject):
    """数据库连接(模拟)"""

    _id_counter = 0
    _lock = threading.Lock()

    def __init__(self, host: str = "localhost", port: int = 5432):
        """
        初始化数据库连接

        Args:
            host: 数据库主机
            port: 数据库端口
        """
        with DatabaseConnection._lock:
            DatabaseConnection._id_counter += 1
            self.id = DatabaseConnection._id_counter

        self.host = host
        self.port = port
        self.in_use = False
        self.query_count = 0

        # 模拟创建连接的开销
        print(f"  创建连接 #{self.id} (耗时操作...)")
        time.sleep(0.1)  # 模拟连接时间

    def execute(self, query: str) -> str:
        """
        执行查询

        Args:
            query: SQL 查询

        Returns:
            查询结果
        """
        self.query_count += 1
        return f"连接 #{self.id} 执行: {query}"

    def reset(self) -> None:
        """重置连接状态"""
        self.in_use = False
        self.query_count = 0

    def __str__(self) -> str:
        status = "使用中" if self.in_use else "空闲"
        return f"Connection #{self.id} [{status}] (查询数: {self.query_count})"


# 对象池
class ObjectPool:
    """通用对象池"""

    def __init__(
        self,
        factory: Callable[[], PoolableObject],
        min_size: int = 2,
        max_size: int = 10
    ):
        """
        初始化对象池

        Args:
            factory: 对象工厂函数
            min_size: 最小池大小
            max_size: 最大池大小
        """
        self.factory = factory
        self.min_size = min_size
        self.max_size = max_size
        self.pool: queue.Queue = queue.Queue(maxsize=max_size)
        self.size = 0
        self._lock = threading.Lock()

        # 预创建最小数量的对象
        print(f"初始化对象池 (min={min_size}, max={max_size})")
        for _ in range(min_size):
            self._create_object()

    def _create_object(self) -> PoolableObject:
        """创建新对象并加入池中"""
        obj = self.factory()
        self.size += 1
        self.pool.put(obj)
        return obj

    def acquire(self, timeout: Optional[float] = None) -> PoolableObject:
        """
        从池中获取对象

        Args:
            timeout: 等待超时时间(秒)

        Returns:
            池中的对象

        Raises:
            queue.Empty: 超时未能获取对象
        """
        try:
            # 尝试从池中获取
            obj = self.pool.get(block=False)
        except queue.Empty:
            # 池为空,尝试创建新对象
            with self._lock:
                if self.size < self.max_size:
                    obj = self.factory()
                    self.size += 1
                else:
                    # 已达最大容量,等待
                    obj = self.pool.get(block=True, timeout=timeout)

        obj.in_use = True
        return obj

    def release(self, obj: PoolableObject) -> None:
        """
        将对象释放回池中

        Args:
            obj: 要释放的对象
        """
        obj.reset()
        self.pool.put(obj)

    def get_stats(self) -> dict:
        """获取池状态统计"""
        return {
            "total": self.size,
            "available": self.pool.qsize(),
            "in_use": self.size - self.pool.qsize()
        }


# 连接池(特���版本)
class ConnectionPool(ObjectPool):
    """数据库连接池"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        min_connections: int = 2,
        max_connections: int = 10
    ):
        """
        初始化连接池

        Args:
            host: 数据库主机
            port: 数据库端口
            min_connections: 最小连接数
            max_connections: 最大连接数
        """
        self.host = host
        self.port = port

        def factory():
            return DatabaseConnection(host, port)

        super().__init__(factory, min_connections, max_connections)


def main():
    """对象池模式示例"""
    print("=" * 60)
    print("对象池模式示例")
    print("=" * 60)

    # 创建连接池
    print("\n1. 创建数据库连接池")
    print("-" * 60)
    pool = ConnectionPool(min_connections=3, max_connections=5)
    print(f"池状态: {pool.get_stats()}")

    # 获取连接
    print("\n2. 从池中获取连接")
    print("-" * 60)
    conn1 = pool.acquire()
    print(f"获取连接: {conn1}")
    result = conn1.execute("SELECT * FROM users")
    print(f"查询结果: {result}")

    conn2 = pool.acquire()
    print(f"获取连接: {conn2}")
    conn2.execute("SELECT * FROM orders")

    print(f"池状态: {pool.get_stats()}")

    # 释放连接
    print("\n3. 释放连接回池中")
    print("-" * 60)
    pool.release(conn1)
    print(f"释放连接 #{conn1.id}")
    print(f"池状态: {pool.get_stats()}")

    # 重新获取(复用)
    print("\n4. 重新获取连接(复用)")
    print("-" * 60)
    conn3 = pool.acquire()
    print(f"获取连接: {conn3} (可能是复用的连接)")
    conn3.execute("INSERT INTO logs ...")

    # 测试池扩展
    print("\n5. 测试池扩展")
    print("-" * 60)
    connections = []
    for i in range(4):
        conn = pool.acquire()
        connections.append(conn)
        print(f"获取连接 {i+1}: #{conn.id}")

    print(f"池状态: {pool.get_stats()}")

    # 释放所有连接
    print("\n6. 释放所有连接")
    print("-" * 60)
    pool.release(conn2)
    pool.release(conn3)
    for conn in connections:
        pool.release(conn)

    print(f"最终池状态: {pool.get_stats()}")

    print("\n" + "=" * 60)
    print("结论: 对象池通过复用对象减少创建开销")
    print("=" * 60)


if __name__ == "__main__":
    main()
