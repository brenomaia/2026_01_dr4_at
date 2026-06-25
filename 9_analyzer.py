import re
from collections import defaultdict
from scapy.all import sniff, TCP, IP

LOG_FILE = 'server_log.txt'
PORT=12345
ERRORS_LIMIT = 3

# Estrutura: { '127.0.0.1': set(['/erro1', '/erro2']) }
# 'set' para registrar paths inválidos
error_history = defaultdict(int)
blocked_ips = set()

def analyze_log_file():
    global error_history, blocked_ips
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        # Se o arquivo não existe ainda, não há o que analisar
        return

    error_history.clear()

    # Regex para extrair IP e Status do formato:
    # [2026-06-25 18:52:05] IP: 127.0.0.1 | Método: GET | Endpoint: /nao-existe | Status: 404
    padrao = r"IP:\s+([\d\.]+).*Status:\s+(\d+)"

    for linha in linhas:
        match = re.search(padrao, linha)
        if match:
            ip = match.group(1)
            status = int(match.group(2))

            if status == 404:
                error_history[ip] += 1
                
                if error_history[ip] >= ERRORS_LIMIT and ip not in blocked_ips:
                    print(f"\n[ALERTA DE ANOMALIA] O IP {ip} tentou acessar paths inválidos {error_history[ip]} vezes!")
                    blocked_ips.add(ip)

def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP):
        payload = packet[TCP].payload
        if payload:
            dados_brutos = bytes(payload).decode('utf-8', errors='ignore')
            
            ip_origem = packet[IP].src
            linha_requisicao = dados_brutos.split('\r\n')[0]
            
            print(f"[Tráfego em Tempo Real] Requisição de {ip_origem} -> {linha_requisicao}")
            analyze_log_file()

def start_analyzer():
    print("=== Analisador de Tráfego HTTP e Logs Iniciado ===")
    print(f"Monitorando porta {PORT} e analisando '{LOG_FILE}'...")
    print("Pressione Ctrl+C para parar.\n")
    
    analyze_log_file()

    sniff(iface="lo0", filter=f"tcp port {PORT}", prn=process_packet, store=0)


start_analyzer()