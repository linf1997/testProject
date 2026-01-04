# 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 创建Excel测试用例模板（如果还没有）

```bash
python scripts/create_excel_template.py
```

## 3. 编辑Excel测试用例

打开 `data/test_cases.xlsx`，按照以下格式填写测试用例：

| 用例ID | 用例名称 | YAML文件路径 | 是否执行 | 备注 |
|--------|----------|--------------|----------|------|
| TC001 | 渠道验证接口测试 | data/test_case_01.yaml | Y | 测试渠道验证接口 |

## 4. 编辑YAML配置文件

在 `data/test_case_01.yaml` 中配置接口信息（已包含示例配置）

## 5. 运行测试

### 方式1：使用pytest直接运行

```bash
pytest
```

### 方式2：使用快速运行脚本

```bash
python run_tests.py
```

### 方式3：生成Allure报告

```bash
# 执行测试（会自动生成allure结果）
pytest

# 生成Allure报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开Allure报告（会自动打开浏览器）
allure open reports/allure-report
```

## 6. 查看测试结果

- **控制台输出**: 测试执行时会在控制台显示结果
- **日志文件**: `logs/test_YYYYMMDD.log`
- **Allure报告**: `reports/allure-report/index.html`
- **HTML报告**: 使用 `pytest --html=reports/report.html` 生成

## 注意事项

1. 确保Excel文件中的YAML文件路径正确
2. YAML文件路径可以是相对路径（相对于项目根目录）
3. 确保测试环境网络可达
4. 如果接口需要认证，可以在YAML文件的headers中配置token等信息



