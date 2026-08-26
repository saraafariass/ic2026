import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords as nltk_stopwords
import random

from assets.styles import vermelho, fundo, cores_projetos
from utils.components import secao

@st.cache_resource
def carregar_stopwords():
    nltk.download("stopwords", quiet=True)
    sw = set(nltk_stopwords.words("portuguese"))
    sw.update([
        "presente", "nesse", "nessa", "assim", "desta", "sobre", "forma", "modo", "além", "disso", "bem", "tanto",
        "sendo", "diante", "meio", "vista", "quais", "vistas", "sentido", "âmbito",
        "propõe", "propõem", "propor", "objetiva", "objetivo", "intuito",
        "visa", "busca", "diversas", "diversos", "cada", "todo", "toda",
        "todos", "todas", "outro", "outra", "outros", "outras", "desde",
        "através", "conforme", "inclusive", "ainda"
    ])
    return sw

def paleta_nuvem_escura(word, font_size, position, orientation, random_state=None, **kwargs):
    tons_grafico = [
        "#f57c5f", "#ee583f", "#e52b20", "#bf1313", "#930c10", "#4a0304"
    ]
    return random.choice(tons_grafico)

def render(projetos_periodo):
    secao("Projetos por tipo")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ensino", len(projetos_periodo[projetos_periodo["tipo"] == "Ensino"]))
    with col2:
        st.metric("Pesquisa", len(projetos_periodo[projetos_periodo["tipo"] == "Pesquisa"]))
    with col3:
        st.metric("Extensão", len(projetos_periodo[projetos_periodo["tipo"] == "Extensão"]))

    st.markdown("---")

    if not projetos_periodo.empty:
        contagem_tipos = projetos_periodo.groupby("tipo").size().reset_index(name="quantidade")
        max_y_proj = contagem_tipos["quantidade"].max()

        fig = px.bar(
            contagem_tipos, x="tipo", y="quantidade", color="tipo",
            color_discrete_map=cores_projetos, text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Tipo de projeto", yaxis_title="Quantidade", showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=False,
                range=[0, max_y_proj * 1.2 if max_y_proj > 0 else 1]
            )
        )
        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    secao("Lista de projetos")

    for tipo_projeto in ["Ensino", "Pesquisa", "Extensão"]:
        projetos_tipo = projetos_periodo[projetos_periodo["tipo"] == tipo_projeto]
        if len(projetos_tipo) > 0:
            st.subheader(tipo_projeto)
            for _, projeto in projetos_tipo.iterrows():
                ano_ini_proj = projeto["ano_ini"]
                ano_fim_proj = projeto.get("ano_fim")
                periodo_str = f"({ano_ini_proj})" if (pd.isna(ano_fim_proj) or ano_fim_proj == ano_ini_proj) else f"({ano_ini_proj} - {ano_fim_proj})"
                label = f"{projeto['nome']} {periodo_str}"

                with st.expander(label):
                    st.markdown(f"""
                    <div style="font-size:0.85rem; line-height:1.6;">
                        <strong>Equipe:</strong> {projeto.get('equipe', 'Não informado')}<br>
                        <strong>Período:</strong> {projeto['periodo']}<br>
                        <strong>Detalhes:</strong> {projeto.get('detalhes', '')}
                    </div>
                    """, unsafe_allow_html=True)
                    resumo = projeto.get("resumo", "")
                    if resumo:
                        st.markdown(f"""
                        <details style="margin-top:0.5rem;">
                            <summary style="cursor:pointer; color:{vermelho}; font-weight:600; font-size:0.85rem;">Ver resumo</summary>
                            <div style="background:#f5f5f5; padding:0.5rem 0.8rem; border-radius:6px; margin-top:0.3rem; font-size:0.85rem; line-height:1.6;">
                                {resumo}
                            </div>
                        </details>
                        """, unsafe_allow_html=True)

    st.markdown(
        '<p class="fonte-site" style="margin-top: 1.5rem;">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/projetos" target="_blank">meninasdigitaisnocerrado.com.br/projetos</a></p>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    secao("Nuvem de palavras (baseada nos resumos dos projetos)")

    if not projetos_periodo.empty and projetos_periodo["resumo"].dropna().any():
        stopwords = carregar_stopwords()
        texto_completo = " ".join(projetos_periodo["resumo"].dropna().astype(str))
        wordcloud = WordCloud(
            width=800, height=400, background_color="white",
            stopwords=stopwords, max_words=80, color_func=paleta_nuvem_escura,
            collocations=False
        ).generate(texto_completo)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Nenhum resumo disponível para gerar a nuvem.")