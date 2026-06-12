import pandas as pd

def ler_dens_conc(ncm):
    # Inicialização de variáveis
    resultado = {}
    densidade = '00,00'
    concentracao = '000'

    df = pd.read_excel('app/media/densidade_concentracao.xlsx')

    # Filtrar diretamente no DataFrame (maneira mais eficiente)
    # IMPORTANTE SALIENTAR que o filtro abaixo busca A PRIMEIRA OCORRÊNCIA, logo se houver mais de uma ocorrência o filtro trará somente a primeira!
    filtro = (df['NCM'].astype(str) == ncm)

    df_filtrado = df[filtro]

    if not df_filtrado.empty:
        resultado = df_filtrado.iloc[0].to_dict()
        densidade = resultado['Densidade']
        concentracao = resultado['Concentração']

    dens_conc = {
        'densidade': densidade,
        'concentracao': concentracao,
    }

    return dens_conc