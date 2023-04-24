# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abelrodr <abelrodr@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/21 19:22:38 by abelrodr          #+#    #+#              #
#    Updated: 2023/04/24 12:09:55 by abelrodr         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import datetime
import hashlib
import hmac
import signal

from cryptography.fernet import Fernet

__author__ = "abelrodr"
__copyright__ = "Copyright 2023, Cybersec Bootcamp Malaga"
__credits__ = ["abelrodr"]
__email__ = "abelrodr42malaga@gmail.com"

print('''
_______/\\\\\_______/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\___        
 _____/\\\///\\\____\///////\\\/////__\/\\\/////////\\\_       
  ___/\\\/__\///\\\________\/\\\_______\/\\\_______\/\\\_      
   __/\\\______\//\\\_______\/\\\_______\/\\\\\\\\\\\\\/__     
    _\/\\\_______\/\\\_______\/\\\_______\/\\\/////////____    
     _\//\\\______/\\\________\/\\\_______\/\\\_____________   
      __\///\\\__/\\\__________\/\\\_______\/\\\_____________  
       ____\///\\\\\/___________\/\\\_______\/\\\_____________ 
        ______\/////_____________\///________\///______________                                     
                                                  
                    ,*,..*****.                   
                 *....,***********                
               **.****       ******.              
              ******           *****              
              *****             *****             
              *****             *****             
              *****             *****             
           ...*****............,*****..           
          *....***..............,***...,*         
          ********,.............,********         
          *******************************         
          **************(%/**************         
          ************(%%%%%*************         
          *************(%%#/*************         
          *************%%%%#*************         
          ************(((((((************         
          ******************************.         
                ,*****************,       
                
''')

# ===================== LIBRARY ======================= #

import argparse    # Módulo para procesar argumentos de línea de comandos
import datetime    # Módulo para manipular fechas y hora
import hashlib     # Módulo para realizar operaciones criptográficas 
import hmac        # Módulo para generar códigos de autenticación de mensajes
from cryptography.fernet import Fernet    # Módulo para cifrar y descifrar datos

# ===================== FUNCTIONS ====================== #

def is_valid_key(key):
    """Verifica si la clave cumple con los requisitos"""
    return len(key) >= 64 and all(c in '0123456789abcdefABCDEF' for c in key)

def generate_key():
    """Genera una nueva clave cifrada y la guarda en un archivo"""
    key = bytes.fromhex(args.generate)    # Convierte la cadena hexadecimal en bytes
    cipher_key = Fernet.generate_key()    # Genera una clave de cifrado aleatoria
    cipher = Fernet(cipher_key)           # Crea un objeto Fernet para cifrar y descifrar datos
    encrypted_key = cipher.encrypt(key)   # Cifra la clave de 64 bytes con la clave de cifrado aleatoria
    with open('ft_otp.key', 'wb') as f:   # Abre el archivo 'ft_otp.key' en modo binario para escribir datos
        f.write(cipher_key)               # Escribe la clave de cifrado aleatoria en el archivo
        f.write(encrypted_key)            # Escribe la clave cifrada en el archivo
    print(f'Se generó una nueva clave cifrada y se guardó en ft_otp.key')

def generate_password():
    """Genera y muestra una nueva contraseña temporal"""
    with open(args.keyfile, 'rb') as f:   # Abre el archivo de clave cifrada en modo binario para leer datos
        cipher_key = f.read(32)           # Lee los primeros 32 bytes del archivo, que corresponden a la clave de cifrado aleatoria
        encrypted_key = f.read()          # Lee el resto del archivo, que corresponde a la clave cifrada
        cipher = hmac.new(cipher_key, None, hashlib.sha1)    # Crea un objeto HMAC usando la clave de cifrado aleatoria
        while True:
            current_time = datetime.datetime.utcnow().replace(second=0, microsecond=0)    # Obtiene la hora actual en formato UTC
            if current_time.time() < datetime.time(8) or current_time.time() > datetime.time(18):    # Verifica si la hora actual está dentro del rango permitido para generar contraseñas temporales
                print("Error: La generación de contraseñas temporales solo está permitida entre las 08:00 y las 18:00 UTC")
                return
            time_code = (current_time - datetime.datetime(1970, 1, 1)).total_seconds() // 30    # Calcula el código de tiempo de 30 segundos correspondiente a la hora actual
            hmac_code = hmac.new(encrypted_key, int.to_bytes(int(time_code), 8, byteorder='big'), hashlib.sha1).digest()    # Calcula el código HMAC correspondiente al código de tiempo y la clave cifrada
            offset = hmac_code[19] & 0xf    # Extrae el último nibble del código HMAC
            password = ((hmac_code[offset] & 0x7f) << 24 |    # Convierte los siguientes 4 bytes del código HMAC en un número de 6 dígitos
                        (hmac_code[offset + 1] & 0xff) << 16 |
                        (hmac_code[offset + 2] & 0xff) << 8 |
                        (hmac_code[offset + 3] & 0xff)) % 1000000
            print(f'{password:06d}')    # Imprime la contraseña temporal
            while datetime.datetime.utcnow().replace(second=0, microsecond=0) == current_time:    # Espera hasta que cambie el código de tiempo
                return

def signal_handler(sig, frame): # Esto lo usamos para que no salgan trazas de error al interrumpir el programa.
    print('\nPrograma interrumpido por el usuario.')
    exit(0)

# ===================== PARSING/MAIN ===================== #

signal.signal(signal.SIGINT, signal_handler)
parser = argparse.ArgumentParser(description='Generador de contraseñas OTP')    # Crea un objeto ArgumentParser para procesar argumentos de línea de comandos
parser.add_argument('-g', '--generate', metavar='KEY', help='Generar una nueva clave cifrada y guardarla en un archivo')    # Agrega un argumento opcional para generar una nueva clave cifrada
parser.add_argument('-k', '--keyfile', metavar='FILE', help='Utilizar una clave previamente generada en el archivo especificado')    # Agrega un argumento opcional para utilizar una clave cifrada previamente generada
args = parser.parse_args()    # Analiza los argumentos de línea de comandos y almacena el resultado en un objeto Namespace

if args.generate:    # Si se especificó el argumento -g, generar una nueva clave cifrada
    if not is_valid_key(args.generate):
        print('Error: La clave debe ser una cadena hexadecimal de al menos 64 caracteres')
    else:
        generate_key()
elif args.keyfile:    # Si se especificó el argumento -k, generar una nueva contraseña temporal
    generate_password()
else:    # Si no se especificó ningún argumento, mostrar el mensaje de ayuda
    parser.print_help()



      
#
#   Creamos este script para que nos genere un codigo de 64 caracteres hexadecimal.
#
#   import secrets
#
#   key = secrets.token_hex(32)
#   while len(key) < 64:
#       key += secrets.token_hex(32)
#   key = key[:64]
#   print(key)
