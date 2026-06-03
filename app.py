import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

from assets.styles import (
    get_css, COR_VERMELHO, COR_VERMELHO_GRAFICO,
    TEXTO, TEXTO_SECUNDARIO, TEXTO_TERCIARIO, FUNDO, CARD, TIPO_COR
)

st.set_page_config(layout="wide", page_title="  Dashboard MDC")
st.markdown(get_css(), unsafe_allow_html=True)


def secao(titulo):
    st.markdown(f'<p class="secao">{titulo}</p>', unsafe_allow_html=True)


def _pub_card_inner(alcance, ano, alcance_cor, ref, aut, btn):
    """Monta HTML do card de publicação sem interpolar dados do usuário na f-string."""
    header = (
        f'<span style="font-size:0.68rem;background:{alcance_cor};color:#fff;'
        f'padding:1px 7px;border-radius:10px;font-weight:600;">' + alcance + '</span>'
        f'<span style="font-size:0.68rem;color:{TEXTO_TERCIARIO};"> ' + ano + '</span><br>'
    )
    body = (
        '<span style="font-size:0.78rem;color:' + TEXTO + ';display:block;margin-top:3px;">' +
        ref + '</span>' + btn
    )
    return (
        f'<div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;'
        f'margin-bottom:0.35rem;border-left:3px solid {alcance_cor};">'
        + header + body + '</div>'
    )


def card_publicacao(p, alcance_cor, btn=''):
    ref = str(p.get('referencia', ''))
    alcance = str(p.get('alcance', ''))
    ano = str(p.get('ano', ''))
    st.markdown(_pub_card_inner(alcance, ano, alcance_cor, ref, '', btn), unsafe_allow_html=True)


def card_publicacao_lista(pub, cor_vermelho, texto, texto_secundario):
    ref = str(pub.get('referencia', ''))
    aut = str(pub.get('autores', 'Não informado'))
    alcance = str(pub.get('alcance', ''))
    link_pub = str(pub.get('link', '')).strip()
    tem_link = pd.notna(pub.get('link')) and link_pub
    btn_html = (
        f'<a href="{link_pub}" target="_blank" style="'
        f'display:inline-block;padding:5px 14px;background:{cor_vermelho};'
        f'color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;'
        f'text-decoration:none;letter-spacing:0.02em;">Acessar trabalho</a>'
    ) if tem_link else ''
    card_html = (
        f'<div class="card-publicacao">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
        f'<span class="alcance-badge">' + alcance + '</span>' + btn_html + '</div>'
        f'<p style="margin:0.4rem 0 0.3rem;font-weight:500;color:{texto};">' + ref + '</p>'
        f'<small style="color:{texto_secundario};">Autores: ' + aut + '</small>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)


def filtrar_periodo(df, ano_ini, ano_fim):
    return df[(df["ano_ini"] <= ano_fim) & (df["ano_fim"] >= ano_ini)]


def _parse_ano(texto):
    """Extrai ano inicial e final de strings como '2020 - atual' ou '2022'."""
    import re
    texto = str(texto).strip()
    anos = re.findall(r'\d{4}', texto)
    if not anos:
        return None, None
    ano_i = int(anos[0])
    ano_f = 2026 if 'atual' in texto.lower() else int(anos[-1])
    return ano_i, ano_f


def filtrar_alunas_periodo(df, ano_ini, ano_fim):
    def no_periodo(row):
        a_i, a_f = _parse_ano(row['periodo'])
        if a_i is None:
            return True
        return a_i <= ano_fim and a_f >= ano_ini
    return df[df.apply(no_periodo, axis=1)]


def _nome_base(nome):
    """Remove prefixos (Profa./Prof.) e sufixos como (2016 - 2022) do nome."""
    import re
    nome = re.sub(r'^Prof[ao]?\.\s*', '', nome.strip())
    nome = re.sub(r'\s*\(.*?\)', '', nome).strip()
    return nome.lower()


def encontrar_projetos_por_pessoa(nome, projetos_df):
    busca = _nome_base(nome)
    return [
        p for _, p in projetos_df.iterrows()
        if busca in str(p.get('equipe', p.get('autores', ''))).lower()
    ]


def encontrar_publicacoes_por_pessoa(nome, publicacoes_df):
    busca = _nome_base(nome)
    return [
        p for _, p in publicacoes_df.iterrows()
        if busca in str(p.get('autores', '')).lower()
    ]


@st.cache_data
def carregar_dados():
    alunas = pd.read_csv("alunas.csv")
    docentes = pd.read_csv("docentes.csv")
    projetos = pd.read_csv("projetos.csv")
    publicacoes = pd.read_csv("publicacoes.csv")
    premiacoes = pd.read_csv("premiacoes.csv")
    eventos = pd.read_csv("eventos.csv")
    return alunas, docentes, projetos, publicacoes, premiacoes, eventos


def criar_nuvem_palavras(projetos_df):
    textos = []
    for _, projeto in projetos_df.iterrows():
        texto = f"{projeto['nome']} {projeto.get('detalhes', '')}"
        textos.append(texto)
    if not textos:
        return None
    texto_completo = " ".join(textos)
    nuvem = WordCloud(
        width=800, height=400, background_color='white',
        colormap='Reds', max_words=50, collocations=False
    ).generate(texto_completo)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(nuvem, interpolation='bilinear')
    ax.axis('off')
    return fig


def iniciais(nome):
    partes = nome.strip().split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[-1][0]).upper()
    return partes[0][:2].upper()


def badge_curso(curso):
    if curso == "Técnico":
        return '<span class="badge badge-tec">Técnico</span>'
    elif curso == "Graduação":
        return '<span class="badge badge-grad">Graduação</span>'
    else:
        return '<span class="badge badge-amb">Técnico + Graduação</span>'


alunas, docentes, projetos, publicacoes, premiacoes, eventos = carregar_dados()

ano_min, ano_max = 2016, 2026

st.sidebar.markdown(
    '<p class="sidebar-titulo">Meninas Digitais no Cerrado</p>'
    '<p class="sidebar-marca">MDC - 10 anos</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="filtro-titulo">Filtrar por ano</p>', unsafe_allow_html=True)
ano_ini, ano_fim = st.sidebar.slider(
    "Período", 2016, 2026, (2016, 2026), label_visibility="collapsed",
)

st.sidebar.markdown('<p class="filtro-titulo">Filtrar estudantes</p>', unsafe_allow_html=True)

cursos_options = ["Todas", "Técnico", "Graduação", "Técnico e Graduação"]
filtro_curso = st.sidebar.selectbox("Curso:", cursos_options)

filtro_verticalizou = st.sidebar.selectbox("Verticalizou:", ["Todas", "Sim", "Não"])
filtro_bolsista = st.sidebar.selectbox("Bolsista:", ["Todas", "Sim", "Não"])

if st.sidebar.button("Atualizar dados do site"):
    st.cache_data.clear()
    st.rerun()

projetos_periodo = filtrar_periodo(projetos, ano_ini, ano_fim)
publicacoes_periodo = publicacoes[publicacoes["ano"].between(ano_ini, ano_fim)]
premiacoes_periodo = premiacoes[premiacoes["ano"].between(ano_ini, ano_fim)]
eventos_periodo = eventos[eventos["ano"].between(ano_ini, ano_fim)]

st.title("    Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado")
st.caption(f"Período {ano_ini} a {ano_fim}")

tab_est, tab_doc, tab_projetos, tab_pub, tab_eventos, tab_parcerias, tab_sobre = st.tabs([
    "Estudantes", "Docentes", "Projetos", "Publicações", "Eventos e Premiações", "Parcerias", "Sobre"
])

#aba estudantes 
with tab_est:
    secao("Participação no Projeto Meninas Digitais no Cerrado")

    alunas_periodo = filtrar_alunas_periodo(alunas, ano_ini, ano_fim)
    alunas_filtradas = alunas_periodo.copy()

    if filtro_curso == "Técnico":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].isin(["Técnico", "Técnico e Graduação"])]
    elif filtro_curso == "Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"].isin(["Graduação", "Técnico e Graduação"])]
    elif filtro_curso == "Técnico e Graduação":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["curso"] == "Técnico e Graduação"]

    if filtro_verticalizou != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["verticalizou"] == filtro_verticalizou]

    if filtro_bolsista != "Todas":
        alunas_filtradas = alunas_filtradas[alunas_filtradas["bolsista"] == filtro_bolsista]

    alunas_tecnico = alunas_filtradas[alunas_filtradas["curso"].isin(["Técnico", "Técnico e Graduação"])]
    alunas_graduacao = alunas_filtradas[alunas_filtradas["curso"].isin(["Graduação", "Técnico e Graduação"])]

    st.markdown("### Ensino Médio Técnico")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de alunas", len(alunas_tecnico))
    with col2:
        st.metric(
            "Verticalizaram",
            len(alunas_tecnico[alunas_tecnico["verticalizou"] == "Sim"]),
        )
    with col3:
        st.metric(
            "Bolsistas",
            len(alunas_tecnico[alunas_tecnico["bolsista"] == "Sim"]),
        )

    st.markdown("---")

    st.markdown("### Bacharelado em Sistemas de Informação")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de alunas", len(alunas_graduacao))
    with col2:
        st.metric(
            "Bolsistas",
            len(alunas_graduacao[alunas_graduacao["bolsista"] == "Sim"]),
        )

    st.markdown("---")

    # Info de resultados 
    total_filtradas = len(alunas_filtradas)
    total_geral = len(alunas_periodo)
    if total_filtradas == total_geral:
        st.markdown(
            f'<p class="resultados-info">{total_geral} estudantes no período</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<p class="resultados-info">Exibindo {total_filtradas} de {total_geral} estudantes no período</p>',
            unsafe_allow_html=True,
        )

    #  Cards individuais 
    if alunas_filtradas.empty:
        st.markdown(
            '<div class="sem-resultado">Nenhuma estudante encontrada com os filtros selecionados.</div>',
            unsafe_allow_html=True,
        )
    else:
        for _, aluna in alunas_filtradas.iterrows():
            projetos_aluna = encontrar_projetos_por_pessoa(aluna["nome"], projetos_periodo)
            publicacoes_aluna = encontrar_publicacoes_por_pessoa(aluna["nome"], publicacoes_periodo)

            vert_val = aluna["verticalizou"]
            vert_display = "Não se aplica" if pd.isna(vert_val) or str(vert_val).strip() == "" else vert_val

            badges_html = badge_curso(aluna["curso"])
            if aluna["bolsista"] == "Sim":
                badges_html += ' <span class="badge badge-bols">Bolsista</span>'
            if vert_val == "Sim":
                badges_html += ' <span class="badge badge-vert">Verticalizou</span>'

            label = f"{aluna['nome']} - {aluna['curso']}: {aluna['periodo']}"
            with st.expander(label):
                st.markdown(f'<div style="margin-bottom:0.5rem;">{badges_html}</div>', unsafe_allow_html=True)

                info_col, proj_col, pub_col = st.columns([1, 1.5, 2])

                with info_col:
                    st.markdown(f"""
                    <div class="det-label">Bolsista</div>
                    <div class="det-valor">{aluna['bolsista']}</div>
                    <div class="det-label">Verticalizou</div>
                    <div class="det-valor">{vert_display}</div>
                    """, unsafe_allow_html=True)

                with proj_col:
                    st.markdown(f'<div class="det-label">Projetos ({len(projetos_aluna)})</div>', unsafe_allow_html=True)
                    if projetos_aluna:
                        for p in projetos_aluna:
                            tipo_cor = {"Ensino": "#1565c0", "Pesquisa": "#4527a0", "Extensao": "#2e7d32"}.get(p["tipo"], COR_VERMELHO)
                            st.markdown(f"""
                            <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                                margin-bottom:0.35rem;border-left:3px solid {tipo_cor};">
                                <span style="font-size:0.8rem;font-weight:600;color:{TEXTO};">{p['nome']}</span><br>
                                <span style="font-size:0.7rem;color:{tipo_cor};font-weight:600;">{p['tipo']}</span>
                                <span style="font-size:0.7rem;color:{TEXTO_TERCIARIO};"> {p['periodo']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("Nenhum projeto no período")

                with pub_col:
                    st.markdown(f'<div class="det-label">Publicações ({len(publicacoes_aluna)})</div>', unsafe_allow_html=True)
                    if publicacoes_aluna:
                        for p in publicacoes_aluna:
                            link = str(p.get('link', '')).strip()
                            tem_link = pd.notna(p.get('link')) and link
                            alcance_cor = COR_VERMELHO if p['alcance'] == "Internacional" else COR_VERMELHO_GRAFICO
                            btn = (
                                f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                                f'padding:3px 10px;background:{COR_VERMELHO};color:#fff;border-radius:4px;'
                                f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                            ) if tem_link else ''
                            card_publicacao(p, alcance_cor, btn)
                    else:
                        st.caption("Nenhuma publicação no período")

# aba docentes
with tab_doc:
    secao("Corpo docente")
    st.metric("Total de docentes", len(docentes))
    st.markdown("---")

    for _, docente in docentes.iterrows():
        proj_doc = encontrar_projetos_por_pessoa(docente["nome"], projetos_periodo)
        pub_doc = encontrar_publicacoes_por_pessoa(docente["nome"], publicacoes_periodo)

        lattes_url = str(docente.get('lattes', '')).strip()
        email = docente.get('email', '')

        nome_exibido = _nome_base(docente["nome"]).title()
        label = f"{docente['nome']}"

        with st.expander(label):
            info_col, proj_col, pub_col = st.columns([1, 1.5, 2])

            with info_col:
                st.markdown(f"""
                <div class="det-label">Email</div>
                <div class="det-valor">{email or 'Não informado'}</div>
                <div class="det-label" style="margin-top:0.65rem;">Lattes</div>
                <div style="margin-top:0.3rem;">
                    {'<a href="' + lattes_url + '" target="_blank" style="display:inline-block;padding:4px 12px;background:' + COR_VERMELHO + ';color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>' if lattes_url else '<span style="font-size:0.82rem;color:' + TEXTO_TERCIARIO + ';">Não informado</span>'}
                </div>
                """, unsafe_allow_html=True)

            with proj_col:
                st.markdown(f'<div class="det-label">Projetos ({len(proj_doc)})</div>', unsafe_allow_html=True)
                if proj_doc:
                    for p in proj_doc:
                        tipo_cor = {"Ensino": "#1565c0", "Pesquisa": "#4527a0", "Extensao": "#2e7d32"}.get(p["tipo"], COR_VERMELHO)
                        st.markdown(f"""
                        <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
                            margin-bottom:0.35rem;border-left:3px solid {tipo_cor};">
                            <span style="font-size:0.8rem;font-weight:600;color:{TEXTO};">{p['nome']}</span><br>
                            <span style="font-size:0.7rem;color:{tipo_cor};font-weight:600;">{p['tipo']}</span>
                            <span style="font-size:0.7rem;color:{TEXTO_TERCIARIO};"> {p['periodo']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("Nenhum projeto no período")

            with pub_col:
                st.markdown(f'<div class="det-label">Publicações ({len(pub_doc)})</div>', unsafe_allow_html=True)
                if pub_doc:
                    for p in pub_doc:
                        link = str(p.get('link', '')).strip()
                        tem_link = pd.notna(p.get('link')) and link
                        alcance_cor = COR_VERMELHO if p['alcance'] == "Internacional" else COR_VERMELHO_GRAFICO
                        btn = (
                            f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
                            f'padding:3px 10px;background:{COR_VERMELHO};color:#fff;border-radius:4px;'
                            f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
                        ) if tem_link else ''
                        card_publicacao(p, alcance_cor, btn)
                else:
                    st.caption("Nenhuma publicação no período")

# aba projetos
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
        tipos_count = projetos_periodo.groupby("tipo").size().reset_index(name="quantidade")
        fig = px.bar(
            tipos_count, x="tipo", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=FUNDO, plot_bgcolor=FUNDO,
            xaxis_title="Tipo de projeto", yaxis_title="Quantidade", showlegend=False
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
                    <small>Integrantes: {projeto.get('equipe', projeto.get('autores', 'Não informado'))}</small>
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

# aba publicações
with tab_pub:
    secao("Publicações por ano")

    if not publicacoes_periodo.empty:
        pubs_por_ano = publicacoes_periodo.groupby("ano").size().reset_index(name="quantidade")

        fig = px.bar(
            pubs_por_ano, x="ano", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade"
        )
        fig.update_layout(
            height=400, paper_bgcolor=FUNDO, plot_bgcolor=FUNDO,
            xaxis_title="Ano", yaxis_title="Número de publicações", showlegend=False,
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        secao("Publicações")

        pubs_por_alcance = publicacoes_periodo.groupby(["ano", "alcance"]).size().reset_index(name="quantidade")

        fig2 = px.bar(
            pubs_por_alcance, x="ano", y="quantidade", color="alcance",
            color_discrete_map={"Nacional": COR_VERMELHO_GRAFICO, "Internacional": COR_VERMELHO},
            text="quantidade", barmode="group"
        )
        fig2.update_layout(
            height=400, paper_bgcolor=FUNDO, plot_bgcolor=FUNDO,
            xaxis_title="Ano", yaxis_title="Número de publicações",
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        secao("Lista de publicações")

        for ano in sorted(publicacoes_periodo["ano"].unique(), reverse=True):
            pubs_ano = publicacoes_periodo[publicacoes_periodo["ano"] == ano]
            st.markdown(f"### {ano}")
            for _, pub in pubs_ano.iterrows():
                link_pub = str(pub.get('link', '')).strip()
                tem_link = pd.notna(pub.get('link')) and link_pub
                card_publicacao_lista(pub, COR_VERMELHO, TEXTO, TEXTO_SECUNDARIO)
    else:
        st.info("Nenhuma publicação no período selecionado.")

    st.markdown(
        f'<p class="fonte-site">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/publicacoes" target="_blank">meninasdigitaisnocerrado.com.br/publicacoes</a></p>',
        unsafe_allow_html=True,
    )

# aba eventos e publicações
with tab_eventos:
    secao("Eventos participados")

    if not eventos_periodo.empty:
        eventos_por_ano = eventos_periodo.groupby("ano")["quantidade"].sum().reset_index()

        fig_eventos = px.bar(
            eventos_por_ano, x="ano", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade", title="Participações em eventos por ano"
        )
        fig_eventos.update_layout(
            height=450, paper_bgcolor=FUNDO, plot_bgcolor=FUNDO,
            xaxis_title="Ano", yaxis_title="Número de participações", showlegend=False,
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig_eventos.update_traces(textposition='outside')
        st.plotly_chart(fig_eventos, use_container_width=True)

        st.markdown("---")
        secao("Eventos mais participados")

        textos_eventos = []
        for _, evento in eventos_periodo.iterrows():
            nome_evento = evento['nome']
            quantidade = int(evento['quantidade'])
            textos_eventos.extend([nome_evento] * (quantidade // 5 + 1))

        if textos_eventos:
            texto_completo = " ".join(textos_eventos)
            nuvem_eventos = WordCloud(
                width=800, height=400, background_color='white',
                colormap='Reds', max_words=30, collocations=False
            ).generate(texto_completo)
            fig_nuvem_eventos, ax_nuvem = plt.subplots(figsize=(10, 5))
            ax_nuvem.imshow(nuvem_eventos, interpolation='bilinear')
            ax_nuvem.axis('off')
            st.pyplot(fig_nuvem_eventos)

        st.markdown("---")
        st.markdown("**Lista de eventos**")
        eventos_lista = eventos_periodo.sort_values("ano", ascending=False)
        for _, evento in eventos_lista.iterrows():
            st.markdown(f"""
            <div class="card-publicacao">
                <strong>{evento['nome']}</strong><br>
                <small>Ano: {int(evento['ano'])} | Participações: {int(evento['quantidade'])}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum evento registrado no período.")

    st.markdown("---")
    secao("Premiações")

    if not premiacoes_periodo.empty:
        premiacoes_por_ano = premiacoes_periodo.groupby("ano").size().reset_index(name="quantidade")

        fig_premiacoes = px.bar(
            premiacoes_por_ano, x="ano", y="quantidade",
            color="quantidade",
            color_continuous_scale=["#e57373", "#c62828"],
            text="quantidade", title="Premiações conquistadas por ano"
        )
        fig_premiacoes.update_layout(
            height=450, paper_bgcolor=FUNDO, plot_bgcolor=FUNDO,
            xaxis_title="Ano", yaxis_title="Número de premiações", showlegend=False,
            xaxis=dict(tickmode='linear', dtick=1)
        )
        fig_premiacoes.update_traces(textposition='outside')
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
    else:
        st.info("Nenhuma premiação no período.")

    st.markdown(
        f'<p class="fonte-site" style="margin-top: 2rem;">Fonte: <a href="https://meninasdigitaisnocerrado.com.br/premiacoes" target="_blank">meninasdigitaisnocerrado.com.br</a></p>',
        unsafe_allow_html=True,
    )

# aba parcerias
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
    except Exception:
        st.info("Nenhuma parceria cadastrada no momento.")

    st.markdown(
        f'<p class="fonte-site">Para mais informações sobre parcerias, acesse o site oficial do projeto.</p>',
        unsafe_allow_html=True,
    )

# aba sobre
with tab_sobre:

 
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{COR_VERMELHO} 0%,#8b0000 100%);
        border-radius:12px;padding:2rem 2.5rem;margin-bottom:1.5rem;color:#fff;">
        <div style="font-size:0.75rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
            opacity:0.8;margin-bottom:0.4rem;">EDITAL Nº 11 de 03 de abril de 2025 - PIBIC</div>
        <div style="font-size:1.6rem;font-weight:700;line-height:1.2;margin-bottom:0.5rem;">
            Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado
    """, unsafe_allow_html=True)

    # Sobre o projeto
    secao("Sobre o projeto")
    st.markdown(f"""
    <div style="background:{CARD};border-radius:10px;padding:1.5rem 2rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);line-height:1.8;color:{TEXTO};font-size:0.95rem;">
        O presente projeto de pesquisa celebra os <strong>10 anos do Meninas Digitais no Cerrado</strong>,
        iniciativa do IF Goiano - Campus Ceres e projeto parceiro do
        <strong>Programa Meninas Digitais (PMD)</strong> que busca incentivar a participação de
        meninas e mulheres nos cursos de Computação.
        <br><br>
        A proposta consiste na construção de uma <strong>base de dados aberta sobre gênero e
        Computação</strong> no âmbito do Campus Ceres. Espera-se sistematizar e visualizar a
        evolução da participação das mulheres na área de tecnologia, promovendo
        <strong>transparência e visibilidade</strong> do projeto e do campus, permitindo integrar
        e sistematizar informações dispersas inerentes ao recorte de gênero.
        <br><br>
        O projeto encontra-se em consonância com outro projeto maior, aprovado via
        <strong>Chamada Pública CNPq/MCTI/Mulheres nº 31/2023</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Equipe
    secao("Equipe")
    col_bol, col_coord = st.columns(2)

    with col_bol:
        st.markdown(f"""
        <div style="background:{CARD};border-radius:10px;padding:1.25rem 1.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:4px solid {COR_VERMELHO_GRAFICO};">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;color:{COR_VERMELHO_GRAFICO};margin-bottom:0.5rem;">Bolsista PIBIC</div>
            <div style="font-size:1.05rem;font-weight:700;color:{TEXTO};">Sara Luiz de Farias</div>
            <div style="font-size:0.82rem;color:{TEXTO_SECUNDARIO};margin-top:0.25rem;">
                Bacharelanda em Sistemas de Informação<br>
                IF Goiano - Campus Ceres<br>
                <a href="http://lattes.cnpq.br/2013698994793152" target="_blank"
                    style="display:inline-block;margin-top:0.4rem;padding:4px 12px;background:{COR_VERMELHO_GRAFICO};color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_coord:
        st.markdown(f"""
        <div style="background:{CARD};border-radius:10px;padding:1.25rem 1.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:4px solid {COR_VERMELHO};">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;color:{COR_VERMELHO};margin-bottom:0.5rem;">Coordenadora</div>
            <div style="font-size:1.05rem;font-weight:700;color:{TEXTO};">Profa. Thalia Santos de Santana</div>
            <div style="font-size:0.82rem;color:{TEXTO_SECUNDARIO};margin-top:0.25rem;">
                Docente em Computação<br>
                IF Goiano - Campus Ceres<br>
                <a href="http://lattes.cnpq.br/8063677996827079" target="_blank"
                    style="display:inline-block;margin-top:0.4rem;padding:4px 12px;background:{COR_VERMELHO};color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Como citar
    secao("Como citar a plataforma")
    st.markdown(f"""
    <div style="background:{CARD};border-radius:10px;padding:1.25rem 1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);border-left:4px solid {COR_VERMELHO};">
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
            color:{TEXTO_SECUNDARIO};margin-bottom:0.75rem;">Citação no texto</div>
        <div style="font-size:0.88rem;color:{TEXTO};background:#f9f9f9;border-radius:6px;
            padding:0.5rem 0.8rem;margin-bottom:1rem;">
            (Meninas Digitais no Cerrado, 2026)
        </div>
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
            color:{TEXTO_SECUNDARIO};margin-bottom:0.5rem;">Referência bibliográfica completa</div>
        <div style="font-size:0.88rem;color:{TEXTO};line-height:1.8;">
            MENINAS DIGITAIS NO CERRADO.
            <em>Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado.</em>
            Ceres: IF Goiano - Campus Ceres, 2026.
            Disponível em:
            <a href="https://meninasdigitaisnocerrado.com.br" target="_blank"
                style="color:{COR_VERMELHO};">meninasdigitaisnocerrado.com.br</a>.
            Acesso em: dia mes e ano.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Como usar
    secao("Como usar")
    st.markdown(f"""
    <div style="background:{CARD};border-radius:10px;padding:1.25rem 1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);border-left:4px solid {COR_VERMELHO};">
        Acesse o repositório no GitHub para instruções de instalação e execução do projeto.<br><br>
        <a href="https://github.com/saraafariass/ic2026" target="_blank"
            style="display:inline-block;padding:6px 16px;background:{COR_VERMELHO};color:#fff;
            border-radius:5px;font-size:0.82rem;font-weight:600;text-decoration:none;">
            Ver no GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tecnologias
    secao("Tecnologias utilizadas")
    techs = [
        ("Python", "Linguagem principal"),
        ("Streamlit", "Interface web interativa"),
        ("Pandas", "Manipulação de dados"),
        ("Plotly", "Gráficos interativos"),
        ("WordCloud", "Visualização de palavras"),
    ]
    cols = st.columns(len(techs))
    for col, (nome, desc) in zip(cols, techs):
        col.markdown(f"""
        <div style="background:{CARD};border-radius:8px;padding:0.75rem 1rem;
            box-shadow:0 1px 2px rgba(0,0,0,0.06);text-align:center;">
            <div style="font-weight:700;font-size:0.88rem;color:{TEXTO};">{nome}</div>
            <div style="font-size:0.72rem;color:{TEXTO_SECUNDARIO};margin-top:3px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    '<p class="fonte-site" style="text-align: center;">Última atualização: 10/02/2026 13:25</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="fonte-site" style="text-align: center;">Feito com <3 por Sara Farias (Meninas Digitais no Cerrado)</p>',
    unsafe_allow_html=True,
)