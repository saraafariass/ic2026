import re
from datetime import datetime
import pandas as pd

ANO_ATUAL = datetime.now().year

def carregar_css():
    with open("assets/style.css", "r", encoding="utf-8") as arquivo:
        return arquivo.read()

def extrair_anos(texto):
    texto = str(texto).strip()
    anos = re.findall(r"\d{4}", texto)
    if not anos:
        return None, None
    ano_inicio = int(anos[0])
    ano_fim = ANO_ATUAL if "atual" in texto.lower() else int(anos[-1])
    return ano_inicio, ano_fim

def filtrar_alunas_periodo(df, ano_inicio, ano_fim):
    def esta_no_periodo(linha):
        a_i, a_f = extrair_anos(linha["periodo"])
        if a_i is None:
            return True
        return a_i <= ano_fim and a_f >= ano_inicio
    return df[df.apply(esta_no_periodo, axis=1)]

def nome_sem_prefixos(nome):
    nome = re.sub(r"^Prof[ao]?\.\s*", "", str(nome).strip())
    nome = re.sub(r"\s*\(.*?\)", "", nome).strip()
    return nome.lower()

def nome_para_busca(nome):
    nome = re.sub(r"^Prof[ao]?\.\s*", "", str(nome).strip())
    nome = re.sub(r"\s*\(.*?\)", "", nome).strip()
    partes = nome.split()
    if len(partes) >= 3:
        return " ".join(partes[:3]).lower()
    elif len(partes) == 2:
        return " ".join(partes[:2]).lower()
    return nome.lower()

def buscar_projetos_por_nome(nome, projetos_df):
    busca = nome_para_busca(nome)
    return [
        p for _, p in projetos_df.iterrows()
        if busca in str(p.get("equipe", p.get("autoria", ""))).lower()
    ]

def buscar_publicacoes_por_nome(nome, publicacoes_df):
    busca = nome_para_busca(nome)
    return [
        p for _, p in publicacoes_df.iterrows()
        if busca in str(p.get("autoria", "")).lower()
    ]

def separar_por_papel(nome, projetos_df, publicacoes_df, alunas_df, docentes_df, ano_inicio, ano_fim):
    busca = nome_para_busca(nome)

    eh_aluna = False
    periodo_aluna_fim = 0
    for _, aluna in alunas_df.iterrows():
        if busca in str(aluna["nome"]).lower():
            periodo = str(aluna.get("periodo", ""))
            anos = re.findall(r"\d{4}", periodo)
            if anos:
                periodo_ini = int(anos[0])
                periodo_fim = ANO_ATUAL if "atual" in periodo.lower() else (int(anos[-1]) if len(anos) > 1 else periodo_ini)
                if periodo_fim >= ano_inicio and periodo_ini <= ano_fim:
                    eh_aluna = True
                    periodo_aluna_fim = periodo_fim
                    break

    eh_docente = False
    for _, docente in docentes_df.iterrows():
        if busca in str(docente["nome"]).lower():
            eh_docente = True
            break

    projetos = buscar_projetos_por_nome(nome, projetos_df)
    publicacoes = buscar_publicacoes_por_nome(nome, publicacoes_df)

    if eh_aluna and eh_docente:
        proj_aluna = [p for p in projetos if p.get("ano", p.get("ano_ini", 0)) <= periodo_aluna_fim]
        proj_docente = [p for p in projetos if p.get("ano", p.get("ano_ini", 0)) > periodo_aluna_fim]
        pub_aluna = [p for p in publicacoes if p.get("ano", 0) <= periodo_aluna_fim]
        pub_docente = [p for p in publicacoes if p.get("ano", 0) > periodo_aluna_fim]
        return proj_aluna, proj_docente, pub_aluna, pub_docente, True
    elif eh_aluna:
        return projetos, [], publicacoes, [], True
    else:
        return [], projetos, [], publicacoes, False

def lista_cursos(curso_str):
    if pd.isna(curso_str) or str(curso_str).strip() == "":
        return []
    return [c.strip() for c in str(curso_str).split(";")]

def badge_curso(curso_str):
    if pd.isna(curso_str) or str(curso_str).strip() == "":
        return ""
    cursos = lista_cursos(curso_str)
    badges = []
    for curso in cursos:
        curso = curso.strip()
        if "Técnico" in curso:
            badges.append('<span class="badge badge-tec">Técnico</span>')
        elif any(g in curso for g in ["Graduação", "Licenciatura", "Bacharelado"]):
            badges.append('<span class="badge badge-grad">Graduação</span>')
    return " ".join(badges)