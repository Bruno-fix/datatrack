
import pandas as pd

from services.data_processing import tratar_dados


def criar_dados_exemplo():
    """Cria dados fictícios para os testes."""

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


def test_remover_duplicatas():
    df = criar_dados_exemplo()

    resultado = tratar_dados(
        df,
        remover_duplicatas=True,
        tratamento_ausentes="Manter valores ausentes"
    )

    assert len(resultado) == 3
    assert resultado.duplicated().sum() == 0


def test_remover_linhas_incompletas():
    df = criar_dados_exemplo()

    resultado = tratar_dados(
        df,
        remover_duplicatas=True,
        tratamento_ausentes="Remover linhas incompletas"
    )

    assert len(resultado) == 2
    assert resultado.isna().sum().sum() == 0


def test_preencher_textos_ausentes():
    df = criar_dados_exemplo()

    resultado = tratar_dados(
        df,
        remover_duplicatas=True,
        tratamento_ausentes="Preencher textos com 'Não informado'"
    )

    email_carla = resultado.loc[
        resultado["nome"] == "Carla",
        "email"
    ].iloc[0]

    assert len(resultado) == 3
    assert email_carla == "Não informado"


def test_preservar_dados_originais():
    df = criar_dados_exemplo()
    copia_original = df.copy(deep=True)

    tratar_dados(
        df,
        remover_duplicatas=True,
        tratamento_ausentes="Remover linhas incompletas"
    )

    pd.testing.assert_frame_equal(
        df,
        copia_original
    )
