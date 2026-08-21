import streamlit as st
from datetime import datetime

from utils.data_loader import carregar_dados, filtrar_periodo
from utils.helpers import carregar_css
from views import (
    estudantes, docentes, projetos,
    publicacoes, eventos, parcerias, sobre
)

st.set_page_config(layout="wide", page_title="Dashboard MDC")
st.markdown(f"<style>{carregar_css()}</style>", unsafe_allow_html=True)

# 1. Carregar dados da pasta data/
alunas, docentes_df, projetos_df, publicacoes_df, premiacoes_df, eventos_df, parcerias_df = carregar_dados()

# 2. Barra Lateral (Filtros)
st.sidebar.markdown(
    '<p class="sidebar-titulo">Meninas Digitais no Cerrado</p>'
    '<p class="sidebar-marca">MDC - 10 anos</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="filtro-titulo">Filtrar por ano</p>', unsafe_allow_html=True)
ano_inicio, ano_fim = st.sidebar.slider("Período", 2016, 2026, (2016, 2026), label_visibility="collapsed")

st.sidebar.markdown('<p class="filtro-titulo">Filtrar estudantes</p>', unsafe_allow_html=True)
filtro_curso = st.sidebar.selectbox("Curso:", ["Todos", "Técnico", "Graduação", "Técnico e Graduação"])
filtro_verticalizou = st.sidebar.selectbox("Verticalizou:", ["Todas", "Sim", "Não"])
filtro_bolsista = st.sidebar.selectbox("Bolsista:", ["Todas", "Sim", "Não"])

# 3. Filtrar dados por período
projetos_p = filtrar_periodo(projetos_df, ano_inicio, ano_fim)
publicacoes_p = publicacoes_df[publicacoes_df["ano"].between(ano_inicio, ano_fim)]
premiacoes_p = premiacoes_df[premiacoes_df["ano"].between(ano_inicio, ano_fim)]
eventos_p = eventos_df[eventos_df["ano"].between(ano_inicio, ano_fim)]

# 4. Título Principal
st.title("Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado")
st.caption(f"Período {ano_inicio} a {ano_fim}")

# 5. Renderização das Abas
aba_estudantes, aba_docentes, aba_projetos, aba_publicacoes, aba_eventos, aba_parcerias, aba_sobre = st.tabs([
    "Estudantes", "Docentes", "Projetos", "Publicações",
    "Eventos e Premiações", "Parcerias", "Sobre"
])

with aba_estudantes:
    estudantes.render(
        alunas, projetos_p, publicacoes_p, docentes_df,
        ano_inicio, ano_fim, filtro_curso, filtro_verticalizou, filtro_bolsista
    )

with aba_docentes:
    docentes.render(docentes_df, alunas, projetos_p, publicacoes_p, ano_inicio, ano_fim)

with aba_projetos:
    projetos.render(projetos_p)

with aba_publicacoes:
    publicacoes.render(publicacoes_p)

with aba_eventos:
    eventos.render(eventos_p, premiacoes_p)

with aba_parcerias:
    parcerias.render(parcerias_df)

with aba_sobre:
    sobre.render()

# 6. Rodapé
st.markdown("---")
st.markdown(f'<p class="fonte-site" style="text-align: center;">Última atualização: {datetime.now().strftime("%d/%m/%Y")}</p>', unsafe_allow_html=True)
st.markdown('<p class="fonte-site" style="text-align: center;">Feito com &lt;3 por Sara Farias (Meninas Digitais no Cerrado)</p>', unsafe_allow_html=True)