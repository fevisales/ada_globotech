import csv
from collections import defaultdict

# NOME DO ARQUIVO CSV ESPERADO NO MESMO DIRETÓRIO DO SCRIPT
NOME_ARQUIVO_CSV = "interacoes_globo.csv"

def carregar_dados_de_arquivo_csv(nome_arquivo):
    """
    Carrega os dados de um arquivo CSV para uma lista de listas.
    A primeira lista retornada é o cabeçalho, e as subsequentes são as linhas de dados.
    Retorna None se o arquivo não for encontrado ou ocorrer um erro.
    """
    dados_com_cabecalho = []
    try:
        with open(nome_arquivo, mode='r', encoding='utf-8', newline='') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            # Adiciona todas as linhas (incluindo o cabeçalho) à lista
            for linha in leitor_csv:
                dados_com_cabecalho.append(linha)
        
        if not dados_com_cabecalho:
            print(f"Aviso: O arquivo CSV '{nome_arquivo}' está vazio.")
            return None
        return dados_com_cabecalho
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado. Certifique-se de que ele está na mesma pasta do script.")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV '{nome_arquivo}': {e}")
        return None

def converter_lista_para_lista_de_dicionarios(dados_em_lista_com_cabecalho):
    """
    Converte uma lista de listas (onde a primeira lista é o cabeçalho)
    para uma lista de dicionários.
    """
	cabecalho = dados_em_lista_com_cabecalho[0]
	linhas = dados_em_lista_com_cabecalho[1:]
	lista_de_dicionarios = []

	for linha in linhas:
		if len(linha) != len(cabecalho):
            continue  # ignora linhas mal formatadas
		dicionario = dict(zip(cabecalho, linha))
		lista_de_dicionarios.append(dicionario)
                
    return lista_de_dicionarios

def tratar_campos_inteiros(interacao_bruta, interacao_limpa):
    
    """
    Trata os campos que devem ser inteiros simples (id_conteudo e id_usuario), convertendo-os e tratando erros.
    Retorna a interacao limpa com os campos convertidos.
    """
    try:
        interacao_limpa['id_conteudo'] = int(interacao_bruta.get('id_conteudo', 0))
    except (ValueError, TypeError):
        interacao_limpa['id_conteudo'] = -1

    try:
        interacao_limpa['id_usuario'] = int(interacao_bruta.get('id_usuario', 0))
    except (ValueError, TypeError):
        interacao_limpa['id_usuario'] = -1

    return interacao_limpa

def tratar_watch_duration_seconds(interacao_bruta, interacao_limpa):

    """
    Trata o campo watch_duration_seconds, convertendo-o e tratando erros.
    Se o campo estiver vazio ou ausente, deve ser definido como 0.
    Retorna a interacao limpa com o campo watch_duration_seconds convertido.
    """
    tipo = interacao_bruta.get('tipo_interacao', '').strip().lower()
    bruto_valor = interacao_bruta.get('watch_duration_seconds', '').strip()

    if tipo == 'view_start':
        try:
            interacao_limpa['watch_duration_seconds'] = int(bruto_valor) if bruto_valor else 0
        except (ValueError, TypeError):
            interacao_limpa['watch_duration_seconds'] = 0
    else:
        interacao_limpa['watch_duration_seconds'] = 0  # padrão seguro e padronizado

    return interacao_limpa

def tratar_campos_texto(interacao_bruta, interacao_limpa):
    """
    Trata os campos de texto, removendo espaços extras e convertendo para string.
    Retorna a interacao limpa com os campos convertidos.
    """
	interacao_limpa['nome_conteudo'] = interacao_bruta.get('nome_conteudo', '').strip()
    interacao_limpa['timestamp_interacao'] = interacao_bruta.get('timestamp_interacao', '').strip()
    interacao_limpa['plataforma'] = interacao_bruta.get('plataforma', '').strip()
    interacao_limpa['tipo_interacao'] = interacao_bruta.get('tipo_interacao', '').strip().lower()
    interacao_limpa['comment_text'] = interacao_bruta.get('comment_text', '').strip()
    
    return interacao_limpa

def limpar_e_transformar_dados(lista_interacoes_brutas_dict):
    """
    Limpa e transforma os dados brutos das interações (lista de dicionários).
    Converte tipos de dados, trata valores ausentes e remove espaços.
    essa função deve usar as 3 funcoes acima
    Retorna a lista de interações limpas (também como lista de dicionários).
    """

    interacoes_limpas = []
    for interacao_bruta in lista_interacoes_brutas_dict:
        interacao_limpa = {}
        interacao_limpa = tratar_campos_inteiros(interacao_bruta, interacao_limpa)
        interacao_limpa = tratar_watch_duration_seconds(interacao_bruta, interacao_limpa)
        interacao_limpa = tratar_campos_texto(interacao_bruta, interacao_limpa)
        interacoes_limpas.append(interacao_limpa)

    return interacoes_limpas

def criar_mapa_conteudos(interacoes_limpas):
    """
    Cria um dicionário que mapeia id_conteudo para nome_conteudo.
    Ren: Chamar depois no main com mapa_conteudos = criar_mapa_conteudos(interacoes_limpas)
    """
    mapa = {}
    for interacao in interacoes_limpas:
        id_conteudo = interacao['id_conteudo']
        nome = interacao['nome_conteudo']
        if id_conteudo not in mapa:
            mapa[id_conteudo] = nome
            
    return mapa

def calcular_metricas_por_conteudo(interacoes_limpas, mapa_conteudos):
    """
    Calcula várias métricas de engajamento agrupadas por conteúdo.
    Aqui você deve varrer as interações limpas e calcular as métricas desejadas.
    Recomenda-se utilizar um loop e verificar se o conteudo ja foi incluido pelo nome ou id_conteudo
    Retorna um dicionário com as métricas calculadas.
    """
    metricas_conteudo = defaultdict(lambda: {
        'nome_conteudo': '',
        'total_interacoes_engajamento': 0, # like, share, comment, vote_bbb
        'contagem_por_tipo_interacao': defaultdict(int),
        'tempo_total_visualizacao': 0,
        'soma_watch_duration_para_media': 0,
        'contagem_watch_duration_para_media': 0,
        'media_tempo_visualizacao': 0.0,
        'comentarios': []
    })

    tipos_engajamento = {'like', 'share', 'comment', 'vote_bbb'}

    for interacao in interacoes_limpas:
        id_c = interacao['id_conteudo']
        metricas_c = metricas_conteudo[id_c]

        if not metricas_c['nome_conteudo']: # Preenche o nome do conteúdo uma vez
            metricas_c['nome_conteudo'] = mapa_conteudos.get(id_c, "Desconhecido")

        # Métrica 1: Total de interações de engajamento
        if interacao['tipo_interacao'] in tipos_engajamento:
            metricas_c['total_interacoes_engajamento'] += 1

        # Métrica 2: Contagem de cada tipo_interacao
        metricas_c['contagem_por_tipo_interacao'][interacao['tipo_interacao']] += 1

        # Métrica 3: Tempo total de watch_duration_seconds
        metricas_c['tempo_total_visualizacao'] += interacao['watch_duration_seconds']
        
        # Métrica 4: Média de watch_duration_seconds (considerar apenas watch_duration_seconds > 0)
        if interacao['watch_duration_seconds'] > 0:
            metricas_c['soma_watch_duration_para_media'] += interacao['watch_duration_seconds']
            metricas_c['contagem_watch_duration_para_media'] += 1

        # Métrica 5: Listar todos os comentários
        if interacao['tipo_interacao'] == 'comment' and interacao['comment_text']:
            metricas_c['comentarios'].append(interacao['comment_text'])

    # Calcular média de visualização final
    for id_c in metricas_conteudo:
        metricas_c = metricas_conteudo[id_c]
        if metricas_c['contagem_watch_duration_para_media'] > 0:
            metricas_c['media_tempo_visualizacao'] = round(
                metricas_c['soma_watch_duration_para_media'] / metricas_c['contagem_watch_duration_para_media'], 2
            )
        # Remover campos auxiliares
        if 'soma_watch_duration_para_media' in metricas_c:
            del metricas_c['soma_watch_duration_para_media']
        if 'contagem_watch_duration_para_media' in metricas_c:
            del metricas_c['contagem_watch_duration_para_media']
            
    return dict(metricas_conteudo) # Converter de volta para dict normal para exibição


def main():
    """
    Função principal para orquestrar a análise.
    """
    print("Iniciando Fase 1: Coleta e Estruturação Inicial de Dados de Engajamento Globo\n")

    # 1. Carregar dados do arquivo CSV para uma lista de listas
    dados_brutos_lista_de_listas = carregar_dados_de_arquivo_csv(NOME_ARQUIVO_CSV)
    
    if dados_brutos_lista_de_listas is None:
        print(f"Não foi possível carregar os dados do arquivo '{NOME_ARQUIVO_CSV}'. Encerrando.")
        return
    
    if len(dados_brutos_lista_de_listas) < 2: # Precisa de cabeçalho + pelo menos uma linha de dados
        print(f"O arquivo '{NOME_ARQUIVO_CSV}' não contém dados suficientes (cabeçalho e linhas de dados). Encerrando.")
        return

    print(f"Total de {len(dados_brutos_lista_de_listas) - 1} linhas de dados (mais cabeçalho) carregadas do CSV.\n")

    # ETAPA PARA OS ALUNOS: Converter a lista de listas para uma lista de dicionários
    # Esta etapa é crucial para que as funções subsequentes funcionem como esperado.
    interacoes_brutas_dict = converter_lista_para_lista_de_dicionarios(dados_brutos_lista_de_listas)
    
    
    # 2. Limpar e transformar dados (agora a partir da lista de dicionários)
    
    
    
    # 3. Criar mapa de conteúdos (id_conteudo -> nome_conteudo)
 

    # 4. Calcular métricas por conteúdo


   
    # 5. Exibir resultados


if __name__ == "__main__":
    main()
