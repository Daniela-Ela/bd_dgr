#Dado un diccionario con claves como nombres de estudiantes y valores como una lista de calificaciones, haz un programa que:
#Cree un nuevo diccionario que contenga el promedio de calificaciones para cada estudiante
#Crea otro diccionario que contengan la nota promedio en cada asignatura
estudiantes = {
    "Ana": {"Matemáticas": 8.5, "Física": 9.0, "Programación": 7.8},
    "Carlos": {"Matemáticas": 9.2, "Física": 8.8, "Programación": 9.4},
    "Luis": {"Matemáticas": 7.6, "Física": 8.0, "Programación": 8.5},
    "María": {"Matemáticas": 9.5, "Física": 10.0, "Programación": 9.8},
    "Jorge": {"Matemáticas": 8.8, "Física": 8.4, "Programación": 7.9},
    "Sofía": {"Matemáticas": 9.1, "Física": 8.9, "Programación": 9.3}
}

# 1️ Promedio de calificaciones por estudiante
promedios_estudiantes = {}

for nombre, notas in estudiantes.items():
    promedio = sum(notas.values()) / len(notas)
    promedios_estudiantes[nombre] = round(promedio, 2)

print("Promedio de cada estudiante:\n")
for nombre, promedio in promedios_estudiantes.items():
    print(f"{nombre}: {promedio}")

# 2️ Promedio de cada asignatura
promedios_asignaturas = {}

# Recorremos todas las asignaturas y sumamos las notas
for notas in estudiantes.values():
    for materia, calificacion in notas.items():
        if materia not in promedios_asignaturas:
            promedios_asignaturas[materia] = []
        promedios_asignaturas[materia].append(calificacion)

# Calculamos el promedio final de cada materia
for materia in promedios_asignaturas:
    lista_notas = promedios_asignaturas[materia]
    promedio = sum(lista_notas) / len(lista_notas)
    promedios_asignaturas[materia] = round(promedio, 2)

print("\nPromedio en cada asignatura:\n")
for materia, promedio in promedios_asignaturas.items():
    print(f"{materia}: {promedio}")
