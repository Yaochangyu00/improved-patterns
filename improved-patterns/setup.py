"""
改进的 Python 设计模式项目安装脚本

使用 setup.py 提供向后兼容性,主要配置在 pyproject.toml
"""
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        packages=find_packages(include=["patterns", "patterns.*", "cli", "cli.*"]),
        package_data={
            "": ["*.json", "*.md"],
        },
        include_package_data=True,
    )
