import socket
import os
import threading

FILES_DIR = "_FILES"
USERS_FILE = "users.txt"

def load_users(filename):
    users = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                username, password = line.strip().split(":")
                users[username] = password
    except FileNotFoundError:
        print(f"Arquivo de usuários '{filename}' não encontrado. Nenhum usuário carregado.")
    return users

def handle_client(client_socket, address):
    print(f"[+] Conexão recebida de {address[0]}:{address[1]}")

    authenticated = False
    while not authenticated:
        client_socket.send("Usuário: ".encode())
        username = client_socket.recv(1024).decode().strip()
        print(f"Usuário recebido: {username}")

        if username in USERS:
            print("Usuário encontrado!")
            client_socket.send("Senha: ".encode())
            password = client_socket.recv(1024).decode().strip()

            if USERS[username] == password:
                authenticated = True
                client_socket.send("Autenticado!\n".encode())

                user_dir = os.path.join(FILES_DIR, username)
                if not os.path.exists(user_dir):
                    os.makedirs(user_dir)

                while True:
                    try:
                        command = client_socket.recv(1024).decode().strip()
                        if not command:
                            break

                        parts = command.split()
                        action = parts[0]

                        if action == "CREATE":
                            filename = parts[1]
                            filepath = os.path.join(user_dir, filename)
                            try:
                                with open(filepath, "w") as f:
                                    pass
                                client_socket.send(f"Arquivo {filename} criado com sucesso.\n".encode())
                            except Exception as e:
                                client_socket.send(f"Erro ao criar arquivo: {e}\n".encode())

                        elif action == "ADD":
                            filename = parts[1]
                            filepath = os.path.join(user_dir, filename)
                            line = " ".join(parts[2:])
                            try:
                                with open(filepath, "a") as f:
                                    f.write(line + "\n")
                                client_socket.send(f"Linha adicionada ao arquivo {filename}.\n".encode())
                            except FileNotFoundError:
                                client_socket.send(f"Arquivo {filename} não encontrado.\n".encode())
                            except Exception as e:
                                client_socket.send(f"Erro ao adicionar linha: {e}\n".encode())

                        elif action == "LIST":
                            try:
                                files = os.listdir(user_dir)
                                file_list = "[ " + ", ".join(files) + " ]" if files else "[]"
                                client_socket.send(f"Arquivos disponíveis: {file_list}\n".encode())
                            except FileNotFoundError:
                                client_socket.send("Diretório de arquivos não encontrado.\n".encode())

                        elif action == "DELETE":
                            filename = parts[1]
                            filepath = os.path.join(user_dir, filename)
                            try:
                                os.remove(filepath)
                                client_socket.send(f"Arquivo {filename} deletado com sucesso.\n".encode())
                            except FileNotFoundError:
                                client_socket.send(f"Arquivo {filename} não encontrado.\n".encode())
                            except Exception as e:
                                client_socket.send(f"Erro ao deletar arquivo: {e}\n".encode())

                        elif action == "EXIT":
                            break
                        else:
                            client_socket.send("Comando inválido.\n".encode())

                    except Exception as e:
                        print(f"Erro: {e}")
                        break
            else:
                client_socket.send("Senha incorreta!\n".encode())
        else:
            client_socket.send("Usuário não encontrado!\n".encode())


    print(f"[+] Conexão encerrada com {address[0]}:{address[1]}")
    client_socket.close()

def main():
    HOST = "127.0.0.1"
    PORT = 65432

    global USERS
    USERS = load_users(USERS_FILE)

    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] Servidor ouvindo em {HOST}:{PORT}")

        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    main()