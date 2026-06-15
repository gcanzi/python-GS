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
# - Persistência de dados em arquivos JSON
"""

import os
import json

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

def carregar_dados(nome_arquivo: str) -> list:
    """Carrega dados de um arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
    if not os.path.exists(nome_arquivo):
        return []
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print(f"  [!] Erro ao decodificar o arquivo {nome_arquivo}. Retornando lista vazia.")
        return []
    except Exception as e:
        print(f"  [!] Erro inesperado ao ler {nome_arquivo}: {e}")
        return []

def salvar_dados(dados: list, nome_arquivo: str) -> None:
    """Salva a lista de dicionários em um arquivo JSON."""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"  [!] Erro ao salvar os dados em {nome_arquivo}: {e}")