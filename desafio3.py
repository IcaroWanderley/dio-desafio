from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\nAgência:\t{self.agencia}\nConta:\t\t{self.numero}\nTitular:\t{self.cliente.nome}\n"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def realizar_deposito(conta, valor):
    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)

def realizar_saque(conta, valor):
    transacao = Saque(valor)
    conta.cliente.realizar_transacao(conta, transacao)

def mostrar_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Nenhuma movimentação.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f}\tData: {transacao['data']}")
    print(f"\nSaldo Atual:\tR$ {conta.saldo:.2f}")
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
    usuarios.append(PessoaFisica(nome, nascimento, cpf, endereco))
    print("=== Usuário cadastrado com sucesso! ===")

def encontrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def abrir_conta(usuarios, contas):
    cpf = input("Informe o CPF do titular: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if usuario:
        numero_conta = len(contas) + 1
        conta = ContaCorrente.nova_conta(usuario, numero_conta)
        usuario.adicionar_conta(conta)
        contas.append(conta)
        print("\n=== Conta aberta com sucesso! ===")
    else:
        print("\n@@@ CPF não encontrado, abertura de conta cancelada! @@@")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
    else:
        for conta in contas:
            print("=" * 100)
            print(conta)

def iniciar_sistema():
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
            numero_conta = int(input("Informe o número da conta: "))
            conta = contas[numero_conta - 1]
            valor = float(input("Informe o valor do depósito: "))
            realizar_deposito(conta, valor)

        elif opcao == "2":
            numero_conta = int(input("Informe o número da conta: "))
            conta = contas[numero_conta - 1]
            valor = float(input("Informe o valor do saque: "))
            realizar_saque(conta, valor)

        elif opcao == "3":
            numero_conta = int(input("Informe o número da conta: "))
            conta = contas[numero_conta - 1]
            mostrar_extrato(conta)

        elif opcao == "4":
            adicionar_usuario(usuarios)

        elif opcao == "5":
            abrir_conta(usuarios, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Saindo do sistema...")
            break

        else:
            print("Operação inválida, por favor selecione novamente.")

# Executa o sistema
iniciar_sistema()
