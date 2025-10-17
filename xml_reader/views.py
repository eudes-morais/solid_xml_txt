# xml_reader/views.py
import xmltodict
from utils.nfelog import ide, infnfe, emit, dest, transp,det,entrega
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
                
                if list(dict_created)[0] == 'nfeProc':
                    infnfe_dict = dict_created['nfeProc']['NFe']['infNFe'] # NF da SOLID
                else:
                    infnfe_dict = dict_created['NFeLog']['procNFe']['NFe']['infNFe'] # NF da SOLID

                # Lê a primeira NF inserida para extrair as informações para a seção EM
                secao_em = ''
                if indice == 1:
                    # Seção EM
                    var_emit = emit.emit(infnfe_dict)
                    cnpj_emitente = var_emit['cnpj']
                    secao_em = f'EM{cnpj_emitente}{mes}{ano}{list_status}\n'
                
                # Seção MVN
                var_ide = ide.ide(infnfe_dict)
                entrada_saida = var_ide['entrada_saida']
                operacao = var_ide['operacao']
                razao_social = var_emit['razao_social']
                razao_social = razao_social.ljust(69)
                data_emissao_nf = var_ide['data_emissao_nf']
                destinatario = dest.dest(infnfe_dict, cnpj_emitente, entrada_saida)
                armazenagem = destinatario['armazenagem']
                cnpj_destinatario = destinatario['cnpj'] # CNPJ utilizado para verificar o responsável pelo transporte
                transporte = transp.transp(infnfe_dict, cnpj_destinatario, cnpj_emitente)
                secao_mvn = f'MVN{entrada_saida}{operacao}{razao_social}{data_emissao_nf}{armazenagem}{transporte}'

                # Subseção MM
                var_det = det.det(infnfe_dict)
                ncm = var_det['codigo_tpn']
                quantidade = var_det['quantidade']
                unidade_medida = var_det['unidade_medida']
                subsecao_mm = f'\nMM{ncm}00000,00{quantidade}{unidade_medida}'

                # Subseção MA (o entendimento aplicado é que esta seção só existirá se na NFe existir a tag ENTREGA)
                if 'entrega' in infnfe_dict:
                    var_armazenagem = entrega.entrega(infnfe_dict)
                    cnpj_armazenadora = var_armazenagem['cnpj']
                    razao_social_armazenadora = var_armazenagem['nome']
                    razao_social_armazenadora = razao_social_armazenadora.ljust(69)
                    endereco_armazenadora = var_armazenagem['endereco']
                    endereco_armazenadora = endereco_armazenadora.ljust(69)
                    cep_armazenadora = var_armazenagem['cep']
                    numero_armazenadora = var_armazenagem['numero']                    
                    complemento_armazenadora = var_armazenagem['complemento']
                    complemento_armazenadora = complemento_armazenadora.ljust(20)
                    bairro_armazenadora = var_armazenagem['bairro']
                    bairro_armazenadora = bairro_armazenadora.ljust(30)
                    uf_armazenadora = var_armazenagem['uf']
                    municipio_armazenadora = var_armazenagem['municipio']

                    subsecao_ma = f'\n{cnpj_armazenadora}{razao_social_armazenadora}{endereco_armazenadora}{cep_armazenadora}{numero_armazenadora}{complemento_armazenadora}'
                    subsecao_ma = f'{subsecao_ma}{bairro_armazenadora}{uf_armazenadora}{municipio_armazenadora}'
                else:
                    subsecao_ma = ''
                    
                txt = f'{secao_em}{secao_mvn}{subsecao_mm}{subsecao_ma}'
                print(txt)

                txt_html = f'<p>{secao_em}</p><p>{secao_mvn}</p><p>{subsecao_mm}</p><p>{subsecao_ma}</p>'

                results.append({
                    'filename': xml_file.name,
                    'success': True,
                    'xml_content': txt_html
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