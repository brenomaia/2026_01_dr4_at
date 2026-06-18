import dns.resolver

def resolve_dns(dominio):
    types = ['A', 'AAAA']
    
    for type in types:
        try:
            resp = dns.resolver.resolve(dominio, type)
            for ip in resp:
                print(f'Tipo: {type} \nIp: {ip}')
                
        except Exception as e:
            print(f"Error during resolve: {e}")
        
        print()

resolve_dns("google.com")