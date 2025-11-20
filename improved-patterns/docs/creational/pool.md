# 对象池模式 (Object Pool Pattern)

## 意图

通过对象复用避免频繁创建和销毁的开销,提高性能和资源利用率。

## 问题

频繁创建和销毁对象面临的问题:
- 对象创建成本很高(如数据库连接)
- 系统资源有限需要控制对象数量
- 频繁的内存分配/释放影响性能
- 垃圾回收压力大

## 解决方案

对象池预先创建一组对象,需要时从池中获取,用完后归还:
1. 初始化时创建最小数量的对象
2. 获取时从池中取出对象
3. 使用完毕后归还对象
4. 按需扩展,但不超过最大容量

## 适用场景

1. **对象创建成本很高**
   - 例如:数据库连接、线程、网络连接

2. **需要频繁创建和销毁相似对象**
   - 例如:请求处理器、图形对象

3. **对象数量有限但需要控制**
   - 例如:许可证限制的资源

4. **需要提高性能和资源利用率**
   - 例如:高并发服务器

## 结构

```
   Client
      |
      ↓
 ObjectPool
 +acquire()
 +release()
      |
      ↓
[Object1][Object2][Object3]...
```

## Python 实现

参见代码: `patterns/creational/pool.py`

### 关键点
- 使用队列(Queue)管理可用对象
- 实现获取(acquire)和释放(release)方法
- 对象需要reset方法重置状态
- 使用锁保证线程安全

### 代码示例

```python
pool = ConnectionPool(min_connections=3, max_connections=10)

# 获取连接
conn = pool.acquire()
conn.execute("SELECT * FROM users")

# 释放连接
pool.release(conn)
```

## 优点

✓ **减少创建开销**: 复用对象避免频繁创建
✓ **控制资源使用**: 限制对象数量
✓ **提高响应速度**: 预创建对象减少等待
✓ **减少GC压力**: 对象复用减少垃圾回收

## 缺点

✗ **增加复杂度**: 需要管理池的生命周期
✗ **对象状态问题**: 必须正确重置对象状态
✗ **可能浪费资源**: 预创建的对象可能未被使用
✗ **线程安全**: 需要处理并发访问

## 最佳实践

### Python 特定建议
- 使用 `queue.Queue` 管理对象池
- 使用上下文管理器自动释放对象
- 考虑使用 `multiprocessing.Pool` 或线程池

### 通用建议
- 正确重置对象状态(reset方法)
- 设置合理的最小和最大容量
- 实现超时机制避免死锁
- 监控池的使用情况

## 上下文管理器实现

```python
@contextmanager
def get_connection(pool):
    conn = pool.acquire()
    try:
        yield conn
    finally:
        pool.release(conn)

with get_connection(pool) as conn:
    conn.execute(query)
```

## 真实应用案例

1. **数据库连接池**: SQLAlchemy, Django ORM
2. **线程池**: `concurrent.futures.ThreadPoolExecutor`
3. **HTTP 连接池**: `requests.Session`
4. **Worker 池**: Celery 的 worker 进程

## 相关模式

- **单例模式**: 池管理器通常是单例
- **工厂模式**: 池可以使用工厂创建对象
- **享元模式**: 都是共享对象,但目的不同

## 注意事项

1. **状态清理**: 归还前必须清理对象状态
2. **异常处理**: 确保异常时也能归还对象
3. **监控**: 监控池的使用率和等待时间
4. **超时**: 获取对象应该有超时机制

## 对比

| 特性 | 对象池 | 享元模式 |
|-----|-------|---------|
| 目的 | 减少创建开销 | 减少内存使用 |
| 对象所有权 | 临时借用 | 共享持有 |
| 状态 | 可变状态 | 内部状态不可变 |
| 典型应用 | 连接池 | 字符/图形缓存 |

## 进一步学习

- 运行示例: `patterns run pool`
- 查看代码: `patterns/creational/pool.py`
- 运行测试: `patterns test pool`
