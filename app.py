import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Configuração da Página
st.set_page_config(layout="wide", page_title="Portal de Dados MDC")

# 2. Estilização CSS (Fundo cinza, Cards brancos e detalhes em Vermelho)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #d32f2f;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        gap: 1px;
        padding-top: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #ff5252; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Carregamento de Dados
# Certifique-se de que o arquivo dados_dashboard.csv está na mesma pasta
df = pd.read_csv("dados_dashboard.csv")

# 4. BARRA LATERAL (Filtros Estilo Analisa UFG)
st.sidebar.title("MDC - 10 ANOS")
st.sidebar.markdown("---")
anos_selecionados = st.sidebar.slider("Período de Análise", 2016, 2025, (2016, 2025))
cursos_disponiveis = df['Curso_ou_Projeto'].unique()
cursos_selecionados = st.sidebar.multiselect("Filtrar Cursos", cursos_disponiveis, default=cursos_disponiveis)

# Filtragem Global baseada nos inputs da sidebar
mask = (df['Ano'].between(anos_selecionados[0], anos_selecionados[1])) & (df['Curso_ou_Projeto'].isin(cursos_selecionados))
df_filtered = df[mask]

# 5. CONTEÚDO PRINCIPAL
st.title("Sistematização de Dados: Gênero na Computação")

# Card de Resumo Principal (Widget de topo)
total_mulheres = df_filtered[df_filtered['Categoria'] == 'Estudantes']['Quantidade_Mulheres'].sum()
st.metric(label="Total de Estudantes Mulheres no Período", value=int(total_mulheres))

# Divisão por ABAS (Conforme os Objetivos do Projeto)
tab_est, tab_pes, tab_prod = st.tabs(["🎓 Estudantes", "👩‍🏫 Pessoas", "🚀 Produção e Ações"])

# --- ABA 1: ESTUDANTES ---
with tab_est:
    # Linha 1: Distribuição e Permanência
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.write("### Distribuição por Curso")
        df_dist = df_filtered[(df_filtered['Categoria'] == 'Estudantes') & (df_filtered['Indicador'] == 'Ingressantes')]
        st.bar_chart(df_dist, x="Curso_ou_Projeto", y="Quantidade_Mulheres", color="#d32f2f", horizontal=True)

    with c2:
        st.write("### Taxa de Permanência")
        df_perm = df_filtered[df_filtered['Indicador'] == 'Taxa de Permanência']
        if not df_perm.empty:
            avg_perm = df_perm['Quantidade_Mulheres'].mean()
            source = pd.DataFrame({"Categoria": ["Permanência", "Evasão"], "Valor": [avg_perm, 100-avg_perm]})
            plot = alt.Chart(source).mark_arc(innerRadius=50).encode(
                theta="Valor", color=alt.Color("Categoria", scale=alt.Scale(range=["#d32f2f", "#eeeeee"]))
            )
            st.altair_chart(plot, use_container_width=True)
            st.write(f"Média: {avg_perm:.1f}%")

    # Linha 2: Ingressantes vs Concluintes e Verticalização
    c3, c4 = st.columns([2, 1])
    with c3:
        st.write("### Ingressantes vs. Concluintes")
        fluxo = df_filtered[df_filtered['Indicador'].isin(['Ingressantes', 'Concluintes'])]
        st.line_chart(fluxo, x="Ano", y="Quantidade_Mulheres", color="Indicador")
    
    with c4:
        st.write("### Verticalização")
        total_vert = df_filtered[df_filtered['Indicador'] == 'Verticalização']['Quantidade_Mulheres'].sum()
        st.metric("Total Verticalização", int(total_vert))
        st.progress(min(int(total_vert * 5), 100)) # Simulação visual de progresso

# --- ABA 2: PESSOAS ---
with tab_pes:
    st.subheader("Corpo Docente e Histórico de Bolsistas")
    p1, p2 = st.columns(2)
    with p1:
        docentes = df_filtered[df_filtered['Indicador'] == 'Corpo Docente']['Quantidade_Mulheres'].sum()
        st.metric("Professoras de TI", int(docentes))
    with p2:
        bolsistas = df_filtered[df_filtered['Indicador'] == 'Histórico de Bolsistas']['Quantidade_Mulheres'].sum()
        st.metric("Bolsistas MDC", int(bolsistas))
    st.dataframe(df_filtered[df_filtered['Categoria'] == 'Pessoas'], use_container_width=True)

# --- ABA 3: PRODUÇÃO E AÇÕES ---
with tab_prod:
    st.subheader("Impacto Acadêmico e Científico")
    
    # Cards de Projetos (Ensino, Pesquisa e Extensão)
    pr1, pr2, pr3 = st.columns(3)
    pr1.metric("Ensino", int(df_filtered[df_filtered['Indicador'] == 'Projeto de Ensino']['Quantidade_Mulheres'].sum()))
    pr2.metric("Pesquisa", int(df_filtered[df_filtered['Indicador'] == 'Projeto de Pesquisa']['Quantidade_Mulheres'].sum()))
    pr3.metric("Extensão", int(df_filtered[df_filtered['Indicador'] == 'Projeto de Extensão']['Quantidade_Mulheres'].sum()))
    
    st.markdown("---")
    st.subheader("🚀 Mineração de Palavras-Chave (10 anos de MDC)")
    
    # Geração da Nuvem de Palavras a partir da coluna 'Detalhes'
    textos = df_filtered[df_filtered['Categoria'] == 'Produção e Ações']['Detalhes'].dropna().tolist()
    
    if textos:
        texto_unificado = " ".join(textos)
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='Reds', # Degradê vermelho
            max_words=50
        ).generate(texto_unificado)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("Sem dados textuais suficientes para gerar a nuvem de palavras.")