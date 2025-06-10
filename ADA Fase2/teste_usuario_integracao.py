dados_csv_mock = [
    {
        "id_conteudo": 1,
        "nome_conteudo": "Jornal Nacional",
        "id_usuario": 101,
        "timestamp_interacao": "2024-10-20 20:05:12",
        "plataforma": "TV Globo",
        "tipo_interacao": "view_start",
        "watch_duration_seconds": 1800,
        "comment_text": ""
    },
    {
        "id_conteudo": 2,
        "nome_conteudo": "Novela Renascer",
        "id_usuario": 102,
        "timestamp_interacao": "2024-10-20 21:15:30",
        "plataforma": "Globoplay",
        "tipo_interacao": "like",
        "watch_duration_seconds": 2700,
        "comment_text": ""
    },
    {
        "id_conteudo": 1,
        "nome_conteudo": "Jornal Nacional",
        "id_usuario": 101,
        "timestamp_interacao": "2024-10-20 20:45:00",
        "plataforma": "TV Globo",
        "tipo_interacao": "comment",
        "watch_duration_seconds": 300,
        "comment_text": "Excelente edição!"
    }
]

from entidades.Interacao import Interacao
from entidades.Usuario import Usuario


class PlataformaMock:
    def __init__(self, nome):
        self.__nome_plataforma = nome

    def __str__(self):
        return self.__nome_plataforma

    def __repr__(self):
        return f"<Plataforma('{self.__nome_plataforma}')>"

# Conteúdo simulado
class ConteudoMock:
    def __init__(self, id_conteudo, nome):
        self._id_conteudo = id_conteudo
        self._nome_conteudo = nome

    def __str__(self):
        return self._nome_conteudo

    def __repr__(self):
        return f"<Conteudo id={self._id_conteudo} nome={self._nome_conteudo}>"



# Dicionários para evitar objetos duplicados
usuarios = {}
conteudos = {}
plataformas = {}

# Lista de interações criadas
interacoes = []

for dado in dados_csv_mock:
    id_usuario = dado["id_usuario"]
    id_conteudo = dado["id_conteudo"]
    nome_conteudo = dado["nome_conteudo"]
    nome_plataforma = dado["plataforma"]

    # Criar/reutilizar objetos de apoio
    if id_usuario not in usuarios:
        usuarios[id_usuario] = Usuario(id_usuario)
    if id_conteudo not in conteudos:
        conteudos[id_conteudo] = ConteudoMock(id_conteudo, nome_conteudo)
    if nome_plataforma not in plataformas:
        plataformas[nome_plataforma] = PlataformaMock(nome_plataforma)

    # Criar interação
    interacao = Interacao(
        conteudo_associado=conteudos[id_conteudo],
        id_usuario=id_usuario,
        timestamp_interacao=dado["timestamp_interacao"],
        plataforma_interacao=plataformas[nome_plataforma],
        tipo_interacao=dado["tipo_interacao"],
        watch_duration_seconds=dado["watch_duration_seconds"],
        comment_text=dado["comment_text"]
    )

    # Registrar nos objetos
    usuarios[id_usuario].registrar_interacao(interacao)
    interacoes.append(interacao)

    # Mostra todas as interações criadas
print("▶️ INTERAÇÕES")
for i in interacoes:
    print(i)

# Métodos de teste para cada usuário
print("\n👤 TESTANDO USUÁRIOS")
for user in usuarios.values():
    print(f"\nUsuário: {user}")
    print("Interações realizadas:")
    for i in user.interacoes_realizadas:
        print("-", i)

    print("Interações do tipo 'comment':")
    for i in user.obter_interacoes_por_tipo("comment"):
        print("-", i)

    print("Conteúdos únicos consumidos:")
    for c in user.obter_conteudos_unicos_consumidos():
        print("-", c)

    print("Tempo total consumido na TV Globo:", user.calcular_tempo_total_consumo_plataforma(plataformas["TV Globo"]))

    print("Plataformas mais frequentes:")
    for p in user.plataformas_mais_frequentes():
        print("-", p)

