import pandas as pd
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

# ==== 1. DADOS SIMULADOS ====
tipo_veiculo = "Caminhão Toco"
consumo_litro_km = 0.35
capacidade_carga_kg = 12000
tipo_carga = "Adubo"
peso_carga = 10000

origem_nome = "Fazenda Nova Esperança"
origem_lat = -21.845
origem_lon = -48.265

destino_nome = "Fazenda Santa Luzia"
destino_lat = -22.014
destino_lon = -48.311

valor_pedagios = 62.5
preco_combustivel = 5.75
n_viagens = 4

# ==== 2. CÁLCULO DA DISTÂNCIA ====
def calcular_distancia_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

distancia_km = calcular_distancia_km(origem_lat, origem_lon, destino_lat, destino_lon)

# ==== 3. CÁLCULO DOS CUSTOS ====
litros_utilizados = distancia_km * consumo_litro_km
custo_combustivel = litros_utilizados * preco_combustivel
custo_total_viagem = custo_combustivel + valor_pedagios
custo_total = custo_total_viagem * n_viagens

# ==== 4. PLOTAGEM SIMPLIFICADA ====
fig, ax = plt.subplots(figsize=(10, 6))

# Plotando as fazendas como bolinhas
ax.plot(origem_lon, origem_lat, 'ro', label=origem_nome)
ax.plot(destino_lon, destino_lat, 'ro', label=destino_nome)

# Adicionando rótulos
ax.text(origem_lon + 0.01, origem_lat + 0.01, origem_nome, fontsize=10)
ax.text(destino_lon + 0.01, destino_lat + 0.01, destino_nome, fontsize=10)

# Desenhando seta entre origem e destino
ax.annotate("",
            xy=(destino_lon, destino_lat),
            xytext=(origem_lon, origem_lat),
            arrowprops=dict(arrowstyle="->", color="blue", linewidth=2))

# Resumo dos custos no canto
resumo = (
    f"Distância: {distancia_km:.2f} km\n"
    f"Litros/Viagem: {litros_utilizados:.1f} L\n"
    f"Custo Combustível: R$ {custo_combustivel:.2f}\n"
    f"Pedágios: R$ {valor_pedagios:.2f}\n"
    f"Custo por Viagem: R$ {custo_total_viagem:.2f}\n"
    f"Nº de Viagens: {n_viagens}\n"
    f"Custo Total: R$ {custo_total:.2f}"
)
plt.text(0.02, 0.02, resumo, transform=ax.transAxes,
         fontsize=10, bbox=dict(facecolor='white', alpha=0.85))

# Finalizando
plt.title("Simulação de Transporte entre Fazendas")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.tight_layout()
plt.show()
