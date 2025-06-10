from entidades import Plataforma, Usuario, Interacao, Video, Podcast, Artigo

import csv
from collections import defaultdict, Counter

class SistemaAnaliseEngajamento:
    VERSAO_ANALISE = "2.0"

    def __init__(self):
        self.__plataformas_registradas = {}
        self.__conteudos_registrados = {}
        self.__usuarios_registrados = {}
        self.__proximo_id_plataforma = 1

    def cadastrar_plataforma(self, nome_plataforma: str) -> Plataforma:
        if nome_plataforma not in self.__plataformas_registradas:
            plataforma = Plataforma(id_plataforma=self.__proximo_id_plataforma, nome_plataforma=nome_plataforma)
            self.__plataformas_registradas[nome_plataforma] = plataforma
            self.__proximo_id_plataforma += 1
        return self.__plataformas_registradas[nome_plataforma]

    def obter_plataforma(self, nome_plataforma: str) -> Plataforma:
        return self.__plataformas_registradas.get(nome_plataforma) or self.cadastrar_plataforma(nome_plataforma)

    def listar_plataformas(self) -> list:
        return list(self.__plataformas_registradas.values())

    def _carregar_interacoes_csv(self, caminho_arquivo: str) -> list:
        with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            return list(leitor)

    def processar_interacoes_do_csv(self, caminho_arquivo: str):
        dados = self._carregar_interacoes_csv(caminho_arquivo)
        for linha in dados:
            id_usuario = int(linha['id_usuario'])
            id_conteudo = int(linha['id_conteudo'])
            nome_conteudo = linha['nome_conteudo']
            tipo_conteudo = linha['tipo_conteudo'].lower()

            if id_conteudo not in self.__conteudos_registrados:
                if tipo_conteudo == 'video':
                    conteudo = Video(id_conteudo, nome_conteudo, int(linha.get('duracao_total_video_seg', 0)))
                elif tipo_conteudo == 'podcast':
                    conteudo = Podcast(id_conteudo, nome_conteudo, int(linha.get('duracao_total_episodio_seg', 0)))
                elif tipo_conteudo == 'artigo':
                    conteudo = Artigo(id_conteudo, nome_conteudo, int(linha.get('tempo_leitura_estimado_seg', 0)))
                else:
                    continue
                self.__conteudos_registrados[id_conteudo] = conteudo
            else:
                conteudo = self.__conteudos_registrados[id_conteudo]

            if id_usuario not in self.__usuarios_registrados:
                usuario = Usuario(id_usuario)
                self.__usuarios_registrados[id_usuario] = usuario
            else:
                usuario = self.__usuarios_registrados[id_usuario]

            plataforma = self.obter_plataforma(linha['nome_plataforma'])

            try:
                interacao = Interacao(
                    conteudo_associado=conteudo,
                    id_usuario=id_usuario,
                    timestamp_interacao=linha['timestamp_interacao'],
                    plataforma_interacao=plataforma,
                    tipo_interacao=linha['tipo_interacao'],
                    watch_duration_seconds=linha.get('watch_duration_seconds', 0),
                    comment_text=linha.get('comment_text', '')
                )
                conteudo.adicionar_interacao(interacao)
                usuario.registrar_interacao(interacao)
            except ValueError:
                continue

    def gerar_relatorio_engajamento_conteudos(self, top_n: int = None):
        conteudos = list(self.__conteudos_registrados.values())
        conteudos.sort(key=lambda c: c.calcular_tempo_total_consumo(), reverse=True)
        for conteudo in conteudos[:top_n]:
            print(f"{conteudo}: Tempo Total = {conteudo.calcular_tempo_total_consumo()}s, Média Tempo = {conteudo.calcular_media_tempo_consumo()}s, Comentários = {len(conteudo.listar_comentarios())}")

    def gerar_relatorio_atividade_usuarios(self, top_n: int = None):
        usuarios = list(self.__usuarios_registrados.values())
        usuarios.sort(key=lambda u: sum(i.watch_duration_seconds for i in u._Usuario__interacoes_realizadas), reverse=True)
        for usuario in usuarios[:top_n]:
            print(f"Usuário {usuario.id_usuario}: {len(usuario._Usuario__interacoes_realizadas)} interações")

    def identificar_top_conteudos(self, metrica: str, n: int):
        chave_funcoes = {
            'tempo_total_consumo': lambda c: c.calcular_tempo_total_consumo(),
            'media_consumo': lambda c: c.calcular_media_tempo_consumo(),
            'comentarios': lambda c: len(c.listar_comentarios())
        }
        if metrica not in chave_funcoes:
            raise ValueError("Métrica inválida")
        conteudos = list(self.__conteudos_registrados.values())
        conteudos.sort(key=chave_funcoes[metrica], reverse=True)
        for conteudo in conteudos[:n]:
            print(f"{conteudo} -> {metrica}: {chave_funcoes[metrica](conteudo)}")
