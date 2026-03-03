"""
Moza Banco · Risk Intelligence Platform  — Premium Light Edition
=================================================================
pip install streamlit plotly pandas numpy
streamlit run moza_risk_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Moza · Risk Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PREMIUM LIGHT CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Mono:wght@300;400;500&display=swap');

/* ── TOKENS ── */
:root {
  --bg:        #F4F1EC;
  --bg2:       #EDE9E2;
  --white:     #FFFFFF;
  --border:    rgba(0,0,0,0.07);
  --border2:   rgba(0,0,0,0.12);
  --ink:       #1C1816;
  --ink2:      #4A4440;
  --ink3:      #9C948E;
  --red:       #C8102E;
  --red-light: #FCEEF1;
  --red-mid:   rgba(200,16,46,0.12);
  --amber:     #B45309;
  --amber-bg:  #FFFBEB;
  --green:     #065F46;
  --green-bg:  #ECFDF5;
  --blue:      #1D4ED8;
  --blue-bg:   #EFF6FF;
  --slate:     #64748B;
  --slate-bg:  #F8FAFC;
  --sans:      'DM Sans', sans-serif;
  --serif:     'Playfair Display', Georgia, serif;
  --mono:      'DM Mono', 'Courier New', monospace;
  --radius:    14px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow:    0 4px 16px rgba(0,0,0,0.07), 0 1px 4px rgba(0,0,0,0.05);
  --shadow-lg: 0 10px 32px rgba(0,0,0,0.10), 0 2px 8px rgba(0,0,0,0.06);
}

/* ── BASE ── */
html, body, [class*="css"] { font-family: var(--sans); }
.stApp { background: var(--bg); }
.main .block-container { padding: 0 2.5rem 4rem; max-width: 1480px; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #D4CFC8; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--white) !important;
  border-right: 1px solid var(--border2) !important;
  box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebar"] * { color: var(--ink2) !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: var(--bg) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important;
  font-family: var(--sans) !important;
}
[data-testid="stSidebar"] label {
  font-family: var(--mono) !important;
  font-size: .65rem !important;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink3) !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] .stMultiSelect span {
  background: var(--red-light) !important;
  color: var(--red) !important;
  border: 1px solid rgba(200,16,46,0.2) !important;
  border-radius: 4px !important;
  font-size: .75rem !important;
}

/* ── HERO ── */
.hero {
  position: relative;
  background: var(--white);
  border: 1px solid var(--border2);
  border-radius: 20px;
  padding: 0;
  margin: 0 0 28px;
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
}
.hero-left {
  flex: 1;
  padding: 38px 44px 38px;
  border-right: 1px solid var(--border);
}
.hero-stripe {
  width: 6px;
  background: linear-gradient(180deg, var(--red) 0%, #8B0000 100%);
  flex-shrink: 0;
}
.hero-right {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 38px 52px;
  background: linear-gradient(135deg, #FBF9F7 0%, #F4F1EC 100%);
  gap: 48px;
}
.hero-eyebrow {
  font-family: var(--mono);
  font-size: .65rem;
  font-weight: 500;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--red);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.hero-eyebrow::before {
  content: '';
  display: inline-block;
  width: 24px;
  height: 1.5px;
  background: var(--red);
}
.hero-title {
  font-family: var(--serif);
  font-size: 2.15rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.15;
  letter-spacing: -.01em;
  margin-bottom: 10px;
}
.hero-title em { color: var(--red); font-style: italic; }
.hero-sub {
  font-family: var(--mono);
  font-size: .78rem;
  color: var(--ink3);
  font-weight: 300;
  letter-spacing: .04em;
}
.hero-stat {
  text-align: center;
}
.hero-stat-val {
  font-family: var(--mono);
  font-size: 2.6rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1;
  letter-spacing: -.04em;
}
.hero-stat-val.red { color: var(--red); }
.hero-stat-lbl {
  font-family: var(--mono);
  font-size: .62rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--ink3);
  margin-top: 6px;
}
.hero-divider {
  width: 1px;
  height: 52px;
  background: var(--border2);
  flex-shrink: 0;
}

/* ── KPI CARDS ── */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  margin-bottom: 32px;
}
.kpi {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px 22px 18px;
  position: relative;
  box-shadow: var(--shadow-sm);
  transition: box-shadow .2s, transform .2s, border-color .2s;
  overflow: hidden;
  cursor: default;
}
.kpi:hover {
  box-shadow: var(--shadow);
  transform: translateY(-2px);
  border-color: var(--border2);
}
.kpi-top-bar {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-icon {
  position: absolute;
  top: 18px; right: 18px;
  width: 34px; height: 34px;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.05rem;
}
.kpi-lbl {
  font-family: var(--mono);
  font-size: .63rem;
  font-weight: 500;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--ink3);
  margin-bottom: 14px;
  margin-top: 4px;
}
.kpi-val {
  font-family: var(--mono);
  font-size: 2.25rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1;
  letter-spacing: -.04em;
}
.kpi-pct {
  font-family: var(--mono);
  font-size: .72rem;
  color: var(--ink3);
  margin-top: 8px;
  font-weight: 300;
}

/* ── SECTION HEADER ── */
.sec {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 36px 0 16px;
}
.sec-num {
  font-family: var(--mono);
  font-size: .62rem;
  color: var(--red);
  letter-spacing: .06em;
  flex-shrink: 0;
}
.sec-label {
  font-family: var(--sans);
  font-size: .7rem;
  font-weight: 600;
  letter-spacing: .13em;
  text-transform: uppercase;
  color: var(--ink2);
  white-space: nowrap;
}
.sec-line {
  flex: 1;
  height: 1px;
  background: var(--border2);
}

/* ── CHART CARDS ── */
.card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px 22px 16px;
  box-shadow: var(--shadow-sm);
  height: 100%;
}
.card-title {
  font-family: var(--mono);
  font-size: .65rem;
  font-weight: 500;
  letter-spacing: .13em;
  text-transform: uppercase;
  color: var(--ink3);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 9px;
}
.card-title::before {
  content: '';
  display: inline-block;
  width: 3px; height: 14px;
  background: var(--red);
  border-radius: 2px;
  flex-shrink: 0;
}

/* ── TABLE ── */
div[data-testid="stDataFrame"] {
  border-radius: 10px !important;
  overflow: hidden;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-sm) !important;
}

/* ── PLOTLY ── */
div[data-testid="stPlotlyChart"] { border-radius: 10px; overflow: hidden; }

/* ── SLIDER ── */
div[data-testid="stSlider"] label {
  font-family: var(--mono) !important;
  font-size: .63rem !important;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink3) !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
  background: var(--red) !important;
  border-color: var(--red) !important;
}

/* ── SIDEBAR BRAND ── */
.brand {
  padding: 28px 22px 22px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.brand-mark {
  width: 38px; height: 38px;
  background: var(--red);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(200,16,46,0.3);
}
.brand-m {
  font-family: var(--serif);
  font-size: 1.2rem;
  font-weight: 700;
  color: white;
  line-height: 1;
}
.brand-name {
  font-family: var(--serif);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--ink) !important;
  letter-spacing: -.01em;
  line-height: 1;
}
.brand-sub {
  font-family: var(--mono);
  font-size: .62rem !important;
  color: var(--ink3) !important;
  letter-spacing: .1em;
  text-transform: uppercase;
  margin-top: 3px;
}
.sidebar-section {
  font-family: var(--mono);
  font-size: .6rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--ink3) !important;
  margin-bottom: 12px;
  padding: 0 2px;
}

/* ── FOOTER ── */
.footer {
  margin-top: 60px;
  padding: 22px 0;
  border-top: 1px solid var(--border2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.footer span {
  font-family: var(--mono);
  font-size: .68rem;
  color: var(--ink3);
  font-weight: 300;
}
.footer-dot {
  width: 4px; height: 4px;
  background: var(--red);
  border-radius: 50%;
  display: inline-block;
  margin: 0 8px;
  vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# ── CHART CONSTANTS ───────────────────────────────────────────────────────────
BG_C   = "#FFFFFF"
PLOT_C = "#FAFAF9"
GRID   = "#F0EDE8"
AXIS   = "#E0DBD4"
TEXT_C = "#9C948E"
C_RED   = "#C8102E"
C_AMB   = "#D97706"
C_GRN   = "#059669"
C_BLU   = "#2563EB"
C_SLT   = "#94A3B8"
NIVEL_C = {"Alto":C_RED, "Médio":C_AMB, "Baixo":C_GRN, "Sem Classificação":C_SLT}

def ql(fig, h=360, lt=10, lb=10, legend_h=False):
    fig.update_layout(
        height=h,
        paper_bgcolor=BG_C,
        plot_bgcolor=PLOT_C,
        font=dict(family="DM Sans", color=TEXT_C, size=11.5),
        margin=dict(l=4, r=4, t=lt, b=lb),
        xaxis=dict(gridcolor=GRID, linecolor=AXIS, tickcolor=AXIS,
                   zerolinecolor=GRID, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRID, linecolor=AXIS, tickcolor=AXIS,
                   zerolinecolor=GRID, tickfont=dict(size=11)),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
            font=dict(color="#4A4440", size=11),
            orientation="h" if legend_h else "v",
            yanchor="bottom" if legend_h else "auto",
            y=1.02 if legend_h else None,
            xanchor="left" if legend_h else "auto",
            x=0 if legend_h else None,
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=AXIS,
            font_color="#1C1816",
            font_family="DM Mono",
            font_size=12,
        ),
    )
    return fig

# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    np.random.seed(42)
    factores = pd.DataFrame({
        "FACTOR_DE_RISCO": [6,8,5,2,3,7,4,1],
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
    dpf = {
        1:["Particular residente","Empresarial PME","Corporativo nacional","Corporativo int.","Entidade pública","ONG/Associação","Embaixada/Diplomata","Político/PEP"],
        2:["Comércio formal","Serviços profissionais","Indústria/Produção","Agricultura","Construção civil","Sector financeiro","Actividades extractivas","Negócio de alto risco"],
        3:["Sucursal presencial","Agência Express","Internet Banking","Mobile Banking","Correspondente bancário","Broker","Plataforma digital terceira","Representante exclusivo"],
        4:["Transacções baixo valor","Cartão débito regular","Transfer. nac. ocasionais","Transfer. int. esporádicas","Alto volume transaccional","Cash frequente","Padrão irregular","Actividade suspeita"],
        5:["Salários/Rendimentos","Poupanças pessoais","Herança","Venda de imóveis","Dividendos/Invest.","Empréstimos externos","Origem desconhecida","Fundos de alto risco"],
        6:["Conta poupança","Conta corrente","Cartão de crédito","Crédito hipotecário","Leasing","Câmbio","Derivados","Offshore"],
        7:["Maputo cidade","Maputo província","Gaza/Inhambane","Sofala/Manica","Tete/Zambézia","Nampula","Niassa/Cabo Delgado","País alto risco GAFI"],
        8:["Balcão principal","ATM","POS/Terminal","Internet Banking directo","App Mobile","Agente bancário","API Fintech","Plataforma não regulada"],
    }
    criterios = []
    for fid, fdesc in zip(factores["FACTOR_DE_RISCO"], factores["DESCRICAO_DO_FACTOR"]):
        for cls in range(1, 9):
            criterios.append({
                "FACTOR_ID": fid, "DESCRICAO_DO_FACTOR": fdesc,
                "CLASSIFICACAO": cls, "DESCRICAO_CRITERIO": dpf[fid][cls-1],
                "NIVEL_RISCO": "Alto" if cls>=6 else ("Médio" if cls>=3 else "Baixo")
            })
    criterios_df = pd.DataFrame(criterios)
    n = 300
    clientes = pd.DataFrame({
        "CLIENTE_ID":    [f"MZ{str(i).zfill(5)}" for i in range(1, n+1)],
        "NOME":          [f"Cliente_{str(i).zfill(4)}" for i in range(1, n+1)],
        "SEGMENTO":      np.random.choice(["Particular","PME","Corporativo","Institucional"], n, p=[0.5,0.25,0.15,0.10]),
        "PROVINCIA":     np.random.choice(["Maputo","Sofala","Nampula","Zambézia","Tete","Gaza"], n),
        "DATA_ABERTURA": [(datetime(2018,1,1)+timedelta(days=int(x))).strftime("%Y-%m-%d")
                         for x in np.random.randint(0, 2000, n)],
    })
    trimestres = pd.date_range("2023-01-01", "2025-01-01", freq="QS")
    classifs = []
    for _, cli in clientes.iterrows():
        for _, fac in factores.iterrows():
            base = np.random.choice(range(1,10), p=[0.12,0.12,0.12,0.11,0.10,0.09,0.08,0.07,0.19])
            for t in trimestres:
                drift = int(np.clip(base + np.random.randint(-1, 2), 1, 9))
                classifs.append({
                    "CLIENTE_ID":       cli["CLIENTE_ID"],
                    "FACTOR_ID":        fac["FACTOR_DE_RISCO"],
                    "DESCRICAO_FACTOR": fac["DESCRICAO_DO_FACTOR"],
                    "CLASSIFICACAO":    drift,
                    "TRIMESTRE":        t.strftime("%Y-T%q"),
                    "DATA":             t,
                    "SEGMENTO":         cli["SEGMENTO"],
                    "PROVINCIA":        cli["PROVINCIA"],
                })
                base = drift
    return factores, criterios_df, clientes, pd.DataFrame(classifs)

factores, criterios_df, clientes, classifs_df = gerar_dados()

ultimo_trim = classifs_df["TRIMESTRE"].max()
df_ultimo   = classifs_df[classifs_df["TRIMESTRE"] == ultimo_trim].copy()
score_cliente = (
    df_ultimo.groupby("CLIENTE_ID")["CLASSIFICACAO"].mean()
    .reset_index().rename(columns={"CLASSIFICACAO":"SCORE_MEDIO"})
    .merge(clientes, on="CLIENTE_ID")
)
score_cliente["NIVEL"] = score_cliente["SCORE_MEDIO"].apply(
    lambda x: "Sem Classificação" if x>=8.5 else ("Alto" if x>=6 else ("Médio" if x>=3 else "Baixo"))
)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-mark"><div class="brand-m">M</div></div>
      <div class="brand-name">Moza Banco</div>
      <div class="brand-sub">Risk Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Filtros de Análise</div>', unsafe_allow_html=True)

    segmento_sel  = st.multiselect("Segmento",
        options=clientes["SEGMENTO"].unique(),
        default=clientes["SEGMENTO"].unique())
    provincia_sel = st.multiselect("Província",
        options=clientes["PROVINCIA"].unique(),
        default=clientes["PROVINCIA"].unique())
    factor_sel    = st.multiselect("Factor de Risco",
        options=factores["DESCRICAO_DO_FACTOR"].tolist(),
        default=factores["DESCRICAO_DO_FACTOR"].tolist())
    nivel_sel     = st.multiselect("Nível de Risco",
        options=["Baixo","Médio","Alto","Sem Classificação"],
        default=["Baixo","Médio","Alto","Sem Classificação"])

    st.markdown(f"""
    <div style="margin-top:28px; padding:16px 18px;
         background:#F4F1EC; border:1px solid rgba(0,0,0,0.08);
         border-radius:10px;">
      <div style="font-family:'DM Mono',monospace; font-size:.6rem; letter-spacing:.12em;
           text-transform:uppercase; color:#9C948E; margin-bottom:5px;">Período activo</div>
      <div style="font-family:'DM Mono',monospace; font-size:.85rem;
           color:#1C1816; font-weight:500;">{ultimo_trim}</div>
      <div style="margin-top:10px; font-family:'DM Mono',monospace; font-size:.6rem;
           letter-spacing:.12em; text-transform:uppercase; color:#9C948E; margin-bottom:5px;">Factores activos</div>
      <div style="font-family:'DM Mono',monospace; font-size:.85rem; color:#1C1816; font-weight:500;">{len(factor_sel)} / {len(factores)}</div>
    </div>
    """, unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────────────────────────
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

total   = score_filtrado["CLIENTE_ID"].nunique()
n_alto  = (score_filtrado["NIVEL"]=="Alto").sum()
n_medio = (score_filtrado["NIVEL"]=="Médio").sum()
n_baixo = (score_filtrado["NIVEL"]=="Baixo").sum()
n_sem   = (score_filtrado["NIVEL"]=="Sem Classificação").sum()
pct     = lambda n: f"{n/max(total,1)*100:.1f}% do total"

# ── HERO ──────────────────────────────────────────────────────────────────────
score_avg = score_filtrado["SCORE_MEDIO"].mean() if total > 0 else 0
pct_alto  = n_alto / max(total, 1) * 100

st.markdown(f"""
<div class="hero">
  <div class="hero-stripe"></div>
  <div class="hero-left">
    <div class="hero-eyebrow">Análise de Risco · KYC / AML</div>
    <div class="hero-title">Risk <em>Intelligence</em><br>Dashboard</div>
    <div class="hero-sub">Moza Banco &nbsp;·&nbsp; {ultimo_trim} &nbsp;·&nbsp; {total:,} clientes analisados</div>
  </div>
  <div class="hero-right">
    <div class="hero-stat">
      <div class="hero-stat-val">{total:,}</div>
      <div class="hero-stat-lbl">Clientes totais</div>
    </div>
    <div class="hero-divider"></div>
    <div class="hero-stat">
      <div class="hero-stat-val red">{n_alto:,}</div>
      <div class="hero-stat-lbl">Alto risco</div>
    </div>
    <div class="hero-divider"></div>
    <div class="hero-stat">
      <div class="hero-stat-val">{pct_alto:.1f}<span style="font-size:1.4rem">%</span></div>
      <div class="hero-stat-lbl">Taxa exposição</div>
    </div>
    <div class="hero-divider"></div>
    <div class="hero-stat">
      <div class="hero-stat-val">{score_avg:.2f}</div>
      <div class="hero-stat-lbl">Score médio</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-top-bar" style="background:{C_BLU};"></div>
    <div class="kpi-icon" style="background:#EFF6FF;">👥</div>
    <div class="kpi-lbl">Total de Clientes</div>
    <div class="kpi-val">{total:,}</div>
    <div class="kpi-pct">{len(segmento_sel)} seg. · {len(provincia_sel)} prov.</div>
  </div>
  <div class="kpi">
    <div class="kpi-top-bar" style="background:{C_RED};"></div>
    <div class="kpi-icon" style="background:#FCEEF1;">⚠️</div>
    <div class="kpi-lbl">Alto Risco</div>
    <div class="kpi-val" style="color:{C_RED};">{n_alto:,}</div>
    <div class="kpi-pct">{pct(n_alto)}</div>
  </div>
  <div class="kpi">
    <div class="kpi-top-bar" style="background:{C_AMB};"></div>
    <div class="kpi-icon" style="background:#FFFBEB;">🔶</div>
    <div class="kpi-lbl">Risco Médio</div>
    <div class="kpi-val" style="color:{C_AMB};">{n_medio:,}</div>
    <div class="kpi-pct">{pct(n_medio)}</div>
  </div>
  <div class="kpi">
    <div class="kpi-top-bar" style="background:{C_GRN};"></div>
    <div class="kpi-icon" style="background:#ECFDF5;">✅</div>
    <div class="kpi-lbl">Baixo Risco</div>
    <div class="kpi-val" style="color:{C_GRN};">{n_baixo:,}</div>
    <div class="kpi-pct">{pct(n_baixo)}</div>
  </div>
  <div class="kpi">
    <div class="kpi-top-bar" style="background:{C_SLT};"></div>
    <div class="kpi-icon" style="background:#F8FAFC;">⬜</div>
    <div class="kpi-lbl">Sem Classificação</div>
    <div class="kpi-val" style="color:{C_SLT};">{n_sem:,}</div>
    <div class="kpi-pct">{pct(n_sem)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

def sec(n, label):
    st.markdown(f"""
    <div class="sec">
      <span class="sec-num">{str(n).zfill(2)}</span>
      <span class="sec-label">{label}</span>
      <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEC 01 · DISTRIBUIÇÃO POR FACTOR
# ═══════════════════════════════════════════════════════════════════════════════
sec(1, "Distribuição de Risco por Factor")
col1, col2 = st.columns([2.3, 1])

with col1:
    st.markdown('<div class="card"><div class="card-title">Classificações empilhadas por Factor</div>', unsafe_allow_html=True)
    dist = df_filtrado.groupby(["DESCRICAO_FACTOR","CLASSIFICACAO"]).size().reset_index(name="TOTAL")
    dist["NIVEL"] = dist["CLASSIFICACAO"].apply(
        lambda x: "Sem Class." if x==9 else ("Alto (6-8)" if x>=6 else ("Médio (3-5)" if x>=3 else "Baixo (1-2)")))
    resumo = dist.groupby(["DESCRICAO_FACTOR","NIVEL"])["TOTAL"].sum().reset_index()
    cm = {"Alto (6-8)":C_RED, "Médio (3-5)":C_AMB, "Baixo (1-2)":C_GRN, "Sem Class.":C_SLT}
    fig1 = px.bar(resumo, x="TOTAL", y="DESCRICAO_FACTOR", color="NIVEL",
        color_discrete_map=cm, orientation="h", barmode="stack",
        labels={"TOTAL":"Classificações","DESCRICAO_FACTOR":"","NIVEL":"Nível"})
    ql(fig1, h=350, lt=6, legend_h=True)
    fig1.update_layout(
        yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor=AXIS,
                   tickfont=dict(size=11.5, color="#4A4440")),
        xaxis=dict(gridcolor=GRID),
        bargap=0.3,
    )
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="card-title">Composição geral</div>', unsafe_allow_html=True)
    pie = score_filtrado["NIVEL"].value_counts().reset_index()
    pie.columns = ["NIVEL","TOTAL"]
    fig2 = go.Figure(go.Pie(
        labels=pie["NIVEL"], values=pie["TOTAL"],
        hole=0.66,
        marker=dict(
            colors=[NIVEL_C.get(n,"#ccc") for n in pie["NIVEL"]],
            line=dict(color="white", width=3),
        ),
        textinfo="percent",
        textfont=dict(size=11.5, color="#1C1816"),
        hovertemplate="<b>%{label}</b><br>%{value} clientes · %{percent}<extra></extra>",
        direction="clockwise",
        sort=False,
    ))
    fig2.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:11px;color:#9C948E'>clientes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color="#1C1816", family="DM Mono"),
    )
    ql(fig2, h=350, lt=6)
    fig2.update_layout(
        showlegend=True,
        legend=dict(orientation="v", x=0.01, y=0.02,
                    font=dict(size=11, color="#4A4440")),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEC 02 · SEM CLASSIFICAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
sec(2, "Clientes sem Classificação (Valor 9) por Factor")

scf = (
    df_filtrado[df_filtrado["CLASSIFICACAO"]==9]
    .groupby("DESCRICAO_FACTOR")["CLIENTE_ID"].nunique()
    .reset_index(name="SEM").sort_values("SEM", ascending=True)
)
tpf = df_filtrado.groupby("DESCRICAO_FACTOR")["CLIENTE_ID"].nunique().reset_index(name="TOTAL")
scf = scf.merge(tpf, on="DESCRICAO_FACTOR")
scf["PERC"] = (scf["SEM"] / scf["TOTAL"] * 100).round(1)

col3, col4 = st.columns([2.3, 1])

with col3:
    st.markdown('<div class="card"><div class="card-title">Exposição por Factor — % sem classificação</div>', unsafe_allow_html=True)
    fig3 = go.Figure()
    # Background full bar (total)
    fig3.add_trace(go.Bar(
        x=scf["TOTAL"], y=scf["DESCRICAO_FACTOR"],
        orientation="h",
        marker=dict(color="#F4F1EC", line=dict(width=0)),
        hoverinfo="skip", showlegend=False, name="",
    ))
    fig3.add_trace(go.Bar(
        x=scf["SEM"], y=scf["DESCRICAO_FACTOR"],
        orientation="h",
        marker=dict(
            color=scf["PERC"],
            colorscale=[[0,"#FCE8EC"],[0.45,"#E8657A"],[1.0,C_RED]],
            showscale=True,
            colorbar=dict(
                title=dict(text="  %", font=dict(color=TEXT_C, size=10)),
                tickfont=dict(color=TEXT_C, size=10),
                bgcolor="rgba(0,0,0,0)", bordercolor=AXIS,
                thickness=12, len=0.8,
            ),
            line=dict(width=0),
        ),
        text=[f" {p}%" for p in scf["PERC"]],
        textposition="outside",
        textfont=dict(color="#9C948E", size=11, family="DM Mono"),
        hovertemplate="<b>%{y}</b><br>%{x} clientes sem classif. (%{text})<extra></extra>",
        name="Sem Classificação",
    ))
    ql(fig3, h=320, lt=6, lb=6)
    fig3.update_layout(
        barmode="overlay",
        xaxis_title="Nº de Clientes",
        yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor=AXIS, tickfont=dict(size=11, color="#4A4440")),
        showlegend=False,
        bargap=0.28,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card"><div class="card-title">Ranking por % exposta</div>', unsafe_allow_html=True)
    tbl = scf[["DESCRICAO_FACTOR","SEM","PERC"]].sort_values("PERC", ascending=False).copy()
    tbl.columns = ["Factor","S/ Class.","% Total"]
    tbl["% Total"] = tbl["% Total"].astype(str) + "%"
    st.dataframe(tbl.reset_index(drop=True), use_container_width=True, height=300)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEC 03 · RANKING DE CLIENTES
# ═══════════════════════════════════════════════════════════════════════════════
sec(3, "Ranking de Clientes por Risco")
col5, col6 = st.columns([1.55, 1])

with col5:
    st.markdown('<div class="card"><div class="card-title">Top clientes — Score Composto</div>', unsafe_allow_html=True)
    top_n = st.slider("", 10, 50, 20, format="%d clientes")
    top_df = (
        score_filtrado.nlargest(top_n, "SCORE_MEDIO")
        [["CLIENTE_ID","NOME","SEGMENTO","PROVINCIA","SCORE_MEDIO","NIVEL"]]
        .reset_index(drop=True)
    )
    top_df["SCORE_MEDIO"] = top_df["SCORE_MEDIO"].round(2)
    top_df.index += 1

    def cn(v):
        m = {
            "Alto":              "background-color:#FCEEF1;color:#C8102E;font-weight:600",
            "Médio":             "background-color:#FFFBEB;color:#B45309;font-weight:600",
            "Baixo":             "background-color:#ECFDF5;color:#065F46;font-weight:600",
            "Sem Classificação": "background-color:#F8FAFC;color:#64748B;font-weight:600",
        }
        return m.get(v, "")

    st.dataframe(
        top_df.style.applymap(cn, subset=["NIVEL"]),
        use_container_width=True, height=430,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="card"><div class="card-title">Distribuição por Segmento</div>', unsafe_allow_html=True)
    seg = score_filtrado.groupby(["SEGMENTO","NIVEL"]).size().reset_index(name="TOTAL")
    fig4 = px.bar(seg, x="SEGMENTO", y="TOTAL", color="NIVEL",
        color_discrete_map=NIVEL_C, barmode="group",
        labels={"TOTAL":"Clientes","SEGMENTO":""})
    ql(fig4, h=430, lt=6, legend_h=True)
    fig4.update_traces(marker_line_width=0)
    fig4.update_layout(
        bargap=0.22, bargroupgap=0.08,
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEC 04 · EVOLUÇÃO TEMPORAL
# ═══════════════════════════════════════════════════════════════════════════════
sec(4, "Evolução do Risco ao Longo do Tempo")
col7, col8 = st.columns(2)

with col7:
    st.markdown('<div class="card"><div class="card-title">Score Médio de Risco Trimestral</div>', unsafe_allow_html=True)
    evo = (
        classifs_df[
            classifs_df["CLIENTE_ID"].isin(clientes_filtrados) &
            classifs_df["DESCRICAO_FACTOR"].isin(factor_sel)
        ]
        .groupby("DATA")["CLASSIFICACAO"].mean()
        .reset_index(name="SCORE_MEDIO")
    )
    fig5 = go.Figure()
    fig5.add_hrect(y0=6, y1=evo["SCORE_MEDIO"].max()*1.08,
        fillcolor="rgba(200,16,46,0.04)", line_width=0)
    fig5.add_trace(go.Scatter(
        x=evo["DATA"], y=evo["SCORE_MEDIO"],
        mode="lines+markers",
        line=dict(color=C_RED, width=2.5, shape="spline"),
        marker=dict(size=8, color="white", line=dict(color=C_RED, width=2.5)),
        fill="tozeroy",
        fillcolor="rgba(200,16,46,0.06)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Score médio: %{y:.2f}<extra></extra>",
    ))
    fig5.add_hline(y=6, line_dash="dot", line_color=C_AMB, line_width=1.5,
        annotation_text=" Limite Alto Risco",
        annotation_font=dict(color=C_AMB, size=10, family="DM Mono"))
    ql(fig5, h=310, lt=10)
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col8:
    st.markdown('<div class="card"><div class="card-title">% Clientes em Alto Risco por Trimestre</div>', unsafe_allow_html=True)
    ea = (
        classifs_df[classifs_df["CLIENTE_ID"].isin(clientes_filtrados)]
        .groupby("DATA")
        .apply(lambda g: (g["CLASSIFICACAO"]>=6).mean() * 100)
        .reset_index(name="PERC")
    )
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=ea["DATA"], y=ea["PERC"],
        mode="lines+markers",
        line=dict(color=C_BLU, width=2.5, shape="spline"),
        marker=dict(size=8, color="white", line=dict(color=C_BLU, width=2.5)),
        fill="tozeroy",
        fillcolor="rgba(37,99,235,0.06)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f}% em alto risco<extra></extra>",
    ))
    ql(fig6, h=310, lt=10)
    fig6.update_layout(yaxis_ticksuffix="%", showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEC 05 · HEATMAP
# ═══════════════════════════════════════════════════════════════════════════════
sec(5, "Mapa de Calor — Factor × Classificação")

hd = df_filtrado.groupby(["DESCRICAO_FACTOR","CLASSIFICACAO"]).size().reset_index(name="TOTAL")
hp = hd.pivot(index="DESCRICAO_FACTOR", columns="CLASSIFICACAO", values="TOTAL").fillna(0)

fig7 = px.imshow(
    hp,
    color_continuous_scale=[
        [0.00, "#F4F1EC"],
        [0.20, "#FDE8EC"],
        [0.55, "#E8657A"],
        [0.78, "#C8102E"],
        [1.00, "#7A0A1B"],
    ],
    labels=dict(x="Classificação  (1 = Baixo · 9 = Sem Classif.)", y="", color="Clientes"),
    aspect="auto",
    height=340,
    text_auto=True,
)
ql(fig7, h=340, lt=10, lb=44)
fig7.update_traces(
    textfont=dict(size=11, color="rgba(28,24,22,0.7)", family="DM Mono"),
)
fig7.update_coloraxes(
    colorbar=dict(
        tickfont=dict(color=TEXT_C, size=10),
        title=dict(text="  N", font=dict(color=TEXT_C, size=10)),
        bgcolor="rgba(0,0,0,0)", bordercolor=AXIS,
        thickness=14, len=0.9,
    )
)
fig7.update_xaxes(
    tickvals=list(range(1,10)),
    ticktext=[str(i) for i in range(1,10)],
    side="bottom",
    tickfont=dict(size=12, family="DM Mono", color="#4A4440"),
)
fig7.update_yaxes(tickfont=dict(size=11, color="#4A4440"))
st.plotly_chart(fig7, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span>© 2025 Moza Banco <span class="footer-dot"></span> Risk Intelligence Platform</span>
  <span>KYC &nbsp;·&nbsp; AML &nbsp;·&nbsp; Dados demonstrativos</span>
</div>
""", unsafe_allow_html=True)
