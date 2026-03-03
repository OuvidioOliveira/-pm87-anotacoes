"""
Dashboard de Análise de Risco de Clientes — Moza Banco
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
from datetime import datetime, timedelta

st.set_page_config(page_title="Moza · Risk Intelligence", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#0D0F14;}
.main .block-container{padding:2rem 2.5rem 3rem;max-width:1400px;}
[data-testid="stSidebar"]{background:#111318!important;border-right:1px solid #1E2028;}
[data-testid="stSidebar"] *{color:#C8CDD8!important;}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#1A1D24!important;border-color:#2A2D36!important;}
::-webkit-scrollbar{width:6px;}::-webkit-scrollbar-track{background:#111318;}::-webkit-scrollbar-thumb{background:#2A2D36;border-radius:3px;}
.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:28px;}
.kpi-card{background:#13151C;border:1px solid #1E2028;border-radius:14px;padding:20px 22px;position:relative;overflow:hidden;transition:border-color .2s;}
.kpi-card:hover{border-color:#2E3140;}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:14px 14px 0 0;}
.kpi-card.total::before{background:#4A90E2;}.kpi-card.alto::before{background:#C8102E;}.kpi-card.medio::before{background:#F59E0B;}.kpi-card.baixo::before{background:#10B981;}.kpi-card.sem::before{background:#6B7280;}
.kpi-label{font-size:.72rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;margin-bottom:10px;}
.kpi-value{font-size:2.1rem;font-weight:700;color:#F0F2F7;line-height:1;font-family:'DM Mono',monospace;}
.kpi-sub{font-size:.78rem;color:#4A5060;margin-top:6px;font-family:'DM Mono',monospace;}
.kpi-icon{position:absolute;top:18px;right:18px;font-size:1.4rem;opacity:.4;}
.sec-header{display:flex;align-items:center;gap:10px;margin:32px 0 16px;}
.sec-header-line{flex:1;height:1px;background:linear-gradient(to right,#1E2028,transparent);}
.sec-header-text{font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#C8102E;white-space:nowrap;}
.sec-header-dot{width:6px;height:6px;border-radius:50%;background:#C8102E;flex-shrink:0;}
.sidebar-logo{padding:24px 16px 20px;border-bottom:1px solid #1E2028;margin-bottom:24px;}
.sidebar-logo-text{font-size:1.3rem;font-weight:700;color:#F0F2F7!important;letter-spacing:-.01em;}
.sidebar-logo-sub{font-size:.72rem;color:#4A5060!important;letter-spacing:.06em;text-transform:uppercase;margin-top:2px;}
div[data-testid="stPlotlyChart"]{border-radius:14px;overflow:hidden;}
</style>
""", unsafe_allow_html=True)

BG_CHART="#13151C"; BG_PAPER="#13151C"; GRID_CLR="#1A1D24"; TEXT_CLR="#8891A4"; AXIS_CLR="#2A2D36"
COR_ALTO="#C8102E"; COR_MEDIO="#F59E0B"; COR_BAIXO="#10B981"; COR_SEM="#6B7280"; COR_TOTAL="#4A90E2"
NIVEL_COLORS={"Alto":COR_ALTO,"Médio":COR_MEDIO,"Baixo":COR_BAIXO,"Sem Classificação":COR_SEM}

def chart_layout(fig,height=360,title="",margin=(10,10,30,10)):
    fig.update_layout(height=height,paper_bgcolor=BG_PAPER,plot_bgcolor=BG_CHART,
        font=dict(family="DM Sans",color=TEXT_CLR,size=12),
        title=dict(text=title,font=dict(size=12,color="#8891A4"),x=0,xanchor="left") if title else None,
        margin=dict(l=margin[0],r=margin[1],t=margin[2],b=margin[3]),
        xaxis=dict(gridcolor=GRID_CLR,linecolor=AXIS_CLR,tickcolor=AXIS_CLR,zerolinecolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR,linecolor=AXIS_CLR,tickcolor=AXIS_CLR,zerolinecolor=GRID_CLR),
        legend=dict(bgcolor="rgba(0,0,0,0)",bordercolor="rgba(0,0,0,0)",font=dict(color=TEXT_CLR)),
        hoverlabel=dict(bgcolor="#1A1D24",bordercolor="#2A2D36",font_color="#F0F2F7",font_family="DM Sans"))
    return fig

@st.cache_data
def gerar_dados():
    np.random.seed(42)
    factores=pd.DataFrame({"FACTOR_DE_RISCO":[6,8,5,2,3,7,4,1],"DESCRICAO_DO_FACTOR":["Produtos Atribuídos","Canais de Distribuição","Origem dos Fundos","Natureza de Negócio/Profissão","Modo de Relacionamento com Banco","Localização Geográfica","Perfil Transacional","Natureza do Cliente"]})
    dpf={1:["Particular residente","Empresarial PME","Corporativo nacional","Corporativo internacional","Entidade pública","ONG/Associação","Embaixada/Diplomata","Político/PEP"],2:["Comércio formal","Serviços profissionais","Indústria/Produção","Agricultura","Construção civil","Sector financeiro","Actividades extractivas","Negócio de alto risco"],3:["Sucursal presencial","Agência Express","Internet Banking","Mobile Banking","Correspondente bancário","Broker","Plataforma digital terceira","Representante exclusivo"],4:["Transacções de baixo valor","Uso regular cartão débito","Transferências nacionais ocasionais","Transferências int. esporádicas","Alto volume transaccional","Transacções em cash frequentes","Padrão irregular","Actividade suspeita reportada"],5:["Salários/Rendimentos","Poupanças pessoais","Herança","Venda de imóveis","Dividendos/Investimentos","Empréstimos externos","Origem desconhecida","Fundos de alto risco"],6:["Conta poupança","Conta corrente","Cartão de crédito","Crédito hipotecário","Leasing","Câmbio","Derivados","Offshore"],7:["Maputo cidade","Maputo província","Gaza/Inhambane","Sofala/Manica","Tete/Zambézia","Nampula","Niassa/Cabo Delgado","País de alto risco GAFI"],8:["Balcão principal","ATM","POS/Terminal","Internet Banking directo","App Mobile","Agente bancário","API Fintech","Plataforma não regulada"]}
    criterios=[]
    for fid,fdesc in zip(factores["FACTOR_DE_RISCO"],factores["DESCRICAO_DO_FACTOR"]):
        for cls in range(1,9):
            criterios.append({"FACTOR_ID":fid,"DESCRICAO_DO_FACTOR":fdesc,"CLASSIFICACAO":cls,"DESCRICAO_CRITERIO":dpf[fid][cls-1],"NIVEL_RISCO":"Alto" if cls>=6 else("Médio" if cls>=3 else "Baixo")})
    criterios_df=pd.DataFrame(criterios)
    n=300; segmentos=["Particular","PME","Corporativo","Institucional"]; provincias=["Maputo","Sofala","Nampula","Zambézia","Tete","Gaza"]
    clientes=pd.DataFrame({"CLIENTE_ID":[f"MZ{str(i).zfill(5)}" for i in range(1,n+1)],"NOME":[f"Cliente_{str(i).zfill(4)}" for i in range(1,n+1)],"SEGMENTO":np.random.choice(segmentos,n,p=[0.5,0.25,0.15,0.10]),"PROVINCIA":np.random.choice(provincias,n),"DATA_ABERTURA":[(datetime(2018,1,1)+timedelta(days=int(x))).strftime("%Y-%m-%d") for x in np.random.randint(0,2000,n)]})
    trimestres=pd.date_range("2023-01-01","2025-01-01",freq="QS")
    classifs=[]
    for _,cliente in clientes.iterrows():
        for _,factor in factores.iterrows():
            base=np.random.choice(range(1,10),p=[0.12,0.12,0.12,0.11,0.10,0.09,0.08,0.07,0.19])
            for t in trimestres:
                drift=int(np.clip(base+np.random.randint(-1,2),1,9))
                classifs.append({"CLIENTE_ID":cliente["CLIENTE_ID"],"FACTOR_ID":factor["FACTOR_DE_RISCO"],"DESCRICAO_FACTOR":factor["DESCRICAO_DO_FACTOR"],"CLASSIFICACAO":drift,"TRIMESTRE":t.strftime("%Y-T%q"),"DATA":t,"SEGMENTO":cliente["SEGMENTO"],"PROVINCIA":cliente["PROVINCIA"]})
                base=drift
    return factores,criterios_df,clientes,pd.DataFrame(classifs)

factores,criterios_df,clientes,classifs_df=gerar_dados()
ultimo_trim=classifs_df["TRIMESTRE"].max()
df_ultimo=classifs_df[classifs_df["TRIMESTRE"]==ultimo_trim].copy()
score_cliente=(df_ultimo.groupby("CLIENTE_ID")["CLASSIFICACAO"].mean().reset_index().rename(columns={"CLASSIFICACAO":"SCORE_MEDIO"}).merge(clientes,on="CLIENTE_ID"))
score_cliente["NIVEL"]=score_cliente["SCORE_MEDIO"].apply(lambda x:"Sem Classificação" if x>=8.5 else("Alto" if x>=6 else("Médio" if x>=3 else "Baixo")))

with st.sidebar:
    st.markdown('<div class="sidebar-logo"><div class="sidebar-logo-text">🏦 Moza Banco</div><div class="sidebar-logo-sub">Risk Intelligence Platform</div></div>', unsafe_allow_html=True)
    st.markdown("**FILTROS**")
    segmento_sel=st.multiselect("Segmento",options=clientes["SEGMENTO"].unique(),default=clientes["SEGMENTO"].unique())
    provincia_sel=st.multiselect("Província",options=clientes["PROVINCIA"].unique(),default=clientes["PROVINCIA"].unique())
    factor_sel=st.multiselect("Factor de Risco",options=factores["DESCRICAO_DO_FACTOR"].tolist(),default=factores["DESCRICAO_DO_FACTOR"].tolist())
    nivel_sel=st.multiselect("Nível de Risco",options=["Baixo","Médio","Alto","Sem Classificação"],default=["Baixo","Médio","Alto","Sem Classificação"])
    st.markdown("---")
    st.caption(f"📅 Período: **{ultimo_trim}**")
    st.caption(f"🗃️ Base: **{len(clientes):,}** clientes · **8** factores")

clientes_filtrados=clientes[clientes["SEGMENTO"].isin(segmento_sel)&clientes["PROVINCIA"].isin(provincia_sel)]["CLIENTE_ID"]
df_filtrado=df_ultimo[df_ultimo["CLIENTE_ID"].isin(clientes_filtrados)&df_ultimo["DESCRICAO_FACTOR"].isin(factor_sel)]
score_filtrado=score_cliente[score_cliente["CLIENTE_ID"].isin(clientes_filtrados)&score_cliente["NIVEL"].isin(nivel_sel)]

st.markdown("""<div style="margin-bottom:28px;"><h1 style="font-family:'DM Sans',sans-serif;font-size:1.8rem;font-weight:700;color:#F0F2F7;margin:0;letter-spacing:-.02em;">Risk Intelligence <span style="color:#C8102E;">·</span> Análise de Clientes</h1><p style="color:#4A5060;font-size:.88rem;margin:6px 0 0;letter-spacing:.02em;">Monitorização KYC/AML · 8 Factores de Risco · Dados demonstrativos</p></div>""", unsafe_allow_html=True)

total=score_filtrado["CLIENTE_ID"].nunique(); alto=(score_filtrado["NIVEL"]=="Alto").sum(); medio=(score_filtrado["NIVEL"]=="Médio").sum(); baixo=(score_filtrado["NIVEL"]=="Baixo").sum(); sem=(score_filtrado["NIVEL"]=="Sem Classificação").sum()
pct=lambda v:f"{v/max(total,1)*100:.1f}% dos clientes"
st.markdown(f"""<div class="kpi-grid"><div class="kpi-card total"><div class="kpi-icon">👥</div><div class="kpi-label">Total Clientes</div><div class="kpi-value">{total:,}</div><div class="kpi-sub">carteira activa</div></div><div class="kpi-card alto"><div class="kpi-icon">🔴</div><div class="kpi-label">Alto Risco</div><div class="kpi-value">{alto:,}</div><div class="kpi-sub">{pct(alto)}</div></div><div class="kpi-card medio"><div class="kpi-icon">🟡</div><div class="kpi-label">Risco Médio</div><div class="kpi-value">{medio:,}</div><div class="kpi-sub">{pct(medio)}</div></div><div class="kpi-card baixo"><div class="kpi-icon">🟢</div><div class="kpi-label">Baixo Risco</div><div class="kpi-value">{baixo:,}</div><div class="kpi-sub">{pct(baixo)}</div></div><div class="kpi-card sem"><div class="kpi-icon">⚪</div><div class="kpi-label">Sem Classific.</div><div class="kpi-value">{sem:,}</div><div class="kpi-sub">{pct(sem)}</div></div></div>""", unsafe_allow_html=True)

def sec(label):
    st.markdown(f'<div class="sec-header"><div class="sec-header-dot"></div><div class="sec-header-text">{label}</div><div class="sec-header-line"></div></div>', unsafe_allow_html=True)

# SEC 1
sec("Distribuição de Risco por Factor")
col1,col2=st.columns([2.2,1])
with col1:
    dist=df_filtrado.groupby(["DESCRICAO_FACTOR","CLASSIFICACAO"]).size().reset_index(name="TOTAL")
    dist["NIVEL"]=dist["CLASSIFICACAO"].apply(lambda x:"Sem Class." if x==9 else("Alto (6-8)" if x>=6 else("Médio (3-5)" if x>=3 else "Baixo (1-2)")))
    resumo=dist.groupby(["DESCRICAO_FACTOR","NIVEL"])["TOTAL"].sum().reset_index()
    fig1=px.bar(resumo,x="TOTAL",y="DESCRICAO_FACTOR",color="NIVEL",color_discrete_map={"Alto (6-8)":COR_ALTO,"Médio (3-5)":COR_MEDIO,"Baixo (1-2)":COR_BAIXO,"Sem Class.":COR_SEM},orientation="h",barmode="stack",labels={"TOTAL":"Classificações","DESCRICAO_FACTOR":"","NIVEL":"Nível"})
    chart_layout(fig1,height=340,margin=(4,10,10,10))
    fig1.update_layout(yaxis=dict(gridcolor="rgba(0,0,0,0)",linecolor=AXIS_CLR,tickfont=dict(size=11)),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0))
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1,use_container_width=True)
with col2:
    pie_data=score_filtrado["NIVEL"].value_counts().reset_index(); pie_data.columns=["NIVEL","TOTAL"]
    fig2=go.Figure(go.Pie(labels=pie_data["NIVEL"],values=pie_data["TOTAL"],hole=0.65,marker=dict(colors=[NIVEL_COLORS.get(n,"#999") for n in pie_data["NIVEL"]],line=dict(color=BG_CHART,width=3)),textinfo="percent",textfont=dict(size=11,color="#F0F2F7"),hovertemplate="<b>%{label}</b><br>%{value} clientes<br>%{percent}<extra></extra>"))
    fig2.add_annotation(text=f"<b>{total}</b><br><span style='font-size:10px'>clientes</span>",x=0.5,y=0.5,showarrow=False,font=dict(size=16,color="#F0F2F7",family="DM Sans"))
    chart_layout(fig2,height=340,margin=(10,10,10,10))
    fig2.update_layout(showlegend=True,legend=dict(orientation="v",x=0,y=0,font=dict(size=11)))
    st.plotly_chart(fig2,use_container_width=True)

# SEC 2
sec("Clientes sem Classificação (Valor 9) por Factor")
scf=df_filtrado[df_filtrado["CLASSIFICACAO"]==9].groupby("DESCRICAO_FACTOR")["CLIENTE_ID"].nunique().reset_index(name="SEM_CLASS").sort_values("SEM_CLASS",ascending=True)
tpf=df_filtrado.groupby("DESCRICAO_FACTOR")["CLIENTE_ID"].nunique().reset_index(name="TOTAL")
scf=scf.merge(tpf,on="DESCRICAO_FACTOR"); scf["PERC"]=(scf["SEM_CLASS"]/scf["TOTAL"]*100).round(1)
col3,col4=st.columns([2.2,1])
with col3:
    fig3=go.Figure(); fig3.add_trace(go.Bar(x=scf["SEM_CLASS"],y=scf["DESCRICAO_FACTOR"],orientation="h",marker=dict(color=COR_SEM,opacity=0.85,line=dict(width=0)),text=[f"{p}%" for p in scf["PERC"]],textposition="outside",textfont=dict(color=TEXT_CLR,size=11),hovertemplate="<b>%{y}</b><br>%{x} clientes (%{text})<extra></extra>"))
    chart_layout(fig3,height=300,margin=(4,60,10,10))
    fig3.update_layout(xaxis_title="Nº Clientes",yaxis=dict(gridcolor="rgba(0,0,0,0)",linecolor=AXIS_CLR,tickfont=dict(size=11)))
    st.plotly_chart(fig3,use_container_width=True)
with col4:
    tbl=scf[["DESCRICAO_FACTOR","SEM_CLASS","PERC"]].sort_values("PERC",ascending=False).copy(); tbl.columns=["Factor","S/ Class.","% Total"]; tbl["% Total"]=tbl["% Total"].astype(str)+"%"
    st.dataframe(tbl.reset_index(drop=True),use_container_width=True,height=285)

# SEC 3
sec("Ranking de Clientes por Risco")
col5,col6=st.columns([1.5,1])
with col5:
    top_n=st.slider("Mostrar top N clientes",10,50,20)
    top_df=score_filtrado.nlargest(top_n,"SCORE_MEDIO")[["CLIENTE_ID","NOME","SEGMENTO","PROVINCIA","SCORE_MEDIO","NIVEL"]].reset_index(drop=True)
    top_df["SCORE_MEDIO"]=top_df["SCORE_MEDIO"].round(2); top_df.index+=1
    def cn(v):
        m={"Alto":"background-color:#C8102E22;color:#FF6B82","Médio":"background-color:#F59E0B22;color:#FBD07C","Baixo":"background-color:#10B98122;color:#6EE7B7","Sem Classificação":"background-color:#6B728022;color:#9CA3AF"}
        return m.get(v,"")
    st.dataframe(top_df.style.applymap(cn,subset=["NIVEL"]),use_container_width=True,height=400)
with col6:
    seg=score_filtrado.groupby(["SEGMENTO","NIVEL"]).size().reset_index(name="TOTAL")
    fig4=px.bar(seg,x="SEGMENTO",y="TOTAL",color="NIVEL",color_discrete_map=NIVEL_COLORS,barmode="group",labels={"TOTAL":"Clientes","SEGMENTO":""})
    chart_layout(fig4,height=400,margin=(10,10,10,10)); fig4.update_traces(marker_line_width=0)
    st.plotly_chart(fig4,use_container_width=True)

# SEC 4
sec("Evolução do Risco ao Longo do Tempo")
col7,col8=st.columns(2)
with col7:
    evo=classifs_df[classifs_df["CLIENTE_ID"].isin(clientes_filtrados)&classifs_df["DESCRICAO_FACTOR"].isin(factor_sel)].groupby("DATA")["CLASSIFICACAO"].mean().reset_index(name="SCORE_MEDIO")
    fig5=go.Figure(); fig5.add_trace(go.Scatter(x=evo["DATA"],y=evo["SCORE_MEDIO"],mode="lines+markers",line=dict(color=COR_ALTO,width=2.5),marker=dict(size=7,color=COR_ALTO,line=dict(color=BG_CHART,width=2)),fill="tozeroy",fillcolor="rgba(200,16,46,0.06)",hovertemplate="<b>%{x|%b %Y}</b><br>Score: %{y:.2f}<extra></extra>"))
    fig5.add_hline(y=6,line_dash="dot",line_color=COR_MEDIO,line_width=1.5,annotation_text="  Limite Alto Risco",annotation_font_color=COR_MEDIO,annotation_font_size=11)
    chart_layout(fig5,height=320,margin=(10,10,30,10))
    fig5.update_layout(title=dict(text="Score Médio de Risco Trimestral",font=dict(size=12,color=TEXT_CLR)))
    st.plotly_chart(fig5,use_container_width=True)
with col8:
    ea=classifs_df[classifs_df["CLIENTE_ID"].isin(clientes_filtrados)].groupby("DATA").apply(lambda g:(g["CLASSIFICACAO"]>=6).mean()*100).reset_index(name="PERC_ALTO")
    fig6=go.Figure(); fig6.add_trace(go.Scatter(x=ea["DATA"],y=ea["PERC_ALTO"],mode="lines+markers",line=dict(color=COR_TOTAL,width=2.5),marker=dict(size=7,color=COR_TOTAL,line=dict(color=BG_CHART,width=2)),fill="tozeroy",fillcolor="rgba(74,144,226,0.07)",hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f}% em alto risco<extra></extra>"))
    chart_layout(fig6,height=320,margin=(10,10,30,10))
    fig6.update_layout(yaxis_ticksuffix="%",title=dict(text="% de Clientes em Alto Risco (Score ≥ 6)",font=dict(size=12,color=TEXT_CLR)))
    st.plotly_chart(fig6,use_container_width=True)

# SEC 5
sec("Mapa de Calor — Factor × Classificação")
hd=df_filtrado.groupby(["DESCRICAO_FACTOR","CLASSIFICACAO"]).size().reset_index(name="TOTAL")
hp=hd.pivot(index="DESCRICAO_FACTOR",columns="CLASSIFICACAO",values="TOTAL").fillna(0)
fig7=px.imshow(hp,color_continuous_scale=[[0,"#13151C"],[0.3,"#1A3A2A"],[0.6,COR_MEDIO],[1.0,COR_ALTO]],labels=dict(x="Classificação (1=Baixo · 9=Sem Classif.)",y="",color="Clientes"),aspect="auto",height=320)
chart_layout(fig7,height=320,margin=(4,10,10,10))
fig7.update_coloraxes(colorbar=dict(tickfont=dict(color=TEXT_CLR),title=dict(text="Clientes",font=dict(color=TEXT_CLR)),bgcolor="rgba(0,0,0,0)",bordercolor=AXIS_CLR))
fig7.update_xaxes(tickvals=list(range(1,10)),ticktext=[str(i) for i in range(1,10)],side="bottom",tickfont=dict(size=12))
fig7.update_yaxes(tickfont=dict(size=11))
st.plotly_chart(fig7,use_container_width=True)

st.markdown("""<div style="margin-top:48px;padding-top:20px;border-top:1px solid #1E2028;display:flex;justify-content:space-between;align-items:center;"><span style="color:#2A2D36;font-size:.78rem;font-family:'DM Mono',monospace;">© 2025 Moza Banco · Risk Intelligence Platform</span><span style="color:#2A2D36;font-size:.78rem;font-family:'DM Mono',monospace;">KYC/AML · Dados demonstrativos</span></div>""", unsafe_allow_html=True)
