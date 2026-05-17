# core/cliente.py

# Importación de la clase abstracta base desde el módulo core
from core.base_person import BasePerson
# Importación de las excepciones personalizadas requeridas para el manejo robusto de errores
from utils.exceptions import InvalidNameError, InvalidIdentificationError, MissingParameterError
# Importación de la función de logging para el registro auditable de fallos
from utils.logger import log_error

# Definición de la clase Cliente que hereda formalmente de la clase abstracta BasePerson
class Cliente(BasePerson):
    """
    Clase que representa a un Cliente dentro de la organización 'Software FJ'.
    Implementa encapsulamiento estricto, validaciones defensivas y trazabilidad de logs.
    """

    # Método constructor de la clase. Inicializa y valida las propiedades del cliente.
    def __init__(self, identification: str = None, name: str = None, contact: str = None):
        
        # Bloque try-except-else-finally estructurado para la captura del flujo de inicialización
        try:
            # Validación defensiva inicial: Verifica que ninguno de los parámetros requeridos sea nulo o vacío
            if not identification or not name or not contact:
                # Dispara una excepción personalizada si falta algún argumento obligatorio
                raise MissingParameterError("Todos los parámetros (identificación, nombre, contacto) son obligatorios.")

            # Asignación de atributos privados (encapsulamiento) utilizando los setters validados
            # El prefijo de doble guion bajo (__ ) activa el Name Mangling en Python para privacidad estricta
            self.__identification = self._validate_and_format_identification(identification)
            # Invoca la validación interna antes de asignar el nombre al estado privado
            self.__name = self._validate_and_format_name(name)
            # Asignación directa del contacto (puede extenderse su validación de la misma manera)
            self.__contact = contact.strip()

        # Captura específica de excepciones de validación de negocio
        except (MissingParameterError, InvalidNameError, InvalidIdentificationError) as error:
            # Registra de forma persistente o simulada el error capturado usando el logger del sistema
            log_error(f"Fallo en la creación del Cliente: {str(error)}")
            # Relanza la excepción para que la capa de presentación o controlador superior la maneje
            raise error
            
        # Bloque else: Se ejecuta únicamente si el bloque try no generó ninguna excepción
        else:
            # Imprime una confirmación técnica de que el objeto pasó los filtros de integridad de datos
            print(f"[SUCCESS] Objeto Cliente instanciado correctamente en memoria para: {name}")
            
        # Bloque finally: Se ejecuta siempre, garantizando la liberación o cierre de operaciones si aplica
        finally:
            # Nota académica de depuración que demuestra el ciclo de vida completo del bloque de control
            print("[INFO] Finalizado el proceso de evaluación del constructor del Cliente.")

    # --- MÉTODOS DE VALIDACIÓN INTERNA (MÉTODOS PRIVADOS / AUXILIARES) ---

    # Método estático auxiliar para validar el formato de la identificación
    @staticmethod
    def _validate_and_format_identification(identification: str) -> str:
        # Remueve espacios en blanco innecesarios en los extremos de la cadena
        clean_id = str(identification).strip()
        # Verifica si la cadena resultante se compone puramente de dígitos numéricos
        if not clean_id.isdigit():
            # Lanza excepción específica si se detectan caracteres no numéricos en la identificación
            raise InvalidIdentificationError(f"La identificación '{identification}' debe ser un valor numérico válido.")
        # Retorna el valor limpio y validado
        return clean_id

    # Método estático auxiliar para validar el formato del nombre
    @staticmethod
    def _validate_and_format_name(name: str) -> str:
        # Remueve espacios en blanco al inicio y al final de la cadena
        clean_name = str(name).strip()
        # Verifica que el nombre no esté vacío tras la limpieza
        if not clean_name:
            # Lanza un error si el parámetro string venía únicamente con espacios vacíos
            raise InvalidNameError("El nombre no puede estar vacío.")
        # Verifica mediante expresiones de caracteres que el nombre solo contenga letras y espacios
        # Reemplaza espacios temporales para validar caracteres alfabéticos puros
        if not clean_name.replace(" ", "").isalpha():
            # Lanza una excepción si se encuentran números o caracteres especiales en el nombre
            raise InvalidNameError(f"El nombre '{name}' es inválido. No se permiten números ni caracteres especiales.")
        # Retorna el nombre formateado limpiamente
        return clean_name

    # --- MÉTODOS PROPIEDAD (GETTERS Y SETTERS) PARA ENCAPSULAMIENTO ---

    # Decorador que expone el atributo de solo lectura para la identificación
    @property
    def identification(self) -> str:
        # Retorna de forma segura la variable privada encapsulada
        return self.__identification

    # Decorador que permite modificar el atributo privado bajo validación previa
    @identification.setter
    def identification(self, value: str) -> None:
        try:
            # Ejecuta la función de validación antes de realizar la mutación del estado
            self.__identification = self._validate_and_format_identification(value)
        except InvalidIdentificationError as error:
            # Reporta el intento fallido de modificación al sistema de logs
            log_error(f"Error al modificar identificación: {str(error)}")
            # Propaga el error para evitar estados corruptos en la aplicación
            raise error

    # Decorador que expone el atributo de solo lectura para el nombre del cliente
    @property
    def name(self) -> str:
        # Retorna de forma segura el valor de la variable privada protegida
        return self.__name

    # Decorador que permite la mutación controlada del nombre del cliente
    @name.setter
    def name(self, value: str) -> None:
        try:
            # Valida el nuevo nombre antes de alterar la propiedad privada del objeto
            self.__name = self._validate_and_format_name(value)
        except InvalidNameError as error:
            # Registra la infracción de las reglas de negocio en el logger corporativo
            log_error(f"Error al modificar nombre: {str(error)}")
            # Lanza el error para control del flujo de ejecución externo
            raise error

    # Decorador que expone el acceso al dato de contacto del cliente
    @property
    def contact(self) -> str:
        # Retorna el valor actual de la propiedad privada de contacto
        return self.__contact

    # Decorador que permite redefinir de manera segura el contacto del cliente
    @contact.setter
    def contact(self, value: str) -> None:
        if not value or not str(value).strip():
            # Registra el error en logs si el contacto que se intenta ingresar es nulo o vacío
            log_error("Intento de asignar un contacto vacío.")
            # Dispara la excepción correspondiente por falta de datos obligatorios
            raise MissingParameterError("El contacto no puede ser un campo vacío.")
        # Aplica el cambio limpiando espacios en blanco residuales si pasa el control
        self.__contact = str(value).strip()

    # --- MÉTODOS MÁGICOS / REPRESENTACIÓN ---

    # Método para dar una representación formal en cadena de la instancia de la clase
    def __repr__(self) -> str:
        # Retorna una cadena estructurada que describe el estado actual de la entidad Cliente
        return f"Cliente(ID='{self.__identification}', Nombre='{self.__name}', Contacto='{self.__contact}')"