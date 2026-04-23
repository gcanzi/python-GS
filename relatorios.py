# relatorios.py
# Processa e exibe estatísticas sobre agendamentos e pacientes.
# Toda a lógica usa apenas iterações em listas e dicionários.

from utilidades import cabecalho, linha_separadora, pausar
from agendamento import TIPOS, MEDICOS


def _total_agendamentos(agendamentos: list) -> int:
    # Conta o total de agendamentos independentemente do status
    return len(agendamentos)


def _medico_mais_escolhido(agendamentos: list) -> tuple:
    # Descobre qual médico tem mais agendamentos ativos
    contagem = {}
    for medico in MEDICOS:
        contagem[medico] = 0

    for a in agendamentos:
        if a["status"] == "ativo":
            contagem[a["medico"]] = contagem.get(a["medico"], 0) + 1

    # Encontra o médico com maior contagem
    mais_escolhido = None
    maior = -1
    for medico, total in contagem.items():
        if total > maior:
            maior = total
            mais_escolhido = medico

    return mais_escolhido, maior


def _agrupar_por_tipo(agendamentos: list) -> dict:
    # Agrupa consultas ativas por tipo e conta cada um
    grupos = {}
    for tipo in TIPOS:
        grupos[tipo] = 0

    for a in agendamentos:
        if a["status"] == "ativo":
            grupos[a["tipo"]] = grupos.get(a["tipo"], 0) + 1

    return grupos


def exibir_relatorios(agendamentos: list, pacientes: list) -> None:
    # Exibe todos os relatórios disponíveis numa única ecrã
    cabecalho("Relatórios e Informações")
    print()

    # 1. Total de agendamentos
    total = _total_agendamentos(agendamentos)
    ativos = sum(1 for a in agendamentos if a["status"] == "ativo")
    cancelados = total - ativos

    print("  [ Agendamentos ]")
    linha_separadora()
    print(f"  Total    : {total}")
    print(f"  Ativos   : {ativos}")
    print(f"  Cancelados: {cancelados}")
    print()

    # 2. Médico mais escolhido
    print("  [ Médico Mais Escolhido ]")
    linha_separadora()
    medico, votos = _medico_mais_escolhido(agendamentos)
    if votos == 0:
        print("  Nenhum agendamento ativo registado.")
    else:
        print(f"  {medico} ({votos} consulta(s) ativa(s))")
    print()

    # 3. Consultas agrupadas por tipo
    print("  [ Consultas por Tipo (ativas) ]")
    linha_separadora()
    grupos = _agrupar_por_tipo(agendamentos)
    for tipo, quantidade in grupos.items():
        print(f"  {tipo:<18}: {quantidade}")
    print()

    # 4. Listagem de pacientes registados
    print("  [ Pacientes Registados ]")
    linha_separadora()
    if not pacientes:
        print("  Nenhum paciente registado.")
    else:
        for p in pacientes:
            print(f"  {p['nome']} | Idade: {p['idade']} | CPF: {p['cpf']}")

    linha_separadora()
    pausar()
