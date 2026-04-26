"""
# Arquivo com funções utilitárias reutilizáveis no sistema.
#
# Funcionalidades:
# - Limpeza do terminal
# - Exibição de cabeçalhos e separadores visuais
# - Validação de entradas do utilizador em menus
# - Seleção de opções em listas numeradas
# - Confirmação de ações (S/N)
# - Pausa da execução para leitura no terminal
"""

import os

def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def cabecalho(titulo: str) -> None:
    print("=" * 45)
    print(f"  CarePlus  |  {titulo}")
    print("=" * 45)

def linha() -> None:
    print("-" * 45)

def pedir_opcao_menu(opcoes_validas: list) -> str:
    while True:
        escolha = input("\nEscolha uma opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("  [!] Opção inválida. Tente novamente.")

def pedir_escolha_lista(lista: list, titulo: str) -> int:
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
            if indice == len(lista):
                return -1
            return indice
        print("  [!] Opção inválida.")

def confirmar_acao(mensagem: str) -> bool:
    while True:
        resposta = input(f"  {mensagem} (S/N): ").strip().upper()
        if resposta == "S":
            return True
        if resposta == "N":
            return False
        print("  [!] Digite S ou N.")

def pausar() -> None:
    input("\n  Pressione ENTER para continuar...")
    limpar_tela()
