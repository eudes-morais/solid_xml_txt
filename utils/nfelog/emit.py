from .autxml import cep_format

def emit(level_dict):
    
    emit = level_dict['emit']

    # Razão Social e CNPJ do emitente
    nome = emit['xNome'].upper()
    cnpj_emitente = emit['CNPJ']
    endereco = emit['enderEmit']['xLgr'].upper()
    endereco_numero = emit['enderEmit']['nro']
    endereco_bairro = emit['enderEmit']['xBairro'].upper()
    endereco_cod_municipio = emit['enderEmit']['cMun']
    endereco_uf = emit['enderEmit']['UF']
    endereco_cep = emit['enderEmit']['CEP']
    endereco_cep = cep_format(endereco_cep)
    endereco_complemento = (emit.get('enderEmit', {}).get('xCpl') or '').upper()
    
    result_emit = {
        'razao_social': nome,
        'endereco': endereco,
        'numero': endereco_numero,
        'bairro': endereco_bairro,
        'municipio': endereco_cod_municipio,
        'uf': endereco_uf,
        'cep': endereco_cep,
        'cnpj': cnpj_emitente,
        'complemento': endereco_complemento
    }

    return result_emit

# def emit(level_dict):
    
#     emit = level_dict['emit']

#     # EM e MVN - CNPJ Adquirente/Fornec
#     cnpj = str(emit['CNPJ'])

#     # MVN - Razão Social Adq/Fornec
#     razao_social = emit['xNome']
#     razao_social = razao_social.upper()

#     result_emit = {
#         'cnpj': cnpj,
#         'razao_social': razao_social,
#     }

#     return result_emit