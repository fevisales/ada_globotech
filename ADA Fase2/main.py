# main.py
from analise import SistemaAnaliseEngajamento

CAMINHO_CSV = "interacoes_globo.csv"

def main():
    print("=" * 60)
    print("Bem-vindo à análise de engajamento das mídias Globo 📺")
    print("Este sistema vai te mostrar os conteúdos e usuários mais ativos!")
    print("=" * 60)

    sistema = SistemaAnaliseEngajamento()

    print("\n[INFO] Lendo os dados do arquivo de interações...")
    sistema.processar_interacoes_do_csv(CAMINHO_CSV)

    try:
        top_n_conteudos = int(input("\n👉 Quantos conteúdos mais engajados você quer visualizar? "))
        top_n_usuarios = int(input("👉 Quantos usuários mais ativos você quer visualizar? "))
        top_n_top = int(input("👉 Quantos conteúdos no TOP consumo você quer ver? "))
    except ValueError:
        print("\n[ERRO] Opa! Parece que algo foi digitado errado. Vamos usar o padrão (5) por enquanto.")
        top_n_conteudos = top_n_usuarios = top_n_top = 5

    print("\n=== Engajamento por Conteúdo ===")
    sistema.gerar_relatorio_engajamento_conteudos(top_n=top_n_conteudos)

    print("\n=== Atividade dos Usuários ===")
    sistema.gerar_relatorio_atividade_usuarios(top_n=top_n_usuarios)

    print("\n=== Top Conteúdos por Tempo Total de Consumo ===")
    sistema.identificar_top_conteudos(metrica='tempo_total_consumo', n=top_n_top)

    print("\n[SUCESSO] Obrigado por usar o analisador de engajamento. Até a próxima! 👋")
    print("=" * 60)


if __name__ == "__main__":
    main()
