#Supón un diccionario donde cada clave es una asignatura y el valor correspondiente una lista de estudiantes matriculados, tal como se muestra en el diccionario de ejemplo. Crea un programa que tenga un menú con tres opciones:
#Listar estudiantes matriculados en una asignatura
#Matricular un estudiante en una asignatura
#Dar de baja un estudiante de una asignatura.

asignaturas = {
    "Matemáticas": ["Ana", "Carlos", "Luis", "María", "Jorge"],
    "Física": ["Elena", "Luis", "Juan", "Sofía"],
    "Programación": ["Ana", "Carlos", "Sofía", "Jorge", "Pedro"],
    "Historia": ["María", "Juan", "Elena", "Ana"],
    "Inglés": ["Carlos", "Sofía", "Jorge", "María"],
}
while True:
    print("\nMenú:")
    print("1. Listar estudiantes matriculados en una asignatura")
    print("2. Matricular un estudiante en una asignatura")
    print("3. Dar de baja un estudiante de una asignatura")
    print("4. Salir")
    op = input("Elige una opción (1-4): ")

    match op:
        case "1":
            asig= input("Introduce el nombre de la asignatura: ")
            alumnos = asignaturas.get(asig)
            print(f"Estudiantes matriculados en {asig}:")
            for a in alumnos:
                print(a)
        case "2":
            alumno = input("Introduce el nombre del estudiante: ")
            asig = input("Introduce el nombre de la asignatura: ") 
            if asig in asignaturas:
                asignaturas[asig].append(alumno)
            else:
                asignaturas[asig] = [alumno]
        case "3":
            alumno = input("Introduce el nombre del estudiante: ")
            asig = input("Introduce el nombre de la asignatura: ")
            asignaturas[asig].remove(alumno)
        case _:
            salir = True
           