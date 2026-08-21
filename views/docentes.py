import streamlit as st
from assets.styles import vermelho, cor_texto_terciario
from utils.components import secao, renderizar_projetos, renderizar_publicacoes
from utils.helpers import separar_por_papel, nome_sem_prefixos

def render(docentes, alunas, projetos_periodo, publicacoes_periodo, ano_inicio, ano_fim):
    secao("Corpo docente")
    st.metric("Total de docentes", len(docentes))
    st.markdown("---")

    for _, docente in docentes.iterrows():
        proj_aluna, proj_docente, pub_aluna, pub_docente, eh_aluna = separar_por_papel(
            docente["nome"], projetos_periodo, publicacoes_periodo, alunas, docentes, ano_inicio, ano_fim
        )

        lattes_url = str(docente.get("lattes", "")).strip()
        email = docente.get("email", "")
        nome_exibido = nome_sem_prefixos(docente["nome"]).title()
        is_thalia = "thalia" in nome_exibido.lower()

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
                    st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(proj_aluna)})</div>', unsafe_allow_html=True)
                    renderizar_projetos(proj_aluna)
                    st.markdown("---")
                    st.markdown(f'<div class="det-label">Como professora ({len(proj_docente)})</div>', unsafe_allow_html=True)
                    renderizar_projetos(proj_docente)
                else:
                    st.markdown(f'<div class="det-label">Projetos ({len(proj_docente)})</div>', unsafe_allow_html=True)
                    renderizar_projetos(proj_docente)

            with col_pub:
                if is_thalia:
                    st.markdown(f'<div class="det-label" style="color:{vermelho};">Como aluna ({len(pub_aluna)})</div>', unsafe_allow_html=True)
                    renderizar_publicacoes(pub_aluna)
                    st.markdown("---")
                    st.markdown(f'<div class="det-label">Como professora ({len(pub_docente)})</div>', unsafe_allow_html=True)
                    renderizar_publicacoes(pub_docente)
                else:
                    st.markdown(f'<div class="det-label">Publicações ({len(pub_docente)})</div>', unsafe_allow_html=True)
                    renderizar_publicacoes(pub_docente)