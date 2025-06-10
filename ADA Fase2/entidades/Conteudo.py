### CLASSE BASE CONTEÚDO
from entidades import Interacao


class Conteudo:
    def __init__(self, id_conteudo, nome_conteudo):
        self.id_conteudo = id_conteudo # acessa o setter que faz a validação e coloca valor no atributo
        self.nome_conteudo = nome_conteudo # acessa o setter que faz a validação e coloca valor no atributo
        self.__interacoes = []

    @property # getter de id_conteudo
    def id_conteudo(self):
        return self.__id_conteudo
    
    @property # getter de nome_conteudo
    def nome_conteudo(self):
        return self.__nome_conteudo
    
    @id_conteudo.setter
    def id_conteudo(self, id):
        if not isinstance(id, int): # checa se o valor inserido para id_conteudo é do tipo int
            raise TypeError("O id_conteudo deve ser um valor inteiro") # levanta TypeError se não for do tipo desejado
        self.__id_conteudo = id # se não der erro é porque o valor inserido é int, então pode ser inserido no atributo

    @nome_conteudo.setter
    def nome_conteudo(self, nome):
        if not isinstance(nome, str): # checa se o valor inserido para nome_conteudo é do tipo str
            raise TypeError("O nome_conteudo deve ser uma string.") # levanta TypeError se não for do tipo desejado
        self.__nome_conteudo = nome # se não der erro é porque o valor inserido é str, então pode ser inserido no atributo
    
    def adicionar_interacao(self, interacao): # recebe uma interação e adiciona à lista contida no atributo privado interacoes
        #if isinstance(interacao, Interacao): # checa se o objeto interacao pertence à classe Interacao
            self.__interacoes.append(interacao) # se for um objeto Interacao, é adicionado à lista

    def ver_interacoes(self): # visualizador das interações
        return self.__interacoes

    def calcular_total_interacoes_engajamento(self):
        lista_tipos_interacao = []

        for objeto in self.__interacoes: # percorre os objetos Interacao inclusos no atributo interacoes
            lista_tipos_interacao.append(objeto.tipo_interacao) # puxa apenas o tipo_interacao, que é o atributo que contém as palavras "like", "share" e "comment"

        # cria contadores pra quantas vezes cada uma das 3 interações de interesse aparece na lista de tipos de interação
        conta_like = lista_tipos_interacao.count('like')
        conta_share = lista_tipos_interacao.count('share')
        conta_comment = lista_tipos_interacao.count('comment')

        return conta_like, conta_share, conta_comment # retorna os 3 contadores em uma tupla
    
    def calcular_contagem_por_tipo_interacao(self):
        contadores = self.calcular_total_interacoes_engajamento() # puxa os valores devolvidos pela função que conta as interações
        interacoes = ['like', 'share', 'comment'] # lista contendo os nomes das interações de interesse
        dicionario = dict(zip(interacoes, contadores)) # cria um dicionário a partir da junção dos nomes e seus valores correspondentes

        return dicionario
    
    def calcular_tempo_total_consumo(self):
        total = 0

        for objeto in self.__interacoes: # percorre os objetos que compõem a lista de interações
            total += objeto.watch_duration_seconds # soma o valor do atributo watch_duration_seconds

        return total
    
    def calcular_media_tempo_consumo(self):
        lista_watch_duration_positivos = []

        for objeto in self.__interacoes: # percorre os objetos que compõem a lista de interações
            if objeto.watch_duration_seconds > 0:
                lista_watch_duration_positivos.append(objeto.watch_duration_seconds) # adiciona em uma lista à parte apenas os valores de watch_duration_seconds > 0

        media = sum(lista_watch_duration_positivos) / len(lista_watch_duration_positivos) # calcula a média a partir dos valores de watch_duration_seconds

        return media
    
    def listar_comentarios(self):
        lista_comentarios = []

        for objeto in self.__interacoes: # percorre os objetos que compõem a lista de interações
            if objeto.comment_text != '': # checa se há algum comentário naquela interação
                lista_comentarios.append(objeto.comment_text) # adiciona aquele comentário em uma lista pra ser devolvida pelo método 

        return lista_comentarios
    
    def __str__(self):
        return f'Conteúdo: {self.nome_conteudo} | ID: {self.id_conteudo}'
    
    def __repr__(self):
        return f'Conteúdo: nome_conteudo = {self.nome.conteudo} | ID: id_conteudo = {self.id_conteudo}'

### SUBCLASSE VIDEO
class Video (Conteudo):
    def __init__(self, id_conteudo_video, nome_conteudo_video, duracao_total_video_seg):
        super().__init__(id_conteudo_video, nome_conteudo_video)
        self.__duracao_total_video_seg = duracao_total_video_seg # acessa o setter que faz a validação e coloca valor no atributo

    @property
    def duracao_total_video_seg(self):
        return self.__duracao_total_video_seg
    
    @duracao_total_video_seg.setter
    def duracao_total_video_seg(self, valor):
        if not isinstance(valor, int): # checa se o valor inserido para duracao_total_video_seg é do tipo int
            raise TypeError("A duracao_total_video_seg deve ser um valor inteiro") # levanta TypeError se não for do tipo desejado
        self.__duracao_total_video_seg = valor
    
    def calcular_percentual_medio_assistido(self):
        tempo_medio_consumo = self.calcular_media_tempo_consumo() # puxa a média de tempo de consumo pelo método correspondente contido na classe Conteudo

        if self.__duracao_total_video_seg == 0:
            return 0
        
        percentual_medio_assistido = (tempo_medio_consumo / self.__duracao_total_video_seg) * 100 # calcula a % a partir da média e do atributo duracao_total_video_seg

        return percentual_medio_assistido
    
### SUBCLASSE PODCAST
class Podcast (Conteudo):
    def __init__(self, id_conteudo_podcast, nome_conteudo_podcast,duracao_total_episodio_seg):
        super().__init__(id_conteudo_podcast, nome_conteudo_podcast)
        self.duracao_total_episodio_seg = None # atribui o valor None como padrão pra esse atributo, sendo opcional inserir valor a ele

    @property
    def duracao_total_episodio_seg(self):
        return self.__duracao_total_episodio_seg
    
    @duracao_total_episodio_seg.setter
    def duracao_total_episodio_seg(self, valor):
        #if not isinstance(valor, int): # checa se o valor inserido para duracao_total_episodio_seg é do tipo int
            #raise TypeError("A duracao_total_episodio_seg deve ser um valor inteiro.") # levanta TypeError se não for do tipo desejado
        self.__duracao_total_episodio_seg = valor

### SUBCLASSE ARTIGO
class Artigo (Conteudo):
    def __init__(self, id_conteudo_artigo, nome_conteudo_artigo, tempo_leitura_estimado_seg):
        super().__init__(id_conteudo_artigo, nome_conteudo_artigo)
        self.__tempo_leitura_estimado_seg = tempo_leitura_estimado_seg

    @property
    def tempo_leitura_estimado_seg(self):
        return self.__tempo_leitura_estimado_seg
    
    @tempo_leitura_estimado_seg.setter
    def tempo_leitura_estimado_seg(self, valor):
        if not isinstance(valor, int): # checa se o valor inserido para tempo_leitura_estimado_seg é do tipo int
            raise TypeError("O tempo_leitura_estimado_seg deve ser um valor inteiro.") # levanta TypeError se não for do tipo desejado
        self.__tempo_leitura_estimado_seg = valor