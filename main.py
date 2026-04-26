"""
Arquivo principal do sistema CarePlus.

Este arquivo funciona como ponto de entrada da aplicação, sendo responsável por:
- Controlar o ciclo principal do programa.
- Gerir o menu interativo apresentado ao usuário.
- Coordenar a navegação entre os diferentes módulos do sistema
  (registo de pacientes, agendamento, gestão de consultas e relatórios).

Também mantém os dados em memória durante a execução, incluindo
o paciente atual da sessão e a lista de agendamentos.
"""

from utilidades import limpar_tela, cabecalho, linha, pedir_opcao_menu, pausar
from paciente   import registar_paciente
from agendamento import agendar_consulta, gerir_consultas
from relatorios  import exibir_relatorios


def exibir_menu(paciente_atual: dict) -> None:
    cabecalho("Menu Principal")
    print()

    if paciente_atual is None:
        print("  1. Registar Paciente")
        print("  2. [Faça o registo primeiro]")
        print("  3. [Faça o registo primeiro]")
        print("  4. [Faça o registo primeiro]")
    else:
        nome_paciente = paciente_atual["nome"].split()[0]
        print(f"  1. Paciente: {nome_paciente} (já registado)")
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
    pacientes    = []

    paciente_atual = None

    while True:
        limpar_tela()
        exibir_menu(paciente_atual)

        validas = opcoes_disponiveis(paciente_atual)
        opcao = pedir_opcao_menu(validas)

        # --- Opção 1: Registo ---
        if opcao == "1":
            if paciente_atual is not None:
                # Já registado — bloqueia novo registo
                limpar_tela()
                cabecalho("Aviso")
                print(f"\n  Paciente '{paciente_atual['nome']}' já está registado.")
                print("  Apenas um paciente por sessão.")
                pausar()
            else:
                limpar_tela()
                paciente_atual = registar_paciente()
                pacientes.append(paciente_atual)

        # --- Opção 2: Agendar ---
        elif opcao == "2":
            limpar_tela()
            agendar_consulta(agendamentos, paciente_atual)

        # --- Opção 3: Gerir ---
        elif opcao == "3":
            limpar_tela()
            gerir_consultas(agendamentos, paciente_atual)

        # --- Opção 4: Relatórios ---
        elif opcao == "4":
            limpar_tela()
            exibir_relatorios(agendamentos, pacientes)

        # --- Opção 5: Sair ---
        elif opcao == "5":
            limpar_tela()
            print("\n  Obrigado por usar o CarePlus. Até logo!\n")
            break


# Ponto de arranque
if __name__ == "__main__":
    main()
