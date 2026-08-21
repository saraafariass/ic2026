import streamlit as st
import plotly.express as px
from assets.styles import vermelho, vermelho_claro, cor_texto, cor_texto_secundario, fundo
from utils.components import secao, card_publicacao_lista

def render(publicacoes_periodo):
    secao("Publicações por ano")

    if not publicacoes_periodo.empty:
        pubs_por_ano = publicacoes_periodo.groupby("ano").size().reset_index(name="quantidade")
        fig = px.bar(
            pubs_por_ano, x="ano", y="quantidade", color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"], text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de publicações", showlegend=False,
            xaxis=dict(tickmode="linear", dtick=1)
        )
        fig.update_traces(textposition="outside")
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
            xaxis=dict(tickmode="linear", dtick=1)
        )
        fig2.update_traces(textposition="outside")
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
        '<p class="fonte-site">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/publicacoes" target="_blank">meninasdigitaisnocerrado.com.br/publicacoes</a></p>',
        unsafe_allow_html=True,
    )