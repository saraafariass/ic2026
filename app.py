
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import re

from assets.styles import (
    vermelho, vermelho_claro, cor_texto, cor_texto_secundario,
    cor_texto_terciario, fundo, fundo_card, cores_projetos, cores_eventos
)

# Configura a página para ocupar a tela toda e define o título
st.set_page_config(layout="wide", page_title="Dashboard MDC")

# ============================================================
# 1. CARREGAR O CSS (estilos) do arquivo externo
# ============================================================
def carregar_css():
    with open("assets/style.css", "r", encoding="utf-8") as arquivo:
        return arquivo.read()

st.markdown(f"<style>{carregar_css()}</style>", unsafe_allow_html=True)

# ============================================================
# 2. FUNÇÕES AUXILIARES (para não repetir código)
# ============================================================

# Cria um título de seção
def secao(titulo):
    st.markdown(f'<p class="secao">{titulo}</p>', unsafe_allow_html=True)

# Monta o HTML de um card de publicação
def _pub_card_inner(alcance, ano, alcance_cor, referencia, autoria, botao):
    cabecalho = (
        f'<span style="font-size:0.68rem;background:{alcance_cor};color:#fff;'
        f'padding:1px 7px;border-radius:10px;font-weight:600;">' + alcance + '</span>'
        f'<span style="font-size:0.68rem;color:{cor_texto_terciario};"> ' + ano + '</span><br>'
    )
    corpo = (
        '<span style="font-size:0.78rem;color:' + cor_texto + ';display:block;margin-top:3px;">' +
        referencia + '</span>' + botao
    )
    return (
        f'<div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;'
        f'margin-bottom:0.35rem;border-left:3px solid {alcance_cor};">'
        + cabecalho + corpo + '</div>'
    )

# Mostra uma publicação em formato de card
def card_publicacao(publicacao, alcance_cor, botao=''):
    referencia = str(publicacao.get('referencia', ''))
    alcance = str(publicacao.get('alcance', ''))
    ano = str(publicacao.get('ano', ''))
    st.markdown(_pub_card_inner(alcance, ano, alcance_cor, referencia, '', botao), unsafe_allow_html=True)

# Mostra uma publicação em formato de lista (com botão)
def card_publicacao_lista(publicacao, cor_vermelho, cor_texto, cor_texto_sec):
    referencia = str(publicacao.get('referencia', ''))
    autoria = str(publicacao.get('autoria', 'Não informado'))
    alcance = str(publicacao.get('alcance', ''))
    link = str(publicacao.get('link', '')).strip()
    tem_link = pd.notna(publicacao.get('link')) and link

    botao_html = (
        f'<a href="{link}" target="_blank" style="'
        f'display:inline-block;padding:5px 14px;background:{cor_vermelho};'
        f'color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;'
        f'text-decoration:none;letter-spacing:0.02em;">Acessar trabalho</a>'
    ) if tem_link else ''

    card_html = (
        f'<div class="card-publicacao">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
        f'<span class="alcance-badge">' + alcance + '</span>' + botao_html + '</div>'
        f'<p style="margin:0.4rem 0 0.3rem;font-weight:500;color:{cor_texto};">' + referencia + '</p>'
        f'<small style="color:{cor_texto_sec};">Autoria: ' + autoria + '</small>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

# Filtra projetos pelo período (ano inicial e final)
def filtrar_periodo(df, ano_inicio, ano_fim):
    return df[(df["ano_ini"] <= ano_fim) & (df["ano_fim"] >= ano_inicio)]

# Extrai ano inicial e final de textos como "2020 - atual" ou "2022"
def extrair_anos(texto):
    texto = str(texto).strip()
    anos = re.findall(r'\d{4}', texto)
    if not anos:
        return None, None
    ano_inicio = int(anos[0])
    ano_fim = 2026 if 'atual' in texto.lower() else int(anos[-1])
    return ano_inicio, ano_fim

# Filtra alunas que estavam ativas no período escolhido
def filtrar_alunas_periodo(df, ano_inicio, ano_fim):
    def esta_no_periodo(linha):
        a_i, a_f = extrair_anos(linha['periodo'])
        if a_i is None:
            return True
        return a_i <= ano_fim and a_f >= ano_inicio
    return df[df.apply(esta_no_periodo, axis=1)]

# Remove prefixos (Prof., Profa.) e sufixos como (2016-2022) do nome
def nome_sem_prefixos(nome):
    nome = re.sub(r'^Prof[ao]?\.\s*', '', nome.strip())
    nome = re.sub(r'\s*\(.*?\)', '', nome).strip()
    return nome.lower()

def nome_para_busca(nome):
    nome = re.sub(r'^Prof[ao]?\.\s*', '', nome.strip())
    nome = re.sub(r'\s*\(.*?\)', '', nome).strip()
    partes = nome.split()
    # Se tiver 3 ou mais nomes (ex: Maria Luiza Silva), usa os 3 primeiros
    if len(partes) >= 3:
        return ' '.join(partes[:3]).lower()
    elif len(partes) == 2:
        return ' '.join(partes[:2]).lower()
    return nome.lower()

# Verifica se a pessoa é aluna e separa projetos/publicações por papel (aluna ou professora)
def separar_por_papel(nome, projetos_df, publicacoes_df, alunas_df, docentes_df, ano_inicio, ano_fim):
    busca = nome_para_busca(nome)

    # Verifica se é aluna no período
    eh_aluna = False
    periodo_aluna_fim = 0
    for _, aluna in alunas_df.iterrows():
        if busca in str(aluna['nome']).lower():
            periodo = str(aluna.get('periodo', ''))
            anos = re.findall(r'\d{4}', periodo)
            if anos:
                periodo_ini = int(anos[0])
                if 'atual' in periodo.lower():
                    periodo_fim = 2026
                else:
                    periodo_fim = int(anos[-1]) if len(anos) > 1 else periodo_ini
                if periodo_fim >= ano_inicio and periodo_ini <= ano_fim:
                    eh_aluna = True
                    periodo_aluna_fim = periodo_fim
                    break

    # Verifica se é docente
    eh_docente = False
    for _, docente in docentes_df.iterrows():
        if busca in str(docente['nome']).lower():
            eh_docente = True
            break

    # Busca projetos e publicações da pessoa
    projetos = buscar_projetos_por_nome(nome, projetos_df)
    publicacoes = buscar_publicacoes_por_nome(nome, publicacoes_df)

    # Se for aluna e docente, separa pelo ano
    if eh_aluna and eh_docente:
        proj_aluna = []
        proj_docente = []
        for p in projetos:
            ano_proj = p.get('ano', p.get('ano_ini', 0))
            if ano_proj <= periodo_aluna_fim:
                proj_aluna.append(p)
            else:
                proj_docente.append(p)

        pub_aluna = []
        pub_docente = []
        for p in publicacoes:
            ano_pub = p.get('ano', 0)
            if ano_pub <= periodo_aluna_fim:
                pub_aluna.append(p)
            else:
                pub_docente.append(p)

        return proj_aluna, proj_docente, pub_aluna, pub_docente, True
    elif eh_aluna:
        return projetos, [], publicacoes, [], True
    else:
        return [], projetos, [], publicacoes, False

# Encontra projetos em que a pessoa aparece na equipe ou autoria
def buscar_projetos_por_nome(nome, projetos_df):
    busca = nome_para_busca(nome)
    return [
        p for _, p in projetos_df.iterrows()
        if busca in str(p.get('equipe', p.get('autoria', ''))).lower()
    ]

# Encontra publicações em que a pessoa é autora
def buscar_publicacoes_por_nome(nome, publicacoes_df):
    busca = nome_para_busca(nome)
    return [
        p for _, p in publicacoes_df.iterrows()
        if busca in str(p.get('autoria', '')).lower()
    ]

# Carrega todos os dados dos arquivos CSV
@st.cache_data
def carregar_dados():
    alunas = pd.read_csv("alunas.csv")
    docentes = pd.read_csv("docentes.csv")
    projetos = pd.read_csv("projetos.csv")
    publicacoes = pd.read_csv("publicacoes.csv")
    premiacoes = pd.read_csv("premiacoes.csv")
    eventos = pd.read_csv("eventos.csv")
    parcerias = pd.read_csv("parcerias.csv")
    eventos['ano'] = pd.to_numeric(eventos['ano'], errors='coerce').astype('Int64')
    premiacoes['ano'] = pd.to_numeric(premiacoes['ano'], errors='coerce').astype('Int64')
    return alunas, docentes, projetos, publicacoes, premiacoes, eventos, parcerias

def iniciais(nome):
    partes = nome.strip().split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[-1][0]).upper()
    return partes[0][:2].upper()

def badge_curso(curso_str):
    if pd.isna(curso_str) or str(curso_str).strip() == '':
        return ''
    cursos = lista_cursos(curso_str)
    badges = []
    for curso in cursos:
        curso = curso.strip()
        if "Técnico" in curso:
            badges.append('<span class="badge badge-tec">Técnico</span>')
        elif "Graduação" in curso or "Licenciatura" in curso or "Bacharelado" in curso:
            badges.append('<span class="badge badge-grad">Graduação</span>')
    return ' '.join(badges)

def lista_cursos(curso_str):
    if pd.isna(curso_str) or str(curso_str).strip() == '':
        return []
    return [c.strip() for c in str(curso_str).split(';')]

# carregar dados
alunas, docentes, projetos, publicacoes, premiacoes, eventos, parcerias = carregar_dados()

ano_minimo, ano_maximo = 2016, 2026

# filtros 
st.sidebar.markdown(
    '<p class="sidebar-titulo">Meninas Digitais no Cerrado</p>'
    '<p class="sidebar-marca">MDC - 10 anos</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="filtro-titulo">Filtrar por ano</p>', unsafe_allow_html=True)
ano_inicio, ano_fim = st.sidebar.slider(
    "Período", 2016, 2026, (2016, 2026), label_visibility="collapsed",
)

st.sidebar.markdown('<p class="filtro-titulo">Filtrar estudantes</p>', unsafe_allow_html=True)
opcoes_curso = ["Todos", "Técnico", "Graduação", "Técnico e Graduação"]
filtro_curso = st.sidebar.selectbox("Curso:", opcoes_curso)
filtro_verticalizou = st.sidebar.selectbox("Verticalizou:", ["Todas", "Sim", "Não"])
filtro_bolsista = st.sidebar.selectbox("Bolsista:", ["Todas", "Sim", "Não"])

# Aplica os filtros de período nos dados
projetos_periodo = filtrar_periodo(projetos, ano_inicio, ano_fim)
publicacoes_periodo = publicacoes[publicacoes["ano"].between(ano_inicio, ano_fim)]
premiacoes_periodo = premiacoes[premiacoes["ano"].between(ano_inicio, ano_fim)]
eventos_periodo = eventos[eventos["ano"].between(ano_inicio, ano_fim)]

# abas
st.title("Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado")
st.caption(f"Período {ano_inicio} a {ano_fim}")

abas = st.tabs([
    "Estudantes", "Docentes", "Projetos", "Publicações",
    "Eventos e Premiações", "Parcerias", "Sobre"
])
aba_estudantes, aba_docentes, aba_projetos, aba_publicacoes, aba_eventos, aba_parcerias, aba_sobre = abas

# aba estudantes 
with aba_estudantes:
    secao("Participação no Projeto Meninas Digitais no Cerrado")

    alunas_periodo = filtrar_alunas_periodo(alunas, ano_inicio, ano_fim)
    alunas_filtradas = alunas_periodo.copy()

    # Filtros adicionais
    if filtro_curso == "Técnico":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: "Técnico" in str(x))]
    elif filtro_curso == "Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: "Graduação" in str(x) or "Licenciatura" in str(x) or "Bacharelado" in str(x))]
    elif filtro_curso == "Técnico e Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: "Técnico" in str(x) and ("Graduação" in str(x) or "Licenciatura" in str(x) or "Bacharelado" in str(x)))]

    if filtro_verticalizou != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["verticalizou"] == filtro_verticalizou]

    if filtro_bolsista != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["bolsista"] == filtro_bolsista]

    # Alunas que fizeram Técnico
    alunas_tecnico = alunas_filtradas[alunas_filtradas["curso"].apply(
        lambda x: any("Técnico" in c for c in lista_cursos(x))
    )]
    # Alunas que fizeram Graduação
    alunas_graduacao = alunas_filtradas[alunas_filtradas["curso"].apply(
        lambda x: any("Graduação" in c or "Licenciatura" in c or "Bacharelado" in c for c in lista_cursos(x))
    )]

    st.markdown("### Ensino Médio Técnico")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de alunas", len(alunas_tecnico))
    with col2:
        verticalizou_count = len(alunas_tecnico[alunas_tecnico["verticalizou"] == "Sim"]) if not alunas_tecnico.empty and "verticalizou" in alunas_tecnico.columns else 0
        st.metric("Verticalizaram", verticalizou_count)
    with col3:
        bolsistas_count = len(alunas_tecnico[alunas_tecnico["bolsista"] == "Sim"]) if not alunas_tecnico.empty and "bolsista" in alunas_tecnico.columns else 0
        st.metric("Bolsistas", bolsistas_count)

    st.markdown("---")
    st.markdown("### Bacharelado em Sistemas de Informação")
    total_graduacao = 0
    bolsistas_graduacao = 0
    for _, aluna in alunas_filtradas.iterrows():
        cursos = lista_cursos(aluna['curso'])
        tem_graduacao = any("Graduação" in c or "Licenciatura" in c or "Bacharelado" in c for c in cursos)
        if tem_graduacao:
            total_graduacao += 1
            if aluna['bolsista'] == 'Sim':
                bolsistas_graduacao += 1
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de alunas", total_graduacao)
    with col2:
        st.metric("Bolsistas", bolsistas_graduacao)

    # Observação sobre alunas que estão em ambas as categorias
    alunas_tec_e_grad = alunas_filtradas[
        alunas_filtradas["curso"].apply(
            lambda x: any("Técnico" in c for c in lista_cursos(x))
        ) &
        alunas_filtradas["curso"].apply(
            lambda x: any("Graduação" in c or "Licenciatura" in c or "Bacharelado" in c for c in lista_cursos(x))
        )
    ]
    if not alunas_tec_e_grad.empty:
        nomes = ", ".join(alunas_tec_e_grad["nome"].tolist())
        soma_totais = len(alunas_tecnico) + total_graduacao
        total_unicas = len(alunas_filtradas)

        st.markdown(f"""
        <div style="background:#fff3cd;border-left:4px solid #ffc107;padding:0.6rem 1rem;
            border-radius:4px;margin-top:1rem;font-size:0.85rem;color:#856404;">
            <strong>Observação:</strong> As alunas <strong>{nomes}</strong> aparecem em <strong>ambas</strong> as categorias
            (cursaram Técnico <em>e</em> Graduação). Por isso, a soma dos totais (Técnico + Graduação) é <strong>{soma_totais}</strong>,
            mas o <strong>total único de alunas no período é {total_unicas}</strong>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Mostra quantas alunas estão sendo exibidas
    total_filtradas = len(alunas_filtradas)
    total_geral = len(alunas_periodo)
    if total_filtradas == total_geral:
        st.markdown(f'<p class="resultados-info">{total_geral} estudantes no período</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="resultados-info">Exibindo {total_filtradas} de {total_geral} estudantes no período</p>', unsafe_allow_html=True)

    # Cards individuais de cada aluna
    if alunas_filtradas.empty:
        st.markdown('<div class="sem-resultado">Nenhuma estudante encontrada com os filtros selecionados.</div>', unsafe_allow_html=True)
    else:
        for _, aluna in alunas_filtradas.iterrows():
            proj_aluna, proj_docente, pub_aluna, pub_docente, eh_aluna = separar_por_papel(
                aluna["nome"], projetos_periodo, publicacoes_periodo, alunas, docentes, ano_inicio, ano_fim
            )

            vert_val = aluna["verticalizou"]
            vert_display = "Não se aplica" if pd.isna(vert_val) or str(vert_val).strip() == "" else vert_val

            badges_html = badge_curso(aluna["curso"])
            if aluna["bolsista"] == "Sim":
                badges_html += ' <span class="badge badge-bols">Bolsista</span>'
            if vert_val == "Sim":
                badges_html += ' <span class="badge badge-vert">Verticalizou</span>'

            label = f"{aluna['nome']} ({aluna['curso']}: {aluna['periodo']})"

            nome_base = nome_sem_prefixos(aluna['nome'])
            is_thalia = 'thalia' in nome_base

            with st.expander(label):
                st.markdown(f'<div style="margin-bottom:0.5rem;">{badges_html}</div>', unsafe_allow_html=True)

                col_info, col_proj, col_pub = st.columns([1, 1.5, 2])

                with col_info:
                    st.markdown(f"""
                    <div class="det-label">Bolsista</div>
                    <div class="det-valor">{aluna['bolsista']}</div>
                    <div class="det-label">Verticalizou</div>
                    <div class="det-valor">{vert_display}</div>
                    <div class="det-label">Curso</div>
                    <div class="det-valor">{aluna['curso']}</div>
                    """, unsafe_allow_html=True)
                    observacao = str(aluna.get('observacao', '')).strip()
                    if observacao and observacao != 'nan':
                        st.markdown(f"""
                        <div class="det-label" style="margin-top:0.65rem;">Observação</div>
                        <div class="det-valor" style="font-size:0.8rem;color:{cor_texto_secundario};">{observacao}</div>
                        """, unsafe_allow_html=True)

                with col_proj:
                    if is_thalia:
                        if proj_aluna or proj_docente:
                            if proj_aluna:
                                st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(proj_aluna)})</div>', unsafe_allow_html=True)
                                for p in proj_aluna:
                                    cor_tipo = cores_projetos.get(p["tipo"], vermelho)
                                    st.markdown(f"""
                                    <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                        margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
                                        <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p['nome']}</span><br>
                                        <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p['tipo']}</span>
                                        <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p['periodo']}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            if proj_docente:
                                st.markdown("---")
                                st.markdown(f'<div class="det-label">Como professora ({len(proj_docente)})</div>', unsafe_allow_html=True)
                                for p in proj_docente:
                                    cor_tipo = cores_projetos.get(p["tipo"], vermelho)
                                    st.markdown(f"""
                                    <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                        margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
                                        <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p['nome']}</span><br>
                                        <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p['tipo']}</span>
                                        <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p['periodo']}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.caption("Nenhum projeto no período")
                    else:
                        st.markdown(f'<div class="det-label">Projetos ({len(proj_aluna)})</div>', unsafe_allow_html=True)
                        if proj_aluna:
                            for p in proj_aluna:
                                cor_tipo = cores_projetos.get(p["tipo"], vermelho)
                                st.markdown(f"""
                                <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                    margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
                                    <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p['nome']}</span><br>
                                    <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p['tipo']}</span>
                                    <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p['periodo']}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.caption("Nenhum projeto no período")

                with col_pub:
                    if is_thalia:
                        if pub_aluna or pub_docente:
                            if pub_aluna:
                                st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(pub_aluna)})</div>', unsafe_allow_html=True)
                                for p in pub_aluna:
                                    link = str(p.get('link', '')).strip()
                                    tem_link = pd.notna(p.get('link')) and link
                                    alcance_cor = vermelho if p['alcance'] == "Internacional" else vermelho_claro
                                    botao = (
                                        f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                        f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
                                        f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                                    ) if tem_link else ''
                                    card_publicacao(p, alcance_cor, botao)
                            if pub_docente:
                                st.markdown("---")
                                st.markdown(f'<div class="det-label">Como professora ({len(pub_docente)})</div>', unsafe_allow_html=True)
                                for p in pub_docente:
                                    link = str(p.get('link', '')).strip()
                                    tem_link = pd.notna(p.get('link')) and link
                                    alcance_cor = vermelho if p['alcance'] == "Internacional" else vermelho_claro
                                    botao = (
                                        f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                        f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
                                        f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                                    ) if tem_link else ''
                                    card_publicacao(p, alcance_cor, botao)
                        else:
                            st.caption("Nenhuma publicação no período")
                    else:
                        st.markdown(f'<div class="det-label">Publicações ({len(pub_aluna)})</div>', unsafe_allow_html=True)
                        if pub_aluna:
                            for p in pub_aluna:
                                link = str(p.get('link', '')).strip()
                                tem_link = pd.notna(p.get('link')) and link
                                alcance_cor = vermelho if p['alcance'] == "Internacional" else vermelho_claro
                                botao = (
                                    f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                    f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
                                    f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                                ) if tem_link else ''
                                card_publicacao(p, alcance_cor, botao)
                        else:
                            st.caption("Nenhuma publicação no período")

    # Gráficos de distribuição
    secao("Indicadores de Raça")
    if not alunas_filtradas.empty and 'raca' in alunas_filtradas.columns:
        contagem_raca = alunas_filtradas['raca'].value_counts().reset_index()
        contagem_raca.columns = ['Raça/Etnia', 'Quantidade']
        fig_raca = px.pie(
            contagem_raca,
            names='Raça/Etnia',
            values='Quantidade',
            color_discrete_sequence=['#e57373', '#c62828', '#b71c1c', '#880e4f', '#4a148c']
        )
        fig_raca.update_layout(height=400, paper_bgcolor=fundo, plot_bgcolor=fundo, showlegend=True)
        st.plotly_chart(fig_raca, use_container_width=True)

    secao("Indicadores de Curso")
    if not alunas_filtradas.empty:
        contagem_cursos = {}
        alunas_contadas = set()
        for idx, aluna in alunas_filtradas.iterrows():
            id_aluna = f"{aluna['nome']}_{aluna['periodo']}"
            if id_aluna not in alunas_contadas:
                alunas_contadas.add(id_aluna)
                cursos = lista_cursos(aluna['curso'])
                for curso in cursos:
                    # Normaliza o nome do curso para ficar padronizado
                    if 'Técnico em Informática para Internet' in curso:
                        curso_norm = 'Técnico em Informática para Internet'
                    elif 'Técnico em Informática' in curso:
                        curso_norm = 'Técnico em Informática'
                    elif 'Técnico em Agropecuária' in curso:
                        curso_norm = 'Técnico em Agropecuária'
                    elif 'Técnico em Inteligência Artificial' in curso:
                        curso_norm = 'Técnico em Inteligência Artificial'
                    elif 'Licenciatura em Química' in curso:
                        curso_norm = 'Licenciatura em Química'
                    elif 'Bacharelado em Sistemas de Informação' in curso:
                        curso_norm = 'Bacharelado em Sistemas de Informação'
                    else:
                        curso_norm = curso
                    contagem_cursos[curso_norm] = contagem_cursos.get(curso_norm, 0) + 1

        if contagem_cursos:
            df_cursos = pd.DataFrame([
                {'Curso': curso, 'Quantidade': qtd}
                for curso, qtd in contagem_cursos.items()
            ])
            ordem = [
                'Técnico em Informática para Internet',
                'Técnico em Informática',
                'Técnico em Agropecuária',
                'Técnico em Inteligência Artificial',
                'Licenciatura em Química',
                'Bacharelado em Sistemas de Informação'
            ]
            df_cursos['ordem'] = df_cursos['Curso'].apply(
                lambda x: ordem.index(x) if x in ordem else len(ordem)
            )
            df_cursos = df_cursos.sort_values('ordem')
            fig_curso = px.pie(
                df_cursos,
                names='Curso',
                values='Quantidade',
                color_discrete_sequence=['#e57373', '#c62828', '#b71c1c', '#880e4f', '#4a148c', '#311b92']
            )
            fig_curso.update_layout(height=400, paper_bgcolor=fundo, plot_bgcolor=fundo, showlegend=True)
            st.plotly_chart(fig_curso, use_container_width=True)

# ============================================================
# 7. ABA DOCENTES
# ============================================================
with aba_docentes:
    secao("Corpo docente")
    st.metric("Total de docentes", len(docentes))
    st.markdown("---")

    for _, docente in docentes.iterrows():
        proj_aluna, proj_docente, pub_aluna, pub_docente, eh_aluna = separar_por_papel(
            docente["nome"], projetos_periodo, publicacoes_periodo, alunas, docentes, ano_inicio, ano_fim
        )

        lattes_url = str(docente.get('lattes', '')).strip()
        email = docente.get('email', '')

        nome_exibido = nome_sem_prefixos(docente["nome"]).title()
        is_thalia = 'thalia' in nome_exibido.lower()

        label = f"{docente['nome']}"

        with st.expander(label):
            col_info, col_proj, col_pub = st.columns([1, 1.5, 2])

            with col_info:
                st.markdown(f"""
                <div class="det-label">Email</div>
                <div class="det-valor">{email or 'Não informado'}</div>
                <div class="det-label" style="margin-top:0.65rem;">Lattes</div>
                <div style="margin-top:0.3rem;">
                    {'<a href="' + lattes_url + '" target="_blank" style="display:inline-block;padding:4px 12px;background:' + vermelho + ';color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>' if lattes_url else '<span style="font-size:0.82rem;color:' + cor_texto_terciario + ';">Não informado</span>'}
                </div>
                """, unsafe_allow_html=True)

            with col_proj:
                if is_thalia:
                    if proj_aluna or proj_docente:
                        if proj_aluna:
                            st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(proj_aluna)})</div>', unsafe_allow_html=True)
                            for p in proj_aluna:
                                cor_tipo = cores_projetos.get(p["tipo"], vermelho)
                                st.markdown(f"""
                                <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                    margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
                                    <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p['nome']}</span><br>
                                    <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p['tipo']}</span>
                                    <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p['periodo']}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        if proj_docente:
                            st.markdown("---")
                            st.markdown(f'<div class="det-label">Como professora ({len(proj_docente)})</div>', unsafe_allow_html=True)
                            for p in proj_docente:
                                cor_tipo = cores_projetos.get(p["tipo"], vermelho)
                                st.markdown(f"""
                                <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                    margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
                                    <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p['nome']}</span><br>
                                    <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p['tipo']}</span>
                                    <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p['periodo']}</span>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.caption("Nenhum projeto no período")
                else:
                    st.markdown(f'<div class="det-label">Projetos ({len(proj_docente)})</div>', unsafe_allow_html=True)
                    if proj_docente:
                        for p in proj_docente:
                            cor_tipo = cores_projetos.get(p["tipo"], vermelho)
                            st.markdown(f"""
                            <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
                                <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p['nome']}</span><br>
                                <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p['tipo']}</span>
                                <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p['periodo']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("Nenhum projeto no período")

            with col_pub:
                if is_thalia:
                    if pub_aluna or pub_docente:
                        if pub_aluna:
                            st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(pub_aluna)})</div>', unsafe_allow_html=True)
                            for p in pub_aluna:
                                link = str(p.get('link', '')).strip()
                                tem_link = pd.notna(p.get('link')) and link
                                alcance_cor = vermelho if p['alcance'] == "Internacional" else vermelho_claro
                                botao = (
                                    f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                    f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
                                    f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                                ) if tem_link else ''
                                card_publicacao(p, alcance_cor, botao)
                        if pub_docente:
                            st.markdown("---")
                            st.markdown(f'<div class="det-label">Como professora ({len(pub_docente)})</div>', unsafe_allow_html=True)
                            for p in pub_docente:
                                link = str(p.get('link', '')).strip()
                                tem_link = pd.notna(p.get('link')) and link
                                alcance_cor = vermelho if p['alcance'] == "Internacional" else vermelho_claro
                                botao = (
                                    f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                    f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
                                    f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                                ) if tem_link else ''
                                card_publicacao(p, alcance_cor, botao)
                    else:
                        st.caption("Nenhuma publicação no período")
                else:
                    st.markdown(f'<div class="det-label">Publicações ({len(pub_docente)})</div>', unsafe_allow_html=True)
                    if pub_docente:
                        for p in pub_docente:
                            link = str(p.get('link', '')).strip()
                            tem_link = pd.notna(p.get('link')) and link
                            alcance_cor = vermelho if p['alcance'] == "Internacional" else vermelho_claro
                            botao = (
                                f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
                                f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                            ) if tem_link else ''
                            card_publicacao(p, alcance_cor, botao)
                    else:
                        st.caption("Nenhuma publicação no período")

# ============================================================
# 8. ABA PROJETOS
# ============================================================
with aba_projetos:
    secao("Projetos por tipo")

    projetos_ensino = projetos_periodo[projetos_periodo["tipo"] == "Ensino"]
    projetos_pesquisa = projetos_periodo[projetos_periodo["tipo"] == "Pesquisa"]
    projetos_extensao = projetos_periodo[projetos_periodo["tipo"] == "Extensão"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ensino", len(projetos_ensino))
    with col2:
        st.metric("Pesquisa", len(projetos_pesquisa))
    with col3:
        st.metric("Extensão", len(projetos_extensao))

    st.markdown("---")

    if not projetos_periodo.empty:
        contagem_tipos = projetos_periodo.groupby("tipo").size().reset_index(name="quantidade")
        fig = px.bar(
            contagem_tipos, x="tipo", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Tipo de projeto", yaxis_title="Quantidade", showlegend=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    secao("Lista de projetos")

    for tipo_projeto in ["Ensino", "Pesquisa", "Extensão"]:
        projetos_tipo = projetos_periodo[projetos_periodo["tipo"] == tipo_projeto]
        if len(projetos_tipo) > 0:
            st.subheader(tipo_projeto)
            for _, projeto in projetos_tipo.iterrows():
                ano_ini_proj = projeto['ano_ini']
                ano_fim_proj = projeto.get('ano_fim')
                if pd.isna(ano_fim_proj) or ano_fim_proj == ano_ini_proj:
                    periodo_str = f"({ano_ini_proj})"
                else:
                    periodo_str = f"({ano_ini_proj} - {ano_fim_proj})"
                label = f"{projeto['nome']} {periodo_str}"

                with st.expander(label):
                    st.markdown(f"""
                    <div style="font-size:0.85rem; line-height:1.6;">
                        <strong>Equipe:</strong> {projeto.get('equipe', 'Não informado')}<br>
                        <strong>Período:</strong> {projeto['periodo']}<br>
                        <strong>Detalhes:</strong> {projeto.get('detalhes', '')}
                    </div>
                    """, unsafe_allow_html=True)

                    resumo = projeto.get('resumo', '')
                    if resumo:
                        st.markdown(f"""
                        <details style="margin-top:0.5rem;">
                            <summary style="cursor:pointer; color:{vermelho}; font-weight:600;">Ver resumo</summary>
                            <div style="background:#f5f5f5; padding:0.5rem 0.8rem; border-radius:6px; margin-top:0.3rem; font-size:0.85rem; line-height:1.6;">
                                {resumo}
                            </div>
                        </details>
                        """, unsafe_allow_html=True)

    st.markdown(
        f'<p class="fonte-site" style="margin-top: 1.5rem;">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/projetos" target="_blank">meninasdigitaisnocerrado.com.br/projetos</a></p>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    secao("Nuvem de palavras (baseada nos resumos dos projetos)")

    if not projetos_periodo.empty and projetos_periodo['resumo'].dropna().any():
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud
        import nltk
        nltk.download('stopwords', quiet=True)
        from nltk.corpus import stopwords as nltk_stopwords

        stopwords = set(nltk_stopwords.words('portuguese'))
        stopwords.update([
            'presente', 'assim', 'desta', 'sobre', 'forma', 'modo', 'além', 'disso', 'bem', 'tanto',
            'sendo', 'diante', 'meio', 'vista', 'quais', 'vistas', 'sentido', 'âmbito',
            'propõe', 'propõem', 'propor', 'objetiva', 'objetivo', 'intuito',
            'visa', 'busca', 'diversas', 'diversos', 'cada', 'todo', 'toda',
            'todos', 'todas', 'outro', 'outra', 'outros', 'outras', 'desde',
            'através', 'conforme', 'inclusive', 'ainda'
        ])

        texto_completo = ' '.join(projetos_periodo['resumo'].dropna().astype(str))
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=stopwords,
            max_words=80,
            colormap='Reds',
            collocations=False
        ).generate(texto_completo)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.info("Nenhum resumo disponível para gerar a nuvem.")

# ============================================================
# 9. ABA PUBLICAÇÕES
# ============================================================
with aba_publicacoes:
    secao("Publicações por ano")

    if not publicacoes_periodo.empty:
        pubs_por_ano = publicacoes_periodo.groupby("ano").size().reset_index(name="quantidade")

        fig = px.bar(
            pubs_por_ano, x="ano", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de publicações", showlegend=False,
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        secao("Publicações")

        pubs_por_alcance = publicacoes_periodo.groupby(["ano", "alcance"]).size().reset_index(name="quantidade")

        fig2 = px.bar(
            pubs_por_alcance, x="ano", y="quantidade", color="alcance",
            color_discrete_map={"Nacional": vermelho_claro, "Internacional": vermelho},
            text="quantidade", barmode="group"
        )
        fig2.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de publicações",
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        secao("Lista de publicações")

        for ano in sorted(publicacoes_periodo["ano"].unique(), reverse=True):
            pubs_ano = publicacoes_periodo[publicacoes_periodo["ano"] == ano]
            st.markdown(f"### {ano}")
            for _, pub in pubs_ano.iterrows():
                card_publicacao_lista(pub, vermelho, cor_texto, cor_texto_secundario)
    else:
        st.info("Nenhuma publicação no período selecionado.")

    st.markdown(
        f'<p class="fonte-site">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/publicacoes" target="_blank">meninasdigitaisnocerrado.com.br/publicacoes</a></p>',
        unsafe_allow_html=True,
    )

with aba_eventos:
    secao("Eventos e Premiações")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de eventos", len(eventos_periodo))
    with col2:
        st.metric("Total de premiações", len(premiacoes_periodo))

    # ============================================================
    # 1. CORRIGIR FUNÇÕES E AGRUPAR DUPLICATAS
    # ============================================================
    if not eventos_periodo.empty:
        eventos_periodo = eventos_periodo.copy()
        eventos_periodo['funcao'] = eventos_periodo['funcao'].replace('Promoção de eventos', 'Organização')
        eventos_periodo['funcao'] = eventos_periodo['funcao'].str.strip().str.title()
        eventos_periodo['funcao'] = eventos_periodo['funcao'].replace({
            'Participante': 'Participante',
            'Ouvinte': 'Ouvinte',
            'Organização': 'Organização'
        })
        eventos_periodo['link'] = eventos_periodo['link'].fillna('')

        eventos_agrupados = eventos_periodo.groupby(
            ['ano', 'nome', 'funcao', 'tipo_atividade', 'local'],
            as_index=False
        ).agg({
            'link': lambda x: '; '.join([l for l in x if l.strip() != ''])
        })
        eventos_agrupados['link'] = eventos_agrupados['link'].replace('', pd.NA)
        eventos_agrupados = eventos_agrupados.dropna(subset=['nome'])
        eventos_para_graficos = eventos_agrupados
    else:
        eventos_para_graficos = eventos_periodo

    # ============================================================
    # 2. LISTA DE EVENTOS POR CATEGORIA (PRIMEIRO NA PÁGINA)
    # ============================================================
    st.markdown("---")
    secao("Eventos por categoria")

    st.markdown(f"""
    <div style="background:#f5f5f5;border-radius:8px;padding:1rem;margin-bottom:1.5rem;font-size:0.85rem;color:#666;line-height:1.6;">
        <strong>Padrão adotado:</strong> As definições das funções foram estabelecidas conforme a padronização do Currículo Lattes:<br>
        • <strong>Organização:</strong> Atuação na organização e promoção do evento.<br>
        • <strong>Participante:</strong> Apresentação de trabalhos, publicação de artigos, palestras dadas ou condução de oficinas.<br>
        • <strong>Ouvinte:</strong> Presença no evento para assistir às apresentações e palestras.<br><br>
        <em>Nota: O tipo de atividade (como Construção Humana, Capacitação Tecnológica, Divulgação Científica, etc.) foram categorizados de acordo com a metodologia proposta no artigo:</em><br>
        <a href="https://sol.sbc.org.br/index.php/wit/article/view/6714/6610" target="_blank" style="color:{vermelho};font-weight:600;text-decoration:underline;">
            Agindo sobre a diferença: atividades de empoderamento feminino em prol da permanência de mulheres em cursos de Tecnologia da Informação
        </a>.
    </div>
    """, unsafe_allow_html=True)

    # Cores em tons de vermelho para as áreas MDC
    cores_mdc_vermelho = {
        'Capacitação Tecnológica': '#b71c1c',
        'Construção humana': '#c62828',
        'Divulgação Científica': '#d32f2f',
        'Representação e ampliação de alcance': '#e53935',
        'Promoção de eventos': '#880e4f'
    }

    for cat in [
        {"nome": "Organização", "funcao": "Organização"},
        {"nome": "Participante", "funcao": "Participante"},
        {"nome": "Ouvinte", "funcao": "Ouvinte"}
    ]:
        eventos_cat = eventos_para_graficos[eventos_para_graficos['funcao'] == cat['funcao']]
        if not eventos_cat.empty:
            eventos_cat = eventos_cat.sort_values(['ano', 'nome'], ascending=[False, True])
            label = f"{cat['nome']} ({len(eventos_cat)})"
            with st.expander(label):
                for _, evento in eventos_cat.iterrows():
                    # Área MDC com tom de vermelho
                    area = str(evento.get('tipo_atividade', '')).strip()
                    cor_area = cores_mdc_vermelho.get(area, '#ef5350')
                    badge_area = f'<span class="badge" style="background:{cor_area};color:#fff;">{area}</span>' if area and area != 'nan' else ''

                    # Badge do local com tom suave de vermelho
                    local = str(evento.get('local', '')).strip()
                    badge_local = f'<span class="badge" style="background:#ffebee;color:#c62828;border:1px solid #ffcdd2;">{local}</span>' if local and local != 'nan' else ''

                    badges = ' '.join(filter(None, [badge_local, badge_area]))

                    # Validação: só exibe o botão se houver link válido no CSV
                    link_bruto = str(evento.get('link', '')).strip()
                    botao_html = ''
                    if pd.notna(evento.get('link')) and link_bruto and link_bruto.lower() not in ['nan', 'none', '']:
                        links_validos = [
                            l.strip() for l in link_bruto.split(';') 
                            if l.strip() and l.strip().lower() not in ['nan', 'none', '']
                        ]
                        if links_validos:
                            botoes = [
                                f'<a href="{l}" target="_blank" style="display:inline-block;margin-top:0.3rem;margin-right:0.3rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:6px;font-size:0.7rem;font-weight:600;text-decoration:none;">Trabalho {idx+1 if len(links_validos) > 1 else ""}</a>'.replace('  ', ' ')
                                for idx, l in enumerate(links_validos)
                            ]
                            botao_html = f'<div style="margin-top:0.5rem;">{" ".join(botoes)}</div>'

                    st.markdown(f"""
                    <div style="background:#ffffff;border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.8rem;
                        border-left:5px solid {vermelho};box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                            <div style="font-weight:600;font-size:0.95rem;color:{cor_texto};flex:1;">
                                {evento['nome']}
                            </div>
                            <div style="font-size:0.75rem;color:{cor_texto_terciario};white-space:nowrap;margin-left:0.5rem;">
                                {int(evento['ano'])}
                            </div>
                        </div>
                        <div style="margin-top:0.2rem;display:flex;flex-wrap:wrap;gap:0.2rem;">
                            {badges}
                        </div>
                        {botao_html}
                    </div>
                    """, unsafe_allow_html=True)

    # ============================================================
    # 3. GRÁFICOS (EM SEGUIDA)
    # ============================================================
    st.markdown("---")
    secao("Indicadores e Gráficos de Eventos")

    if not eventos_para_graficos.empty and 'funcao' in eventos_para_graficos.columns:
        eventos_por_ano_funcao = eventos_para_graficos.groupby(['ano', 'funcao']).size().reset_index(name='quantidade')
        eventos_por_ano_funcao = eventos_por_ano_funcao.sort_values('ano')

        cores_funcao = {
            'Organização': '#c62828',
            'Ouvinte': '#e57373',
            'Participante': '#ef5350'
        }

        fig_func = px.bar(
            eventos_por_ano_funcao,
            x='ano',
            y='quantidade',
            color='funcao',
            barmode='group',
            color_discrete_map=cores_funcao,
            text='quantidade',
            title='Participações em eventos por função e ano'
        )
        fig_func.update_layout(
            height=400,
            paper_bgcolor=fundo,
            plot_bgcolor=fundo,
            xaxis_title='Ano',
            yaxis_title='Número de participações',
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig_func.update_traces(textposition='outside')
        st.plotly_chart(fig_func, use_container_width=True)

    if not eventos_para_graficos.empty and 'tipo_atividade' in eventos_para_graficos.columns:
        eventos_por_ano_tipo = eventos_para_graficos.groupby(['ano', 'tipo_atividade']).size().reset_index(name='quantidade')
        eventos_por_ano_tipo = eventos_por_ano_tipo.sort_values('ano')

        tipos = sorted(eventos_por_ano_tipo['tipo_atividade'].unique())
        from plotly import colors
        paleta_vermelhos = colors.sequential.Reds[3:]
        cores_tipo = {}
        for i, t in enumerate(tipos):
            cores_tipo[t] = paleta_vermelhos[i % len(paleta_vermelhos)]

        fig_tipo = px.bar(
            eventos_por_ano_tipo,
            x='ano',
            y='quantidade',
            color='tipo_atividade',
            barmode='group',
            color_discrete_map=cores_tipo,
            text='quantidade',
            title='Eventos por tipo de atividade e ano'
        )
        fig_tipo.update_layout(
            height=400,
            paper_bgcolor=fundo,
            plot_bgcolor=fundo,
            xaxis_title='Ano',
            yaxis_title='Número de eventos',
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig_tipo.update_traces(textposition='outside')
        st.plotly_chart(fig_tipo, use_container_width=True)

    # ============================================================
    # 4. PREMIAÇÕES
    # ============================================================
    st.markdown("---")
    secao("Premiações")

    if not premiacoes_periodo.empty:
        premiacoes_por_ano = premiacoes_periodo.groupby("ano").size().reset_index(name="quantidade")

        fig_premiacoes = px.bar(
            premiacoes_por_ano, x="ano", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade", title="Premiações conquistadas por ano"
        )
        fig_premiacoes.update_layout(
            height=450, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de premiações", showlegend=False,
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig_premiacoes.update_traces(textposition='outside')
        st.plotly_chart(fig_premiacoes, use_container_width=True)

        st.markdown("---")
        st.markdown("**Lista de premiações**")
        for _, premio in premiacoes_periodo.iterrows():
            st.markdown(f"""
            <div class="card-publicacao">
                <strong>{premio['premio']}</strong><br>
                <small>Ano: {premio['ano']} - {premio.get('descricao', '')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma premiação no período.")

    st.markdown(
        f'<p class="fonte-site" style="margin-top: 2rem;">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/premiacoes" target="_blank">meninasdigitaisnocerrado.com.br/premiacoes</a></p>',
        unsafe_allow_html=True,
    )
    
# ============================================================
# 11. ABA PARCERIAS
# ============================================================
with aba_parcerias:
    secao("Parcerias")

    if not parcerias.empty:
        import html

        for _, parceria in parcerias.iterrows():
            nome = str(parceria.get('nome', ''))
            descricao = str(parceria.get('descricao', '')).replace('\n', ' ')
            ano_ini = str(parceria.get('ano_ini', ''))
            ano_fim = str(parceria.get('ano_fim', ''))
            link = str(parceria.get('link', '')).strip()

            periodo = f"{ano_ini} - {ano_fim}" if ano_fim and ano_fim != 'nan' else ano_ini

            botao_link = ''
            if link and link != 'nan' and link != '':
                botao_link = f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.5rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:6px;font-size:0.7rem;font-weight:600;text-decoration:none;">Acessar site</a>'

            nome_escapado = html.escape(nome)
            descricao_escapada = html.escape(descricao)
            descricao_formatada = descricao_escapada.replace('\n', '<br>')

            html_card = (
                f'<div class="card-publicacao" style="margin-bottom:1.5rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
                f'<span class="alcance-badge" style="background:{vermelho};">{periodo}</span>'
                f'{botao_link}'
                f'</div>'
                f'<p style="margin:0.4rem 0 0.3rem;font-weight:500;color:{cor_texto};">{nome_escapado}</p>'
                f'<p style="margin:0.2rem 0 0;color:{cor_texto_secundario};line-height:1.6;">{descricao_formatada}</p>'
                f'</div>'
            )

            st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.info("Nenhuma parceria cadastrada.")

# ============================================================
# 12. ABA SOBRE
# ============================================================
with aba_sobre:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{vermelho} 0%,#8b0000 100%);
        border-radius:12px;padding:2rem 2.5rem;margin-bottom:1.5rem;color:#fff;">
        <div style="font-size:0.75rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
            opacity:0.8;margin-bottom:0.4rem;">EDITAL Nº 11 de 03 de abril de 2025 - PIBIC</div>
        <div style="font-size:1.6rem;font-weight:700;line-height:1.2;margin-bottom:0.5rem;">
            Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado
    """, unsafe_allow_html=True)

    secao("Sobre o projeto")
    st.markdown(f"""
    <div style="background:{fundo_card};border-radius:10px;padding:1.5rem 2rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);line-height:1.8;color:{cor_texto};font-size:0.95rem;">
        O presente projeto de pesquisa celebra os <strong>10 anos do Meninas Digitais no Cerrado</strong>,
        iniciativa do IF Goiano - Campus Ceres e projeto parceiro do
        <strong>Programa Meninas Digitais (PMD)</strong> que busca incentivar a participação de
        meninas e mulheres nos cursos de Computação.
        <br><br>
        A proposta consiste na construção de uma <strong>base de dados aberta sobre gênero e
        Computação</strong> no âmbito do Campus Ceres. Espera-se sistematizar e visualizar a
        evolução da participação das mulheres na área de tecnologia, promovendo
        <strong>transparência e visibilidade</strong> do projeto e do campus, permitindo integrar
        e sistematizar informações dispersas inerentes ao recorte de gênero.
        <br><br>
        O projeto encontra-se em consonância com outro projeto maior, aprovado via
        <strong>Chamada Pública CNPq/MCTI/Mulheres nº 31/2023</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    secao("Equipe")
    col_bol, col_coord = st.columns(2)

    with col_bol:
        st.markdown(f"""
        <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:4px solid {vermelho};">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;color:{vermelho};margin-bottom:0.5rem;">Bolsista PIBIC</div>
            <div style="font-size:1.05rem;font-weight:700;color:{cor_texto};">Sara Luiz de Farias</div>
            <div style="font-size:0.82rem;color:{cor_texto_secundario};margin-top:0.25rem;">
                Bacharelanda em Sistemas de Informação<br>
                IF Goiano - Campus Ceres<br>
                <a href="http://lattes.cnpq.br/2013698994793152" target="_blank"
                    style="display:inline-block;margin-top:0.4rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_coord:
        st.markdown(f"""
        <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:4px solid {vermelho};">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;color:{vermelho};margin-bottom:0.5rem;">Coordenadora</div>
            <div style="font-size:1.05rem;font-weight:700;color:{cor_texto};">Profa. Thalia Santos de Santana</div>
            <div style="font-size:0.82rem;color:{cor_texto_secundario};margin-top:0.25rem;">
                Docente em Computação<br>
                IF Goiano - Campus Ceres<br>
                <a href="http://lattes.cnpq.br/8063677996827079" target="_blank"
                    style="display:inline-block;margin-top:0.4rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    secao("Como citar o dashboard")
    st.markdown(f"""
    <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);border-left:4px solid {vermelho};">
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
            color:{cor_texto_secundario};margin-bottom:0.75rem;">Citação no texto</div>
        <div style="font-size:0.88rem;color:{cor_texto};background:#f9f9f9;border-radius:6px;
            padding:0.5rem 0.8rem;margin-bottom:1rem;">
            (Meninas Digitais no Cerrado, 2026)
        </div>
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
            color:{cor_texto_secundario};margin-bottom:0.5rem;">Referência bibliográfica completa</div>
        <div style="font-size:0.88rem;color:{cor_texto};line-height:1.8;">
            MENINAS DIGITAIS NO CERRADO.
            <em>Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado.</em>
            Ceres: IF Goiano - Campus Ceres, 2026.
            Disponível em:
            <a href="https://meninasdigitaisnocerrado.com.br/indicadores" target="_blank"
                style="color:{vermelho};">meninasdigitaisnocerrado.com.br</a>.
            Acesso em: dia mes e ano.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    secao("Como usar")
    st.markdown(f"""
    <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);border-left:4px solid {vermelho};">
        Acesse o repositório no GitHub para instruções de instalação e execução do projeto.<br><br>
        <a href="https://github.com/saraafariass/ic2026" target="_blank"
            style="display:inline-block;padding:6px 16px;background:{vermelho};color:#fff;
            border-radius:5px;font-size:0.82rem;font-weight:600;text-decoration:none;">
            Ver no GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    secao("Tecnologias utilizadas")
    tecnologias = [
        ("Python", "Linguagem principal"),
        ("Streamlit", "Interface web interativa"),
        ("Pandas", "Manipulação de dados"),
        ("Plotly", "Gráficos interativos"),
    ]
    cols = st.columns(len(tecnologias))
    for col, (nome, desc) in zip(cols, tecnologias):
        col.markdown(f"""
        <div style="background:{fundo_card};border-radius:8px;padding:0.75rem 1rem;
            box-shadow:0 1px 2px rgba(0,0,0,0.06);text-align:center;">
            <div style="font-weight:700;font-size:0.88rem;color:{cor_texto};">{nome}</div>
            <div style="font-size:0.72rem;color:{cor_texto_secundario};margin-top:3px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 13. RODAPÉ
# ============================================================
st.markdown("---")
st.markdown(
    f'<p class="fonte-site" style="text-align: center;">Última atualização: {datetime.now().strftime("%d/%m/%Y")}</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="fonte-site" style="text-align: center;">Feito com <3 por Sara Farias (Meninas Digitais no Cerrado)</p>',
    unsafe_allow_html=True,
)