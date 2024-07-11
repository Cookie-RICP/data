#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @created by CYang on 14:43 2024/6/18 0018
# @File: score.py
# import openai
from openai import OpenAI
import httpx
import logging
import json

# openai.api_key = 'sk-qhqfahNGOAlmAnN66bC736B7D8884890A8F7234331E48b31'

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("application.log", mode='a'),
                        logging.StreamHandler()
                    ])

client = OpenAI(
    base_url="https://api.gpts.vin/v1",
    api_key="sk-qhqfahNGOAlmAnN66bC736B7D8884890A8F7234331E48b31",
    http_client=httpx.Client(
        base_url="https://api.gpts.vin/v1",
        follow_redirects=True,
    ),
)

# 定义问题和满分回答标准
questions = [
    ("解释了什么是cookie？", "完整的定义和功能解释，包括cookie是什么、它们如何工作以及它们用于存储什么类型的信息。"),
    ("说明了为什么要使用cookie？", "详细解释了cookie的主要用途和优势，包括提高用户体验、个性化服务、广告管理等。"),
    ("说明了是怎样使用cookie的？", "具体描述了cookie是如何被网站使用的，包括用途、存储的具体信息和使用方式。"),
    ("哪些描述中对cookie功能进行了分类？", "分类说明了不同类型的cookie，如按cookie的目的进行分类，或其他任何相关的分类方式。"),
    ("哪些描述说明了了cookie的用途？", "对每一类或每一个cookie的具体用途进行了详细的说明和描述。"),
    ("对cookie的有效期说明？", "详细说明了cookie的有效期，包括会话性和持久性cookie的区别，以及可能的过期机制。"),
    ("解释了第三方cookie等信息？", "清晰解释了第三方cookie如何被使用，包括第三方广告商如何访问和设置cookie，以及相关的隐私政策限制。"),
    ("说明了用户如何管理cookie？", "提供了详细的用户指南，说明如何管理、控制或删除cookie，以及管理cookie可能带来的影响。"),
    ("说明了如何保护数据的安全性？", "详细解释了cookie在数据安全性方面的措施和保护措施。"),
    ("提供了其它详情页或链接？", "提供了其他详细信息或相关链接，以便用户获取更多关于cookie的详细信息。")
]

# 提供的文本
cookie_statement = """
我们或我们的合作伙伴可能通过COOKIES或同类技术获取和使用您的信息，并将该等信息存储为日志信息。通过使用COOKES，我们向用户提供简单易行并富个性化的网络体验。一个COOKIES早少量的数据，它们从一个网络服务器送至您的湖览器并存在计算机硬盘上。我们使用COOKES是为了让其用户可以受益。比如，为使得网易虚拟社区的登录过程更快捷，您可以选择把用户名存在一个COOKIES中，这样下次当您要登录网易的服务时能更加方便快捷。COOKES能帮助我们确定您连接的!页面和内容，您在网易特定服务上花费的时间和您所选择的网易服务。 COOKIES使得我们能更好、更快地为您服务，并且使您在网易服务上的经历更富个性化。然而，您应该能够控制COOKIES是否以及怎样被您的浏览器接受。请查阅您的浏览器附带的文件以获得更多这方面的信息。 我们和第三方合作伙伴可能通过COOKIES或同类技术收集和使用您的信息，并将该等信息存储， 我们使用自己的COOKIES或同类技术，可能用于以下用途: 1、记住您的身份。例如:COOKIES或同类技术有助于我们辨认您作为我们的注册用户的身份，或保存您向我们提供有关您的喜好或其他信息 2、分析您使用我们服务的情况。我们可利用COOKIES或同类技术来了解您使用网易服务进行什么活动、或哪些服务最受欢迎;
"""

def extract_answers_from_text(text):

    answers = []
    for question, _ in questions:
        prompt = f"cookie声明：\n{text}\n \n 问题：{question}" \
                 f"\n 以上cookie声明中的哪些句子对上面的问题进行了回答？" \
                 f"\n如果没有，直接返回' '，不需要解释；如果有对应的回答，仅仅返回回答了问题的句子（如果有多处，拼接为一个字符串返回）。注意不要返回其它任何信息！"

        # response = openai.Completion.create(prompt=prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        if response.choices:
            answer = response.choices[0].message.content.strip()
            answers.append(answer)
            logging.info(question + ": " + answer)
        else:
            # 如果没有提取到答案则返回空字符串
            answers.append("")
            logging.info(question + ": null")
    return answers


def score_answer(question, answer, full_answer):
    if len(answer) < 5:
        logging.info("{score: 0.0, reason: ' '}")
        return "0"
    prompt = f"question：{question}\n answer：{answer}\n" \
             f"\n Please rate the answers to the previous questions based on the following full-score standardized responses, " \
             f'returning {{"score":x,"reason":"x"}} in json string format\nfull_answer:{full_answer}' \
             f"\n Scoring level：没有回答：0分，回答的非常简略：0.25分，回答的一般：0.5分，回答的较为详细：0.75分，回答的很详细：1分。" \
             f"只有回答的内容符合满分回答才可以得1分，离标准答案越远，分越低" \

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    if response.choices:
        result = response.choices[0].message.content
        parsed_json = json.loads(result)
        score = parsed_json['score']
        logging.info(result)
        return score
    return "0"


def score_answers(answers, scores):
    for i, (question, full_answer) in enumerate(questions):
        extracted_answer = answers[i].strip()
        score = score_answer(question, extracted_answer, full_answer)
        scores.append(score)
    return scores


with open('D:\\papercode\\cookie-classifier\\CookieBlock-Consent-Classifier-main\\cookie_statement\\data\\statement.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for domain, statement in data.items():

    logging.info(domain)
    logging.info(statement)
    extracted_answers = extract_answers_from_text(statement)

    # 评分
    scores = []
    scores_list = score_answers(extracted_answers, scores)
    logging.info(scores_list)
    logging.info("==============================================")
