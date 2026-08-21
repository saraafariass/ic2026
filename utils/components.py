import streamlit as st
import pandas as pd
from assets.styles import vermelho, vermelho_claro, cor_texto, cor_texto_terciario, cores_projetos

def secao(titulo):
    st.markdown(f'<p class="secao">{titulo}</p>', unsafe_allow_html=True)

def card_publicacao(publicacao, alcance_cor, botao=""):
    referencia = str(publicacao.get("referencia", ""))
    alcance = str(publicacao.get("alcance", ""))
    ano = str(publicacao.get("ano", ""))
    cabecalho = (
        f'<span style="font-size:0.68rem;background:{alcance_cor};color:#fff;'
        f'padding:1px 7px;border-radius:10px;font-weight:600;">{alcance}</span>'
        f'<span style="font-size:0.68rem;color:{cor_texto_terciario};"> {ano}</span><br>'
    )
    corpo = (
        f'<span style="font-size:0.78rem;color:{cor_texto};display:block;margin-top:3px;">{referencia}</span>{botao}'
    )
    html = (
        f'<div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;'
        f'margin-bottom:0.35rem;border-left:3px solid {alcance_cor};">{cabecalho}{corpo}</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def card_publicacao_lista(publicacao, cor_vermelho, cor_texto_val, cor_texto_sec):
    referencia = str(publicacao.get("referencia", ""))
    autoria = str(publicacao.get("autoria", "Não informado"))
    alcance = str(publicacao.get("alcance", ""))
    link = str(publicacao.get("link", "")).strip()
    tem_link = pd.notna(publicacao.get("link")) and link and link.lower() not in ["nan", "none"]

    botao_html = (
        f'<a href="{link}" target="_blank" style="'
        f'display:inline-block;padding:5px 14px;background:{cor_vermelho};'
        f'color:#fff;border-radius:5px;font-size:0.75rem;font-weight:600;'
        f'text-decoration:none;letter-spacing:0.02em;">Acessar trabalho</a>'
    ) if tem_link else ""

    card_html = (
        f'<div class="card-publicacao">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
        f'<span class="alcance-badge">{alcance}</span>{botao_html}</div>'
        f'<p style="margin:0.4rem 0 0.3rem;font-weight:500;color:{cor_texto_val};">{referencia}</p>'
        f'<small style="color:{cor_texto_sec};">Autoria: {autoria}</small>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

def renderizar_projetos(lista_projetos):
    if not lista_projetos:
        st.caption("Nenhum projeto no período")
        return
    for p in lista_projetos:
        cor_tipo = cores_projetos.get(p.get("tipo"), vermelho)
        st.markdown(f"""
        <div style="background:#f9f9f9;border-radius:6px;padding:0.45rem 0.7rem;
            margin-bottom:0.35rem;border-left:3px solid {cor_tipo};">
            <span style="font-size:0.8rem;font-weight:600;color:{cor_texto};">{p.get('nome', '')}</span><br>
            <span style="font-size:0.7rem;color:{cor_tipo};font-weight:600;">{p.get('tipo', '')}</span>
            <span style="font-size:0.7rem;color:{cor_texto_terciario};"> {p.get('periodo', '')}</span>
        </div>
        """, unsafe_allow_html=True)

def renderizar_publicacoes(lista_publicacoes):
    if not lista_publicacoes:
        st.caption("Nenhuma publicação no período")
        return
    for p in lista_publicacoes:
        link = str(p.get("link", "")).strip()
        tem_link = pd.notna(p.get("link")) and link and link.lower() not in ["nan", "none"]
        alcance_cor = vermelho if p.get("alcance") == "Internacional" else vermelho_claro
        botao = (
            f'<a href="{link}" target="_blank" style="display:inline-block;margin-top:0.3rem;'
            f'padding:3px 10px;background:{vermelho};color:#fff;border-radius:4px;'
            f'font-size:0.68rem;font-weight:600;text-decoration:none;">Acessar trabalho</a>'
        ) if tem_link else ""
        card_publicacao(p, alcance_cor, botao)