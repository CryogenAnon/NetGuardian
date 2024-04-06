import socket

def extract_service_version(banner):
    service = 'Unknown'
    version = 'Unknown'
    
    # Parsing logic based on common patterns in banner responses
    if 'Server:' in banner:
        info = banner.split('Server:')[1].split()[0].strip()
        if '/' in info:
            service = info.split('/')[0].strip()
            version = info.split('/')[1].strip()
        else:
            service = info
    
    return service, version

# Input for a host specified by the user to scan for open ports
host = input("Please enter a host to scan: ")

# Scan for open ports and extract service names and versions from the banner
for port in range(20, 1025):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                service = socket.getservbyport(port)
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as service_sock:
                        service_sock.settimeout(1)
                        service_sock.connect((host, port))
                        service_sock.send(b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n')
                        banner = service_sock.recv(1024).decode()
                        service_name, service_version = extract_service_version(banner)
                        print(f'Port {port}: Open + ({service_name} - {service_version})')
                except (socket.timeout, socket.error):
                    print(f'Port {port}: Open + ({service} - Unknown version)')
    except (socket.timeout, socket.error):
        pass