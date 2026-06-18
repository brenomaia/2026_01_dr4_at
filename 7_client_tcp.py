import socket
import time

HOST = "localhost"
PORT = 12345
BUF_SIZE = 1024

def simulate_client(client_id):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"[Cliente {client_id}] Conectado ao servidor!")
        
        message = f"Mensagem do Cliente {client_id}"
        with_size = f'Tamanho: {len(message)}\n{message}'
        print(f"[Cliente {client_id}] Enviando: '{message}'")
        client_socket.sendall(with_size.encode('utf-8'))
        
        resposta = client_socket.recv(BUF_SIZE)
        print(f"[Cliente {client_id}] Resposta recebida: '{resposta.decode('utf-8')}'")

        time.sleep(3)

        print(f"\n[Cliente {client_id}] Enviando mensagem de tamanho incorreto.")
        with_size = with_size + "---"
        print(f"[Cliente {client_id}] Enviando com tamanho errado: '{message}'")
        client_socket.sendall(with_size.encode('utf-8'))
        
        resposta = client_socket.recv(BUF_SIZE)
        print(f"[Cliente {client_id}] Resposta recebida: '{resposta.decode('utf-8')}'")


    except Exception as e:
        print(f"[Cliente {client_id}] Erro: {e}")
    finally:
        client_socket.close()
        print(f"[Cliente {client_id}] Conexão encerrada.")

simulate_client(1)