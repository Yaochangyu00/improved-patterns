"""
配置加载器模块

负责加载和验证配置文件(categories.json, patterns.json, cli_commands.json)
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class ConfigLoader:
    """配置加载器类"""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        初始化配置加载器

        Args:
            config_dir: 配置文件目录路径,默认为项目根目录的 config/
        """
        if config_dir is None:
            # 默认配置目录:从 cli 目录向上一级,然后进入 config
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)

        self._categories: Optional[List[Dict[str, str]]] = None
        self._patterns: Optional[List[Dict[str, Any]]] = None
        self._cli_commands: Optional[List[Dict[str, Any]]] = None

    def load_categories(self) -> List[Dict[str, str]]:
        """
        加载模式分类配置

        Returns:
            分类列表
        """
        if self._categories is None:
            config_file = self.config_dir / "categories.json"
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._categories = data.get("categories", [])
        return self._categories

    def load_patterns(self) -> List[Dict[str, Any]]:
        """
        加载设计模式配置

        Returns:
            模式列表
        """
        if self._patterns is None:
            config_file = self.config_dir / "patterns.json"
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._patterns = data.get("patterns", [])
        return self._patterns

    def load_cli_commands(self) -> List[Dict[str, Any]]:
        """
        加载 CLI 命令配置

        Returns:
            命令列表
        """
        if self._cli_commands is None:
            config_file = self.config_dir / "cli_commands.json"
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cli_commands = data.get("commands", [])
        return self._cli_commands

    def get_category_by_name(self, name: str) -> Optional[Dict[str, str]]:
        """
        根据名称获取分类

        Args:
            name: 分类名称(英文或中文)

        Returns:
            分类字典,如果未找到则返回 None
        """
        categories = self.load_categories()
        for category in categories:
            if category["name"] == name or category["display_name_zh"] == name:
                return category
        return None

    def validate_config(self) -> bool:
        """
        验证配置文件的完整性

        Returns:
            验证是否成功
        """
        try:
            categories = self.load_categories()
            patterns = self.load_patterns()

            # 验证分类不为空
            if not categories:
                print("错误: categories.json 中没有定义分类")
                return False

            # 验证模式不为空
            if not patterns:
                print("错误: patterns.json 中没有定义模式")
                return False

            # 验证每个模式的 category 都存在
            valid_categories = {cat["name"] for cat in categories}
            for pattern in patterns:
                if pattern["category"] not in valid_categories:
                    print(f"错误: 模式 '{pattern['id']}' 的分类 '{pattern['category']}' 不存在")
                    return False

            return True
        except Exception as e:
            print(f"配置验证失败: {e}")
            return False


# 全局配置加载器实例
_config_loader: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """
    获取全局配置加载器实例

    Returns:
        ConfigLoader 实例
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader
