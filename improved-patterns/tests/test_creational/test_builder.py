"""
建造者模式测试
"""
import pytest


def test_builder_creates_computer():
    """测试建造者创建计算机"""
    from patterns.creational.builder import OfficeComputerBuilder

    builder = OfficeComputerBuilder()
    computer = (builder
                .build_cpu()
                .build_ram()
                .build_storage()
                .get_computer())

    assert computer.cpu != ""
    assert computer.ram != ""
    assert computer.storage != ""


def test_builder_chain_returns_self():
    """测试建造者链式调用返回自身"""
    from patterns.creational.builder import GamingComputerBuilder

    builder = GamingComputerBuilder()

    result1 = builder.build_cpu()
    result2 = result1.build_ram()
    result3 = result2.build_storage()

    assert result1 is builder
    assert result2 is builder
    assert result3 is builder


def test_different_builders_create_different_configs():
    """测试不同建造者创建不同配置"""
    from patterns.creational.builder import OfficeComputerBuilder, GamingComputerBuilder

    office_computer = (OfficeComputerBuilder()
                      .build_cpu()
                      .build_ram()
                      .get_computer())

    gaming_computer = (GamingComputerBuilder()
                      .build_cpu()
                      .build_ram()
                      .get_computer())

    assert office_computer.cpu != gaming_computer.cpu
    assert office_computer.ram != gaming_computer.ram


def test_director_constructs_computer():
    """测试指挥者构建计算机"""
    from patterns.creational.builder import (
        ServerBuilder, ComputerDirector
    )

    builder = ServerBuilder()
    director = ComputerDirector(builder)

    minimal = director.construct_minimal_computer()
    assert minimal.cpu != ""
    assert minimal.ram != ""
    assert minimal.storage != ""

    full = director.construct_full_computer()
    assert full.os != ""


def test_optional_components():
    """测试可选组件"""
    from patterns.creational.builder import GamingComputerBuilder

    computer = (GamingComputerBuilder()
                .build_cpu()
                .build_ram()
                .build_storage()
                .build_gpu()
                .get_computer())

    assert computer.gpu != ""


def test_main_function():
    """测试 main 函数正常运行"""
    from patterns.creational.builder import main

    try:
        main()
    except Exception as e:
        pytest.fail(f"main 函数执行失败: {e}")
