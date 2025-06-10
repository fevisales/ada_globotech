from entidades.Conteudo import Video, Podcast, Artigo
from entidades.Interacao import Interacao
from entidades.Usuario import Usuario

class PlataformaMock:
    def __init__(self, nome):
        self.__nome_plataforma = nome
    def __str__(self):
        return self.__nome_plataforma

tv_globo = PlataformaMock("TV Globo")

# Criar conteúdo do tipo Video
video = Video(1, "Jornal Nacional", duracao_total_video_seg=3600)
usuario = Usuario(101)

# Criar e registrar interações
inter1 = Interacao(video, 101, "2024-10-20T20:00:00", tv_globo, "view_start", 1800)
inter2 = Interacao(video, 101, "2024-10-20T20:30:00", tv_globo, "comment", 600, "Muito bom!")

video.adicionar_interacao(inter1)
video.adicionar_interacao(inter2)
usuario.registrar_interacao(inter1)
usuario.registrar_interacao(inter2)

# Testes
print(f"\n🎥 Video: {video}")
print("Total de interações de engajamento:", video.calcular_total_interacoes_engajamento())
print("Contagem por tipo:", video.calcular_contagem_por_tipo_interacao())
print("Tempo total consumo:", video.calcular_tempo_total_consumo())
print("Média tempo consumo:", video.calcular_media_tempo_consumo())
print("Percentual médio assistido:", video.calcular_percentual_medio_assistido())
print("Comentários:", video.listar_comentarios())

# Criando um podcast
podcast = Podcast(2, "Podcast Política", duracao_total_episodio_seg=1800)
inter3 = Interacao(podcast, 102, "2024-10-21T08:00:00", tv_globo, "view_start", 900)
podcast.adicionar_interacao(inter3)

print(f"\n🎧 Podcast: {podcast}")
print("Tempo total consumo:", podcast.calcular_tempo_total_consumo())

# Criando um artigo
artigo = Artigo(3, "Especial Eleições", tempo_leitura_estimado_seg=600)
inter4 = Interacao(artigo, 103, "2024-10-21T09:00:00", tv_globo, "view_start", 300)
artigo.adicionar_interacao(inter4)

print(f"\n📰 Artigo: {artigo}")
print("Tempo total consumo:", artigo.calcular_tempo_total_consumo())
