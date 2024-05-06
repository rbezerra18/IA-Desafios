"""
Faça uma análise sobre como este usuário tem usado o tempo dele na internet, criando um resumo do que mais é acessado, quantidade de uso e tipo de site.
https://drive.google.com/file/d/1JT06CU6I8cS9a7i7wmguclUtIzO6r5Yq/view?usp=sharing, https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221f6YY6vCSkxsWoA4eiptw6pwChLLg-C6H%22%5D,%22action%22:%22open%22,%22userId%22:%22109441343803653228203%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing
"""

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
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

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1].uri]

def extract_pdf_pages(pathname: str) -> list[str]:
  parts = [f"--- START OF PDF ${pathname} ---"]
  # Add logic to read the PDF and return a list of pages here.
  pages = []
  for index, page in enumerate(pages):
    parts.append(f"--- PAGE {index} ---")
    parts.append(page)
  return parts

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Faça uma análise sobre como este usuário tem usado o tempo dele na internet, criando um resumo do que mais é acessado, quantidade de uso e tipo de site."]
  },
  {
    "role": "user",
    "parts": extract_pdf_pages("<path>/document0.pdf")
  },
  {
    "role": "model",
    "parts": ["## Análise de Uso da Internet\n\nCom base no histórico fornecido, podemos observar os seguintes padrões de uso da internet pelo usuário:\n\n**Sites Mais Acessados:**\n\n* **Email:** O usuário acessa frequentemente o email, tanto pelo Outlook quanto pelo Gmail. O Outlook parece ser o principal serviço utilizado, com várias visitas ao longo do dia.\n* **WhatsApp Web:** O usuário acessa regularmente o WhatsApp Web para comunicação.\n* **Google:** O Google é usado para realizar pesquisas e acessar outros sites.\n* **Planilhas Google:** O usuário usa planilhas Google, principalmente para controle de ações e calendário de médicos.\n* **Discord:** O usuário participa ativamente de um servidor do Discord chamado \"Imersão IA\" e usa o Discord para comunicação com amigos.\n* **Sites de Investimentos:** O usuário acessa sites como ADVFN Brasil, Clube FII e XP Investimentos para acompanhar o mercado de ações e fundos imobiliários. \n* **Sites de Comércio Eletrônico:** O usuário realiza compras online em sites como Mercado Livre, Coto Digital, Natura e Amazon.\n* **Outros:** O histórico também mostra acessos a sites como Youtube, Netflix, Disney+, Alura (cursos online), Booking.com, gov.br (serviços governamentais) e outros.\n\n**Quantidade de Uso:**\n\n* O histórico abrange um período de 30 dias, de 29 de abril de 2024 a 6 de maio de 2024.\n* O usuário demonstra um alto volume de atividade na internet, com centenas de visitas a diversos sites. \n* Há uma concentração de acessos durante o horário comercial, sugerindo que o usuário utiliza a internet para trabalho e atividades pessoais.\n\n**Tipo de Site:**\n\n* A maioria dos sites acessados são relacionados a **comunicação**, **finanças/investimentos**, **trabalho** e **comércio eletrônico**.\n* Há também acessos a sites de **entretenimento** como Youtube, Netflix e Disney+.\n* O usuário demonstra interesse em **tecnologia e inteligência artificial**, acessando sites como Google AI Studio e participando da \"Imersão IA\" no Discord.\n\n\n## Resumo\n\nO usuário é um usuário ativo da internet que utiliza a rede para uma variedade de propósitos, incluindo comunicação, trabalho, finanças/investimentos, compras online e entretenimento. Ele demonstra interesse em tecnologia e inteligência artificial e utiliza ferramentas online para organizar suas atividades."]
  },
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)
for uploaded_file in uploaded_files:
  genai.delete_file(name=uploaded_file.name)