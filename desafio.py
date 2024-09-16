menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    operacao = input(menu)
    print(f"Operação escolhida: {operacao}")

    if operacao == "1":
        try:
            valor = float(input("Informe o valor do depósito: "))
            if valor <= 0:
                raise ValueError("O valor do depósito deve ser positivo.")
        except ValueError as e:
            print(f"Operação falhou! {e}")
        else:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito realizado com sucesso. Saldo atual: R$ {saldo:.2f}")

    elif operacao == "2":
        if numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques diários atingido.")
            continue
    
        try:
            valor = float(input("Informe o valor do saque: "))
            if valor <= 0:
                raise ValueError("O valor do saque deve ser positivo.")
            if valor > saldo:
                raise ValueError("Saldo insuficiente.")
            if valor > limite:
                raise ValueError("O valor do saque excede o limite permitido de R$ 500.")
        except ValueError as e:
            print(f"Operação falhou! {e}")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Saque realizado com sucesso. Saldo atual: R$ {saldo:.2f}")

    elif operacao == "3":
        print("\nEXTRATO\n")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")

    elif operacao == "4":
        print("Saindo...")
        break

    else:
        print("Operação inválida, por favor selecione novamente.")