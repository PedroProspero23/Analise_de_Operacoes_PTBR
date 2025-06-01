import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF

# Caminho dos dados e saída para gráficos
data_path = "C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Estoque Analysis/estoque_exemplo.csv"
graficos_path = "output/graficos"
os.makedirs(graficos_path, exist_ok=True)

# Leitura dos dados
df = pd.read_csv(data_path, parse_dates=["Data"])
produto = df["Produto"].unique()[0]  # Consideramos um único produto por enquanto

# Ordenar por data
df = df.sort_values("Data")

# Cálculos
estoque_medio = df["Estoque"].mean()
consumo_total = df["Saida"].sum()
dias_totais = (df["Data"].max() - df["Data"].min()).days
consumo_medio_diario = consumo_total / dias_totais
giro_estoque = consumo_total / estoque_medio if estoque_medio else 0
cobertura = df["Estoque"].iloc[-1] / consumo_medio_diario if consumo_medio_diario else 0

# Parâmetros fictícios (ajustáveis)
estoque_minimo = consumo_medio_diario * 7  # 1 semana de cobertura
ponto_reposicao = consumo_medio_diario * 10  # Repor se atingir menos de 10 dias

# Gráfico: Estoque ao longo do tempo
plt.figure(figsize=(10, 5))
plt.plot(df["Data"], df["Estoque"], marker="o", label="Estoque")
plt.axhline(estoque_minimo, color='red', linestyle='--', label='Estoque Mínimo')
plt.axhline(ponto_reposicao, color='orange', linestyle='--', label='Ponto de Reposição')
plt.title(f"Evolução do Estoque - {produto}")
plt.xlabel("Data")
plt.ylabel("Quantidade em Estoque")
plt.legend()
plt.tight_layout()
grafico_estoque_path = os.path.join(graficos_path, "estoque.png")
plt.savefig(grafico_estoque_path)
plt.close()

# Gráfico: Entradas e Saídas
plt.figure(figsize=(10, 5))
plt.bar(df["Data"], df["Entrada"], color='green', label='Entrada')
plt.bar(df["Data"], df["Saida"], color='red', label='Saída', alpha=0.7)
plt.title(f"Movimentações - {produto}")
plt.xlabel("Data")
plt.ylabel("Quantidade")
plt.legend()
plt.tight_layout()
grafico_mov_path = os.path.join(graficos_path, "movimentacoes.png")
plt.savefig(grafico_mov_path)
plt.close()

# Relatório PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, f"Relatório de Estoque - {produto}", ln=True)

pdf.set_font("Arial", "", 12)
pdf.ln(5)
pdf.cell(0, 10, f"Período analisado: {df['Data'].min().date()} a {df['Data'].max().date()}", ln=True)
pdf.cell(0, 10, f"Estoque médio: {estoque_medio:.2f}", ln=True)
pdf.cell(0, 10, f"Consumo médio diário: {consumo_medio_diario:.2f}", ln=True)
pdf.cell(0, 10, f"Giro de estoque: {giro_estoque:.2f}", ln=True)
pdf.cell(0, 10, f"Cobertura de estoque (dias): {cobertura:.1f}", ln=True)
pdf.cell(0, 10, f"Ponto de reposição sugerido: {ponto_reposicao:.2f}", ln=True)

pdf.ln(10)
pdf.image(grafico_estoque_path, w=180)
pdf.ln(10)
pdf.image(grafico_mov_path, w=180)

# Novo caminho: Downloads
relatorio_pdf = "C:/Users/pedro/Downloads/relatorio_estoque.pdf"
pdf.output(relatorio_pdf)

print("✅ Relatório salvo em: Downloads/relatorio_estoque.pdf")
