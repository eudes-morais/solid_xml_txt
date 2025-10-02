def ide(level_dict):
    
    ide = level_dict['ide']

    # MVN - Entrada-Saída
    entrada_saida = 'E' if ide['tpNF'] == '0' else 'S'

    # MVN - Operação
    for palavra in ide['natOp'].split():
        if entrada_saida == 'E':
            if palavra.upper() == 'COMPRA':
                operacao = 'C'
            elif palavra.upper() == 'TRANSFERÊNCIA':
                operacao = 'T'
            elif palavra.upper() == 'DOAÇÃO':
                operacao = 'D'
            elif palavra.upper() == 'ARMAZENADO':
                operacao = 'A'
            elif palavra.upper() == 'INDUSTRIALIZADO':
                operacao = 'P'
            elif palavra.upper() == 'INDUSTRIALIZAÇÃO':
                operacao = 'I'
            else:
                operacao = 'R'
        else:
            if palavra.upper() == 'VENDA':
                operacao = 'V'
            elif palavra.upper() == 'TRANSFERÊNCIA':
                operacao = 'T'
            elif palavra.upper() == 'DOAÇÃO':
                operacao = 'D'
            elif palavra.upper() == 'ARMAZENADO':
                operacao = 'A'
            elif palavra.upper() == 'INDUSTRIALIZADO':
                operacao = 'I'
            elif palavra.upper() == 'INDUSTRIALIZAÇÃO':
                operacao = 'P'
            elif palavra.upper() == 'ARMAZENAGEM':
                operacao = 'R'
            else:
                operacao = 'S'

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
        'entrada_saida': entrada_saida,
        'operacao': f'{entrada_saida}{operacao}',
        'numero_nf': numero_nf,
        'data_emissao_nf': data_emissao_nf,
    }

    return result_ide