# Perfil Geográfico de Possíveis Focos de Dengue (Geographic Profiling)

Versão Aprimorada do projeto de modelagem espacial aplicada a surtos de dengue, com identificação dos focos mais prováveis de forma precisa e visualização interativa.

---

## 📌 Visão Geral

Este projeto implementa um **Geographic Profiling** para casos de dengue, inspirado em técnicas de criminologia espacial (como o modelo de Rossmo). Ele permite:

- Identificar os pontos de maior probabilidade de foco de dengue.
- Gerar mapas interativos com heatmap e marcadores dos casos.
- Obter endereços aproximados dos top focos via geocodificação reversa.

---

## 🛠 Tecnologias e Dependências

- Python 3.x
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Scikit-learn](https://scikit-learn.org/) (para Kernel Density Estimation)
- [Folium](https://python-visualization.github.io/folium/) (para mapas interativos)
- [Geopy](https://geopy.readthedocs.io/en/stable/) (para geocodificação reversa)

Instalação rápida das dependências:

pip install folium geopy scikit-learn pandas numpy

## 🗂 Estrutura do Projeto

dengue-perfil-geografico/
│
├── app.py # Código principal do projeto
├── requirements.txt # Dependências
├── sample_data/
│ └── casos_dengue.csv # Exemplo de dataset de casos
└── README.md # Documentação do projeto

## 🚀 Como Usar

Faça o download ou clone este repositório.

Coloque o arquivo CSV com os casos de dengue na pasta sample_data/.

Execute o script app.py (por exemplo, no Google Colab ou localmente).

Faça o upload do arquivo CSV quando solicitado.

O script irá gerar:

Top 5 focos mais prováveis de dengue com coordenadas e endereços.

Mapa interativo mostrando todos os casos, heatmap e os top focos.

Opcional: Salve o mapa gerado com:

m.save("mapa_dengue.html")

## 📊 Funcionalidades

KDE (Kernel Density Estimation) para identificar regiões de alta densidade de casos.

Geocodificação reversa com Nominatim para obter endereços aproximados.

Visualização interativa usando Folium:

Heatmap de casos.

Marcadores individuais.

Marcadores dos top 5 focos.

## ⚙️ Configurações e Ajustes

Bandwidth do KDE: ajustável para suavizar ou detalhar a densidade (padrão: 0.002).

Rate Limiter do Geopy: evita bloqueio do Nominatim (min_delay_seconds=1), pode ser ajustado conforme o tamanho do dataset.

Número de focos: atualmente 5, pode ser alterado na seção de seleção dos top focos.

## 📌 Observações

Este projeto é voltado para análise espacial e prevenção, não substitui medidas oficiais de saúde pública.

Recomenda-se uso com datasets pequenos ou médios devido às limitações da API do Nominatim.

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais informações.
