from collections import Counter

class Usuario:
    def __init__(self, id_usuario):
        self.__id_usuario = int(id_usuario)
        self.__interacoes_realizadas = []

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def interacoes_realizadas(self):
        return list(self.__interacoes_realizadas)

    def registrar_interacao(self, interacao):
        self.__interacoes_realizadas.append(interacao)

    def obter_interacoes_por_tipo(self, tipo_desejado):
        return [i for i in self.__interacoes_realizadas if i.tipo_interacao == tipo_desejado]

    def obter_conteudos_unicos_consumidos(self):
        return set(i._Interacao__conteudo_associado for i in self.__interacoes_realizadas)

    def calcular_tempo_total_consumo_plataforma(self, plataforma):
        return sum(i.watch_duration_seconds for i in self.__interacoes_realizadas
                   if i._Interacao__plataforma_interacao == plataforma)

    def plataformas_mais_frequentes(self, top_n=3):
        contagem = Counter(i._Interacao__plataforma_interacao for i in self.__interacoes_realizadas)
        return [plataforma for plataforma, _ in contagem.most_common(top_n)]

    def __str__(self):
        return f"Usuário {self.__id_usuario}"

    def __repr__(self):
        return f"<Usuario id={self.__id_usuario}>"
