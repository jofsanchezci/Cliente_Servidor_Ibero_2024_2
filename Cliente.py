import socket

# Función para enviar comandos al servidor
def send_request(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    client_socket.sendall(command.encode())
    response = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")
    client_socket.close()

# Menú para el cliente
while True:
    print("\n1. Insertar usuario")
    print("2. Leer usuarios")
    print("3. Salir")
    choice = input("Elija una opción: ")

    if choice == '1':
        name = input("Ingrese el nombre: ")
        age = input("Ingrese la edad: ")
        send_request(f"INSERT,{name},{age}")
    elif choice == '2':
        send_request("READ")
    elif choice == '3':
        break
    else:
        print("Opción no válida")
