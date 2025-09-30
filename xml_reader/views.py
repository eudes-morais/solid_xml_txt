# xml_reader/views.py
import xmltodict
from nfelog import ide, infnfe, emit
from django.shortcuts import render
from django.http import JsonResponse
# import xml.etree.ElementTree as ET


def upload_multiple_xml(request):
    if request.method == 'POST':
        # --- Captura os campos de operação individualmente ---
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        
        # Lista com os nomes de todas as operações possíveis
        tipos_de_operacao = [
            'comercializacao_nacional', 'comercializacao_internacional', 'producao',
            'transformacao', 'consumo', 'fabricacao', 'transporte', 'armazenamento'
        ]

        # Cria um dicionário para armazenar o status (0 ou 1) de cada operação
        # operacoes_status = {
        #     operacao: request.POST.get(operacao) for operacao in tipos_de_operacao
        # }

        # Armazenando o status de cada operação numa lista
        list_status = ''
        for operacao in tipos_de_operacao:
            list_status = list_status + request.POST.get(operacao)

        # Para demonstração, vamos imprimi-los no console do servidor
        # print(f"Mês recebido: {mes}")
        # print(f"Ano recebido: {ano}")
        # print(f"Status das Operações: {list_status}")
        # --- FIM DA ALTERAÇÃO ---

        # request.FILES.getlist() é a chave para obter múltiplos arquivos
        xml_files = request.FILES.getlist('xml_files[]')

        if not xml_files:
            return JsonResponse({'error': 'Nenhum arquivo XML enviado.'}, status=400)

        results = []
        for indice, xml_file in enumerate(xml_files, start=1):
            # Verifica a extensão de cada arquivo
            if not xml_file.name.endswith('.xml'):
                results.append({
                    'filename': xml_file.name,
                    'error': 'O arquivo não é um XML válido.'
                })
                continue # Pula para o próximo arquivo

            try:
                # Lê o conteúdo do arquivo
                file_content = xml_file.read().decode('utf-8')

                # Use xmltodict to parse and convert the XML document
                dict_created = xmltodict.parse(file_content)
                infnfe_dict = dict_created['NFeLog']['procNFe']['NFe']['infNFe'] # NF da SOLID

                # Lê a primeira NF inserida para extrair as informações da seção EM
                if indice == 1:
                    cnpj = emit.emit(infnfe_dict)
                    em = f'EM{cnpj}{mes}{ano}{list_status}'
                    print(em)

                if list(dict_created)[0] == 'nfeProc':
                    msg = "nfeProc"
                elif list(dict_created)[0] == 'NFeLog':                                        
                    msg = infnfe.infnfe(infnfe_dict)
                else:
                    msg = "Seção ainda não mapeada"
                
                msg = f'Arquivo {msg} parseado'
                
                results.append({
                    'filename': xml_file.name,
                    'success': True,
                    'root_tag': list(dict_created)[0],
                    'xml_content': msg
                })
                    
            except Exception as e:
                results.append({
                    'filename': xml_file.name,
                    'error': f'Ocorreu um erro inesperado: {str(e)}'
                })

        # --- Inclui os dados recebidos na resposta JSON ---
        return JsonResponse({
            'dados_recebidos': {
                'mes': mes,
                'ano': ano,
                'operacoes_status': list_status
            },
            'results': results
        })

    # Se a requisição for GET, renderiza a página de upload
    return render(request, 'upload.html')