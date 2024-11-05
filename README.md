# TRABALHO-SOCKET: Servidor TCP com Autenticação e Gerenciamento de Arquivos

Este projeto implementa um servidor TCP em Python que permite aos clientes realizar operações básicas em arquivos de texto, incluindo criar, adicionar linhas, listar e excluir arquivos. O servidor inclui autenticação de usuário baseada em arquivo e organiza os arquivos dos usuários em diretórios individuais.

## Estrutura do Projeto

* **`client/client.py`:** Contém o código do cliente.
* **`server/server.py`:** Contém o código do servidor.
* **`server/_FILES/`:** Diretório onde os arquivos dos usuários são armazenados.  Criado automaticamente se não existir.
* **`server/users.txt`:** Arquivo que armazena os nomes de usuário e senhas.


## Como Executar

1. **Configurar o ambiente:**
    * Certifique-se de ter o Python 3 instalado.
2. **Criar o arquivo de usuários:**
    * Crie o arquivo `users.txt` dentro do diretório `server`.
    * Adicione usuários e senhas, um por linha, no formato `usuario:senha`.  Exemplo:
        ```
        usuario1:senha123
        usuario2:senha456
        ```
3. **Iniciar o servidor:**
    * Abra um terminal, navegue até o diretório `server` e execute: `python server.py`
4. **Iniciar o cliente:**
    * Abra outro terminal, navegue até o diretório `client` e execute: `python client.py`

## Uso do Cliente

Após se conectar, o cliente será solicitado a inserir seu nome de usuário e senha. Após a autenticação bem-sucedida, o cliente pode usar os seguintes comandos:

* **`CREATE <nome_do_arquivo>`:** Cria um novo arquivo.
* **`ADD <nome_do_arquivo> <texto>`:** Adiciona uma linha de texto ao final do arquivo especificado.
* **`LIST`:** Lista os arquivos disponíveis no diretório do usuário.
* **`DELETE <nome_do_arquivo>`:** Exclui o arquivo especificado.
* **`EXIT`:** Encerra a conexão com o servidor.

## Detalhes de Implementação

* **Autenticação:** O servidor usa um arquivo de texto (`users.txt`) para armazenar as credenciais do usuário.
* **Diretórios por usuário:**  Cada usuário tem um diretório dedicado dentro do diretório `_FILES` para armazenar seus arquivos.
* **Multithreading:** O servidor usa multithreading para lidar com múltiplas conexões de clientes simultaneamente.
* **Tratamento de erros:** O servidor inclui tratamento básico de erros para lidar com arquivos inexistentes e outros erros.


## Melhorias Futuras

* **Criptografia de senha:** Armazenar senhas de forma mais segura usando hashing.
* **Tratamento de erros mais robusto:**  Melhorar o tratamento de erros no servidor e no cliente.
* **Interface gráfica do usuário (GUI):** Desenvolver uma interface gráfica para o cliente.
* **Recursos adicionais:** Adicionar mais comandos, como renomear arquivos, ler o conteúdo de um arquivo, etc.



## Autor

Anderson Gomes