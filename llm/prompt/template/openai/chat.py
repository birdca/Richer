from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from llm.config import OPENAI_API_KEY
from openai import OpenAI

llm_model = "gpt-4-1106-preview"
client = OpenAI(api_key=OPENAI_API_KEY)

"""
Use the OpenAI API to get a completion for a prompt for single-turn chat.
"""


def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


"""
Use langchain ChatOpenAI and ChatPromptTemplate to get a completion for a prompt for single-turn chat.
but response is not a dict, it is a ChatResponse object.
"""
chat = ChatOpenAI(temperature=0.0, model=llm_model)


def get_stylish_completion(prompt, style="Passionate and friendly"):
    template_string = """Consider the text \
    that is delimited by triple backticks \
    and respond it with a style that is {style} within 100 tokens. \
    text: ```{prompt}```
    """
    prompt_template = ChatPromptTemplate.from_template(template_string)
    messages = prompt_template.format_messages(style=style, prompt=prompt)
    response = chat(messages)
    return response.content
