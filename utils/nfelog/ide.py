def ide(level_dict, entrada_saida, tipo_declarante):
    
    ide = level_dict['ide']

    # MVN - Operação
    if entrada_saida == 'E':
        for palavra in ide['natOp'].split():
            if palavra.upper() in ('COMPRA', 'TRANSFERÊNCIA', 'DOAÇÃO', 'ARMAZENADO', 'INDUSTRIALIZADO', 'INDUSTRIALIZAÇÃO'):
                operacao = palavra[0].upper()
            else:
                if tipo_declarante == 'destinatario':
                    operacao = 'C'
                else:
                    operacao = 'R'            
            break
            
        
    else:
        for palavra in ide['natOp'].split():
            if palavra.upper() in('VENDA', 'TRANSFERÊNCIA', 'DOAÇÃO', 'ARMAZENADO', 'INDUSTRIALIZADO', 'INDUSTRIALIZAÇÃO', 'ARMAZENAGEM'):
                operacao = palavra[0].upper()
                break
            operacao = 'O'

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