import xmltodict, traceback

def det(infnfe_dict):
    # Caso a tag DET tenha somente um elemento @nItem ele é um dicionário (dict)
    # Caso a tag DET tenha mais de um elemento, ela é uma lista de dicionário (list dict)
    if type(infnfe_dict['det']) is list:
        for value_dict in infnfe_dict['det']:
            # print(value_dict['@nItem'], value_dict['prod']['NCM'])
            value_ncm = value_dict['prod']['NCM']
            
            codigo_tpn = ler_codigo_ncm(value_ncm)

            quantidade = value_dict['prod']['qCom']
            
            unidade_medida = value_dict['prod']['uCom']
            unidade_medida = unidade_medida[0].upper()
    else:
        value_ncm = infnfe_dict['det']['prod']['NCM']
        
        codigo_tpn = ler_codigo_ncm(value_ncm)
        
        qtde = infnfe_dict['det']['prod']['qCom']
        qtde = qtde.split('.')
        qtde_inteiro = qtde[0]
        qtde_cents = qtde[1]
        
        qtde_inteiro = qtde_inteiro.zfill(9)
        qtde_inteiro = f'{qtde_inteiro[:3]}.{qtde_inteiro[3:6]}.{qtde_inteiro[6:]}'
        qtde_cents = qtde_cents[:3].ljust(3,'0')
        quantidade = f'{qtde_inteiro},{qtde_cents}'
        unidade_medida = infnfe_dict['det']['prod']['uCom']
        unidade_medida = unidade_medida[0].upper()
    
    print(codigo_tpn)
    
    result_det = {
        'codigo_tpn': codigo_tpn,
        'quantidade': quantidade,
        'unidade_medida': unidade_medida
    }
    
    return result_det

# Consome o arquivo PRODUTOS.XML para converter o Código NCM em Código Produto NCM dos produtos controlados (PR)
def ler_codigo_ncm(ncm):
    try:
        # Abre o arquivo
        with open('produtos.xml', 'r') as file:
            file_xml = file.read()
        
        # Use xmltodict to parse and convert the XML document
        dict_tpn = xmltodict.parse(file_xml)

        tpn = 'PR00000000'
        for codigo_ncm in dict_tpn['produtos']['produto']:
            if codigo_ncm['codigoNcm'] == ncm:
                codigo_produto_ncm = codigo_ncm['codigoProdutoNcm']
                tpn = f'PR{codigo_produto_ncm}'
                break

    except:
        tpn = traceback.format_exc()
    
    return tpn