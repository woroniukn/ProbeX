import socket
import requests

# socket: Used for low-level network communication (connecting to ports).
# requests: Used for making HTTP requests (web scanning).

def scan_ports(target, ports):
    print(f"\n[+] Scanning ports on {target}")
    open_ports = []

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"[OPEN] Port {port}")
                open_ports.append(port)
            sock.close()
        except:
            pass

    return open_ports

# Scans a range of ports on a target (IP or domain) to find which ones are open.

def grab_banner(target, port):
    try:
        if port in [80, 8000, 8080]:
            import requests
            url = f"http://{target}:{port}"
            r = requests.get(url, timeout=3)
            server = r.headers.get("Server", "Unknown")
            print(f"[HTTP] Port {port}: Server = {server}")
        else:
            sock = socket.socket()
            sock.settimeout(2)
            sock.connect((target, port))
            banner = sock.recv(1024).decode().strip()
            print(f"[BANNER] Port {port}: {banner}")
            sock.close()
    except:
        print(f"[BANNER] Port {port}: Unable to retrieve")

# Attempts to identify the service running on an open port.

def check_headers(url):
    print(f"\n[+] Checking security headers for {url}")
    try:
        response = requests.get(url, timeout=5)

        headers = response.headers

        for header in [
            "X-Frame-Options",
            "X-XSS-Protection",
            "Content-Security-Policy",
            "Strict-Transport-Security"
        ]:
            if header in headers:
                print(f"[OK] {header}")
            else:
                print(f"[MISSING] {header}")

    except:
        print("[ERROR] Could not connect")

# Checks if important HTTP security headers are present.

def check_common_paths(url):
    print("\n[+] Checking common paths")

    for path in ["/admin", "/login", "/.git", "/backup"]:
        try:
            full = url + path
            r = requests.get(full, timeout=3)
            if r.status_code == 200:
                print(f"[FOUND] {full}")
        except:
            pass

# Looks for sensitive or common directories on a web server.

def main():
    target = input("Target (IP/domain): ").strip() # Get target input
    url = f"http://{target}:8000" # Set base URL

    ports = range(1, 1025) # Define port range

    open_ports = scan_ports(target, ports)

    print("\n[+] Banner grabbing...")
    for port in open_ports:
        grab_banner(target, port)

    check_headers(url)
    check_common_paths(url)


if __name__ == "__main__":
    main()
