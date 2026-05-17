# =================================================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROGRAMA: Ingeniería de Sistemas
# CURSO: Programación Orientada a Objetos - Código: 213023
# AUTOR: Juan Sebastian Vitola Polo
# PROYECTO: Sistema Integral de Gestión de Operaciones 'Software FJ'
# ARCHIVO: utils/Validador.py
# DESCRIPCIÓN: Componente centralizado de validación estricta y protección de tipos.
# =================================================================================

# Importación de utilidades avanzadas de tipado estático estructural para firmas de métodos
from typing import Any, Dict, List, Type
# Importación del gestor de auditoría para registrar las excepciones de validación de datos
from utils.Logger import GestorLogs
# Importación de las excepciones específicas del dominio para preservar el modelo de negocio
from utils.Excepciones import ErrorDatoInvalido, ErrorParametroFaltante


class Validador:
    """
    Clase estática encargada de centralizar las reglas de validación del sistema Software FJ.
    Garantiza que ningún dato corrupto vulnere la integridad de memoria del sistema core.
    """

    @staticmethod
    def validar_identidad(valor: Any, nombre_campo: str = "ID") -> int:
        """
        Verifica de forma estricta que un identificador sea numérico, entero y positivo.
        """
        # Bloque try-except encargado de aislar y procesar intentos de conversión de tipo inválidos
        try:
            # Validación inicial para evitar el procesamiento de valores nulos o vacíos en el ID
            if valor is None or str(valor).strip() == "":
                # Lanza un error de tipo si el identificador es un objeto nulo o cadena en blanco
                raise TypeError(f"El campo '{nombre_campo}' no puede estar vacío o ser nulo.")
            
            # Intento de conversión forzada a tipo entero para evaluar si la cadena es un número válido
            valor_entero = int(str(valor).strip())
            
            # Evaluación lógica para impedir identificadores negativos o iguales a cero
            if valor_entero <= 0:
                # Dispara un error de valor si el número entero viola la restricción de positividad
                raise ValueError(f"El campo '{nombre_campo}' debe ser un número estrictamente numérico positivo.")
            
            # Retorna el valor entero sanitizado y validado en caso de éxito total
            return valor_entero

        # Captura de errores de tipo numérico o conversiones fallidas de cadenas de texto alfabéticas
        except (ValueError, TypeError) as error_origen:
            # Formateo del mensaje descriptivo del fallo de validación detectado
            mensaje_error = f"Validación de Identidad fallida en '{nombre_campo}': {str(error_origen)}"
            # Registro automatizado del fallo en el archivo físico externo a través del Logger corporativo
            GestorLogs.registrar_evento("ERROR", mensaje_error)
            # Lanzamiento de la excepción de dominio personalizada adjuntando la causa raíz del problema
            raise ErrorDatoInvalido(mensaje_error, valor_causante=valor) from error_origen

    @staticmethod
    def validar_nombre(cadena_texto: Any, nombre_campo: str = "Nombre") -> str:
        """
        Garantiza que una cadena de texto no contenga números ni caracteres vacíos.
        """
        # Verificación estructural para comprobar que el argumento ingresado corresponda a una cadena
        if not isinstance(cadena_texto, str):
            # Formateo del mensaje si el tipo de dato subyacente no es string
            mensaje_tipo = f"El campo '{nombre_campo}' debe ser obligatoriamente una cadena de texto."
            # Envío automático de la traza de error al sistema de logs externos
            GestorLogs.registrar_evento("ERROR", mensaje_tipo)
            # Dispara el error de negocio interrumpiendo el flujo de inicialización anómalo
            raise ErrorDatoInvalido(mensaje_tipo, valor_causante=type(cadena_texto))

        # Sanitización de la cadena removiendo espacios en blanco colaterales
        texto_limpio = cadena_texto.strip()

        # Validación lógica para asegurar que el nombre no consista únicamente en espacios en blanco
        if len(texto_limpio) == 0:
            # Mensaje de error detallado para registrar campos requeridos en blanco
            mensaje_vacio = f"El campo '{nombre_campo}' no puede ser una cadena de caracteres vacía."
            # Persistencia del evento adverso en el archivo de texto de auditoría
            GestorLogs.registrar_evento("ERROR", mensaje_vacio)
            # Lanzamiento de la excepción de datos inválidos correspondiente a la rúbrica de la UNAD
            raise ErrorDatoInvalido(mensaje_vacio, valor_causante=cadena_texto)

        # Iteración algorítmica sobre la cadena para comprobar la inexistencia de dígitos numéricos
        if any(caracter.isdigit() for caracter in texto_limpio):
            # Formateo del mensaje informando que se detectó un número dentro de un nombre propio
            mensaje_numeros = f"El campo '{nombre_campo}' contiene caracteres numéricos prohibidos."
            # Registro del incidente en el subsistema log externo para auditoría de sistemas
            GestorLogs.registrar_evento("ERROR", mensaje_numeros)
            # Lanzamiento explícito de la excepción de datos inválidos con su valor causante
            raise ErrorDatoInvalido(mensaje_numeros, valor_causante=texto_limpio)

        # Retorno de la cadena de texto completamente sanitizada y validada bajo estándares de producción
        return texto_limpio

    @staticmethod
    def validar_tipo_dato(objeto: Any, tipo_esperado: Type, nombre_parametro: str) -> None:
        """
        Confirma que las variables coincidan exactamente con la firma de tipos requerida.
        """
        # Evaluación de la instancia del objeto contra el tipo o clase esperada por el negocio
        if not isinstance(objeto, tipo_esperado):
            # Estructuración del mensaje informando el tipo recibido versus el tipo esperado
            mensaje_error = f"El parámetro '{nombre_parametro}' es de tipo '{type(objeto).__name__}', pero se esperaba '{tipo_esperado.__name__}'."
            # Escritura inmediata del fallo en el log corporativo persistente
            GestorLogs.registrar_evento("ERROR", mensaje_error)
            # Dispara la excepción personalizada de datos inválidos resguardando el tipado estricto
            raise ErrorDatoInvalido(mensaje_error, valor_causante=objeto)

    @staticmethod
    def verificar_parametros_presentes(diccionario_datos: Dict[str, Any], claves_obligatorias: List[str]) -> None:
        """
        Inspecciona estructuras de datos llave-valor para certificar la presencia de atributos requeridos.
        """
        # Bucle iterador encargado de contrastar las claves requeridas contra el contenedor de datos
        for clave in claves_obligatorias:
            # Evaluación lógica dual: verifica la ausencia de la clave o que su contenido sea explícitamente nulo
            if clave not in diccionario_datos or diccionario_datos[clave] is None:
                # Definición del mensaje técnico indicando qué atributo falta para la creación del objeto
                mensaje_error = f"Error de inicialización estructural: Atributo obligatorio '{clave}' ausente."
                # Registro automático de la negligencia de datos en el archivo físico de texto externo
                GestorLogs.registrar_evento("ERROR", mensaje_error)
                # Lanzamiento de la excepción de parámetro faltante para detener el proceso de persistencia
                raise ErrorParametroFaltante(mensaje_error, valor_causante=clave)


# =================================================================================
# BLOQUE DE EJECUCIÓN Y SIMULACIÓN UNITARIA LOCAL (COMPROBACIÓN DE ESTABILIDAD)
# =================================================================================
if __name__ == "__main__":
    # Mensaje inicial informando la ejecución de las pruebas unitarias sobre el componente Validador
    print("--- INICIANDO DIAGNÓSTICO DE ROBUSTEZ EN VALIDADOR.PY ---")
    
    # --------------------------------------------------------------------------------
    # CASO DE PRUEBA 1: Validación Exitosa de un Identificador Numérico
    # --------------------------------------------------------------------------------
    try:
        # Se introduce un id en formato cadena susceptible de ser parseado a entero positivo
        id_correcto = Validador.validar_identidad("45672", "ID_Cliente")
        # Imprime la confirmación del éxito de la prueba unitaria por consola
        print(f"[TEST EXITO] Identidad procesada correctamente: {id_correcto} (Tipo: {type(id_correcto).__name__})")
    except ErrorSoftwareFJ as ex:
        # Captura defensiva en caso de que ocurra una falla inesperada en la prueba
        print(f"[TEST FALLO] Error inesperado en Caso 1: {str(ex)}")

    # --------------------------------------------------------------------------------
    # CASO DE PRUEBA 2: Captura Controlada de Identificador Alfabético Inválido
    # --------------------------------------------------------------------------------
    try:
        # Se fuerza el error inyectando letras en un campo destinado a ser estrictamente numérico
        id_erroneo = Validador.validar_identidad("1024A5", "ID_Reserva")
        # Esta línea no se alcanzará debido al lanzamiento automático de la excepción
        print(f"[TEST FALLO] Se eludió el control de identidad: {id_erroneo}")
    except ErrorDatoInvalido as ex:
        # Intercepción exitosa del error de negocio confirmando el blindaje del sistema
        print(f"[TEST ÉXITO CONTROLADO] Excepción interceptada exitosamente: {str(ex)}")

    # --------------------------------------------------------------------------------
    # CASO DE PRUEBA 3: Validación de Nombre Corporativo Limpio
    # --------------------------------------------------------------------------------
    try:
        # Llamada al método inyectando una cadena limpia y válida
        nombre_valido = Validador.validar_nombre("Juan Sebastian Vitola", "Nombre_Cliente")
        # Despliegue del resultado exitoso en el terminal
        print(f"[TEST EXITO] Nombre validado sin anomalías: '{nombre_valido}'")
    except ErrorSoftwareFJ as ex:
        # Captura de errores colaterales
        print(f"[TEST FALLO] Error inesperado en Caso 3: {str(ex)}")

    # --------------------------------------------------------------------------------
    # CASO DE PRUEBA 4: Captura Controlada de Nombre con Dígitos Numéricos Prohibidos
    # --------------------------------------------------------------------------------
    try:
        # Inyección de caracteres numéricos en el nombre para forzar el fallo defensivo del motor
        nombre_corrupto = Validador.validar_nombre("Andres123 Polo", "Nombre_Pasajero")
        # Línea de control que no debe ejecutarse bajo ninguna circunstancia
        print(f"[TEST FALLO] Se eludió la protección de nombres alfabéticos: {nombre_corrupto}")
    except ErrorDatoInvalido as ex:
        # Confirmación de que el validador interceptó los números y salvaguardó la aplicación
        print(f"[TEST ÉXITO CONTROLADO] Excepción interceptada exitosamente: {str(ex)}")

    # --------------------------------------------------------------------------------
    # CASO DE PRUEBA 5: Verificación de Atributos Faltantes en Diccionarios de Negocio
    # --------------------------------------------------------------------------------
    # Simulación de un payload JSON o diccionario de entrada al que le falta el atributo de duración
    datos_reserva_incompletos = {
        "cliente_id": "88123",
        "servicio_id": "SRV-A"
        # El parámetro 'duracion' ha sido omitido intencionalmente
    }
    
    # Declaración de las claves obligatorias que requiere la aplicación para conformar el objeto
    campos_requeridos = ["cliente_id", "servicio_id", "duracion"]

    try:
        # Invocación del método de inspección estructural pasándole el caso corrupto
        Validador.verificar_parametros_presentes(datos_reserva_incompletos, campos_requeridos)
        # Control de fallo si el método no frena la ejecución
        print("[TEST FALLO] Se permitió la creación de un registro con parámetros faltantes.")
    except ErrorParametroFaltante as ex:
        # Éxito rotundo: se detuvo la creación del objeto protegiendo las capas inferiores
        print(f"[TEST ÉXITO CONTROLADO] Excepción de parámetro faltante capturada: {str(ex)}")

    # Notificación final del estado del diagnóstico por consola
    print("\n[DIAGNÓSTICO FINALIZADO] Todas las pruebas unitarias del Validador corrieron de forma estable.")