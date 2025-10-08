def dest(level_dict, razao_social, entrada_saida):
    
    dest = level_dict['dest']

    # Razão Social e CNPJ do Destinatário
    nome = dest['xNome'].upper()
    cnpj = dest['CNPJ']

    if entrada_saida == 'E':
        if razao_social.upper() == nome:
            armazenagem = 'S'
        else:
            armazenagem = 'N'
    else:
        if razao_social.upper() == nome:
            armazenagem = 'F'
        else:
            armazenagem = 'T'

    result_dest = {
        'armazenagem': armazenagem,
        'cnpj': cnpj
    }

    return result_dest