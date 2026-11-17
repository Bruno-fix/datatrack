
import pandas as pd

from services.data_analysis import (
    calcular_indicadores,
    localizar_inconsistencias
)


def criar_dados_exemplo():
    """Cria um DataFrame com inconsistências conhecidas."""

    return pd.DataFrame({
        "nome": ["Ana", "Bruno", "Ana", "Carla"],
        "email": [
            "ana@exemplo.com",
            "bruno@exemplo.com",
            "ana@exemplo.com",
            None
        ],
        "setor": [
            "Financeiro",
            "TI",
            "Financeiro",
            "Comercial"
        ]
    })


def test_calcular_indicadores():
    df = criar_dados_exemplo()

    indicadores = calcular_indicadores(df)

    assert indicadores["total_registros"] == 4
    assert indicadores["registros_duplicados"] == 1
    assert indicadores["valores_ausentes"] == 1


def test_localizar_duplicatas():
    df = criar_dados_exemplo()

    duplicatas, _ = localizar_inconsistencias(df)

    assert len(duplicatas) == 2
    assert duplicatas["nome"].tolist() == ["Ana", "Ana"]


def test_localizar_linhas_incompletas():
    df = criar_dados_exemplo()

    _, incompletas = localizar_inconsistencias(df)

    assert len(incompletas) == 1
    assert incompletas.iloc[0]["nome"] == "Carla"


def test_dados_sem_inconsistencias():
    df = pd.DataFrame({
        "nome": ["Ana", "Bruno"],
        "email": [
            "ana@exemplo.com",
            "bruno@exemplo.com"
        ]
    })

    indicadores = calcular_indicadores(df)

    duplicatas, incompletas = localizar_inconsistencias(df)

    assert indicadores["registros_duplicados"] == 0
    assert indicadores["valores_ausentes"] == 0

    assert duplicatas.empty
    assert incompletas.empty
