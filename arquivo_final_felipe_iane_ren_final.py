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
        # a primeira sublista dos dados contém o cabeçalho (nomes das colunas/variáveis que serão as chaves dos novos dicionários)
    valores = dados_em_lista_com_cabecalho[1:]
        # separa as linhas que contêm os valores
    lista_de_dicionarios = []
        # a linha que será preenchida com os dicionários dentro do for

    for linha in valores:
        if len(linha) == len(cabecalho):
            # só cria o dicionário se todos os campos existem (mesmo que alguns estejam vazios de acordo com o significado dos dados), ignorando as linhas mal formatadas
            dicionario_novo = dict(zip(cabecalho, linha))
                # cria pares com cada elemento do cabeçalho e o elemento correspondente na linha de valores, e transforma esses pares em um dicionário chave:valor
            lista_de_dicionarios.append(dicionario_novo)
                # junta o dicionário criado à nova lista de dicionários
            
    return lista_de_dicionarios # retorna a lista contendo todos os dicionários

def tratar_campos_inteiros(interacao_bruta, interacao_limpa):
    # os argumentos devem ser um dicionário com os dados brutos e um dicionário vazio

    """
    Trata os campos que devem ser inteiros simples (id_conteudo e id_usuario), convertendo-os e tratando erros.
    Retorna a interacao limpa com os campos convertidos.
    """
    try:
        interacao_limpa['id_conteudo'] = int(interacao_bruta.get('id_conteudo', 0))
            # no dicionário novo é criada a chave 'id_conteudo' e nela é colocado o valor original id_conteudo transformado pra int,
            # e caso essa chave não exista no original, é trazido o número 0

    except (ValueError, TypeError): 
        # se o valor encontrado dentro da chave 'id_conteudo' não puder ser convertido pra int por algum motivo
        interacao_limpa['id_conteudo'] = -1 # o valor salvo na nova chave id_conteudo é -1, indicando que é um valor inválido

    try:
        interacao_limpa['id_usuario'] = int(interacao_bruta.get('id_usuario', 0))
            # tentar criar no dicionário novo a chave 'watch_duration_seconds',
            # nela é colocado o valor original id_usuario transformado pra int,
            # e caso essa chave não exista no original, é trazido o número 0
    except (ValueError, TypeError):
        # se o valor encontrado dentro da chave 'id_conteudo' não puder ser convertido pra int por algum motivo (por haver caractere não numérico ou conter um None)
        interacao_limpa['id_usuario'] = -1 # o valor salvo na nova chave id_conteudo é -1, indicando que é um valor inválido

    return interacao_limpa
        # retorna um dicionário contendo dois pares chave:valor, o de id_conteudo e o de id_usuario, com seus valores tratados
        # exemplo: interacao_limpa = {'id_conteudo': 4, 'id_usuario': 106}

def tratar_watch_duration_seconds(interacao_bruta, interacao_limpa):
    # os argumentos devem ser um dicionário com os dados brutos e um dicionário que vai ser preenchido com os dados tratados

    """
    Trata o campo watch_duration_seconds, convertendo-o e tratando erros.
    Se o campo estiver vazio ou ausente, deve ser definido como 0.
    Retorna a interacao limpa com o campo watch_duration_seconds convertido.
    """
    tipo = interacao_bruta.get('tipo_interacao', '').strip().lower()
        # salva na variável tipo o tipo da interação daquela linha de dados, com os tratamentos de string necessário pra fazer a comparação no if abaixo,
        # e se não houver essa chave no dicionário, devolve uma string vazia
    valor_duracao_bruto = interacao_bruta.get('watch_duration_seconds', '').strip()
        # salva na variável valor_duracao_bruto o valor da chave 'watch_duration_seconds' tirando os espaços das pontas (não precisa do lower por ser um valor numérico),
        # e se não houver essa chave no dicionário, devolve uma string vazia

    if tipo == 'view_start': # se o tipo da interação for de visualização do conteúdo, que é relacionada a um tempo de duração
        try:
            interacao_limpa['watch_duration_seconds'] = int(valor_duracao_bruto) if valor_duracao_bruto else 0
                # tentar criar no dicionário novo a chave 'watch_duration_seconds',
                # nela é colocado o valor contido na variável valor_duracao_bruto transformado em int (pois veio como string),
                # e caso essa string esteja vazia, guarda nessa chave o valor 0
        except (ValueError, TypeError): # se o valor da variável valor_duracao_bruto não puder ser convertido pra int por algum motivo (por haver caractere não numérico ou conter um None)
            interacao_limpa['watch_duration_seconds'] = 0 # cria a chave e guarda o valor 0 nela
    else:
        # se o tipo de interação não foi 'view_start', ou seja, de visualização de um conteúdo de vídeo
        interacao_limpa['watch_duration_seconds'] = 0  # a chave é criada e é guardado nela o valor padrão 0, pois não houve duração da visualização

    return interacao_limpa
        # retorna um dicionário  com o par chave:valor de watch_duration_seconds tratado e adicionado
        # exemplo de saída: interacao_limpa = {'id_conteudo': 4, 'id_usuario': 106, 'watch_duration_seconds': 7200}

def tratar_campos_texto(interacao_bruta, interacao_limpa):
    # os argumentos devem ser um dicionário com os dados brutos e um dicionário que vai ser preenchido com os dados tratados
    # nas outras funções foram tratadas as variáveis numéricas, nessa são as variáveis que contêm strings, palavras, e outros tipos de caracteres que não números

    """
    Trata os campos de texto, removendo espaços extras e convertendo para string.
    Retorna a interacao limpa com os campos convertidos.
    """
    # cria as chaves no dicionário que entrou como segundo argumento e guarda nelas os valores retirados do dicionário original,
    # com tratamento de tirar os espaços das pontas,
    # e se não houver aquela chave no dicionário original ou o valor não puder ser resgatado, é colocada uma string vazia como padrão
    interacao_limpa['nome_conteudo'] = interacao_bruta.get('nome_conteudo', '').strip()
    interacao_limpa['timestamp_interacao'] = interacao_bruta.get('timestamp_interacao', '').strip()
    interacao_limpa['plataforma'] = interacao_bruta.get('plataforma', '').strip()
    interacao_limpa['tipo_interacao'] = interacao_bruta.get('tipo_interacao', '').strip().lower()
        # só nessa chave foi aplicado o lower, pois para todos os seus valores possíveis não existe nenhuma letra maiúscula, então é feita a padronização sem prejuízo de conteúdo
    interacao_limpa['comment_text'] = interacao_bruta.get('comment_text', '').strip()
    
    return interacao_limpa
        # retorna um dicionário com todos os pares chave:valor de variáveis de texto tratados e adicionados
        # exemplo de saída:
        # interacao_limpa = {'id_conteudo': 4, 'id_usuario': 106, 'watch_duration_seconds': 7200, 'nome_conteudo': 'Jogo do Brasileirão Série A', 'timestamp_interacao': '2024-10-21 16:00:00', 'plataforma': 'Premiere', 'tipo_interacao': 'view_start', 'comment_text': ''}

def limpar_e_transformar_dados(lista_interacoes_brutas_dict):
    """
    Limpa e transforma os dados brutos das interações (lista de dicionários).
    Converte tipos de dados, trata valores ausentes e remove espaços.
    essa função deve usar as 3 funcoes acima
    Retorna a lista de interações limpas (também como lista de dicionários).
    """

    interacoes_limpas = []
    for interacao_bruta in lista_interacoes_brutas_dict:
        # percorre cada dicionário da lista que contém a base de dados inteira
        interacao_limpa = {}
            # cria um dicionário que começa vazio e vai ser usado por todas as funcões de tratamento,
            # sendo preenchido por partes com as chaves e valores tratados de cada linha da base de dados
        interacao_limpa = tratar_campos_inteiros(interacao_bruta, interacao_limpa)
            # sai um dicionário contendo só as chaves 'id_conteudo' e 'id_usuario' e seus valores tratados
        interacao_limpa = tratar_watch_duration_seconds(interacao_bruta, interacao_limpa)
            # reutiliza o dicionário anterior, adicionando a chave 'watch_duration_seconds' e seu valor tratado 
        interacao_limpa = tratar_campos_texto(interacao_bruta, interacao_limpa)
            # reutiliza o dicionário anterior, adicionando as chaves das variáveis de texto e seus valores tratados
        interacoes_limpas.append(interacao_limpa)
            # adiciona à lista final (que é iniciada vazia) o dicionário que acabou de ser tratado
        # repete o processo para todas as linhas de dados da base (lista de dicionários)

    return interacoes_limpas
        # retorna uma lista de dicionários com os dados limpos, tratados e padronizados

def criar_mapa_conteudos(interacoes_limpas):
    # o argumento é a base de dados (lista de dicionários) já tratada

    """
    Cria um dicionário que mapeia id_conteudo para nome_conteudo.
    """
    mapa = {}

    for interacao in interacoes_limpas:
        # percorre todas as linhas de dados em busca de um id_conteudo e um nome_conteudo que ainda não foi mapeado
        id_cont = interacao['id_conteudo'] # guarda o id do conteúdo daquela linha em uma variável id_conteudo
        nome_cont = interacao['nome_conteudo'] # guarda o nome do conteúdo daquela linha em uma variável nome
        if id_cont not in mapa:
            # checa se o id do conteúdo da linha analisada nesse momento ainda não existe no dicionário que está sendo construído pela função
            mapa[id_cont] = nome_cont
                # se aquele id ainda não existir no dicionário mapa, ele é adicionado como chave,
                # e seu valor correspondente vai ser o nome do conteúdo daquela mesma linha de dados
            
    return mapa
        # retorna um dicionário com os pares chave: valor sendo o id_conteudo: nome_conteudo
        # saída = {1: 'Jornal Nacional', 2: 'Novela Renascer', 3: 'Podcast Papo de Segunda', 4: 'Jogo do Brasileirão Série A', 5: 'Mais Você', 6: 'The Voice Brasil', 7: 'Podcast GE Tabelando', 8: 'Sessão da Tarde Clássicos', 9: 'Show da Virada', 10: 'Documentário Amazônia Viva', 11: 'Receitas da Ana Maria', 12: 'Futebol de Sabado', 13: 'Desenrola Brasil Podcast', 14: 'Globo Repórter Especial', 15: 'Domingão com Huck'}

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

    # 1: Carrega os dados do CSV em formato de lista de listas
    dados_brutos_lista_de_listas = carregar_dados_de_arquivo_csv(NOME_ARQUIVO_CSV)
    
    if dados_brutos_lista_de_listas is None:
        print(f"Não foi possível carregar os dados do arquivo '{NOME_ARQUIVO_CSV}'. Encerrando.")
        return
    
    if len(dados_brutos_lista_de_listas) < 2:# Precisa de cabeçalho + pelo menos uma linha de dados
        print(f"O arquivo '{NOME_ARQUIVO_CSV}' não contém dados suficientes. Encerrando.")
        return

    print(f"Total de {len(dados_brutos_lista_de_listas) - 1} interações carregadas do CSV.\n")

    # 2: Converte para dicionário e aplica limpeza nos dados
    interacoes_brutas_dict = converter_lista_para_lista_de_dicionarios(dados_brutos_lista_de_listas)
        # aplica a função que transforma a lista lida em uma lista de dicionários relacionando o cabeçalho com os dados
    interacoes_limpas = limpar_e_transformar_dados(interacoes_brutas_dict)
        # faz todos os tratamentos de dados na lista de dicionários
    print("Etapa 2 concluída: dados limpos e estruturados.\n")

    # 3: Cria um dicionário que mapeia id_conteudo para nome_conteudo
    mapa_conteudos = criar_mapa_conteudos(interacoes_limpas)
        # cria o mapa de conteúdos
    print("Etapa 3 concluída: mapa de conteúdos criado.\n")

    # 4: Calcula métricas de engajamento agrupadas por conteúdo
    metricas = calcular_metricas_por_conteudo(interacoes_limpas, mapa_conteudos)
        # cria um dicionário contendo as métricas para cada um dos conteúdos que receberam interações
    print("Etapa 4 concluída: métricas de engajamento calculadas.\n")

    # 5: Exibe os dados calculados em formato de relatório
    print("===== RESULTADOS FINAIS POR CONTEÚDO =====\n")

    for id_conteudo, dados in metricas.items():
        # percorrendo cada conteúdo e suas respectivas métricas dentro do dicionários de métricas,
        # o id_conteudo é a chave no dicionário chamado metricas, dados é o dicionário correspondente contendo suas métricas
        print(f"Conteúdo: {dados['nome_conteudo']} (ID: {id_conteudo})")
            # printa o nome do conteúdo e seu ID
        print(f"- Total de interações de engajamento: {dados['total_interacoes_engajamento']}")
            # localiza e printa o valor contido na chave 'total_interacoes_engajamento' para aquele conteúdo
        print(f"- Tempo total de visualização: {dados['tempo_total_visualizacao']} segundos")
            # localiza o valor contido na chave 'tempo_total_visualizacao' para aquele conteúdo
        print(f"- Média de tempo de visualização: {dados['media_tempo_visualizacao']} segundos")
            # localiza o valor contido na chave 'media_tempo_visualizacao' para aquele conteúdo
        print("- Tipos de interação:")
        for tipo, quantidade in dados['contagem_por_tipo_interacao'].items():
            # dados['contagem_por_tipo_interacao'] é um dicionário contendo como chaves cada tipo de interação (view_start, like, share, comment)
            # feito para aquele conteúdo, e o valor de cada chave é a quantidade daquela interação feita para aquele conteúdo
            print(f"    • {tipo}: {quantidade}")
                # printa cada tipo de interação e sua respectiva quantidade
        if dados['comentarios']:
            # checa se existe algum valor dentro da chave de comentários, ou seja se algum comentário foi feito para aquele conteúdo
            print("- Comentários (até 3 exemplos):")
            for comentario in dados['comentarios'][:3]:
                # esses comentários estão em uma lista, os prints serão feitos dos 3 primeiros elementos dessa lista
                print(f"    • \"{comentario}\"")
        print("-" * 50)
        # os prints das métricas serão repetidos para cada um dos conteúdos presentes na base de dados

    print("\nAnálise concluída com sucesso.")

if __name__ == "__main__":
    main()