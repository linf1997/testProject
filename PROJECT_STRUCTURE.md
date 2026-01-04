# 项目结构说明

## 目录结构

```
testProject/
│
├── data/                          # 测试数据目录
│   ├── test_cases.xlsx            # Excel测试用例文件（通过脚本生成）
│   └── test_case_01.yaml          # YAML接口配置文件（示例）
│
├── config/                        # 配置文件目录（预留）
│
├── logs/                          # 日志文件目录
│   └── test_YYYYMMDD.log          # 按日期生成的日志文件
│
├── testcases/                     # 测试用例目录
│   ├── __init__.py               # Python包初始化文件
│   └── test_api.py               # 接口自动化测试用例
│
├── utils/                         # 工具类目录
│   ├── __init__.py               # Python包初始化文件
│   ├── excel_handler.py          # Excel文件处理工具
│   ├── yaml_handler.py           # YAML文件处理工具
│   ├── http_client.py            # HTTP请求封装类
│   └── logger_config.py          # 日志配置模块
│
├── scripts/                       # 脚本目录
│   └── create_excel_template.py  # 创建Excel模板脚本
│
├── reports/                       # 测试报告目录
│   ├── allure-results/           # Allure测试结果（自动生成）
│   └── allure-report/            # Allure测试报告（手动生成）
│
├── conftest.py                    # pytest配置文件（fixtures定义）
├── pytest.ini                     # pytest配置文件（运行配置）
├── requirements.txt               # Python依赖包列表
├── run_tests.py                   # 快速运行测试脚本
├── README.md                      # 项目说明文档
├── QUICK_START.md                 # 快速开始指南
└── PROJECT_STRUCTURE.md           # 本文件（项目结构说明）
```

## 核心文件说明

### 1. 测试用例管理

- **data/test_cases.xlsx**: Excel格式的测试用例文件，包含用例ID、用例名称、YAML文件路径等
- **data/*.yaml**: YAML格式的接口配置文件，包含URL、请求方法、请求参数等

### 2. 工具类模块

- **utils/excel_handler.py**: 读取Excel测试用例文件
- **utils/yaml_handler.py**: 读取YAML接口配置文件
- **utils/http_client.py**: 封装HTTP请求（GET、POST、PUT、DELETE等）
- **utils/logger_config.py**: 配置日志记录器

### 3. 测试用例

- **testcases/test_api.py**: 使用pytest.mark.parametrize实现参数化测试

### 4. 配置文件

- **conftest.py**: 定义pytest fixtures（http_client、log_test_info等）
- **pytest.ini**: pytest运行配置（测试路径、标记、日志等）

## 工作流程

1. **准备阶段**
   - 运行 `python scripts/create_excel_template.py` 创建Excel模板
   - 在Excel中填写测试用例信息
   - 创建对应的YAML配置文件

2. **执行阶段**
   - 运行 `pytest` 执行测试
   - 测试框架自动读取Excel文件
   - 根据YAML文件路径读取接口配置
   - 发送HTTP请求并验证响应

3. **报告阶段**
   - 查看控制台输出
   - 查看日志文件（logs/目录）
   - 生成Allure报告查看详细结果

## 扩展建议

- 在 `config/` 目录下添加环境配置文件（开发、测试、生产环境）
- 扩展 `utils/http_client.py` 支持更多HTTP特性（代理、重试等）
- 在 `testcases/` 目录下添加更多测试文件
- 扩展断言逻辑，支持更复杂的验证规则



