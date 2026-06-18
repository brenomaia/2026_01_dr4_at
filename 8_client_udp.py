import socket

HOST = "localhost"
PORT = 12345
BUF_SIZE = 1024
TIMEOUT_IN_SECONDS = 5

def simulate_client(client_id, content, max_attempts=3):
    attempt = 1
    success = None
    while attempt <= max_attempts:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.settimeout(TIMEOUT_IN_SECONDS)
            
            client_socket.connect((HOST, PORT))
            print(f"[Cliente {client_id}] Conectado ao servidor!")
            
            message = f"Mensagem enviada na tentativa {attempt}"
            
            print(f"[Cliente {client_id}] Enviando tentativa {attempt}: '{message}'")
            client_socket.sendall(message.encode('utf-8'))
            
            resp, addr = client_socket.recvfrom(BUF_SIZE)
            print(f"[Cliente {client_id}] Resposta recebida: '{resp.decode('utf-8')}'")
            success = True
            break

        except TimeoutError as e:
            attempt += 1
            print(f'[Cliente {client_id}] sofreu timeout.')

        except Exception as e:
            print(f"[Cliente {client_id}] Erro: {e}")
        finally:
            client_socket.close()
            print(f"[Cliente {client_id}] Conexão encerrada.")

    if success:
        print(f'Mensagem enviada com sucesso na tentativa {attempt}')
    else:
        print(f'Não foi possível enviar a mensagem com sucesso após {max_attempts} tentativas.')

simulate_client(1, "minha mensagem")