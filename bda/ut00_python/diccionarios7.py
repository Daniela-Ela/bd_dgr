#Dado un diccionario de empleados y salarios, filtra e imprime solo los empleados con un salario mayor a un umbral definido.
empleados = {
    "Ana": 1800,
    "Luis": 2500,
    "Marta": 2200,
    "Carlos": 1500,
    "Sofía": 2700,
    "Javier": 1900
}

umbral = int(input("Introduce el salario mínimo (umbral): "))

print(f"\nEmpleados con salario mayor a {umbral}:\n")

for nombre, salario in empleados.items():
    if salario > umbral:
        print(f"{nombre}: {salario}")