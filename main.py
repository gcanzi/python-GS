# main.py
# Ponto de entrada do sistema CarePlus.
# Controla o loop principal, o menu dinâmico e coordena os módulos.

from utilidades import limpar_ecra, cabecalho, linha_separadora, pedir_opcao_menu, pausar
from paciente   import registar_paciente
from agendamento import agendar_consulta, gerir_consultas
from relatorios  import exibir_relatorios


def exibir_menu(paciente_atual: dict) -> None:
    # Monta e exibe o menu principal de forma dinâmica
    cabecalho("Menu Principal")
    print()

    # Opção 1 muda conforme o estado do registo
    if paciente_atual is None:
        print("  1. Registar Paciente")
        print("  2. [Faça o registo primeiro]")
        print("  3. [Faça o registo primeiro]")
        print("  4. [Faça o registo primeiro]")
    else:
        nome_curto = paciente_atual["nome"].split()[0]  # só o primeiro nome
        print(f"  1. Paciente: {nome_curto} (já registado)")
        print("  2. Agendar Consulta")
        print("  3. Gerir Consultas")
        print("  4. Relatórios / Informações")

    print("  5. Sair")
    linha_separadora()


def opcoes_disponiveis(paciente_atual: dict) -> list:
    # Retorna quais opções o utilizador pode escolher agora
    if paciente_atual is None:
        return ["1", "5"]
    return ["1", "2", "3", "4", "5"]


def main() -> None:
    # Dados em memória — lista de agendamentos e lista de pacientes
    agendamentos = []
    pacientes    = []

    # Paciente da sessão actual (None até ao registo)
    paciente_atual = None

    while True:
        limpar_ecra()
        exibir_menu(paciente_atual)

        validas = opcoes_disponiveis(paciente_atual)
        opcao = pedir_opcao_menu(validas)

        # --- Opção 1: Registo ---
        if opcao == "1":
            if paciente_atual is not None:
                # Já registado — bloqueia novo registo
                limpar_ecra()
                cabecalho("Aviso")
                print(f"\n  Paciente '{paciente_atual['nome']}' já está registado.")
                print("  Apenas um paciente por sessão.")
                pausar()
            else:
                limpar_ecra()
                paciente_atual = registar_paciente()
                pacientes.append(paciente_atual)

        # --- Opção 2: Agendar ---
        elif opcao == "2":
            limpar_ecra()
            agendar_consulta(agendamentos, paciente_atual)

        # --- Opção 3: Gerir ---
        elif opcao == "3":
            limpar_ecra()
            gerir_consultas(agendamentos, paciente_atual)

        # --- Opção 4: Relatórios ---
        elif opcao == "4":
            limpar_ecra()
            exibir_relatorios(agendamentos, pacientes)

        # --- Opção 5: Sair ---
        elif opcao == "5":
            limpar_ecra()
            print("\n  Obrigado por usar o CarePlus. Até logo!\n")
            break


# Ponto de arranque
if __name__ == "__main__":
    main()
