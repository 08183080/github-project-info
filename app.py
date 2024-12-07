import requests
import base64
import re
import os
import random
from openai import OpenAI
import markdown2
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, scrolledtext
from dotenv import load_dotenv

load_dotenv()

def get_info(url):
    # 正则表达式解析GitHub URL
    pattern = r'https://github\.com/([^/]+)/([^/]+)'
    match = re.match(pattern, url)
    
    if not match:
        raise ValueError("Invalid GitHub URL")
    
    username, repo = match.groups()
    return username, repo

def get_readme(username, repo):
    # GitHub API的URL
    url = f'https://api.github.com/repos/{username}/{repo}/readme'

    # 需要提供GitHub API token（如果有的话）
    headers = {
        'Authorization': f"token {os.getenv('GITHUB_PAT')}"
    }

    # 发送请求
    response = requests.get(url, headers=headers)

    # 如果请求成功，返回README内容
    if response.status_code == 200:
        readme_data = response.json()
        readme_content = readme_data['content']
        # print(f"README (base64 encoded):\n{readme_content}")
    else:
        print(f"Error: {response.status_code}")

    decoded_content = base64.b64decode(readme_content).decode('utf-8')
    # print(f"Decoded README:\n{decoded_content}")
    return decoded_content
    
def get_project_intro(project):
    # client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
    client = OpenAI(api_key=os.getenv('ZHIPUAI_API_TOKEN'), base_url="https://open.bigmodel.cn/api/paas/v4/")

    # deepseek-chat
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "system", "content": "你是Github项目剖析专家，针对输入的Github项目的readme文档，\
             写篇中文文章多维度多层次多视角深入详细犀利介绍该项目的方方面面。发散思考产品如何商业化，以及产品的哲学意义"},
            {"role": "user", "content": project},
        ],
        stream=False
    )
    ans = response.choices[0].message.content
    ans = markdown2.markdown(ans, extras=["strip"])
    soup = BeautifulSoup(ans, 'html.parser')
    text = soup.get_text()
    return text
# 按钮点击事件
def analyze_project():
    github_url = entry.get()
    try:
        username, repo = get_info(github_url)
        readme_content = get_readme(username, repo)
        project_intro = get_project_intro(readme_content)
        output_text.delete(1.0, tk.END)  # 清空现有内容
        output_text.insert(tk.END, project_intro)  # 显示分析结果
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 创建 GUI 界面
root = tk.Tk()
root.title("GitHub 项目分析工具")

# 输入框
frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="输入 GitHub 项目链接：")
label.grid(row=0, column=0, padx=5)

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1, padx=5)

# 按钮
button = tk.Button(frame, text="分析项目", command=analyze_project)
button.grid(row=0, column=2, padx=5)

# 输出框
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(pady=10)

# 启动主循环
root.mainloop()
