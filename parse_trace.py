import re

def parse_curl_trace(trace):
    results = {
        "metodo": "Não encontrado",
        "host": "Não encontrado",
        "status_code": "Não encontrado",
        "ip_remoto": "Não encontrado",
        "headers": {}
    }
    
    main_headers = ["Location", "Content-Type", "Server", "Content-Length", "Date"]

    ip_match = re.search(r"Connected to \S+ \(([^)]+)\)", trace)
    if ip_match:
        results["ip_remoto"] = ip_match.group(1)

    lines = trace.splitlines()
    for i, line in enumerate(lines):
        
        # Limpar o prefixo de offset hexadecimal do curl (ex: "0000: ")
        clean_line = re.sub(r"^[0-9a-fA-F]+:\s*", "", line).strip()
        
        if "GET" in clean_line or "POST" in clean_line:
            metodo_match = re.match(r"^([A-Z]+)\s", clean_line)
            if metodo_match:
                results["metodo"] = metodo_match.group(1)
        
        if clean_line.startswith("Host:"):
            results["host"] = clean_line.split(":", 1)[1].strip()
            
        if "HTTP/1." in clean_line or "HTTP/2" in clean_line:
            status_match = re.search(r"HTTP/\d\.\d\s+(\d{3})", clean_line)
            if status_match:
                results["status_code"] = status_match.group(1)

        for h in main_headers:
            if clean_line.startswith(f"{h}:"):
                valor = clean_line.split(":", 1)[1].strip()
                results["headers"][h] = valor

    return results

with open('./trace.txt', 'r') as trace_file:
    curl_trace_output = trace_file.read()
    parsed = parse_curl_trace(curl_trace_output)

    print(f"Método HTTP:  {parsed['metodo']}")
    print(f"Host:        {parsed['host']}")
    print(f"Status Code: {parsed['status_code']}")
    print(f"IP Remoto:   {parsed['ip_remoto']}\n")

    print("Headers Principais da Resposta:")
    for header, valor in parsed["headers"].items():
        print(f"   - {header}: {valor}")
