
# Aplicación Cliente-Servidor para Manipulación de Base de Datos

Este es un ejemplo básico de una aplicación Cliente-Servidor en Python que permite la manipulación de una base de datos SQLite a través de sockets.

## Instrucciones para ejecutar

### 1. Requisitos
- Python 3.x
- SQLite (incluido en Python por defecto)
- Conexión local (localhost) para la comunicación del servidor y cliente

### 2. Configuración del Servidor

El código del servidor utiliza `SQLite` para crear una base de datos y manipular una tabla de usuarios. Ejecuta el siguiente código en tu máquina:

```python
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
```

### 3. Configuración del Cliente

El cliente se conecta al servidor para enviar solicitudes de inserción de usuarios o lectura de los usuarios existentes. Usa el siguiente código para ejecutar el cliente:

```python
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
```

### 4. Ejecución
1. Ejecuta primero el servidor en una terminal o consola para que esté listo para recibir conexiones.
2. Luego, ejecuta el cliente en otra terminal para conectarte al servidor.
3. El cliente te permitirá insertar usuarios o leer todos los usuarios almacenados en la base de datos.

### 5. Explicación del funcionamiento
- **Servidor**: Escucha en el puerto `12345` y manipula la base de datos `SQLite`. El servidor puede procesar comandos para insertar usuarios o leer los datos existentes.
- **Cliente**: Envía comandos al servidor para realizar operaciones como insertar un usuario (nombre y edad) o leer los datos de los usuarios.

