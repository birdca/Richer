from llm.prompt.template.openai.chat import get_completion_in_html


prompt = "primes from 1 to 100"
response = get_completion_in_html(prompt)
print(response)
