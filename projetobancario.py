import textwrap


def menu():
    menu_text = """
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [N]\tNova conta
    [L]\tListar contas
    [U]\tNovo usuário
    [S]\tSair

    => """
    return input(textwrap.dedent(menu_text))


def depositar(saldo, valor):
    if valor > 0:
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} aceito.")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo


def sacar(saldo, extrato, valor, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\n**** Operação falhou! O valor informado é inválido. ****")
        return saldo, extrato

    if valor > saldo:
        print("\n==( Operação falhou! Você não tem saldo suficiente. )==")
    elif valor > limite:
        print("\n==( Operação falhou! O valor de saque excede o limite. )==")
    elif numero_saques >= limite_saques:
        print("\n==( Operação falhou! Número máximo de saques excedido. )==")
    else:
        saldo -= valor
        extrato[valor] = f"Saque: R$ {valor:.2f}"
        numero_saques += 1
        print("\n==( Saque realizado com sucesso! Deseja realizar outra operação? )==")

    return saldo, extrato


def exibir_extrato(saldo, extrato):
    print("\n=========== EXTRATO ============")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for valor, descricao in extrato.items():
            print(f"{descricao}")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("================================\n\n Obrigado por utilizar nossos serviços!")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n*** Já existe usuário com esse CPF! Insira um CPF válido. ***")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                    "cpf": cpf, "endereco": endereco})
    print("==( Usuário criado com sucesso! )==")


def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n==( Conta criada com sucesso! )==")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n*** Usuário não encontrado, fluxo de criação de conta encerrado! ***")
    return None


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta["agencia"]}
            C/C:\t\t{conta["numero_conta"]}
            Titular:\t{conta["usuario"]["nome"]}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = {}
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo = depositar(saldo, valor)

        elif opcao == "2":
            valor = float(input("Informe o valor de saque: "))
            saldo, extrato = sacar(saldo, extrato, valor,
                                   limite, numero_saques, LIMITE_SAQUES)

        elif opcao == "3":
            exibir_extrato(saldo, extrato)

        elif opcao.upper() == "U":
            criar_usuario(usuarios)

        elif opcao.upper() == "N":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao.upper() == "L":
            listar_contas(contas)

        elif opcao.upper() == "S":
            print("Você saiu do sistema, tenha um bom dia!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()


