from llm.prompt.template.openai import chat


prompt = "primes from 1 to 50"
result = chat.get_completion(prompt)

style = f"""
Format everything as HTML that can be used in a website.
Place the description in a <div> element.
Collect information in <Table> if it's help to visualization.
"""
response = chat.get_stylish_completion(result, style)
print(response)
