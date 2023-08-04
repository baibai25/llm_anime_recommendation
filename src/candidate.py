import json
import re

import numpy as np
import openai
from langchain import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from prompt_list import USER_INPUT


def get_prompt(template, input_text):
    prompt = PromptTemplate(template=template, input_variables=["input"])
    prompt_text = prompt.format(input=input_text)

    return prompt_text


def get_anime_name(anime_name):
    anime_list = anime_name.split("\n")
    anime_list = [anime for anime in anime_list if anime]

    return anime_list


def get_similarity_item(db, input):
    input = input.lower()
    sim = db.similarity_search_with_score(query=input, k=1)
    anime_name = sim[0][0].page_content.split("\n")[0]
    match = re.search(r"Name: (.*)", anime_name)

    if match:
        anime_name = match.group(1)
    else:
        anime_name = np.nan

    sim_value = sim[0][1]
    if sim_value >= 0.3:
        return None
    else:
        return anime_name


def get_candidate_list(user_input):
    embeddings = OpenAIEmbeddings()
    anime_name_db = FAISS.load_local("../data/anime_name_db", embeddings)

    template_user_input = USER_INPUT

    prompt = get_prompt(template_user_input, user_input)

    functions = [
        {
            "name": "get_anime_name_list",
            "description": "入力文章から、アニメ名のリストを作成する。",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "array",
                        "description": "アニメ名",
                        "items": {"type": "string"},
                    }
                },
                "required": ["name"],
            },
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ],
        functions=functions,
        function_call="auto",
        temperature=0,
    )
    message = response["choices"][0]["message"]
    candidate_list = json.loads(message["function_call"]["arguments"])["name"]

    rated_anime = []
    for item in candidate_list:
        rated_anime.append(get_similarity_item(anime_name_db, item))

    return rated_anime
