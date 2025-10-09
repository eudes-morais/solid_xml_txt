def dest(level_dict, cnpj_emitente, entrada_saida):
    
    dest = level_dict['dest']

    # Razão Social e CNPJ do Destinatário
    nome = dest['xNome'].upper()
    cnpj_destinatario = dest['CNPJ']

    if entrada_saida == 'E':
        if cnpj_emitente == cnpj_destinatario:
            armazenagem = 'S'
        else:
            armazenagem = 'N'
    else:
        if cnpj_emitente == cnpj_destinatario:
            armazenagem = 'F'
        else:
            armazenagem = 'T'

    result_dest = {
        'armazenagem': armazenagem,
        'cnpj': cnpj_destinatario
    }

    return result_dest