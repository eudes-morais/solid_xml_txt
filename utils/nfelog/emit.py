def emit(level_dict):
    
    emit = level_dict['emit']

    # EM e MVN - CNPJ Adquirente/Fornec
    cnpj = emit['CNPJ']

    # MVN - Razão Social Adq/Fornec
    razao_social = emit['xNome']
    razao_social = razao_social.upper()

    result_emit = {
        'cnpj': cnpj,
        'razao_social': razao_social,
    }

    return result_emit