# utilidades.py
# Funções genéricas reutilizadas por todo o sistema:
# limpar ecrã, validar escolhas de menu e formatar cabeçalhos.

import os


def limpar_tela() -> None:
    # Limpa o terminal dependendo do sistema operativo
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho(titulo: str) -> None:
    # Exibe um cabeçalho visual simples para cada secção
    print("=" * 45)
    print(f"  CarePlus  |  {titulo}")
    print("=" * 45)


def linha() -> None:
    print("-" * 45)


def pedir_opcao_menu(opcoes_validas: list) -> str:
    # Pede uma opção ao utilizador e repete enquanto for inválida
    while True:
        escolha = input("\nEscolha uma opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("  [!] Opção inválida. Tente novamente.")


def pedir_escolha_lista(lista: list, titulo: str) -> int:
    # Mostra uma lista numerada e retorna o índice escolhido
    # Retorna -1 se o utilizador escolher voltar
    print(f"\n  {titulo}")
    linha()
    for i, item in enumerate(lista):
        print(f"  {i + 1}. {item}")
    print(f"  {len(lista) + 1}. Voltar")
    linha()

    opcoes_validas = [str(i + 1) for i in range(len(lista) + 1)]

    while True:
        escolha = input("  Escolha: ").strip()
        if escolha in opcoes_validas:
            indice = int(escolha) - 1
            # Se escolheu "Voltar", retorna -1
            if indice == len(lista):
                return -1
            return indice
        print("  [!] Opção inválida.")


def confirmar_acao(mensagem: str) -> bool:
    # Pede confirmação S/N e retorna True ou False
    while True:
        resposta = input(f"  {mensagem} (S/N): ").strip().upper()
        if resposta == "S":
            return True
        if resposta == "N":
            return False
        print("  [!] Digite S ou N.")


def pausar() -> None:
    # Pausa o ecrã para o utilizador ler a mensagem antes de continuar
    input("\n  Pressione ENTER para continuar...")
