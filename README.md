# Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado

Dashboard interativo desenvolvido em **Python** e **Streamlit** para visualização, sistematização e análise de 10 anos de indicadores históricos (2016 - 2026) do projeto **Meninas Digitais no Cerrado**.

---

## Pré-requisitos

* **Python 3.10+** instalado no seu computador.
* **Git** configurado (opcional, para clonar o repositório).

---

## Como Executar o Projeto

Siga os passos abaixo no terminal do seu computador (Linux, macOS ou Windows):

### 1. Clonar o repositório

```bash
git clone https://github.com/saraafariass/ic2026.git
cd ic2026
```

### 2. Criar e ativar o ambiente virtual (Recomendado)

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando - CMD):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instalar as dependências

Com o ambiente ativado, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Executar o Dashboard

Execute a aplicação via Streamlit:

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente no seu navegador padrão no endereço:

```
http://localhost:8501
```

---

## Dependências Principais

* **streamlit** — Interface web interativa
* **pandas** — Manipulação e tratamento das bases de dados
* **plotly** — Gráficos interativos e dinâmicos
* **matplotlib** — Renderização de gráficos estáticos
* **wordcloud** — Geração de nuvem de palavras
* **nltk** — Processamento de linguagem natural (Stopwords)

---

## Estrutura de Pastas

```
ic2026/
├── assets/          # Estilos CSS
├── data/            # 7 csvs
├── utils/           # Módulos de carregamento, filtros e componentes visuais
├── views/           # Módulos de cada aba do painel
├── app.py           # Arquivo principal de execução
├── requirements.txt # Lista de dependências Python
└── README.md        # Documentação do projeto
```

---

## Equipe e Contato

* **Bolsista PIBIC:** Sara Luiz de Farias ([Lattes](http://lattes.cnpq.br/))
* **Coordenadora:** Profa. Thalia Santos de Santana ([Lattes](http://lattes.cnpq.br/))
* **Instituição:** Instituto Federal Goiano - Campus Ceres
