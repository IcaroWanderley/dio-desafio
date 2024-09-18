import textwrap

# Funções do sistema bancário
def realizar_deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
    else:
        print(f"\n@@@ Depósito não permitido! Valor {valor:.2f} inválido. @@@")
    return saldo, extrato

def realizar_saque(saldo, valor, extrato, limite, saques_realizados, max_saques):
    saldo_insuficiente = valor > saldo
    limite_excedido = valor > limite
    saques_excedidos = saques_realizados >= max_saques

    if saldo_insuficiente:
        print("\n@@@ Saque não realizado! Saldo insuficiente. @@@")
    elif limite_excedido:
        print(f"\n@@@ Saque negado! Valor de R$ {valor:.2f} acima do limite de R$ {limite:.2f}. @@@")
    elif saques_excedidos:
        print(f"\n@@@ Saque bloqueado! Limite de {max_saques} saques atingido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        saques_realizados += 1
        print(f"\n=== Saque de R$ {valor:.2f} efetuado com sucesso! ===")
    else:
        print(f"\n@@@ Saque não realizado! Valor {valor:.2f} inválido. @@@")
    return saldo, extrato, saques_realizados

def mostrar_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Nenhuma movimentação." if not extrato else extrato)
    print(f"\nSaldo Atual:\tR$ {saldo:.2f}")
    print("==========================================")

def adicionar_usuario(usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    usuario = encontrar_usuario(cpf, usuarios)
    if usuario:
        print("\n@@@ Já existe um usuário com esse CPF! @@@")
        return
    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Rua, Número - Bairro - Cidade/UF): ")
    usuarios.append({"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário cadastrado com sucesso! ===")

def encontrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def abrir_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do titular: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if usuario:
        print("\n=== Conta aberta com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ CPF não encontrado, abertura de conta cancelada! @@@")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
    else:
        for conta in contas:
            info_conta = f"""\n
            Agência:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(info_conta))

# Início do sistema
def iniciar_sistema():
    MAX_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    saques_realizados = 0
    usuarios = []
    contas = []

    menu = """
    ================ MENU ================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Usuário
    [5] Abrir Conta
    [6] Listar Contas
    [7] Sair
    => """

    while True:
        opcao = input(menu)
        print(f"Operação escolhida: {opcao}")

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = realizar_deposito(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, saques_realizados = realizar_saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                saques_realizados=saques_realizados,
                max_saques=MAX_SAQUES
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato)

        elif opcao == "4":
            adicionar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = abrir_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Saindo do sistema...")
            break

        else:
            print("Operação inválida, por favor selecione novamente.")

# Executa o sistema
iniciar_sistema()
