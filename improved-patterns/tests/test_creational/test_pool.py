"""
对象池模式测试
"""
import pytest


def test_pool_creates_min_objects():
    """测试对象池创建最小数量对象"""
    from patterns.creational.pool import ConnectionPool

    pool = ConnectionPool(min_connections=3, max_connections=5)
    stats = pool.get_stats()

    assert stats["total"] == 3
    assert stats["available"] == 3


def test_pool_acquire_returns_object():
    """测试从池获取对象"""
    from patterns.creational.pool import ConnectionPool

    pool = ConnectionPool(min_connections=2, max_connections=5)
    conn = pool.acquire()

    assert conn is not None
    assert conn.in_use is True


def test_pool_release_returns_object():
    """测试释放对象回池"""
    from patterns.creational.pool import ConnectionPool

    pool = ConnectionPool(min_connections=2, max_connections=5)

    conn = pool.acquire()
    initial_available = pool.get_stats()["available"]

    pool.release(conn)
    final_available = pool.get_stats()["available"]

    assert final_available == initial_available + 1
    assert conn.in_use is False


def test_pool_expands_when_needed():
    """测试池在需要时扩展"""
    from patterns.creational.pool import ConnectionPool

    pool = ConnectionPool(min_connections=2, max_connections=5)

    # 获取所有初始连接
    conns = [pool.acquire() for _ in range(2)]
    assert pool.get_stats()["available"] == 0

    # 获取更多连接(触发扩展)
    conn3 = pool.acquire()
    assert pool.get_stats()["total"] == 3

    for c in conns:
        pool.release(c)
    pool.release(conn3)


def test_database_connection_execute():
    """测试数据库连接执行查询"""
    from patterns.creational.pool import DatabaseConnection

    conn = DatabaseConnection("localhost", 5432)
    result = conn.execute("SELECT 1")

    assert "SELECT 1" in result
    assert conn.query_count == 1


def test_connection_reset():
    """测试连接重置"""
    from patterns.creational.pool import DatabaseConnection

    conn = DatabaseConnection("localhost", 5432)
    conn.in_use = True
    conn.query_count = 5

    conn.reset()

    assert conn.in_use is False
    assert conn.query_count == 0


def test_main_function():
    """测试 main 函数正常运行"""
    from patterns.creational.pool import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
