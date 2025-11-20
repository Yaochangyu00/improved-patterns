"""
文档查看器模块

负责加载和显示设计模式文档
"""
from pathlib import Path
from typing import Optional

from cli.pattern_index import get_pattern_index


class DocumentationViewer:
    """文档查看器类"""

    def __init__(self):
        """初始化文档查看器"""
        self.pattern_index = get_pattern_index()

    def view_docs(
        self,
        pattern_name: str,
        section: Optional[str] = None,
        verbose: bool = False
    ) -> bool:
        """
        查看指定模式的文档

        Args:
            pattern_name: 模式名称(ID或中文/英文名称)
            section: 仅显示特定章节
            verbose: 是否显示详细输出

        Returns:
            查看是否成功
        """
        # 查找模式
        pattern = self.pattern_index.find_pattern_by_name(pattern_name)

        if pattern is None:
            print(f"✗ 错误: 未找到模式 '{pattern_name}'")
            print("\n建议:")
            print("  • 使用 'patterns list' 查看所有可用模式")
            print("  • 检查拼写是否正确")
            return False

        # 获取文档路径
        doc_path = self.pattern_index.get_pattern_path(pattern["id"], "doc")

        if doc_path is None or not doc_path.exists():
            print(f"✗ 错误: 文档文件不存在")
            if verbose:
                print(f"[DEBUG] 期望路径: {doc_path}")
            return False

        try:
            # 读取文档内容
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if section:
                # 只显示特定章节
                content = self._extract_section(content, section)
                if not content:
                    print(f"✗ 错误: 未找到章节 '{section}'")
                    return False

            # 显示文档
            print("━" * 60)
            print(f"{pattern['name_zh']} ({pattern['name_en']})")
            print("━" * 60)
            print()
            print(content)
            print()
            print("━" * 60)

            return True

        except Exception as e:
            print(f"✗ 错误: 无法读取文档 - {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            return False

    def _extract_section(self, content: str, section_name: str) -> str:
        """
        从文档中提取特定章节

        Args:
            content: 完整文档内容
            section_name: 章节名称

        Returns:
            章节内容,如果未找到返回空字符串
        """
        lines = content.split('\n')
        section_content = []
        in_section = False
        section_level = None

        section_mappings = {
            "intent": ["意图", "## 意图"],
            "use_cases": ["适用场景", "## 适用场景"],
            "pros_cons": ["优点", "缺点", "## 优点", "## 缺点"],
            "examples": ["示例", "Python 实现", "## Python 实现"],
            "best_practices": ["最佳实践", "## 最佳实践"],
        }

        target_headers = section_mappings.get(section_name, [section_name])

        for line in lines:
            # 检查是否是目标章节的开始
            if any(header in line for header in target_headers):
                if line.startswith('#'):
                    in_section = True
                    section_level = len(line) - len(line.lstrip('#'))
                    section_content.append(line)
                    continue

            # 如果在章节中
            if in_section:
                # 检查是否遇到同级或更高级的标题(章节结束)
                if line.startswith('#'):
                    current_level = len(line) - len(line.lstrip('#'))
                    if current_level <= section_level:
                        break

                section_content.append(line)

        return '\n'.join(section_content)


def view_docs_cli(args) -> int:
    """
    CLI 入口函数

    Args:
        args: 命令行参数

    Returns:
        退出码(0 表示成功, 非0 表示失败)
    """
    viewer = DocumentationViewer()

    success = viewer.view_docs(
        pattern_name=args.pattern,
        section=getattr(args, 'section', None),
        verbose=getattr(args, 'verbose', False)
    )

    return 0 if success else 1
