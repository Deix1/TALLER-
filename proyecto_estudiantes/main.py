from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    obtener_promedio, materias_ofertadas, estudiantes_en_comun
)


def esperar():
    input("\nPresione Enter para seguir...")


def mostrar_mensaje(correcto, texto):
    if correcto:
        imprimir_exito(texto)
    else:
        imprimir_error(texto)


def solicitar_id(mensaje="Ingrese el ID del estudiante: "):
    try:
        return int(input(mensaje))
    except ValueError:
        imprimir_error("El ID debe ser un número entero")
        return None


def imprimir_tabla(lista):
    print(f"{'ID':<5}{'NOMBRE':<25}{'CORREO':<28}{'CARNET':<15}{'PROMEDIO':<10}")
    print("-" * 83)

    for alumno in lista:
        promedio = alumno.obtener_promedio()

        print(
            f"{alumno.id:<5}"
            f"{alumno.obtener_nombre_completo():<25}"
            f"{alumno.email:<28}"
            f"{alumno.carnet:<15}"
            f"{promedio:<10.2f}"
        )

    print("-" * 83)
    imprimir_info(f"Cantidad total: {len(lista)} estudiante(s)")


def crear_opcion():
    imprimir_titulo("REGISTRAR ESTUDIANTE")

    informacion = {}

    for campo in CAMPOS_ESTUDIANTE:
        informacion[campo] = input(
            f"Ingrese {campo.capitalize()}: "
        )

    correcto, mensaje = crear_estudiante(informacion)

    mostrar_mensaje(correcto, mensaje)
    esperar()


def mostrar_todos():
    imprimir_titulo("ESTUDIANTES REGISTRADOS")

    lista = obtener_todos()

    if not lista:
        imprimir_info("No existen estudiantes registrados todavía.")
    else:
        imprimir_tabla(lista)

    esperar()


def buscar_opcion():
    imprimir_titulo("CONSULTAR ESTUDIANTE")

    busqueda = input("Ingrese nombre, apellido, correo o carnet: ")

    resultados = buscar_estudiantes(busqueda)

    if not resultados:
        imprimir_info("No se encontraron coincidencias.")
    else:
        imprimir_tabla(resultados)

    esperar()


def consultar_por_id():
    imprimir_titulo("CONSULTAR POR ID")

    codigo = solicitar_id()

    if codigo is None:
        esperar()
        return

    alumno = obtener_por_id(codigo)

    if alumno is None:
        imprimir_error(f"No se encontró ningún estudiante con ID {codigo}")
    else:
        informacion = alumno.a_diccionario()

        for campo, valor in informacion.items():
            print(f"  {campo.capitalize()}: {valor}")

    esperar()


def modificar_opcion():
    imprimir_titulo("MODIFICAR INFORMACIÓN")

    codigo = solicitar_id()

    if codigo is None:
        esperar()
        return

    alumno = obtener_por_id(codigo)

    if alumno is None:
        imprimir_error(f"No se encontró ningún estudiante con ID {codigo}")
        esperar()
        return

    print("Deje vacío cualquier campo que desee conservar.\n")

    informacion = alumno.a_diccionario()
    modificaciones = {}

    for campo in CAMPOS_ESTUDIANTE:
        nuevo_valor = input(
            f"{campo.capitalize()} [{informacion[campo]}]: "
        ).strip()

        if nuevo_valor:
            modificaciones[campo] = nuevo_valor

    correcto, mensaje = actualizar_estudiante(
        codigo,
        modificaciones
    )

    mostrar_mensaje(correcto, mensaje)
    esperar()


def eliminar_opcion():
    imprimir_titulo("BORRAR ESTUDIANTE")

    codigo = solicitar_id()

    if codigo is None:
        esperar()
        return

    alumno = obtener_por_id(codigo)

    if alumno is None:
        imprimir_error(f"No se encontró ningún estudiante con ID {codigo}")
        esperar()
        return

    imprimir_info(
        f"Estudiante seleccionado: {alumno.obtener_nombre_completo()}"
    )

    if confirmar("¿Desea confirmar esta eliminación?"):
        correcto, mensaje = eliminar_estudiante(codigo)
        mostrar_mensaje(correcto, mensaje)
    else:
        imprimir_info("La operación fue cancelada.")

    esperar()


def registrar_nota_opcion():
    imprimir_titulo("REGISTRAR CALIFICACIÓN")

    codigo = solicitar_id()

    if codigo is None:
        esperar()
        return

    asignatura = input("Ingrese la materia: ")
    calificacion = input(
        "Ingrese la nota de 0 a 20 (ejemplo: 18.5): "
    )

    correcto, mensaje = agregar_nota(
        codigo,
        asignatura,
        calificacion
    )

    mostrar_mensaje(correcto, mensaje)
    esperar()


def consultar_promedio():
    imprimir_titulo("CONSULTAR PROMEDIO")

    codigo = solicitar_id()

    if codigo is None:
        esperar()
        return

    correcto, mensaje = obtener_promedio(codigo)

    mostrar_mensaje(correcto, mensaje)

    if correcto:
        alumno = obtener_por_id(codigo)

        for asignatura, calificaciones in alumno.notas.items():
            print(f"  {asignatura}: {calificaciones}")

    esperar()


def comparar_materias():
    imprimir_titulo("COMPARAR MATERIAS")

    primer_id = solicitar_id(
        "ID del primer estudiante: "
    )

    if primer_id is None:
        esperar()
        return

    segundo_id = solicitar_id(
        "ID del segundo estudiante: "
    )

    if segundo_id is None:
        esperar()
        return

    correcto, resultado = estudiantes_en_comun(
        primer_id,
        segundo_id
    )

    if not correcto:
        imprimir_error(resultado)

    elif not resultado:
        imprimir_info(
            "No existen materias compartidas entre los estudiantes."
        )

    else:
        for asignatura in sorted(resultado):
            print(f"  - {asignatura}")

    esperar()


def mostrar_materias():
    imprimir_titulo("ASIGNATURAS REGISTRADAS")

    lista_materias = materias_ofertadas()

    if not lista_materias:
        imprimir_info(
            "Todavía no existen materias registradas."
        )
    else:
        for asignatura in sorted(lista_materias):
            print(f"  - {asignatura}")

    esperar()


def cerrar_programa():
    imprimir_info("¡Gracias por utilizar el sistema!")
    return "salir"


# DICCIONARIO de opciones: número -> (nombre mostrado, función)
MENU = {
    "1": ("Registrar estudiante", crear_opcion),
    "2": ("Mostrar estudiantes", mostrar_todos),
    "3": ("Buscar estudiante", buscar_opcion),
    "4": ("Consultar por ID", consultar_por_id),
    "5": ("Modificar estudiante", modificar_opcion),
    "6": ("Borrar estudiante", eliminar_opcion),
    "7": ("Registrar calificación", registrar_nota_opcion),
    "8": ("Consultar promedio", consultar_promedio),
    "9": ("Comparar materias", comparar_materias),
    "10": ("Mostrar materias", mostrar_materias),
    "0": ("Cerrar programa", cerrar_programa),
}


def menu_principal():
    imprimir_titulo("GESTIÓN ACADÉMICA DE ESTUDIANTES")

    for numero, (descripcion, funcion) in MENU.items():
        print(f"  {numero}. {descripcion}")

    print()


def ejecutar():
    while True:
        menu_principal()

        seleccion = input(
            "Seleccione una alternativa: "
        ).strip()

        if seleccion not in MENU:
            imprimir_error("La opción seleccionada no es válida.")
            esperar()
            continue

        descripcion, accion = MENU[seleccion]

        try:
            if accion() == "salir":
                break

        except (ValueError, OSError) as error:
            imprimir_error(
                f"No fue posible realizar la operación: {error}"
            )
            esperar()


if __name__ == "__main__":
    try:
        ejecutar()
    except KeyboardInterrupt:
        print("\nEl programa fue detenido por el usuario.")