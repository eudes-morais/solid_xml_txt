from .autxml import cep_format

def dest(level_dict):
    
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
    
    result_dest = {
        'razao_social': nome,
        'endereco': endereco,
        'numero': endereco_numero,
        'bairro': endereco_bairro,
        'municipio': endereco_cod_municipio,
        'uf': endereco_uf,
        'cep': endereco_cep,
        'cnpj': cnpj_destinatario
    }

    return result_dest