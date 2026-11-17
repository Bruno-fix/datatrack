
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


# Apresentação da aplicação
st.title("📊 DataTrack")

st.caption(
    "Plataforma de Análise e Tratamento de Dados"
)

st.markdown(
    "Importe planilhas, identifique inconsistências "
    "e exporte dados tratados de forma simples e segura."
)

st.divider()

# Importação de arquivos
with st.container(border=True):
    st.subheader("1. Importação de Dados")

    st.caption(
        "Selecione um arquivo CSV ou Excel "
        "para iniciar a análise."
    )

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

        # Indicadores em cartões
        col1, col2, col3 = st.columns(3, gap="medium")

        col1.metric(
            label="Total de registros",
            value=total_registros,
            border=True
        )

        col2.metric(
            label="Registros duplicados",
            value=registros_duplicados,
            border=True
        )

        col3.metric(
            label="Valores ausentes",
            value=valores_ausentes,
            border=True
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
        st.subheader("2. Diagnóstico de Dados")

        duplicatas, linhas_incompletas = (
            localizar_inconsistencias(df)
        )

        # Cria abas para organizar o diagnóstico
        aba_duplicatas, aba_incompletas = st.tabs(
            [
                "🔁 Registros duplicados",
                "⚠️ Registros incompletos"
            ]
        )

        # Primeira aba: registros duplicados
        with aba_duplicatas:
            st.caption(
                f"{len(duplicatas)} ocorrência(s) "
                "envolvida(s) em duplicidades."
            )

            if not duplicatas.empty:
                st.dataframe(
                    duplicatas,
                    width="stretch",
                    hide_index=True
                )
            else:
                st.success(
                    "Nenhum registro duplicado encontrado."
                )

        # Segunda aba: registros incompletos
        with aba_incompletas:
            st.caption(
                f"{len(linhas_incompletas)} registro(s) "
                "com pelo menos um campo vazio."
            )

            if not linhas_incompletas.empty:
                st.dataframe(
                    linhas_incompletas,
                    width="stretch",
                    hide_index=True
                )
            else:
                st.success(
                    "Nenhum registro incompleto encontrado."
                )
                
        # Tratamento de dados
        with st.container(border=True):
            st.subheader("3. Tratamento de Dados")

            st.caption(
                "Escolha as operações que deseja aplicar. "
                "O arquivo original será preservado."
            )

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

            # Calcula os resultados
            registros_removidos = (
                df.shape[0] - df_tratado.shape[0]
            )

            valores_ausentes_restantes = int(
                df_tratado.isna().sum().sum()
            )

            # Indicadores em cartões
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Registros originais",
                df.shape[0],
                border=True
            )

            col2.metric(
                "Registros após tratamento",
                df_tratado.shape[0],
                border=True
            )

            col3.metric(
                "Valores ausentes restantes",
                valores_ausentes_restantes,
                border=True
            )

            st.caption(
                f"Registros removidos: {registros_removidos}"
            )

        # Exportação de dados
        with st.container(border=True):
            st.subheader("4. Exportação de Dados")

            st.caption(
                "Confira o resultado antes de baixar "
                "a planilha tratada."
            )

            # Pré-visualização
            st.dataframe(
                df_tratado.head(20),
                width="stretch",
                hide_index=True
            )

            # Converte o DataFrame em CSV
            csv = df_tratado.to_csv(
                index=False
            ).encode("utf-8-sig")

            # Botão de download
            st.download_button(
                label="📥 Baixar planilha tratada",
                data=csv,
                file_name="datatrack_tratado.csv",
                mime="text/csv",
                type="primary",
                width="stretch"
            )

    except Exception as erro:
        st.error(f"Não foi possível ler o arquivo: {erro}")

else:
    st.info("Para começar, importe uma planilha.")
