from scapy.all import sniff, TCP, IP

PORT = 12345

def process_packet(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        sport = packet[TCP].sport
        dport = packet[TCP].dport
        
        if packet[TCP].payload:
            payload = bytes(packet[TCP].payload).decode('utf-8', errors='ignore')
            
            if payload:
                print("-" * 50)
                if dport == PORT:
                    print(f"[CLIENTE -> SERVIDOR] ({ip_src}:{sport} -> {ip_dst}:{dport})")
                elif sport == PORT:
                    print(f"[SERVIDOR -> CLIENTE] ({ip_src}:{sport} -> {ip_dst}:{dport})")
                
                print(f"Conteúdo: {payload}")

print(f"Iniciando captura de tráfego na porta {PORT}...")
print("Pressione Ctrl+C para parar.")


sniff(iface="lo0", filter=f"tcp port {PORT}", prn=process_packet, store=0)