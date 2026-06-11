def ide(level_dict, tipo_declarante):
    
    ide = level_dict['ide']

    # MVN - Operação
    if tipo_declarante == 'destinatario':
        operacao = 'C'
    else:
        operacao = 'V'

    # MVN - Número NF
    numero_nf = ide['nNF']
    numero_nf = numero_nf.ljust(10)

    # MVN - Data Emissão NF
    data_emissao_nf = ide['dhEmi']
    ano = data_emissao_nf[:4]
    mes = data_emissao_nf[5:7]
    dia = data_emissao_nf[8:10]
    data_emissao_nf = f'{dia}/{mes}/{ano}'

    result_ide = {
        'operacao': operacao,
        'numero_nf': numero_nf,
        'data_emissao_nf': data_emissao_nf,
    }

    return result_ide