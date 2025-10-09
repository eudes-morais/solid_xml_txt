def transp(level_dict, cnpj_dest, cnpj_emit):
    
    transp = level_dict['transp']

    # Transforma o dicionário numa lista e retira o elemento q se deseja. Neste caso é a tag TRANSPORTA
    # if list(transp)[1] == 'transporta':

    # 0 (CIF - por conta do emitente), 
    # 1 (FOB - por conta do destinatário),
    # 2 (por conta de terceiros),
    # 3 (transporte próprio por conta do remetente),
    # 4 (transporte próprio por conta do destinatário) e
    # 9 (sem ocorrência de transporte). 

    if transp['modFrete'] == '0' or transp['modFrete'] == '3':
        transporte = 'F'
    elif transp['modFrete'] == '1' or transp['modFrete'] == '4':
        transporte = 'A'
    else: # ['modFrete'] == '2':
        transporte = 'T'

    # result_emit = {
    #     'cnpj': cnpj,
    #     'razao_social': razao_social,
    # }

    return transporte