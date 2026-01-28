import pandas as pd

def ler_dens_conc(cnpj, ncm):

    # Lendo o arquivo mantendo o cabeçalho original
    df = pd.read_excel('app/media/densidade_concentracao.xlsx')

    # Convertendo para lista de dicionários
    dados_lista = df.to_dict(orient='records')

    resultado = [registro for registro in dados_lista if (str(registro['NCM']) == ncm) and (str(registro['CNPJ']) == cnpj) ]

    # Caso não tenha encontrado resultado
    if not resultado:
        print(f"Nenhum resultado encontrado para NCM {ncm}")

    
    # Caso tenha mais de um resultado    
    if len(resultado) > 1:
        print(f'Encontrado mais de um resultado para o mesmo NCM e o mesmo CNPJ:\n{resultado}')

    concentracao = str(resultado[0]['Concentração'])

    if len(concentracao) < 3:
        concentracao = concentracao.zfill(3)

    dens_conc = {
        'densidade': resultado[0]['Densidade'],
        'concentracao': concentracao,
    }

    return dens_conc