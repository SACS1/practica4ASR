from ftplib import FTP
import telnetlib

HOST = ["30.30.30.1", "192.168.100.2"]
FILES = ["startup-config1", "startup-config2"]
USER = "rcp"
PASSWORD = "rcp"

def pedirNumeroEntero():

    correcto = False
    num = 0
    while(not correcto):
        try:
            num = int(input("Introduzca un numero entero: "))
            correcto = True
        except ValueError:
            print("Error, introduzca un numero entero")

    return num

def listaEnrutadores():
    salir = False
    while not salir:
        print ("\nElige una opcion\n")

        print("1. Enrutador 1")
        print("2. Enrutador 2")
        print("3. Cancelar\n")

        opcion = pedirNumeroEntero()
        if opcion < 3:
            return opcion
        elif opcion == 3:
            return 3
        else:
            print ("Introduce un numero entre 1 y 4")


def cambiarHostName(opcion):
    hostname = input("Ingrese el nombre del hostname: ")
    setHostname = "hostname " + hostname + "\n"
    tn = telnetlib.Telnet()
    #tn = ""
    try:
        tn.open(HOST[opcion-1], 23)
    except:
        print("% S falló"% HOST[opcion-1])

    tn.read_until(b"User: ")
    tn.write(USER.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(PASSWORD.encode('ascii') + b"\n")
    #print(tn.read_all())
    print(tn.read_very_eager().decode('utf-8'))
    tn.write(b"en\n")
    tn.write(b"conf\n")
    tn.write(setHostname.encode('ascii'))
    tn.write(b"exit\n")
    tn.write(b"exit\n")
    tn.read_all()
    tn.close()

def crearStartup(opcion):
    tn = telnetlib.Telnet()
    #tn = ""
    try:
        tn.open(HOST[opcion-1], 23)
    except:
        print("% S falló"% HOST[opcion-1])
    tn.read_until(b"User: ")
    tn.write(USER.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(PASSWORD.encode('ascii') + b"\n")
    #print(tn.read_all())
    print(tn.read_very_eager().decode('utf-8'))
    tn.write(b"en\n")
    tn.write(b"copy running-config startup-config\n")
    tn.write(b"exit\n")
    tn.read_all()
    tn.close()

def extraerStartup(opcion):
    ftp = FTP()
    ftp.connect(HOST[opcion-1], 21)
    ftp.login(USER, PASSWORD)
    with open(FILES[opcion-1], 'wb') as local_file:
        response = ftp.retrbinary('RETR startup-config', local_file.write)
    if response.startswith('226'):
        print("Transferencia completa")
    else:
        print('Error de transferencia. El archivo puede estar incompleto o corrupto.')
    ftp.close()

def importarStartup(opcion):
    ftp = FTP()
    ftp.connect(HOST[opcion-1], 21)
    ftp.login(USER, PASSWORD)
    with open(FILES[opcion-1], 'rb') as local_file:
        ftp.storbinary('STOR startup-config', local_file)
    ftp.close()
    print("Transferencia completa")

salir = False
opcion = 0
while not salir:
    print ("\nElige una opcion\n")

    print("1. Cambiar hostname")
    print("2. Crear archivo de configuración")
    print("3. Extraer archivo de configuración")
    print("4. Importar archivo de configuración")
    print("5. Salir\n")

    opcion = pedirNumeroEntero()

    if opcion == 1:
        router = listaEnrutadores()
        if(router < 3):
            cambiarHostName(router)
    elif opcion == 2:
        router = listaEnrutadores()
        if(router < 3):
            crearStartup(router)
    elif opcion == 3:
        router = listaEnrutadores()
        if(router < 3):
            extraerStartup(router)
    elif opcion == 4:
        router = listaEnrutadores()
        if(router < 3):
            importarStartup(router)
    elif opcion == 5:
        salir = True
    else:
        print ("Introduce un numero entre 1 y 5")

print ("Fin")
