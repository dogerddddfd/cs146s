# Action Item Extractor

## 项目概述

Action Item Extractor 是一个基于 FastAPI 和 SQLite 构建的应用程序，用于从自由格式的笔记中提取行动项（Action Items）。该应用提供了两种提取方法：

- **启发式方法**：基于规则的模式匹配，快速高效
- **LLM 方法**：使用大型语言模型进行自然语言处理，提供更智能的提取

应用还支持将原始笔记保存到数据库，并提供行动项管理功能。

## 项目结构

```
week2/
├── app/                  # 主应用目录
│   ├── __init__.py      # Python 包初始化文件
│   ├── main.py          # FastAPI 应用入口
│   ├── db.py            # 数据库连接和操作
│   ├── models.py        # Pydantic 数据模型
│   ├── exceptions.py    # 自定义异常
│   ├── routers/         # API 路由
│   │   ├── __init__.py
│   │   ├── action_items.py  # 行动项相关路由
│   │   └── notes.py         # 笔记相关路由
│   └── services/        # 业务逻辑层
│       ├── __init__.py
│       ├── extract.py       # 行动项提取服务
│       ├── action_item_service.py  # 行动项业务逻辑
│       └── note_service.py         # 笔记业务逻辑
├── data/                # 数据目录
│   └── app.db           # SQLite 数据库文件
├── frontend/            # 前端界面
│   └── index.html       # 主页面
├── tests/               # 测试目录
│   ├── __init__.py
│   └── test_extract.py  # 提取功能测试
├── assignment.md        # 任务说明
├── writeup.md           # 任务报告
└── README.md            # 项目文档
```

## 设置和运行项目

### 环境要求

- Python 3.10 或更高版本
- Poetry（用于依赖管理）
- conda（可选，用于虚拟环境管理）
- Ollama（可选，用于 LLM 功能）

### 安装步骤

1. **激活 conda 环境（可选）**

```bash
conda activate cs146s
```

2. **安装依赖**

```bash
cd /path/to/week2
poetry install
```

3. **启动应用**

```bash
poetry run uvicorn week2.app.main:app --reload
```

4. **访问应用**

打开浏览器，导航到：http://127.0.0.1:8000/

## API 端点和功能

### 行动项相关

#### 1. 提取行动项

- **URL**: `/action-items/extract`
- **方法**: POST
- **参数**:
  - `text`: string (必填) - 要提取行动项的文本内容
  - `save_note`: boolean (可选) - 是否将原始文本保存为笔记
  - `method`: string (可选) - 提取方法 (`heuristic` 或 `llm`，默认为 `llm`)
- **响应**: 包含提取的行动项列表和可选的笔记 ID

#### 2. 获取所有行动项

- **URL**: `/action-items`
- **方法**: GET
- **参数**:
  - `note_id`: integer (可选) - 筛选特定笔记的行动项
- **响应**: 行动项列表

#### 3. 标记行动项完成状态

- **URL**: `/action-items/{action_item_id}/done`
- **方法**: POST
- **参数**:
  - `done`: boolean (可选) - 完成状态，默认为 `true`
- **响应**: 更新后的行动项信息

### 笔记相关

#### 1. 创建笔记

- **URL**: `/notes`
- **方法**: POST
- **参数**:
  - `content`: string (必填) - 笔记内容
- **响应**: 创建的笔记信息

#### 2. 获取所有笔记

- **URL**: `/notes`
- **方法**: GET
- **响应**: 所有笔记的列表

#### 3. 获取特定笔记

- **URL**: `/notes/{note_id}`
- **方法**: GET
- **响应**: 特定笔记的信息

## 前端功能

前端提供了一个简洁的用户界面，支持以下功能：

1. **文本输入**：输入要提取行动项的自由格式笔记
2. **提取选项**：
   - 保存为笔记（复选框）
   - Extract 按钮：使用启发式方法提取行动项
   - Extract LLM 按钮：使用 LLM 方法提取行动项
3. **List Notes 按钮**：查看所有保存的笔记

## 运行测试套件

项目包含了测试文件，用于验证行动项提取功能。

### 运行测试

```bash
cd /path/to/week2
poetry run pytest tests/
```

### 测试内容

测试套件主要验证 `extract_action_items_llm()` 函数的功能，包括：
- 从项目符号列表中提取行动项
- 从关键字前缀的行中提取行动项
- 处理空输入

## 技术栈

- **后端框架**: FastAPI
- **数据库**: SQLite
- **ORM**: 原生 SQLite 连接
- **数据验证**: Pydantic
- **依赖管理**: Poetry
- **前端**: HTML5 + JavaScript
- **LLM 集成**: Ollama

## 许可证

本项目仅供教育目的使用。
