from .autxml import cep_format

def dest(level_dict, cnpj_emitente, entrada_saida, armazenagem_form):
    
    dest = level_dict['dest']

    # Razão Social e CNPJ do Destinatário
    nome = dest['xNome'].upper()
    cnpj_destinatario = dest['CNPJ']
    endereco = dest['enderDest']['xLgr'].upper()
    endereco_numero = dest['enderDest']['nro']
    endereco_bairro = dest['enderDest']['xBairro']
    endereco_cod_municipio = dest['enderDest']['cMun']
    endereco_uf = dest['enderDest']['UF']
    endereco_cep = dest['enderDest']['CEP']
    endereco_cep = cep_format(endereco_cep)


    # if entrada_saida == 'E':
    #     if cnpj_emitente == cnpj_destinatario:
    #         armazenagem = 'S'
    #     else:
    #         armazenagem = 'N'
    # else:
    #     if cnpj_emitente == cnpj_destinatario:
    #         armazenagem = 'F'
    #     else:
    #         armazenagem = 'T'
    
    if entrada_saida == 'E':
        if armazenagem_form == 'S':
            armazenagem = 'S'
        else:
            armazenagem = 'N'
    else:
        if armazenagem_form == 'N':
            armazenagem = 'F'
        else:
            armazenagem = 'T'

    result_dest = {
        'destinatario': nome,
        'endereco': endereco,
        'numero': endereco_numero,
        'bairro': endereco_bairro,
        'municipio': endereco_cod_municipio,
        'uf': endereco_uf,
        'cep': endereco_cep,
        'armazenagem': armazenagem,
        'cnpj': cnpj_destinatario
    }

    return result_dest