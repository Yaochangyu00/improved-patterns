"""
测试运行器模块

负责运���设计模式的测试
"""
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from cli.pattern_index import get_pattern_index


class TestRunner:
    """测试运行器类"""

    def __init__(self):
        """初始化测试运行器"""
        self.pattern_index = get_pattern_index()
        self.project_root = Path(__file__).parent.parent

    def run_tests(
        self,
        pattern_name: Optional[str] = None,
        coverage: bool = False,
        verbose: bool = False,
        failfast: bool = False
    ) -> int:
        """
        运行测试

        Args:
            pattern_name: 模式名称(如果指定,只运行该模式的测试)
            coverage: 是否显示测试覆盖率
            verbose: 是否显示详细输出
            failfast: 是否在首次失败后停止

        Returns:
            测试退出码(0 表示成功)
        """
        # 构建 pytest 命令
        cmd = [sys.executable, "-m", "pytest"]

        if pattern_name:
            # 运行特定模式的测试
            pattern = self.pattern_index.find_pattern_by_name(pattern_name)

            if pattern is None:
                print(f"✗ 错误: 未找到模式 '{pattern_name}'")
                return 1

            test_path = self.pattern_index.get_pattern_path(pattern["id"], "test")

            if test_path is None or not test_path.exists():
                print(f"✗ 错误: 测试文件不存在: {test_path}")
                return 1

            cmd.append(str(test_path))

            print("━" * 60)
            print(f"运行测试: {pattern['name_zh']}")
            print("━" * 60)
            print()
        else:
            # 运行所有测试
            cmd.append("tests")

            print("━" * 60)
            print("运行所有测试")
            print("━" * 60)
            print()

        # 添加选项
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-v")  # 默认详细输出

        if failfast:
            cmd.append("-x")

        if coverage:
            cmd.extend(["--cov=patterns", "--cov=cli", "--cov-report=term-missing"])

        # 运行测试
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                check=False
            )

            print()
            if result.returncode == 0:
                print("✓ 所有测试通过")
            else:
                print("✗ 部分测试失败")

            return result.returncode

        except FileNotFoundError:
            print("✗ 错误: pytest 未安装")
            print("\n安装pytest:")
            print("  pip install pytest")
            if coverage:
                print("  pip install pytest-cov")
            return 1

        except Exception as e:
            print(f"✗ 错误: 测试运行失败 - {e}")
            return 1


def run_tests_cli(args) -> int:
    """
    CLI 入口函数

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    runner = TestRunner()

    return runner.run_tests(
        pattern_name=getattr(args, 'pattern', None),
        coverage=getattr(args, 'coverage', False),
        verbose=getattr(args, 'verbose', False),
        failfast=getattr(args, 'failfast', False)
    )
