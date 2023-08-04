from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from prompt_list import RECOMMEND_PROMPT, TRANSLATE_PROMPT


def get_prompt(template, input_text):
    prompt = PromptTemplate(template=template, input_variables=["input"])
    prompt_text = prompt.format(input=input_text)

    return prompt_text


def get_output_result(recommend_result):
    embeddings = OpenAIEmbeddings()
    anime_info_db = FAISS.load_local("../data/anime_info_db", embeddings)
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    chain = RetrievalQA.from_chain_type(
        llm,
        retriever=anime_info_db.as_retriever(),
    )

    # English prompt
    template_recommend = RECOMMEND_PROMPT

    # Get English ver LLM result
    # データセットが英語のため初めに英語で結果を出力させる
    result_list = []
    for l in recommend_result["Name"][0:3]:
        input = l.lower()
        prompt = get_prompt(template_recommend, input)
        result = chain(prompt)
        result_list.append(result["result"])

    # Japanese prompt
    template_translate = TRANSLATE_PROMPT

    # 英語の出力結果を日本語に変換
    result_translate = []
    for l in result_list:
        prompt = get_prompt(template_translate, l)
        result = chain(prompt)
        result_translate.append(result["result"])

    return result_translate
