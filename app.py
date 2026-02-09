import streamlit as st
import pandas as pd

# Carregar dados
df = pd.read_csv("dados_dashboard.csv")

st.title("Dashboards: 10 anos de Meninas Digitais no Cerrado")

# Criando as abas conforme o seu projeto
tab1, tab2, tab3 = st.tabs(["Estudantes", "Pessoas", "Produção e Ações"])

# --- ABA ESTUDANTES ---
with tab1:
    st.subheader("Fluxo Acadêmico e Distribuição")
    # Filtro de curso para Ingressantes vs Concluintes
    fluxo = df[(df['Categoria'] == 'Estudantes') & (df['Indicador'].isin(['Ingressantes', 'Concluintes']))]
    st.bar_chart(fluxo, x='Ano', y='Quantidade_Mulheres', color='Indicador')
    
    # Taxa de Permanência e Verticalização
    st.write("Taxa de Permanência e Verticalização (Superior)")
    extra = df[(df['Categoria'] == 'Estudantes') & (df['Indicador'].isin(['Taxa de Permanência', 'Verticalização']))]
    st.line_chart(extra, x='Ano', y='Quantidade_Mulheres', color='Indicador')

# --- ABA PESSOAS ---
with tab2:
    st.subheader("Corpo Docente e Histórico de Bolsistas")
    pessoas = df[df['Categoria'] == 'Pessoas']
    st.dataframe(pessoas[['Ano', 'Indicador', 'Quantidade_Mulheres', 'Detalhes']])

# --- ABA PRODUÇÃO E AÇÕES ---
with tab3:
    st.subheader("Eventos, Projetos e Produção Científica")
    acoes = df[df['Categoria'] == 'Produção e Ações']
    # Aqui você pode usar a coluna 'Detalhes' para gerar a Nuvem de Palavras
    st.write("Palavras-chave da Produção Científica:", ", ".join(acoes['Detalhes'].dropna().unique()[:10]))
    st.bar_chart(acoes[acoes['Indicador'].str.contains('Projeto')], x='Ano', y='Quantidade_Mulheres', color='Indicador')