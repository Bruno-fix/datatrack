# DataTrack

**Aplicação para Análise de Qualidade e Limpeza de Dados**

O **DataTrack** é uma aplicação web desenvolvida em Python, projetada para analisar, validar e realizar a limpeza de conjuntos de dados estruturados provenientes de arquivos CSV e Excel.

O projeto tem como objetivo simplificar tarefas comuns relacionadas à qualidade dos dados, incluindo a detecção de registros duplicados, a análise de valores ausentes e o tratamento de inconsistências.

Desenvolvido com **Streamlit e Pandas**, o DataTrack oferece uma interface interativa para exploração de conjuntos de dados e exportação dos resultados processados.

## Demonstração Online

Acesse a aplicação DataTrack diretamente pelo navegador:

[Experimentar o DataTrack](https://datatrack-bruno.streamlit.app/)

## Tecnologias

- Python
- Streamlit
- Pandas
- OpenPyXL
- Pytest
- Git

## Funcionalidades

### Importação de Dados

- Importação de arquivos CSV e Excel (.xlsx)
- Pré-visualização dos conjuntos de dados importados
- Exibição da quantidade de linhas e colunas

### Análise da Qualidade dos Dados

- Detecção de registros duplicados
- Identificação de valores ausentes
- Exibição de indicadores de qualidade dos dados
- Inspeção de registros duplicados e incompletos

### Limpeza de Dados

- Remoção de registros duplicados
- Remoção de linhas que contenham valores ausentes
- Preenchimento de valores ausentes em colunas de texto
- Preservação do conjunto de dados original durante o processamento

### Exportação de Dados

- Exportação dos conjuntos de dados processados em formato CSV
- Download dos dados tratados diretamente pela interface

## Estrutura do Projeto

```text
datatrack/
├── services/
│   ├── __init__.py
│   ├── data_analysis.py
│   └── data_processing.py
├── tests/
│   ├── test_data_analysis.py
│   └── test_data_processing.py
├── .gitignore
├── app.py
├── exemplo.csv
├── README.md
├── requirements-dev.txt
└── requirements.txt
```

## Arquitetura

A aplicação segue uma arquitetura modular, com responsabilidades separadas entre seus componentes.

- `app.py`: Gerencia a interface desenvolvida com Streamlit e as interações do usuário.
- `services/data_analysis.py`: Calcula indicadores de qualidade e identifica inconsistências nos dados.
- `services/data_processing.py`: Executa operações de limpeza, preservando o DataFrame original.
- `tests/`: Contém testes automatizados para os módulos de análise e processamento.

Essa separação melhora a manutenibilidade, a testabilidade e a reutilização do código.

## Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/Bruno-fix/datatrack.git
cd datatrack
```

### 2. Criar um Ambiente Virtual

```bash
py -m venv .venv
```

### 3. Ativar o Ambiente Virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as Dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Executar a Aplicação

```bash
python -m streamlit run app.py
```

Acesse a URL local exibida no terminal.

## Execução dos Testes

Instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute a suíte de testes automatizados:

```bash
python -m pytest -v
```

Atualmente, o projeto possui **oito testes automatizados**, abrangendo as operações de análise e limpeza de dados.

## Conjunto de Dados de Exemplo

O repositório inclui o arquivo `exemplo.csv`, que contém um conjunto de dados fictício com registros duplicados e valores ausentes.

Esse arquivo pode ser utilizado para explorar e testar as funcionalidades de validação e limpeza oferecidas pela aplicação.

## Limitações Atuais

- A importação de arquivos CSV utiliza atualmente valores separados por vírgulas.
- A importação de arquivos Excel realiza, por padrão, a leitura da primeira planilha.
- A detecção de duplicatas compara todas as colunas de cada registro.
- O preenchimento de valores ausentes está limitado às colunas de texto.
- A aplicação processa os conjuntos de dados importados sem armazenamento persistente.

## Status do Projeto

**MVP funcional — Melhorias futuras planejadas.**

## Licença

O projeto ainda não possui uma licença definida.