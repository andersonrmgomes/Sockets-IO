import sys
import os
import socket

# Adiciona o diretório pai (TRABALHO-SOCKET) ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def display_menu():
    print("\n--- Menu ---")
    print("1. CREATE <nome_do_arquivo>")
    print("2. ADD <nome_do_arquivo> <texto>")
    print("3. LIST")
    print("4. DELETE <nome_do_arquivo>")
    print("5. BACKUP")
    print("6. EXIT")
    print("------------")


def get_command():
    while True:
        display_menu()
        choice = input("Escolha uma opção: ")

        try:
            choice = int(choice)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Opção inválida. Escolha um número entre 1 e 6.")
        except ValueError:
            print("Entrada inválida. Digite um número.")


def get_filename():
    while True:
        filename = input("Nome do arquivo: ")
        if filename:
            return filename
        else:
            print("Nome de arquivo inválido. Tente novamente.")


def get_text_to_add():
    text = input("Texto a adicionar: ")
    return text


def main():
    HOST = "127.0.0.1"
    PORT = 65432

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            username = input("Usuário: ")
            client_socket.send(username.encode())

            authenticated = False
            while not authenticated:
                password_request = client_socket.recv(1024).decode()
                print(password_request, end="")

                if "Usuário não encontrado" in password_request:
                    break

                if "Senha:" in password_request:
                    password = input()
                    client_socket.send(password.encode())

                    auth_response = client_socket.recv(1024).decode()
                    print(auth_response)
                    if "Autenticado" in auth_response:
                        authenticated = True
                elif "Senha incorreta" in password_request:
                    pass  # Continua no loop se a senha estiver incorreta

            if authenticated:
                while True:
                    choice = get_command()

                    if choice == 1:
                        filename = get_filename()
                        command = f"CREATE {filename}"
                    elif choice == 2:
                        filename = get_filename()
                        text = get_text_to_add()
                        command = f"ADD {filename} {text}"
                    elif choice == 3:
                        command = "LIST"
                    elif choice == 4:
                        filename = get_filename()
                        command = f"DELETE {filename}"
                    elif choice == 5:  # Comando BACKUP
                        command = "BACKUP"
                        client_socket.send(command.encode())
                        response = client_socket.recv(1024).decode()
                        print(response)
                        continue  # Volta ao menu
                    elif choice == 6:  # Comando EXIT
                        command = "EXIT"
                        client_socket.send(command.encode())
                        break  # Sai do loop

                    client_socket.send(command.encode())

                    response = client_socket.recv(1024).decode()
                    print(response)


    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Certifique-se de que o servidor está em execução.")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()