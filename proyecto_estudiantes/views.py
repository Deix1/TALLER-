from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido, normalizar_materia


administrador = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración: fijas, nadie las modifica durante la ejecución
CAMPOS_REQUERIDOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_DE_BUSQUEDA = ("nombre", "apellido", "email", "carnet")


def obtener_carnets(excepto_id=None):
    lista_carnets = set()
    for registro in administrador.leer():
        if registro["id"] != excepto_id:
            lista_carnets.add(registro["carnet"].strip().lower())
    return lista_carnets


def generar_id():
    id_mayor = 0
    for registro in administrador.leer():
        if registro["id"] > id_mayor:
            id_mayor = registro["id"]
    return id_mayor + 1


def comprobar_datos(datos, excepto_id=None):
    for campo in CAMPOS_REQUERIDOS:
        if datos[campo] == "":
            return False, f"El campo {campo} es requerido"

    if not es_email_valido(datos["email"]):
        return False, "El correo electrónico no tiene un formato válido"

    if " " in datos["email"]:
        return False, "El correo electrónico no puede contener espacios"

    if datos["carnet"].lower() in obtener_carnets(excepto_id):
        return False, "El carnet ingresado ya se encuentra registrado"

    return True, "Información válida"


def registrar_estudiante(datos):
    informacion = {}

    for campo in CAMPOS_ESTUDIANTE:
        informacion[campo] = str(datos.get(campo, "")).strip()

    correcto, mensaje = comprobar_datos(informacion)

    if not correcto:
        return False, mensaje

    alumno = Estudiante(
        generar_id(),
        informacion["nombre"],
        informacion["apellido"],
        informacion["email"],
        informacion["carnet"],
    )

    # Se agrega el estudiante a la lista y se almacena
    registros = administrador.leer()
    registros.append(alumno.a_diccionario())

    if not administrador.guardar(registros):
        return False, "No fue posible escribir en el archivo"

    return True, f"Estudiante registrado con id {alumno.id}"


def listar_estudiantes():
    lista_estudiantes = []

    for registro in administrador.leer():
        lista_estudiantes.append(
            Estudiante.desde_diccionario(registro)
        )

    return lista_estudiantes


def consultar_por_id(id_estudiante):
    for alumno in listar_estudiantes():
        if alumno.id == id_estudiante:
            return alumno

    return None


def localizar_estudiantes(termino):
    termino = termino.strip().lower()
    resultados = []

    if termino == "":
        return resultados

    for alumno in listar_estudiantes():
        informacion = alumno.a_diccionario()

        for campo in CAMPOS_DE_BUSQUEDA:
            if termino in informacion[campo].lower():
                resultados.append(alumno)
                break

    return resultados


def modificar_estudiante(id_estudiante, cambios):
    registros = administrador.leer()

    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:

            if not cambios:
                return False, "No se especificaron cambios"

            datos_actualizados = registro.copy()

            for campo in cambios:
                if campo not in CAMPOS_ESTUDIANTE:
                    return False, f"El campo {campo} no puede ser modificado"

                datos_actualizados[campo] = str(cambios[campo]).strip()

            correcto, mensaje = comprobar_datos(
                datos_actualizados,
                id_estudiante
            )

            if not correcto:
                return False, mensaje

            alumno = Estudiante.desde_diccionario(datos_actualizados)
            registros[indice] = alumno.a_diccionario()

            if not administrador.guardar(registros):
                return False, "No fue posible guardar los cambios"

            return True, f"Estudiante {id_estudiante} modificado correctamente"

    return False, f"No se encontró un estudiante con id {id_estudiante}"


def borrar_estudiante(id_estudiante):
    registros = administrador.leer()
    registros_restantes = []
    encontrado = False

    for registro in registros:
        if registro["id"] == id_estudiante:
            encontrado = True
        else:
            registros_restantes.append(registro)

    if not encontrado:
        return False, f"No se encontró un estudiante con id {id_estudiante}"

    if not administrador.guardar(registros_restantes):
        return False, "No fue posible guardar la eliminación"

    return True, f"Estudiante {id_estudiante} eliminado correctamente"


def registrar_nota(id_estudiante, materia, nota):
    alumno = consultar_por_id(id_estudiante)

    if alumno is None:
        return False, f"No se encontró un estudiante con id {id_estudiante}"

    materia = normalizar_materia(materia)

    if materia == "":
        return False, "Debe ingresar una materia"

    try:
        nota = float(str(nota).strip())
    except ValueError:
        return False, "La nota debe ser un número entre 0 y 20"

    if not (0 <= nota <= 20):
        return False, "La nota debe encontrarse entre 0 y 20"

    alumno.agregar_nota(materia, nota)

    registros = administrador.leer()

    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[indice] = alumno.a_diccionario()
            break

    if not administrador.guardar(registros):
        return False, "No fue posible guardar la calificación"

    return True, f"Calificación {nota:g} registrada en {materia}"


def consultar_promedio(id_estudiante):
    alumno = consultar_por_id(id_estudiante)

    if alumno is None:
        return False, f"No se encontró un estudiante con id {id_estudiante}"

    promedio = alumno.obtener_promedio()

    return True, (
        f"Promedio de {alumno.obtener_nombre_completo()}: "
        f"{promedio:.2f}"
    )


def listar_materias():
    materias = set()

    for alumno in listar_estudiantes():
        for materia in alumno.materias:
            materias.add(materia)

    return materias


def comparar_materias(id_a, id_b):
    alumno_a = consultar_por_id(id_a)
    alumno_b = consultar_por_id(id_b)

    if alumno_a is None or alumno_b is None:
        return False, "Uno o los dos estudiantes no existen"

    return True, alumno_a.materias_en_comun(alumno_b)