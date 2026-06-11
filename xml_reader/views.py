# xml_reader/views.py
import xmltodict
from utils.nfelog import ide, infnfe, emit, dest, transp, det, entrega
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from utils.ler_dens_conc import ler_dens_conc
import io
import zipfile
from datetime import datetime


def upload_multiple_xml(request):
    meses = ["", "JAN", "FEV", "MAR", "ABR", "MAI", "JUN", 
             "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    
    if request.method == 'POST':        
        # --- Captura os campos CNPJ, operação e armazenagem ---
        cnpj = request.POST.get('cnpj_empresa')
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        armazenagem_form = request.POST.get('armazenagem')

        nome_mes = meses[int(mes)]
        
        # Lista com os nomes de todas as operações possíveis
        tipos_de_operacao = [
            'comercializacao_nacional', 'comercializacao_internacional', 'producao',
            'transformacao', 'consumo', 'fabricacao', 'transporte', 'armazenamento'
        ]

        # Armazenando o status de cada operação numa lista
        list_status = ''
        for op in tipos_de_operacao:
            valor = request.POST.get(op)
            if valor:  # Verifica se o valor existe
                list_status = list_status + valor

        # request.FILES.getlist() é a chave para obter múltiplos arquivos
        xml_files = request.FILES.getlist('xml_files[]')

        if not xml_files:
            return JsonResponse({'error': 'Nenhum arquivo XML enviado.'}, status=400)

        results = []
        
        # Variável para armazenar TODO o conteúdo do arquivo TXT
        conteudo_txt_completo = ""
        
        for indice, xml_file in enumerate(xml_files, start=1):
            # Verifica a extensão de cada arquivo
            if not xml_file.name.endswith('.xml'):
                results.append({
                    'filename': xml_file.name,
                    'error': 'O arquivo não é um XML válido.'
                })
                continue  # Pula para o próximo arquivo

            try:
                # Lê o conteúdo do arquivo
                file_content = xml_file.read().decode('utf-8')

                # Use xmltodict to parse and convert the XML document
                dict_created = xmltodict.parse(file_content)
                
                # Aqui se verifica qual é o tipo de NFe. Se ela inicia com nfeProc ou NFeLog
                # As NFs que a SOLID recebe são do tipo NFeLog versão 1.00 com ID versão 4.00
                if list(dict_created)[0] == 'nfeProc':
                    infnfe_dict = dict_created['nfeProc']['NFe']['infNFe']  
                else:
                    infnfe_dict = dict_created['NFeLog']['procNFe']['NFe']['infNFe']  

                # Lê a primeira NF inserida para extrair as informações para a seção EM (apenas no primeiro arquivo)
                # Seção EM
                secao_em = ''
                if indice == 1:
                    secao_em = f'EM{cnpj}{mes}{ano}{list_status}'
                    conteudo_txt_completo += secao_em
                
                # Seção MVN
                # Diferente da abordagem utilizada anteriormente, aqui se verifica se o CNPJ digitado na tela modal
                # é do emitente ou do destinatário. Com esta informação, se define se a NF é de entrada ou saída
                emitente = emit.emit(infnfe_dict)
                destinatario = dest.dest(infnfe_dict)

                # Este deverá ser o emitente ou o destinatário. Ele é o responsável pela informação da NF
                # Segue também a inicialização de algumas variáveis do declarante
                declarante = []
                tipo_declarante = ''
                entrada_saida = ''

                # Verifica se o CNPJ digitado é da empresa que será gerado o TXT
                if cnpj not in(emitente['cnpj'],destinatario['cnpj']):
                    raise RuntimeError("CNPJ inválido")
                else:
                    if cnpj == emitente['cnpj']:
                        tipo_declarante = 'emitente'
                        declarante = emitente.copy()
                        entrada_saida = 'S'
                        if armazenagem_form == 'S':
                            armazenagem = 'F'
                        else:
                            armazenagem = 'T'

                    else:
                        tipo_declarante = 'destinatario'
                        declarante = destinatario.copy()
                        entrada_saida = 'E'
                        armazenagem = armazenagem_form
                        
                var_ide = ide.ide(infnfe_dict, tipo_declarante)
                operacao = var_ide['operacao']
                razao_social = declarante['razao_social']
                razao_social = razao_social.ljust(69)
                cnpj_declarante = declarante['cnpj']
                numero_nf = var_ide['numero_nf']
                data_emissao_nf = var_ide['data_emissao_nf']
                armazenagem = armazenagem
                transporte = transp.transp(infnfe_dict)
                secao_mvn = f'\nMVN{entrada_saida}{operacao}{cnpj_declarante}{razao_social}{numero_nf}{data_emissao_nf}{armazenagem}{transporte}'
                conteudo_txt_completo += secao_mvn

                # Subseção MM
                var_det = det.det(infnfe_dict)
                ncm = var_det['codigo_tpn']
                ncm_original = var_det['ncm']
                quantidade = var_det['quantidade']
                unidade_medida = var_det['unidade_medida']
                dens_conc = ler_dens_conc(cnpj, ncm_original)
                densidade = dens_conc['densidade']
                concentracao = dens_conc['concentracao']
                subsecao_mm = f'\nMM{ncm}{concentracao}{densidade}{quantidade}{unidade_medida}'
                conteudo_txt_completo += subsecao_mm

                # Subseção MA (o entendimento aplicado é que esta seção só existirá se na NFe existir a tag ENTREGA)
                if 'entrega' in infnfe_dict:
                    var_entrega = entrega.entrega(infnfe_dict)
                    cnpj_armazenadora = var_entrega['cnpj']
                    razao_social_armazenadora = var_entrega['nome']
                    # if not razao_social_armazenadora:
                    #     razao_social_armazenadora = var_dest['destinatario']
                    razao_social_armazenadora = razao_social_armazenadora.ljust(70)
                    endereco_armazenadora = var_entrega['endereco']
                    endereco_armazenadora = endereco_armazenadora.ljust(70)
                    cep_armazenadora = var_entrega['cep']
                    # if not cep_armazenadora:
                    #     cep_armazenadora = var_dest['cep']
                    cep_armazenadora = cep_armazenadora.ljust(10)
                    numero_armazenadora = var_entrega['numero']
                    numero_armazenadora = numero_armazenadora.ljust(5)
                    complemento_armazenadora = var_entrega['complemento']
                    complemento_armazenadora = complemento_armazenadora.ljust(20)
                    bairro_armazenadora = var_entrega['bairro']
                    bairro_armazenadora = bairro_armazenadora.ljust(30)
                    uf_armazenadora = var_entrega['uf']
                    municipio_armazenadora = var_entrega['municipio']

                    subsecao_ma = f'\nMA{cnpj_armazenadora}{razao_social_armazenadora}{endereco_armazenadora}'
                    subsecao_ma = f'{subsecao_ma}{cep_armazenadora}{numero_armazenadora}{complemento_armazenadora}'
                    subsecao_ma = f'{subsecao_ma}{bairro_armazenadora}{uf_armazenadora}{municipio_armazenadora}'
                else:
                    subsecao_ma = ''

                conteudo_txt_completo += subsecao_ma
                
                # txt = f'{secao_em}{secao_mvn}{subsecao_mm}{subsecao_ma}'
                txt_filename = f'M{ano}{nome_mes}{cnpj}.txt'
                
                txt_html = f'<p>{secao_em}<br/>{subsecao_mm}<br/>{subsecao_ma}'
                # txt_html = f'<br>{secao_em}<br/>{secao_mvn}<br/>{subsecao_mm}<br/>{subsecao_ma}'

                results.append({
                    'filename': txt_filename,
                    'success': True,
                    'xml_content': txt_html
                })

            except RuntimeError as e:
                results.append({
                    'filename': xml_file.name,
                    'error': f'O CNPJ digitado é inválido'
                })

            except Exception as e:
                results.append({
                    'filename': xml_file.name,
                    'error': f'Ocorreu um erro inesperado: {str(e)}'
                })
        
        # Gera um único arquivo TXT com todo o conteúdo
        # nome_arquivo_txt = f"dados_processados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        arquivo_txt_unico = [{
            'filename': results[0]['filename'],
            'content': conteudo_txt_completo
        }]

        # Armazena os dados na sessão para usar na página de resultados
        request.session['txt_contents'] = arquivo_txt_unico  # Agora é uma lista com UM único arquivo
        request.session['dados_recebidos'] = {
            'mes': mes,
            'ano': ano,
            'operacoes_status': list_status
        }
        request.session['results'] = results
        
        # Garante que a sessão seja salva
        request.session.modified = True
        
        # Redireciona para a página de resultados
        return JsonResponse({
            'success': True,
            'redirect_url': '/resultados/',  # URL para onde o JavaScript deve redirecionar
            'dados_recebidos': {
                'mes': mes,
                'ano': ano,
                'operacoes_status': list_status
            },
            'results': results,
            'txt_contents': arquivo_txt_unico
        })

    # Se a requisição for GET, renderiza a página de upload
    return render(request, 'upload.html')


def resultados_page(request):
    """View para exibir a página de resultados com downloads"""
    # Recupera os dados da sessão
    txt_contents = request.session.get('txt_contents', [])
    dados_recebidos = request.session.get('dados_recebidos', {})
    results = request.session.get('results', [])
    
    return render(request, 'resultados.html', {
        'dados_recebidos': dados_recebidos,
        'results': results,
        'txt_contents': txt_contents
    })


def download_txt(request, file_index):
    """
    View para download de um arquivo .txt específico
    """
    txt_contents = request.session.get('txt_contents', [])
    
    try:
        file_index = int(file_index)
        if 0 <= file_index < len(txt_contents):
            file_data = txt_contents[file_index]
            
            # Cria a resposta HTTP com o arquivo .txt
            response = HttpResponse(file_data['content'], content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{file_data["filename"]}"'
            return response
        else:
            return HttpResponse('Arquivo não encontrado', status=404)
    except (ValueError, IndexError):
        return HttpResponse('Arquivo não encontrado', status=404)


def download_all_txt(request):
    """
    View para download de todos os arquivos .txt em um arquivo ZIP
    (Agora com apenas um arquivo, mas mantida para compatibilidade)
    """
    txt_contents = request.session.get('txt_contents', [])
    
    if not txt_contents:
        return HttpResponse('Nenhum arquivo para download', status=404)
    
    # Se tiver apenas um arquivo, oferece download direto
    if len(txt_contents) == 1:
        file_data = txt_contents[0]
        response = HttpResponse(file_data['content'], content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_data["filename"]}"'
        return response
    
    # Se por algum motivo tiver múltiplos arquivos, cria ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for txt_file in txt_contents:
            zip_file.writestr(txt_file['filename'], txt_file['content'])
    
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="arquivos_txt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip"'
    
    return response