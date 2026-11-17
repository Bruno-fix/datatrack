
def tratar_dados(df, remover_duplicatas, tratamento_ausentes):
    """
    Aplica tratamentos em um DataFrame,
    preservando os dados originais.
    """

    df_tratado = df.copy()

    # Remoção de registros duplicados
    if remover_duplicatas:
        df_tratado = df_tratado.drop_duplicates()

    # Tratamento de valores ausentes
    if tratamento_ausentes == "Remover linhas incompletas":
        df_tratado = df_tratado.dropna()

    elif tratamento_ausentes == "Preencher textos com 'Não informado'":
        colunas_texto = df_tratado.select_dtypes(
            include=["object", "string"]
        ).columns

        df_tratado[colunas_texto] = (
            df_tratado[colunas_texto].fillna("Não informado")
        )

    return df_tratado
