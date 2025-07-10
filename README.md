# Excel处理自动化工作台

一个专为HR部门设计的Excel数据自动拆分与合并工具，支持格式保留、字段筛选、排序等功能。

## 功能特性

- ✅ **智能拆分**: 按字段值将大表拆分为多个小表
- ✅ **智能合并**: 将多个小表合并为一个大表
- ✅ **格式保留**: 完整保留单元格格式（字体、背景色、边框等）
- ✅ **配置化**: 支持JSON/YAML配置文件自定义处理参数
- ✅ **多sheet支持**: 支持处理多个工作表
- ✅ **字段筛选**: 可指定保留的字段列表
- ✅ **智能排序**: 支持多字段排序
- ✅ **批量处理**: 支持批量文件处理
- ✅ **日志记录**: 详细的操作日志和错误提示

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 创建配置文件

```bash
python 花名册智能处理工具.py --create-config
```

这将创建 `config.json` 和 `config.yaml` 示例配置文件。

### 2. 拆分Excel文件

```bash
python 花名册智能处理工具.py --mode split --config config.json --input 员工花名册.xlsx
```

### 3. 合并Excel文件

```bash
python 花名册智能处理工具.py --mode merge --config config.json --input "部门-销售.xlsx,部门-技术.xlsx,部门-人事.xlsx" --output 合并后花名册.xlsx
```

## 配置文件说明

### JSON格式 (config.json)

```json
{
  "split_field": "部门",
  "keep_fields": ["姓名", "部门", "职位", "入职日期", "薪资"],
  "sort_fields": ["部门", "姓名"],
  "output_dir": "output",
  "sheet_name": "Sheet1",
  "preserve_format": true
}
```

### YAML格式 (config.yaml)

```yaml
split_field: 部门
keep_fields:
  - 姓名
  - 部门
  - 职位
  - 入职日期
  - 薪资
sort_fields:
  - 部门
  - 姓名
output_dir: output
sheet_name: Sheet1
preserve_format: true
```

### 配置参数说明

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `split_field` | string | 拆分字段名（拆分模式必需） | "" |
| `keep_fields` | list | 保留字段列表，空列表表示保留所有字段 | [] |
| `sort_fields` | list | 排序字段列表，按顺序排序 | [] |
| `output_dir` | string | 输出目录路径 | "output" |
| `sheet_name` | string | 工作表名称 | "Sheet1" |
| `preserve_format` | boolean | 是否保留单元格格式 | true |

## 使用示例

### 示例1: 按部门拆分员工花名册

**输入文件**: `员工花名册.xlsx`
```
姓名    部门    职位    入职日期    薪资
张三    销售    经理    2023-01-01  8000
李四    技术    工程师  2023-02-01  12000
王五    销售    专员    2023-03-01  6000
赵六    技术    主管    2023-04-01  15000
```

**配置文件**: `config.json`
```json
{
  "split_field": "部门",
  "keep_fields": ["姓名", "部门", "职位", "入职日期", "薪资"],
  "sort_fields": ["姓名"],
  "output_dir": "output"
}
```

**执行命令**:
```bash
python 花名册智能处理工具.py --mode split --config config.json --input 员工花名册.xlsx
```

**输出结果**:
- `output/部门-销售.xlsx` (包含张三、王五)
- `output/部门-技术.xlsx` (包含李四、赵六)

### 示例2: 合并多个部门花名册

**输入文件**: 
- `部门-销售.xlsx`
- `部门-技术.xlsx`
- `部门-人事.xlsx`

**配置文件**: `config.json`
```json
{
  "keep_fields": ["姓名", "部门", "职位", "入职日期", "薪资"],
  "sort_fields": ["部门", "姓名"],
  "output_dir": "output"
}
```

**执行命令**:
```bash
python 花名册智能处理工具.py --mode merge --config config.json --input "部门-销售.xlsx,部门-技术.xlsx,部门-人事.xlsx" --output 合并花名册.xlsx
```

## 高级功能

### 多工作表处理

如果Excel文件包含多个工作表，可以通过配置文件指定要处理的工作表：

```json
{
  "sheet_name": "员工信息",
  "split_field": "部门"
}
```

### 字段筛选

只保留需要的字段，减少文件大小：

```json
{
  "keep_fields": ["姓名", "部门", "职位", "薪资"],
  "split_field": "部门"
}
```

### 智能排序

按多个字段进行排序：

```json
{
  "sort_fields": ["部门", "职位", "姓名"],
  "split_field": "部门"
}
```

### 格式保留控制

如果不需要保留格式（提高处理速度）：

```json
{
  "preserve_format": false,
  "split_field": "部门"
}
```

## 错误处理

工具提供详细的错误信息和日志记录：

- 所有操作日志保存在 `excel_processor.log` 文件中
- 控制台实时显示处理进度
- 详细的错误提示和解决建议

### 常见错误及解决方案

1. **拆分字段不存在**
   ```
   错误: 拆分字段 '部门' 不存在于数据中
   解决: 检查配置文件中的 split_field 是否与Excel表头一致
   ```

2. **文件读取失败**
   ```
   错误: 读取文件失败 xxx.xlsx
   解决: 检查文件路径是否正确，文件是否被其他程序占用
   ```

3. **配置文件格式错误**
   ```
   错误: 不支持的配置文件格式
   解决: 确保配置文件为JSON(.json)或YAML(.yml/.yaml)格式
   ```

## 性能优化建议

1. **大文件处理**: 对于超过10万行的文件，建议先按其他字段预筛选
2. **格式保留**: 如果不需要保留格式，设置 `preserve_format: false` 可显著提高速度
3. **内存优化**: 处理超大文件时，可考虑分批处理

## 技术支持

- 支持Excel格式: `.xlsx`, `.xls`
- Python版本要求: 3.7+
- 操作系统: Windows, macOS, Linux

## 更新日志

### v1.0
- 初始版本发布
- 支持Excel拆分和合并
- 支持格式保留
- 支持配置文件
- 支持命令行接口 
