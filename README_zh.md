**[English](README.md) | [中文](README_zh.md)**

# HAAA: 问问 AI 如何？

一个基于 Python 和 [uv](https://docs.astral.sh/uv/) 构建的小型命令行 AI 助手工具。

直接在终端中提问。由 OpenAI 兼容 API 驱动。

## 特性

- 用一条命令提问：`haaa "你的问题"`
- 管理多个模型配置（API URL / API KEY / 模型名）
- 轻松设置默认模型并随时切换
- 针对简洁、诚实的 CLI 回答优化的系统提示词
- 使用非流式请求，并启用思考（thinking）与高推理强度（reasoning effort）

## 使用方法

```bash
# 提问
uv run main.py "今天天气怎么样？"
```

> **第一次使用 HAAA？** 运行 `uv run main.py`（不带参数）或 `uv run main.py help` 查看完整用法。你需要先添加你的第一个模型：
>
> ```bash
> uv run main.py add --url <API_URL> --key <API_KEY> --name <模型名>
> uv run main.py use 0
> ```
>
> 之后就可以开始提问了。未知选项或缺少参数时也会显示帮助页面。

## 模型管理

直接在命令行管理你的 AI 模型配置（任何 OpenAI 兼容 API）：

```bash
# 列出所有已保存的模型
uv run main.py list

# 显示当前默认模型
uv run main.py show

# 添加一个模型（URL / API KEY / 模型名）
uv run main.py add --url https://api.example.com/v1/chat/completions --key sk-xxxx --name 模型名

# 按索引删除模型（索引见 `list` 输出）
uv run main.py delete 0

# 将指定索引的模型设为默认
uv run main.py use 0

# 显示帮助
uv run main.py help
```

> 第一个参数 `list` / `show` / `add` / `delete` / `use` / `help` 会触发管理模式；其他文本则视为要提问的问题。

## 配置

### 模型列表（`.models`）

每个模型占 3 行：`API_URL`、`API_KEY`、`model_name`。

```
https://api.example.com/v1/chat/completions
sk-xxxx
模型名
```

### 默认模型（`.default_model`）

存放当前选中的模型，同样为 3 行格式：
`API_URL`、`API_KEY`、`model_name`。

## 项目结构

```
├── main.py          # CLI 入口：管理命令 + 发送问题到 API
├── data.py          # model_data 类：API URL / KEY / 模型 + 系统提示词
├── dataManager.py   # 模型列表管理（.models / .default_model）
└── pyproject.toml   # 项目元数据与依赖
```

## 待办

- [ ] 模型列表与翻译
- [ ] 提问模型与翻译模型
- [ ] 带参数提问
- [ ] token 明细按钮
- [ ] 设置 token 使用上限

---

这是我的第一个个人 Python 项目。
欢迎 star、fork、PR！
