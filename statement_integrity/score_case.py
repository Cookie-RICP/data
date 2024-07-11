#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @created by CYang on 9:31 2024/6/17 0017
# @File: partition.py
from http import HTTPStatus

import openai
import dashscope

# 设置OpenAI API密钥
openai.api_key = 'your-api-key'  # 替换为你的API密钥

# 示例cookie声明
cookie_statement = """
我们如何使用 Cookie 和同类技术Cookie 是指一种技术，Cookie 通常包含标识符、站点名称以及一些号码和字符。Cookie
主要的功能是便于用户使用网络平台产品和服务，以及帮助网络平台统计独立访客数量等。为确保网络平台正常运转，我们会
在您的计算机或移动设备上存储名为 Cookie 的小数据文件。当用户访问设有 Cookie 装置的本网络平台时，本网络平台之服
务器会自动发送Cookie至用户浏览器并储存到本地设备内，此Cookie负责记录日后用户到访本网络平台的种种活动、浏览习惯
。Cookie主要的功能是便于您使用网络平台产品和服务，以及帮助网络平台统计独立访客数量等。运用Cookies技术，本网络
平台向用户提供感兴趣的信息资料或储存密码，以便用户造访本网络平台时不必每次重复输入密码;运用Cookie技术，我们还
能够为您提供更加周到的个性化服务，并允许您设定您特定的服务选项。我们不会将 Cookie用于本政策所述目的之外的任何
用途。您可根据自己的偏好管理或删除 Cookie。您可以清除计算机上保存的所有 Cookie，大部分网络浏览器都设有阻止 
Cookie 的功能。但如果您这么做，则需要在每一次访问我们的网络平台时亲自更改用户设置，但您可能因为该等修改，无法
登录或使用依赖于Cookie的太保提供的服务或功能。您可以通过更改您的浏览器设置限制太保集团网络平台对Cookie的使用，
相关详情，请参见:http://www.aboutcookies.org
"""

# 评分标准
criteria = [
    "解释了什么是cookie？",
    "说明了为什么要使用cookie？",
    "说明了是怎样使用cookie的？",
    "是否分类了cookie？",
    "是否明确了cookie的用途？",
    "对cookie的有效期说明？",
    "第三方信息的解释？",
    "说明了用户如何修改cookie设置？",
    "说明了用户如何禁用cookie？",
    "数据安全性解释？"
]

# 满分回答标准


# 提取内容函数
def extract_content(statement, criterion):
    prompt = f"从以下cookie声明中提取出回答了'{criterion}'问题的内容，\ncookie声明：{statement}\n"
    dashscope.api_key = "sk-251a24a9100042c1a7d2f13ebf1eaff3"
    # 调用模型
    rsp = dashscope.Generation.call(model='baichuan2-13b-chat-v1', prompt=prompt)
    if rsp.status_code == HTTPStatus.OK:
        # 返回模型生成的文本
        print(rsp.output)
        return rsp.output
    else:
        # 返回请求失败的信息
        return 'Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message)
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=150,
    #     n=1,
    #     stop=None,
    #     temperature=0.7
    # )
    # return response.choices[0].text.strip()


# 评估内容函数
def evaluate_content(content, criterion):
    prompt = f"请根据以下评分标准对问题的回答进行评分：\n评分标准：没有回答：0分，\n回答的非常简略：0.25分，\n回答的一般：0.5分，\n回答的较为详细：0.75分，\n回答的很详细：1分\n问题：'{criterion}'\n回答：{content}\n得分（0到1）："
    rsp = dashscope.Generation.call(model='baichuan2-13b-chat-v1', prompt=prompt)
    if rsp.status_code == HTTPStatus.OK:
        # 返回模型生成的文本
        print(rsp.output)
        print("\n")
        return rsp.output
    else:
        # 返回请求失败的信息
        return 'Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message)
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=5,
    #     n=1,
    #     stop=None,
    #     temperature=0
    # )
    # score_text = response.choices[0].text.strip()
    # try:
    #     return float(score_text)
    # except ValueError:
    #     return 0.0  # 如果解析失败，默认给0分


# 评估示例cookie声明
def evaluate_statement(statement, criteria):
    scores = {}
    for criterion in criteria:
        content = extract_content(statement, criterion)
        score = evaluate_content(content, criterion)
        scores[criterion] = score
    return scores


# 执行评估
scores = evaluate_statement(cookie_statement, criteria)

# 打印每个规则上的得分结果
for criterion, score in scores.items():
    print(f"{criterion}: {score}")
