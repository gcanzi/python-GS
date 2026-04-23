# agendamento.py
# Toda a lógica de marcação, cancelamento, reagendamento
# e consulta de status das consultas.

from utilidades import (
    cabecalho, linha_separadora, pausar,
    pedir_escolha_lista, confirmar_acao, pedir_opcao_menu
)

# Dados fixos disponíveis no sistema
MEDICOS      = ["Dr. Carlos", "Dra. Ana", "Dr. Pedro"]
LOCALIZACOES = ["Unidade Centro", "Unidade Norte", "Unidade Sul"]
TIPOS        = ["Clínica Geral", "Cardiologia", "Dermatologia"]
HORARIOS     = ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]

# Limite máximo de agendamentos ativos por paciente
LIMITE_AGENDAMENTOS = 3


def _gerar_id(agendamentos: list) -> int:
    # Gera um ID único incrementando o maior existente
    if not agendamentos:
        return 1
    maior = 0
    for a in agendamentos:
        if a["id"] > maior:
            maior = a["id"]
    return maior + 1


def _contar_ativos(agendamentos: list, cpf: str) -> int:
    # Conta quantos agendamentos ativos o paciente tem
    total = 0
    for a in agendamentos:
        if a["cpf"] == cpf and a["status"] == "ativo":
            total += 1
    return total


def _horario_ocupado(agendamentos: list, medico: str, horario: str) -> bool:
    # Verifica se o médico já tem esse horário ocupado (ativo)
    for a in agendamentos:
        if a["medico"] == medico and a["horario"] == horario and a["status"] == "ativo":
            return True
    return False


def _listar_consultas_paciente(agendamentos: list, cpf: str, apenas_ativos: bool = False) -> list:
    # Retorna lista de consultas do paciente com filtro opcional
    resultado = []
    for a in agendamentos:
        if a["cpf"] == cpf:
            if apenas_ativos and a["status"] != "ativo":
                continue
            resultado.append(a)
    return resultado


def _exibir_consulta(agendamento: dict) -> None:
    # Exibe os detalhes de um agendamento de forma formatada
    print(f"  ID       : {agendamento['id']}")
    print(f"  Médico   : {agendamento['medico']}")
    print(f"  Local    : {agendamento['localizacao']}")
    print(f"  Tipo     : {agendamento['tipo']}")
    print(f"  Horário  : {agendamento['horario']}")
    print(f"  Status   : {agendamento['status'].upper()}")


def agendar_consulta(agendamentos: list, paciente: dict) -> None:
    # Fluxo completo de marcação de uma nova consulta
    cabecalho("Agendar Consulta")

    cpf = paciente["cpf"]

    # Verificar limite de agendamentos ativos
    if _contar_ativos(agendamentos, cpf) >= LIMITE_AGENDAMENTOS:
        print(f"\n  [!] Limite de {LIMITE_AGENDAMENTOS} agendamentos ativos atingido.")
        print("  Cancele uma consulta antes de agendar outra.")
        pausar()
        return

    # Escolha do médico
    idx_medico = pedir_escolha_lista(MEDICOS, "Escolha o Médico:")
    if idx_medico == -1:
        return
    medico = MEDICOS[idx_medico]

    # Escolha da localização
    idx_local = pedir_escolha_lista(LOCALIZACOES, "Escolha a Localização:")
    if idx_local == -1:
        return
    localizacao = LOCALIZACOES[idx_local]

    # Escolha do tipo de consulta
    idx_tipo = pedir_escolha_lista(TIPOS, "Escolha o Tipo de Consulta:")
    if idx_tipo == -1:
        return
    tipo = TIPOS[idx_tipo]

    # Escolha do horário — mostra apenas os disponíveis para o médico
    horarios_livres = []
    for h in HORARIOS:
        if not _horario_ocupado(agendamentos, medico, h):
            horarios_livres.append(h)

    if not horarios_livres:
        print(f"\n  [!] {medico} não tem horários disponíveis.")
        pausar()
        return

    idx_horario = pedir_escolha_lista(horarios_livres, "Escolha o Horário:")
    if idx_horario == -1:
        return
    horario = horarios_livres[idx_horario]

    # Resumo completo antes de confirmar
    print()
    cabecalho("Resumo do Agendamento")
    print(f"  Paciente : {paciente['nome']}")
    print(f"  Médico   : {medico}")
    print(f"  Local    : {localizacao}")
    print(f"  Tipo     : {tipo}")
    print(f"  Horário  : {horario}")
    linha_separadora()

    if not confirmar_acao("Confirmar agendamento?"):
        print("  [!] Agendamento cancelado.")
        pausar()
        return

    # Cria o novo agendamento e adiciona à lista
    novo = {
        "id": _gerar_id(agendamentos),
        "cpf": cpf,
        "medico": medico,
        "localizacao": localizacao,
        "tipo": tipo,
        "horario": horario,
        "status": "ativo"
    }
    agendamentos.append(novo)

    print(f"\n  [✓] Consulta agendada com ID #{novo['id']}!")
    pausar()


def _escolher_consulta_paciente(agendamentos: list, cpf: str, apenas_ativos: bool = False) -> dict:
    # Mostra as consultas do paciente e devolve a escolhida (ou None)
    consultas = _listar_consultas_paciente(agendamentos, cpf, apenas_ativos)

    if not consultas:
        msg = "Nenhuma consulta ativa encontrada." if apenas_ativos else "Nenhuma consulta encontrada."
        print(f"\n  [!] {msg}")
        pausar()
        return None

    print("\n  Suas consultas:")
    linha_separadora()
    for i, c in enumerate(consultas):
        print(f"  {i + 1}. ID #{c['id']} | {c['medico']} | {c['horario']} | {c['status'].upper()}")
    linha_separadora()

    opcoes = [str(i + 1) for i in range(len(consultas))]
    while True:
        escolha = input("  Escolha o número da consulta (ou 0 para voltar): ").strip()
        if escolha == "0":
            return None
        if escolha in opcoes:
            return consultas[int(escolha) - 1]
        print("  [!] Opção inválida.")


def cancelar_consulta(agendamentos: list, cpf: str) -> None:
    # Cancela uma consulta ativa do paciente
    cabecalho("Cancelar Consulta")

    consulta = _escolher_consulta_paciente(agendamentos, cpf, apenas_ativos=True)
    if not consulta:
        return

    print()
    _exibir_consulta(consulta)
    linha_separadora()

    if not confirmar_acao("Cancelar esta consulta?"):
        print("  [!] Operação cancelada.")
        pausar()
        return

    # Atualiza o status na lista original (busca por ID)
    for a in agendamentos:
        if a["id"] == consulta["id"]:
            a["status"] = "cancelado"
            break

    print("  [✓] Consulta cancelada com sucesso.")
    pausar()


def ver_status(agendamentos: list, cpf: str) -> None:
    # Exibe todas as consultas do paciente com seus status
    cabecalho("Status das Consultas")

    consultas = _listar_consultas_paciente(agendamentos, cpf)
    if not consultas:
        print("\n  [!] Nenhuma consulta encontrada.")
        pausar()
        return

    print()
    for c in consultas:
        linha_separadora()
        _exibir_consulta(c)
    linha_separadora()
    pausar()


def reagendar_consulta(agendamentos: list, cpf: str) -> None:
    # Permite trocar o horário de uma consulta ativa
    cabecalho("Reagendar Consulta")

    consulta = _escolher_consulta_paciente(agendamentos, cpf, apenas_ativos=True)
    if not consulta:
        return

    print()
    _exibir_consulta(consulta)
    linha_separadora()

    # Mostra horários livres para o mesmo médico (exceto o atual)
    medico = consulta["medico"]
    horarios_livres = []
    for h in HORARIOS:
        # O horário atual da consulta fica disponível para ela mesma
        if h == consulta["horario"]:
            continue
        if not _horario_ocupado(agendamentos, medico, h):
            horarios_livres.append(h)

    if not horarios_livres:
        print(f"\n  [!] Não há outros horários disponíveis para {medico}.")
        pausar()
        return

    idx_horario = pedir_escolha_lista(horarios_livres, "Escolha o novo horário:")
    if idx_horario == -1:
        return
    novo_horario = horarios_livres[idx_horario]

    if not confirmar_acao(f"Reagendar para {novo_horario}?"):
        print("  [!] Operação cancelada.")
        pausar()
        return

    # Atualiza o horário na lista original
    for a in agendamentos:
        if a["id"] == consulta["id"]:
            a["horario"] = novo_horario
            break

    print(f"  [✓] Consulta reagendada para {novo_horario}.")
    pausar()


def gerir_consultas(agendamentos: list, paciente: dict) -> None:
    # Submenu de gestão de consultas
    cpf = paciente["cpf"]

    while True:
        cabecalho("Gerir Consultas")
        print()
        print("  1. Cancelar Consulta")
        print("  2. Ver Status")
        print("  3. Reagendar Consulta")
        print("  4. Voltar ao Menu Principal")

        opcao = pedir_opcao_menu(["1", "2", "3", "4"])

        if opcao == "1":
            cancelar_consulta(agendamentos, cpf)
        elif opcao == "2":
            ver_status(agendamentos, cpf)
        elif opcao == "3":
            reagendar_consulta(agendamentos, cpf)
        elif opcao == "4":
            break
