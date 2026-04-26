"""
Arquivo principal do sistema CarePlus.

Este arquivo funciona como ponto de entrada da aplicação, sendo responsável por:
- Controlar o ciclo principal do programa.
- Gerir o menu interativo apresentado ao usuário.
- Coordenar a navegação entre os diferentes módulos do sistema
  (registro de pacientes, agendamento, gestão de consultas e relatórios).

Também mantém os dados em memória durante a execução, incluindo
o paciente atual da sessão e a lista de agendamentos.
"""

from utilidades import limpar_tela, cabecalho, linha, pedir_opcao_menu, pausar
from paciente   import registrar_paciente
from agendamento import agendar_consulta, gerir_consultas
from relatorios  import exibir_relatorios


def exibir_menu(paciente_atual: dict) -> None:
    cabecalho("Menu Principal")
    print()

    if paciente_atual is None:
        print("  1. Registrar Paciente")
        print("  2. [Faça o registro primeiro]")
        print("  3. [Faça o registro primeiro]")
        print("  4. [Faça o registro primeiro]")
    else:
        nome_paciente = paciente_atual["nome"].split()[0]
        print(f"  1. Paciente: {nome_paciente} (já registrado)")
        print("  2. Agendar Consulta")
        print("  3. Gerir Consultas")
        print("  4. Relatórios / Informações")

    print("  5. Sair")
    linha()


def opcoes_disponiveis(paciente_atual: dict) -> list:
    if paciente_atual is None:
        return ["1", "5"]
    return ["1", "2", "3", "4", "5"]


def main() -> None:

    agendamentos = []
    pacientes = []

    paciente_atual = None

    while True:
        limpar_tela()
        exibir_menu(paciente_atual)

        validas = opcoes_disponiveis(paciente_atual)
        opcao = pedir_opcao_menu(validas)

        # 1 - Paciente
        if opcao == "1":
            if paciente_atual is not None:
                # Se já estiver registrado — bloqueia novo registo
                limpar_tela()
                cabecalho("Aviso")
                print(f"\n  Paciente '{paciente_atual['nome']}' já está registrado.")
                print("  Apenas um paciente por sessão.")
                pausar()
            else:
                limpar_tela()
                paciente_atual = registrar_paciente()
                pacientes.append(paciente_atual)

        # 2 - Agendamento
        elif opcao == "2":
            limpar_tela()
            agendar_consulta(agendamentos, paciente_atual)

        # 3 - Gerir Consultas
        elif opcao == "3":
            limpar_tela()
            gerir_consultas(agendamentos, paciente_atual)

        # 4 - Relatórios
        elif opcao == "4":
            limpar_tela()
            exibir_relatorios(agendamentos, pacientes)

        # 5 - Sair
        elif opcao == "5":
            limpar_tela()
            print("\n  Obrigado por usar o CarePlus. Até logo!\n")
            break


# Inicia o programa ao executar o arquivo main.py
if __name__ == "__main__":
    main()
