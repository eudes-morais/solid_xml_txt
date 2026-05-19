import pandas as pd

def ler_dens_conc(cnpj, ncm):
    # Lendo o arquivo mantendo o cabeçalho original
    df = pd.read_excel('app/media/densidade_concentracao.xlsx')

    # Convertendo para lista de dicionários
    dados_lista = df.to_dict(orient='records')

    resultado = {}

    for registro in dados_lista:
        if (str(registro['NCM']) == ncm) and (str(registro['CNPJ']) == cnpj):
            resultado = registro
    
    if resultado == {}:
        print(f"Nenhum resultado foi encontrado para NCM {ncm} com o CNPJ {cnpj}")
    else:
        print(f"Resultado: {resultado}")
    
    # Inicializando variáveis que  serão utilizadas tanto dentro como fora da função
    densidade = '0.0'
    concentracao = '0'

    # Caso tenha mais de um resultado    
    if len(resultado) > 1:
        print(f'Resultado:\n{resultado[0]}\n{resultado[1]}')
        print(f'Encontrado mais de um resultado para o mesmo NCM e o mesmo CNPJ:\n{resultado}')

    concentracao = str(resultado[0]['Concentração'])
    if len(concentracao) < 3:
        concentracao = concentracao.zfill(3)
    print(f'COncentração: {concentracao}')
    
    densidade = str(resultado[0]['Densidade'])
    if len(densidade) < 5:
        densidade = densidade.zfill(5)
    print(f'Densidade: {densidade}')

    dens_conc = {
        'densidade': densidade,
        'concentracao': concentracao,
    }

    print(dens_conc)

    return dens_conc