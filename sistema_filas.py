import json  # biblioteca para guardar os dados num ficheiro
import os  # biblioteca para verificar se o ficheiro existe

#Nome do ficheiro onde vamos guardar
FICHEIRO = "utentes.json"

#Lista onde guardamos os utentes
fila = []
#Contador da senha
senha_atual = 0
#Contador de quantos ja foram atendidos
total_atendidos = 0

#Guarda a fila e os contadores no ficheiro utentes.json
def guardar():
    dados = {"fila": fila, "senha": senha_atual, "atendidos": total_atendidos}
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


#Quando o programa abre, vai buscar os dados que estavam guardados
def carregar():
    global fila, senha_atual, total_atendidos
    if os.path.exists(FICHEIRO):  # so carrega se o ficheiro existir
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)  # le o ficheiro
                fila = dados["fila"]
                senha_atual = dados["senha"]
                total_atendidos = dados["atendidos"]
            except:
                pass  # se o ficheiro estiver vazio, ignora e comeca do zero

#Carrega logo no inicio, antes de mostrar o menu
carregar()

#Funcao para registar utente
def registar():
    global senha_atual
    nome = input("Nome do utente: ")
    if nome == " ":
        print("Nome nao pode ficar vazio.")
        return

    idade = input("Idade: ")

    print("1 - Clinica Geral | 2 - Pediatria | 3 - Maternidade | 4 - Urgencia")
    servico = input("Escolha o servico: ")

    if servico == "1":
        sala, medico = "Sala 1", "Dr. Afonso Orlando"
    elif servico == "2":
        sala, medico = "Sala 2", "Dra. Kassako Madia"
    elif servico == "3":
        sala, medico = "Sala 3", "Dra. Langa Maria"
    else:
        sala, medico = "Sala 4", "Dr. Matondo Mauricio"

    print("1 - Emergencia | 2 - Gravida | 3 - Idoso | 4 - Deficiencia | 5 - Normal")
    prioridade = input("Escolha a prioridade: ")

    if prioridade == "1":
        nivel, texto = 1, "EMERGENCIA"
    elif prioridade == "2":
        nivel, texto = 2, "GRAVIDA"
    elif prioridade == "3":
        nivel, texto = 3, "IDOSO"
    elif prioridade == "4":
        nivel, texto = 4, "DEFICIENCIA"
    else:
        nivel, texto = 5, "NORMAL"

    senha_atual += 1

    utente = {
        "senha": senha_atual,
        "nome": nome,
        "idade": idade,
        "sala": sala,
        "medico": medico,
        "nivel": nivel,
        "prioridade": texto
    }
    fila.append(utente)
    guardar()  # guarda logo depois de registar

    print(f"\nSenha {senha_atual:03d} emitida para {nome}")
    print(f"Vai para {sala} - Medico: {medico} - Prioridade: {texto}\n")

#Funcao para mostrar a fila ja ordenada
def mostrar_fila():
    print("\n--- FILA DE ESPERA ---")
    if len(fila) == 0:
        print("Nenhum utente a espera.")
        return
    # Ordena: primeiro por nivel, depois por senha
    ordenada = sorted(fila, key=lambda u: (u["nivel"], u["senha"]))
    for u in ordenada:
        print(f"Senha {u['senha']:03d} | {u['nome']} | {u['prioridade']} | {u['sala']} | {u['medico']}")
    print(f"\nTotal a espera: {len(fila)} | Ja atendidos hoje: {total_atendidos}")

#Funcao para chamar o proximo
def chamar():
    global total_atendidos
    if len(fila) == 0:
        print("Fila vazia.")
        return
    proximo = sorted(fila, key=lambda u: (u["nivel"], u["senha"]))[0]
    print(f"\nA CHAMAR: Senha {proximo['senha']:03d} - {proximo['nome']} -> {proximo['sala']}")
    fila.remove(proximo)
    total_atendidos += 1  # aumenta o contador de atendidos
    guardar()  # guarda de novo, para nao perder

#Funcao NOVA: consultar pela senha
def consultar():
    numero = input("Digite o numero da senha: ")
    try:
        numero = int(numero)  # tenta transformar em numero
    except:
        print("Senha invalida.")
        return
    for u in fila:  # procura na fila
        if u["senha"] == numero:
            print(f"\nEncontrado: {u['nome']} | Idade: {u['idade']} | {u['prioridade']} | {u['sala']} | {u['medico']}")
            return
    print("Utente nao encontrado na fila. Pode ja ter sido atendido.")
medicos = []
atendidos = []

def eliminar_utente():
    if not fila:
        print("Nenhum utente na fila.")
        return
    mostrar_fila()
    senha = input("Digite a senha do utente a eliminar: ")
    for u in fila:
        if str(u['senha']) == str(senha):
            fila.remove(u)
            print(f"Utente {u['nome']} eliminado!")
            return
    print("Senha não encontrada.")

def editar_utente():
    if not fila:
        print("Nenhum utente na fila.")
        return
    mostrar_fila()
    senha = input("Digite a senha do utente a editar: ")
    for u in fila:
        if str(u['senha']) == str(senha):
            print(f"A editar: {u['nome']} - Deixe em branco para não alterar")
            novo_nome = input("Novo nome: ")
            if novo_nome:
                u['nome'] = novo_nome
            nova_idade = input("Nova idade: ")
            if nova_idade:
                u['idade'] = nova_idade
            print("Utente actualizado!")
            return
    print("Senha não encontrada.")

def ver_todos_utentes():
    print("\n--- TODOS OS UTENTES ---")
    print("NA FILA (Não atendidos):")
    if not fila:
        print("Nenhum na fila.")
    else:
        for u in fila:
            print(f"Senha: {u['senha']} | {u['nome']} | Idade: {u['idade']} | Prioridade: {u['prioridade']} | NÃO ATENDIDO")
    print("\nJÁ ATENDIDOS:")
    if not atendidos:
        print("Nenhum atendido ainda.")
    else:
        for u in atendidos:
            print(f"Senha: {u['senha']} | {u['nome']} | ATENDIDO")
    print("------------------------")

def relatorios():
    print("\n--- RELATÓRIO ---")
    print(f"Na fila (não atendidos): {len(fila)}")
    print(f"Já atendidos: {len(atendidos)}")
    print(f"Total: {len(fila) + len(atendidos)}")
    print(f"Total de médicos: {len(medicos)}")
    ver_todos_utentes()

def registar_medico():
    print("\n--- REGISTAR MÉDICO ---")
    nome = input("Nome do médico: ")
    especialidade = input("Especialidade: ")
    telefone = input("Telefone: ")
    medicos.append({'nome': nome, 'especialidade': especialidade, 'telefone': telefone})
    print(f"Médico {nome} registado!")

def ver_medicos():
    if not medicos:
        print("Nenhum médico registado.")
        return
    print("\n--- MÉDICOS ---")
    for i, m in enumerate(medicos, 1):
        print(f"{i}. {m['nome']} | {m['especialidade']} | Tel: {m['telefone']}")

#Menu principal
while True:
    print("\n===== HOSPITAL GERAL DO UIGE =====")
    print("1 - Registar utente")
    print("2 - Ver fila")
    print("3 - Chamar proximo")
    print("4 - Consultar pela senha")
    print("5 - Eliminar utente")
    print("6 - Editar utente")
    print("7 - Ver todos os utentes")
    print("8 - Relatórios")
    print("9 - Registar médico")
    print("10 - Ver médicos")
    print("0 - Sair")
    opcao = input("Escolha: ")

    if opcao == "1":
        registar()
    elif opcao == "2":
        mostrar_fila()
    elif opcao == "3":
        chamar()
    elif opcao == "4":
        consultar()
    elif opcao == "5":
        eliminar_utente()
    elif opcao == "6":
        editar_utente()
    elif opcao == "7":
        ver_todos_utentes()
    elif opcao == "8":
        relatorios()
    elif opcao == "9":
        registar_medico()
    elif opcao == "10":
        ver_medicos()

    elif opcao == "0":
        print("A sair... Obrigado!")
        break
    else:
        print("Opcao invalida.")

