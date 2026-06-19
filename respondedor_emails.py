
import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# -----------------------------------------------
# CONFIGURE AQUI O NEGÓCIO DO CLIENTE
# -----------------------------------------------
NEGOCIO = """
Você é um atendente da Pizzaria Bella Napoli.
Somos uma pizzaria artesanal em São Paulo.
Funcionamos de terça a domingo, das 18h às 23h.
Delivery disponível pelo iFood e WhatsApp: (11) 99999-9999.
Pizzas a partir de R$45. Aceitamos Pix, cartão e dinheiro.
Não aceitamos reservas — é por ordem de chegada.
Responda sempre em português, de forma simpática e profissional.
"""

# -----------------------------------------------
# E-MAILS DE CLIENTES PARA TESTAR
# -----------------------------------------------
emails = [
    {
        "de": "maria@email.com",
        "assunto": "Horário de funcionamento",
        "mensagem": "Boa tarde! Vocês abrem no domingo? Quero ir com minha família."
    },
    {
        "de": "joao@email.com",
        "assunto": "Delivery",
        "mensagem": "Vocês fazem entrega no bairro Vila Madalena? Qual o valor mínimo?"
    },
    {
        "de": "ana@email.com",
        "assunto": "Reserva de mesa",
        "mensagem": "Olá, gostaria de reservar uma mesa para 6 pessoas no sábado à noite."
    },
]

# -----------------------------------------------
# GERA AS RESPOSTAS
# -----------------------------------------------
def gerar_resposta(email):
    prompt = f"""
E-mail recebido de: {email['de']}
Assunto: {email['assunto']}
Mensagem: {email['mensagem']}

Escreva uma resposta profissional e simpática para este e-mail.
"""
    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=NEGOCIO,
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.content[0].text

# -----------------------------------------------
# SALVA AS RESPOSTAS EM ARQUIVO
# -----------------------------------------------
print("🤖 Gerando respostas automáticas...\n")

with open("respostas.txt", "w") as arquivo:
    for i, email in enumerate(emails, 1):
        print(f"Processando e-mail {i}/{len(emails)}: {email['assunto']}")
        resposta = gerar_resposta(email)

        arquivo.write(f"{'='*50}\n")
        arquivo.write(f"PARA: {email['de']}\n")
        arquivo.write(f"ASSUNTO: Re: {email['assunto']}\n")
        arquivo.write(f"{'='*50}\n")
        arquivo.write(resposta)
        arquivo.write(f"\n\n")

print("\n✅ Respostas salvas em: respostas.txt")
print("Abra o arquivo para revisar e enviar!")