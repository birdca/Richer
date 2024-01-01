from llm.prompt.template.openai import chat

# There are 4 types of Chain:
# 1. LLMChain
prompt = "Give me 5 best names to describe a company that makes {product}?"
product = "software company for customized web frontend, backend, devops"
res = chat.llmChain(prompt, product)
print(res)

# 2. SimpleSequentialChain
prompt2 = "Write a 20 words description for the following company:{company_name}"
res = chat.simpleSequentialChain([prompt, prompt2], product)
print(res)

# 3. SequentialChain
prompt1 = "Translate the following review to english:\n\n{Review}"
prompt2 = "Can you summarize the following review in 1 sentence:\n\n{english_review}"
prompt3 = "What language is the following review:\n\n{Review}"
prompt4 = "Write a follow up response to the following summary in the specified language:\n\nSummary: {summary}\n\nLanguage: {language}"
prompts_and_outputs = [
    (prompt1, "english_review"),
    (prompt2, "summary"),
    (prompt3, "language"),
    (prompt4, "followup_message")
]
review = "Je trouve le goût médiocre. La mousse ne tient pas, c'est bizarre. J'achète les mêmes dans le commerce et le goût est bien meilleur...\nVieux lot ou contrefaçon !?"
res = chat.sequentialChain(prompts_and_outputs, review, ["Review"])
print(res)

# 4. Router Chain
