import streamlit as st
import pandas as pd
import plotly.express as px
from assets.styles import (
    vermelho, cor_texto_secundario, fundo,
    cores_raca, cores_cursos
)
from utils.components import secao, renderizar_projetos, renderizar_publicacoes
from utils.helpers import (
    filtrar_alunas_periodo, lista_cursos, badge_curso,
    separar_por_papel, nome_sem_prefixos
)

def render(alunas, projetos_periodo, publicacoes_periodo, docentes_df, ano_inicio, ano_fim, filtro_curso, filtro_verticalizou, filtro_bolsista):
    secao("Participação no projeto Meninas Digitais no Cerrado")

    alunas_periodo = filtrar_alunas_periodo(alunas, ano_inicio, ano_fim)
    alunas_filtradas = alunas_periodo.copy()

    # Filtro de Curso
    if filtro_curso == "Técnico":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].astype(str).str.contains("Técnico", case=False, na=False)]
    elif filtro_curso == "Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: any(g.lower() in str(x).lower() for g in ["Graduação", "Licenciatura", "Bacharelado"]))]
    elif filtro_curso == "Técnico e Graduação":
        alunas_filtradas = alunas_filtradas[
            alunas_filtradas["curso"].astype(str).str.contains("Técnico", case=False, na=False) &
            alunas_filtradas["curso"].apply(lambda x: any(g.lower() in str(x).lower() for g in ["Graduação", "Licenciatura", "Bacharelado"]))
        ]

    # Filtro de Verticalização
    if filtro_verticalizou != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["verticalizou"].astype(str).str.strip().str.lower() == filtro_verticalizou.strip().lower()]

    # Filtro de Bolsista
    if filtro_bolsista != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["bolsista"].astype(str).str.strip().str.lower() == filtro_bolsista.strip().lower()]

    alunas_tecnico = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: any("Técnico" in c for c in lista_cursos(x)))]
    alunas_graduacao = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: any(any(g in c for g in ["Graduação", "Licenciatura", "Bacharelado"]) for c in lista_cursos(x)))]

    # Métricas Ensino Médio Técnico
    st.markdown("### Ensino Médio Técnico")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de alunas", len(alunas_tecnico))
    with col2:
        verticalizou_count = len(alunas_tecnico[alunas_tecnico["verticalizou"].astype(str).str.strip().str.lower() == "sim"]) if not alunas_tecnico.empty and "verticalizou" in alunas_tecnico.columns else 0
        st.metric("Verticalizaram", verticalizou_count)
    with col3:
        bolsistas_count = len(alunas_tecnico[alunas_tecnico["bolsista"].astype(str).str.strip().str.lower() == "sim"]) if not alunas_tecnico.empty and "bolsista" in alunas_tecnico.columns else 0
        st.metric("Bolsistas", bolsistas_count)

    st.markdown("---")
    # Métricas Graduação
    st.markdown("### Bacharelado em Sistemas de Informação")
    total_graduacao = len(alunas_graduacao)
    bolsistas_graduacao = len(alunas_graduacao[alunas_graduacao["bolsista"].astype(str).str.strip().str.lower() == "sim"]) if not alunas_graduacao.empty and "bolsista" in alunas_graduacao.columns else 0
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de alunas", total_graduacao)
    with col2:
        st.metric("Bolsistas", bolsistas_graduacao)

    # Identifica alunas presentes em ambas as categorias
    alunas_tec_e_grad = alunas_filtradas[
        alunas_filtradas["curso"].apply(lambda x: any("Técnico" in c for c in lista_cursos(x))) &
        alunas_filtradas["curso"].apply(lambda x: any(any(g in c for g in ["Graduação", "Licenciatura", "Bacharelado"]) for c in lista_cursos(x)))
    ]

    st.markdown("---")
    total_filtradas = len(alunas_filtradas)
    st.markdown(f'<p class="resultados-info">{total_filtradas} estudantes no período</p>', unsafe_allow_html=True)

    # Listagem de Estudantes
    if alunas_filtradas.empty:
        st.markdown('<div class="sem-resultado">Nenhuma estudante encontrada com os filtros selecionados.</div>', unsafe_allow_html=True)
    else:
        for _, aluna in alunas_filtradas.iterrows():
            proj_aluna, proj_docente, pub_aluna, pub_docente, eh_aluna = separar_por_papel(
                aluna["nome"], projetos_periodo, publicacoes_periodo, alunas, docentes_df, ano_inicio, ano_fim
            )

            vert_val = aluna.get("verticalizou", "")
            vert_display = "Não se aplica" if pd.isna(vert_val) or str(vert_val).strip() == "" else vert_val

            badges_html = badge_curso(aluna.get("curso", ""))
            if str(aluna.get("bolsista", "")).strip().lower() == "sim":
                badges_html += ' <span class="badge badge-bols">Bolsista</span>'
            if str(vert_val).strip().lower() == "sim":
                badges_html += ' <span class="badge badge-vert">Verticalizou</span>'

            label = f"{aluna['nome']} ({aluna.get('curso', '')}: {aluna.get('periodo', '')})"
            nome_base = nome_sem_prefixos(aluna['nome'])
            is_thalia = "thalia" in nome_base

            with st.expander(label):
                st.markdown(f'<div style="margin-bottom:0.5rem;">{badges_html}</div>', unsafe_allow_html=True)
                col_info, col_proj, col_pub = st.columns([1, 1.5, 2])

                with col_info:
                    st.markdown(f"""
                    <div class="det-label">Bolsista</div>
                    <div class="det-valor">{aluna.get('bolsista', 'Não informado')}</div>
                    <div class="det-label">Verticalizou</div>
                    <div class="det-valor">{vert_display}</div>
                    <div class="det-label">Curso</div>
                    <div class="det-valor">{aluna.get('curso', 'Não informado')}</div>
                    """, unsafe_allow_html=True)
                    observacao = str(aluna.get("observacao", "")).strip()
                    if observacao and observacao != "nan":
                        st.markdown(f"""
                        <div class="det-label" style="margin-top:0.65rem;">Observação</div>
                        <div class="det-valor" style="font-size:0.8rem;color:{cor_texto_secundario};">{observacao}</div>
                        """, unsafe_allow_html=True)

                with col_proj:
                    if is_thalia:
                        st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(proj_aluna)})</div>', unsafe_allow_html=True)
                        renderizar_projetos(proj_aluna)
                        st.markdown("---")
                        st.markdown(f'<div class="det-label">Como professora ({len(proj_docente)})</div>', unsafe_allow_html=True)
                        renderizar_projetos(proj_docente)
                    else:
                        st.markdown(f'<div class="det-label">Projetos ({len(proj_aluna)})</div>', unsafe_allow_html=True)
                        renderizar_projetos(proj_aluna)

                with col_pub:
                    if is_thalia:
                        st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(pub_aluna)})</div>', unsafe_allow_html=True)
                        renderizar_publicacoes(pub_aluna)
                        st.markdown("---")
                        st.markdown(f'<div class="det-label">Como professora ({len(pub_docente)})</div>', unsafe_allow_html=True)
                        renderizar_publicacoes(pub_docente)
                    else:
                        st.markdown(f'<div class="det-label">Publicações ({len(pub_aluna)})</div>', unsafe_allow_html=True)
                        renderizar_publicacoes(pub_aluna)

    # Observação inserida ao final da listagem de estudantes
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

    # Indicadores de Raça
    secao("Indicadores de raça")
    if not alunas_filtradas.empty and "raca" in alunas_filtradas.columns:
        alunas_unicas = alunas_filtradas.drop_duplicates(subset=["nome"])
        dados_raca = alunas_unicas["raca"].dropna()
        dados_raca = dados_raca[dados_raca.astype(str).str.strip() != ""]
        
        if not dados_raca.empty:
            contagem_raca = dados_raca.value_counts().reset_index()
            contagem_raca.columns = ["Raça/Etnia", "Quantidade"]
            
            max_x_raca = contagem_raca["Quantidade"].max()

            fig_raca = px.bar(
                contagem_raca,
                y="Raça/Etnia",
                x="Quantidade",
                orientation="h",
                color="Raça/Etnia",
                color_discrete_map=cores_raca,
                text="Quantidade"
            )
            fig_raca.update_layout(
                height=260,
                paper_bgcolor=fundo,
                plot_bgcolor=fundo,
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=40),
                xaxis=dict(
                    title="Número de estudantes",
                    dtick=2,
                    showgrid=False,
                    range=[0, max_x_raca * 1.15]
                ),
                yaxis=dict(title=None, showgrid=False, autorange="reversed")
            )
            fig_raca.update_traces(
                textposition="outside",
                cliponaxis=False
            )
            st.plotly_chart(fig_raca, use_container_width=True)
        else:
            st.info("Nenhum dado de raça disponível para a seleção atual.")
    else:
        st.info("Nenhum dado disponível para a seleção atual.")

    secao("Indicadores de curso")
    if not alunas_filtradas.empty:
        contagem_cursos = {}
        for _, aluna in alunas_filtradas.iterrows():
            cursos = lista_cursos(aluna.get("curso", ""))
            for curso in cursos:
                if "Informática para Internet" in curso:
                    curso_norm = "Técnico em Informática para Internet"
                elif "Técnico em Informática" in curso:
                    curso_norm = "Técnico em Informática"
                elif "Agropecuária" in curso:
                    curso_norm = "Técnico em Agropecuária"
                elif "Inteligência Artificial" in curso:
                    curso_norm = "Técnico em Inteligência Artificial"
                elif "Química" in curso:
                    curso_norm = "Licenciatura em Química"
                elif "Sistemas de Informação" in curso:
                    curso_norm = "Bacharelado em Sistemas de Informação"
                else:
                    curso_norm = curso
                contagem_cursos[curso_norm] = contagem_cursos.get(curso_norm, 0) + 1

        if contagem_cursos:
            df_cursos = pd.DataFrame([{"Curso": c, "Quantidade": q} for c, q in contagem_cursos.items()])
            df_cursos = df_cursos.sort_values(by="Quantidade", ascending=False)

            max_y_curso = df_cursos["Quantidade"].max()

            fig_curso = px.bar(
                df_cursos,
                x="Curso",
                y="Quantidade",
                color="Curso",
                color_discrete_map=cores_cursos,
                text="Quantidade"
            )
            fig_curso.update_layout(
                height=420,
                paper_bgcolor=fundo,
                plot_bgcolor=fundo,
                showlegend=False,
                margin=dict(t=50, b=20, l=20, r=20),
                xaxis=dict(title=None, tickangle=-15, showgrid=False),
                yaxis=dict(
                    title="Número de estudantes",
                    dtick=5,
                    showgrid=False,
                    range=[0, max_y_curso * 1.18]
                )
            )
            fig_curso.update_traces(
                textposition="outside",
                cliponaxis=False
            )
            st.plotly_chart(fig_curso, use_container_width=True)
        else:
            st.info("Nenhum dado de curso disponível para a seleção atual.")
    else:
        st.info("Nenhum dado disponível para a seleção atual.")