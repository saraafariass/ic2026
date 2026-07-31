# 📊 Dashboard MDC - Meninas Digitais no Cerrado

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-blue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.14+-purple?logo=plotly)

**Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado**

[🚀 Acessar Dashboard](https://meninasdigitaisnocerrado.com.br)
</div>

---

## 🎯 Sobre o Projeto

Este dashboard apresenta uma visualização interativa dos dados do projeto **Meninas Digitais no Cerrado**, uma iniciativa do **IF Goiano - Campus Ceres** que busca incentivar a participação de meninas e mulheres nos cursos de Computação.

### 📈 O que você encontrará:

- **📊 Estudantes**: Participação, verticalização e bolsistas
- **👨‍🏫 Docentes**: Corpo docente e suas produções
- **🛠️ Projetos**: Por tipo (Ensino, Pesquisa, Extensão)
- **📚 Publicações**: Artigos e trabalhos científicos
- **🎉 Eventos e Premiações**: Participações e conquistas
- **🤝 Parcerias**: Redes e colaborações

---

## 🚀 Como Usar

### Localmente

1. **Clone o repositório:**
```bash
git clone https://github.com/saraafariass/ic2026.git
cd ic2026
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute o dashboard:**
```bash
streamlit run app.py
```

O dashboard abrirá no navegador em `http://localhost:8501`

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) | Linguagem principal |
| ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit) | Interface web interativa |
| ![Pandas](https://img.shields.io/badge/Pandas-1.5+-blue?logo=pandas) | Manipulação de dados |
| ![Plotly](https://img.shields.io/badge/Plotly-5.14+-purple?logo=plotly) | Gráficos interativos |
| ![WordCloud](https://img.shields.io/badge/WordCloud-1.8+-orange?logo=python) | Visualização de palavras |

---

## 📁 Estrutura do Projeto

```
ic2026/
├── app.py                  # Arquivo principal do dashboard
├── requirements.txt        # Dependências do projeto
├── README.md              # Documentação
├── alunas.csv             # Dados das alunas
├── docentes.csv           # Dados dos docentes
├── projetos.csv           # Dados dos projetos
├── publicacoes.csv        # Dados das publicações
├── eventos.csv            # Dados dos eventos
├── premiacoes.csv         # Dados das premiações
├── parcerias.csv          # Dados das parcerias
├── assets/
│   └── styles.py          # Estilos personalizados
└── icframework/           # Framework do IF Goiano
```

---

## 📊 Dados Abertos

Todos os dados são abertos e podem ser acessados em:
- [Projetos](https://meninasdigitaisnocerrado.com.br/projetos)
- [Publicações](https://meninasdigitaisnocerrado.com.br/publicacoes)
- [Premiações](https://meninasdigitaisnocerrado.com.br/premiacoes)

---

## 👥 Equipe

| Papel | Nome | GitHub | Lattes |
|-------|------|--------|--------|
| 💻 Bolsista PIBIC | Sara Luiz de Farias | [@saraafariass](https://github.com/saraafariass) | [Currículo](http://lattes.cnpq.br/2013698994793152) |
| 👩‍🏫 Coordenadora | Profa. Thalia Santos de Santana | - | [Currículo](http://lattes.cnpq.br/8063677996827079) |

---

## 📝 Como Citar

```
(Meninas Digitais no Cerrado, 2026)
```

**Referência bibliográfica completa:**

MENINAS DIGITAIS NO CERRADO. *Sistematização de dados abertos sobre gênero na Computação no Campus Ceres: 10 anos de Meninas Digitais no Cerrado.* Ceres: IF Goiano - Campus Ceres, 2026. Disponível em: [meninasdigitaisnocerrado.com.br](https://meninasdigitaisnocerrado.com.br). Acesso em: dia mes e ano.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

**Feito com ❤️ por Sara Farias (Meninas Digitais no Cerrado)**

[![GitHub](https://img.shields.io/badge/GitHub-100000?logo=github)](https://github.com/saraafariass/ic2026)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?logo=gmail)](mailto:meninasdigitais@ceres.ifgoiano.edu.br)

</div>
