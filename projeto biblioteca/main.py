from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from datetime import datetime
from tabulate import tabulate
from datetime import datetime, timedelta

username = input("Digite seu username: ")
password = input("Digite sua password: ")


encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# URI para conexão com o MongoDB
uri = "mongodb+srv://gabimafuze4:min09031993@cluster0.uz8iwno.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client['Cluster0']

# Coleções
livros_collection = db['livros']
usuarios_collection = db['usuarios']
emprestimos_collection = db['emprestimos']

# Funções CRUD para Livros
def adicionar_livro():
    isbn = input("Digite o ISBN do livro: ")

    # Verifica se já existe um livro com o mesmo ISBN
    livro_existente = livros_collection.find_one({"_id": isbn})

    if livro_existente:
        print(f"Já existe um livro com o ISBN {isbn}.")
        return

    titulo = input("Digite o título do livro: ")
    autor = input("Digite o nome do autor: ")
    genero = input("Digite o gênero do livro: ")
    ano = input("Digite o ano de publicação: ")
    editora = input("Digite a editora do livro: ")
    edicao = input("Digite a edição do livro: ")
    exemplares = int(input("Digite a quantidade de exemplares disponíveis: "))

    livro = {
        "_id": isbn,  # ISBN como chave primária
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "ano": ano,
        "editora": editora,
        "edicao": edicao,
        "exemplares_disponiveis": exemplares
    }

    livros_collection.insert_one(livro)
    print("Livro adicionado com sucesso!")


def atualizar_livro():
    isbn = input("Digite o ISBN do livro que deseja atualizar: ")

    # Verifica se o livro existe
    livro_existente = livros_collection.find_one({"_id": isbn})

    if not livro_existente:
        print(f"Nenhum livro encontrado com o ISBN {isbn}.")
        return

    print("Livro encontrado:")
    print(livro_existente)

    # Solicita novos dados para atualização
    titulo = input("Digite o novo título do livro (enter p/ não alterar): ")
    autor = input("Digite o novo nome do autor (enter p/ não alterar): ")
    genero = input("Digite o novo gênero do livro (enter p/ não alterar): ")
    ano = input("Digite o novo ano de publicação (enter p/ não alterar): ")
    editora = input("Digite a nova editora do livro (enter p/ não alterar): ")
    edicao = input("Digite a nova edição do livro (enter p/ não alterar): ")
    exemplares = input("Digite a nova quantidade de exemplares disponíveis (enter p/ não alterar): ")

    # Cria um dicionário para atualizar os dados
    atualizacoes = {}
    if titulo:
        atualizacoes["titulo"] = titulo
    if autor:
        atualizacoes["autor"] = autor
    if genero:
        atualizacoes["genero"] = genero
    if ano:
        atualizacoes["ano"] = ano
    if editora:
        atualizacoes["editora"] = editora
    if edicao:
        atualizacoes["edicao"] = edicao
    if exemplares:
        atualizacoes["exemplares_disponiveis"] = int(exemplares)

    # Atualiza o livro no banco de dados
    if atualizacoes:
        livros_collection.update_one({"_id": isbn}, {"$set": atualizacoes})
        print("Livro atualizado com sucesso!")
    else:
        print("Nenhuma alteração foi feita.")


def deletar_livro():
    isbn = input("Digite o ISBN do livro que deseja deletar: ")

    # Verifica se o livro existe
    livro_existente = livros_collection.find_one({"_id": isbn})

    if not livro_existente:
        print(f"Nenhum livro encontrado com o ISBN {isbn}.")
        return

    # Deleta o livro do banco de dados
    livros_collection.delete_one({"_id": isbn})
    print("Livro deletado com sucesso!")


# Funções CRUD para Usuários
def adicionar_usuario():
    cpf = input("Digite o CPF do usuário: ")
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    numero_documento = cpf  # Agora o CPF é o identificador único

    usuario = {
        "_id": cpf,
        "nome": nome,
        "email": email,
        "data_nascimento": data_nascimento,
        "numero_documento": numero_documento
    }
    usuarios_collection.insert_one(usuario)
    print(f"Usuário '{nome}' adicionado com sucesso.")

def atualizar_usuario():
    cpf = input("Digite o CPF do usuário que deseja atualizar: ")

    # Verifica se o usuário existe
    usuario_existente = usuarios_collection.find_one({"_id": cpf})

    if not usuario_existente:
        print(f"Nenhum usuário encontrado com o CPF {cpf}.")
        return

    print("Usuário encontrado:")
    print(usuario_existente)

    # Solicita novos dados para atualização
    nome = input("Digite o novo nome do usuário (enter p/ não alterar): ")
    email = input("Digite o novo e-mail do usuário (enter p/ não alterar): ")
    data_nascimento = input("Digite a nova data de nascimento (DD/MM/AAAA) (enter p/ não alterar): ")

    # Cria um dicionário para atualizar os dados
    atualizacoes = {}
    if nome:
        atualizacoes["nome"] = nome
    if email:
        atualizacoes["email"] = email
    if data_nascimento:
        atualizacoes["data_nascimento"] = data_nascimento

    # Atualiza o usuário no banco de dados
    if atualizacoes:
        usuarios_collection.update_one({"_id": cpf}, {"$set": atualizacoes})
        print("Usuário atualizado com sucesso!")
    else:
        print("Nenhuma alteração foi feita.")

def listar_usuarios():
    usuarios = list(usuarios_collection.find())
    if usuarios:
        tabela = [[usuario['_id'], usuario['nome'], usuario['email'], usuario['data_nascimento']] for usuario in usuarios]
        print(tabulate(tabela, headers=["CPF", "Nome", "Email", "Data Nascimento"], tablefmt="pretty"))
    else:
        print("Nenhum usuário cadastrado encontrado.")

# Função para registrar empréstimo
def registrar_emprestimo():
    livro_id = input("Digite o ISBN do livro: ")
    usuario_id = input("Digite o CPF do usuário: ")

    livro = livros_collection.find_one({"_id": livro_id})
    if not livro or livro['exemplares_disponiveis'] <= 0:  # Modificado para 'exemplares_disponiveis'
        print(f"Livro {livro_id} não está disponível para empréstimo.")
        return

    # Data prevista de devolução (7 dias após o empréstimo)
    data_prevista_devolucao = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    emprestimo = {
        "livro_id": livro_id,
        "usuario_id": usuario_id,
        "data_emprestimo": datetime.now().strftime("%Y-%m-%d"),
        "data_prevista_devolucao": data_prevista_devolucao,
        "data_devolucao": None
    }
    emprestimos_collection.insert_one(emprestimo)

    # Atualizar a quantidade de exemplares
    livros_collection.update_one({"_id": livro_id}, {"$set": {"exemplares_disponiveis": livro['exemplares_disponiveis'] - 1}})  # Modificado para 'exemplares_disponiveis'
    print(f"Empréstimo do livro {livro_id} registrado para o usuário {usuario_id}, com devolução prevista em {data_prevista_devolucao}.")
# Função para registrar devolução
def registrar_devolucao():
    livro_id = input("Digite o ISBN do livro: ")

    emprestimo = emprestimos_collection.find_one({"livro_id": livro_id, "data_devolucao": None})
    if not emprestimo:
        print(f"Não há empréstimo ativo para o livro {livro_id}.")
        return

    emprestimos_collection.update_one({"_id": emprestimo["_id"]}, {"$set": {"data_devolucao": datetime.now().strftime("%Y-%m-%d")}})
    livro = livros_collection.find_one({"_id": livro_id})
    livros_collection.update_one({"_id": livro_id}, {"$set": {"quantidade_disponiveis": livro['quantidade_disponiveis'] + 1}})
    print(f"Devolução do livro {livro_id} registrada com sucesso.")

# Funções de consulta e relatórios
def listar_livros_disponiveis():
    livros = list(livros_collection.find({"exemplares_disponiveis": {"$gt": 0}}))  # Modificado para 'exemplares_disponiveis'
    if livros:
        tabela = [[livro['_id'], livro['titulo'], livro['autor'], livro['genero'], livro['ano'], livro['editora'], livro['edicao'], livro['exemplares_disponiveis']] for livro in livros]
        print(tabulate(tabela, headers=["ISBN", "Título", "Autor", "Gênero", "Ano", "Editora", "Edição", "Exemplares Disponíveis"], tablefmt="pretty"))
    else:
        print("Nenhum livro disponível encontrado.")

def consultar_emprestimos_usuario():
    usuario_id = input("Digite o CPF do usuário: ")
    emprestimos = list(emprestimos_collection.find({"usuario_id": usuario_id, "data_devolucao": None}))
    if emprestimos:
        tabela = [[emprestimo['livro_id'], emprestimo['data_emprestimo'], emprestimo['data_prevista_devolucao']] for emprestimo in emprestimos]
        print(tabulate(tabela, headers=["ID Livro", "Data Empréstimo", "Data Prevista Devolução"], tablefmt="pretty"))
    else:
        print(f"Nenhum empréstimo em aberto encontrado para o usuário {usuario_id}.")

def consultar_usuarios_vencidos():
    data_atual = datetime.now().strftime("%Y-%m-%d")
    emprestimos_vencidos = list(emprestimos_collection.find({"data_devolucao": None, "data_prevista_devolucao": {"$lt": data_atual}}))
    if emprestimos_vencidos:
        tabela = [[emprestimo['usuario_id'], emprestimo['livro_id'], emprestimo['data_emprestimo']] for emprestimo in emprestimos_vencidos]
        print(tabulate(tabela, headers=["CPF Usuário", "ISBN Livro", "Data Empréstimo"], tablefmt="pretty"))
    else:
        print("Nenhum usuário com empréstimos vencidos encontrado.")

def relatorio_livros():
    livros = list(livros_collection.find())
    if livros:
        tabela = [[livro['_id'], livro['titulo'], livro['autor'], livro['genero'], livro['ano'], livro['quantidade_disponiveis']] for livro in livros]
        print(tabulate(tabela, headers=["ISBN", "Título", "Autor", "Gênero", "Ano", "Exemplares Disponíveis"], tablefmt="pretty"))
    else:
        print("Nenhum livro cadastrado encontrado.")

def relatorio_usuarios():
    usuarios = list(usuarios_collection.find())
    if usuarios:
        tabela = [[usuario['_id'], usuario['nome'], usuario['email'], usuario['data_nascimento'], usuario['numero_documento']] for usuario in usuarios]
        print(tabulate(tabela, headers=["CPF", "Nome", "Email", "Data Nascimento", "Documento"], tablefmt="pretty"))
    else:
        print("Nenhum usuário cadastrado encontrado.")

def relatorio_emprestimos():
    periodo_inicio = input("Digite a data de início (YYYY-MM-DD): ")
    periodo_fim = input("Digite a data de fim (YYYY-MM-DD): ")
    emprestimos = list(emprestimos_collection.find({"data_emprestimo": {"$gte": periodo_inicio, "$lte": periodo_fim}}))
    if emprestimos:
        tabela = [[emprestimo['livro_id'], emprestimo['usuario_id'], emprestimo['data_emprestimo'], emprestimo['data_prevista_devolucao'], emprestimo['data_devolucao'] or "Em andamento"] for emprestimo in emprestimos]
        print(tabulate(tabela, headers=["ID Livro", "CPF Usuário", "Data Empréstimo", "Data Prevista Devolução", "Data Devolução"], tablefmt="pretty"))
    else:
        print("Nenhum empréstimo encontrado nesse período.")

# Menu com submenus
def menu_livros():
    while True:
        print("\n--- Menu Livros ---")
        print("1. Adicionar Livro")
        print("2. Listar Livros Disponíveis")
        print("3. Atualizar Livro")
        print("4. Deletar Livro")
        print("5. Relatório de Livros")
        print("0. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_livro()
        elif opcao == "2":
            listar_livros_disponiveis()
        elif opcao == "3":
            atualizar_livro()
        elif opcao == "4":
            deletar_livro()
        elif opcao == "5":
            relatorio_livros()
        elif opcao == "0":
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_usuarios():
    while True:
        print("\n--- Menu Usuários ---")
        print("1. Adicionar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Consultar Empréstimos do Usuário")
        print("5. Relatório de Usuários")
        print("0. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            atualizar_usuario()
        elif opcao == "4":
            consultar_emprestimos_usuario()
        elif opcao == "5":
            relatorio_usuarios()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_emprestimos():
    while True:
        print("\n--- Menu Empréstimos ---")
        print("1. Registrar Empréstimo")
        print("2. Registrar Devolução")
        print("3. Consultar Usuários com Empréstimos Vencidos")
        print("4. Relatório de Empréstimos por Período")
        print("0. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar_emprestimo()
        elif opcao == "2":
            registrar_devolucao()
        elif opcao == "3":
            consultar_usuarios_vencidos()
        elif opcao == "4":
            relatorio_emprestimos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_principal():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Livros")
        print("2. Usuários")
        print("3. Empréstimos")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_livros()
        elif opcao == "2":
            menu_usuarios()
        elif opcao == "3":
            menu_emprestimos()
        elif opcao == "0":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu principal
menu_principal()





