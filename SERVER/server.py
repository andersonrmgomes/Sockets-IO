# server/server.py
import socket
import os
import threading

FILES_DIR = "_FILES"  # Define o diretório de arquivos

def handle_client(client_socket, address):
    print(f"[+] Conexão recebida de {address[0]}:{address[1]}")

    authenticated = False
    while not authenticated:
        client_socket.send("Senha: ".encode())
        password = client_socket.recv(1024).decode().strip()
        if password == "senha123":
            authenticated = True
            client_socket.send("Autenticado!\n".encode())
        else:
            client_socket.send("Senha incorreta!\n".encode())

    while True:
        try:
            command = client_socket.recv(1024).decode().strip()
            if not command:
                break

            parts = command.split()
            action = parts[0]

            if action == "CREATE":
                filename = os.path.join(FILES_DIR, parts[1])
                try:
                    with open(filename, "w") as f:
                        pass
                    client_socket.send(f"Arquivo {parts[1]} criado com sucesso.\n".encode())
                except Exception as e:
                    client_socket.send(f"Erro ao criar arquivo: {e}\n".encode())

            elif action == "ADD":
                filename = os.path.join(FILES_DIR, parts[1])
                line = " ".join(parts[2:])
                try:
                    with open(filename, "a") as f:
                        f.write(line + "\n")
                    client_socket.send(f"Linha adicionada ao arquivo {parts[1]}.\n".encode())
                except FileNotFoundError:
                    client_socket.send(f"Arquivo {parts[1]} não encontrado.\n".encode())
                except Exception as e:
                    client_socket.send(f"Erro ao adicionar linha: {e}\n".encode())

            elif action == "LIST":
                try:
                    files = os.listdir(FILES_DIR)
                    file_list = "[ " + ", ".join(files) + " ]" if files else "[]"
                    client_socket.send(f"Arquivos disponíveis: {file_list}\n".encode())
                except FileNotFoundError:
                    client_socket.send("Diretório de arquivos não encontrado.\n".encode())


            elif action == "DELETE":
                filename = os.path.join(FILES_DIR, parts[1])
                try:
                    os.remove(filename)
                    client_socket.send(f"Arquivo {parts[1]} deletado com sucesso.\n".encode())
                except FileNotFoundError:
                    client_socket.send(f"Arquivo {parts[1]} não encontrado.\n".encode())
                except Exception as e:
                    client_socket.send(f"Erro ao deletar arquivo: {e}\n".encode())

            elif action == "EXIT":
                break
            else:
                client_socket.send("Comando inválido.\n".encode())

        except Exception as e:
            print(f"Erro: {e}")
            break

    print(f"[+] Conexão encerrada com {address[0]}:{address[1]}")
    client_socket.close()


def main():
    HOST = "127.0.0.1"
    PORT = 65432

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