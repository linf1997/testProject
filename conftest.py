"""
pytest配置文件
"""
import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger_config import setup_logger
from utils.http_client import HttpClient

# 配置日志
logger = setup_logger()


@pytest.fixture(scope="session")
def http_client():
    """
    创建HTTP客户端fixture
    :return: HttpClient实例
    """
    client = HttpClient(timeout=30)
    yield client
    client.close()


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """
    自动记录测试信息
    """
    logger.info(f"开始执行测试: {request.node.name}")
    yield
    logger.info(f"测试完成: {request.node.name}")



