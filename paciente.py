"""
Arquivo responsável pelo registro e gestão de pacientes.

Funcionalidades:
- Validação de CPF (formato simples: 11 dígitos numéricos)
- Recolha de dados do paciente (nome, idade, CPF) com tratamento de erros (try-except)
- Armazenamento dos dados do paciente
- Exibição dos dados do paciente na interface

Observações:
- A validação de CPF não verifica autenticidade, apenas o formato
- Todos dados coletados tem validação
"""

from utilidades import cabecalho, linha, pausar

def validar_cpf(cpf: str) -> bool:
    cpf = cpf.strip()
    if len(cpf) == 11 and cpf.isdigit():
        return True
    return False

def pedir_nome() -> str:
    while True:
        try:
            nome = input("  Nome completo: ").strip()

            if not nome:
                print("  [!] Nome não pode ser vazio.")
                continue

            partes = nome.split()
            if len(partes) < 2:
                print("  [!] Digite nome e sobrenome.")
                continue

            nome_valido = True
            for parte in partes:
                for c in parte:
                    if not c.isalpha():
                        nome_valido = False
                        break
                if not nome_valido:
                    break

            if not nome_valido:
                print("  [!] Use apenas letras. Números e símbolos não são permitidos.")
                continue

            return nome
        except Exception as e:
            print(f"  [!] Erro inesperado ao ler o nome: {e}")

def pedir_idade() -> int:
    while True:
        try:
            valor = input("  Idade: ").strip()
            idade = int(valor)
            if idade > 0:
                return idade
            print("  [!] Idade inválida. Digite um número inteiro positivo.")
        except ValueError:
            print("  [!] Entrada inválida. Por favor, digite apenas números inteiros para a idade.")
        except Exception as e:
            print(f"  [!] Erro inesperado ao ler a idade: {e}")

def pedir_cpf() -> str:
    while True:
        try:
            cpf = input("  CPF (somente 11 dígitos): ").strip()
            if validar_cpf(cpf):
                return cpf
            print("  [!] CPF inválido. Use exatamente 11 dígitos numéricos.")
        except Exception as e:
            print(f"  [!] Erro inesperado ao ler o CPF: {e}")

def registrar_paciente() -> dict:
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
    cabecalho("Dados do Paciente")
    print()
    print(f"  Nome  : {paciente['nome']}")
    print(f"  Idade : {paciente['idade']}")
    print(f"  CPF   : {paciente['cpf']}")
    pausar()