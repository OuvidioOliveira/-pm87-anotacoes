import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Notas — Currículo Moçambicano",
    page_icon="🏫",
    layout="wide",
)

# ── Dados do Currículo Moçambicano ────────────────────────────────────────────
TURMAS = {
    "8ª Classe (ESG1)": {
        "disciplinas": [
            "Português", "Matemática", "Inglês", "Física",
            "Química", "Biologia", "História", "Geografia",
            "Educação Visual", "Educação Física", "ITIC",
        ]
    },
    "9ª Classe (ESG1)": {
        "disciplinas": [
            "Português", "Matemática", "Inglês", "Física",
            "Química", "Biologia", "História", "Geografia",
            "Educação Visual", "Educação Física", "ITIC",
        ]
    },
    "10ª Classe (ESG1)": {
        "disciplinas": [
            "Português", "Matemática", "Inglês", "Física",
            "Química", "Biologia", "História", "Geografia",
            "Educação Física", "ITIC",
        ]
    },
    "11ª Classe (ESG2)": {
        "disciplinas": [
            "Português", "Matemática", "Inglês", "Física",
            "Química", "Biologia", "História", "Educação Física",
        ]
    },
    "12ª Classe (ESG2)": {
        "disciplinas": [
            "Português", "Matemática", "Inglês", "Física",
            "Química", "Biologia", "História", "Educação Física",
        ]
    },
}

TRIMESTRES = ["1º Trimestre", "2º Trimestre", "3º Trimestre"]
NOTA_MIN = 10
NOTA_MAX = 20
ANO_LECTIVO = "2024"

NOMES_M = [
    "Alberto Muianga", "Bendito Chissano", "Carlos Macuácua", "Dário Nhantumbo",
    "Eduardo Sitoe", "Feliciano Mondlane", "Gilberto Cossa", "Hélder Bila",
    "Inocêncio Tembe", "José Cumbe", "Leonardo Matusse", "Manuel Guambe",
    "Nuno Chaúque", "Osvaldo Mabunda", "Paulo Chicuamba", "Renato Zunguze",
    "Samuel Ngwenya", "Tomás Macamo", "Vicente Mate", "Wilson Machava",
]
NOMES_F = [
    "Ana Machava", "Beatriz Nhacolo", "Cláudia Ussene", "Diana Cumbe",
    "Elena Mafalala", "Fátima Sithole", "Graça Mavie", "Helena Muiambo",
    "Inês Cossa", "Joana Tembe", "Lurdes Zandamela", "Maria Macuacua",
    "Nádia Bila", "Olívia Cumbane", "Palmira Mulhanga", "Raquel Nhabomba",
    "Sofia Nguenha", "Teresa Sigauque", "Ursula Timbe", "Vera Mondlane",
]

# ── Geração de Mock Data ──────────────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    random.seed(42)
    np.random.seed(42)
    registros = []

    for turma, info in TURMAS.items():
        disciplinas = info["disciplinas"]
        alunos = random.sample(NOMES_M, 12) + random.sample(NOMES_F, 10)
        alunos = alunos[:22]

        for aluno in alunos:
            genero = "M" if aluno in NOMES_M else "F"
            # Perfil de desempenho do aluno (bom, médio, fraco)
            perfil = np.random.choice(["bom", "médio", "fraco"], p=[0.4, 0.45, 0.15])
            if perfil == "bom":
                media_base = np.random.uniform(14, 19)
            elif perfil == "médio":
                media_base = np.random.uniform(11, 15)
            else:
                media_base = np.random.uniform(8, 12)

            for disciplina in disciplinas:
                ajuste_disc = np.random.uniform(-1.5, 1.5)
                for trimestre in TRIMESTRES:
                    nota = round(
                        np.clip(
                            np.random.normal(media_base + ajuste_disc, 1.5),
                            0, 20
                        ), 1
                    )
                    registros.append({
                        "Turma": turma,
                        "Aluno": aluno,
                        "Género": genero,
                        "Disciplina": disciplina,
                        "Trimestre": trimestre,
                        "Nota": nota,
                        "Aprovado": nota >= NOTA_MIN,
                        "Ano": ANO_LECTIVO,
                    })

    return pd.DataFrame(registros)

df = gerar_dados()

# ── Sidebar — Filtros ─────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Flag_of_Mozambique.svg/320px-Flag_of_Mozambique.svg.png",
        width=120,
    )
    st.title("🏫 Filtros")
    st.markdown("**Ano Lectivo:** 2024")

    turma_sel = st.selectbox("Turma", ["Todas"] + list(TURMAS.keys()))
    trimestre_sel = st.multiselect(
        "Trimestre", TRIMESTRES, default=TRIMESTRES
    )
    genero_sel = st.radio("Género", ["Todos", "Masculino", "Feminino"])

    if turma_sel != "Todas":
        discs_disponiveis = TURMAS[turma_sel]["disciplinas"]
    else:
        discs_disponiveis = sorted(df["Disciplina"].unique().tolist())

    disc_sel = st.multiselect(
        "Disciplinas", discs_disponiveis, default=discs_disponiveis
    )

# ── Aplicar filtros ───────────────────────────────────────────────────────────
dfF = df.copy()
if turma_sel != "Todas":
    dfF = dfF[dfF["Turma"] == turma_sel]
if trimestre_sel:
    dfF = dfF[dfF["Trimestre"].isin(trimestre_sel)]
if genero_sel == "Masculino":
    dfF = dfF[dfF["Género"] == "M"]
elif genero_sel == "Feminino":
    dfF = dfF[dfF["Género"] == "F"]
if disc_sel:
    dfF = dfF[dfF["Disciplina"].isin(disc_sel)]

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#006B3C;'>
    📊 Dashboard de Desempenho Escolar
</h1>
<h4 style='text-align:center; color:#CE1126;'>
    Currículo Moçambicano · ESG · Ano Lectivo 2024
</h4>
<hr style='border:2px solid #FCB912;'>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_alunos = dfF["Aluno"].nunique()
media_geral = dfF["Nota"].mean()
taxa_aprovacao = (dfF["Aprovado"].sum() / len(dfF) * 100) if len(dfF) > 0 else 0
total_reprovados = dfF[~dfF["Aprovado"]]["Aluno"].nunique()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("👩‍🎓 Total de Alunos", total_alunos)
with k2:
    cor = "normal" if media_geral >= NOTA_MIN else "inverse"
    st.metric("📈 Média Geral", f"{media_geral:.1f} / 20", delta=f"{media_geral - NOTA_MIN:+.1f} vs mínimo")
with k3:
    st.metric("✅ Taxa de Aprovação", f"{taxa_aprovacao:.1f}%")
with k4:
    st.metric("❌ Alunos c/ Reprovação", total_reprovados)

st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)

# ── Linha 1: Distribuição de notas + Aprovação por disciplina ─────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Distribuição das Notas")
    fig_hist = px.histogram(
        dfF, x="Nota", nbins=22,
        color_discrete_sequence=["#006B3C"],
        labels={"Nota": "Nota (0–20)", "count": "Frequência"},
        title="Distribuição das notas (todos os alunos e disciplinas)"
    )
    fig_hist.add_vline(
        x=NOTA_MIN, line_dash="dash", line_color="#CE1126",
        annotation_text="Nota mínima (10)", annotation_position="top right"
    )
    fig_hist.update_layout(bargap=0.05, plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("📚 Média por Disciplina")
    media_disc = (
        dfF.groupby("Disciplina")["Nota"]
        .mean()
        .reset_index()
        .sort_values("Nota", ascending=True)
    )
    media_disc["Cor"] = media_disc["Nota"].apply(
        lambda n: "#CE1126" if n < NOTA_MIN else "#006B3C"
    )
    fig_disc = px.bar(
        media_disc, x="Nota", y="Disciplina",
        orientation="h", color="Cor",
        color_discrete_map="identity",
        text=media_disc["Nota"].round(1),
        title="Média por disciplina"
    )
    fig_disc.add_vline(x=NOTA_MIN, line_dash="dash", line_color="#FCB912")
    fig_disc.update_layout(showlegend=False, plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig_disc, use_container_width=True)

# ── Linha 2: Evolução trimestral + Aprovação por género ──────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("📅 Evolução por Trimestre")
    evolucao = (
        dfF.groupby(["Trimestre", "Disciplina"])["Nota"]
        .mean()
        .reset_index()
    )
    fig_evo = px.line(
        evolucao, x="Trimestre", y="Nota",
        color="Disciplina",
        markers=True,
        title="Evolução da média por disciplina ao longo dos trimestres"
    )
    fig_evo.add_hline(
        y=NOTA_MIN, line_dash="dot", line_color="#CE1126",
        annotation_text="Mínimo"
    )
    fig_evo.update_layout(plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig_evo, use_container_width=True)

with col4:
    st.subheader("⚖️ Aprovação por Género")
    gen_aprov = (
        dfF.groupby(["Género", "Aprovado"])
        .size()
        .reset_index(name="Contagem")
    )
    gen_aprov["Status"] = gen_aprov["Aprovado"].map({True: "Aprovado ✅", False: "Reprovado ❌"})
    gen_aprov["Género"] = gen_aprov["Género"].map({"M": "Masculino", "F": "Feminino"})
    fig_gen = px.bar(
        gen_aprov, x="Género", y="Contagem",
        color="Status",
        barmode="group",
        color_discrete_map={"Aprovado ✅": "#006B3C", "Reprovado ❌": "#CE1126"},
        title="Comparativo de aprovação por género"
    )
    fig_gen.update_layout(plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig_gen, use_container_width=True)

# ── Linha 3: Heatmap de notas ─────────────────────────────────────────────────
st.subheader("🗺️ Mapa de Calor — Notas Médias por Turma e Disciplina")
if turma_sel == "Todas":
    pivot = dfF.pivot_table(index="Turma", columns="Disciplina", values="Nota", aggfunc="mean")
    fig_heat = px.imshow(
        pivot,
        color_continuous_scale=["#CE1126", "#FCB912", "#006B3C"],
        zmin=8, zmax=20,
        aspect="auto",
        text_auto=".1f",
        title="Mapa de calor: Nota média por Turma × Disciplina"
    )
    fig_heat.add_shape(
        type="rect", x0=-0.5, y0=-0.5,
        x1=len(pivot.columns)-0.5, y1=len(pivot)-0.5,
        line=dict(color="#333", width=1)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    pivot = dfF.pivot_table(index="Aluno", columns="Disciplina", values="Nota", aggfunc="mean")
    fig_heat = px.imshow(
        pivot,
        color_continuous_scale=["#CE1126", "#FCB912", "#006B3C"],
        zmin=0, zmax=20,
        aspect="auto",
        text_auto=".1f",
        title=f"Mapa de calor: {turma_sel} — Nota por Aluno × Disciplina"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Linha 4: Top e Bottom alunos ─────────────────────────────────────────────
col5, col6 = st.columns(2)

media_aluno = (
    dfF.groupby(["Turma", "Aluno", "Género"])["Nota"]
    .mean()
    .reset_index()
    .rename(columns={"Nota": "Média"})
    .sort_values("Média", ascending=False)
)

with col5:
    st.subheader("🏆 Top 10 Alunos")
    top10 = media_aluno.head(10).copy()
    top10["Média"] = top10["Média"].round(1)
    top10["Género"] = top10["Género"].map({"M": "👦", "F": "👧"})
    st.dataframe(
        top10[["Aluno", "Género", "Turma", "Média"]].reset_index(drop=True),
        use_container_width=True, hide_index=True
    )

with col6:
    st.subheader("⚠️ Alunos em Risco (Média < 10)")
    em_risco = media_aluno[media_aluno["Média"] < NOTA_MIN].copy()
    em_risco["Média"] = em_risco["Média"].round(1)
    em_risco["Género"] = em_risco["Género"].map({"M": "👦", "F": "👧"})
    if em_risco.empty:
        st.success("Nenhum aluno com média abaixo do mínimo no filtro actual.")
    else:
        st.dataframe(
            em_risco[["Aluno", "Género", "Turma", "Média"]]
            .sort_values("Média")
            .reset_index(drop=True),
            use_container_width=True, hide_index=True
        )

# ── Tabela de notas por trimestre ─────────────────────────────────────────────
st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)
st.subheader("📋 Tabela de Notas por Trimestre")

with st.expander("Ver tabela completa de notas", expanded=False):
    tabela_pivot = dfF.pivot_table(
        index=["Turma", "Aluno", "Disciplina"],
        columns="Trimestre",
        values="Nota",
        aggfunc="mean"
    ).reset_index()
    # Média final
    trim_cols = [c for c in tabela_pivot.columns if "Trimestre" in c]
    tabela_pivot["Média Final"] = tabela_pivot[trim_cols].mean(axis=1).round(1)
    tabela_pivot["Situação"] = tabela_pivot["Média Final"].apply(
        lambda n: "✅ Aprovado" if n >= NOTA_MIN else "❌ Reprovado"
    )

    def highlight_row(row):
        cor = "background-color: #ffeaea" if "Reprovado" in str(row.get("Situação", "")) else ""
        return [cor] * len(row)

    st.dataframe(
        tabela_pivot.style.apply(highlight_row, axis=1),
        use_container_width=True,
        hide_index=True
    )

# ── Rodapé ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border:2px solid #FCB912;'>
<p style='text-align:center; font-size:0.8em; color:#888;'>
    📍 República de Moçambique · Ministério da Educação e Desenvolvimento Humano (MINEDH)<br>
    Sistema Nacional de Educação · ESG1 & ESG2 · Dashboard de Desempenho Escolar 2024<br>
    <em>Nota mínima de aprovação: 10 valores · 3 trimestres por ano lectivo</em>
</p>
""", unsafe_allow_html=True)
