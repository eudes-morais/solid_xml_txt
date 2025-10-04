def dest(level_dict):
    
    dest = level_dict['dest']

    # Razão Social do Destinatário
    nome = dest['xNome'].upper()

    result_dest = {
        'nome': nome
    }

    return result_dest