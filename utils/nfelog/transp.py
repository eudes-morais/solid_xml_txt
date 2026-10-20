def transp(level_dict):

    # A tag <transporta> pode não existir (ex.: frete sem ocorrência de transporte)
    transp = level_dict.get('transp', {}).get('transporta', {}) or {}

    # Nem toda NF com <transporta> traz CNPJ/xNome (ex.: transporte próprio).
    # Usa .get() para não quebrar quando os campos não existirem.

    # 0 (CIF - por conta do emitente), 
    # 1 (FOB - por conta do destinatário),
    # 2 (por conta de terceiros),
    # 3 (transporte próprio por conta do remetente),
    # 4 (transporte próprio por conta do destinatário) e
    # 9 (sem ocorrência de transporte). 

    transporte = {
        'cnpj': f"{transp.get('CNPJ', '')}",
        'razao_social': f"{transp.get('xNome', '')}"
    }

    return transporte