from entidades.Plataforma import Plataforma
from entidades.Conteudo import Conteudo
from entidades.Interacao import Interacao

# Criando Plataforma
print("\n🧪 Testando Plataforma")
globoplay = Plataforma("Globoplay")
print(globoplay)                         # Deve imprimir "Globoplay"
print(repr(globoplay))                   # Deve imprimir Plataforma(nome='Globoplay')

# Testando comparação e hash
globo1 = Plataforma("TV Globo")
globo2 = Plataforma("tv globo")          # Mesmo nome (case-insensitive)
print(globo1 == globo2)                  # True
print({globo1, globo2})                  # Deve conter só um elemento

# Criando Conteúdo
print("\n🧪 Testando Conteudo")
conteudo = Conteudo(1, "Matéria Especial")
print(conteudo)

# Criando interações simuladas
inter1 = Interacao(conteudo, 201, "2024-06-01T10:00:00", globoplay, "like", 0)
inter2 = Interacao(conteudo, 202, "2024-06-01T10:05:00", globoplay, "comment", 120, "Muito interessante")
inter3 = Interacao(conteudo, 203, "2024-06-01T10:10:00", globoplay, "view_start", 600)

conteudo.adicionar_interacao(inter1)
conteudo.adicionar_interacao(inter2)
conteudo.adicionar_interacao(inter3)

# Testes dos métodos
print("Total de interações de engajamento:", conteudo.calcular_total_interacoes_engajamento())  # 2
print("Contagem por tipo:", conteudo.calcular_contagem_por_tipo_interacao())                    # {'like': 1, 'comment': 1, 'view_start': 1}
print("Tempo total consumo:", conteudo.calcular_tempo_total_consumo())                          # 720
print("Média tempo consumo:", conteudo.calcular_media_tempo_consumo())                          # 360.0
print("Comentários:", conteudo.listar_comentarios())                                            # ["Muito interessante"]
