# Dashboard Meninas Digitais no Cerrado

Dashboard interativo com a sistematização de 10 anos de dados abertos sobre gênero na Computação no Campus Ceres, desenvolvido no âmbito do projeto **Meninas Digitais no Cerrado**.

🔗 **Acesse o dashboard:** [mdc-dashboard.streamlit.app](https://mdc-dashboard.streamlit.app/)

📍 Também disponível embutido na página de [Indicadores](https://meninasdigitaisnocerrado.com.br/indicadores) do site oficial.

---

## Sobre o projeto

Este projeto integra o edital institucional **Nº 11 de 03 de abril de 2025 (PIBIC)**, com o tema *"Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado"*.

O dashboard reúne e visualiza dados sobre:

- **Estudantes**: participação de alunas no Ensino Médio Técnico e na Graduação
- **Docentes**: corpo docente envolvido no projeto
- **Projetos**: iniciativas de ensino, pesquisa e extensão
- **Publicações**: produção científica ao longo dos anos
- **Eventos e Premiações**: participações e reconhecimentos
- **Parcerias**: articulação com a Rede Nacional RENACEE_MD

## Equipe

| Papel | Nome |
|---|---|
| Bolsista PIBIC | Sara Luiz de Farias |
| Coordenadora | Profa. Thalia Santos de Santana |

**Instituição:** IF Goiano - Campus Ceres

## Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) - interface web interativa
- [Pandas](https://pandas.pydata.org/) - manipulação de dados
- [Plotly](https://plotly.com/python/) - gráficos interativos

## Estrutura do repositório

```
ic2026/
├── app.py                 # aplicação principal (Streamlit)
├── requirements.txt       # dependências Python
├── assets/
│   └── styles.py           # estilos (CSS) do dashboard
├── alunas.csv
├── docentes.csv
├── projetos.csv
├── publicacoes.csv
├── premiacoes.csv
└── eventos.csv
```

## Como rodar localmente

```bash
# clonar o repositório
git clone https://github.com/saraafariass/ic2026.git
cd ic2026

# instalar as dependências
pip install -r requirements.txt

# rodar o dashboard
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`.

## Deploy

O dashboard está hospedado gratuitamente no [Streamlit Community Cloud](https://share.streamlit.io/), conectado diretamente a este repositório. Qualquer atualização enviada para a branch `main` é refletida automaticamente no app publicado.

## Fontes dos dados

Os dados são atualizados manualmente a partir das informações disponíveis no [site oficial do projeto](https://meninasdigitaisnocerrado.com.br).

## Como citar

```
MENINAS DIGITAIS NO CERRADO. Sistematização de dados abertos sobre gênero
na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado.
Ceres: IF Goiano - Campus Ceres, 2026. Disponível em:
https://meninasdigitaisnocerrado.com.br. Acesso em: dia mês ano.
```

---

Feito com 🤍 por Sara Farias - Meninas Digitais no Cerrado
