"""
Imposto de Renda
https://aistudio.google.com/app/prompts/1fZfzv_YqIP6LSwRQGw5kIBSh3RgMrryG
"""

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Pergunta:\nTenho uma lista de valores. O meu resultado final será 30% da soma de valores. Porém, nem todos os valores serão somados, apenas aqueles acima de R$40.000,00. Para a lista abaixo, conte quantos valores existem e me diga qual é o meu resultado final?\nR$10.000,00\nR$20.000,00\nR$50.000,00\nR$60.000,00\n\nResposta:\nNessa lista existem 4 valores. Há 2 valores acima de R$40.000,00, que são R$50.000,00 e R$60.000,00. A soma desses valores é R$110.000,00. O resultado final é 30% da soma desses valores, portanto, 30% de R$110.000,00, que resulta em R$33.000,00.\n\nPergunta:\nTenho uma lista de valores. O meu resultado final será 30% da soma de valores. Porém, nem todos os valores serão somados, apenas aqueles acima de R$40.000,00. Para a lista abaixo, conte quantos valores existem e me diga qual é o meu resultado final?\nR$31.000,00\nR$15.000,00\nR$52.000,00\nR$103.000,00\nR$42.000,00\nR$156.000,00\nR$15.000,00\nR$27.000,00\nR$82.000,00\nR$33.000,00"]
  },
  {
    "role": "model",
    "parts": ["Resposta: \nNessa lista existem 10 valores. Há 5 valores acima de R$40.000,00, que são R$52.000,00, R$103.000,00, R$42.000,00, R$156.000,00 e R$82.000,00. A soma desses valores é R$435.000,00. O resultado final é 30% da soma desses valores, portanto, 30% de R$435.000,00, que resulta em R$130.500,00."]
  },
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)