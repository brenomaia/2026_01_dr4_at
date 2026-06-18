import socket

HOST = "localhost"
PORT = 12345
BUF_SIZE = 1024

def handle_client(conn, addr):
    print(f'Nova conexão com {addr}')

    try:
        with conn:
            while True:
                incoming_data = conn.recv(BUF_SIZE)
                if not incoming_data:
                    break
                print(f"Recebido: {incoming_data.decode('utf-8')}")
                conn.sendall(b"Recebido com sucesso.")
    except Exception as e:
        print(f'Erro ao lidar com cliente {addr}: {e}')
    finally:
        print(f'Cliente {addr} desconectou.')
                

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    try:
        print("Iniciando servidor...")
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor iniciado em {HOST}:{PORT}")


        while True:
            conn, addr = server.accept()
            print(f'Cliente {addr} conectado')

            while True:
                incoming_data = conn.recv(BUF_SIZE)
                if not incoming_data:
                    break

                incoming_message = incoming_data.decode('utf-8')
                
                split_message = incoming_message.split("\n", 1)
                size_part, message = split_message[0], split_message[1]
                size = int(size_part.split("Tamanho: ")[1])

                if size != len(message):
                    print(f'Cliente mandou mensagem de tamanho diferente. \nTamanho especificado: {size}\n Tamanho real: {len(message)}')
                    conn.sendall("Mensagem inválida".encode('utf-8'))
                else:
                    print("Tamanho correto! Mensagem processada.")
                    conn.sendall("Mensagem processada com sucesso.".encode('utf-8'))


    except Exception as e:
        print(f'falha {e}')
    finally:
        server.close()