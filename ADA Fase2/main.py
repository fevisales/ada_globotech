# main.py
from analise import SistemaAnaliseEngajamento

# Caminho para o CSV de interações
CAMINHO_CSV = "interacoes_globo.csv"


def main():
    print("Iniciando o sistema de análise de engajamento...")
    sistema = SistemaAnaliseEngajamento()

    print(f"Carregando dados do arquivo: {CAMINHO_CSV}")
    sistema.processar_interacoes_do_csv(CAMINHO_CSV)

    print("\n===== RELATÓRIO DE ENGAJAMENTO DOS CONTEÚDOS =====")
    sistema.gerar_relatorio_engajamento_conteudos(top_n=5)

    print("\n===== RELATÓRIO DE ATIVIDADE DOS USUÁRIOS =====")
    sistema.gerar_relatorio_atividade_usuarios(top_n=5)

    print("\n===== TOP 3 CONTEÚDOS POR TEMPO TOTAL DE CONSUMO =====")
    sistema.identificar_top_conteudos(metrica='tempo_total_consumo', n=3)

    print("\n===== FIM DA EXECUÇÃO =====")


if __name__ == "__main__":
    main()
