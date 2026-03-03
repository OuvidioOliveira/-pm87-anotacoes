"""
Moza Banco · Risk Intelligence Platform
========================================
pip install streamlit plotly pandas numpy
streamlit run moza_risk_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Moza · Risk Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PREMIUM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --red:      #C8102E;
  --red-dim:  rgba(200,16,46,0.12);
  --red-glow: rgba(200,16,46,0.35);
  --bg:       #090B10;
  --surface:  #0E1118;
  --surface2: #131720;
  --border:   rgba(255,255,255,0.055);
  --border2:  rgba(255,255,255,0.09);
  --text:     #E2E8F0;
  --muted:    #4A5568;
  --muted2:   #718096;
  --amber:    #F6AD55;
  --green:    #68D391;
  --blue:     #63B3ED;
  --mono:     'JetBrains Mono', monospace;
  --sans:     'Syne', sans-serif;
}

html, body, [class*="css"] { font-family: var(--sans); }
.stApp { background: var(--bg); }
.main .block-container { padding: 0 2.4rem 3rem; max-width: 1460px; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #1E2535; border-radius: 3px; }

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0A0C12 0%, #0D1018 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: #A0AEC0 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: #111520 !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 8px !important;
}
[data-testid="stSidebar"] label {
  font-size: .72rem !important; letter-spacing: .09em;
  text-transform: uppercase; color: #4A5568 !important;
}

.hero {
  position: relative; padding: 36px 40px; margin: 0 0 32px;
  background:
    radial-gradient(ellipse 80% 60% at 100% 50%, rgba(200,16,46,0.18) 0%, transparent 70%),
    radial-gradient(ellipse 40% 80% at 0% 50%, rgba(200,16,46,0.06) 0%, transparent 60%),
    linear-gradient(135deg, #0E1118 0%, #111620 100%);
  border: 1px solid var(--border2); border-radius: 20px; overflow: hidden;
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background: repeating-linear-gradient(-55deg, transparent, transparent 48px,
    rgba(255,255,255,0.012) 48px, rgba(255,255,255,0.012) 50px);
  pointer-events: none;
}
.hero-eyebrow {
  font-size: .68rem; font-weight: 600; letter-spacing: .18em;
  text-transform: uppercase; color: var(--red); margin-bottom: 10px;
  display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before {
  content: ''; display: inline-block; width: 20px; height: 2px; background: var(--red);
}
.hero-title {
  font-size: 2rem; font-weight: 800; color: var(--text);
  letter-spacing: -.03em; line-height: 1.1; margin-bottom: 8px;
}
.hero-title span { color: var(--red); }
.hero-sub { font-size: .85rem; color: var(--muted2); font-family: var(--mono); font-weight: 300; }
.hero-badge {
  position: absolute; right: 40px; top: 50%; transform: translateY(-50%); text-align: right;
}
.hero-badge-val {
  font-family: var(--mono); font-size: 3.8rem; font-weight: 500;
  color: rgba(200,16,46,0.15); letter-spacing: -.06em; line-height: 1;
}
.hero-badge-lbl { font-size: .65rem; letter-spacing: .15em; text-transform: uppercase; color: var(--muted); }

.kpi-row { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 32px; }
.kpi {
  background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
  padding: 22px 22px 18px; position: relative; overflow: hidden;
  transition: border-color .25s, transform .2s; cursor: default;
}
.kpi:hover { border-color: var(--border2); transform: translateY(-1px); }
.kpi-accent { position: absolute; inset: 0 auto 0 0; width: 3px; border-radius: 16px 0 0 16px; }
.kpi-icon-wrap {
  position: absolute; top: 18px; right: 18px; width: 32px; height: 32px;
  border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem;
}
.kpi-lbl {
  font-size: .67rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 12px;
}
.kpi-val { font-family: var(--mono); font-size: 2.2rem; font-weight: 500; color: var(--text); line-height: 1; }
.kpi-pct { font-family: var(--mono); font-size: .78rem; color: var(--muted); margin-top: 7px; }

.sec { display: flex; align-items: center; gap: 12px; margin: 36px 0 18px; }
.sec-num { font-family: var(--mono); font-size: .65rem; color: var(--red); opacity: .7; width: 24px; }
.sec-label { font-size: .7rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--text); white-space: nowrap; }
.sec-line { flex: 1; height: 1px; background: linear-gradient(to right, rgba(255,255,255,0.07), transparent); }

.chart-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; height: 100%;
}
.chart-title {
  font-size: .7rem; font-weight: 700; letter-spacing: .11em; text-transform: uppercase;
  color: var(--muted2); margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
}
.chart-title::before { content: ''; display: inline-block; width: 4px; height: 14px; background: var(--red); border-radius: 2px; }

.brand { padding: 28px 20px 22px; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
.brand-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.brand-dot { width: 10px; height: 10px; background: var(--red); border-radius: 50%; box-shadow: 0 0 8px var(--red); }
.brand-name { font-size: 1.15rem; font-weight: 800; color: #E2E8F0 !important; letter-spacing: -.02em; }
.brand-sub { font-size: .67rem !important; color: #2D3748 !important; letter-spacing: .1em; text-transform: uppercase; }

div[data-testid="stPlotlyChart"] { border-radius: 12px; overflow: hidden; }

.footer {
  margin-top: 56px; padding: 20px 0; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}
.footer span { font-family: var(--mono); font-size: .72rem; color: #1E2535; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ────────────────────────────────────────────────────────────────
BG    = "#090B10"
SURF  = "#0E1118"
GRID  = "#131720"
AXIS  = "#1A1F2E"
TEXT  = "#8896AA"
C_RED   = "#C8102E"
C_AMBER = "#F6AD55"
C_GREEN = "#68D391"
C_BLUE  = "#63B3ED"
C_GRAY  = "#4A5568"
NIVEL_C = {"Alto":C_RED,"Médio":C_AMBER,"Baixo":C_GREEN,"Sem Classificação":C_GRAY}

def ql(fig, h=360, lt=30, lb=10):
    fig.update_layout(
        height=h, paper_bgcolor=BG, plot_bgcolor=SURF,
        font=dict(family="Syne", color=TEXT, size=11),
        margin=dict(l=6, r=6, t=lt, b=lb),
        xaxis=dict(gridcolor=GRID, linecolor=AXIS, tickcolor=AXIS, zerolinecolor=GRID, tickfont=dict(size=10.5)),
        yaxis=dict(gridcolor=GRID, linecolor=AXIS, tickcolor=AXIS, zerolinecolor=GRID, tickfont=dict(size=10.5)),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=10.5)),
        hoverlabel=dict(bgcolor="#111520", bordercolor="#1E2535",
                        font_color="#E2E8F0", font_family="JetBrains Mono", font_size=12),
    )
    return fig

# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    np.random.seed(42)
    factores = pd.DataFrame({
        "FACTOR_DE_RISCO": [6,8,5,2,3,7,4,1],
        "DESCRICAO_DO_FACTOR": [
            "Produtos Atribuídos","Canais de Distribuição","Origem dos Fundos",
            "Natureza de Negócio/Profissão","Modo de Relacionamento com Banco",
            "Localização Geográfica","Perfil Transacional","Natureza do Cliente",
        ]
    })
    dpf = {
        1:["Particular residente","Empresarial PME","Corporativo nacional","Corporativo internacional","Entidade pública","ONG/Associação","Embaixada/Diplomata","Político/PEP"],
        2:["Comércio formal","Serviços profissionais","Indústria/Produção","Agricultura","Construção civil","Sector financeiro","Actividades extractivas","Negócio de alto risco"],
        3:["Sucursal presencial","Agência Express","Internet Banking","Mobile Banking","Correspondente bancário","Broker","Plataforma digital terceira","Representante exclusivo"],
        4:["Transacções de baixo valor","Uso regular cartão débito","Transferências nacionais ocasionais","Transferências int. esporádicas","Alto volume transaccional","Transacções em cash frequentes","Padrão irregular","Actividade suspeita reportada"],
        5:["Salários/Rendimentos","Poupanças pessoais","Herança","Venda de imóveis","Dividendos/Investimentos","Empréstimos externos","Origem desconhecida","Fundos de alto risco"],
        6:["Conta poupança","Conta corrente","Cartão de crédito","Crédito hipotecário","Leasing","Câmbio","Derivados","Offshore"],
        7:["Maputo cidade","Maputo província","Gaza/Inhambane","Sofala/Manica","Tete/Zambézia","Nampula","Niassa/Cabo Delgado","País de alto risco GAFI"],
        8:["Balcão principal","ATM","POS/Terminal","Internet Banking directo","App Mobile","Agente bancário","API Fintech","Plataforma não regulada"],
    }
    criterios = []
    for fid, fdesc in zip(factores["FACTOR_DE_RISCO"], factores["DESCRICAO_DO_FACTOR"]):
        for cls in range(1, 9):
            criterios.append({"FACTOR_ID":fid,"DESCRICAO_DO_FACTOR":fdesc,"CLASSIFICACAO":cls,
                "DESCRICAO_CRITERIO":dpf[fid][cls-1],
                "NIVEL_RISCO":"Alto" if cls>=6 else ("Médio" if cls>=3 else "Baixo")})
    criterios_df = pd.DataFrame(criterios)
    n = 300
    clientes = pd.DataFrame({
        "CLIENTE_ID": [f"MZ{str(i).zfill(5)}" for i in range(1,n+1)],
        "NOME":       [f"Cliente_{str(i).zfill(4)}" for i in range(1,n+1)],
        "SEGMENTO":   np.random.choice(["Particular","PME","Corporativo","Institucional"],n,p=[0.5,0.25,0.15,0.10]),
        "PROVINCIA":  np.random.choice(["Maputo","Sofala","Nampula","Zambézia","Tete","Gaza"],n),
        "DATA_ABERTURA": [(datetime(2018,1,1)+timedelta(days=int(x))).strftime("%Y-%m-%d")
                          for x in np.random.randint(0,2000,n)],
    })
    trimestres = pd.date_range("2023-01-01","2025-01-01",freq="QS")
    classifs = []
    for _, cliente in clientes.iterrows():
        for _, factor in factores.iterrows():
            base = np.random.choice(range(1,10),p=[0.12,0.12,0.12,0.11,0.10,0.09,0.08,0.07,0.19])
            for t in trimestres:
                drift = int(np.clip(base+np.random.randint(-1,2),1,9))
                classifs.append({
                    "CLIENTE_ID":       cliente["CLIENTE_ID"],
                    "FACTOR_ID":        factor["FACTOR_DE_RISCO"],
                    "DESCRICAO_FACTOR": factor["DESCRICAO_DO_FACTOR"],
                    "CLASSIFICACAO":    drift,
                    "TRIMESTRE":        t.strftime("%Y-T%q"),
                    "DATA":             t,
                    "SEGMENTO":         cliente["SEGMENTO"],
                    "PROVINCIA":        cliente["PROVINCIA"],
                })
                base = drift
    return factores, criterios_df, clientes, pd.DataFrame(classifs)

factores, criterios_df, clientes, classifs_df = gerar_dados()

ultimo_trim = classifs_df["TRIMESTRE"].max()
df_ultimo   = classifs_df[classifs_df["TRIMESTRE"]==ultimo_trim].copy()
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
      <div class="brand-logo">
        <div class="brand-dot"></div>
        <div class="brand-name">MOZA</div>
      </div>
      <div class="brand-sub">Risk Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:#2D3748;margin-bottom:14px;">Filtros de Análise</p>', unsafe_allow_html=True)
    segmento_sel  = st.multiselect("Segmento",  options=clientes["SEGMENTO"].unique(),              default=clientes["SEGMENTO"].unique())
    provincia_sel = st.multiselect("Província",  options=clientes["PROVINCIA"].unique(),             default=clientes["PROVINCIA"].unique())
    factor_sel    = st.multiselect("Factor de Risco", options=factores["DESCRICAO_DO_FACTOR"].tolist(), default=factores["DESCRICAO_DO_FACTOR"].tolist())
    nivel_sel     = st.multiselect("Nível de Risco", options=["Baixo","Médio","Alto","Sem Classificação"], default=["Baixo","Médio","Alto","Sem Classificação"])
    st.markdown(f"""
    <div style="margin-top:32px;padding:16px;background:#0A0C12;border:1px solid rgba(255,255,255,0.05);border-radius:10px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#2D3748;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px;">Período activo</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.85rem;color:#4A5568;">{ultimo_trim}</div>
    </div>""", unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────────────────────────
clientes_filtrados = clientes[
    clientes["SEGMENTO"].isin(segmento_sel) & clientes["PROVINCIA"].isin(provincia_sel)
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
pct = lambda n: f"{n/max(total,1)*100:.1f}% do total"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">Análise de Risco KYC · AML</div>
  <div class="hero-title">Risk <span>Intelligence</span><br>Dashboard</div>
  <div class="hero-sub">Moza Banco · {ultimo_trim} · {total:,} clientes analisados</div>
  <div class="hero-badge">
    <div class="hero-badge-val">{n_alto}</div>
    <div class="hero-badge-lbl">clientes alto risco</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-accent" style="background:{C_BLUE};"></div>
    <div class="kpi-icon-wrap" style="background:rgba(99,179,237,.1);">👥</div>
    <div class="kpi-lbl">Total Clientes</div>
    <div class="kpi-val">{total:,}</div>
    <div class="kpi-pct">{len(segmento_sel)} seg. · {len(provincia_sel)} prov.</div>
  </div>
  <div class="kpi">
    <div class="kpi-accent" style="background:{C_RED};"></div>
    <div class="kpi-icon-wrap" style="background:rgba(200,16,46,.1);">⚠️</div>
    <div class="kpi-lbl">Alto Risco</div>
    <div class="kpi-val">{n_alto:,}</div>
    <div class="kpi-pct">{pct(n_alto)}</div>
  </div>
  <div class="kpi">
    <div class="kpi-accent" style="background:{C_AMBER};"></div>
    <div class="kpi-icon-wrap" style="background:rgba(246,173,85,.1);">🔶</div>
    <div class="kpi-lbl">Risco Médio</div>
    <div class="kpi-val">{n_medio:,}</div>
    <div class="kpi-pct">{pct(n_medio)}</div>
  </div>
  <div class="kpi">
    <div class="kpi-accent" style="background:{C_GREEN};"></div>
    <div class="kpi-icon-wrap" style="background:rgba(104,211,145,.1);">✅</div>
    <div class="kpi-lbl">Baixo Risco</div>
    <div class="kpi-val">{n_baixo:,}</div>
    <div class="kpi-pct">{pct(n_baixo)}</div>
  </div>
  <div class="kpi">
    <div class="kpi-accent" style="background:{C_GRAY};"></div>
    <div class="kpi-icon-wrap" style="background:rgba(74,85,104,.1);">⬜</div>
    <div class="kpi-lbl">Sem Classificação</div>
    <div class="kpi-val">{n_sem:,}</div>
    <div class="kpi-pct">{pct(n_sem)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

def sec(n, label):
    st.markdown(f"""<div class="sec">
      <span class="sec-num">{str(n).zfill(2)}</span>
      <span class="sec-label">{label}</span>
      <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)

# ── SEC 01 ────────────────────────────────────────────────────────────────────
sec(1, "Distribuição de Risco por Factor")
col1, col2 = st.columns([2.3, 1])

with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">Classificações por Factor</div>', unsafe_allow_html=True)
    dist = df_filtrado.groupby(["DESCRICAO_FACTOR","CLASSIFICACAO"]).size().reset_index(name="TOTAL")
    dist["NIVEL"] = dist["CLASSIFICACAO"].apply(
        lambda x: "Sem Class." if x==9 else ("Alto (6-8)" if x>=6 else ("Médio (3-5)" if x>=3 else "Baixo (1-2)")))
    resumo = dist.groupby(["DESCRICAO_FACTOR","NIVEL"])["TOTAL"].sum().reset_index()
    cm = {"Alto (6-8)":C_RED,"Médio (3-5)":C_AMBER,"Baixo (1-2)":C_GREEN,"Sem Class.":C_GRAY}
    fig1 = px.bar(resumo, x="TOTAL", y="DESCRICAO_FACTOR", color="NIVEL",
        color_discrete_map=cm, orientation="h", barmode="stack",
        labels={"TOTAL":"Classificações","DESCRICAO_FACTOR":"","NIVEL":"Nível"})
    ql(fig1, h=340, lt=6)
    fig1.update_layout(
        yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor=AXIS, tickfont=dict(size=11.5, color="#8896AA")),
        xaxis=dict(gridcolor=GRID),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, font=dict(size=10.5)),
        bargap=0.28,
    )
    fig1.update_traces(marker_line_width=0, marker_opacity=0.9)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-title">Composição Geral</div>', unsafe_allow_html=True)
    pie = score_filtrado["NIVEL"].value_counts().reset_index(); pie.columns=["NIVEL","TOTAL"]
    fig2 = go.Figure(go.Pie(
        labels=pie["NIVEL"], values=pie["TOTAL"], hole=0.68,
        marker=dict(colors=[NIVEL_C.get(n,"#999") for n in pie["NIVEL"]],
                    line=dict(color=BG, width=4)),
        textinfo="percent", textfont=dict(size=11, color="#E2E8F0"),
        hovertemplate="<b>%{label}</b><br>%{value} clientes · %{percent}<extra></extra>",
        direction="clockwise",
    ))
    fig2.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:11px'>clientes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color="#E2E8F0", family="JetBrains Mono"),
    )
    ql(fig2, h=340, lt=6)
    fig2.update_layout(showlegend=True,
        legend=dict(orientation="v", x=-0.05, y=0, font=dict(size=10.5)))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── SEC 02 ────────────────────────────────────────────────────────────────────
sec(2, "Clientes sem Classificação (Valor 9) por Factor")
scf = (df_filtrado[df_filtrado["CLASSIFICACAO"]==9]
       .groupby("DESCRICAO_FACTOR")["CLIENTE_ID"].nunique()
       .reset_index(name="SEM").sort_values("SEM", ascending=True))
tpf = df_filtrado.groupby("DESCRICAO_FACTOR")["CLIENTE_ID"].nunique().reset_index(name="TOTAL")
scf = scf.merge(tpf, on="DESCRICAO_FACTOR")
scf["PERC"] = (scf["SEM"]/scf["TOTAL"]*100).round(1)

col3, col4 = st.columns([2.3, 1])
with col3:
    st.markdown('<div class="chart-card"><div class="chart-title">Exposição por Factor</div>', unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=scf["SEM"], y=scf["DESCRICAO_FACTOR"], orientation="h",
        marker=dict(color=scf["PERC"],
            colorscale=[[0,"#1A1F2E"],[0.5,"#3D2B2B"],[1.0,C_RED]],
            showscale=True,
            colorbar=dict(title="  %", titlefont=dict(color=TEXT, size=10),
                tickfont=dict(color=TEXT, size=10), bgcolor="rgba(0,0,0,0)",
                bordercolor=AXIS, thickness=14, len=0.85),
            line=dict(width=0)),
        text=[f" {p}%" for p in scf["PERC"]], textposition="outside",
        textfont=dict(color="#5A6478", size=11, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x} clientes · %{text}<extra></extra>",
    ))
    ql(fig3, h=310, lt=6, lb=6)
    fig3.update_layout(xaxis_title="Nº de Clientes",
        yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor=AXIS, tickfont=dict(size=11)))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><div class="chart-title">Ranking</div>', unsafe_allow_html=True)
    tbl = scf[["DESCRICAO_FACTOR","SEM","PERC"]].sort_values("PERC",ascending=False).copy()
    tbl.columns = ["Factor","S/ Class.","% Total"]
    tbl["% Total"] = tbl["% Total"].astype(str)+"%"
    st.dataframe(tbl.reset_index(drop=True), use_container_width=True, height=285)
    st.markdown('</div>', unsafe_allow_html=True)

# ── SEC 03 ────────────────────────────────────────────────────────────────────
sec(3, "Ranking de Clientes por Risco")
col5, col6 = st.columns([1.6, 1])

with col5:
    st.markdown('<div class="chart-card"><div class="chart-title">Top Clientes — Score Composto</div>', unsafe_allow_html=True)
    top_n = st.slider("", 10, 50, 20, format="%d clientes")
    top_df = (score_filtrado.nlargest(top_n,"SCORE_MEDIO")
              [["CLIENTE_ID","NOME","SEGMENTO","PROVINCIA","SCORE_MEDIO","NIVEL"]]
              .reset_index(drop=True))
    top_df["SCORE_MEDIO"] = top_df["SCORE_MEDIO"].round(2)
    top_df.index += 1
    def cn(v):
        m = {"Alto":"background-color:rgba(200,16,46,.18);color:#FC8181",
             "Médio":"background-color:rgba(246,173,85,.15);color:#FBD07C",
             "Baixo":"background-color:rgba(104,211,145,.15);color:#9AE6B4",
             "Sem Classificação":"background-color:rgba(74,85,104,.15);color:#718096"}
        return m.get(v,"")
    st.dataframe(top_df.style.applymap(cn, subset=["NIVEL"]), use_container_width=True, height=420)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-card"><div class="chart-title">Risco por Segmento</div>', unsafe_allow_html=True)
    seg = score_filtrado.groupby(["SEGMENTO","NIVEL"]).size().reset_index(name="TOTAL")
    fig4 = px.bar(seg, x="SEGMENTO", y="TOTAL", color="NIVEL",
        color_discrete_map=NIVEL_C, barmode="group",
        labels={"TOTAL":"Clientes","SEGMENTO":""})
    ql(fig4, h=420, lt=6)
    fig4.update_traces(marker_line_width=0, marker_opacity=0.88)
    fig4.update_layout(bargap=0.22, bargroupgap=0.08,
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── SEC 04 ────────────────────────────────────────────────────────────────────
sec(4, "Evolução do Risco ao Longo do Tempo")
col7, col8 = st.columns(2)

with col7:
    st.markdown('<div class="chart-card"><div class="chart-title">Score Médio Trimestral</div>', unsafe_allow_html=True)
    evo = (classifs_df[classifs_df["CLIENTE_ID"].isin(clientes_filtrados) &
            classifs_df["DESCRICAO_FACTOR"].isin(factor_sel)]
           .groupby("DATA")["CLASSIFICACAO"].mean().reset_index(name="SCORE_MEDIO"))
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=evo["DATA"], y=evo["SCORE_MEDIO"], mode="lines+markers",
        line=dict(color=C_RED, width=2.5, shape="spline"),
        marker=dict(size=8, color=C_RED, line=dict(color=BG, width=2.5)),
        fill="tozeroy", fillcolor="rgba(200,16,46,0.07)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Score médio: %{y:.2f}<extra></extra>",
    ))
    fig5.add_hrect(y0=6, y1=evo["SCORE_MEDIO"].max()*1.1,
        fillcolor="rgba(200,16,46,0.04)", line_width=0)
    fig5.add_hline(y=6, line_dash="dot", line_color=C_AMBER, line_width=1.5,
        annotation_text="  Alto risco",
        annotation_font=dict(color=C_AMBER, size=10, family="JetBrains Mono"))
    ql(fig5, h=310, lt=10)
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col8:
    st.markdown('<div class="chart-card"><div class="chart-title">% Clientes em Alto Risco (Score >= 6)</div>', unsafe_allow_html=True)
    ea = (classifs_df[classifs_df["CLIENTE_ID"].isin(clientes_filtrados)]
          .groupby("DATA").apply(lambda g:(g["CLASSIFICACAO"]>=6).mean()*100)
          .reset_index(name="PERC"))
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=ea["DATA"], y=ea["PERC"], mode="lines+markers",
        line=dict(color=C_BLUE, width=2.5, shape="spline"),
        marker=dict(size=8, color=C_BLUE, line=dict(color=BG, width=2.5)),
        fill="tozeroy", fillcolor="rgba(99,179,237,0.07)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f}% em alto risco<extra></extra>",
    ))
    ql(fig6, h=310, lt=10)
    fig6.update_layout(yaxis_ticksuffix="%", showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── SEC 05 ────────────────────────────────────────────────────────────────────
sec(5, "Mapa de Calor — Factor x Classificacao")
hd = df_filtrado.groupby(["DESCRICAO_FACTOR","CLASSIFICACAO"]).size().reset_index(name="TOTAL")
hp = hd.pivot(index="DESCRICAO_FACTOR", columns="CLASSIFICACAO", values="TOTAL").fillna(0)
fig7 = px.imshow(hp,
    color_continuous_scale=[[0.0,"#0E1118"],[0.25,"#111A2A"],[0.55,"#2D1B1B"],[0.78,"#7A1020"],[1.0,C_RED]],
    labels=dict(x="Classificacao (1=Baixo · 9=Sem Class.)", y="", color="Clientes"),
    aspect="auto", height=340, text_auto=True)
ql(fig7, h=340, lt=10, lb=40)
fig7.update_traces(textfont=dict(size=10.5, color="rgba(255,255,255,0.6)", family="JetBrains Mono"))
fig7.update_coloraxes(colorbar=dict(
    tickfont=dict(color=TEXT, size=10), title=dict(text="  N", font=dict(color=TEXT, size=10)),
    bgcolor="rgba(0,0,0,0)", bordercolor=AXIS, thickness=14, len=0.9))
fig7.update_xaxes(tickvals=list(range(1,10)), ticktext=[str(i) for i in range(1,10)],
    side="bottom", tickfont=dict(size=12, family="JetBrains Mono"))
fig7.update_yaxes(tickfont=dict(size=11))
st.plotly_chart(fig7, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span>© 2025 Moza Banco · Risk Intelligence Platform</span>
  <span>KYC · AML · Dados demonstrativos</span>
</div>
""", unsafe_allow_html=True)
