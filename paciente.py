# paciente.py
# Responsável pelo registo do paciente, validação de CPF
# e acesso aos dados do paciente em sessão.

from utilidades import cabecalho, linha, pausar


def validar_cpf(cpf: str) -> bool:
    # CPF válido: exatamente 11 dígitos numéricos
    cpf = cpf.strip()
    if len(cpf) == 11 and cpf.isdigit():
        return True
    return False


def pedir_nome() -> str:
    # Garante que o nome não está vazio
    while True:
        nome = input("  Nome completo: ").strip()
        if nome:
            return nome
        print("  [!] Nome não pode ser vazio.")


def pedir_idade() -> int:
    # Garante que a idade é um número inteiro positivo
    while True:
        valor = input("  Idade: ").strip()
        if valor.isdigit() and int(valor) > 0:
            return int(valor)
        print("  [!] Idade inválida. Digite um número inteiro positivo.")


def pedir_cpf() -> str:
    # Pede CPF e valida até estar correto
    while True:
        cpf = input("  CPF (somente 11 dígitos): ").strip()
        if validar_cpf(cpf):
            return cpf
        print("  [!] CPF inválido. Use exatamente 11 dígitos numéricos.")


def registrar_paciente() -> dict:
    # Recolhe os dados do paciente e retorna o dicionário preenchido
    cabecalho("Registo de Paciente")
    print()

    nome = pedir_nome()
    idade = pedir_idade()
    cpf = pedir_cpf()

    paciente = {
        "nome": nome,
        "idade": idade,
        "cpf": cpf
    }

    linha()
    print(f"  Nome  : {paciente['nome']}")
    print(f"  Idade : {paciente['idade']}")
    print(f"  CPF   : {paciente['cpf']}")
    linha()
    print("  [✓] Paciente registado com sucesso!")
    pausar()

    return paciente


def exibir_dados_paciente(paciente: dict) -> None:
    # Mostra os dados do paciente atual
    cabecalho("Dados do Paciente")
    print()
    print(f"  Nome  : {paciente['nome']}")
    print(f"  Idade : {paciente['idade']}")
    print(f"  CPF   : {paciente['cpf']}")
    pausar()
