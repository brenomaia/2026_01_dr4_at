import socket 
import random

HOST = "localhost"
PORT = 12345
BUF_SIZE = 1024

socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def create_udp_socket_server(server):
    print("Iniciando servidor...")
    try:
        server.bind((HOST, PORT))

        while True:
            incoming_data, client_addr = server.recvfrom(1024)
            print(f"Recebido: {incoming_data.decode('utf-8')}")

            send_with_loss(server, client_addr)
    
    except Exception as e:
        print(f"Falha: {e}")
        print(e)
    finally:
        server.close()


def send_with_loss(conn, addr):
    rand = random.randint(1, 10)
    is_sent = rand <= 5
    if is_sent:
        print('Enviando mensagem de recebimento.')
        conn.sendto(b'Recebido com sucesso', addr)
        return
    
    print('Mensagem de recebimento não foi enviada.')


create_udp_socket_server(socket_udp)