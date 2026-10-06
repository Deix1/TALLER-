from shared.herramientas import normalizar_materia


# TUPLA de información: los nombres y el orden permanecen establecidos.
# Es utilizada por el Controlador y la Vista para evitar repetir valores.
CAMPOS_ALUMNO = ("nombre", "apellido", "email", "carnet")


class Estudiante:
    """MODELO: contiene la información y funciones de un estudiante."""

    def __init__(self, codigo, nombre, apellido, correo, identificacion,
                 calificaciones=None, asignaturas=None):
        self.id = codigo
        self.nombre = nombre
        self.apellido = apellido
        self.email = correo
        self.carnet = identificacion

        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        self.notas = {}

        if calificaciones is not None:
            for asignatura, lista_calificaciones in calificaciones.items():
                asignatura = normalizar_materia(asignatura)

                if asignatura not in self.notas:
                    self.notas[asignatura] = []

                for calificacion in lista_calificaciones:
                    self.notas[asignatura].append(calificacion)

        # CONJUNTO: asignaturas registradas, evitando elementos repetidos
        self.materias = set()

        if asignaturas is not None:
            for asignatura in asignaturas:
                self.materias.add(normalizar_materia(asignatura))

        for asignatura in self.notas:
            self.materias.add(asignatura)

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def registrar_materia(self, asignatura):
        # add() evita duplicados si la materia ya se encuentra registrada
        self.materias.add(normalizar_materia(asignatura))

    def registrar_nota(self, asignatura, calificacion):
        asignatura = normalizar_materia(asignatura)
        self.registrar_materia(asignatura)

        if asignatura not in self.notas:
            self.notas[asignatura] = []

        self.notas[asignatura].append(calificacion)

    def calcular_promedio(self):
        suma = 0
        cantidad_notas = 0

        for grupo_notas in self.notas.values():
            for calificacion in grupo_notas:
                suma = suma + calificacion
                cantidad_notas = cantidad_notas + 1

        if cantidad_notas == 0:
            return 0

        return round(suma / cantidad_notas, 2)

    def asignaturas_compartidas(self, estudiante):
        # INTERSECCIÓN de conjuntos: materias que tienen ambos estudiantes
        return self.materias & estudiante.materias

    def convertir_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            # Los conjuntos se convierten en listas para poder guardarlos en JSON
            "materias": sorted(self.materias),
        }

    @classmethod
    def convertir_desde_diccionario(cls, informacion):
        return cls(
            informacion["id"],
            informacion["nombre"],
            informacion["apellido"],
            informacion["email"],
            informacion["carnet"],
            informacion.get("notas", {}),
            informacion.get("materias", []),
        )

    def __str__(self):
        return (f"[{self.carnet}] {self.nombre_completo()} "
                f"- Promedio: {self.calcular_promedio()}")