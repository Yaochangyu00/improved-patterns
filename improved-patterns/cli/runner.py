"""
模式运行器模块

负责动态加载和运行设计模式示例
"""
import importlib
import sys
import time
from pathlib import Path
from typing import Optional

from cli.pattern_index import get_pattern_index


class PatternRunner:
    """模式运行器类"""

    def __init__(self):
        """初始化模式运行器"""
        self.pattern_index = get_pattern_index()

    def run_pattern(
        self,
        pattern_name: str,
        interactive: bool = False,
        timing: bool = False,
        verbose: bool = False
    ) -> bool:
        """
        运行指定的设计模式示例

        Args:
            pattern_name: 模式名称(ID或中文/英文名称)
            interactive: 是否使用交互模式
            timing: 是否显示执行时间
            verbose: 是否显示详细输出

        Returns:
            运行是否成功
        """
        # 查找模式
        pattern = self.pattern_index.find_pattern_by_name(pattern_name)

        if pattern is None:
            print(f"✗ 错误: 未找到模式 '{pattern_name}'")
            print("\n建议:")
            print("  • 使用 'patterns list' 查看所有可用模式")
            print("  • 检查拼写是否正确")
            return False

        # 显示运行信息
        print("=" * 60)
        print(f"运行模式: {pattern['name_zh']} ({pattern['name_en']})")
        print("=" * 60)

        try:
            # 动态导入模式模块
            module_path = self._get_module_path(pattern)
            if verbose:
                print(f"\n[DEBUG] 导入模块: {module_path}")

            module = importlib.import_module(module_path)

            # 获取入口函数
            entry_function = pattern.get("example", {}).get("entry_function", "main")
            if not hasattr(module, entry_function):
                print(f"✗ 错误: 模块中未找到 {entry_function} 函数")
                return False

            main_func = getattr(module, entry_function)

            # 运行示例
            print()
            start_time = time.time()

            if interactive:
                print("[交互模式]")
                main_func()
            else:
                main_func()

            elapsed_time = time.time() - start_time

            # 显示成功信息
            print()
            if timing:
                print(f"✓ 示例执行成功 (耗时: {elapsed_time:.3f}s)")
            else:
                print("✓ 示例执行成功")

            return True

        except ImportError as e:
            print(f"✗ 错误: 无法导入模块 - {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            return False

        except Exception as e:
            print(f"✗ 错误: 示例执行失败 - {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            return False

    def _get_module_path(self, pattern: dict) -> str:
        """
        根据模式信息获取模块导入路径

        Args:
            pattern: 模式字典

        Returns:
            模块导入路径(例如: 'patterns.creational.singleton')
        """
        # 从 code_path 生成模块路径
        # 例如: 'patterns/creational/singleton.py' -> 'patterns.creational.singleton'
        code_path = pattern["code_path"]
        module_path = code_path.replace("/", ".").replace("\\", ".")

        # 移除 .py 扩展名
        if module_path.endswith(".py"):
            module_path = module_path[:-3]

        return module_path


def run_pattern_cli(args) -> int:
    """
    CLI 入口函数

    Args:
        args: 命令行参数

    Returns:
        退出码(0 表示成功, 非0 表示失败)
    """
    runner = PatternRunner()

    success = runner.run_pattern(
        pattern_name=args.pattern,
        interactive=getattr(args, 'interactive', False),
        timing=getattr(args, 'timing', False),
        verbose=getattr(args, 'verbose', False)
    )

    return 0 if success else 10  # 10 = 示例运行失败
