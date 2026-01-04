# 接口自动化测试框架

基于 Python + Requests + Pytest + Openpyxl + YAML + Allure + Logging 构建的接口自动化测试框架。

## 项目结构

```
testProject/
├── data/                    # 测试数据目录
│   ├── test_cases.xlsx      # Excel测试用例文件
│   └── test_case_01.yaml    # YAML接口配置文件
├── config/                  # 配置文件目录
├── logs/                    # 日志文件目录
├── testcases/               # 测试用例目录
│   └── test_api.py          # 接口测试用例
├── utils/                   # 工具类目录
│   ├── __init__.py
│   ├── excel_handler.py     # Excel文件处理
│   ├── yaml_handler.py      # YAML文件处理
│   ├── http_client.py       # HTTP请求封装
│   └── logger_config.py     # 日志配置
├── reports/                 # 测试报告目录
│   └── allure-results/      # Allure测试结果
├── scripts/                 # 脚本目录
│   └── create_excel_template.py  # 创建Excel模板脚本
├── conftest.py              # pytest配置文件
├── pytest.ini               # pytest配置
├── requirements.txt         # 依赖包文件
└── README.md                # 项目说明文档
```

## 环境要求

- Python 3.7+
- pip

## 安装步骤

1. **安装依赖包**

```bash
pip install -r requirements.txt
```

2. **创建Excel测试用例模板**

```bash
python scripts/create_excel_template.py
```

3. **安装Allure（用于生成测试报告）**

Windows:
```bash
# 下载并安装 Allure
# 访问: https://github.com/allure-framework/allure2/releases
# 下载后解压，将bin目录添加到系统PATH
```

或使用choco安装:
```bash
choco install allure
```

## 使用方法

### 1. 编写测试用例

#### Excel测试用例格式

在 `data/test_cases.xlsx` 文件中维护测试用例，包含以下列：

| 用例ID | 用例名称 | YAML文件路径 | 是否执行 | 备注 |
|--------|----------|--------------|----------|------|
| TC001 | 渠道验证接口测试 | data/test_case_01.yaml | Y | 测试渠道验证接口 |

- **用例ID**: 唯一标识测试用例
- **用例名称**: 测试用例的名称
- **YAML文件路径**: 对应的YAML配置文件路径（相对于项目根目录）
- **是否执行**: Y/N，控制是否执行该用例
- **备注**: 用例说明

#### YAML配置文件格式

在 `data/` 目录下创建YAML文件，配置接口信息：

```yaml
# 接口测试用例配置
name: 渠道验证接口测试
description: 测试渠道验证接口

# 接口配置
api:
  url: http://117.72.72.134:8080/gateway/mcp/outChannel/validate?c=WI
  method: POST
  headers:
    Content-Type: application/json
  
  # 请求参数
  params:
    requestId: hebaojiaoyanma_3453946894536
    c: WI
    data:
      productId: A100000013
      # ... 更多参数

# 预期结果
expected:
  status_code: 200
```

### 2. 运行测试

#### 运行所有测试用例

```bash
pytest
```

#### 运行指定测试文件

```bash
pytest testcases/test_api.py
```

#### 运行并生成HTML报告

```bash
pytest --html=reports/report.html --self-contained-html
```

#### 运行并生成Allure报告

```bash
# 执行测试
pytest

# 生成Allure报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开Allure报告
allure open reports/allure-report
```

### 3. 查看测试日志

测试日志会保存在 `logs/` 目录下，按日期命名，例如：`test_20231228.log`

## 框架特性

- ✅ **Excel管理用例**: 使用Excel表格维护测试用例，便于非技术人员管理
- ✅ **YAML配置接口**: 使用YAML文件配置接口信息，清晰直观
- ✅ **参数化测试**: 使用pytest.mark.parametrize实现参数化，支持批量执行
- ✅ **HTTP请求封装**: 封装Requests库，统一管理HTTP请求
- ✅ **日志记录**: 完善的日志记录功能，便于问题排查
- ✅ **Allure报告**: 集成Allure，生成美观的测试报告
- ✅ **灵活扩展**: 模块化设计，易于扩展和维护

## 核心模块说明

### ExcelHandler (utils/excel_handler.py)
- 读取Excel测试用例文件
- 支持按用例ID查询

### YamlHandler (utils/yaml_handler.py)
- 读取YAML配置文件
- 解析接口配置信息

### HttpClient (utils/http_client.py)
- 封装HTTP请求方法（GET、POST、PUT、DELETE等）
- 统一异常处理和日志记录

### LoggerConfig (utils/logger_config.py)
- 配置日志记录器
- 支持控制台和文件双重输出

## 扩展指南

### 添加新的断言规则

在 `testcases/test_api.py` 中的 `test_api_request` 函数中，可以扩展断言逻辑：

```python
# 示例：添加响应内容断言
expected_result = expected.get("result")
if expected_result:
    actual_result = response.json()
    assert actual_result.get("code") == expected_result.get("code")
```

### 添加请求前置处理

可以在 `conftest.py` 中添加fixture，实现登录、获取token等前置操作：

```python
@pytest.fixture(scope="session")
def auth_token():
    # 获取token的逻辑
    return token
```

## 注意事项

1. Excel文件路径需正确配置在测试用例中
2. YAML文件路径可以是相对路径（相对于项目根目录）或绝对路径
3. 确保测试环境网络可达
4. 日志文件会按天生成，注意定期清理

## 常见问题

### Q: 如何跳过某些测试用例？
A: 在Excel中将"是否执行"列设置为"N"

### Q: 如何添加请求头？
A: 在YAML文件的 `api.headers` 中配置

### Q: 如何查看详细的请求和响应信息？
A: 查看 `logs/` 目录下的日志文件

## 作者

接口自动化测试框架

## 许可证

MIT License



