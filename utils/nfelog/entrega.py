from .autxml import cep_format

# def entrega(level_dict, cnpj_emitente, entrada_saida):
def entrega(level_dict):
    
    entrega = level_dict['entrega']

    # Razão Social e CNPJ do Destinatário
    if 'xNome' in entrega:
        nome = entrega['xNome'].upper()
    else:
        nome = ''
    cnpj = entrega['CNPJ']
    endereco = entrega['xLgr'].upper()
    if 'CEP' in entrega:
        cep = entrega['CEP']
        cep = cep_format(cep)
        # cep = f'{cep[0:2]}.{cep[2:5]}-{cep[5:]}'
    else:
        cep = ''
    # cep = f'{cep[0:2]}.{cep[2:5]}-{cep[5:]}'
    
    numero = entrega['nro']

    if 'xCpl' in entrega:
        complemento = entrega['xCpl']
    else:
        complemento = ''
    bairro = entrega['xBairro']
    uf = entrega['UF']
    municipio = entrega['cMun']

    # Talvez não seja necessário a verificação abaixo
    # if entrada_saida == 'E':
    #     if cnpj_emitente == cnpj:
    #         armazenagem = 'S'
    #     else:
    #         armazenagem = 'N'
    # else:
    #     if cnpj_emitente == cnpj:
    #         armazenagem = 'F'
    #     else:
    #         armazenagem = 'T'

    result_entrega = {
        # 'armazenagem': armazenagem,
        'nome': nome,
        'cnpj': cnpj,
        'endereco': endereco,
        'cep': cep,
        'numero': numero,
        'complemento': complemento,
        'bairro': bairro,
        'uf': uf,
        'municipio': municipio,
    }

    return result_entrega