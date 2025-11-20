"""
模式索引模块

提供快速查找和访问设计模式的功能
"""
from typing import Dict, List, Optional, Any
from pathlib import Path
from cli.config_loader import get_config_loader


class PatternIndex:
    """模式索引类"""

    def __init__(self):
        """初始化模式索引"""
        self.config_loader = get_config_loader()
        self._index: Optional[Dict[str, Dict[str, Any]]] = None
        self._name_index: Optional[Dict[str, str]] = None

    def build_index(self) -> None:
        """构建模式索引"""
        if self._index is not None:
            return

        patterns = self.config_loader.load_patterns()
        self._index = {}
        self._name_index = {}

        for pattern in patterns:
            pattern_id = pattern["id"]
            self._index[pattern_id] = pattern

            # 同时索引中文名称(不区分大小写)
            name_zh = pattern["name_zh"].lower()
            self._name_index[name_zh] = pattern_id

            # 索引英文名称(不区分大小写)
            name_en = pattern["name_en"].lower()
            self._name_index[name_en] = pattern_id

    def get_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取模式

        Args:
            pattern_id: 模式 ID

        Returns:
            模式字典,如果未找到则返回 None
        """
        self.build_index()
        return self._index.get(pattern_id)

    def find_pattern_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据名称(中文或英文)查找模式

        Args:
            name: 模式名称(支持中文或英文,不区分大小写)

        Returns:
            模式字典,如果未找到则返回 None
        """
        self.build_index()

        # 首先尝试作为 ID 查找
        pattern = self.get_pattern(name.lower())
        if pattern:
            return pattern

        # 然后尝试通过名称索引查找
        pattern_id = self._name_index.get(name.lower())
        if pattern_id:
            return self._index.get(pattern_id)

        return None

    def get_patterns_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        根据分类获取模式列表

        Args:
            category: 分类名称

        Returns:
            模式列表
        """
        self.build_index()

        # 如果是中文分类名,转换为英文
        cat_obj = self.config_loader.get_category_by_name(category)
        if cat_obj:
            category = cat_obj["name"]

        return [p for p in self._index.values() if p["category"] == category]

    def get_all_patterns(self) -> List[Dict[str, Any]]:
        """
        获取所有模式

        Returns:
            所有模式的列表
        """
        self.build_index()
        return list(self._index.values())

    def search_patterns(self, keyword: str) -> List[Dict[str, Any]]:
        """
        搜索包含关键词的模式

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的模式列表
        """
        self.build_index()
        keyword_lower = keyword.lower()
        results = []

        for pattern in self._index.values():
            # 在 ID、名称、描述和关键词中搜索
            if (keyword_lower in pattern["id"].lower() or
                keyword_lower in pattern["name_en"].lower() or
                keyword_lower in pattern["name_zh"].lower() or
                keyword_lower in pattern["description_zh"].lower() or
                any(keyword_lower in kw.lower() for kw in pattern.get("keywords_zh", []))):
                results.append(pattern)

        return results

    def get_pattern_path(self, pattern_id: str, path_type: str) -> Optional[Path]:
        """
        获取模式文件的完整路径

        Args:
            pattern_id: 模式 ID
            path_type: 路径类型 ('code', 'doc', 'test')

        Returns:
            文件的完整路径,如果未找到则返回 None
        """
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            return None

        # 获取项目根目录(从 cli 目录向上一级)
        project_root = Path(__file__).parent.parent

        path_key = f"{path_type}_path"
        if path_key not in pattern:
            return None

        return project_root / pattern[path_key]


# 全局模式索引实例
_pattern_index: Optional[PatternIndex] = None


def get_pattern_index() -> PatternIndex:
    """
    获取全局模式索引实例

    Returns:
        PatternIndex 实例
    """
    global _pattern_index
    if _pattern_index is None:
        _pattern_index = PatternIndex()
    return _pattern_index
