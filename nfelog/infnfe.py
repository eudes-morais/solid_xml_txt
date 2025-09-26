
def infnfe(level_dict):
    # Verifica se as informações contidas nas tags de nível inferior à tag INFNFE.
    
    # Tag IDE
    print(level_dict['ide'])
    print('\n')

    # Tag EMIT
    print(level_dict['emit'])
    print('\n')

    # Tag DEST
    print(level_dict['dest'])
    print('\n')
    
    # DET tem somente um elemento @nItem (dict)
    # ou se tem mais de um elemento (lista de dict)
    if type(level_dict['det']) == 'list':
        for value_dict in level_dict:
            print(value_dict['det'])
    else:
        print(level_dict['det'])
    
    msg = "NFeLog"

    return msg