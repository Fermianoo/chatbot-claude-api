import anthropic
import os
import pandas as pd
from datetime import datetime

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# -----------------------------------------------
# LÊ E PROCESSA OS DADOS DO CSV
# -----------------------------------------------
print("📊 Lendo dados de vendas...\n")

df = pd.read_csv("vendas.csv")
df["total"] = df["quantidade"] * df["valor_unitario"]

# Calcula os indicadores principais
total_vendas = df["total"].sum()
total_pedidos = len(df)
ticket_medio = total_vendas / total_pedidos
produto_top = df.groupby("produto")["total"].sum().idxmax()
vendedor_top = df.groupby("vendedor")["total"].sum().idxmax()
dia_top = df.groupby("data")["total"].sum().idxmax()

vendas_por_produto = df.groupby("produto")["total"].sum().to_dict()
vendas_por_vendedor = df.groupby("vendedor")["total"].sum().to_dict()

# -----------------------------------------------
# MONTA O RESUMO DOS DADOS PARA A IA
# -----------------------------------------------
resumo = f"""
Dados de vendas do período:

- Total de vendas: R$ {total_vendas:.2f}
- Total de pedidos: {total_pedidos}
- Ticket médio: R$ {ticket_medio:.2f}
- Produto mais vendido: {produto_top}
- Melhor vendedor: {vendedor_top}
- Dia de maior faturamento: {dia_top}

Vendas por produto:
{chr(10).join([f"  {p}: R$ {v:.2f}" for p, v in vendas_por_produto.items()])}

Vendas por vendedor:
{chr(10).join([f"  {v}: R$ {val:.2f}" for v, val in vendas_por_vendedor.items()])}
"""

# -----------------------------------------------
# IA GERA O RELATÓRIO EM LINGUAGEM NATURAL
# -----------------------------------------------
print("🤖 Gerando relatório com IA...\n")

prompt = f"""
Você é um analista de negócios especialista. Com base nos dados abaixo,
escreva um relatório executivo completo com:

1. Resumo geral do desempenho
2. Destaques positivos
3. Pontos de atenção
4. 3 recomendações práticas para o gestor

Use linguagem clara, profissional e objetiva. Formate bem o relatório.

{resumo}
"""

resposta = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

relatorio = resposta.content[0].text

# -----------------------------------------------
# SALVA O RELATÓRIO EM ARQUIVO
# -----------------------------------------------
nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

with open(nome_arquivo, "w") as f:
    f.write("=" * 60 + "\n")
    f.write("RELATÓRIO DE VENDAS — GERADO POR IA\n")
    f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    f.write("=" * 60 + "\n\n")
    f.write(relatorio)

print(relatorio)
print(f"\n✅ Relatório salvo em: {nome_arquivo}")