import requests
import os

api_key = os.getenv("DEEPSEEK_API_KEY")

url = "https://api.deepseek.com/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

msg=input()
payload = {
    "model": "deepseek-v4-flash",
    "messages": [
        {"role": "system", "content": "你是一个命令行AI助手。回答用户问题时必须：(1) 只给出确认的事实，绝不捏造信息；(2) 用最简洁的语言直接回答，通常不超过1-2句;(3) 不使用任何格式（如Markdown、列表、代码块）；(4) 如果不知道就说“不清楚”,避免任何解释或附加内容。"},
        {"role": "user", "content": f"{msg}"}
    ],
    "thinking": {"type": "enabled"},
    "reasoning_effort": "high",
    "stream": False
}

response = requests.post(url, headers=headers, json=payload)
print(response.json()['choices'][0]['message']['content'])
