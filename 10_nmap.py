import nmap

def local_sweep():
    nm = nmap.PortScanner()
    
    # Argumentos: -sV (Detecção de versão/serviço), -F (Varredura rápida das 100 portas mais comuns)
    target = '127.0.0.1'
    print(f"Iniciando varredura em {target}...\n")
    
    try:
        nm.scan(hosts=target, arguments='-sV -F')
    except Exception as e:
        print(f"Erro ao executar o Nmap: {e}")
        return

    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"Estado do Host: {nm[host].state()}")
        print("-" * 40)
        
        for proto in nm[host].all_protocols():
            print(f"Protocolo: {proto.upper()}")
            
            lport = nm[host][proto].keys()
            sorted_ports = sorted(lport)
            
            for port in sorted_ports:
                state = nm[host][proto][port]['state']
                name = nm[host][proto][port]['name']
                product = nm[host][proto][port].get('product', '')
                version = nm[host][proto][port].get('version', '')
                
                info_servico = f"{name} {product} {version}".strip()
                
                print(f"  Porta: {port:<6} | Estado: {state:<6} | Serviço: {info_servico}")


local_sweep()
