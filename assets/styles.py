COR_VERMELHO = "#c62828"
COR_VERMELHO_GRAFICO = "#e57373"
TEXTO = "#212121"
TEXTO_SECUNDARIO = "#616161"
TEXTO_TERCIARIO = "#9e9e9e"
FUNDO = "#f5f5f5"
CARD = "#ffffff"

TIPO_COR = {
    "Ensino": "#1565c0",
    "Pesquisa": "#4527a0",
    "Extensão": "#2e7d32",
}

EVENTO_TIPO_COR = {
    "Palestra": "#d32f2f",
    "Publicação": "#7b1fa2",
    "Oficina": "#388e3c",
    "Evento": "#1976d2",
    "Viagem técnica": "#f57c00",
}


def get_css():
    return f"""
<style>
    .main {{ background: {FUNDO}; }}

    h1 {{
        color: {TEXTO}; font-weight: 700; font-size: 1.85rem;
        letter-spacing: -0.02em; margin-bottom: 0.25rem;
    }}

    [data-testid="stCaption"] {{ color: {TEXTO_SECUNDARIO} !important; }}
    [data-testid="stSidebar"] {{ background: {CARD}; border-right: 1px solid #e0e0e0; }}
    [data-testid="stMarkdown"] strong {{ color: {TEXTO}; }}

    hr {{ border-color: #e0e0e0; margin: 1.5rem 0; }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 1px solid #e0e0e0; }}
    .stTabs [data-baseweb="tab"] {{
        height: 44px; padding: 0 1.1rem; background: {CARD};
        border-radius: 8px 8px 0 0; font-weight: 600;
        color: {TEXTO_SECUNDARIO}; border: 1px solid #e0e0e0; border-bottom: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: {COR_VERMELHO}; color: #fff; border-color: {COR_VERMELHO};
    }}

    /* Sidebar */
    .sidebar-titulo {{ font-size: 1.05rem; font-weight: 700; color: {TEXTO}; margin: 0; }}
    .sidebar-marca {{ font-size: 0.8rem; color: {COR_VERMELHO}; font-weight: 600; margin-top: 0.15rem; }}
    .filtro-titulo {{
        font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.06em; color: {TEXTO_SECUNDARIO}; margin: 1rem 0 0.25rem 0;
    }}

    /* Seção */
    .secao {{
        color: {TEXTO}; font-size: 1.1rem; font-weight: 600;
        padding-bottom: 0.4rem; margin: 1.5rem 0 0.85rem 0;
        border-bottom: 2px solid {COR_VERMELHO};
    }}

    /* Cards */
    .card-projeto {{
        background: {CARD}; border-radius: 8px; padding: 1rem;
        margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid {COR_VERMELHO};
        word-wrap: break-word;
        overflow-wrap: break-word;
    }}
    .card-publicacao {{
        background: {CARD}; border-radius: 8px; padding: 0.8rem 1rem;
        margin-bottom: 0.8rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid {COR_VERMELHO_GRAFICO};
    }}
    /* Cards de eventos */
    .card-evento {{
        background: #fff;
        border-radius: 12px;
        padding: 1.2rem 3.5rem 1.2rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border-left: 4px solid {COR_VERMELHO};
        transition: all 0.3s ease;
        position: relative;
    }}
    .card-evento:hover {{
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }}
    .card-evento.destaque {{
        background: linear-gradient(135deg, #fff5f5 0%, #ffebee 100%);
        border-left-color: {COR_VERMELHO};
        box-shadow: 0 6px 10px rgba(198, 40, 40, 0.15);
        border: 1px solid #ffcdd2;
    }}
    .card-evento.destaque::before {{
        content: '';
        position: absolute;
        right: 1rem;
        top: 1rem;
    }}

    /* Badges */
    .alcance-badge {{
        background-color: {COR_VERMELHO_GRAFICO}; color: white;
        padding: 0.2rem 0.6rem; border-radius: 15px;
        font-size: 0.7rem; display: inline-block;
    }}
    .badge {{
        font-size: 0.65rem; font-weight: 600;
        padding: 2px 8px; border-radius: 20px; white-space: nowrap;
        margin-right: 5px; margin-bottom: 3px;
    }}
    .badge-tec  {{ background: #fce4e4; color: {COR_VERMELHO}; border: 1px solid #f7c1c1; }}
    .badge-grad {{ background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }}
    .badge-amb  {{ background: #ede7f6; color: #4527a0; border: 1px solid #ce93d8; }}
    .badge-bols {{ background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }}
    .badge-vert {{ background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }}
    .badge-local {{ background: #f0f4c3; color: #7cb342; border: 1px solid #aed581; }}
    .badge-palestra {{ background: #ffebee; color: #c62828; border: 1px solid #e57373; }}
    .badge-publicacao {{ background: #f3e5f5; color: #7b1fa2; border: 1px solid #ba68c8; }}
    .badge-oficina {{ background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }}
    .badge-evento {{ background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }}
    .badge-viagem {{ background: #fff3e0; color: #f57c00; border: 1px solid #ffcc80; }}
    .badge-organizacao {{ background: #673ab7; color: white; padding: 3px 10px; }}
    .badge-ouvinte {{ background: #4caf50; color: white; padding: 3px 10px; }}
    .badge-participante {{ background: #2196f3; color: white; padding: 3px 10px; }}

    /* Labels e valores internos */
    .det-label {{
        font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em;
        color: {TEXTO_TERCIARIO}; margin-top: 0.65rem; margin-bottom: 0.2rem;
    }}
    .det-valor {{ font-size: 0.82rem; color: {TEXTO}; }}

    /* Resultados e estados */
    .resultados-info {{ font-size: 0.75rem; color: {TEXTO_TERCIARIO}; margin-bottom: 0.75rem; }}
    .sem-resultado {{ text-align: center; padding: 2rem; color: {TEXTO_SECUNDARIO}; font-size: 0.9rem; }}

    /* Fonte/rodapé */
    .fonte-site {{ font-size: 0.78rem; color: {TEXTO_TERCIARIO}; margin-top: 0.75rem; }}
    .fonte-site a {{ color: {COR_VERMELHO}; font-weight: 500; text-decoration: none; }}
    .fonte-site a:hover {{ text-decoration: underline; }}
</style>
"""
