# otp

Generador de contraseñas OTP
Este es un programa en Python que genera contraseñas temporales de un solo uso utilizando el algoritmo de contraseña basada en tiempo (TOTP). El programa utiliza una clave cifrada para generar las contraseñas, lo que garantiza que solo las personas autorizadas puedan generar contraseñas válidas.

Requisitos
El programa requiere Python 3 y las siguientes bibliotecas:

argparse: para procesar argumentos de línea de comandos
datetime: para manipular fechas y hora
hashlib: para realizar operaciones criptográficas
hmac: para generar códigos de autenticación de mensajes
cryptography: para cifrar y descifrar datos
Puedes instalar las bibliotecas utilizando pip:

# Code

pip install argparse datetime hashlib hmac cryptography

# Usage

El programa se puede ejecutar desde la línea de comandos con los siguientes argumentos:

python otp.py [-g KEY | -k FILE]
-g KEY: genera una nueva clave cifrada y la guarda en un archivo. KEY debe ser una cadena hexadecimal de al menos 64 caracteres.
-k FILE: utiliza una clave previamente generada en el archivo especificado. FILE debe ser el nombre del archivo que contiene la clave cifrada.
Si no se especifica ningún argumento, se mostrará el mensaje de ayuda.

# Funcionamiento
El programa consta de dos funciones principales:

generate_key(): genera una nueva clave cifrada y la guarda en un archivo.
generate_password(): genera y muestra una nueva contraseña temporal.
Generación de clave cifrada
Para generar una nueva clave cifrada, el programa utiliza la función generate_key(). Esta función toma una cadena hexadecimal de 64 caracteres como entrada y la convierte en una clave de 64 bytes. Luego, genera una clave de cifrado aleatoria utilizando la biblioteca cryptography.fernet y cifra la clave de 64 bytes utilizando la clave de cifrado aleatoria. Finalmente, guarda la clave de cifrado aleatoria y la clave cifrada en un archivo llamado ft_otp.key.

Generación de contraseña temporal
Para generar una nueva contraseña temporal, el programa utiliza la función generate_password(). Esta función lee la clave cifrada del archivo especificado en el argumento -k. Luego, utiliza la hora actual en formato UTC para calcular el código de tiempo de 30 segundos correspondiente. A continuación, utiliza la clave cifrada y el código de tiempo para generar un código HMAC utilizando la función hmac.new(). Finalmente, extrae los últimos 4 bytes del código HMAC y los convierte en un número de 6 dígitos utilizando una operación de módulo.

El programa verifica que la hora actual esté dentro del rango permitido para generar contraseñas temporales (entre las 08:00 y las 18:00 UTC). Si la hora actual está fuera de este rango, se muestra un mensaje de error y se sale de la función.

Ejemplo de uso
Para generar una nueva clave cifrada y guardarla en un archivo:

# Code

python otp.py -g 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
Para generar una nueva contraseña temporal utilizando una clave cifrada previamente generada:

# Code

python otp.py -k ft_otp.key
Notas adicionales
El programa utiliza la función signal.signal() para asociar la señal SIGINT con la función signal_handler(). Esto permite que el programa salga de forma segura cuando se presiona Ctrl+C.
