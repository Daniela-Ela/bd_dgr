#Partiendo de un diccionario donde las claves son nombres de departamentos y los valores, diccionarios de empleados y sus puestos, tal como se ve en el código de ejemplo, crea un programa que permita realizar las siguientes funciones:
#Mostrar el listado de todos los empleados de un departamento
#Añadir un empleado a un departamento
#Eliminar un empleado de un departamento
departamentos = {
    "Recursos Humanos": {
        "Ana": "Gerente de Recursos Humanos",
        "Luis": "Especialista en Reclutamiento",
        "Elena": "Asistente de Recursos Humanos"
    },
    "Tecnología": {
        "Carlos": "Desarrollador Backend",
        "María": "Desarrolladora Frontend",
        "Pedro": "Administrador de Sistemas"
    },
    "Marketing": {
        "Sofía": "Directora de Marketing",
        "Jorge": "Especialista en SEO",
        "Laura": "Community Manager"
    },
    "Finanzas": {
        "Juan": "Analista Financiero",
        "Lucía": "Contadora",
        "Raúl": "Asesor Financiero"
    }
}

# Mostrar empleados de un departamento
depto = input("Escribe el nombre del departamento: ")
if depto in departamentos:
    print("Empleados en", depto)
    for nombre, puesto in departamentos[depto].items():
        print("-", nombre, ":", puesto)
else:
    print("Ese departamento no existe.")

# Añadir empleado
depto = input("\nDepartamento al que quieres añadir un empleado: ")
nombre = input("Nombre del empleado: ")
puesto = input("Puesto del empleado: ")

if depto not in departamentos:
    departamentos[depto] = {}
departamentos[depto][nombre] = puesto
print(nombre, "añadido al departamento", depto)

# Eliminar empleado
depto = input("\nDepartamento del empleado que quieres eliminar: ")
nombre = input("Nombre del empleado: ")

if depto in departamentos and nombre in departamentos[depto]:
    del departamentos[depto][nombre]
    print(nombre, "eliminado del departamento", depto)
else:
    print("No se encontró el empleado o el departamento.")
