"""
接口自动化测试用例
使用pytest.mark.parametrize实现参数化测试
"""
import pytest
import os
import sys
import allure

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.excel_handler import ExcelHandler
from utils.yaml_handler import YamlHandler
from utils.logger_config import setup_logger

logger = setup_logger()


def get_test_cases_from_excel(excel_path: str = "data/test_cases.xlsx"):
    """
    从Excel文件读取测试用例
    :param excel_path: Excel文件路径
    :return: 测试用例列表
    """
    try:
        # 处理相对路径
        if not os.path.isabs(excel_path):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            excel_path = os.path.join(project_root, excel_path)
        
        excel_handler = ExcelHandler(excel_path)
        test_cases = excel_handler.read_test_cases()  # 默认使用活动工作表
        return test_cases
    except Exception as e:
        logger.error(f"读取测试用例失败: {str(e)}")
        return []


# 获取测试用例数据
test_cases_data = get_test_cases_from_excel()


@pytest.mark.parametrize("test_case", test_cases_data)
@allure.feature("接口自动化测试")
def test_api_request(test_case, http_client):
    """
    参数化测试用例
    :param test_case: 测试用例数据（从Excel读取）
    :param http_client: HTTP客户端fixture
    """
    # 获取用例信息
    case_id = test_case.get("用例ID") or test_case.get("case_id") or ""
    case_name = test_case.get("用例名称") or test_case.get("case_name") or ""
    yaml_path = test_case.get("YAML文件路径") or test_case.get("yaml_path") or ""
    is_run = test_case.get("是否执行") or test_case.get("is_run") or "Y"
    # 跳过不执行的用例
    if str(is_run).upper() != "Y":
        pytest.skip(f"用例 {case_id} 设置为不执行")
    
    if not yaml_path:
        pytest.fail(f"用例 {case_id} 未配置YAML文件路径")
    
    # 构建YAML文件的完整路径
    if not os.path.isabs(yaml_path):
        yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), yaml_path)
    
    # 添加allure报告信息
    allure.dynamic.title(f"{case_id}: {case_name}")
    allure.dynamic.description(f"测试用例ID: {case_id}\n用例名称: {case_name}\nYAML配置: {yaml_path}")
    
    try:
        # 读取YAML配置
        yaml_handler = YamlHandler(yaml_path)
        api_config = yaml_handler.get_api_config()
        
        if not api_config or "api" not in api_config:
            pytest.fail(f"YAML文件 {yaml_path} 配置格式错误")
        
        api_info = api_config["api"]
        url = api_info.get("url")
        method = api_info.get("method", "POST").upper()
        headers = api_info.get("headers", {})
        params = api_info.get("params", {})
        
        # 添加allure步骤
        with allure.step("读取接口配置"):
            allure.attach(f"URL: {url}", "接口地址", allure.attachment_type.TEXT)
            allure.attach(f"Method: {method}", "请求方法", allure.attachment_type.TEXT)
            allure.attach(str(params), "请求参数", allure.attachment_type.JSON)
        
        # 发送HTTP请求
        with allure.step("发送HTTP请求"):
            if method == "GET":
                response = http_client.get(url, headers=headers, params=params)
            elif method == "POST":
                response = http_client.post(url, headers=headers, json=params)
            elif method == "PUT":
                response = http_client.put(url, headers=headers, json=params)
            elif method == "DELETE":
                response = http_client.delete(url, headers=headers)
            else:
                response = http_client.request(method, url, headers=headers, json=params)
        
        # 记录响应信息
        with allure.step("验证响应结果"):
            allure.attach(f"状态码: {response.status_code}", "响应状态码", allure.attachment_type.TEXT)
            try:
                allure.attach(response.text, "响应内容", allure.attachment_type.JSON)
            except:
                allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
        
        # 断言
        expected = api_config.get("expected", {})
        expected_status_code = expected.get("status_code", 200)
        
        assert response.status_code == expected_status_code, \
            f"状态码断言失败: 期望 {expected_status_code}, 实际 {response.status_code}"
        
        logger.info(f"用例 {case_id} 执行成功")
        
    except FileNotFoundError as e:
        logger.error(f"用例 {case_id} 执行失败: YAML文件不存在 - {str(e)}")
        pytest.fail(f"YAML文件不存在: {str(e)}")
    except Exception as e:
        logger.error(f"用例 {case_id} 执行失败: {str(e)}")
        pytest.fail(f"测试执行失败: {str(e)}")

