import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="MDC · Gênero na Computação")

COR_VERMELHO = "#c62828"
COR_VERMELHO_GRAFICO = "#e57373"
TEXTO = "#212121"
TEXTO_SECUNDARIO = "#616161"
TEXTO_TERCIARIO = "#9e9e9e"
FUNDO = "#f5f5f5"
CARD = "#ffffff"

st.markdown(f"""
<style>
    .main {{ background: {FUNDO}; }}
    h1 {{
        color: {TEXTO}; font-weight: 700; font-size: 1.85rem;
        letter-spacing: -0.02em; margin-bottom: 0.25rem;
    }}
    [data-testid="stCaption"] {{ color: {TEXTO_SECUNDARIO} !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 1px solid #e0e0e0; }}
    .stTabs [data-baseweb="tab"] {{
        height: 44px; padding: 0 1.1rem; background: {CARD};
        border-radius: 8px 8px 0 0; font-weight: 600;
        color: {TEXTO_SECUNDARIO}; border: 1px solid #e0e0e0; border-bottom: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: {COR_VERMELHO}; color: #fff; border-color: {COR_VERMELHO};
    }}
    .kpi {{
        border-radius: 10px; padding: 1rem 1.2rem;
        border-left: 4px solid {COR_VERMELHO};
        background: {CARD};
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    }}
    .kpi-rotulo {{
        font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.05em; color: {TEXTO_SECUNDARIO}; margin-bottom: 0.4rem;
    }}
    .kpi-valor {{
        font-size: 2rem; font-weight: 700; color: {TEXTO}; line-height: 1.1;
    }}
    .secao {{
        color: {TEXTO}; font-size: 1.1rem; font-weight: 600;
        padding-bottom: 0.4rem; margin: 1.5rem 0 0.85rem 0;
        border-bottom: 2px solid {COR_VERMELHO};
    }}
    .sidebar-titulo {{
        font-size: 1.05rem; font-weight: 700; color: {TEXTO}; margin: 0;
    }}
    .sidebar-marca {{
        font-size: 0.8rem; color: {COR_VERMELHO}; font-weight: 600; margin-top: 0.15rem;
    }}
    .filtro-titulo {{
        font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.06em; color: {TEXTO_SECUNDARIO}; margin: 1rem 0 0.25rem 0;
    }}
    .fonte-site {{ font-size: 0.78rem; color: {TEXTO_TERCIARIO}; margin-top: 0.75rem; }}
    .fonte-site a {{ color: {COR_VERMELHO}; font-weight: 500; text-decoration: none; }}
    .fonte-site a:hover {{ text-decoration: underline; }}
    hr {{ border-color: #e0e0e0; margin: 1.5rem 0; }}
    [data-testid="stSidebar"] {{
        background: {CARD}; border-right: 1px solid #e0e0e0;
    }}
    [data-testid="stMarkdown"] strong {{ color: {TEXTO}; }}
    .card-projeto {{
        background: {CARD};
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid {COR_VERMELHO};
    }}
    .card-publicacao {{
        background: {CARD};
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid {COR_VERMELHO_GRAFICO};
    }}
    .ano-badge {{
        background-color: {COR_VERMELHO};
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        display: inline-block;
        margin-right: 0.5rem;
    }}
    .alcance-badge {{
        background-color: {COR_VERMELHO_GRAFICO};
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        display: inline-block;
    }}
    .autor-link {{
        color: {COR_VERMELHO};
        text-decoration: none;
        font-weight: 500;
    }}
    .autor-link:hover {{
        text-decoration: underline;
    }}
    .card-evento {{
        background: {CARD};
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .numero-grande {{
        font-size: 2rem;
        font-weight: 700;
        color: {COR_VERMELHO};
    }}
    .chart-container {{
        background: {CARD};
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)


def secao(titulo):
    st.markdown(f'<p class="secao">{titulo}</p>', unsafe_allow_html=True)


def kpi(col, rotulo, valor):
    col.markdown(
        f"""<div class="kpi">
            <div class="kpi-rotulo">{rotulo}</div>
            <div class="kpi-valor">{valor}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def filtrar_periodo(df, ano_ini, ano_fim):
    return df[(df["ano_ini"] <= ano_fim) & (df["ano_fim"] >= ano_ini)]


@st.cache_data
def carregar_dados():
    alunas = pd.read_csv("alunas.csv")
    alunas["ano_conclusao"] = pd.to_numeric(alunas["ano_conclusao"], errors="coerce")
    return (
        alunas,
        pd.read_csv("docentes.csv"),
        pd.read_csv("projetos.csv"),
        pd.read_csv("publicacoes.csv"),
        pd.read_csv("premiacoes.csv"),
        pd.read_csv("eventos.csv"),
    )


def alunas_no_periodo(alunas, ano_ini, ano_fim, cursos):
    ativas = alunas["ano_conclusao"].isna()
    concluiu_no_periodo = alunas["ano_conclusao"].between(ano_ini, ano_fim)
    ingressou_antes_fim = alunas["ano_ingresso"] <= ano_fim
    mask = ingressou_antes_fim & (ativas | concluiu_no_periodo) & alunas["curso"].isin(cursos)
    return alunas[mask]


def criar_nuvem_palavras(projetos_df):
    textos = []
    for _, projeto in projetos_df.iterrows():
        texto = f"{projeto['nome']} {projeto.get('detalhes', '')}"
        textos.append(texto)
    
    if not textos:
        return None
    
    texto_completo = " ".join(textos)
    
    nuvem = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='Reds',
        max_words=50,
        collocations=False
    ).generate(texto_completo)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(nuvem, interpolation='bilinear')
    ax.axis('off')
    return fig


def linkar_autores_com_projetos(projetos_df, docentes_df):
    st.markdown("### Autores e seus projetos")
    
    for _, docente in docentes_df.iterrows():
        nome = docente['nome']
        email = docente.get('email', '')
        lattes = docente.get('lattes', '')
        
        st.markdown(f"**{nome}**")
        if email:
            st.markdown(f"Email: {email}")
        if lattes:
            st.markdown(f"Lattes: {lattes}")
        
        st.markdown("Projetos participantes:")
        for _, projeto in projetos_df.iterrows():
            if nome in str(projeto.get('autores', '')):
                st.markdown(f"- {projeto['nome']} ({projeto['tipo']}, {projeto['periodo']})")
        st.markdown("---")


alunas, docentes, projetos, publicacoes, premiacoes, eventos = carregar_dados()

# Definir anos fixos de 2016 a 2026
ano_min, ano_max = 2016, 2026

# Cursos específicos
cursos_disponiveis = [
    "Ensino Médio Técnico em Inteligência Artificial",
    "Ensino Médio Técnico em Informatica para Internet",
    "Ensino Médio Técnico em Informatica",
    "Bacharelado em Sistemas de Informação"
]

st.sidebar.markdown(
    '<p class="sidebar-titulo">Meninas Digitais no Cerrado</p>'
    '<p class="sidebar-marca">MDC · 10 anos</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="filtro-titulo">Filtrar por ano</p>', unsafe_allow_html=True)
ano_ini, ano_fim = st.sidebar.slider(
    "Período", 2016, 2026, (2016, 2026), label_visibility="collapsed",
)
st.sidebar.markdown('<p class="filtro-titulo">Filtrar cursos</p>', unsafe_allow_html=True)
cursos_selecionados = st.sidebar.multiselect(
    "Cursos", cursos_disponiveis, default=cursos_disponiveis, label_visibility="collapsed",
)

if st.sidebar.button("Atualizar dados do site"):
    import subprocess
    import sys
    subprocess.run([sys.executable, "atualizar_dados_site.py"], check=True)
    st.cache_data.clear()
    st.rerun()

if not cursos_selecionados:
    st.warning("Selecione ao menos um curso na barra lateral.")
    st.stop()

# Filtrar alunas apenas pelos cursos selecionados
alunas_filtradas = alunas[alunas["curso"].isin(cursos_selecionados)]
alunas_periodo = alunas_no_periodo(alunas_filtradas, ano_ini, ano_fim, cursos_selecionados)

# Separar alunas por tipo de curso
cursos_medio = [c for c in cursos_selecionados if "Ensino Médio" in c]
cursos_graduacao = ["Bacharelado em Sistemas de Informação"] if "Bacharelado em Sistemas de Informação" in cursos_selecionados else []

alunas_medio = alunas_periodo[alunas_periodo["curso"].isin(cursos_medio)]
alunas_graduacao = alunas_periodo[alunas_periodo["curso"].isin(cursos_graduacao)]

formadas_medio = alunas_medio[alunas_medio["status"] == "Formada"]
formadas_graduacao = alunas_graduacao[alunas_graduacao["status"] == "Formada"]

projetos_periodo = filtrar_periodo(projetos, ano_ini, ano_fim)
publicacoes_periodo = publicacoes[publicacoes["ano"].between(ano_ini, ano_fim)]
premiacoes_periodo = premiacoes[premiacoes["ano"].between(ano_ini, ano_fim)]
eventos_periodo = eventos[eventos["ano"].between(ano_ini, ano_fim)]

st.title("Sistematização de Dados: Gênero na Computação")
st.caption(f"Período {ano_ini} a {ano_fim} · {len(cursos_selecionados)} curso(s)")

# Abas principais
tab_est, tab_doc, tab_projetos, tab_pub, tab_eventos, tab_parcerias, tab_sobre = st.tabs([
    "Estudantes", "Docentes", "Projetos", "Publicações", "Eventos e Premiações", "Parcerias", "Sobre e Citação"
])

# ==================== ABA ESTUDANTES ====================
with tab_est:
    st.subheader("Ensino Médio Técnico")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de alunas no período", len(alunas_medio))
    with col2:
        st.metric("Alunas formadas", len(formadas_medio))
    with col3:
        st.metric("Verticalizaram para graduação", int(formadas_medio["verticalizou"].sum()) if len(formadas_medio) > 0 else 0)
    
    st.markdown("---")
    
    st.subheader("Bacharelado em Sistemas de Informação")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de alunas no período", len(alunas_graduacao))
    with col2:
        st.metric("Alunas formadas", len(formadas_graduacao))
    with col3:
        st.metric("Bolsistas", int(formadas_graduacao["bolsista"].sum()) if len(formadas_graduacao) > 0 else 0)
    
    st.markdown("---")
    secao("Mulheres por curso")
    
    # Gráfico de barras horizontal mais bonito com plotly
    if len(alunas_periodo) > 0:
        por_curso = alunas_periodo.groupby("curso").size().reset_index(name="quantidade")
        por_curso = por_curso.sort_values("quantidade", ascending=True)
        
        fig = px.bar(
            por_curso,
            x="quantidade",
            y="curso",
            orientation='h',
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor=FUNDO,
            plot_bgcolor=FUNDO,
            xaxis_title="Número de alunas",
            yaxis_title="",
            showlegend=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma aluna no período selecionado.")

# ==================== ABA DOCENTES ====================
with tab_doc:
    secao("Corpo docente")
    
    st.metric("Total de docentes", len(docentes))
    
    st.markdown("---")
    
    for _, docente in docentes.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card-projeto">
                <strong>{docente['nome']}</strong><br>
                <small>Email: {docente.get('email', 'Não informado')}</small><br>
                <small>Lattes: <a href="{docente.get('lattes', '#')}" target="_blank">{docente.get('lattes', 'Não informado')}</a></small>
            </div>
            """, unsafe_allow_html=True)
    
    secao("Relacionamento docentes e projetos")
    linkar_autores_com_projetos(projetos_periodo, docentes)

# ==================== ABA PROJETOS ====================
with tab_projetos:
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
        # Gráfico de barras com plotly
        tipos_count = projetos_periodo.groupby("tipo").size().reset_index(name="quantidade")
        fig = px.bar(
            tipos_count,
            x="tipo",
            y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400,
            paper_bgcolor=FUNDO,
            plot_bgcolor=FUNDO,
            xaxis_title="Tipo de projeto",
            yaxis_title="Quantidade",
            showlegend=False
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
                st.markdown(f"""
                <div class="card-projeto">
                    <strong>{projeto['nome']}</strong><br>
                    Período: {projeto['periodo']}<br>
                    Detalhes: {projeto.get('detalhes', '')}<br>
                    <small>Autores: {projeto.get('autores', 'Não informado')}</small>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    secao("Nuvem de palavras dos projetos")
    
    fig_nuvem = criar_nuvem_palavras(projetos_periodo)
    if fig_nuvem:
        st.pyplot(fig_nuvem)
    else:
        st.info("Nenhum projeto no período para gerar nuvem de palavras.")
    
    st.markdown(
        f'<p class="fonte-site">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/projetos" target="_blank">meninasdigitaisnocerrado.com.br/projetos</a></p>',
        unsafe_allow_html=True,
    )

# ==================== ABA PUBLICAÇÕES ====================
with tab_pub:
    secao("Publicações por ano")
    
    if not publicacoes_periodo.empty:
        # Gráfico de barras com valores mostrados
        pubs_por_ano = publicacoes_periodo.groupby("ano").size().reset_index(name="quantidade")
        
        fig = px.bar(
            pubs_por_ano,
            x="ano",
            y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400,
            paper_bgcolor=FUNDO,
            plot_bgcolor=FUNDO,
            xaxis_title="Ano",
            yaxis_title="Número de publicações",
            showlegend=False,
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        secao("Publicações por alcance")
        
        pubs_por_alcance = publicacoes_periodo.groupby(["ano", "alcance"]).size().reset_index(name="quantidade")
        
        fig2 = px.bar(
            pubs_por_alcance,
            x="ano",
            y="quantidade",
            color="alcance",
            color_discrete_map={"Nacional": COR_VERMELHO_GRAFICO, "Internacional": COR_VERMELHO},
            text="quantidade",
            barmode="group"
        )
        fig2.update_layout(
            height=400,
            paper_bgcolor=FUNDO,
            plot_bgcolor=FUNDO,
            xaxis_title="Ano",
            yaxis_title="Número de publicações",
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        secao("Lista de publicações")
        
        # Mostrar publicações agrupadas por ano de forma mais limpa
        for ano in sorted(publicacoes_periodo["ano"].unique(), reverse=True):
            pubs_ano = publicacoes_periodo[publicacoes_periodo["ano"] == ano]
            st.markdown(f"### {ano}")
            for _, pub in pubs_ano.iterrows():
                st.markdown(f"""
                <div class="card-publicacao">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span class="alcance-badge">{pub['alcance']}</span>
                    </div>
                    <p style="margin: 0.5rem 0; font-weight: 500;">{pub.get('referencia', '')}</p>
                    <small style="color: {TEXTO_SECUNDARIO};">Autores: {pub.get('autores', 'Não informado')}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma publicação no período selecionado.")
    
    st.markdown(
        f'<p class="fonte-site">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/publicacoes" target="_blank">meninasdigitaisnocerrado.com.br/publicacoes</a></p>',
        unsafe_allow_html=True,
    )

# ==================== ABA EVENTOS E PREMIAÇÕES ====================
with tab_eventos:
    col1, col2 = st.columns(2)
    
    with col1:
        secao("Eventos participados")
        
        if not eventos_periodo.empty:
            # Mostrar total de participações
            total_participacoes = eventos_periodo["quantidade"].sum()
            st.markdown(f"""
            <div class="card-evento">
                <div class="numero-grande">{int(total_participacoes)}</div>
                <p>participações em eventos</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Gráfico de participações por ano
            eventos_por_ano = eventos_periodo.groupby("ano")["quantidade"].sum().reset_index()
            
            fig = px.line(
                eventos_por_ano,
                x="ano",
                y="quantidade",
                markers=True,
                line_shape="spline"
            )
            fig.update_traces(line_color=COR_VERMELHO, marker_color=COR_VERMELHO, marker_size=10)
            fig.update_layout(
                height=350,
                paper_bgcolor=FUNDO,
                plot_bgcolor=FUNDO,
                xaxis_title="Ano",
                yaxis_title="Número de participações",
                xaxis=dict(tickmode='linear', dtick=1)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar dados em cards por ano
            st.markdown("---")
            st.markdown("**Participações por ano**")
            
            cols = st.columns(min(5, len(eventos_por_ano)))
            for i, row in eventos_por_ano.iterrows():
                with cols[i % 5]:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div class="numero-grande" style="font-size: 1.5rem;">{int(row['quantidade'])}</div>
                        <small>{int(row['ano'])}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Nenhum evento registrado no período.")
    
    with col2:
        secao("Premiações")
        
        if not premiacoes_periodo.empty:
            total_premiacoes = len(premiacoes_periodo)
            st.markdown(f"""
            <div class="card-evento">
                <div class="numero-grande">{total_premiacoes}</div>
                <p>premiações conquistadas</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Gráfico de premiações por ano
            premiacoes_por_ano = premiacoes_periodo.groupby("ano").size().reset_index(name="quantidade")
            
            fig2 = px.bar(
                premiacoes_por_ano,
                x="ano",
                y="quantidade",
                color="quantidade",
                color_continuous_scale=["#e57373", "#c62828"],
                text="quantidade"
            )
            fig2.update_layout(
                height=350,
                paper_bgcolor=FUNDO,
                plot_bgcolor=FUNDO,
                xaxis_title="Ano",
                yaxis_title="Número de premiações",
                showlegend=False,
                xaxis=dict(tickmode='linear', dtick=1)
            )
            fig2.update_traces(textposition='outside')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Lista de premiações em formato compacto
            st.markdown("---")
            st.markdown("**Premiações conquistadas**")
            
            for _, premio in premiacoes_periodo.iterrows():
                st.markdown(f"""
                <div class="card-publicacao">
                    <strong>{premio['premio']}</strong><br>
                    <small>{premio['ano']} - {premio.get('descricao', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma premiação no período.")
    
    st.markdown(
        f'<p class="fonte-site" style="margin-top: 2rem;">Fonte: <a href="https://meninasdigitaisnocerrado.com.br" target="_blank">meninasdigitaisnocerrado.com.br</a></p>',
        unsafe_allow_html=True,
    )

# ==================== ABA PARCERIAS ====================
with tab_parcerias:
    secao("Instituições parceiras")
    
    try:
        parcerias = pd.read_csv("parcerias.csv")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de parcerias", len(parcerias))
        with col2:
            st.metric("Parcerias acadêmicas", len(parcerias[parcerias["tipo"] == "Acadêmica"]) if "tipo" in parcerias.columns else 0)
        with col3:
            st.metric("Parcerias institucionais", len(parcerias[parcerias["tipo"] == "Institucional"]) if "tipo" in parcerias.columns else 0)
        
        st.markdown("---")
        
        for _, parceria in parcerias.iterrows():
            st.markdown(f"""
            <div class="card-projeto">
                <strong>{parceria['instituicao']}</strong><br>
                Tipo: {parceria.get('tipo', 'Não informado')}<br>
                Atividade: {parceria.get('atividade', 'Não informado')}<br>
                Contato: {parceria.get('contato', 'Não informado')}
            </div>
            """, unsafe_allow_html=True)
    except:
        st.info("Nenhuma parceria cadastrada no momento.")
    
    st.markdown(
        f'<p class="fonte-site">Para mais informações sobre parcerias, acesse o site oficial do projeto.</p>',
        unsafe_allow_html=True,
    )

# ==================== ABA SOBRE E CITAÇÃO ====================
with tab_sobre:
    secao("Sobre o projeto Meninas Digitais no Cerrado")
    
    st.markdown("""
    O projeto Meninas Digitais no Cerrado é uma iniciativa que busca incentivar a participação feminina nas áreas de Computação e Tecnologia da Informação.
    
    **Objetivos do projeto:**
    - Estimular o interesse de meninas e mulheres por carreiras em TI
    - Reduzir a desigualdade de gênero na área da Computação
    - Criar uma rede de apoio e mentoria para mulheres na tecnologia
    - Documentar e sistematizar dados sobre a participação feminina na área
    
    **Público-alvo:**
    Estudantes do Ensino Médio Técnico e da Graduação em Computação, principalmente nos cursos de Bacharelado em Sistemas de Informação.
    """)
    
    st.markdown("---")
    secao("Como citar este trabalho - Normas ABNT")
    
    st.markdown("""
    **Citação no texto:**
    
    (MENINAS DIGITAIS NO CERRADO, ano)
    
    **Referência bibliográfica completa:**
    
    MENINAS DIGITAIS NO CERRADO. Sistematização de Dados: Gênero na Computação. 
    [S.l.], ano. Disponível em: https://meninasdigitaisnocerrado.com.br. 
    Acesso em: dia mês ano.
    
    **Exemplo prático:**
    
    MENINAS DIGITAIS NO CERRADO. Sistematização de Dados: Gênero na Computação. 
    2024. Disponível em: https://meninasdigitaisnocerrado.com.br. 
    Acesso em: 15 maio 2024.
    
    **Para citar um projeto específico:**
    
    MENINAS DIGITAIS NO CERRADO. "Nome do projeto". In: Sistematização de Dados: 
    Gênero na Computação. ano. Disponível em: URL do site. Acesso em: dia mês ano.
    """)
    
    st.markdown("---")
    secao("Desenvolvimento do site")
    
    st.markdown("""
    Este site foi desenvolvido como parte da sistematização de dados do projeto Meninas Digitais no Cerrado.
    
    **Tecnologias utilizadas:**
    - Python com Streamlit para a interface
    - Pandas para manipulação de dados
    - Plotly para gráficos interativos
    - WordCloud para visualização de palavras
    
    A base de dados é atualizada periodicamente a partir das informações coletadas pelo projeto.
    """)

st.markdown("---")
st.markdown(
    '<p class="fonte-site" style="text-align: center;">Meninas Digitais no Cerrado · Dados sistematizados para pesquisa sobre gênero na computação</p>',
    unsafe_allow_html=True,
)