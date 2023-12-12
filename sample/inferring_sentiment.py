from llm.prompt.template.openai.chat import get_completion

description = "It's sunny today."
prompt = f"""
What is the sentiment of the following description.
Give the answer as a single word, either "positive" \
or "negative".

Review text: '''{description}'''
"""
response = get_completion(prompt)
print(response)
