# xml_reader/views.py
import xmltodict
from django.shortcuts import render
from django.http import JsonResponse
from nfelog.infnfe import infnfe
# import xml.etree.ElementTree as ET


def upload_multiple_xml(request):
    if request.method == 'POST':
        # request.FILES.getlist() é a chave para obter múltiplos arquivos
        xml_files = request.FILES.getlist('xml_files[]')

        if not xml_files:
            return JsonResponse({'error': 'Nenhum arquivo XML enviado.'}, status=400)

        results = []
        for xml_file in xml_files:
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

                if list(dict_created)[0] == 'nfeProc':
                    msg = "nfeProc"
                elif list(dict_created)[0] == 'NFeLog':                    
                    infnfe_dict = dict_created['NFeLog']['procNFe']['NFe']['infNFe'] # NF da SOLID
                    msg = infnfe(infnfe_dict)
                else:
                    msg = "ainda não mapeado"
                
                msg = f'Arquivo {msg} parseado'

                # Analisa (parse) o XML
                # root = ET.fromstring(file_content)

                # Extrai os dados (neste exemplo, o nome do elemento raiz e o conteúdo formatado)
                # formatted_xml = ET.tostring(root, encoding='unicode', method='xml')

                # root_tag = root.tag

                results.append({
                    'filename': xml_file.name,
                    'success': True,
                    # 'root_tag': root_tag,
                    # 'xml_content': formatted_xml
                    'root_tag': list(dict_created)[0],
                    'xml_content': msg
                })
                    
            # except ET.ParseError:
            #     results.append({
            #         'filename': xml_file.name,
            #         'error': 'Erro ao analisar o arquivo. Verifique o formato.'
            #     })
            except Exception as e:
                results.append({
                    'filename': xml_file.name,
                    'error': f'Ocorreu um erro inesperado: {str(e)}'
                })

        return JsonResponse({'results': results})

    # Se a requisição for GET, renderiza a página de upload
    return render(request, 'upload.html')