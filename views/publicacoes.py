import streamlit as st
import plotly.express as px
from plotly import colors

from assets.styles import vermelho, vermelho_claro, cor_texto, cor_texto_secundario, fundo
from utils.components import secao, card_publicacao_lista

def render(publicacoes_periodo):
    secao("Publicações por ano")

    if not publicacoes_periodo.empty:
        # 1. Total por Ano
        pubs_por_ano = publicacoes_periodo.groupby("ano").size().reset_index(name="quantidade")
        pubs_por_ano = pubs_por_ano.sort_values("ano")
        pubs_por_ano["ano_str"] = pubs_por_ano["ano"].astype(str)

        anos = pubs_por_ano["ano_str"].tolist()
        paleta_vermelhos = colors.sequential.Reds[3:]
        cores_ano = {ano: paleta_vermelhos[i % len(paleta_vermelhos)] for i, ano in enumerate(anos)}

        max_y_ano = pubs_por_ano["quantidade"].max()

        fig = px.bar(
            pubs_por_ano, x="ano", y="quantidade", color="ano_str",
            color_discrete_map=cores_ano, text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de publicações", showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            xaxis=dict(tickmode="linear", dtick=1, showgrid=False),
            yaxis=dict(
                showgrid=False,
                range=[0, max_y_ano * 1.2 if max_y_ano > 0 else 1]
            )
        )
        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        secao("Publicações por alcance e ano")

        # 2. Por Alcance - Nacional vs Internacional
        pubs_por_alcance = publicacoes_periodo.groupby(["ano", "alcance"]).size().reset_index(name="quantidade")
        max_y_alcance = pubs_por_alcance["quantidade"].max()

        fig2 = px.bar(
            pubs_por_alcance.sort_values("ano"), x="ano", y="quantidade", color="alcance",
            color_discrete_map={"Nacional": "#e57373", "Internacional": "#c62828"},
            text="quantidade", barmode="group",
        )
        fig2.update_layout(
            height=420, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de publicações",
            legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=20, l=20, r=20),
            xaxis=dict(tickmode="linear", dtick=1, showgrid=False),
            yaxis=dict(
                showgrid=False,
                range=[0, max_y_alcance * 1.25 if max_y_alcance > 0 else 1]
            )
        )
        fig2.update_traces(
            textposition="outside",
            cliponaxis=False
        )
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