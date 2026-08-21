import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    alunas = pd.read_csv("data/alunas.csv")
    docentes = pd.read_csv("data/docentes.csv")
    projetos = pd.read_csv("data/projetos.csv")
    publicacoes = pd.read_csv("data/publicacoes.csv")
    premiacoes = pd.read_csv("data/premiacoes.csv")
    eventos = pd.read_csv("data/eventos.csv", on_bad_lines="skip")
    parcerias = pd.read_csv("data/parcerias.csv")

    eventos["ano"] = pd.to_numeric(eventos["ano"], errors="coerce").astype("Int64")
    premiacoes["ano"] = pd.to_numeric(premiacoes["ano"], errors="coerce").astype("Int64")

    return alunas, docentes, projetos, publicacoes, premiacoes, eventos, parcerias

def filtrar_periodo(df, ano_inicio, ano_fim):
    return df[(df["ano_ini"] <= ano_fim) & (df["ano_fim"] >= ano_inicio)]