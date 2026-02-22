import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


cursor = conexao.cursor()


def adicionar_tarefa(nome_tarefa):
    sql = "INSERT INTO tarefas (nome, completada) VALUES (%s, %s)"
    valores = (nome_tarefa, False)
    cursor.execute(sql, valores)
    conexao.commit()
    print(f"A tarefa '{nome_tarefa}' foi adicionada com sucesso!")


def ver_tarefas():
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()

    print("\nLista de tarefas:")
    for indice, tarefa in enumerate(tarefas, start=1):
        status = "✓" if tarefa[2] else " "
        print(f"{indice}. [{status}] {tarefa[1]}")

    return tarefas


def atualizar_nome_tarefa(id_tarefa, novo_nome):
    sql = "UPDATE tarefas SET nome = %s WHERE id = %s"
    cursor.execute(sql, (novo_nome, id_tarefa))
    conexao.commit()
    print("Tarefa atualizada com sucesso!")


def completar_tarefa(id_tarefa):
    sql = "UPDATE tarefas SET completada = TRUE WHERE id = %s"
    cursor.execute(sql, (id_tarefa,))
    conexao.commit()
    print("Tarefa marcada como completada!")


def deletar_tarefas_completadas():
    cursor.execute("SELECT COUNT(*) FROM tarefas WHERE completada = TRUE")
    quantidade = cursor.fetchone()[0]

    if quantidade > 0:
        cursor.execute("DELETE FROM tarefas WHERE completada = TRUE")
        conexao.commit()
        print(f"{quantidade} tarefa(s) concluída(s) foram deletadas com sucesso!")

    else:
        print("Não há tarefas concluídas.")
        escolha = input("Deseja deletar uma tarefa mesmo assim? (s/n): ").lower()

        if escolha == "s":
            tarefas = ver_tarefas()

            if not tarefas:
                print("Não há tarefas para deletar.")
                return

            try:
                indice_usuario = int(input("Digite o número da tarefa que deseja deletar: "))

                if indice_usuario < 1 or indice_usuario > len(tarefas):
                    print("Número inválido.")
                    return

                id_real = tarefas[indice_usuario - 1][0]

                cursor.execute("DELETE FROM tarefas WHERE id = %s", (id_real,))
                conexao.commit()
                print("Tarefa deletada com sucesso!")

            except ValueError:
                print("Digite um número válido.")

        else:
            print("Operação cancelada.")


while True:
    print("\nMenu do Gerenciador de tarefas: ")
    print("1. Adicionar tarefa")
    print("2. Ver tarefas")
    print("3. Atualizar tarefa")
    print("4. Completar tarefa")
    print("5. Deletar tarefas completadas")
    print("6. Sair")

    try:
        escolha = int(input("Digite sua escolha: "))
    except ValueError:
        print("Digite um número válido.")
        continue

    if escolha == 1:
        nome_tarefa = input("Digite a tarefa que deseja adicionar: ")
        adicionar_tarefa(nome_tarefa)

    elif escolha == 2:
        ver_tarefas()

    elif escolha == 3:
        tarefas = ver_tarefas()

        if not tarefas:
            print("Não há tarefas cadastradas.")
        else:
            try:
                indice_usuario = int(input("Digite o número da tarefa que deseja atualizar: "))

                if indice_usuario < 1 or indice_usuario > len(tarefas):
                    print("Número inválido.")
                    continue

                id_real = tarefas[indice_usuario - 1][0]
                novo_nome = input("Digite o novo nome da tarefa: ")
                atualizar_nome_tarefa(id_real, novo_nome)

            except ValueError:
                print("Digite um número válido.")

    elif escolha == 4:
        tarefas = ver_tarefas()

        if not tarefas:
            print("Não há tarefas cadastradas.")
        else:
            try:
                indice_usuario = int(input("Digite o número da tarefa que deseja completar: "))

                if indice_usuario < 1 or indice_usuario > len(tarefas):
                    print("Número inválido.")
                    continue

                id_real = tarefas[indice_usuario - 1][0]
                completar_tarefa(id_real)

            except ValueError:
                print("Digite um número válido.")

    elif escolha == 5:
        deletar_tarefas_completadas()
        ver_tarefas()

    elif escolha == 6:
        break

cursor.close()
conexao.close()
