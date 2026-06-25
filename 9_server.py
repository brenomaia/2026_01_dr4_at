import socket
from datetime import datetime

"""
Testando com curl:
curl -H "Accept-Language: en" http://127.0.0.1:12345/home.html
curl -H "Accept-Language: en" http://127.0.0.1:12345/contato.html
"""

HOST = '127.0.0.1'
PORT = 12345
LOG_FILE = 'server_log.txt'

PAGES = {
    '/home.html': {
        'pt': '<h1>Bem-vindo à Página Inicial do meu AT!</h1>',
        'en': '<h1>Welcome to the Assessment Home Page!</h1>'
    },
    '/contato.html': {
        'pt': '<h1>Entre em contato: contato@email.com</h1>',
        'en': '<h1>Contact us: contact@email.com</h1>'
    }
}

def log_request(ip, method, endpoint, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] IP: {ip} | Método: {method} | Endpoint: {endpoint} | Status: {status}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)

def build_http_response(status_code, status_text, body):
    response_body = body.encode('utf-8')
    response_headers = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return response_headers.encode('utf-8') + response_body

def parse_request(request_text):
    lines = request_text.split('\r\n')
    if not lines or len(lines[0].split()) < 3:
        return None, None, None

    # Extrai a Request Line (ex: GET /home.html HTTP/1.1)
    method, endpoint, _ = lines[0].split()
    
    # Extrai headers relevantes
    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip().lower()] = value.strip()
            
    return method, endpoint, headers

def handle_client(client_socket, client_address):
    ip = client_address[0]
    try:
        request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
        if not request_data:
            return

        method, endpoint, headers = parse_request(request_data)

        if method != 'GET':
            response = build_http_response(405, "Method Not Allowed", "<h1>405 Method Not Allowed</h1>")
            client_socket.sendall(response)
            log_request(ip, method, endpoint, 405)
            return

        if endpoint in PAGES:
            accept_language = headers.get('accept-language', 'pt')
            lang = 'en' if accept_language.startswith('en') else 'pt'
            
            body = PAGES[endpoint][lang]
            response = build_http_response(200, "OK", body)
            status_code = 200
        else:
            body = "<h1>404 Not Found</h1>"
            response = build_http_response(404, "Not Found", body)
            status_code = 404

        client_socket.sendall(response)
        
        log_request(ip, method, endpoint, status_code)

    except Exception as e:
        print(f"Erro ao processar requisição: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Servidor HTTP rodando em http://{HOST}:{PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
            
    except KeyboardInterrupt:
        print("\nDesligando o servidor...")
    finally:
        server_socket.close()

start_server()