import requests
import base64
import re
import os
import random
from openai import OpenAI
import markdown2
from bs4 import BeautifulSoup
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

def work(url):
    username, repo = get_info(url)
    project = get_readme(username, repo)    
    ans = get_project_intro(project)
    return ans

if __name__ == '__main__':
    # print(get_project_intro("https://github.com/openai/openai-cookbook"))
    # print(get_project_intro("https://github.com/microsoft/mu_feature_ipmi"))
    # print(get_project_intro('https://github.com/jubalh/awesome-os'))
    # print(get_project_intro('https://github.com/08183080/be-yourself'))
    # print(get_project_intro())

    urls = [
        'https://github.com/openai/openai-cookbook',
        'https://github.com/microsoft/mu_feature_ipmi',
        'https://github.com/jubalh/awesome-os',
        'https://github.com/08183080/be-yourself',
        'https://github.com/FoundationVision/VAR'
    ]

    # username, repo = get_info(urls[random.randint(0,len(urls)-1)])
    # project = get_readme(username, repo)
    # # print(project)
    # print(get_project_intro(project))

    print(work(urls[random.randint(0,len(urls)-1)]))