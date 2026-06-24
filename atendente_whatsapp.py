import anthropic
import os
from datetime import datetime

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# -----------------------------------------------
# CONFIGURE O NEGÓCIO DO CLIENTE
# -----------------------------------------------
NEGOCIO = """
Você é o atendente virtual da Pizzaria Bella Napoli via WhatsApp.
Somos uma pizzaria artesanal em São Paulo.
Funcionamos de terça a domingo, das 18h às 23h.
Delivery pelo iFood e WhatsApp: (11) 99999-9999.
Pizzas a partir de R$45. Aceitamos Pix, cartão e dinheiro.
Não aceitamos reservas — atendimento por ordem de chegada.
Sabores disponíveis: Margherita, Calabresa, Frango com Catupiry,
Quatro Queijos, Portuguesa e Vegana (R$55).

Regras importantes:
- Seja simpático e use linguagem informal, como no WhatsApp
- Respostas curtas — no máximo 3 linhas por mensagem
- Use emojis com moderação (1-2 por mensagem)
- Nunca invente informações que não estão aqui
- Se não souber responder, diga: "Vou verificar e te retorno em instantes!"
"""

# -----------------------------------------------
# MEMÓRIA SEPARADA POR CLIENTE (número de WhatsApp)
# -----------------------------------------------
clientes = {}

def atender(numero, mensagem):
    # Cria histórico vazio se for o primeiro contato
    if numero not in clientes:
        clientes[numero] = []
        print(f"  📱 Novo cliente conectado: {numero}")

    # Adiciona mensagem do cliente ao histórico DELE
    clientes[numero].append({
        "role": "user",
        "content": mensagem
    })

    # Chama o Claude com o histórico completo do cliente
    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=NEGOCIO,
        messages=clientes[numero]
    )

    texto = resposta.content[0].text

    # Salva a resposta no histórico do cliente
    clientes[numero].append({
        "role": "assistant",
        "content": texto
    })

    return texto

# -----------------------------------------------
# SIMULADOR — escolha o cliente e envie mensagens
# -----------------------------------------------
print("=" * 50)
print("📱 SIMULADOR DE ATENDENTE WHATSAPP")
print("=" * 50)
print("Simule múltiplos clientes com números diferentes.")
print("Digite 'clientes' para ver quem está ativo.")
print("Digite 'sair' para encerrar.\n")

while True:
    numero = input("Número do cliente (ex: 11999991111): ").strip()

    if numero.lower() == "sair":
        print("\nAtendente encerrado. Até mais!")
        break

    if numero.lower() == "clientes":
        if clientes:
            print(f"\n📋 Clientes ativos: {list(clientes.keys())}")
            for num, hist in clientes.items():
                msgs = len([m for m in hist if m["role"] == "user"])
                print(f"  {num} → {msgs} mensagem(ns)")
        else:
            print("  Nenhum cliente ativo ainda.")
        print()
        continue

    if not numero:
        continue

    mensagem = input(f"[{numero}] Mensagem: ").strip()

    if not mensagem:
        continue

    print("\n⏳ Atendente respondendo...\n")
    resposta = atender(numero, mensagem)

    hora = datetime.now().strftime("%H:%M")
    print(f"[{hora}] 🤖 Atendente → {numero}:")
    print(f"{resposta}\n")
    print("-" * 40)