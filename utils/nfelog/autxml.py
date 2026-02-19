def cep_format(cep):
    if cep:
        cep = f'{cep[0:2]}.{cep[2:5]}-{cep[5:]}'
    else:
        cep = ''
    
    return cep