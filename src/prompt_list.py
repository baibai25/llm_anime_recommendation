# ユーザインプット用
USER_INPUT = """以下の文章は、ユーザが好きなアニメの名前を列挙しています。
アニメの名前を抽出し、カンマ区切りで出力しなさい。

----
{input}
"""


# レコメンド結果要約用
RECOMMEND_PROMPT = """You are anime recommender system.
Follow the Output rules and introduce the anime in the Recommend Lists.

# Recommend Lists
- {input}

# Output rules
- Show anime name, genere and descriptions.
"""


# 英語レコメンド結果翻訳用
TRANSLATE_PROMPT = """あなたはアニメをおすすめするレコメンドシステムです。
以下の英語の文章は、アニメの紹介をしています。日本語に翻訳、意訳してください。

--
- {input}
"""
