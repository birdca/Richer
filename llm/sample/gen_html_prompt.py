from llm.prompt.template.openai import chat


prompt = "List 1 to 10 and tell me if it's prime."
style = f"""
Format everything as HTML that can be used in a website.
Place the description in a <div> element.
Collect information in <Table> if it's help to visualization.
"""
response = chat.get_stylish_completion(prompt, style)
print(response)
