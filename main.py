import requests
import argparse
import sys
import data
import dataManager

# 管理子命令及其帮助信息
MANAGEMENT_COMMANDS = {"list", "show", "add", "delete", "use", "help"}

HELP_TEXT = """HAAA - 命令行 AI 助手

用法:
  uv run main.py "你的问题"                          直接提问
  uv run main.py list                             列出所有已保存的模型
  uv run main.py show                             显示当前默认模型
  uv run main.py add --url URL --key KEY --name NAME  添加一个模型
  uv run main.py delete INDEX                     按索引删除模型
  uv run main.py use INDEX                        将指定索引的模型设为默认
  uv run main.py help                             显示本帮助"""


class HelpOnErrorParser(argparse.ArgumentParser):
    """参数解析出错时显示完整帮助，而不是默认的 usage"""

    def error(self, message):
        print(f"[ERROR] {message}")
        print()
        print(HELP_TEXT)
        sys.exit(1)


def cmd_list():
    dataManager.show_list()


def cmd_show():
    dataManager.show_default()


def cmd_add(args):
    if not args.url or not args.key or not args.name:
        print("[ERROR] add 需要提供 --url --key --name 三个参数")
        print("示例: uv run main.py add --url https://api.example.com/v1/chat/completions --key sk-xxx --name model-name")
        print("输入 `uv run main.py help` 获取完整帮助")
        sys.exit(1)
    from data import model_data
    dataManager.add_model(model_data(args.url, args.key, args.name))
    dataManager.save_list()
    print(f"[OK] 已添加模型: {args.name}")


def cmd_delete(args):
    idx = args.index
    if idx < 0 or idx >= len(dataManager.get_list()):
        print(f"[ERROR] 索引 {idx} 无效，请用 `list` 查看可用索引")
        sys.exit(1)
    removed = dataManager.get_list()[idx]
    _, _, name = removed.get_ALL()
    dataManager.delete_model(idx)
    dataManager.save_list()
    print(f"[OK] 已删除模型: {name} (index {idx})")


def cmd_use(args):
    idx = args.index
    if idx < 0 or idx >= len(dataManager.get_list()):
        print(f"[ERROR] 索引 {idx} 无效，请用 `list` 查看可用索引")
        sys.exit(1)
    dataManager.save_default(idx)
    _, _, name = dataManager.get_list()[idx].get_ALL()
    print(f"[OK] 已将默认模型切换为: {name} (index {idx})")


def cmd_help():
    print(HELP_TEXT)


def main():
    args_list = sys.argv[1:]

    # 无任何参数：显示完整帮助
    if not args_list:
        cmd_help()
        return

    first = args_list[0]

    # 以 - 开头的参数视为未知选项，显示帮助
    if first.startswith("-"):
        print(f"[ERROR] 未知选项: {first}")
        print()
        print(HELP_TEXT)
        sys.exit(1)

    # --- 管理子命令分支 ---
    if first in MANAGEMENT_COMMANDS:
        # 管理命令需要先加载模型列表
        dataManager.init_list()
        parser = HelpOnErrorParser(prog=f"main.py {first}")

        if first == "list":
            parser.parse_args(args_list[1:])
            cmd_list()
        elif first == "show":
            parser.parse_args(args_list[1:])
            cmd_show()
        elif first == "add":
            parser.add_argument("--url", type=str, default=None)
            parser.add_argument("--key", type=str, default=None)
            parser.add_argument("--name", type=str, default=None)
            args = parser.parse_args(args_list[1:])
            cmd_add(args)
        elif first == "delete":
            parser.add_argument("index", type=int)
            args = parser.parse_args(args_list[1:])
            cmd_delete(args)
        elif first == "use":
            parser.add_argument("index", type=int)
            args = parser.parse_args(args_list[1:])
            cmd_use(args)
        elif first == "help":
            parser.parse_args(args_list[1:])
            cmd_help()
        return

    # --- 提问流程 ---
    # 从未提交的默认配置文件 .default_model 读取配置
    try:
        config = dataManager.get_default()
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print()
        print("首次使用？标准用法如下：")
        print("  uv run main.py add --url <API_URL> --key <API_KEY> --name <模型名>   添加你的 AI 模型")
        print("  uv run main.py use <索引>                                          将该模型设为默认")
        print("  uv run main.py help                                                获取完整帮助")
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] {e}")
        print("输入 `uv run main.py help` 获取完整帮助")
        sys.exit(1)

    api_key = config.get_API_KEY()
    ai_prompts = data.model_data.ai_prompts
    url = config.get_API_URL()
    model = config.get_model()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    parser = HelpOnErrorParser()
    parser.add_argument("msg", type=str, help="your question")
    args = parser.parse_args(args_list)
    payload = {
        "model": f"{model}",
        "messages": [
            {"role": "system", "content": f"{ai_prompts}"},
            {"role": "user", "content": f"{args.msg}"}
        ],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 无法连接到 API: {e}")
        sys.exit(1)

    if response.status_code != 200:
        try:
            err = response.json().get("error", {})
            if isinstance(err, dict):
                message = err.get("message", response.text)
            else:
                message = response.text
        except ValueError:
            message = response.text
        print(f"[ERROR] API 请求失败 (HTTP {response.status_code}): {message}")
        print("提示：请检查 .default_model 中的 API_KEY / API_URL 是否正确。")
        sys.exit(1)

    try:
        content = response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError):
        print("[ERROR] API 返回了无法解析的响应格式。")
        print(f"原始响应: {response.text[:500]}")
        sys.exit(1)

    print(content)


if __name__ == "__main__":
    main()
