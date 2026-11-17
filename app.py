
import pandas as pd
import streamlit as st

from services.data_processing import tratar_dados
from services.data_analysis import (
    calcular_indicadores,
    localizar_inconsistencias
)

# Configuração da página
st.set_page_config(
    page_title="DataTrack",
    page_icon="📊",
    layout="wide"
)

# Apresentação
st.title("DataTrack")
st.subheader("Sistema de Análise e Tratamento de Dados")

st.write(
    "Importe, analise e organize suas planilhas "
    "de maneira simples e eficiente."
)

# Importação de arquivos
st.header("Importação de Dados")

uploaded_file = st.file_uploader(
    "Selecione uma planilha CSV ou Excel",
    type=["csv", "xlsx"]
)

# Verifica se o usuário enviou um arquivo
if uploaded_file is not None:
    try:
        # Identifica o formato do arquivo
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(
                uploaded_file,
                sep=","
            )
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Arquivo importado com sucesso!")

        # Informações sobre os dados
        st.write(f"Total de registros: {df.shape[0]}")
        st.write(f"Total de colunas: {df.shape[1]}")

        # Exibe as primeiras 20 linhas
        st.subheader("Pré-visualização dos Dados")

        st.dataframe(
            df.head(20),
            width="stretch",
            hide_index=True
        )

        # Análise de qualidade dos dados
        st.subheader("Qualidade dos Dados")

        # Obtém os indicadores de qualidade
        indicadores = calcular_indicadores(df)

        total_registros = indicadores["total_registros"]
        registros_duplicados = indicadores["registros_duplicados"]
        valores_ausentes = indicadores["valores_ausentes"]

        # Criação dos indicadores
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total de registros",
            total_registros
        )

        col2.metric(
            "Registros duplicados",
            registros_duplicados
        )

        col3.metric(
            "Valores ausentes",
            valores_ausentes
        )

        # Exibe um aviso se houver problemas
        if registros_duplicados > 0 or valores_ausentes > 0:
            st.warning(
                "Foram encontradas inconsistências nos dados."
            )
        else:
            st.success(
                "Nenhuma duplicata ou valor ausente encontrado!"
            )
    
        # Diagnóstico detalhado dos dados
        st.subheader("Diagnóstico de Dados")

        # Obtém os registros com inconsistências
        duplicatas, linhas_incompletas = (
            localizar_inconsistencias(df)
        )

        # Apresenta as duplicatas
        with st.expander("Visualizar registros duplicados"):
            if not duplicatas.empty:
                st.dataframe(
                    duplicatas,
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("Nenhum registro duplicado encontrado.")

        # Apresenta os registros incompletos
        with st.expander("Visualizar registros incompletos"):
            if not linhas_incompletas.empty:
                st.dataframe(
                    linhas_incompletas,
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("Nenhum registro incompleto encontrado.")
    
        # Tratamento de dados
        st.subheader("Tratamento de Dados")

        # Opções de tratamento
        remover_duplicatas = st.checkbox(
            "Remover registros duplicados"
        )

        tratamento_ausentes = st.selectbox(
            "Como deseja tratar os valores ausentes?",
            [
                "Manter valores ausentes",
                "Remover linhas incompletas",
                "Preencher textos com 'Não informado'"
            ]
        )

        # Executa as regras de tratamento
        df_tratado = tratar_dados(
            df=df,
            remover_duplicatas=remover_duplicatas,
            tratamento_ausentes=tratamento_ausentes
        )

        # Indicadores antes e depois
        col1, col2 = st.columns(2)

        col1.metric(
            "Registros originais",
            df.shape[0]
        )

        col2.metric(
            "Registros após tratamento",
            df_tratado.shape[0]
        )

        valores_ausentes_restantes = int(
            df_tratado.isna().sum().sum()
        )

        st.metric(
            "Valores ausentes restantes",
            valores_ausentes_restantes
        )

        # Pré-visualização
        st.write("Pré-visualização dos dados tratados")

        st.dataframe(
            df_tratado.head(20),
            width="stretch",
            hide_index=True
        )

        # Exportação dos dados tratados
        csv = df_tratado.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="Baixar planilha tratada",
            data=csv,
            file_name="datatrack_tratado.csv",
            mime="text/csv"
        )

    except Exception as erro:
        st.error(f"Não foi possível ler o arquivo: {erro}")

else:
    st.info("Para começar, importe uma planilha.")
