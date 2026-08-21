import streamlit as st
import html
import pandas as pd
from assets.styles import vermelho, cor_texto, cor_texto_secundario
from utils.components import secao

def render(parcerias):
    secao("Parcerias")

    if not parcerias.empty:
        for _, parceria in parcerias.iterrows():
            nome = str(parceria.get("nome", ""))
            descricao = str(parceria.get("descricao", "")).replace("\n", " ").strip()
            ano_ini = str(parceria.get("ano_ini", "")).strip()
            ano_fim = str(parceria.get("ano_fim", "")).strip()
            link = str(parceria.get("link", "")).strip()

            periodo = f"{ano_ini} - {ano_fim}" if ano_fim and ano_fim != "nan" else ano_ini
            
            tem_link = pd.notna(parceria.get("link")) and link and link.lower() not in ["nan", "none", ""]
            botao_link = (
                f'<a href="{link}" target="_blank" style="display:inline-block;padding:4px 12px;'
                f'background:{vermelho};color:#fff;border-radius:6px;font-size:0.7rem;'
                f'font-weight:600;text-decoration:none;">Acessar site</a>'
            ) if tem_link else ""

            nome_escapado = html.escape(nome)
            descricao_formatada = html.escape(descricao)

            card_html = (
                f'<div class="card-publicacao" style="margin-bottom:1rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
                f'<span class="alcance-badge" style="background:{vermelho};">{periodo}</span>'
                f'{botao_link}</div>'
                f'<p style="margin:0.4rem 0 0.2rem;font-weight:600;color:{cor_texto};font-size:0.95rem;">{nome_escapado}</p>'
                f'<p style="margin:0;color:{cor_texto_secundario};line-height:1.6;font-size:0.85rem;">{descricao_formatada}</p>'
                f'</div>'
            )

            st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("Nenhuma parceria cadastrada.")