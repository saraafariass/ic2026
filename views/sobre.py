import streamlit as st
from assets.styles import vermelho, fundo_card, cor_texto, cor_texto_secundario
from utils.components import secao

def render():
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{vermelho} 0%,#8b0000 100%);
        border-radius:12px;padding:2rem 2.5rem;margin-bottom:1.5rem;color:#fff;">
        <div style="font-size:0.75rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
            opacity:0.8;margin-bottom:0.4rem;">EDITAL Nº 11 de 03 de abril de 2025 - PIBIC</div>
        <div style="font-size:1.6rem;font-weight:700;line-height:1.2;margin-bottom:0.5rem;">
            Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado
        </div>
    </div>
    """, unsafe_allow_html=True)

    secao("Sobre o projeto")
    st.markdown(f"""
    <div style="background:{fundo_card};border-radius:10px;padding:1.5rem 2rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);line-height:1.8;color:{cor_texto};font-size:0.95rem;">
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
    secao("Equipe")
    col_bol, col_coord = st.columns(2)

    with col_bol:
        st.markdown(f"""
        <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:4px solid {vermelho};">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;color:{vermelho};margin-bottom:0.5rem;">Bolsista PIBIC</div>
            <div style="font-size:1.05rem;font-weight:700;color:{cor_texto};">Sara Luiz de Farias</div>
            <div style="font-size:0.82rem;color:{cor_texto_secundario};margin-top:0.25rem;">
                Bacharelanda em Sistemas de Informação<br>
                IF Goiano - Campus Ceres<br>
                <a href="http://lattes.cnpq.br/2013698994793152" target="_blank"
                    style="display:inline-block;margin-top:0.4rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_coord:
        st.markdown(f"""
        <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
            box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:4px solid {vermelho};">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;
                letter-spacing:0.08em;color:{vermelho};margin-bottom:0.5rem;">Coordenadora</div>
            <div style="font-size:1.05rem;font-weight:700;color:{cor_texto};">Profa. Thalia Santos de Santana</div>
            <div style="font-size:0.82rem;color:{cor_texto_secundario};margin-top:0.25rem;">
                Docente em Computação<br>
                IF Goiano - Campus Ceres<br>
                <a href="http://lattes.cnpq.br/8063677996827079" target="_blank"
                    style="display:inline-block;margin-top:0.4rem;padding:4px 12px;background:{vermelho};color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;text-decoration:none;">Acessar currículo Lattes</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    secao("Como citar o dashboard")
    st.markdown(f"""
    <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);border-left:4px solid {vermelho};">
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
            color:{cor_texto_secundario};margin-bottom:0.75rem;">Citação no texto</div>
        <div style="font-size:0.88rem;color:{cor_texto};background:#f9f9f9;border-radius:6px;
            padding:0.5rem 0.8rem;margin-bottom:1rem;">
            (Meninas Digitais no Cerrado, 2026)
        </div>
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
            color:{cor_texto_secundario};margin-bottom:0.5rem;">Referência bibliográfica completa</div>
        <div style="font-size:0.88rem;color:{cor_texto};line-height:1.8;">
            MENINAS DIGITAIS NO CERRADO.
            <em>Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado.</em>
            Ceres: IF Goiano - Campus Ceres, 2026.
            Disponível em:
            <a href="https://meninasdigitaisnocerrado.com.br/indicadores" target="_blank"
                style="color:{vermelho};">meninasdigitaisnocerrado.com.br</a>.
            Acesso em: dia mes e ano.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    secao("Como usar")
    st.markdown(f"""
    <div style="background:{fundo_card};border-radius:10px;padding:1.25rem 1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.07);border-left:4px solid {vermelho};">
        Acesse o repositório no GitHub para instruções de instalação e execução do projeto.<br><br>
        <a href="https://github.com/saraafariass/ic2026" target="_blank"
            style="display:inline-block;padding:6px 16px;background:{vermelho};color:#fff;
            border-radius:5px;font-size:0.82rem;font-weight:600;text-decoration:none;">
            Ver no GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    secao("Tecnologias utilizadas")
    tecnologias = [
        ("Python", "Linguagem principal"),
        ("Streamlit", "Interface web interativa"),
        ("Pandas", "Manipulação de dados"),
        ("Plotly", "Gráficos interativos"),
    ]
    cols = st.columns(len(tecnologias))
    for col, (nome, desc) in zip(cols, tecnologias):
        col.markdown(f"""
        <div style="background:{fundo_card};border-radius:8px;padding:0.75rem 1rem;
            box-shadow:0 1px 2px rgba(0,0,0,0.06);text-align:center;">
            <div style="font-weight:700;font-size:0.88rem;color:{cor_texto};">{nome}</div>
            <div style="font-size:0.72rem;color:{cor_texto_secundario};margin-top:3px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)