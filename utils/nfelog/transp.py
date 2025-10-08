def transp(level_dict, cnpj_dest, cnpj_emit):
    
    transp = level_dict['transp']

    if list(transp)[1] == 'transporta':
        cnpj_transporte = transp['transporta']

        if cnpj_transporte == cnpj_dest:
            transporte = 'A'
        elif cnpj_transporte == cnpj_emit:
            transporte = 'F'
        else:
            transporte = 'T'
    else:
        transporte = 'F'

    # result_emit = {
    #     'cnpj': cnpj,
    #     'razao_social': razao_social,
    # }

    return transporte