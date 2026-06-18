import requests
import os
import argparse
import data

#api_key = os.getenv("DEEPSEEK_API_KEY")
api_key=data.get_API_KEY()
#url = "https://api.deepseek.com/chat/completions"
ai_prompts=data.aiprompts
url=data.get_API_URL()
model=data.get_model()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# msg=input()
parser=argparse.ArgumentParser()
parser.add_argument("msg",type=str,help="your question")
args=parser.parse_args()
payload = {
    "model": f"model",
    "messages": [
        {"role": "system", "content": f"{ai_prompts}"},
        {"role": "user", "content": f"{args.msg}"}
    ],
    "thinking": {"type": "enabled"},
    "reasoning_effort": "high",
    "stream": False
}

response = requests.post(url, headers=headers, json=payload)
print(response.json()['choices'][0]['message']['content'])
