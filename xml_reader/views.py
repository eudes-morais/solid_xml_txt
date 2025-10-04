# xml_reader/views.py
import xmltodict
from utils.nfelog import ide, infnfe, emit, dest
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
        for op in tipos_de_operacao:
            list_status = list_status + request.POST.get(op)

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
                # Seção EM
                if indice == 1:
                    var_emit = emit.emit(infnfe_dict)
                    cnpj = var_emit['cnpj']
                    em = f'EM{cnpj}{mes}{ano}{list_status}'
                
                # Seção MVN
                var_ide = ide.ide(infnfe_dict)
                entrada_saida = var_ide['entrada_saida']
                operacao = var_ide['operacao']
                razao_social = var_emit['razao_social']
                data_emissao_nf = var_ide['data_emissao_nf']
                if entrada_saida == 'E' :
                    local_armazenagem = dest.dest(infnfe_dict)
                    if razao_social == local_armazenagem['nome']:
                        armazenagem = 'S'
                    else:
                        armazenagem = 'N'
                else:
                    resp_armazenagem = dest.dest(infnfe_dict)
                    if razao_social == resp_armazenagem['nome']:
                        armazenagem = 'F'
                    else:
                        armazenagem = 'T'

                results.append({
                    'filename': xml_file.name,
                    'success': True,
                    'root_tag': 'Lido com sucesso!',
                    'xml_content': f'{em}\n{entrada_saida}{operacao}{razao_social}{data_emissao_nf}{armazenagem}'
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