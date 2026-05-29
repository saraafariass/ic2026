"""Atualiza projetos.csv, publicacoes.csv e premiacoes.csv a partir do site MDC."""
import re
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup

URLS = {
    "projetos": "https://meninasdigitaisnocerrado.com.br/projetos",
    "publicacoes": "https://meninasdigitaisnocerrado.com.br/publicacoes",
    "premiacoes": "https://meninasdigitaisnocerrado.com.br/premiacoes",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_periodo(text: str) -> tuple[int, int]:
    m = re.match(r"(\d{4})(?:/(\d{4}))?", text.strip())
    if not m:
        raise ValueError(f"Período inválido: {text}")
    ini = int(m.group(1))
    fim = int(m.group(2) or ini)
    return ini, fim


def alcance_publicacao(texto: str) -> str:
    t = texto.lower()
    internacional = (
        "chile", "bolívia", "bolivia", "costa rica", "valparaíso", "valparaiso",
        "la paz", "san josé", "san jose", "lawcc",
        "latin american women", "congreso de la mujer latinoamericana",
        "proceedings xv congress", "proceedings xiii congress",
        "doi.org/10.3390/soc",
    )
    return "Internacional" if any(k in t for k in internacional) else "Nacional"


def scrape_projetos(html: str) -> pd.DataFrame:
    section = BeautifulSoup(html, "html.parser").find("section", id="three")
    rows, tipo_atual, periodo, ano_ini, ano_fim = [], None, None, None, None
    for el in section.find_all(["h3", "p", "dl"]):
        if el.name == "h3":
            tipo_atual = el.get_text(strip=True)
        elif el.name == "p":
            b = el.find("b")
            if b and re.match(r"\d{4}", b.get_text(strip=True)):
                periodo = b.get_text(strip=True)
                ano_ini, ano_fim = parse_periodo(periodo)
        elif el.name == "dl" and tipo_atual and periodo:
            dt, dd = el.find("dt"), el.find("dd")
            if dt:
                rows.append({
                    "periodo": periodo,
                    "ano_ini": ano_ini,
                    "ano_fim": ano_fim,
                    "tipo": tipo_atual,
                    "nome": dt.get_text(" ", strip=True),
                    "detalhes": dd.get_text(" ", strip=True) if dd else "",
                })
    return pd.DataFrame(rows)


def scrape_publicacoes(html: str) -> pd.DataFrame:
    section = BeautifulSoup(html, "html.parser").find("section", id="three")
    rows, ano_atual = [], None
    for el in section.find_all("p"):
        b = el.find("b")
        if b and re.fullmatch(r"\d{4}", b.get_text(strip=True)):
            ano_atual = int(b.get_text(strip=True))
            continue
        texto = el.get_text(" ", strip=True)
        if ano_atual and len(texto) > 40:
            rows.append({
                "ano": ano_atual,
                "referencia": texto,
                "alcance": alcance_publicacao(texto),
            })
    return pd.DataFrame(rows)


def scrape_premiacoes(html: str) -> pd.DataFrame:
    section = BeautifulSoup(html, "html.parser").find("section", id="three")
    rows, ano_atual = [], None
    for el in section.find_all("p"):
        b = el.find("b")
        if b and re.fullmatch(r"\d{4}", b.get_text(strip=True)):
            ano_atual = int(b.get_text(strip=True))
            continue
        texto = el.get_text(" ", strip=True)
        if ano_atual and len(texto) > 15:
            premio = el.find("b").get_text(strip=True) if el.find("b") else texto[:80]
            rows.append({"ano": ano_atual, "premio": premio, "descricao": texto})
    return pd.DataFrame(rows)


def main():
    df_proj = scrape_projetos(fetch(URLS["projetos"]))
    df_pub = scrape_publicacoes(fetch(URLS["publicacoes"]))
    df_prem = scrape_premiacoes(fetch(URLS["premiacoes"]))
    df_proj.to_csv("projetos.csv", index=False)
    df_pub.to_csv("publicacoes.csv", index=False)
    df_prem.to_csv("premiacoes.csv", index=False)
    print(f"projetos: {len(df_proj)} | publicacoes: {len(df_pub)} | premiacoes: {len(df_prem)}")


if __name__ == "__main__":
    main()
