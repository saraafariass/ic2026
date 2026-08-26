import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import colors

from assets.styles import vermelho, cor_texto, cor_texto_terciario, fundo
from utils.components import secao

def render(eventos_periodo, premiacoes_periodo):
    secao("Eventos e Premiações")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de atividades", len(eventos_periodo))
    with col2:
        st.metric("Total de premiações", len(premiacoes_periodo))

    if not eventos_periodo.empty:
        eventos_periodo = eventos_periodo.copy()
        
        # Garante a existência da coluna categoria mapeando a partir de funcao, se necessário
        col_cat = "categoria" if "categoria" in eventos_periodo.columns else "funcao"
        eventos_periodo["categoria"] = eventos_periodo[col_cat].replace("Promoção de eventos", "Organização")
        eventos_periodo["categoria"] = eventos_periodo["categoria"].str.strip().str.title()
        eventos_periodo["link"] = eventos_periodo["link"].fillna("")

        eventos_agrupados = eventos_periodo.groupby(
            ["ano", "nome", "categoria", "tipo_atividade", "local"],
            as_index=False
        ).agg({
            "link": lambda x: "; ".join([l for l in x if l.strip() != ""])
        })
        eventos_agrupados["link"] = eventos_agrupados["link"].replace("", pd.NA)
        eventos_agrupados = eventos_agrupados.dropna(subset=["nome"])
        eventos_para_graficos = eventos_agrupados
    else:
        eventos_para_graficos = eventos_periodo

    st.markdown("---")
    secao("Eventos por categoria")

    st.markdown(f"""
    <div style="background:#f5f5f5;border-radius:8px;padding:1rem;margin-bottom:1.5rem;font-size:0.85rem;color:#666;line-height:1.6;">
        <strong>Padrão adotado:</strong> As definições das categorias foram estabelecidas conforme a padronização do Currículo Lattes:<br>
        • <strong>Organização:</strong> Atuação na organização e promoção do evento.<br>
        • <strong>Participante:</strong> Apresentação de trabalhos, publicação de artigos, palestras dadas ou condução de oficinas.<br>
        • <strong>Ouvinte:</strong> Presença no evento para assistir às apresentações e palestras.<br><br>
        <em>Nota: O tipo de atividade foi categorizado de acordo com a metodologia proposta no artigo:</em><br>
        <a href="https://sol.sbc.org.br/index.php/wit/article/view/6714/6610" target="_blank" style="color:{vermelho};font-weight:600;text-decoration:underline;">
            Agindo sobre a diferença: atividades de empoderamento feminino em prol da permanência de mulheres em cursos de Tecnologia da Informação
        </a>.
    </div>
    """, unsafe_allow_html=True)

    cores_mdc_vermelho = {
        "Capacitação Tecnológica": "#b71c1c",
        "Construção humana": "#c62828",
        "Divulgação Científica": "#d32f2f",
        "Representação e ampliação de alcance": "#e53935",
        "Promoção de eventos": "#880e4f"
    }

    for cat in [
        {"nome": "Organização", "categoria": "Organização"},
        {"nome": "Participante", "categoria": "Participante"},
        {"nome": "Ouvinte", "categoria": "Ouvinte"}
    ]:
        eventos_cat = eventos_para_graficos[eventos_para_graficos["categoria"] == cat["categoria"]]
        if not eventos_cat.empty:
            eventos_cat = eventos_cat.sort_values(["ano", "nome"], ascending=[False, True])
            label = f"{cat['nome']} ({len(eventos_cat)})"
            with st.expander(label):
                for _, evento in eventos_cat.iterrows():
                    area = str(evento.get("tipo_atividade", "")).strip()
                    cor_area = cores_mdc_vermelho.get(area, "#ef5350")
                    badge_area = f'<span class="badge" style="background:{cor_area};color:#fff;">{area}</span>' if area and area != "nan" else ""

                    local = str(evento.get("local", "")).strip()
                    badge_local = f'<span class="badge" style="background:#ffebee;color:#c62828;border:1px solid #ffcdd2;">{local}</span>' if local and local != "nan" else ""

                    badges = " ".join(filter(None, [badge_local, badge_area]))

                    link_bruto = str(evento.get("link", "")).strip()
                    botao_html = ""
                    if pd.notna(evento.get("link")) and link_bruto and link_bruto.lower() not in ["nan", "none", ""]:
                        links_validos = [l.strip() for l in link_bruto.split(";") if l.strip() and l.strip().lower() not in ["nan", "none", ""]]
                        if links_validos:
                            botoes = [
                                f'<a href="{l}" target="_blank" style="display:inline-block;margin-top:0.3rem;margin-right:0.3rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:6px;font-size:0.7rem;font-weight:600;text-decoration:none;">Trabalho {idx+1 if len(links_validos) > 1 else ""}</a>'.replace("  ", " ")
                                for idx, l in enumerate(links_validos)
                            ]
                            botao_html = f'<div style="margin-top:0.5rem;">{" ".join(botoes)}</div>'

                    st.markdown(f"""
                    <div style="background:#ffffff;border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.8rem;
                        border-left:5px solid {vermelho};box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                            <div style="font-weight:600;font-size:0.95rem;color:{cor_texto};flex:1;">{evento['nome']}</div>
                            <div style="font-size:0.75rem;color:{cor_texto_terciario};white-space:nowrap;margin-left:0.5rem;">{int(evento['ano'])}</div>
                        </div>
                        <div style="margin-top:0.2rem;display:flex;flex-wrap:wrap;gap:0.2rem;">{badges}</div>
                        {botao_html}
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    secao("Participações em eventos por categoria e ano")

    # 1. Gráfico por Categoria
    if not eventos_para_graficos.empty and "categoria" in eventos_para_graficos.columns:
        eventos_por_ano_cat = eventos_para_graficos.groupby(["ano", "categoria"]).size().reset_index(name="quantidade")
        max_y_cat = eventos_por_ano_cat["quantidade"].max()

        fig_cat = px.bar(
            eventos_por_ano_cat.sort_values("ano"), x="ano", y="quantidade", color="categoria", barmode="group",
            color_discrete_map={"Organização": "#c62828", "Ouvinte": "#e57373", "Participante": "#ef5350"},
            text="quantidade"
        )
        fig_cat.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de participações",
            legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=20, l=20, r=20),
            xaxis=dict(tickmode="linear", dtick=1, showgrid=False),
            yaxis=dict(
                showgrid=False,
                range=[0, max_y_cat * 1.22 if max_y_cat > 0 else 1]
            )
        )
        fig_cat.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
        
    st.markdown("---")
    secao("Eventos por tipo de atividade e ano")

    # 2. Gráfico por Tipo de Atividade
    if not eventos_para_graficos.empty and "tipo_atividade" in eventos_para_graficos.columns:
        eventos_por_ano_tipo = eventos_para_graficos.groupby(["ano", "tipo_atividade"]).size().reset_index(name="quantidade")
        tipos = sorted(eventos_por_ano_tipo["tipo_atividade"].unique())
        paleta_vermelhos = colors.sequential.Reds[3:]
        cores_tipo = {t: paleta_vermelhos[i % len(paleta_vermelhos)] for i, t in enumerate(tipos)}
        max_y_tipo = eventos_por_ano_tipo["quantidade"].max()

        fig_tipo = px.bar(
            eventos_por_ano_tipo.sort_values("ano"), x="ano", y="quantidade", color="tipo_atividade", barmode="group",
            color_discrete_map=cores_tipo, text="quantidade"
        )
        fig_tipo.update_layout(
            height=400, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de eventos",
            legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=20, l=20, r=20),
            xaxis=dict(tickmode="linear", dtick=1, showgrid=False),
            yaxis=dict(
                showgrid=False,
                range=[0, max_y_tipo * 1.22 if max_y_tipo > 0 else 1]
            )
        )
        fig_tipo.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        st.plotly_chart(fig_tipo, use_container_width=True)

    st.markdown("---")
    secao("Premiações conquistadas por ano")

    # 3. Gráfico de Premiações
    if not premiacoes_periodo.empty:
        premiacoes_por_ano = premiacoes_periodo.groupby("ano").size().reset_index(name="quantidade")
        premiacoes_por_ano["ano_str"] = premiacoes_por_ano["ano"].astype(str)
        max_y_prem = premiacoes_por_ano["quantidade"].max()

        # Paleta de vermelhos alinhada ao projeto
        anos_prem = premiacoes_por_ano["ano_str"].tolist()
        paleta_vermelhos_prem = ["#f57c5f", "#ee583f", "#e52b20", "#bf1313", "#930c10", "#4a0304"]
        cores_prem = {ano: paleta_vermelhos_prem[i % len(paleta_vermelhos_prem)] for i, ano in enumerate(anos_prem)}

        fig_premiacoes = px.bar(
            premiacoes_por_ano, x="ano", y="quantidade", color="ano_str",
            color_discrete_map=cores_prem, text="quantidade"
        )
        fig_premiacoes.update_layout(
            height=450, paper_bgcolor=fundo, plot_bgcolor=fundo,
            xaxis_title="Ano", yaxis_title="Número de premiações", showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            xaxis=dict(tickmode="linear", dtick=1, showgrid=False),
            yaxis=dict(
                showgrid=False,
                range=[0, max_y_prem * 1.2 if max_y_prem > 0 else 1]
            )
        )
        fig_premiacoes.update_traces(
            textposition="outside",
            cliponaxis=False
        )
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