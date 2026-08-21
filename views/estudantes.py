import streamlit as st
import pandas as pd
import plotly.express as px
from assets.styles import vermelho, cor_texto_secundario, fundo
from utils.components import secao, renderizar_projetos, renderizar_publicacoes
from utils.helpers import (
    filtrar_alunas_periodo, lista_cursos, badge_curso,
    separar_por_papel, nome_sem_prefixos
)

def render(alunas, projetos_periodo, publicacoes_periodo, docentes_df, ano_inicio, ano_fim, filtro_curso, filtro_verticalizou, filtro_bolsista):
    secao("Participação no Projeto Meninas Digitais no Cerrado")

    alunas_periodo = filtrar_alunas_periodo(alunas, ano_inicio, ano_fim)
    alunas_filtradas = alunas_periodo.copy()

    if filtro_curso == "Técnico":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: "Técnico" in str(x))]
    elif filtro_curso == "Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: any(g in str(x) for g in ["Graduação", "Licenciatura", "Bacharelado"]))]
    elif filtro_curso == "Técnico e Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: "Técnico" in str(x) and any(g in str(x) for g in ["Graduação", "Licenciatura", "Bacharelado"]))]

    if filtro_verticalizou != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["verticalizou"] == filtro_verticalizou]

    if filtro_bolsista != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["bolsista"] == filtro_bolsista]

    alunas_tecnico = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: any("Técnico" in c for c in lista_cursos(x)))]
    alunas_graduacao = alunas_filtradas[alunas_filtradas["curso"].apply(lambda x: any(any(g in c for g in ["Graduação", "Licenciatura", "Bacharelado"]) for c in lista_cursos(x)))]

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
    total_graduacao = len(alunas_graduacao)
    bolsistas_graduacao = len(alunas_graduacao[alunas_graduacao["bolsista"] == "Sim"]) if not alunas_graduacao.empty and "bolsista" in alunas_graduacao.columns else 0
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de alunas", total_graduacao)
    with col2:
        st.metric("Bolsistas", bolsistas_graduacao)

    alunas_tec_e_grad = alunas_filtradas[
        alunas_filtradas["curso"].apply(lambda x: any("Técnico" in c for c in lista_cursos(x))) &
        alunas_filtradas["curso"].apply(lambda x: any(any(g in c for g in ["Graduação", "Licenciatura", "Bacharelado"]) for c in lista_cursos(x)))
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
    total_filtradas = len(alunas_filtradas)
    total_geral = len(alunas_periodo)
    if total_filtradas == total_geral:
        st.markdown(f'<p class="resultados-info">{total_geral} estudantes no período</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="resultados-info">Exibindo {total_filtradas} de {total_geral} estudantes no período</p>', unsafe_allow_html=True)

    if alunas_filtradas.empty:
        st.markdown('<div class="sem-resultado">Nenhuma estudante encontrada com os filtros selecionados.</div>', unsafe_allow_html=True)
    else:
        for _, aluna in alunas_filtradas.iterrows():
            proj_aluna, proj_docente, pub_aluna, pub_docente, eh_aluna = separar_por_papel(
                aluna["nome"], projetos_periodo, publicacoes_periodo, alunas, docentes_df, ano_inicio, ano_fim
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
            is_thalia = "thalia" in nome_base

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

    secao("Indicadores de Raça")
    if not alunas_filtradas.empty and "raca" in alunas_filtradas.columns:
        contagem_raca = alunas_filtradas["raca"].value_counts().reset_index()
        contagem_raca.columns = ["Raça/Etnia", "Quantidade"]
        fig_raca = px.pie(
            contagem_raca, names="Raça/Etnia", values="Quantidade",
            color_discrete_sequence=["#e57373", "#c62828", "#b71c1c", "#880e4f", "#4a148c"]
        )
        fig_raca.update_layout(height=400, paper_bgcolor=fundo, plot_bgcolor=fundo, showlegend=True)
        st.plotly_chart(fig_raca, use_container_width=True)

    secao("Indicadores de Curso")
    if not alunas_filtradas.empty:
        contagem_cursos = {}
        alunas_contadas = set()
        for _, aluna in alunas_filtradas.iterrows():
            id_aluna = f"{aluna['nome']}_{aluna['periodo']}"
            if id_aluna not in alunas_contadas:
                alunas_contadas.add(id_aluna)
                cursos = lista_cursos(aluna["curso"])
                for curso in cursos:
                    if "Técnico em Informática para Internet" in curso:
                        curso_norm = "Técnico em Informática para Internet"
                    elif "Técnico em Informática" in curso:
                        curso_norm = "Técnico em Informática"
                    elif "Técnico em Agropecuária" in curso:
                        curso_norm = "Técnico em Agropecuária"
                    elif "Técnico em Inteligência Artificial" in curso:
                        curso_norm = "Técnico em Inteligência Artificial"
                    elif "Licenciatura em Química" in curso:
                        curso_norm = "Licenciatura em Química"
                    elif "Bacharelado em Sistemas de Informação" in curso:
                        curso_norm = "Bacharelado em Sistemas de Informação"
                    else:
                        curso_norm = curso
                    contagem_cursos[curso_norm] = contagem_cursos.get(curso_norm, 0) + 1

        if contagem_cursos:
            df_cursos = pd.DataFrame([{"Curso": c, "Quantidade": q} for c, q in contagem_cursos.items()])
            fig_curso = px.pie(
                df_cursos, names="Curso", values="Quantidade",
                color_discrete_sequence=["#e57373", "#c62828", "#b71c1c", "#880e4f", "#4a148c", "#311b92"]
            )
            fig_curso.update_layout(height=400, paper_bgcolor=fundo, plot_bgcolor=fundo, showlegend=True)
            st.plotly_chart(fig_curso, use_container_width=True)