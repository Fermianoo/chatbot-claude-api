import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Histórico da conversa — começa vazio
historico = []

# Personalidade do chatbot
sistema = "Você é um assistente especialista em IA. Responda sempre em português, de forma clara e objetiva."

print("🤖 Chatbot ativo! Digite 'sair' para encerrar.\n")

while True:
    # Lê a mensagem do usuário
    entrada = input("Você: ").strip()

    if entrada.lower() == "sair":
        print("Até mais!")
        break

    if not entrada:
        continue

    # Adiciona a mensagem do usuário ao histórico
    historico.append({
        "role": "user",
        "content": entrada
    })

    # Chama a API enviando o histórico completo
    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=sistema,
        messages=historico
    )

    texto = resposta.content[0].text

    # Adiciona a resposta do Claude ao histórico
    historico.append({
        "role": "assistant",
        "content": texto
    })

    print(f"\nClaude: {texto}\n")
