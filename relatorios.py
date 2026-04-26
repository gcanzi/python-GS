"""
Este arquivo concentra a lógica analítica do sistema, transformando os dados 
brutos de agendamentos e pacientes em informações úteis.
Funcionalidades:
    - Contagem total de consultas (ativas e canceladas).
    - Identificação do médico com maior número de agendamentos.
    - Agrupamento e contagem de consultas por especialidade/tipo.
    - Listagem formatada de todos os pacientes cadastrados no sistema.
    """

from utilidades import cabecalho, linha, pausar
from agendamento import TIPOS, MEDICOS

def total_agendamentos(agendamentos: list) -> int:
    return len(agendamentos)

def medico_mais_escolhido(agendamentos: list) -> tuple:
    contagem = {}
    for medico in MEDICOS:
        contagem[medico] = 0

    for a in agendamentos:
        if a["status"] == "ativo":
            contagem[a["medico"]] = contagem.get(a["medico"], 0) + 1

    mais_escolhido = None
    maior = -1
    for medico, total in contagem.items():
        if total > maior:
            maior = total
            mais_escolhido = medico

    return mais_escolhido, maior

def agrupar_por_tipo(agendamentos: list) -> dict:
    grupos = {}
    for tipo in TIPOS:
        grupos[tipo] = 0

    for a in agendamentos:
        if a["status"] == "ativo":
            grupos[a["tipo"]] = grupos.get(a["tipo"], 0) + 1

    return grupos

def exibir_relatorios(agendamentos: list, pacientes: list) -> None:
    cabecalho("Relatórios e Informações")
    print()

    total = total_agendamentos(agendamentos)
    ativos = sum(1 for a in agendamentos if a["status"] == "ativo")
    cancelados = total - ativos

    print("  [ Agendamentos ]")
    linha()
    print(f"  Total    : {total}")
    print(f"  Ativos   : {ativos}")
    print(f"  Cancelados: {cancelados}")
    print()

    print("  [ Médico Mais Escolhido ]")
    linha()
    medico, votos = medico_mais_escolhido(agendamentos)
    if votos == 0:
        print("  Nenhum agendamento ativo registado.")
    else:
        print(f"  {medico} ({votos} consulta(s) ativa(s))")
    print()

    print("  [ Consultas por Tipo (ativas) ]")
    linha()
    grupos = agrupar_por_tipo(agendamentos)
    for tipo, quantidade in grupos.items():
        print(f"  {tipo:<18}: {quantidade}")
    print()

    print("  [ Pacientes Registados ]")
    linha()
    if not pacientes:
        print("  Nenhum paciente registado.")
    else:
        for p in pacientes:
            print(f"  {p['nome']} | Idade: {p['idade']} | CPF: {p['cpf']}")

    linha()
    pausar()
