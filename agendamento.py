"""
 Este arquivo contém toda a lógica de negócio para o gerenciamento de consultas, 
 incluindo as funcionalidades de:
    - Agendamento de novas consultas.
    - Cancelamento de consultas ativas.
    - Reagendamento de horários para consultas existentes.
    - Consulta de status e histórico de agendamentos por paciente.
 
 O módulo também implementa regras de validação, como o limite de agendamentos 
 por CPF e a verificação de disponibilidade da agenda dos médicos.
"""

from utilidades import *

MEDICOS = ["Dr. Carlos", "Dra. Ana", "Dr. Pedro"]
LOCALIZACOES = ["Unidade Centro", "Unidade Norte", "Unidade Sul"]
TIPOS = ["Clínica Geral", "Cardiologia", "Dermatologia"]
HORARIOS = ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]

LIMITE_AGENDAMENTOS = 3

def gerar_id(agendamentos: list) -> int:
    if not agendamentos:
        return 1
    maior = 0
    for a in agendamentos:
        if a["id"] > maior:
            maior = a["id"]
    return maior + 1

def contar_ativos(agendamentos: list, cpf: str) -> int:
    total = 0
    for a in agendamentos:
        if a["cpf"] == cpf and a["status"] == "ativo":
            total += 1
    return total

def horario_ocupado(agendamentos: list, medico: str, horario: str) -> bool:
    for a in agendamentos:
        if a["medico"] == medico and a["horario"] == horario and a["status"] == "ativo":
            return True
    return False

def listar_consultas_paciente(agendamentos: list, cpf: str, apenas_ativos: bool = False) -> list:
    resultado = []
    for a in agendamentos:
        if a["cpf"] == cpf:
            if apenas_ativos and a["status"] != "ativo":
                continue
            resultado.append(a)
    return resultado

def exibir_consulta(agendamento: dict) -> None:
    print(f"  ID       : {agendamento['id']}")
    print(f"  Médico   : {agendamento['medico']}")
    print(f"  Local    : {agendamento['localizacao']}")
    print(f"  Tipo     : {agendamento['tipo']}")
    print(f"  Horário  : {agendamento['horario']}")
    print(f"  Status   : {agendamento['status'].upper()}")

def agendar_consulta(agendamentos: list, paciente: dict) -> None:
    cabecalho("Agendar Consulta")

    cpf = paciente["cpf"]

    if contar_ativos(agendamentos, cpf) >= LIMITE_AGENDAMENTOS:
        print(f"\n  [!] Limite de {LIMITE_AGENDAMENTOS} agendamentos ativos atingido.")
        print("  Cancele uma consulta antes de agendar outra.")
        pausar()
        return

    opcao_medico = pedir_escolha_lista(MEDICOS, "Escolha o Médico:")
    if opcao_medico == -1:
        return
    medico = MEDICOS[opcao_medico]

    opcao_local = pedir_escolha_lista(LOCALIZACOES, "Escolha a Localização:")
    if opcao_local == -1:
        return
    localizacao = LOCALIZACOES[opcao_local]

    opcao_tipo = pedir_escolha_lista(TIPOS, "Escolha o Tipo de Consulta:")
    if opcao_tipo == -1:
        return
    tipo = TIPOS[opcao_tipo]

    horarios_livres = []
    for h in HORARIOS:
        if not horario_ocupado(agendamentos, medico, h):
            horarios_livres.append(h)

    if not horarios_livres:
        print(f"\n  [!] {medico} não tem horários disponíveis.")
        pausar()
        return

    opcao_horario = pedir_escolha_lista(horarios_livres, "Escolha o Horário:")
    if opcao_horario == -1:
        return
    horario = horarios_livres[opcao_horario]

    print()
    cabecalho("Resumo do Agendamento")
    print(f"  Paciente : {paciente['nome']}")
    print(f"  Médico   : {medico}")
    print(f"  Local    : {localizacao}")
    print(f"  Tipo     : {tipo}")
    print(f"  Horário  : {horario}")
    linha()

    if not confirmar_acao("Confirmar agendamento?"):
        print("  [!] Agendamento cancelado.")
        pausar()
        return

    novo = {
        "id": gerar_id(agendamentos),
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

def escolher_consulta_paciente(agendamentos: list, cpf: str, apenas_ativos: bool = False) -> dict:
    consultas = listar_consultas_paciente(agendamentos, cpf, apenas_ativos)

    if not consultas:
        msg = "Nenhuma consulta ativa encontrada." if apenas_ativos else "Nenhuma consulta encontrada."
        print(f"\n  [!] {msg}")
        pausar()
        return None

    print("\n  Suas consultas:")
    linha()
    for i, c in enumerate(consultas):
        print(f"  {i + 1}. ID #{c['id']} | {c['medico']} | {c['horario']} | {c['status'].upper()}")
    linha()

    opcoes = [str(i + 1) for i in range(len(consultas))]
    while True:
        escolha = input("  Escolha o número da consulta (ou 0 para voltar): ").strip()
        if escolha == "0":
            return None
        if escolha in opcoes:
            return consultas[int(escolha) - 1]
        print("  [!] Opção inválida.")

def cancelar_consulta(agendamentos: list, cpf: str) -> None:
    cabecalho("Cancelar Consulta")

    consulta = escolher_consulta_paciente(agendamentos, cpf, apenas_ativos=True)
    if not consulta:
        return

    print()
    exibir_consulta(consulta)
    linha()

    if not confirmar_acao("Cancelar esta consulta?"):
        print("  [!] Operação cancelada.")
        pausar()
        return

    for a in agendamentos:
        if a["id"] == consulta["id"]:
            a["status"] = "cancelado"
            break

    print("  [✓] Consulta cancelada com sucesso.")
    pausar()

def ver_status(agendamentos: list, cpf: str) -> None:
    cabecalho("Status das Consultas")

    consultas = listar_consultas_paciente(agendamentos, cpf)
    if not consultas:
        print("\n  [!] Nenhuma consulta encontrada.")
        pausar()
        return

    print()
    for c in consultas:
        linha()
        exibir_consulta(c)
    linha()
    pausar()

def reagendar_consulta(agendamentos: list, cpf: str) -> None:
    cabecalho("Reagendar Consulta")

    consulta = escolher_consulta_paciente(agendamentos, cpf, apenas_ativos=True)
    if not consulta:
        return

    print()
    exibir_consulta(consulta)
    linha()

    medico = consulta["medico"]
    horarios_livres = []
    for h in HORARIOS:
        if h == consulta["horario"]:
            continue
        if not horario_ocupado(agendamentos, medico, h):
            horarios_livres.append(h)

    if not horarios_livres:
        print(f"\n  [!] Não há outros horários disponíveis para {medico}.")
        pausar()
        return

    opcao_horario = pedir_escolha_lista(horarios_livres, "Escolha o novo horário:")
    if opcao_horario == -1:
        return
    novo_horario = horarios_livres[opcao_horario]

    if not confirmar_acao(f"Reagendar para {novo_horario}?"):
        print("  [!] Operação cancelada.")
        pausar()
        return

    for a in agendamentos:
        if a["id"] == consulta["id"]:
            a["horario"] = novo_horario
            break

    print(f"  [✓] Consulta reagendada para {novo_horario}.")
    pausar()


def gerir_consultas(agendamentos: list, paciente: dict) -> None:
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
