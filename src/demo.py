import gradio as gr

from candidate import get_candidate_list
from recommend import get_recommend_result
from summarize_result import get_output_result


def get_text(input_text):
    rated_anime = get_candidate_list(input_text)
    recommend_result = get_recommend_result(rated_anime)
    output_result = get_output_result(recommend_result)

    output_string = ""
    for s in output_result:
        output_string += s + "\n\n"

    return output_string


demo = gr.Interface(fn=get_text, inputs="text", outputs="text")
