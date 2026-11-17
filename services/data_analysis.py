
import pandas as pd


def calcular_indicadores(df: pd.DataFrame) -> dict[str, int]:
    """
    Calcula indicadores de qualidade de um DataFrame.
    """

    indicadores = {
        "total_registros": df.shape[0],
        "registros_duplicados": int(df.duplicated().sum()),
        "valores_ausentes": int(df.isna().sum().sum())
    }

    return indicadores


def localizar_inconsistencias(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Localiza registros duplicados e incompletos.
    """

    duplicatas = df.loc[
        df.duplicated(keep=False)
    ].copy()

    linhas_incompletas = df.loc[
        df.isna().any(axis=1)
    ].copy()

    return duplicatas, linhas_incompletas
