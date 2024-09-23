import socket
import sqlite3

# Configuración de la base de datos
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Crear una tabla
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Función para insertar datos en la base de datos
def insert_user(name, age):
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()

# Función para obtener todos los usuarios de la base de datos
def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Configuración del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Servidor escuchando en el puerto 12345...")

while True:
    client_socket, address = server_socket.accept()
    print(f"Conexión establecida con {address}")

    # Recibir solicitud del cliente
    data = client_socket.recv(1024).decode()
    command, *params = data.split(',')

    if command == 'INSERT':
        name, age = params
        insert_user(name, int(age))
        client_socket.sendall("Usuario insertado correctamente.".encode())
    elif command == 'READ':
        users = get_users()
        response = "\n".join([f"ID: {user[0]}, Nombre: {user[1]}, Edad: {user[2]}" for user in users])
        client_socket.sendall(response.encode())
    
    client_socket.close()
