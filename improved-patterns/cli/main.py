"""
CLI 主入口模块

实现命令行工具的主要功能
"""
import argparse
import sys
from typing import List, Optional

from cli import __version__
from cli.runner import run_pattern_cli
from cli.viewer import view_docs_cli
from cli.test_runner import run_tests_cli
from cli.pattern_index import get_pattern_index
from cli.config_loader import get_config_loader


def cmd_list(args) -> int:
    """
    list 命令处理函数

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    pattern_index = get_pattern_index()
    config_loader = get_config_loader()

    # 获取分类参数
    category = getattr(args, 'category', None)

    if category:
        # 列出特定分类的模式
        cat_obj = config_loader.get_category_by_name(category)
        if not cat_obj:
            print(f"✗ 错误: 未找到分类 '{category}'")
            return 1

        patterns = pattern_index.get_patterns_by_category(cat_obj["name"])
        print(f"\n{cat_obj['display_name_zh']} ({cat_obj['name'].capitalize()} Patterns)")
        print("━" * 60)
    else:
        # 列出所有模式,按分类分组
        categories = config_loader.load_categories()

        for cat in categories:
            patterns = pattern_index.get_patterns_by_category(cat["name"])
            if not patterns:
                continue

            print(f"\n{cat['display_name_zh']} ({cat['name'].capitalize()} Patterns)")
            print("━" * 60)

            _print_pattern_list(patterns)

        return 0

    _print_pattern_list(patterns)
    return 0


def _print_pattern_list(patterns: List[dict]) -> None:
    """
    打印模式列表

    Args:
        patterns: 模式列表
    """
    if not patterns:
        print("(无可用模式)")
        return

    # 打印表头
    print(f"{'ID':<20} {'中文名称':<15} {'描述'}")
    print("─" * 60)

    # 打印每个模式
    for pattern in patterns:
        print(
            f"{pattern['id']:<20} "
            f"{pattern['name_zh']:<15} "
            f"{pattern['description_zh'][:30]}"
        )

    print(f"\n共 {len(patterns)} 个模式")


def cmd_run(args) -> int:
    """
    run 命令处理函数

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    return run_pattern_cli(args)


def cmd_docs(args) -> int:
    """
    docs 命令处理函数

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    return view_docs_cli(args)


def cmd_test(args) -> int:
    """
    test 命令处理函数

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    return run_tests_cli(args)


def create_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器

    Returns:
        ArgumentParser 实例
    """
    parser = argparse.ArgumentParser(
        prog="patterns",
        description="改进的 Python 设计模式学习工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细输出"
    )

    # 创建子命令
    subparsers = parser.add_subparsers(
        title="可用命令",
        dest="command",
        help="使用 'patterns <命令> --help' 查看命令帮助"
    )

    # run 命令
    parser_run = subparsers.add_parser(
        "run",
        help="运行指定设计模式的示例"
    )
    parser_run.add_argument(
        "pattern",
        help="模式ID或名称"
    )
    parser_run.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互模式"
    )
    parser_run.add_argument(
        "--timing",
        action="store_true",
        help="显示执行时间"
    )
    parser_run.set_defaults(func=cmd_run)

    # list 命令
    parser_list = subparsers.add_parser(
        "list",
        help="列出所有或指定分类的设计模式"
    )
    parser_list.add_argument(
        "category",
        nargs="?",
        help="模式分类(creational, structural, behavioral, other)"
    )
    parser_list.set_defaults(func=cmd_list)

    # docs 命令
    parser_docs = subparsers.add_parser(
        "docs",
        help="查看指定模式的文档"
    )
    parser_docs.add_argument(
        "pattern",
        help="模式ID或名称"
    )
    parser_docs.add_argument(
        "--section", "-s",
        help="仅显示特定章节"
    )
    parser_docs.set_defaults(func=cmd_docs)

    # test 命令
    parser_test = subparsers.add_parser(
        "test",
        help="运行模式示例的测试"
    )
    parser_test.add_argument(
        "pattern",
        nargs="?",
        help="模式ID(省略则运行所有测试)"
    )
    parser_test.add_argument(
        "--coverage",
        action="store_true",
        help="显示测试覆盖率"
    )
    parser_test.add_argument(
        "--failfast", "-x",
        action="store_true",
        help="首次失败后停止"
    )
    parser_test.set_defaults(func=cmd_test)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """
    CLI 主函数

    Args:
        argv: 命令行参数列表

    Returns:
        退出码
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # 如果没有指定命令,显示帮助
    if not hasattr(args, 'func'):
        parser.print_help()
        return 0

    # 执行命令
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        return 130
    except Exception as e:
        print(f"✗ 错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
