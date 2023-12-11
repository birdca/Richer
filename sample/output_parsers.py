import llm.prompt.template.openai.chat as chat
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate

payment_success_schema = ResponseSchema(name="success",
                                        description="If the payment is successful, return True.")

price_value_schema = ResponseSchema(name="price_value",
                                    description="Extract any sentences about the value or price.")

response_schemas = [payment_success_schema,
                    price_value_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

description = """  
Hi dear cutomer, congrats on your purchase of the new iPhone 16 Pro Max.
Your order number is 123456789.
price: $999
"""

json_message = """
For the following text, extract the following information:
```{description}```

Format the output as JSON with the following keys:
success
price_value
"""

# list of HumanMessage objects
message = ChatPromptTemplate.from_template(json_message).format_messages(description=description)

response = chat.get_completion(message[0].content)
print(f"response: {response}")
print(type(response))
output_dict = output_parser.parse(response)
print(type(output_dict))
print(output_dict)
