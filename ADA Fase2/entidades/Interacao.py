from datetime import datetime

class Interacao:
    TIPOS_INTERACAO_VALIDOS = {'view_start', 'like', 'share', 'comment'}

    def __init__(self, conteudo_associado, id_usuario, timestamp_interacao, 
                 plataforma_interacao, tipo_interacao, 
                 watch_duration_seconds=0, comment_text="", interacao_id=None):
        self.__interacao_id = interacao_id
        self.__conteudo_associado = conteudo_associado
        self.__id_usuario = int(id_usuario)
        self.__timestamp_interacao = self._converter_timestamp(timestamp_interacao)
        self.__plataforma_interacao = plataforma_interacao
        self.tipo_interacao = tipo_interacao  # validador via property
        self.watch_duration_seconds = watch_duration_seconds  # idem
        self.comment_text = comment_text.strip()

    def _converter_timestamp(self, ts):
        if isinstance(ts, datetime):
            return ts
        return datetime.fromisoformat(ts)

    @property
    def tipo_interacao(self):
        return self.__tipo_interacao

    @tipo_interacao.setter
    def tipo_interacao(self, valor):
        if valor not in self.TIPOS_INTERACAO_VALIDOS:
            raise ValueError(f"Tipo de interação inválido: {valor}")
        self.__tipo_interacao = valor

    @property
    def watch_duration_seconds(self):
        return self.__watch_duration_seconds

    @watch_duration_seconds.setter
    def watch_duration_seconds(self, valor):
        self.__watch_duration_seconds = max(0, int(valor))

    @property
    def comment_text(self):
        return self.__comment_text

    @comment_text.setter
    def comment_text(self, texto):
        self.__comment_text = texto.strip() if texto else ""

    def __str__(self):
        return f"Interacao({self.__tipo_interacao} por usuário: {self.__id_usuario})"

    def __repr__(self):
        return f"<Interacao tipo={self.__tipo_interacao} usuario={self.__id_usuario}>"
