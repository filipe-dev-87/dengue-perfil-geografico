# ===============================================
# GEO-PERFIS DE DENGUE (Geographic Profiling)
# Versão Aprimorada
# ===============================================

# Instalar dependências
!pip install --quiet folium geopy scikit-learn pandas numpy

# ------------------------------------------------
# 1. IMPORTS
# ------------------------------------------------
from google.colab import files
import pandas as pd
import numpy as np
import folium
from sklearn.neighbors import KernelDensity
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from folium.plugins import HeatMap

# ------------------------------------------------
# 2. UPLOAD DO CSV
# ------------------------------------------------
print("Faça upload do arquivo 'casos_dengue.csv'")
uploaded = files.upload()
arquivo = list(uploaded.keys())[0]

df = pd.read_csv(arquivo)
print(f"Arquivo '{arquivo}' carregado com sucesso!")
print(df.head())

# ------------------------------------------------
# 3. CONFIGURAÇÃO DO KDE
# ------------------------------------------------
coords = df[['latitude', 'longitude']].to_numpy()
bandwidth = 0.002  # Ajuste conforme necessário

kde = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
kde.fit(coords)

# Criação da grade de pontos
lat_min, lat_max = coords[:,0].min() - 0.005, coords[:,0].max() + 0.005
lon_min, lon_max = coords[:,1].min() - 0.005, coords[:,1].max() + 0.005
grid_lat, grid_lon = np.mgrid[lat_min:lat_max:100j, lon_min:lon_max:100j]
grid_points = np.vstack([grid_lat.ravel(), grid_lon.ravel()]).T

# Calcula densidade
log_dens = kde.score_samples(grid_points)
dens = np.exp(log_dens)

# Top 5 focos mais prováveis
indices_top5 = np.argsort(dens)[-5:][::-1]
top5_coords = grid_points[indices_top5]

# ------------------------------------------------
# 4. GEOCODIFICAÇÃO REVERSA COM RATE LIMITER
# ------------------------------------------------
geolocator = Nominatim(user_agent="geo_dengue_model")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)  # evita bloqueio

enderecos = []
for lat, lon in top5_coords:
    try:
        location = geocode((lat, lon), timeout=10)
        endereco = location.address if location else "Endereço não encontrado"
    except Exception as e:
        endereco = f"Erro: {e}"
    enderecos.append(endereco)

# Mostra ranking
print("\nTop 5 locais mais prováveis de foco:")
for i, (lat, lon, end) in enumerate(zip(top5_coords[:,0], top5_coords[:,1], enderecos), 1):
    print(f"{i}. ({lat:.6f}, {lon:.6f}) -> {end}")

# ------------------------------------------------
# 5. MAPA INTERATIVO COM FOLIUM
# ------------------------------------------------
m = folium.Map(location=[coords[:,0].mean(), coords[:,1].mean()], zoom_start=14)

# HeatMap de todos os casos
HeatMap(coords, radius=10, blur=15, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}).add_to(m)

# Marcadores dos casos confirmados
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=4, color='red', fill=True, fill_opacity=0.6,
        popup=f"Caso confirmado: ID {row['id']}"
    ).add_to(m)

# Marcadores dos top 5 focos
for i, (lat, lon, end) in enumerate(zip(top5_coords[:,0], top5_coords[:,1], enderecos), 1):
    folium.Marker(
        [lat, lon],
        popup=f"Foco {i}\n{end}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Exibe mapa
m
