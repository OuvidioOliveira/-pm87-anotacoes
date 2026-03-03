"""
Dashboard de Análise de Risco de Clientes - Moza Banco
======================================================
Para executar:
    pip install streamlit plotly pandas numpy
    streamlit run moza_risk_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Moza Risk Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Cores Moza */
    :root {
        --moza-primary: #C8102E;
        --moza-dark:    #8B0000;
        --moza-light:   #F5F5F5;
    }

    .main { background-color: #F8F9FA; }

    .stMetric {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #C8102E;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #C8102E;
        border-bottom: 2px solid #C8102E;
        padding-bottom: 6px;
        margin-bottom: 16px;
    }

    .risk-badge-alto    { background:#FFE5E5; color:#C8102E; padding:3px 10px; border-radius:20px; font-weight:600; font-size:0.82rem; }
    .risk-badge-medio   { background:#FFF3CD; color:#856404; padding:3px 10px; border-radius:20px; font-weight:600; font-size:0.82rem; }
    .risk-badge-baixo   { background:#D4EDDA; color:#155724; padding:3px 10px; border-radius:20px; font-weight:600; font-size:0.82rem; }
    .risk-badge-sem     { background:#E2E3E5; color:#383D41; padding:3px 10px; border-radius:20px; font-weight:600; font-size:0.82rem; }

    .header-banner {
        background: linear-gradient(135deg, #C8102E 0%, #8B0000 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 14px;
        margin-bottom: 24px;
    }

    div[data-testid="stSidebar"] { background-color: #1A1A2E; }
    div[data-testid="stSidebar"] * { color: #ECECEC !important; }
    div[data-testid="stSidebar"] .stSelectbox label,
    div[data-testid="stSidebar"] .stMultiSelect label { color: #ECECEC !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    random.seed(42)
    np.random.seed(42)

    # Tabela de Factores
    factores = pd.DataFrame({
        "FACTOR_DE_RISCO": [6, 8, 5, 2, 3, 7, 4, 1],
        "DESCRICAO_DO_FACTOR": [
            "Produtos Atribuídos",
            "Canais de Distribuição",
            "Origem dos Fundos",
            "Natureza de Negócio/Profissão",
            "Modo de Relacionamento com Banco",
            "Localização Geográfica",
            "Perfil Transacional",
            "Natureza do Cliente",
        ]
    })

    # Critérios de classificação (1–8 por factor)
    criterios = []
    descricoes_por_factor = {
        1: ["Particular residente", "Empresarial PME", "Corporativo nacional",
            "Corporativo internacional", "Entidade pública", "ONG/Associação",
            "Embaixada/Diplomata", "Político/PEP"],
        2: ["Comércio formal", "Serviços profissionais", "Indústria/Produção",
            "Agricultura", "Construção civil", "Sector financeiro",
            "Actividades extractivas", "Negócio de alto risco"],
        3: ["Sucursal presencial", "Agência Express", "Internet Banking",
            "Mobile Banking", "Correspondente bancário", "Broker",
            "Plataforma digital terceira", "Representante exclusivo"],
        4: ["Transacções de baixo valor", "Uso regular cartão débito",
            "Transferências nacionais ocasionais", "Transferências int. esporádicas",
            "Alto volume transaccional", "Transacções em cash frequentes",
            "Padrão irregular", "Actividade suspeita reportada"],
        5: ["Salários/Rendimentos", "Poupanças pessoais", "Herança",
            "Venda de imóveis", "Dividendos/Investimentos",
            "Empréstimos externos", "Origem desconhecida", "Fundos de alto risco"],
        6: ["Conta poupança", "Conta corrente", "Cartão de crédito",
            "Crédito hipotecário", "Leasing", "Câmbio", "Derivados", "Offshore"],
        7: ["Maputo cidade", "Maputo província", "Gaza/Inhambane",
            "Sofala/Manica", "Tete/Zambézia", "Nampula", "Niassa/Cabo Delgado",
            "País de alto risco GAFI"],
        8: ["Balcão principal", "ATM", "POS/Terminal", "Internet Banking directo",
            "App Mobile", "Agente bancário", "API Fintech", "Plataforma não regulada"],
    }
    for fid, fdesc in zip(factores["FACTOR_DE_RISCO"], factores["DESCRICAO_DO_FACTOR"]):
        for cls in range(1, 9):
            criterios.append({
                "FACTOR_ID": fid,
                "DESCRICAO_DO_FACTOR": fdesc,
                "CLASSIFICACAO": cls,
                "DESCRICAO_CRITERIO": descricoes_por_factor[fid][cls - 1],
                "NIVEL_RISCO": "Sem Classificação" if cls == 9
                               else ("Alto" if cls >= 6 else ("Médio" if cls >= 3 else "Baixo")),
            })
    criterios_df = pd.DataFrame(criterios)

    # Clientes
    n = 300
    segmentos = ["Particular", "PME", "Corporativo", "Institucional"]
    provincias = ["Maputo", "Sofala", "Nampula", "Zambézia", "Tete", "Gaza"]
    nomes = [
        f"Cliente_{str(i).zfill(4)}" for i in range(1, n + 1)
    ]
    clientes = pd.DataFrame({
        "CLIENTE_ID": [f"MZ{str(i).zfill(5)}" for i in range(1, n + 1)],
        "NOME": nomes,
        "SEGMENTO": np.random.choice(segmentos, n, p=[0.5, 0.25, 0.15, 0.10]),
        "PROVINCIA": np.random.choice(provincias, n),
        "DATA_ABERTURA": [
            (datetime(2018, 1, 1) + timedelta(days=int(x))).strftime("%Y-%m-%d")
            for x in np.random.randint(0, 2000, n)
        ],
    })

    # Classificações por cliente/factor (com histórico trimestral)
    trimestres = pd.date_range("2023-01-01", "2025-01-01", freq="QS")
    classifs = []
    for _, cliente in clientes.iterrows():
        for _, factor in factores.iterrows():
            base = np.random.choice(range(1, 10), p=[0.12, 0.12, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.19])
            for t in trimestres:
                drift = np.clip(base + np.random.randint(-1, 2), 1, 9)
                classifs.append({
                    "CLIENTE_ID": cliente["CLIENTE_ID"],
                    "FACTOR_ID": factor["FACTOR_DE_RISCO"],
                    "DESCRICAO_FACTOR": factor["DESCRICAO_DO_FACTOR"],
                    "CLASSIFICACAO": drift,
                    "TRIMESTRE": t.strftime("%Y-T%q"),
                    "DATA": t,
                    "SEGMENTO": cliente["SEGMENTO"],
                    "PROVINCIA": cliente["PROVINCIA"],
                })
                base = drift

    classifs_df = pd.DataFrame(classifs)
    return factores, criterios_df, clientes, classifs_df

factores, criterios_df, clientes, classifs_df = gerar_dados()

# Score composto por cliente (última trimestre)
ultimo_trim = classifs_df["TRIMESTRE"].max()
df_ultimo = classifs_df[classifs_df["TRIMESTRE"] == ultimo_trim].copy()
score_cliente = (
    df_ultimo.groupby("CLIENTE_ID")["CLASSIFICACAO"]
    .mean()
    .reset_index()
    .rename(columns={"CLASSIFICACAO": "SCORE_MEDIO"})
    .merge(clientes, on="CLIENTE_ID")
)
score_cliente["NIVEL"] = score_cliente["SCORE_MEDIO"].apply(
    lambda x: "Sem Classificação" if x >= 8.5
    else ("Alto" if x >= 6 else ("Médio" if x >= 3 else "Baixo"))
)

# ─────────────────────────────────────────────
# SIDEBAR – FILTROS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 Moza Risk")
    st.markdown("### Filtros")

    segmento_sel = st.multiselect(
        "Segmento de Cliente",
        options=clientes["SEGMENTO"].unique(),
        default=clientes["SEGMENTO"].unique(),
    )

    provincia_sel = st.multiselect(
        "Província",
        options=clientes["PROVINCIA"].unique(),
        default=clientes["PROVINCIA"].unique(),
    )

    factor_sel = st.multiselect(
        "Factor de Risco",
        options=factores["DESCRICAO_DO_FACTOR"].tolist(),
        default=factores["DESCRICAO_DO_FACTOR"].tolist(),
    )

    nivel_sel = st.multiselect(
        "Nível de Risco",
        options=["Baixo", "Médio", "Alto", "Sem Classificação"],
        default=["Baixo", "Médio", "Alto", "Sem Classificação"],
    )

    st.markdown("---")
    st.caption(f"Dados até: **{ultimo_trim}**")
    st.caption("© 2025 Moza Banco")

# ─────────────────────────────────────────────
# FILTROS APLICADOS
# ─────────────────────────────────────────────
clientes_filtrados = clientes[
    clientes["SEGMENTO"].isin(segmento_sel) &
    clientes["PROVINCIA"].isin(provincia_sel)
]["CLIENTE_ID"]

df_filtrado = df_ultimo[
    df_ultimo["CLIENTE_ID"].isin(clientes_filtrados) &
    df_ultimo["DESCRICAO_FACTOR"].isin(factor_sel)
]

score_filtrado = score_cliente[
    score_cliente["CLIENTE_ID"].isin(clientes_filtrados) &
    score_cliente["NIVEL"].isin(nivel_sel)
]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h2 style="margin:0; font-size:1.7rem;">🏦 Dashboard de Análise de Risco — Moza Banco</h2>
    <p style="margin:4px 0 0; opacity:0.85;">Monitorização e avaliação do risco de clientes por factores KYC/AML</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
total_clientes = score_filtrado["CLIENTE_ID"].nunique()
sem_class = (score_filtrado["NIVEL"] == "Sem Classificação").sum()
alto_risco = (score_filtrado["NIVEL"] == "Alto").sum()
medio_risco = (score_filtrado["NIVEL"] == "Médio").sum()
baixo_risco = (score_filtrado["NIVEL"] == "Baixo").sum()
score_medio_geral = score_filtrado["SCORE_MEDIO"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👥 Total de Clientes", f"{total_clientes:,}")
c2.metric("🔴 Alto Risco", f"{alto_risco:,}", f"{alto_risco/max(total_clientes,1)*100:.1f}%")
c3.metric("🟡 Risco Médio", f"{medio_risco:,}", f"{medio_risco/max(total_clientes,1)*100:.1f}%")
c4.metric("🟢 Baixo Risco", f"{baixo_risco:,}", f"{baixo_risco/max(total_clientes,1)*100:.1f}%")
c5.metric("⚪ Sem Classificação", f"{sem_class:,}", f"{sem_class/max(total_clientes,1)*100:.1f}%")

st.markdown("---")

# ─────────────────────────────────────────────
# LINHA 1: Distribuição por Factor + Pizza Níveis
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Distribuição de Risco por Factor</p>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    dist_factor = (
        df_filtrado.groupby(["DESCRICAO_FACTOR", "CLASSIFICACAO"])
        .size()
        .reset_index(name="TOTAL")
    )
    dist_factor["NIVEL"] = dist_factor["CLASSIFICACAO"].apply(
        lambda x: "Sem Class." if x == 9
        else ("Alto (6-8)" if x >= 6 else ("Médio (3-5)" if x >= 3 else "Baixo (1-2)"))
    )
    resumo_factor = (
        dist_factor.groupby(["DESCRICAO_FACTOR", "NIVEL"])["TOTAL"]
        .sum()
        .reset_index()
    )
    cor_map = {
        "Alto (6-8)": "#C8102E",
        "Médio (3-5)": "#FFC107",
        "Baixo (1-2)": "#28A745",
        "Sem Class.": "#ADB5BD",
    }
    fig1 = px.bar(
        resumo_factor,
        x="TOTAL", y="DESCRICAO_FACTOR",
        color="NIVEL",
        color_discrete_map=cor_map,
        orientation="h",
        barmode="stack",
        labels={"TOTAL": "Nº de Classificações", "DESCRICAO_FACTOR": "Factor", "NIVEL": "Nível"},
        height=380,
    )
    fig1.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(title=""),
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    pie_data = score_filtrado["NIVEL"].value_counts().reset_index()
    pie_data.columns = ["NIVEL", "TOTAL"]
    cor_pie = {
        "Alto": "#C8102E", "Médio": "#FFC107",
        "Baixo": "#28A745", "Sem Classificação": "#ADB5BD"
    }
    fig2 = px.pie(
        pie_data, values="TOTAL", names="NIVEL",
        color="NIVEL", color_discrete_map=cor_pie,
        hole=0.55, height=380,
        title="Composição de Risco",
    )
    fig2.update_traces(textposition="outside", textinfo="percent+label")
    fig2.update_layout(
        showlegend=False,
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# LINHA 2: Clientes sem classificação
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">⚪ Clientes sem Classificação (Valor 9) por Factor</p>', unsafe_allow_html=True)

sem_class_factor = (
    df_filtrado[df_filtrado["CLASSIFICACAO"] == 9]
    .groupby("DESCRICAO_FACTOR")["CLIENTE_ID"]
    .nunique()
    .reset_index(name="SEM_CLASSIFICACAO")
    .sort_values("SEM_CLASSIFICACAO", ascending=False)
)
total_por_factor = (
    df_filtrado.groupby("DESCRICAO_FACTOR")["CLIENTE_ID"]
    .nunique()
    .reset_index(name="TOTAL")
)
sem_class_factor = sem_class_factor.merge(total_por_factor, on="DESCRICAO_FACTOR")
sem_class_factor["PERC"] = (sem_class_factor["SEM_CLASSIFICACAO"] / sem_class_factor["TOTAL"] * 100).round(1)

col3, col4 = st.columns([2, 1])

with col3:
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=sem_class_factor["DESCRICAO_FACTOR"],
        y=sem_class_factor["SEM_CLASSIFICACAO"],
        marker_color="#ADB5BD",
        name="Sem Classificação",
        text=sem_class_factor["PERC"].astype(str) + "%",
        textposition="outside",
    ))
    fig3.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        height=320, margin=dict(l=10, r=10, t=10, b=80),
        xaxis=dict(tickangle=-30),
        yaxis=dict(title="Nº de Clientes"),
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.dataframe(
        sem_class_factor[["DESCRICAO_FACTOR", "SEM_CLASSIFICACAO", "PERC"]]
        .rename(columns={
            "DESCRICAO_FACTOR": "Factor",
            "SEM_CLASSIFICACAO": "S/ Classif.",
            "PERC": "% do Total"
        }),
        use_container_width=True,
        height=300,
    )

# ─────────────────────────────────────────────
# LINHA 3: Top clientes por risco + Segmento
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">🏆 Ranking de Clientes por Risco</p>', unsafe_allow_html=True)

col5, col6 = st.columns([1.5, 1])

with col5:
    top_n = st.slider("Nº de clientes no ranking", 10, 50, 20)
    top_clientes = (
        score_filtrado
        .nlargest(top_n, "SCORE_MEDIO")[
            ["CLIENTE_ID", "NOME", "SEGMENTO", "PROVINCIA", "SCORE_MEDIO", "NIVEL"]
        ]
        .reset_index(drop=True)
    )
    top_clientes.index += 1
    top_clientes["SCORE_MEDIO"] = top_clientes["SCORE_MEDIO"].round(2)

    def color_nivel(val):
        colors = {
            "Alto": "background-color:#FFE5E5; color:#C8102E",
            "Médio": "background-color:#FFF3CD; color:#856404",
            "Baixo": "background-color:#D4EDDA; color:#155724",
            "Sem Classificação": "background-color:#E2E3E5; color:#383D41",
        }
        return colors.get(val, "")

    styled = top_clientes.style.applymap(color_nivel, subset=["NIVEL"])
    st.dataframe(styled, use_container_width=True, height=400)

with col6:
    seg_risco = (
        score_filtrado.groupby(["SEGMENTO", "NIVEL"])
        .size()
        .reset_index(name="TOTAL")
    )
    fig4 = px.bar(
        seg_risco, x="SEGMENTO", y="TOTAL",
        color="NIVEL", color_discrete_map={
            "Alto": "#C8102E", "Médio": "#FFC107",
            "Baixo": "#28A745", "Sem Classificação": "#ADB5BD"
        },
        barmode="group",
        title="Risco por Segmento",
        height=400,
        labels={"TOTAL": "Nº Clientes", "SEGMENTO": "Segmento"},
    )
    fig4.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(title="Nível"),
    )
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# LINHA 4: Evolução temporal
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📈 Evolução do Risco ao Longo do Tempo</p>', unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    # Score médio geral por trimestre
    evolucao = (
        classifs_df[
            classifs_df["CLIENTE_ID"].isin(clientes_filtrados) &
            classifs_df["DESCRICAO_FACTOR"].isin(factor_sel)
        ]
        .groupby("DATA")["CLASSIFICACAO"]
        .mean()
        .reset_index(name="SCORE_MEDIO")
    )
    fig5 = px.line(
        evolucao, x="DATA", y="SCORE_MEDIO",
        title="Score Médio de Risco por Trimestre",
        markers=True,
        color_discrete_sequence=["#C8102E"],
        labels={"SCORE_MEDIO": "Score Médio", "DATA": ""},
        height=340,
    )
    fig5.add_hline(y=6, line_dash="dash", line_color="orange", annotation_text="Limite Alto Risco")
    fig5.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig5, use_container_width=True)

with col8:
    # % clientes alto risco por trimestre
    evolucao_alto = (
        classifs_df[classifs_df["CLIENTE_ID"].isin(clientes_filtrados)]
        .groupby("DATA")
        .apply(lambda g: (g["CLASSIFICACAO"] >= 6).mean() * 100)
        .reset_index(name="PERC_ALTO")
    )
    fig6 = px.area(
        evolucao_alto, x="DATA", y="PERC_ALTO",
        title="% de Clientes em Alto Risco (Score ≥ 6)",
        color_discrete_sequence=["#C8102E"],
        labels={"PERC_ALTO": "% Clientes", "DATA": ""},
        height=340,
    )
    fig6.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig6, use_container_width=True)

# ─────────────────────────────────────────────
# LINHA 5: Heatmap Factor x Classificação
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">🔥 Mapa de Calor — Factor vs Classificação</p>', unsafe_allow_html=True)

heat_data = (
    df_filtrado.groupby(["DESCRICAO_FACTOR", "CLASSIFICACAO"])
    .size()
    .reset_index(name="TOTAL")
)
heat_pivot = heat_data.pivot(index="DESCRICAO_FACTOR", columns="CLASSIFICACAO", values="TOTAL").fillna(0)

fig7 = px.imshow(
    heat_pivot,
    color_continuous_scale=["#D4EDDA", "#FFF3CD", "#C8102E"],
    labels=dict(x="Classificação (1=Baixo, 9=Sem Class.)", y="Factor", color="Nº Clientes"),
    aspect="auto",
    height=370,
    title="Concentração de Clientes por Factor e Classificação",
)
fig7.update_layout(
    plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(l=10, r=10, t=40, b=10),
    coloraxis_colorbar=dict(title="Clientes"),
)
st.plotly_chart(fig7, use_container_width=True)

# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("🏦 Moza Banco · Dashboard de Risco KYC/AML · Dados gerados para demonstração · © 2025")
